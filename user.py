import pickle
from collections import defaultdict
from decimal import Decimal

import settings


class User:
    """User object for comunicate with market"""

    filepath = settings.DEFAULT_USER_DIR + settings.DEFAULT_USER_DATA_FILE

    def __init__(self):
        self.money = Decimal(settings.DEFAULT_USER_START_MONEY)
        self.pocket = defaultdict(int)


    def writing_off(self, name, price, count):
        self.money -= count * price
        self.pocket[name] += count


    def refill(self, name, price, count):
        self.pocket[name] -= count
        self.money += price * count

        if self.pocket[name] <= 0:
            del self.pocket[name]


    def can_buy(self, price, count):
        return (self.money - (price * count)) >= 0


    def can_sell(self, name, count):
        return (self.pocket[name] - count) >= 0


    def get_coin_count(self, name):
        return self.pocket[name]


    def load(self):
        try:
            with open(self.filepath, "rb") as file:
                self = pickle.load(file)

        except FileNotFoundError:
            #logger
            print(f"[ERROR] can't load user data from: {self.filepath}, default will be used")
            return User.new()

        except EOFError:
            print(f"[ERROR] file '{self.filepath}' may be corrupted, default data will be used")
            return User.new()

        return self


    def save(self) -> bool:
        res = False

        try:
            with open(self.filepath, "wb") as file:
                pickle.dump(self, file)

        except FileNotFoundError:
            res = False

        else:
            res = True

        return res


    def __str__(self):
        money = f"Money: {self.money}"
        res = "Name  |  Count\n--------------\n"

        for name, count in self.pocket.items():
            res += f"{name}  |  {count}\n"

        return money + "\n" + res


    @staticmethod
    def new():
        return User()
