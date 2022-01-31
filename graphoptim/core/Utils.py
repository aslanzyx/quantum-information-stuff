from math import pi, sin, cos


def rotate_coordinates(angle: float, rx: float, ry: float):
    return cos(angle) * rx - sin(angle) * ry, \
           sin(angle) * rx + cos(angle) * ry


def is_pauli_angle(angle: float):
    return angle % (pi / 2) == 0
