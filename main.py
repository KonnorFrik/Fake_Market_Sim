import os
from typing import Any

from global_scope import global_vars
from all_commands import *
#from user import User
#from market import Market
#from session import Session
from commands_handler import _name_func_map, handler, register # last in import section
import settings



@register
def quit(*a, code=0, **kw):
    """Exit from programm"""

    print(" Exit? [y/N]")

    if ask_bool():
        save_all()
        print("Bye")
        exit(code)


#def get_obj(args):
    #"""Return object by his name for use as command argument"""
#
    #if args and len(args) >= 1:
        #name = args[0]
        #return global_vars[name] if name in global_vars else None
#
    #return None


def main():
    while True:
        try:
            user_input = input(settings.INPUT_PROMT)
            handler(user_input)

        except KeyboardInterrupt:
            quit(code=1)


if __name__ == "__main__":
    _abs_path = "/".join(os.path.abspath(__file__).split("/")[:-1])

    try:
        setup()
        _set_abs_path(_abs_path)
        check_dirs()
        print(f"Username: {global_vars[settings.GLOBAL_USER_NAME].name}\n")
        main()

    except KeyboardInterrupt:
        save_all()
        exit(2)

    except EOFError:
        save_all()
        exit(2)

    #except Exception:
        #save_all()
        #print("Found Unknown Error\nExit")
