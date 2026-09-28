from dataclasses import FrozenInstanceError, replace
import json

import pandas as pd
import pytest

from calculator.core import Calculator
from calculator.history import History, PersistenceObserver
from calculator.operations import Builtin, Registry
from calculator.storage import CsvRepository, StorageError


def make(path):
    repo = CsvRepository(path)
    return Calculator(Registry.discover(lambda _: None, entries=[]),
                      History(repo.load(), PersistenceObserver(repo)))


def test_uat_01_08_roundtrip(tmp_path):
    path = tmp_path / 'nested' / 'history.csv'
    calc = make(path)
    assert calc.history == ()
    record = calc.calculate('add', 2, 3, 4)
    calc.calculate('stddev', 2, 4, 6, ddof=1)
    assert record.result == 9
    assert make(path).history == calc.history
    with pytest.raises(FrozenInstanceError):
        record.result = 8


def test_uat_11_12_delete_clear(tmp_path):
    path = tmp_path / 'history.csv'
    calc = make(path)
    first = calc.calculate('add', 1, 2)
    calc.calculate('multiply', 3, 4)
    calc.delete(first.id[:8])
    assert len(make(path).history) == 1
    with pytest.raises(ValueError):
        calc.delete('missing')
    calc.clear()
    assert make(path).history == ()


@pytest.mark.parametrize('action', ['calculate', 'delete', 'clear'])
def test_uat_10_atomic_failure(tmp_path, monkeypatch, action):
    path = tmp_path / 'history.csv'
    calc = make(path)
    record = calc.calculate('add', 1, 2)
    before, contents = calc.history, path.read_bytes()
    def fail(*args):
        raise OSError('disk unavailable')
    monkeypatch.setattr('calculator.storage.os.replace', fail)
    with pytest.raises(StorageError, match='disk unavailable'):
        if action == 'calculate':
            calc.calculate('add', 3, 4)
        elif action == 'delete':
            calc.delete(record.id)
        else:
            calc.clear()
    assert calc.history == before
    assert path.read_bytes() == contents
    assert not list(tmp_path.glob('.calculator-*'))


@pytest.mark.parametrize('field,value', [
    ('id', 'bad'), ('timestamp', 'yesterday'), ('timestamp', '2026-01-01T00:00:00'),
    ('operation', 'bad name'), ('args', '{}'), ('args', '[true]'), ('args', '[NaN]'),
    ('kwargs', '[]'), ('kwargs', '{"bad key": 2}'), ('kwargs', '{'), ('result', 'inf'),
])
def test_uat_09_corrupt_records(tmp_path, field, value):
    path = tmp_path / 'history.csv'
    make(path).calculate('add', 1, 2)
    frame = pd.read_csv(path, dtype=str)
    frame.loc[0, field] = value
    frame.to_csv(path, index=False)
    contents = path.read_bytes()
    with pytest.raises(StorageError):
        make(path)
    assert path.read_bytes() == contents


@pytest.mark.parametrize('contents', ['', 'wrong,header\n',
    'id,timestamp,operation,args,kwargs,result\n1,2\n'])
def test_uat_09_corrupt_shape(tmp_path, contents):
    path = tmp_path / 'history.csv'
    path.write_text(contents)
    with pytest.raises(StorageError):
        make(path)


def test_uat_09_duplicate_ids(tmp_path):
    path = tmp_path / 'history.csv'
    make(path).calculate('add', 1, 2)
    frame = pd.read_csv(path)
    pd.concat([frame, frame]).to_csv(path, index=False)
    with pytest.raises(StorageError, match='duplicate'):
        make(path)


def test_uat_03_plugin_failure_and_nonfinite_results(tmp_path):
    calc = make(tmp_path / 'history.csv')
    calc.registry.register(Builtin('broken', 'Broken', lambda *a: float('inf')))
    with pytest.raises(ValueError):
        calc.calculate('broken', 1, 2)
    with pytest.raises(ValueError):
        calc.calculate('divide', 1, 0)
    assert calc.history == ()


def test_uat_08_uninstalled_plugin_record(tmp_path):
    path = tmp_path / 'history.csv'
    calc = make(path)
    calc.registry.register(Builtin('square', 'Square', lambda a: a*a, 1))
    calc.calculate('square', 4)
    assert make(path).history[0].result == 16


def test_uat_12_ambiguous_prefix(tmp_path):
    calc = make(tmp_path / 'history.csv')
    first = calc.calculate('add', 1, 2)
    second = replace(first, id=first.id[:8] + '-0000-0000-0000-000000000000')
    calc._history.records = (first, second)
    with pytest.raises(ValueError, match='ambiguous'):
        calc.delete(first.id[:8])
    assert len(calc.history) == 2


def test_csv_json_options(tmp_path):
    path = tmp_path / 'history.csv'
    make(path).calculate('stddev', 2, 4, 6, ddof=1)
    row = pd.read_csv(path).iloc[0]
    assert json.loads(row['kwargs']) == {'ddof': 1}
