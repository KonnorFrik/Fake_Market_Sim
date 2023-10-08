import os
from random import choice
from string import ascii_uppercase
import settings

__vowels = "aeiou".upper()
__consonants = "".join(filter(lambda x: x not in __vowels, ascii_uppercase))


def word_gen(syllable = 5):
    return "".join((choice(__consonants) + choice(__vowels) for _ in range(syllable)))


def update_names_by_token(token):
    settings.DEFAULT_SESSION_DIR = settings.DEFAULT_SESSION_DIR_TEMPLATE.format(token)


def get_session_token():
    try:
        dirs = os.listdir(settings.SESSION_DIR)

    except FileNotFoundError:
        dirs = None

    if dirs:
        return dirs[0]

    return word_gen()


#Command for switch, create new
class Session:
    def __init__(self, force = False, _token = ""):
        if not _token:
            self.session_token = get_session_token() if not force else word_gen()

        else:
            self.session_token = _token

        update_names_by_token(self.token)


    @property
    def token(self):
        return self.session_token


    def save(self, *a, **kw):
        return False


    @classmethod
    def open(cls, name):
        return cls(_token=name)

