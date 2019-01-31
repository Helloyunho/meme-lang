from .builtin_symbol import BuiltinTypeSymbol as BuiltinSymbol

class ScopedSymbolTable:
    def __init__(self, name, level, enclosing_scope=None):
        self._symbols = {}
        self.name = name
        self.level = level
        self.enclosing_scope = enclosing_scope
        self.define(BuiltinSymbol('NUMBER'))
        self.define(BuiltinSymbol('STRING'))
        self.define(BuiltinSymbol('BOOLEAN'))

    def define(self, symbol):
        if self._symbols.get(symbol.name) is not None and self._symbols[symbol.name].type == ':=':
            raise SyntaxError('You cannot edit const vars.')
        if self.enclosing_scope is not None and self.enclosing_scope.lookup(symbol.name) is not None and self.enclosing_scope.lookup(symbol.name).type == ':=':
            raise SyntaxError('You cannot edit const vars.')
        self._symbols[symbol.name] = symbol
        if self.enclosing_scope is not None and self.enclosing_scope.lookup(symbol.name) is not None:
            self.enclosing_scope.define(symbol)

    def unsafe_define(self, symbol):
        self._symbols[symbol.name] = symbol

    def lookup(self, name):
        if self._symbols.get(name) is not None:
            return self._symbols.get(name)
        else:
            if self.enclosing_scope is not None:
                return self.enclosing_scope.lookup(name)
