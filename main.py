from all_commands import *
from user import User
from commands_handler import _name_func_map, handler, register # last in import section
import settings

# table
# name: obj
# user.name: user_obj
_name_obj_map = dict()
_name_obj_map["user"] = User()


@register
def quit(*a, **kw):
    """Exit from programm"""
    print(" Exit? [y/N]")
    if (answ := input(settings.INPUT_PROMT).lower()) == "y" or answ == "yes":
        print("Bye")
        # save thing if need
        exit(1)


def get_obj(args: list): #None or Any
    if args and len(args) >= 1:
        name = args[0]
        return _name_obj_map[name] if name in _name_obj_map else None

    return None


def main():
    run = True

    while run:
        try:
            user_input = input(settings.INPUT_PROMT)
            message = handler(user_input, get_obj)
            print(message) if message else ...

        except KeyboardInterrupt:
            quit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # save things if need
        exit(2)
