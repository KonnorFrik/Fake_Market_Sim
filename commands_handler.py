__all__ = [
    "register",
    "handler",
]

import settings

_name_func_map = dict()
_name_doc_func = dict()


def register(func):
    """Store functions and their doc_string for call them by name later"""

    _name_func_map[func.__name__] = func
    _name_doc_func[func.__name__] = func.__doc__

    return func


def handler(raw_command):
    """Process user command and call stored functions"""

    error_message = ""

    command_splitter = raw_command.split()
    command = command_splitter[0]
    args = command_splitter[1:] if len(command_splitter) > 1 else None

    try:
        _name_func_map[command](*args if args is not None else tuple())

    except KeyError:
        error_message = settings.UNKNOWN_COMMAND_MESSAGE

    return error_message


@register
def help(*a, **kw):
    """Show help message"""

    print()

    for name, doc in _name_doc_func.items():
        print(f"{name} -\t{doc}")

    print()

