import pytest

from calculator.commands import CalculateCommand, ExitCommand, HistoryCommand, parse


@pytest.mark.parametrize('text', ['help x y', 'quit x', 'history delete',
    'add 1 no', 'stddev 1 ddof=0 ddof=1', 'stddev 1 ddof=0 2',
    'stddev 1 Bad=0', 'add 1 inf', 'add "', 'mean 1 x='])
def test_uat_03_12_invalid_syntax(text):
    with pytest.raises(ValueError):
        parse(text)


def test_parse_commands():
    assert parse('  ') is None
    assert isinstance(parse('quit'), ExitCommand)
    assert isinstance(parse('history'), HistoryCommand)
    parsed = parse('stddev -2 4 6 ddof=1')
    assert isinstance(parsed, CalculateCommand)
    assert parsed.args == (-2, 4, 6)
    assert parsed.kwargs == {'ddof': 1}


def test_uat_11_unique_compact_ids_and_timestamp():
    from calculator.history import Record
    from types import SimpleNamespace
    records = tuple(Record(identifier, '2026-09-28T12:34:56.123456+00:00',
                           'add', (1, 2), (), 3)
                    for identifier in ['12345678-1000-0000-0000-000000000000',
                                       '12345678-2000-0000-0000-000000000000'])
    output = HistoryCommand().execute(SimpleNamespace(history=records))
    assert '12345678-1' in output and '12345678-2' in output
    assert '2026-09-28 12:34:56' in output
    assert '.123456' not in output
    assert records[0].id not in output
