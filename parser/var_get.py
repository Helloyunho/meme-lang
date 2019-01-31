class VarGet:
    def __init__(self, name, get):
        self.var_name = name.value
        self.token = name
        self.get = get
        self.name = 'VarGet'
