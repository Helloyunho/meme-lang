import random as ran
from builtin import convert

def random(_, __):
    return ran.random()

def randInt(args, visit):
    if len(args) == 1:
        return convert(ran.randint(visit.visit(args[0])))
    elif len(args) == 2:
        return convert(ran.randint(visit.visit(args[0]), visit.visit(args[1])))
def choice(args, visit):
    a = visit.visit(args[0]).value
    return convert(ran.choice(a))

__all__ = [random, randInt, choice]
