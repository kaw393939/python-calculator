"""Application facade, independent of terminal and pandas."""
import re

from calculator.history import History, Record
from calculator.operations import Registry, finite


class Calculator:
    def __init__(self, registry: Registry, history: History):
        self.registry = registry
        self._history = history

    @property
    def history(self) -> tuple[Record, ...]:
        return self._history.records

    def calculate(self, name: str, *args: float, **kwargs: float) -> Record:
        if not all(re.fullmatch(r'[a-z][a-z0-9_]*', key) for key in kwargs):
            raise ValueError('Option names must be lowercase identifiers')
        args = tuple(finite(value) for value in args)
        kwargs = {key: finite(value) for key, value in kwargs.items()}
        result = finite(self.registry.get(name).execute(*args, **kwargs))
        record = Record.create(name, args, kwargs, result)
        self._history.replace((*self.history, record))
        return record

    def delete(self, identifier: str) -> None:
        matches = [r for r in self.history if identifier and r.id.startswith(identifier)]
        if len(matches) != 1:
            raise ValueError('History ID is unknown or ambiguous; use a longer ID from history')
        self._history.replace(tuple(r for r in self.history if r.id != matches[0].id))

    def clear(self) -> None:
        self._history.replace(())
