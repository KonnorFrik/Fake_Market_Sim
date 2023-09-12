__all__ = [
    "register",
    "handler",
]

import settings
from typing import Callable

_name_func_map = dict()
_name_doc_func = dict()


def register(func):
    _name_func_map[func.__name__] = func
    _name_doc_func[func.__name__] = func.__doc__
    return func


def handler(raw_command: str, obj_search: Callable):
    error_message = ""

    command_splitter = raw_command.split()
    command = command_splitter[0]
    args = command_splitter[1:] if len(command_splitter) > 1 else None

    try:
        obj = obj_search(args)
        _name_func_map[command](obj or args)

    except KeyError:
        error_message = settings.UNKNOWN_COMMAND_MESSAGE

    #except Exception as err:
        #error_message = f"Unknown error: '{err}'"

    return error_message


@register
def help(*a, **kw):
    """Show help message"""
    print()
    for name, doc in _name_doc_func.items():
        print(f"{name} -\t{doc}")

    print()


if __name__ == "__main__":
    while True:
        error_message = handler(input("~> "))
        print(error_message) if error_message else ...
