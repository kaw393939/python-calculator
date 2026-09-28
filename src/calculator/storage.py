"""Strict pandas CSV adapter with atomic replacement."""
import csv
from datetime import datetime
import json
import os
from pathlib import Path
import re
import tempfile
from uuid import UUID

import pandas as pd

from calculator.history import Record
from calculator.operations import finite

COLUMNS = ['id', 'timestamp', 'operation', 'args', 'kwargs', 'result']


class StorageError(ValueError):
    pass


class CsvRepository:
    def __init__(self, path: Path):
        self.path = Path(path).expanduser()

    def load(self) -> tuple[Record, ...]:
        if not self.path.exists():
            return ()
        try:
            # pandas tolerates extra/missing fields in some cases; validate shape first.
            with self.path.open(newline='', encoding='utf-8') as handle:
                rows = csv.reader(handle, strict=True)
                if next(rows, None) != COLUMNS or any(len(row) != len(COLUMNS) for row in rows):
                    raise ValueError('Unexpected CSV columns or row width')
            frame = pd.read_csv(self.path, dtype=str, keep_default_na=False)
            records = []
            ids = set()
            for row in frame.to_dict('records'):
                identifier = str(UUID(row['id']))
                if identifier != row['id'] or identifier in ids:
                    raise ValueError('Invalid or duplicate ID')
                ids.add(identifier)
                stamp = datetime.fromisoformat(row['timestamp'])
                if stamp.utcoffset() is None or stamp.utcoffset().total_seconds() != 0:
                    raise ValueError('Timestamp must use UTC')
                if not re.fullmatch(r'[a-z][a-z0-9_]*', row['operation']):
                    raise ValueError('Invalid operation name')
                args, kwargs = json.loads(row['args']), json.loads(row['kwargs'])
                if not isinstance(args, list) or not isinstance(kwargs, dict):
                    raise ValueError('Invalid argument schema')
                if not all(re.fullmatch(r'[a-z][a-z0-9_]*', key) for key in kwargs):
                    raise ValueError('Invalid option name')
                records.append(Record(identifier, row['timestamp'], row['operation'],
                    tuple(finite(value) for value in args),
                    tuple(sorted((key, finite(value)) for key, value in kwargs.items())),
                    finite(float(row['result']))))
            return tuple(records)
        except Exception as exc:
            raise StorageError(f'Cannot load history {self.path}: {exc}') from exc

    def save(self, records: tuple[Record, ...]) -> None:
        temporary = None
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            rows = [dict(id=r.id, timestamp=r.timestamp, operation=r.operation,
                         args=json.dumps(r.args, allow_nan=False),
                         kwargs=json.dumps(dict(r.options), allow_nan=False), result=r.result)
                    for r in records]
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='',
                    dir=self.path.parent, prefix='.calculator-', suffix='.tmp', delete=False) as file:
                temporary = Path(file.name)
                pd.DataFrame(rows, columns=COLUMNS).to_csv(file, index=False)
                file.flush()
                os.fsync(file.fileno())
            os.replace(temporary, self.path)
        except Exception as exc:
            raise StorageError(f'Cannot save history {self.path}: {exc}') from exc
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
