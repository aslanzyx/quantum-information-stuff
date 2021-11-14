from .BlochSphere import BlochSphere


class PauliOperator(BlochSphere):
    def __init__(self, base: str):
        base = base.lower()
        if base == 'x':
            super(PauliOperator, self).__init__([1, 0, 0])
        elif base == 'y':
            super(PauliOperator, self).__init__([0, 1, 0])
        elif base == 'z':
            super(PauliOperator, self).__init__([0, 0, 1])
        else:
            print("Not available")

    def to_base(self):
        if self.vector[1] == 0 and self.vector[2] == 0:
            return "X", self.vector[0]
        elif self.vector[0] == 0 and self.vector[2] == 0:
            return "Y", self.vector[1]
        elif self.vector[1] == 0 and self.vector[1] == 0:
            return "Z", self.vector[2]

    def __repr__(self):
        if self.vector == [1, 0, 0]:
            return 'X'
        elif self.vector == [-1, 0, 0]:
            return '-X'
        elif self.vector == [0, 1, 0]:
            return 'Y'
        elif self.vector == [0, -1, 0]:
            return '-Y'
        elif self.vector == [0, 0, 1]:
            return 'Z'
        elif self.vector == [0, 0, -1]:
            return '-Z'
        else:
            print("error")
