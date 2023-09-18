import pickle
from collections import defaultdict
from decimal import Decimal
from global_scope import global_vars

import settings


class User:
    """User object for comunicate with market"""

    filepath = settings.DEFAULT_USER_DIR + settings.DEFAULT_USER_DATA_FILE

    def __init__(self):
        self.money = Decimal(settings.DEFAULT_USER_START_MONEY)
        self.pocket = defaultdict(int)


    def _clear_pocket(self):
        to_del = list()
        for name, val in self.pocket.items():
            if val <= 0:
                to_del.append(name)

        for name in to_del:
            del self.pocket[name]

    def writing_off(self, name, price, count):
        self.money -= count * price
        self.pocket[name] += count


    def refill(self, name, price, count):
        self.pocket[name] -= count
        self.money += price * count

        self._clear_pocket()

    def can_buy(self, price, count):
        return (self.money - (price * count)) >= 0


    def can_sell(self, name, count):
        res = (self.pocket[name] - count) >= 0
        self._clear_pocket()
        return res

    def get_coin_count(self, name):
        res = self.pocket[name]
        self._clear_pocket()
        return res


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


    def portfolio_cost(self):
        res = 0
        market = global_vars[settings.GLOBAL_MARKET_NAME]

        for name, count in self.pocket.items():
            price = market.get_price(name)
            res += price * count

        return res

    @staticmethod
    def new():
        return User()
