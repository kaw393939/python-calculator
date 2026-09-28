"""Optional readline editing; piped commands remain plain text."""


def configure_editing(registry, backend=None):
    if backend is None:
        try:
            import readline as backend
        except ImportError:
            return False
    choices = sorted({op.name for op in registry.all()} |
                     {'help', 'operations', 'history', 'exit', 'quit', 'delete', 'clear', '--yes'})

    def complete(text, state):
        matches = [choice for choice in choices if choice.startswith(text.lower())]
        return matches[state] + ' ' if state < len(matches) else None

    backend.set_completer(complete)
    backend.set_completer_delims(' \t\n')
    backend.parse_and_bind('bind ^I rl_complete' if 'libedit' in (backend.__doc__ or '')
                           else 'tab: complete')
    # Command recall is session-local; calculation persistence stays in the CSV.
    return True
