from .base import Symbol

class VarSymbol(Symbol):
    def __init__(self, name, typee=None, value=None):
        super().__init__(name, typee)
        self.var_value = value
        self.value = self.var_value.value if hasattr(self.var_value, 'value') else self.var_value
