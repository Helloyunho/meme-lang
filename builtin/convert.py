from .string import String
from .array import Array
from .dictionary import Dict
from .number import Number
from .boolean import Boolean

def convert(a):
    if type(a) == str:
        return String(a)
    elif type(a) == int or type(a) == float:
        return Number(a)
    elif type(a) == bool:
        return Boolean(a)
    elif type(a) == list:
        return Array(a)
    elif type(a) == dict:
        return Dict(a)
    return a
