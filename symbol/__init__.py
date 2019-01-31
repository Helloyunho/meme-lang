import builtin
import module
from .var import VarSymbol
from .scopesymbols import ScopedSymbolTable
from .function import FunctionSymbol

class SymbolTableInterpreter:
    def __init__(self):
        self.current_state = None

    def visit(self, node):
        a = getattr(self, f'visit{node.name}', self.noneError)(node)
        return a

    def noneError(self, node):
        raise SyntaxError(f'visiter visit{node.name} is not found.')

    def visitProgram(self, node):
        self.current_state = ScopedSymbolTable('global', 1, self.current_state)
        self.visit(node.block)

    def visitBinOp(self, node):
        result = None
        if node.op.type == '+':
            result = self.visit(node.left).value + self.visit(node.right).value
        elif node.op.type == '-':
            result = self.visit(node.left).value - self.visit(node.right).value
        elif node.op.type == '*':
            result = self.visit(node.left).value * self.visit(node.right).value
        elif node.op.type == '/':
            result = self.visit(node.left).value / self.visit(node.right).value

        return builtin.convert(result)

    def visitNumber(self, node):
        return builtin.convert(node.value)

    def visitString(self, node):
        return builtin.convert(node.value)

    def visitArray(self, node):
        values = []
        for x in node.values:
            values.append(self.visit(x))
        return builtin.convert(values)

    def visitBoolean(self, node):
        return builtin.convert(node.value)

    def visitDict(self, node):
        value = {}
        for x in node.values:
            value[self.visit(x.left).value] = self.visit(x.right).value
        return builtin.convert(value)

    def visitUnaryOp(self, node):
        op = node.op.type
        if op == '+':
            return builtin.convert(+(self.visit(node.expr).value))
        elif op == '-':
            return builtin.convert(+(self.visit(node.expr).value))

    def visitBoolOp(self, node):
        left = self.visit(node.left)
        op = node.op.type
        right = self.visit(node.right)
        if op == '==':
            return builtin.convert(left.value == right.value)
        elif op == '!=':
            return builtin.convert(left.value != right.value)
        elif op == '>':
            return builtin.convert(left.value > right.value)
        elif op == '<':
            return builtin.convert(left.value < right.value)
        elif op == '>=':
            return builtin.convert(left.value >= right.value)
        elif op == '<=':
            return builtin.convert(left.value <= right.value)
        elif op == '||':
            return builtin.convert(left.value or right.value)
        elif op == '&&':
            return builtin.convert(left.value and right.value)

    def visitIf(self, node):
        when = self.visit(node.check)
        then = node.then
        Else = node.Else
        if when:
            self.current_state = ScopedSymbolTable('IF', self.current_state.level + 1, self.current_state)
            self.visit(then)
            self.current_state = self.current_state.enclosing_scope
        else:
            if Else is not None:
                self.current_state = ScopedSymbolTable('ELSE', self.current_state.level + 1, self.current_state)
                self.visit(Else)
                self.current_state = self.current_state.enclosing_scope

    def visitImport(self, node):
        a = getattr(module, node.module_name, None)
        if a is None:
            self.noModuleError()
        self.current_state.unsafe_define(VarSymbol(node.module_name, ':=', a))

    def noModuleError(self, node):
        raise ImportError(f'Module {node.module_name} not found.')

    def visitCompound(self, node):
        for child in node.children:
            self.visit(child)

    def visitNoOp(self, node):
        pass

    def visitFor(self, node):
        self.current_state = ScopedSymbolTable('FOR', self.current_state.level + 1, self.current_state)
        a = self.visit(node.check[0])
        if a is not None:
            varSymbol = VarSymbol(node.check[0].value, None, a.var_value if hasattr(a, 'var_value') else a)
            self.current_state.unsafe_define(varSymbol)
        while self.visit(node.check[1]).value:
            self.visit(node.run)
            self.visit(node.check[2])
        self.current_state = self.current_state.enclosing_scope

    def visitWhile(self, node):
        self.current_state = ScopedSymbolTable('WHILE', self.current_state.level + 1, self.current_state)
        while self.visit(node.whil).value:
            self.visit(node.run)
        self.current_state = self.current_state.enclosing_scope

    def visitTimes(self, node):
        self.current_state = ScopedSymbolTable('TIMES', self.current_state.level + 1, self.current_state)
        self.current_state.unsafe_define(VarSymbol(node.id.value, None, 0))
        while self.visit(node.times).value > self.current_state.lookup(node.id.value).value:
            self.visit(node.run)
            self.current_state.unsafe_define(VarSymbol(node.id.value, None, self.current_state.lookup(node.id.value).value + 1))
        self.current_state = self.current_state.enclosing_scope
    def visitDot(self, node):
        left = self.visit(node.left)
        if hasattr(left, 'var_value'):
            left = left.var_value
        right = node.right
        if not hasattr(left, right.value) and not hasattr(left, right.func_name if hasattr(right, 'func_name') else '__init__') and hasattr(left, right.left.value) if hasattr(right, 'left') else False:
            raise SyntaxError('{}  not found in type {}'.format(right.func_name if hasattr(right, 'func_name') else (right.value if hasattr(right, 'value') else right.left.value), name))
        else:
            if right.name == 'Call':
                return getattr(left, right.func_name)(right.vars, self)
            elif right.name == 'Var':
                return getattr(left, right.value)
            elif right.name == 'VarGet':
                return (getattr(left, right.value)).value[self.visit(right.get)]

    def visitVarGet(self, node):
        var_name = node.var_name
        var_symbol = self.current_state.lookup(var_name)
        if var_symbol is None:
            var_symbol = getattr(builtin, var_name, None)
        if var_symbol is None:
            raise NameError(f'Variable {var_name} not found.')

        return builtin.convert(var_symbol.value[self.visit(node.get).value])

    def visitNormalGet(self, node):
        return builtin.convert(self.visit(node.From).value[self.visit(node.get).value])

    def visitVarSet(self, node):
        var_name = node.var_name
        var_symbol = self.current_state.lookup(var_name)
        if var_symbol is None:
            var_symbol = getattr(builtin, var_name, None)
        if var_symbol is None:
            raise NameError(f'Variable {var_name} not found.')
        var_symbol.value[self.visit(node.token.get).value] = self.visit(node.set).value

    def visitNormalSet(self, node):
        self.visit(node.From.From).value[self.visit(node.From.get).value] = self.visit(node.set).value

    def visitCall(self, node):
        name = node.func_name
        symbol = self.current_state.lookup(name)
        if symbol is None:
            symbol = getattr(builtin, name, None)
        if symbol is None:
            raise NameError(f'Variable {name} not found.')
        if hasattr(symbol, 'var_value'):
            symbol.var_value(node.vars, self)
        else:
            symbol(node.vars, self)

    def visitAssign(self, node):
        var_name = node.left.value
        var_symbol = VarSymbol(var_name, node.token.type, self.visit(node.right))
        self.current_state.define(var_symbol)

    def visitVar(self, node):
        var_name = node.value
        var_symbol = self.current_state.lookup(var_name)
        if var_symbol is None:
            var_symbol = getattr(builtin, var_name, None)
        if var_symbol is None:
            raise NameError(f'Variable {var_name} not found.')
        return var_symbol

    def visitFunction(self, node):
        def a(args, _):
            symbol = FunctionSymbol()
            self.current_state = ScopedSymbolTable('FUNCTION', self.current_state.level + 1, self.current_state)
            for i in range(len(node.vars)):
                name = node.vars[i].value
                As = self.visit(args[i])
                var_symbol = VarSymbol(name, None, getattr(As, 'var_value', As))
                self.current_state.unsafe_define(var_symbol)
                symbol.params.append(var_symbol)
            self.visit(node.block)
            self.current_state = self.current_state.enclosing_scope
        return a
