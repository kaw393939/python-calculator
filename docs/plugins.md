# Extending the calculator

A plugin is trusted Python code installed into the calculator's virtual environment.
It implements `name`, `description`, `usage`, and
`execute(self, *args: float, **kwargs: float) -> float`. It must return a finite
number and validate its arity and options, raising ValueError for user mistakes.
Use a lowercase identifier that does not collide with built-ins or CLI commands.

The distribution declares a no-argument class through an entry point:

```toml
[project.entry-points."python_calculator.operations"]
square = "calculator_square:Square"
```

Install the working example from the project root:

```sh
python -m pip install -e examples/square_plugin
calc --command 'square 4'
python -m pip uninstall calculator-square-example
```

Restart the calculator after installation or removal. `operations` lists the
available strategies and usage. Records remain readable after uninstalling their
plugin. Discovery errors warn and skip the offending plugin; plugins cannot replace
built-ins. A plugin execution error becomes a command error and creates no record.

Test algorithms in isolation and then register them with a Calculator backed by a
temporary CSV repository. Packaging entry point discovery deserves an integration
test as well: import success alone does not prove correct package metadata.
