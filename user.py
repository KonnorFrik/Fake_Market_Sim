from commands_handler import register # last in import section


class User:
    def __init__(self):
        self.money = 234

    def __str__(self):
        var_s = ", ".join([f"{key}='{val}'" for key, val in self.__dict__.items()])
        return var_s


