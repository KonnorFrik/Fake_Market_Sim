from typing import Any

from global_scope import global_vars
from all_commands import *
from user import User
from market import Market
from commands_handler import _name_func_map, handler, register # last in import section
import settings
#from trading_pairs import new_pairs

global_vars[settings.GLOBAL_USER_NAME] = User().load()
global_vars[settings.GLOBAL_MARKET_NAME] = Market().load()


def save_all():
    saved_count = 0

    for obj in global_vars.values():
        if "save" in dir(obj):
            if obj.save():
                saved_count += 1

    #print(f"Saved: {saved_count}/{len(global_vars.values())} objects")


@register
def new(choose = None, *a, **kw):
    """Create a new user or market
        Usage: new <user/market>"""

    if not choose:
        print("No argument")
        return

    if choose.lower() == settings.GLOBAL_USER_NAME:
        global_vars[settings.GLOBAL_USER_NAME] = User.new()

    elif choose.lower() == settings.GLOBAL_MARKET_NAME:
        global_vars[settings.GLOBAL_MARKET_NAME] = Market.new()

    else:
        print("Unknown argument")


@register
def quit(*a, code=0, **kw):
    """Exit from programm"""

    print(" Exit? [y/N]")

    if ask_bool():
        save_all()
        print("Bye")
        exit(code)


def get_obj(args):
    """Return object by his name for use as command argument"""

    if args and len(args) >= 1:
        name = args[0]
        return global_vars[name] if name in global_vars else None

    return None


def main():
    while True:
        try:
            user_input = input(settings.INPUT_PROMT)
            handler(user_input)

        except KeyboardInterrupt:
            quit(code=1)


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        save_all()
        exit(2)

    #except Exception:
        #save_all()
        #print("Found Unknown Error\nExit")
