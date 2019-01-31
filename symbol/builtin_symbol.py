from .base import Symbol

class BuiltinTypeSymbol(Symbol):
    def __str__(self):
        return self.name
