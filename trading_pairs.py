from decimal import Decimal
from enum import Enum
from random import randint, choice
from string import ascii_uppercase


def new_product_name():
    """ Random name for new product """
    return "".join((choice(ascii_uppercase) for _ in range(4)))


def new_price(start=10, end=10_000):
    return Decimal(randint(start, end))


def new_count(start=10, end=10_000):
    return randint(start, end)


def new_pairs() -> tuple:
    """ Random pairs with name, count and price """
    assets = list()
    counts = list()

    for _ in range(10):
        name = new_product_name()
        assets.append((name, new_price()))
        counts.append((name, new_count()))

    assets.append(("SBER", Decimal(250)))
    assets.append(("LKOH", Decimal(5872)))
    counts.append(("SBER", new_count()))
    counts.append(("LKOH", new_count()))

    return assets, counts

