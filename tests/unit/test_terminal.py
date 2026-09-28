from calculator.cli import main


def test_uat_13_interactive_banner_interrupt(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin.isatty', lambda: True)
    def interrupt(prompt):
        raise KeyboardInterrupt
    monkeypatch.setattr('builtins.input', interrupt)
    assert main(['--history', str(tmp_path / 'history.csv')]) == 130
    output = capsys.readouterr()
    assert 'type help' in output.out
    assert 'Interrupted' in output.err
