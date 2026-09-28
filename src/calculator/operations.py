"""Mathematical strategies and installed-plugin discovery."""
import re
import statistics
from collections.abc import Callable
from difflib import get_close_matches
from importlib.metadata import entry_points
from math import isfinite, prod
from numbers import Real
from typing import Protocol


class Operation(Protocol):
    name: str
    description: str
    usage: str

    def execute(self, *args: float, **kwargs: float) -> float: ...


def finite(value: object) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError("Expected a finite number")
    result = float(value)
    if not isfinite(result):
        raise ValueError("Expected a finite number")
    return result


class Builtin:
    """One configurable strategy; algorithms remain ordinary pure functions."""

    def __init__(self, name: str, description: str, function: Callable,
                 minimum: int = 2, options: bool = False):
        self.name, self.description, self.function = name, description, function
        self.minimum, self.options = minimum, options
        self.usage = f"{name} NUMBER" + (" NUMBER" if minimum == 2 else "") + " ..."
        if options:
            self.usage += " [ddof=0|1]"

    def execute(self, *args: float, **kwargs: float) -> float:
        if len(args) < self.minimum:
            raise ValueError(f"{self.name} requires at least {self.minimum} operand(s)")
        values = tuple(finite(value) for value in args)
        if kwargs and (not self.options or set(kwargs) != {"ddof"}):
            raise ValueError(f"Unsupported option for {self.name}")
        return finite(self.function(*values, **kwargs))


def subtract(*values: float) -> float:
    result = values[0]
    for value in values[1:]:
        result -= value
    return result


def divide(*values: float) -> float:
    result = values[0]
    for value in values[1:]:
        if value == 0:
            raise ValueError("Cannot divide by zero")
        result /= value
    return result


def stddev(*values: float, ddof: float = 0) -> float:
    if ddof not in (0, 1):
        raise ValueError("ddof must be 0 (population) or 1 (sample)")
    if len(values) <= ddof:
        raise ValueError("stddev requires more operands than ddof")
    return statistics.pstdev(values) if ddof == 0 else statistics.stdev(values)


def builtins() -> list[Operation]:
    return [
        Builtin("add", "Add two or more numbers", lambda *a: sum(a)),
        Builtin("subtract", "Subtract left to right", subtract),
        Builtin("multiply", "Multiply two or more numbers", lambda *a: prod(a)),
        Builtin("divide", "Divide left to right", divide),
        Builtin("mean", "Arithmetic mean", lambda *a: statistics.mean(a), 1),
        Builtin("median", "Middle value", lambda *a: statistics.median(a), 1),
        Builtin("stddev", "Population or sample standard deviation", stddev, 1, True),
    ]


class Registry:
    def __init__(self):
        self._operations: dict[str, Operation] = {}

    def register(self, operation: Operation) -> None:
        name = operation.name
        if not isinstance(name, str) or not re.fullmatch(r"[a-z][a-z0-9_]*", name):
            raise ValueError("Plugin name must be a lowercase identifier")
        if name in self._operations or name in {"help", "operations", "history", "exit", "quit"}:
            raise ValueError(f"Duplicate or reserved operation: {name}")
        if not all(isinstance(getattr(operation, attr, None), str)
                   and getattr(operation, attr).strip() for attr in ("description", "usage")):
            raise ValueError("Plugin requires description and usage")
        if not callable(getattr(operation, "execute", None)):
            raise ValueError("Plugin requires execute")
        self._operations[name] = operation

    def get(self, name: str) -> Operation:
        try:
            return self._operations[name]
        except KeyError:
            matches = get_close_matches(name, self._operations, n=1)
            hint = f" Did you mean '{matches[0]}'?" if matches else ''
            raise ValueError(f"Unknown operation '{name}'; type operations to list choices.{hint}") from None

    def all(self) -> tuple[Operation, ...]:
        return tuple(self._operations[name] for name in sorted(self._operations))

    @classmethod
    def discover(cls, warn: Callable[[str], None], entries=None) -> "Registry":
        registry = cls()
        for operation in builtins():
            registry.register(operation)
        if entries is None:
            entries = entry_points(group="python_calculator.operations")
        for entry in sorted(entries, key=lambda item: (item.name, item.value)):
            try:
                registry.register(entry.load()())
            except Exception as exc:
                warn(f"Skipped plugin {entry.name}: {exc}")
        return registry
