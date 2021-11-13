from graphoptim.graph_state import Clifford


class BlochSphere:
    def __init__(self, vector):
        self.vector = vector

    def rotate(self, operator: Clifford):
        if operator == Clifford.X:
            self.rotate_x()
        elif operator == Clifford.Z:
            self.rotate_z()
        elif operator == Clifford.Y:
            self.rotate_y()
        elif operator == Clifford.SQRT_X:
            self.rotate_sqrt_x(1)
        elif operator == -Clifford.SQRT_X:
            self.rotate_sqrt_x(-1)
        elif operator == Clifford.SQRT_Y:
            self.rotate_sqrt_y(1)
        elif operator == -Clifford.SQRT_Y:
            self.rotate_sqrt_y(-1)
        elif operator == Clifford.SQRT_Z:
            self.rotate_sqrt_z(1)
        elif operator == -Clifford.SQRT_Z:
            self.rotate_sqrt_z(1)
        else:
            pass

    def rotate_x(self):
        self.vector[1], self.vector[2] = -self.vector[1], -self.vector[2]

    def rotate_y(self):
        self.vector[0], self.vector[2] = -self.vector[0], -self.vector[2]

    def rotate_z(self):
        self.vector[0], self.vector[1] = -self.vector[0], -self.vector[1]

    def rotate_sqrt_x(self, direction):
        self.vector[1], self.vector[2] = direction * self.vector[2], -direction * self.vector[1]

    def rotate_sqrt_y(self, direction):
        self.vector[0], self.vector[2] = direction * self.vector[2], -direction * self.vector[0]

    def rotate_sqrt_z(self, direction):
        self.vector[0], self.vector[1] = direction * self.vector[1], -direction * self.vector[0]

    def __repr__(self):
        return "Bloch sphere object with vector {}".format(self.vector)
