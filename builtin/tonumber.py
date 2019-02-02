from .number import Number

def tonumber(values, visit):
    a = visit.visit(values[0])
    result = a.toNumber()
    return Number(result)
