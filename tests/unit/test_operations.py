from types import SimpleNamespace

import pytest

from calculator.operations import Builtin, Registry, finite


@pytest.fixture
def registry():
    return Registry.discover(lambda message: None, entries=[])


@pytest.mark.parametrize('name,args,kwargs,expected', [
    ('add', (2, 3, 4), {}, 9), ('subtract', (20, 5, 3), {}, 12),
    ('multiply', (-2, 3, 4), {}, -24), ('divide', (100, 2, 5), {}, 10),
    ('mean', (1, 2, 6), {}, 3), ('median', (1, 2, 6), {}, 2),
    ('median', (1, 4), {}, 2.5), ('stddev', (2, 4, 6), {'ddof': 1}, 2),
    ('stddev', (2, 4, 4, 4, 5, 5, 7, 9), {}, 2), ('stddev', (8,), {}, 0),
])
def test_uat_02_04_valid_operations(registry, name, args, kwargs, expected):
    assert registry.get(name).execute(*args, **kwargs) == pytest.approx(expected)


@pytest.mark.parametrize('name,args,kwargs', [
    ('add', (1,), {}), ('divide', (1, 0), {}), ('mean', (), {}),
    ('add', (1, float('nan')), {}), ('add', (1, float('inf')), {}),
    ('multiply', (1e308, 1e308), {}), ('add', (1, 2), {'ddof': 0}),
    ('stddev', (1,), {'ddof': 1}), ('stddev', (1, 2), {'ddof': 2}),
    ('stddev', (1, 2), {'unknown': 0}), ('divide', (1, 2), {'x': 2}),
])
def test_uat_03_05_invalid_operations(registry, name, args, kwargs):
    with pytest.raises(ValueError):
        registry.get(name).execute(*args, **kwargs)


@pytest.mark.parametrize('value', [True, '2', object(), float('-inf')])
def test_finite_contract(value):
    with pytest.raises(ValueError):
        finite(value)


def test_uat_06_07_discovery():
    warnings = []
    def entry(name, factory):
        return SimpleNamespace(name=name, value=name, load=lambda: factory)
    def good():
        return Builtin('square', 'Square', lambda x: x*x, 1)
    def broken():
        return 1/0
    registry = Registry.discover(warnings.append, [entry('square', good),
        entry('broken', broken), entry('add', lambda: Builtin('add', 'Collision', sum))])
    assert registry.get('square').execute(4) == 16
    assert registry.get('add').execute(1, 2) == 3
    assert len(warnings) == 2
    assert [op.name for op in registry.all()] == sorted(op.name for op in registry.all())


@pytest.mark.parametrize('changes', [
    {'name': 'Bad name'}, {'name': 'history'}, {'description': ''},
    {'usage': None}, {'execute': None},
])
def test_uat_07_invalid_metadata(changes):
    plugin = Builtin('test', 'Test', sum)
    for key, value in changes.items():
        setattr(plugin, key, value)
    with pytest.raises(ValueError):
        Registry().register(plugin)


def test_unknown_operation(registry):
    with pytest.raises(ValueError, match='Unknown operation'):
        registry.get('missing')
