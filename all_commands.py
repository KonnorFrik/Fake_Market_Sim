__all__ = [
    "setup",
    "ask_bool",
    "check_dirs",
    "save_all",
    "_set_abs_path",
]


import os
import math
import random
from decimal import Decimal

import settings
from user import User
from market import Market
from session import Session
from global_scope import global_vars
from commands_handler import register

_abs_path = ""

def _set_abs_path(path):
    global _abs_path
    _abs_path = path


def how_many_perc(num1, num2):
    """ What percentage is 'num1' of 'num2' """
    koef = num2 / num1
    return 100 / koef


def perc_from(perc, num):
    """ What number corresponds to 'perc' percent of the 'num' """
    koef = num / 100
    return perc * koef


def setup(session = None, user = None, market = None):
    global_vars[settings.GLOBAL_SESSION_NAME] = Session() if not session else session
    global_vars[settings.GLOBAL_USER_NAME] = User().load(settings.DEFAULT_SESSION_DIR) if not user else user
    global_vars[settings.GLOBAL_MARKET_NAME] = Market().load(settings.DEFAULT_SESSION_DIR) if not market else market


def ask_bool():
    res = input(settings.INPUT_PROMT).lower()
    return (res == "y") or (res == "yes")


def convert_to_int(obj):
    return Decimal(obj) if obj.isdigit() else None


def check_dir(_dir):
    #print("check:", _dir)
    if not os.path.exists(_abs_path + "/" + _dir):
        #print("create:", _abs_path + "/" + _dir)
        os.mkdir(_abs_path + "/" + _dir)


def check_dirs():
    check_dir(settings.DEFAULT_DATA_DIR)
    check_dir(settings.SESSION_DIR)
    check_dir(settings.DEFAULT_SESSION_DIR)
    check_dir(settings.DEFAULT_SESSION_DIR + settings.DEFAULT_USER_DIR)
    check_dir(settings.DEFAULT_SESSION_DIR + settings.DEFAULT_MARKET_DIR)


def save_all():
    saved_count = 0

    for obj in global_vars.values():
        if "save" in dir(obj):
            if obj.save(settings.DEFAULT_SESSION_DIR):
                saved_count += 1

    #print(f"Saved: {saved_count}/{len(global_vars.values())} objects")


@register
def follow(name = "", *a, **kw):
    """Follow your favorite products
        Usage: follow <name>"""
    name = name.upper()

    if not name:
        print("No argument")
        return

    user = global_vars[settings.GLOBAL_USER_NAME]

    try:
        user.follow(name)

    except Exception as e:
        print(*e.args)


@register
def unfollow(name = "", *a, **kw):
    """Unfollow products
        Usage: unfollow <name>"""
    name = name.upper()

    if not name:
        print("No argument")
        return

    user = global_vars[settings.GLOBAL_USER_NAME]

    try:
        user.unfollow(name)

    except Exception as e:
        print(e.args)


@register
def followed(*a, **kw):
    """Show your favorite products"""

    market = global_vars[settings.GLOBAL_MARKET_NAME]
    user = global_vars[settings.GLOBAL_USER_NAME]


    print("Name  |  Price")
    print("--------------")
    for name in user.followed:
        price = market.get_price(name)
        print(f"{name}  |  {price}")

    print()


@register
def wait(days = "1", *a, **kw):
    """Skip 'days' for change price
        Usage: wait <n>"""

    try:
        days = int(days)

    except ValueError:
        print("Wrong argument")
        return

    if days < 0:
        print("Wait time can't be less then 0")
        return

    market_obj = global_vars[settings.GLOBAL_MARKET_NAME]

    for name, price in market_obj.trade_pairs.items():
        min_lim = 5
        days_passed = (random.randint(-1, 1) for _ in range(days))

        one_perc = max(perc_from(1, price), 1)
        half_price = max(perc_from(25, price), 1)
        price_changes = (random.choice((one_perc, half_price)) for _ in range(days))
        result_change = max(sum((mod * price for mod, price in zip(days_passed, price_changes))), 1)
        modifier = random.randint(-1, 1)
        result_change *= (modifier)

        product_price = market_obj.trade_pairs[name]

        if (product_price + result_change) < min_lim:
            result_change = result_change * -1 if result_change < 0 else result_change

        if result_change > (product_price * 2):
            result_change = product_price // 2

        product_price += result_change
        product_price = round(product_price, 8)

        if int(product_price) <= 0:
            product_price = Decimal(0)

        market_obj.trade_pairs[name] = product_price

    print()
    print("Followed products:")
    followed()


