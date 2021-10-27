import enum


class MeasurementPlane(enum.Enum):
    XY_PLANE = "xy"
    YZ_PLANE = "yz"
    ZX_PLANE = "zx"


class LocalUnitary(enum.Enum):
    SQRT_X = 1
    SQRT_Y = 2
    SQRT_Z = 3
    Z = 0


class DIRECTION(enum.Enum):
    POSITIVE = +1
    NEGATIVE = -1


class MeasurementBase:
    """
    Measurement base of a qubit
    """

    def __init__(self, plane=MeasurementPlane.XY_PLANE, angle=0):
        """

        :param plane:
        :param angle:
        """
        self.vector: (int, int, int) = {
            (MeasurementPlane.XY_PLANE, 0): [0, 0, 0],
            (MeasurementPlane.XY_PLANE, 0): [0, 0, 0],
            (MeasurementPlane.XY_PLANE, 0): [0, 0, 0],
            (MeasurementPlane.XY_PLANE, 0): [0, 0, 0],
            (MeasurementPlane.XY_PLANE, 0): [0, 0, 0],
            (MeasurementPlane.XY_PLANE, 0): [0, 0, 0],
            (MeasurementPlane.XY_PLANE, 0): [0, 0, 0],
            (MeasurementPlane.XY_PLANE, 0): [0, 0, 0],
            (MeasurementPlane.XY_PLANE, 0): [0, 0, 0],
        }[(plane, angle)]

    def is_pauli(self) -> bool:
        return sum([abs(i) for i in self.vector]) == 1

    def to_pauli_base(self) -> (str, int):
        if self.vector[1] == 0 and self.vector[2] == 0:
            return "x", self.vector[0]
        elif self.vector[0] == 0 and self.vector[2] == 0:
            return "y", self.vector[1]
        elif self.vector[0] == 0 and self.vector[1] == 0:
            return "z", self.vector[2]

    def rotate_sqrt_x(self, direction):
        self.vector[1], self.vector[2] = \
            direction * self.vector[2], -direction * self.vector[1]

    def rotate_sqrt_y(self, direction):
        self.vector[3], self.vector[1] = \
            direction * self.vector[1], -direction * self.vector[3]

    def rotate_sqrt_z(self, direction) -> None:
        self.vector[0], self.vector[1] = \
            direction * self.vector[1], -direction * self.vector[0]

    def rotate_x(self) -> None:
        """
        rotate the measurement base about X axis
        """
        self.vector = (self.vector[0], -self.vector[1], -self.vector[2])

    def rotate_z(self) -> None:
        """
        Rotate the measurement base about Z axis
        """
        self.vector = (-self.vector[0], -self.vector[1], self.vector[2])

    def rotate_y(self) -> None:
        """
        Rotate the measurement base about X axis
        """
        self.vector = (-self.vector[0], self.vector[1], -self.vector[2])

    #     """
    #     Update measurement base with rotation gate
    #     [SQRT_X](X,Y,a) -> (Z,X,a+pi/2)
    #     [SQRT_Y](X,Y,a) -> (Y,Z,pi/2-a)
    #     [SQRT_Z](X,Y,a) -> (X,Y,a-pi/2)
    #
    #     [SQRT_X](Y,Z,a) -> (Y,Z,a-pi/2)
    #     [SQRT_Y](Y,Z,a) -> (X,Y,a+pi/2)
    #     [SQRT_Z](Y,Z,a) -> (Z,X,pi/2-a)
    #
    #     [SQRT_X](Z,X,a) -> (X,Y,pi/2-a)
    #     [SQRT_Y](Z,X,a) -> (Z,X,a-pi/2)
    #     [SQRT_Z](Z,X,a) -> (Y,Z,a+pi/2)
    #
    #     [Z](X,Y,a) -> (X,Y,a+pi)
    #     [Z](Y,Z,a) -> (Y,Z,pi-a)
    #     [Z](Z,X,a) -> (Z,X,-a)
    #     """
