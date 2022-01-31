from .Utils import rotate_coordinates
from .Exceptions import BaseException
import numpy as np


class BlochSphere:
    def __init__(self, vector: np.ndarray = np.array([0, 0, 1])):
        self.vector: np.ndarray = vector

    def rotate(self, angle: float, base: str) -> None:
        if base == 'x':
            self.rotate_x(angle)
        elif base == 'y':
            self.rotate_y(angle)
        elif base == 'z':
            self.rotate_z(angle)
        else:
            raise BaseException("Invalid base")

    # def is_pauli(self):
    #     return np.abs(np.sum(self.vector)) == 1

    def pauli_base(self):
        if self.vector[0] == 1:
            return "x"
        elif self.vector[1] == 1:
            return "y"
        elif self.vector[2] == 1:
            return "z"
        else:
            return None

    def rotate_x(self, angle) -> None:
        self.vector[1], self.vector[2] = \
            rotate_coordinates(angle, self.vector[1], self.vector[2])

    def rotate_y(self, angle) -> None:
        self.vector[2], self.vector[0] = \
            rotate_coordinates(angle, self.vector[2], self.vector[0])

    def rotate_z(self, angle) -> None:
        self.vector[0], self.vector[1] = \
            rotate_coordinates(angle, self.vector[0], self.vector[1])

    def flip_x(self) -> None:
        self.vector[1], self.vector[2] = -self.vector[1], -self.vector[2]

    def flip_y(self) -> None:
        self.vector[2], self.vector[0] = -self.vector[2], -self.vector[0]

    def flip_z(self) -> None:
        self.vector[0], self.vector[1] = -self.vector[0], -self.vector[1]

    def rotate_sqrt_x(self, direction):
        self.vector[1], self.vector[2] = -direction * self.vector[2], direction * self.vector[1]

    def rotate_sqrt_y(self, direction):
        self.vector[2], self.vector[0] = -direction * self.vector[0], direction * self.vector[2]

    def rotate_sqrt_z(self, direction):
        self.vector[0], self.vector[1] = -direction * self.vector[1], direction * self.vector[0]

    def rotate_h(self):
        self.rotate_sqrt_x(1)
        self.rotate_sqrt_z(1)
        self.rotate_sqrt_x(1)

    def __repr__(self):
        return "Bloch sphere object with vector {}".format(self.vector)
