"""Local web adapter: the same commands, facade, plugins and CSV repository."""
import argparse
from dataclasses import asdict
import io
import os
from pathlib import Path
from threading import RLock

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
import pandas as pd
from pydantic import BaseModel, Field

from calculator.commands import CalculateCommand, parse
from calculator.core import Calculator
from calculator.history import History, PersistenceObserver
from calculator.operations import Registry
from calculator.storage import COLUMNS, CsvRepository, StorageError


class CalculationInput(BaseModel):
    command: str = Field(min_length=1, max_length=4096)


def create_app(history_path: Path | None = None, registry: Registry | None = None) -> FastAPI:
    path = history_path or Path(os.environ.get('CALCULATOR_HISTORY',
                                              '~/.python-calculator/web-history.csv'))
    repository = CsvRepository(path)
    warnings = []
    registry = registry or Registry.discover(warnings.append)
    calculator = Calculator(registry, History(repository.load(), PersistenceObserver(repository)))
    lock = RLock()
    app = FastAPI(title='Calculator Studio', version='0.2.0')
    app.state.calculator = calculator
    static = Path(__file__).parent / 'static'

    @app.middleware('http')
    async def same_origin(request: Request, call_next):
        if request.method in {'POST', 'DELETE'}:
            origin = request.headers.get('origin')
            if origin and origin != str(request.base_url).rstrip('/'):
                return JSONResponse({'detail': 'Cross-origin changes are not allowed'}, status_code=403)
        response = await call_next(request)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response

    @app.exception_handler(ValueError)
    async def invalid(request, exc):
        return JSONResponse({'detail': str(exc)}, status_code=400)

    @app.exception_handler(StorageError)
    async def storage_failure(request, exc):
        return JSONResponse({'detail': 'History could not be saved. No changes were applied.'},
                            status_code=503)

    @app.get('/api/operations')
    def operations():
        return {'operations': [dict(name=op.name, description=op.description, usage=op.usage)
                               for op in registry.all()], 'warnings': warnings}

    @app.get('/api/history')
    def history():
        with lock:
            return {'records': [asdict(record) for record in reversed(calculator.history)]}

    @app.post('/api/calculations', status_code=201)
    def calculate(body: CalculationInput):
        command = parse(body.command)
        if not isinstance(command, CalculateCommand):
            raise HTTPException(400, 'Enter a calculation, such as add 2 3')
        with lock:
            try:
                command.execute(calculator)
            except (ValueError, StorageError):
                raise
            except Exception as exc:
                raise HTTPException(400, f'Calculation failed: {exc}') from exc
            return asdict(calculator.history[-1])

    @app.delete('/api/history/{identifier}', status_code=204)
    def delete(identifier: str):
        with lock:
            calculator.delete(identifier)
        return Response(status_code=204)

    @app.delete('/api/history', status_code=204)
    def clear(confirm: bool = Query(False)):
        if not confirm:
            raise HTTPException(400, 'Confirm before clearing history')
        with lock:
            calculator.clear()
        return Response(status_code=204)

    @app.get('/api/history.csv')
    def export():
        import json
        with lock:
            rows = [dict(id=r.id, timestamp=r.timestamp, operation=r.operation,
                         args=json.dumps(r.args), kwargs=json.dumps(dict(r.options)), result=r.result)
                    for r in calculator.history]
            stream = io.StringIO()
            pd.DataFrame(rows, columns=COLUMNS).to_csv(stream, index=False)
        return Response(stream.getvalue(), media_type='text/csv',
                        headers={'Content-Disposition': 'attachment; filename="calculations.csv"'})

    @app.get('/', include_in_schema=False)
    def index():
        return FileResponse(static / 'index.html')

    app.mount('/static', StaticFiles(directory=static), name='static')
    return app


def main():
    import uvicorn
    parser = argparse.ArgumentParser(description='Open Calculator Studio at http://127.0.0.1:8000')
    parser.add_argument('--history', type=Path, help='CSV path (default: ~/.python-calculator/web-history.csv)')
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    uvicorn.run(create_app(args.history), host='127.0.0.1', port=args.port)
