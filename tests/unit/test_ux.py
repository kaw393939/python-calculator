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
