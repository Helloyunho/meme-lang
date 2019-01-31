from .array import Array
from .assign import Assign
from .binop import BinOp
from .boolean import Boolean
from .boolop import BoolOp
from .call import Call
from .compond import Compound
from .dot import Dot
from .Dict import Dict
from .dictlr import DictLR
from .For import For
from .function import Function
from .If import If
from .Import import Import
from .none import NoOp
from .normal_get import NormalGet
from .normal_set import NormalSet
from .num import Number
from .program import Program
from .string import String
from .times import Times
from .unaryop import UnaryOp
from .var import Var
from .var_get import VarGet
from .var_set import VarSet
from .While import While

BoolOps = ['==', '!=', '>', '<', '<=', '>=', '||', 'and']

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.indexToken = 0

    def program(self):
        node = self.compoundStatement()
        return Program(node)

    def checker(self, name):
        if self.tokens[self.indexToken].type == '\n' and name != '\n':
            self.indexToken += 1
        if self.tokens[self.indexToken].type == ';' and name != ';':
            self.indexToken += 1
        if self.tokens[self.indexToken].type == name:
            self.indexToken += 1
        else:
            raise SyntaxError('Error! Type: {}, Expected: {}'.format(self.tokens[self.indexToken].type, name))

    def compoundStatement(self):
        self.checker('{')
        nodes = self.statementList()
        self.checker('}')

        root = Compound()

        for a in nodes:
            root.children.append(a)

        return root

    def statementList(self):
        node = self.statement()

        results = [node]

        while self.tokens[self.indexToken].type == ';' or self.tokens[self.indexToken].type == '\n':
            if self.tokens[self.indexToken].type == ';' or self.tokens[self.indexToken].type == '\n':
                self.indexToken += 1
            else:
                raise SyntaxError(f'Error! Type: {self.tokens[self.indexToken].type}, Expected: ; or \n')

            results.append(self.statement())

        return results

    def statement(self):
        token = self.tokens[self.indexToken]
        node = None
        if token.type == '{':
            node = self.compoundStatement()
        elif token.type == 'ID' and self.tokens[self.indexToken + 1].type == '(':
            node = self.callStatement()
        elif self.tokens[self.indexToken + 1].type == '.':
            node = self.dotStatement()
        elif self.tokens[self.indexToken + 1].type == '[':
            node = self.assignmentSetStatement()
        elif token.type == 'IF':
            node = self.ifStatement()
        elif token.type == 'WHILE':
            node = self.whileStatement()
        elif token.type == 'TIMES':
            node = self.timesStatement()
        elif token.type == 'FOR':
            node = self.forStatement()
        elif token.type == 'ID' and (self.tokens[self.indexToken + 1].type == '=' or self.tokens[self.indexToken + 1].type == ':='):
            node = self.assignmentStatement()
        elif token.type == 'ID':
            node = self.variable()
        elif token.type == 'IMPORT':
            node = self.importModule()
        else:
            node = NoOp()

        return node

    def importModule(self):
        self.checker('IMPORT')
        name = self.tokens[self.indexToken].value
        self.checker('ID')
        return Import(name)

    def whileStatement(self):
        self.checker('WHILE')
        self.checker('(')
        whil = self.exce()
        self.checker(')')
        run = self.compoundStatement()

        return While(whil, run)

    def timesStatement(self):
        self.checker('TIMES')
        self.checker('(')
        idd = self.variable()
        self.checker(',')
        times = Number(self.tokens[self.indexToken])
        self.checker('NUMBER')
        self.checker(')')
        run = self.compoundStatement()

        return Times(idd, times, run)

    def forStatement(self):
        self.checker('FOR')
        self.checker('(')
        checker = []
        i = 0
        while i < 3:
            checker.append(self.exce())
            if self.tokens[self.indexToken].type != ')':
                if self.tokens[self.indexToken].type == ';':
                    self.checker(';')
                else:
                    self.checker('\n')
            i += 1

        self.checker(')')
        run = self.compoundStatement()

        return For(checker, run)

    def dotStatement(self):
        left = self.getNumber()
        self.checker('.')
        right = None
        if self.tokens[self.indexToken + 1].type != '(':
            self.indexToken += 1
            right = self.variable()
        else:
            right = self.callStatement()

        return Dot(left, right)

    def ifStatement(self):
        self.checker('IF')
        self.checker('(')
        when = self.exce()
        self.checker(')')
        then = self.compoundStatement()
        Else = self.tokens[self.indexToken].type == 'ELSE'
        if (Else):
            self.indexToken += 1
            Else = self.compoundStatement()
        else:
            Else = None

        return If(when, then, Else)

    def functionStatement(self):
        varss = []
        self.checker('(')
        while self.tokens[self.indexToken].type != ')':
            varss.append(self.tokens[self.indexToken])
            self.checker('ID')
            if self.tokens[self.indexToken].type == ',':
                self.checker(',')
            if self.tokens[self.indexToken].type == '\n':
                self.indexToken += 1
            if self.tokens[self.indexToken].type == ';':
                self.indexToken += 1
        self.checker(')')
        node = self.compoundStatement()

        return Function(varss, node)

    def assignmentSetStatement(self):
        left = self.exce()
        self.checker('=')
        right = self.exce()
        if left.name == 'VarGet':
            return VarSet(left, right)
        else:
            return NormalSet(left, right)

    def assignmentStatement(self):
        left = self.variable()
        token = self.tokens[self.indexToken]
        if not token.type in ['=', ':=']:
            raise SyntaxError(f'Error! Type: {token.type}, Expected: = or :=')
        self.indexToken += 1
        right = self.exce()
        node = Assign(left, token, right)
        return node

    def callStatement(self):
        name = self.tokens[self.indexToken].value
        self.checker('ID')
        varss = []
        self.checker('(')
        while self.tokens[self.indexToken].type != ')':
            varss.append(self.exce())
            if self.tokens[self.indexToken].type == ',':
                self.checker(',')
            if self.tokens[self.indexToken].type == '\n':
                self.indexToken += 1
            if self.tokens[self.indexToken].type == ';':
                self.indexToken += 1
        self.checker(')')

        return Call(name, varss)

    def variable(self):
        node = Var(self.tokens[self.indexToken])
        self.checker('ID')
        return node

    def getNumber(self):
        if self.tokens[self.indexToken].type == '\n':
            self.indexToken += 1
        if self.tokens[self.indexToken].type == ';':
            self.indexToken += 1
        token = self.tokens[self.indexToken]
        if token.type == 'NUMBER':
            self.checker('NUMBER')
            return Number(token)
        elif token.type == '+':
            self.checker('+')
            return UnaryOp(token, self.getNumber())
        elif token.type == '-':
            self.checker('-')
            return UnaryOp(token, self.getNumber())
        elif token.type == '(':
            self.checker('(')
            result = self.exce()
            self.checker(')')
        elif token.type == 'STRING':
            self.checker('STRING')
            return String(token)
        elif token.type == 'BOOLEAN':
            self.checker('BOOLEAN')
            return Boolean(token)
        elif token.type == 'FUNCTION':
            self.checker('FUNCTION')
            return self.functionStatement()
        elif self.tokens[self.indexToken + 1].type == '=':
            return self.assignmentStatement()
        elif token.type == '[':
            self.checker('[')
            varss = []
            while self.tokens[self.indexToken].type != ']':
                varss.append(self.exce())
                if self.tokens[self.indexToken].type == ',':
                    self.checker(',')
                if self.tokens[self.indexToken].type == '\n':
                    self.indexToken += 1
                if self.tokens[self.indexToken].type == ';':
                    self.indexToken += 1
            self.checker(']')
            return Array(varss)
        elif token.type == '{':
            self.checker('{')
            varss = []
            while self.tokens[self.indexToken].type != '}':
                left = self.exce()
                self.checker(':')
                right = self.exce()
                varss.append(DictLR(left, right))
                if self.tokens[self.indexToken].type == ',':
                    self.checker(',')
                if self.tokens[self.indexToken].type == '\n':
                    self.indexToken += 1
                if self.tokens[self.indexToken].type == ';':
                    self.indexToken += 1
            self.checker('}')

            return Dict(varss)
        elif token.type == 'ID':
            return self.variable()

    def calcHigh(self):
        result = self.getNumber()

        while self.tokens[self.indexToken].type == '/' or self.tokens[self.indexToken].type == '*':
            token = self.tokens[self.indexToken]
            if token.type == '*':
                self.checker('*')
            elif token.type == '/':
                self.checker('/')
            result = BinOp(result, token, self.getNumber())

        return result

    def exce(self):
        result = self.calcHigh()

        while self.tokens[self.indexToken].type == '.':
            self.checker('.')
            right = None
            if self.tokens[self.indexToken + 1].type != '(':
                if self.tokens[self.indexToken + 1].type == '=':
                    right = self.assignmentStatement()
                else:
                    right = self.variable()
            else:
                right = self.callStatement()

            result = Dot(result, right)

        while self.tokens[self.indexToken].type == '+' or self.tokens[self.indexToken].type == '-':
            token = self.tokens[self.indexToken]
            if token.type == '+':
                self.checker('+')
            elif token.type == '-':
                self.checker('-')
            result = BinOp(result, token, self.exce())

        while self.tokens[self.indexToken].type in BoolOps:
            token = self.tokens[self.indexToken]
            if (token.type == '=='):
                self.checker('==')
            elif token.type == '!=':
                self.checker('!=')
            elif token.type == '>=':
                self.checker('>=')
            elif token.type == '<=':
                self.checker('<=')
            elif token.type == '>':
                self.checker('>')
            elif token.type == '<':
                self.checker('<')
            elif token.type == '||':
                self.checker('||')
            elif token.type == 'and':
                self.checker('and')

            result = BoolOp(result, token, self.exce())

        while self.tokens[self.indexToken].type == '[':
            self.checker('[')
            a = self.exce()
            self.checker(']')
            if result.name == 'Var':
                result = VarGet(result, a)
            else:
                result = NormalGet(result, a)

        return result

    def parse(self):
        node = self.program()

        return node
