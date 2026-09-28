"""Composition root and terminal entry point."""
import argparse
from pathlib import Path
import sys

from calculator.commands import ExitCommand, parse
from calculator.core import Calculator
from calculator.history import History, PersistenceObserver
from calculator.operations import Registry
from calculator.storage import CsvRepository


def run(calculator: Calculator, text: str) -> bool:
    command = parse(text)
    if command is not None:
        print(command.execute(calculator))
    return isinstance(command, ExitCommand)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description='Extensible calculator with automatic CSV history')
    parser.add_argument('--history', type=Path, default=Path.home() / '.python-calculator/history.csv')
    parser.add_argument('--command', help='Run one command and exit')
    options = parser.parse_args(argv)
    try:
        repository = CsvRepository(options.history)
        registry = Registry.discover(lambda message: print(f'Warning: {message}', file=sys.stderr))
        calculator = Calculator(registry, History(repository.load(), PersistenceObserver(repository)))
        if options.command is not None:
            run(calculator, options.command)
            return 0
        interactive = sys.stdin.isatty()
        if interactive:
            print(f'Calculator — type help for commands. History: {repository.path}')
        while True:
            try:
                text = input('calc> ' if interactive else '')
            except EOFError:
                return 0
            try:
                if run(calculator, text):
                    return 0
            except Exception as exc:
                print(f'Error: {exc}', file=sys.stderr)
    except KeyboardInterrupt:
        print('\nInterrupted.', file=sys.stderr)
        return 130
    except Exception as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 1
