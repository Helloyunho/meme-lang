class UnaryOp:
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr
        self.name = 'UnaryOp'
