"""Parse terminal syntax into independently executable command objects."""
from dataclasses import dataclass
import re
import shlex
from typing import Protocol

from calculator.core import Calculator
from calculator.operations import finite

HELP = '''Commands:
  add|subtract|multiply|divide NUMBER NUMBER ...
  mean|median NUMBER ...
  stddev NUMBER ... [ddof=0|1]       0=population, 1=sample
  operations                       List all installed calculations
  history                          Show saved calculations
  history delete ID                Delete a full ID or unique prefix
  history clear --yes               Delete all history
  help                             Show this guide
  exit | quit                      Leave the calculator
Examples: add 2 3 4; stddev 2 4 6 ddof=1
Use one command per line. All numbers and options must be finite.'''


def number(value: float) -> str:
    return format(value, '.12g')


def table(headers, rows) -> str:
    rows = [[str(cell) for cell in row] for row in rows]
    widths = [max(len(header), *(len(row[i]) for row in rows))
              for i, header in enumerate(headers)]
    def line(row):
        return ' | '.join(cell.ljust(width) for cell, width in zip(row, widths)).rstrip()
    return '\n'.join([line(headers), '-+-'.join('-' * w for w in widths),
                      *(line(row) for row in rows)])


class Command(Protocol):
    def execute(self, calculator: Calculator) -> str: ...


@dataclass(frozen=True)
class CalculateCommand:
    name: str
    args: tuple[float, ...]
    kwargs: dict[str, float]

    def execute(self, calculator: Calculator) -> str:
        return number(calculator.calculate(self.name, *self.args, **self.kwargs).result)


@dataclass(frozen=True)
class HistoryCommand:
    action: str = 'list'
    identifier: str = ''

    def execute(self, calculator: Calculator) -> str:
        if self.action == 'delete':
            calculator.delete(self.identifier)
            return 'Calculation deleted.'
        if self.action == 'clear':
            calculator.clear()
            return 'History cleared.'
        if not calculator.history:
            return 'No calculations yet.'
        rows = []
        for record in calculator.history:
            expression = ' '.join([record.operation, *(number(v) for v in record.args),
                                   *(f'{k}={number(v)}' for k, v in record.options)])
            rows.append([record.id, record.timestamp, expression, number(record.result)])
        return table(['ID', 'Timestamp (UTC)', 'Calculation', 'Result'], rows)


@dataclass(frozen=True)
class InformationCommand:
    operations: bool = False

    def execute(self, calculator: Calculator) -> str:
        if self.operations:
            return table(['Operation', 'Description', 'Usage'],
                         [[op.name, op.description, op.usage] for op in calculator.registry.all()])
        return HELP


class ExitCommand:
    def execute(self, calculator: Calculator) -> str:
        return 'Goodbye.'


def parse(text: str) -> Command | None:
    tokens = shlex.split(text)
    if not tokens:
        return None
    name, *values = tokens
    if name in {'help', 'operations', 'exit', 'quit'}:
        if values:
            raise ValueError(f'{name} takes no arguments')
        if name in {'exit', 'quit'}:
            return ExitCommand()
        return InformationCommand(name == 'operations')
    if name == 'history':
        if not values:
            return HistoryCommand()
        if len(values) == 2 and values[0] == 'delete':
            return HistoryCommand('delete', values[1])
        if values == ['clear', '--yes']:
            return HistoryCommand('clear')
        raise ValueError('Usage: history | history delete ID | history clear --yes')
    args, kwargs = [], {}
    for token in values:
        if '=' in token:
            key, value = token.split('=', 1)
            if not re.fullmatch(r'[a-z][a-z0-9_]*', key) or key in kwargs:
                raise ValueError('Options must have unique lowercase names')
            kwargs[key] = finite(float(value))
        else:
            if kwargs:
                raise ValueError('Positional operands must come before named options')
            args.append(finite(float(token)))
    return CalculateCommand(name, tuple(args), kwargs)
