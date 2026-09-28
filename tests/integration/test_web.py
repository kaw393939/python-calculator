from concurrent.futures import ThreadPoolExecutor

from fastapi.testclient import TestClient
import pytest

from calculator.operations import Builtin, Registry
from calculator.web import create_app


@pytest.fixture
def client(tmp_path):
    registry = Registry.discover(lambda _: None, entries=[])
    registry.register(Builtin('square', 'Square a value', lambda x: x*x, 1))
    with TestClient(create_app(tmp_path/'web.csv', registry)) as client:
        yield client


def test_web_operations_and_assets(client):
    assert client.get('/').status_code == 200
    assert client.get('/static/app.js').status_code == 200
    operations = client.get('/api/operations').json()['operations']
    assert any(op['name'] == 'square' for op in operations)
    assert client.post('/api/calculations', json={'command': 'square 4'}).json()['result'] == 16


def test_web_calculate_reload_delete_export(client, tmp_path):
    first = client.post('/api/calculations', json={'command': 'add 2 3 4'})
    assert first.status_code == 201
    assert first.json()['result'] == 9
    assert client.post('/api/calculations', json={'command': 'multiply ans 2'}).json()['result'] == 18
    with TestClient(create_app(tmp_path/'web.csv')) as restarted:
        assert len(restarted.get('/api/history').json()['records']) == 2
    csv = client.get('/api/history.csv')
    assert 'attachment' in csv.headers['content-disposition']
    assert first.json()['id'] in csv.text
    assert client.delete('/api/history/'+first.json()['id']).status_code == 204
    assert len(client.get('/api/history').json()['records']) == 1
    assert client.delete('/api/history').status_code == 400
    assert client.delete('/api/history?confirm=true').status_code == 204
    assert client.get('/api/history').json()['records'] == []


@pytest.mark.parametrize('command', ['history clear --yes', 'help', 'divide 1 0',
    'add 2 bad', 'multiply ans 2', 'stddev 2 ddof=1', 'unknown 1 2', 'add 1 inf'])
def test_web_invalid_no_history(client, command):
    assert client.post('/api/calculations', json={'command': command}).status_code == 400
    assert client.get('/api/history').json()['records'] == []


def test_web_validation_origin_failure(client, monkeypatch):
    assert client.post('/api/calculations', json={}).status_code == 422
    assert client.post('/api/calculations', json={'command': 'add 1 2'},
                       headers={'Origin': 'https://other.example'}).status_code == 403
    def fail(*args):
        raise OSError('disk failure')
    monkeypatch.setattr('calculator.storage.os.replace', fail)
    assert client.post('/api/calculations', json={'command': 'add 1 2'}).status_code == 503
    assert client.get('/api/history').json()['records'] == []


def test_web_concurrent_requests_do_not_lose_records(client):
    with ThreadPoolExecutor(max_workers=4) as pool:
        statuses = list(pool.map(lambda i: client.post('/api/calculations',
                json={'command': f'add {i} 1'}).status_code, range(12)))
    assert statuses == [201]*12
    assert len(client.get('/api/history').json()['records']) == 12


def test_web_plugin_exception_does_not_commit(client):
    def fail(*args):
        raise RuntimeError('Plugin cannot calculate this')
    client.app.state.calculator.registry.register(Builtin('broken', 'Broken', fail))
    response = client.post('/api/calculations', json={'command': 'broken 1 2'})
    assert response.status_code == 400
    assert 'Plugin cannot calculate' in response.json()['detail']
    assert client.get('/api/history').json()['records'] == []
