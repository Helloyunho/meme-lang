class BoolOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = self.token = op
        self.right = right
        self.name = 'BoolOp'
