class Boolean:
    def __init__(self, token):
        self.token = token
        self.value = token.value == 'true'
        self.name = 'Boolean'
