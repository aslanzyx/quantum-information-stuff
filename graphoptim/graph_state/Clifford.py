# from enum import Enum
#
# class LocalUnitary(Enum):
#     X = 'x'
#     Y = 'y'
#     Z = 'z'
#     SQRT_X = 'half-x'
#     SQRT_Y = 'half-y'
#     SQRT_Z = 'half-z'
#
# class Direction(Enum):
#     POSITIVE = 0
#     NEAGTIVE = 1
#
# class MeasurementPlane(Enum):
#     XY = 'xy'
#     YZ = 'yz'
#     XZ = 'xz'

from enum import Enum


class Clifford(Enum):
    I = 0
    X = 1
    Z = 2
    Y = 3
    SQRT_X = 4
    SQRT_Z = 5
    SQRT_Y = 6
