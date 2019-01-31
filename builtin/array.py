from .number import Number
from .string import String

class Array:
    def __init__(self, array):
        self.array = self.value = []
        for x in array:
            self.array.append(x.value)

    def __str__(self):
        a = [str(x) for x in self.array]
        return '[{}]'.format('\n' + '\n'.join(a))

    def indexOf(self, a, visit):
        return Number(self.array.index(visit.visit(a[0])))


    def push(self, a, visit):
        aa = self.array.append(visit.visit(a[0]).value)
        if type(aa) == int or type(aa) == float:
            return Number(aa)
        elif type(aa) == str:
            return String(aa)

    def pop(self):
        a = self.array[-1]
        del self.array[-1]
        if type(a) == int or type(a) == float:
            return Number(a)
        elif type(a) == str:
            return String(a)

    def remove(a, visit):
        del self.array[visit.visit(a[0])]

    def delete(a, visit):
        i = self.array.index(visit.visit(a[0]))
        del self.array[i]
