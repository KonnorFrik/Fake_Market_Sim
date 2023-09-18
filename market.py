import settings
import pickle
from trading_pairs import new_pairs


class Market:
    """Store trading pairs
        Provide API for trade them"""

    filepath = settings.DEFAULT_MARKET_DIR + settings.DEFAULT_MARKET_DATA_FILE

    def __init__(self, trade_pairs = None, count_pairs = None):

        self.trade_pairs = dict(trade_pairs) if trade_pairs else dict()
        self.count_pairs = dict(count_pairs) if count_pairs else dict()


    def buy(self, name, count=1) -> bool:
        """Request for buy
            True if request approved
            False otherwise"""

        if name not in self.trade_pairs and name not in self.count_pairs:
            return False

        if (self.count_pairs[name] - count) >= 0:
            self.count_pairs[name] -= count
            return True

        else:
            return False


    def sell(self, name, count=1):
        """Request for sell
            True if request approved
            False otherwise"""

        if name not in self.trade_pairs and name not in self.count_pairs:
            return False

        self.count_pairs[name] += count
        return True


    def get_price(self, name):
        return self.trade_pairs[name]


    def get_count(self, name):
        return self.count_pairs[name]


    def load(self):
        try:
            with open(self.filepath, "rb") as file:
                self = pickle.load(file)

        except FileNotFoundError:
            print(f"[ERROR] can't load market data from: {self.filepath}, default will be used")
            return Market.new()

        except EOFError:
            print(f"[ERROR] file '{self.filepath}' may be corrupted, default data will be used")
            return Market.new()

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


    def __repr__(self):
        buf = list()

        for (name, price), (name, count) in zip(sorted(self.trade_pairs.items()), sorted(self.count_pairs.items())):
            buf.append(f"{name}=(price={price},count={count})")

        return f"Market({', '.join(buf)})"


    def __str__(self):
        buf = "Name  |  Price  |  Count\n------------------------\n"

        for (name, price), (name, count) in zip(sorted(self.trade_pairs.items()), sorted(self.count_pairs.items())):
            buf += f"{name}  |  {price}\t|  {count}\n"

        return buf


    @staticmethod
    def new():
        return Market(*new_pairs())

