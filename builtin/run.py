import lexer
from parser import Parser

def run(args, visit):
    a = visit.visit(args[0])

    l = lexer.run(a.value)
    p = Parser(l)
    visit.visit(p.parse())
