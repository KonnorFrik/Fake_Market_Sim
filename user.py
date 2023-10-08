import pickle
from collections import defaultdict
from decimal import Decimal
from global_scope import global_vars

import settings


class User:
    """ User object for comunicate with market """

    def __init__(self, name = None, start_money = None):
        self.money = Decimal(start_money) if start_money else Decimal(settings.DEFAULT_USER_START_MONEY)
        self.pocket = defaultdict(int)
        self._name = name

        self.following = list()


    @property
    def followed(self):
        for name in self.following:
            yield name


    def follow(self, name):
        if name not in global_vars[settings.GLOBAL_MARKET_NAME].trade_pairs:
            raise Exception(f"Name: '{name}' not in market")

        self.following.append(name)


    def unfollow(self, name):
        if name not in self.following:
            raise Exception(f"Name: '{name}' not in following")

        self.following.pop(self.following.index(name))


    @property
    def name(self):
        return self._name


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


    def load(self, session_path):
        """ Try load from session file
            If fail - create new User """
        filepath = session_path + settings.DEFAULT_USER_DATA_FILE

        try:
            with open(filepath, "rb") as file:
                self = pickle.load(file)

        except FileNotFoundError:
            #logger
            #print(f"[ERROR] can't load user data from: {filepath}, default will be used")
            print(f"Can't load user. Create new")
            return User.new()

        except EOFError:
            #print(f"[ERROR] file '{filepath}' may be corrupted, default data will be used")
            print(f"Can't load user. Create new")
            return User.new()

        return self


    def save(self, session_path) -> bool:
        """ Try save to self to session folder
            If can't open file return False """
        filepath = session_path + settings.DEFAULT_USER_DATA_FILE
        res = False

        try:
            with open(filepath, "wb") as file:
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
        """ Sum of all things in pocket """
        res = 0
        market = global_vars[settings.GLOBAL_MARKET_NAME]

        for name, count in self.pocket.items():
            price = market.get_price(name)
            res += price * count

        return res


    @staticmethod
    def new():
        print("Enter a User name: ")
        name = input(settings.SPECIAL_PROMT)

        print("Enter a User start money")
        start_money = input(settings.SPECIAL_PROMT)
        return User(name=name, start_money=start_money)
