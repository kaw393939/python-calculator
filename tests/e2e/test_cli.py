import os
from pathlib import Path
import subprocess
import sys

import pandas as pd
import pytest


def invoke(path, command=None, input=None, flags=()):
    args = [sys.executable, '-m', 'calculator', '--history', str(path), *flags]
    if command is not None:
        args += ['--command', command]
    env = os.environ.copy()
    # Isolate installed external plugins; tests use a clean metadata selection via
    # the built-in-only development environment (example is uninstalled after smoke).
    return subprocess.run(args, input=input, capture_output=True, text=True,
                          env=env, timeout=20)


def test_uat_01_02_04_08_13_repl(tmp_path):
    path = tmp_path / 'history.csv'
    result = invoke(path, input='\nhelp\noperations\nadd 2 3 4\nsubtract 20 5 3\n'
        'divide 100 2 5\nmean 1 2 6\nmedian 1 2 6\nstddev 2 4 6 ddof=1\n'
        'divide 1 0\nadd 7 8\nhistory\nexit\n')
    assert result.returncode == 0
    assert 'Cannot divide by zero' in result.stderr
    assert '\n9\n12\n10\n3\n2\n2\n15\n' in result.stdout
    assert 'Timestamp (UTC)' in result.stdout
    assert 'Goodbye.' in result.stdout
    assert len(pd.read_csv(path)) == 7
    restarted = invoke(path, 'history')
    assert 'stddev 2 4 6 ddof=1' in restarted.stdout
    assert invoke(path, input='').returncode == 0


@pytest.mark.parametrize('command', ['divide 1 0', 'add 1', 'add 1 NaN',
    'multiply 1e308 1e308', 'stddev 1 ddof=1', 'stddev 1 2 ddof=3',
    'mean 1 nope=1', 'missing 1 2', 'history clear', 'history delete bogus'])
def test_uat_03_05_12_14_bad_command(tmp_path, command):
    path = tmp_path / 'history.csv'
    result = invoke(path, command)
    assert result.returncode == 1
    assert 'Error:' in result.stderr
    assert not path.exists()


def test_uat_11_12_delete_clear(tmp_path):
    path = tmp_path / 'history.csv'
    assert invoke(path, 'add 1 2').returncode == 0
    identifier = pd.read_csv(path).iloc[0]['id']
    assert invoke(path, f'history delete {identifier[:8]}').returncode == 0
    assert invoke(path, 'history').stdout.strip() == 'No calculations yet.'
    invoke(path, 'multiply 2 3')
    before = path.read_bytes()
    assert invoke(path, 'history clear').returncode == 1
    assert before == path.read_bytes()
    assert invoke(path, 'history clear --yes').returncode == 0
    assert pd.read_csv(path).empty


def test_uat_09_corrupt_startup(tmp_path):
    path = tmp_path / 'history.csv'
    path.write_text('broken')
    result = invoke(path, 'add 1 2')
    assert result.returncode == 1
    assert 'Cannot load history' in result.stderr
    assert path.read_text() == 'broken'


def test_uat_14_flags_and_console_entrypoint(tmp_path):
    assert invoke(tmp_path/'h.csv', flags=['--bogus']).returncode == 2
    executable = Path(sys.executable).parent / 'calc'
    result = subprocess.run([str(executable), '--history', str(tmp_path/'h.csv'),
                             '--command', 'multiply 6 7'], capture_output=True, text=True)
    assert result.returncode == 0
    assert result.stdout.strip() == '42'
