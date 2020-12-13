class TFact:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.name == other.name

    def __str__(self):
        return 'Fact[{}]'.format(self.name)
