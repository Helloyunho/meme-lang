from .rand import random as rand
from .rand import randInt as randInt
from .rand import choice as choice

class random(object):
    @staticmethod
    def random(*args):
        return rand(*args)

    @staticmethod
    def randInt(*args):
        return randInt(*args)

    @staticmethod
    def choice(*args):
        return choice(*args)
