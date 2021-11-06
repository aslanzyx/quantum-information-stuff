import numpy as np

from measurement_base import MeasurementBase


def test_is_pauli():
    assert not MeasurementBase([1, 1, 1]).is_pauli()
    print("pass case: not pauli")
    assert MeasurementBase([1, 0, 0]).is_pauli()
    print("pass case: indeed pauli")
    assert MeasurementBase([-1, 0, 0]).is_pauli()
    print("pass case: negative direction")


def test_to_pauli_base():
    # assert MeasurementBase([1, 1, 1])
    pass


def test_rotation():
    measurement_base = MeasurementBase([1, 1, 1])
    measurement_base.rotate_x()
    assert measurement_base.vector == [1, -1, -1]
    print("pass case: x rotation")
    measurement_base.rotate_y()
    assert measurement_base.vector == [-1, -1, 1]
    print("pass case: y rotation")
    measurement_base.rotate_z()
    assert measurement_base.vector == [1, 1, 1]
    print("pass case: z rotation")

    measurement_base.rotate_sqrt_x(1)
    assert measurement_base.vector == [1, 1, -1]
    print("pass case: positive sqrt x rotation")
    measurement_base.rotate_sqrt_x(-1)
    assert measurement_base.vector == [1, 1, 1]
    print("pass case: negative sqrt x rotation")
    measurement_base.rotate_sqrt_y(1)
    assert measurement_base.vector == [-1, 1, 1]
    print("pass case: positive sqrt y rotation")
    measurement_base.rotate_sqrt_y(-1)
    assert measurement_base.vector == [1, 1, 1]
    print("pass case: negative sqrt y rotation")
    measurement_base.rotate_sqrt_z(-1)
    assert measurement_base.vector == [-1, 1, 1]
    print("pass case: negative sqrt z rotation")
    measurement_base.rotate_sqrt_z(1)
    assert measurement_base.vector == [1, 1, 1]
    print("pass case: positive sqrt z rotation")


def main():
    test_is_pauli()
    test_rotation()


# main()

f = open("teleportation.qasm")
a = f.read().splitlines()
f.close()
print(a)

_b = np.zeros((5, 2))
_b[1, 1] += 4
print(np.sign(_b))

from qiskit import QuantumCircuit

qc = QuantumCircuit(4, 4)
qc.h([0, 1, 2, 3])
qc.measure(0,0)
qc.draw()
