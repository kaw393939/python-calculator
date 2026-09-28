import pytest

from calculator.commands import CalculateCommand, ExitCommand, HistoryCommand, parse


@pytest.mark.parametrize('text', ['help x', 'quit x', 'history clear', 'history delete',
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
