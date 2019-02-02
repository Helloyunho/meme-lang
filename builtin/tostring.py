from .string import String

def tostring(values, visit):
    a = visit.visit(values[0])
    result = str(a)
    return String(result)
