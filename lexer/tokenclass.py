class Token:
    def __init__(self, typee, value):
        self.type = typee
        self.value = value

    def __str__(self):
        return f'<Token type=\'{self.type}\', value=\'{self.value}\'>'

    __repr__ = __str__
