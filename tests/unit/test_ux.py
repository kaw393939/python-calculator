import pytest
from calculator.commands import parse
from calculator.core import Calculator
from calculator.history import History
from calculator.operations import Registry


@pytest.fixture
def calculator():
    class Observer:
        def on_change(self, records):
            pass
    return Calculator(Registry.discover(lambda _: None, entries=[]), History((), Observer()))


def test_contextual_help(calculator):
    output = parse('help stddev').execute(calculator)
    assert 'ddof=0|1' in output
    assert 'sample' in output
    assert calculator.history == ()


def test_case_insensitive_and_typo(calculator):
    assert parse('ADD 2 3').execute(calculator) == '5'
    with pytest.raises(ValueError, match="Did you mean 'multiply'"):
        parse('multipy 2 3').execute(calculator)


@pytest.mark.parametrize('text,message', [
    ('add 2 three', "Operand 2 must be a finite number; received 'three'"),
    ('stddev 1 2 ddof=true', "Option 'ddof' must be a finite number"),
    ('add 1 nan', 'Operand 2 must be a finite number'),
    ('2 + 3', 'Use an operation name'),
])
def test_actionable_errors(text, message):
    with pytest.raises(ValueError, match=message):
        parse(text)


def test_completion_includes_plugins(calculator):
    from calculator.operations import Builtin
    from calculator.terminal import configure_editing
    calculator.registry.register(Builtin('square', 'Square', lambda x: x*x, 1))
    class Backend:
        __doc__ = 'libedit'
        def set_completer(self, completer):
            self.complete = completer
        def set_completer_delims(self, delimiters):
            self.delimiters = delimiters
        def parse_and_bind(self, binding):
            self.binding = binding
    backend = Backend()
    assert configure_editing(calculator.registry, backend)
    assert backend.complete('squ', 0) == 'square '
    assert backend.complete('squ', 1) is None
    assert backend.binding == 'bind ^I rl_complete'


def test_ans_resolves_latest_retained_history(calculator):
    with pytest.raises(ValueError, match='No previous result'):
        parse('multiply ans 2').execute(calculator)
    parse('add 2 3').execute(calculator)
    assert parse('multiply ans 2').execute(calculator) == '10'
    calculator.delete(calculator.history[-1].id)
    assert parse('add ans 1').execute(calculator) == '6'
    calculator.clear()
    with pytest.raises(ValueError, match='No previous result'):
        parse('add ans 1').execute(calculator)


def test_history_navigation_and_clear_guidance(calculator):
    for value in range(25):
        calculator.calculate('add', value, 1)
    output = parse('history').execute(calculator)
    assert 'Showing 20 of 25' in output
    output = parse('history last 2').execute(calculator)
    assert 'add 24 1' in output and 'add 22 1' not in output
    assert 'Showing 2 of 25' in output
    assert 'add 0 1' in parse('history all').execute(calculator)
    identifier = calculator.history[-1].id
    assert identifier in parse(f'history show {identifier[:8]}').execute(calculator)
    with pytest.raises(ValueError, match='25 records'):
        parse('history clear').execute(calculator)
    assert len(calculator.history) == 25


@pytest.mark.parametrize('text', ['history last 0', 'history last -1', 'history last many'])
def test_history_limit_validation(text):
    with pytest.raises(ValueError, match='positive integer'):
        parse(text)
