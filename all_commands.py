from typing import Optional
from decimal import Decimal
from global_scope import global_vars
from commands_handler import register
import settings


def ask_bool():
    res = input(settings.INPUT_PROMT).lower()
    return (res == "y") or (res == "yes")


def convert_to_int(obj):
    return Decimal(obj) if obj.isdigit() else None


@register
def info(name = None, *a, **kw):
    """Show info about given object
        Usage: info <object>"""

    obj = global_vars[name] if name in global_vars else None

    if obj:
        print(obj)

    else:
        print("No argument for display")


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

