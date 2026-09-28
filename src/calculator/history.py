"""Immutable history and synchronous persistence notifications."""
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Protocol
from uuid import uuid4


@dataclass(frozen=True)
class Record:
    id: str
    timestamp: str
    operation: str
    args: tuple[float, ...]
    options: tuple[tuple[str, float], ...]
    result: float

    @classmethod
    def create(cls, operation, args, kwargs, result):
        return cls(str(uuid4()), datetime.now(timezone.utc).isoformat(), operation,
                   tuple(args), tuple(sorted(kwargs.items())), result)


class HistoryRepository(Protocol):
    def load(self) -> tuple[Record, ...]: ...
    def save(self, records: tuple[Record, ...]) -> None: ...


class HistoryObserver(Protocol):
    def on_change(self, records: tuple[Record, ...]) -> None: ...


class PersistenceObserver:
    def __init__(self, repository: HistoryRepository):
        self.repository = repository

    def on_change(self, records: tuple[Record, ...]) -> None:
        self.repository.save(records)


class History:
    """Required observer persists proposed changes before they become visible."""

    def __init__(self, records: tuple[Record, ...], observer: HistoryObserver):
        self.records = records
        self.observer = observer

    def replace(self, records: tuple[Record, ...]) -> None:
        self.observer.on_change(records)
        self.records = records
