import lexer
from parser import Parser

def toarray(values, visit):
    a = visit.visit(values[0]).value
    if type(a) is str:
        tokened = lexer.run(a)
        tokened = tokened[1:-2]
        tokened.append(lexer.Token('None', None))
        if tokened[0].type == '[' and tokened[-2].type == ']':
            ready_for_parse = Parser(tokened)
            result = ready_for_parse.exce()
            return visit.visit(result)
