"""Parse terminal syntax into independently executable command objects."""
from dataclasses import dataclass
from datetime import datetime
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
  history [last N | all]           Show recent (default 20) or all records
  history show ID                  Show full record details
  history delete ID                Delete a full ID or unique prefix
  history clear --yes               Delete all history
  help [OPERATION]                 Show guide or operation usage
  exit | quit                      Leave the calculator
Examples: add 2 3 4; stddev 2 4 6 ddof=1
Use ans as an operand to reuse the latest retained result.
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
    args: tuple[float | str, ...]
    kwargs: dict[str, float]

    def execute(self, calculator: Calculator) -> str:
        if 'ans' in self.args and not calculator.history:
            raise ValueError('No previous result; calculate something first')
        args = tuple(calculator.history[-1].result if value == 'ans' else value
                     for value in self.args)
        return number(calculator.calculate(self.name, *args, **self.kwargs).result)


@dataclass(frozen=True)
class HistoryCommand:
    action: str = 'list'
    identifier: str = ''
    limit: int | None = 20

    def execute(self, calculator: Calculator) -> str:
        if self.action == 'confirm':
            raise ValueError(f'This deletes {len(calculator.history)} records. '
                             'Use history clear --yes to confirm.')
        if self.action == 'show':
            record = calculator.find(self.identifier)
            return (f'ID: {record.id}\nTimestamp: {record.timestamp}\n'
                    f'Operation: {record.operation}\nArguments: {record.args}\n'
                    f'Options: {dict(record.options)}\nResult: {record.result}')
        if self.action == 'delete':
            calculator.delete(self.identifier)
            return 'Calculation deleted.'
        if self.action == 'clear':
            calculator.clear()
            return 'History cleared.'
        if not calculator.history:
            return 'No calculations yet.'
        rows = []
        identifiers = [record.id for record in calculator.history]
        prefix_length = 8
        while len({identifier[:prefix_length] for identifier in identifiers}) < len(identifiers):
            prefix_length += 1
        selected = calculator.history if self.limit is None else calculator.history[-self.limit:]
        for record in selected:
            expression = ' '.join([record.operation, *(number(v) for v in record.args),
                                   *(f'{k}={number(v)}' for k, v in record.options)])
            stamp = datetime.fromisoformat(record.timestamp).strftime('%Y-%m-%d %H:%M:%S')
            rows.append([record.id[:prefix_length], stamp, expression, number(record.result)])
        return table(['ID', 'Timestamp (UTC)', 'Calculation', 'Result'], rows) + (
            f'\nShowing {len(selected)} of {len(calculator.history)}. Use history all to see every record.'
            if len(selected) < len(calculator.history) else '')


@dataclass(frozen=True)
class InformationCommand:
    operations: bool = False
    topic: str = ""

    def execute(self, calculator: Calculator) -> str:
        if self.topic:
            operation = calculator.registry.get(self.topic)
            return f'{operation.name}: {operation.description}\nUsage: {operation.usage}'
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
    name = name.lower()
    if not re.fullmatch(r'[a-z][a-z0-9_]*', name):
        raise ValueError('Use an operation name, for example: add 2 3')
    if name == 'help' and len(values) == 1:
        return InformationCommand(topic=values[0].lower())
    if name in {'help', 'operations', 'exit', 'quit'}:
        if values:
            raise ValueError(f'{name} takes no arguments')
        if name in {'exit', 'quit'}:
            return ExitCommand()
        return InformationCommand(name == 'operations')
    if name == 'history':
        if not values:
            return HistoryCommand()
        if len(values) == 2 and values[0] in {'delete', 'show'}:
            return HistoryCommand(values[0], values[1])
        if values == ['all']:
            return HistoryCommand(limit=None)
        if values == ['clear']:
            return HistoryCommand('confirm')
        if len(values) == 2 and values[0] == 'last':
            if not values[1].isdigit() or int(values[1]) < 1:
                raise ValueError('History limit must be a positive integer')
            return HistoryCommand(limit=int(values[1]))
        if values == ['clear', '--yes']:
            return HistoryCommand('clear')
        raise ValueError('Usage: history | history delete ID | history clear --yes')
    args, kwargs = [], {}
    for token in values:
        if '=' in token:
            key, value = token.split('=', 1)
            if not re.fullmatch(r'[a-z][a-z0-9_]*', key) or key in kwargs:
                raise ValueError('Options must have unique lowercase names')
            kwargs[key] = numeric(value, f"Option {key!r}")
        else:
            if kwargs:
                raise ValueError('Positional operands must come before named options')
            args.append('ans' if token.lower() == 'ans' else numeric(token, f"Operand {len(args) + 1}"))
    return CalculateCommand(name, tuple(args), kwargs)


def numeric(token: str, label: str) -> float:
    try:
        return finite(float(token))
    except ValueError:
        raise ValueError(f"{label} must be a finite number; received {token!r}. "
                         "Example: add 2 3. Use help OPERATION for usage.") from None
