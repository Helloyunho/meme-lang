from .base import Symbol

class FunctionSymbol(Symbol):
    def __init__(self, params=[]):
        super().__init__('')
        self.params = params

    def __str__(self):
        return self.name
