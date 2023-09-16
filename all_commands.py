from typing import Optional
from global_scope import global_vars
from commands_handler import register # last in import section
import settings


def ask_bool():
    res = input(settings.INPUT_PROMT).lower()
    return (res == "y") or (res == "yes")


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
def sell(name = None, raw_count = None, *a, **kw):
    """Sell goods from user
        Usage: 'sell <product_name> <count>'"""

    if not name or not raw_count:
        print("No arguments for sell")
        return

    if raw_count.isdigit():
        count = int(raw_count)

    else:
        return False

    user = global_vars["user"]
    market = global_vars["market"]

    try:
        price = market.get_price(name)

    except KeyError:
        print(f"Wrong product name")
        return

    def market_sale(user, market, name, price, count):
        if market.sell(name, count):
            user.refill(name, price, count)

        else:
            print("No product in market")

    if user.can_sell(name, count):
        market_sale(user, market, name, price, count)

    else:
        print(f"Not enough products in pocket.\nSell All? [y/N]")
        if ask_bool():
            market_sale(user, market, name, price, count)


@register
def buy(name = None, raw_count = None, *a, **kw):
    """Buy goods from market
        Usage: 'buy <product_name> <count>'"""

    if not name or not raw_count:
        print("No arguments for buy")
        return

    if raw_count.isdigit():
        count = int(raw_count)

    else:
        return False

    user = global_vars["user"]
    market = global_vars["market"]

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

