from .number import Number
from .boolean import Boolean

class String:
    def __init__(self, string):
        self.str = self.value = string
        self.length = Number(len(self.str))

    def __str__(self):
        return self.value

    def toNumber(self):
        return float(self.str) if '.' in self.str else int(self.str)

    def standsFor(self, str, visit):
        return Boolean((visit.visit(str[0]).value).startswith(self.str))