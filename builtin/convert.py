from .string import String
from .array import Array
from .dictionary import Dict
from .number import Number
from .boolean import Boolean

def convert(a):
    if type(a) is str:
        return String(a)
    elif type(a) is int or type(a) is float:
        return Number(a)
    elif type(a) is bool:
        return Boolean(a)
    elif type(a) is list:
        return Array(a)
    elif type(a) is dict:
        return Dict(a)
    return a