@register
def new(*a, **kw):
    """Create a new session
        Usage: new"""

    save_all()
    new_session = Session(force=True)
    check_dirs()
    setup(session=new_session,
          user=User().load(settings.DEFAULT_SESSION_DIR),
          market=Market().load(settings.DEFAULT_SESSION_DIR))


@register
def info(name = None, *a, **kw):
    """Show info about given object
        Usage: info <object>"""

    obj = global_vars[name] if name in global_vars else None

    if obj:
        print(obj)

    else:
        session_token = global_vars[settings.GLOBAL_SESSION_NAME].token
        user_name = global_vars[settings.GLOBAL_USER_NAME].name

        print()
        print(f"Session name: {session_token}")
        print(f"User name: {user_name}")
        print()


@register
def switch(name = None, *a, **kw):
    """Switch between sessions
        Usage: switch [name]"""
    sessions = {ind: name for ind, name in enumerate(os.listdir(settings.SESSION_DIR), 1)}
    print("Switch To:")
    print("0. Abort")

    for ind, name in sessions.items():
        print(f"\t{ind}: {name}")

    try:
        answer = int(input(settings.SPECIAL_PROMT))

    except ValueError:
        print("Wrong input")
        print("Abort Switching")
        return

    if answer <= 0:
        return

    if answer > max(sessions):
        print("Wrong input")
        print("Abort Switching")
        return

    save_all()
    print("Opening:" , sessions[answer])
    new_session = Session.open(sessions[answer])
    setup(session=new_session,
          user=User().load(settings.DEFAULT_SESSION_DIR),
          market=Market().load(settings.DEFAULT_SESSION_DIR))
    print(f"Username: {global_vars[settings.GLOBAL_USER_NAME].name}\n")


@register
def portfolio(*a, **kw):
    """Show sum of all items in your pocket"""
    user = global_vars[settings.GLOBAL_USER_NAME]

    cost = user.portfolio_cost()
    print(f"Your portfolio value: '{cost}'")


@register
def sell(name = None, raw_count = None, *a, **kw):
    """Sell goods from user
        Usage: 'sell <product_name> <count>'"""

    if not name or not raw_count:
        print("No arguments for sell")
        return

    if not (count := convert_to_int(raw_count)):
        return

    user = global_vars[settings.GLOBAL_USER_NAME]
    market = global_vars[settings.GLOBAL_MARKET_NAME]
    name = name.upper()

    try:
        price = market.get_price(name)

    except KeyError:
        print(f"Wrong product name")
        return

    if user.can_sell(name, count):
        if market.sell(name, count):
            user.refill(name, price, count)

        else:
            print("No product in market")

    else:
        print(f"Wrong count for sell")


@register
def buy(name = None, raw_count = None, *a, **kw):
    """Buy goods from market
        Usage: 'buy <product_name> <count>'"""

    if not name or not raw_count:
        print("No arguments for buy")
        return

    if not (count := convert_to_int(raw_count)):
        return

    user = global_vars[settings.GLOBAL_USER_NAME]
    market = global_vars[settings.GLOBAL_MARKET_NAME]
    name = name.upper()

    try:
        price = market.get_price(name)

    except KeyError:
        print(f"Wrong product name")
        return False

    if user.can_buy(price, count):
        if market.buy(name, count):
            user.writing_off(name, price, count)

        else:
            print("Not enough product in market for buy")

    else:
        print(f"Not enough money for buy")

