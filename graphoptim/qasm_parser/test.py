# from MeasurementBase import MeasurementBase
# from Node import Node
from graphoptim.graph_state.Node import Node
from graphoptim.graph_state.MeasurementBase import MeasurementBase


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





def stabilizer_generator():
    links = [
        {1, 2},
        {0, 2},
        {0, 1}
    ]

    measurements = [
        (1, 0, 0),
        (0, 1, 0),
        (1, 1, 0),
    ]




def main():
    test_is_pauli()
    test_rotation()
    test_node()


main()

# f = open("teleportation.qasm")
# a = f.read().splitlines()
# f.close()
# print(a)
#
# _b = np.zeros((5, 2))
# _b[1, 1] += 4
# print(np.sign(_b))

# from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
#
# qr = QuantumRegister(4)
# c0 = ClassicalRegister(1)
# c1 = ClassicalRegister(1)
# qc = QuantumCircuit(qr, c0, c1)
#
# qc.h([0, 1, 2, 3])
# qc.cz(0, 1)
# qc.cz(1, 2)
# qc.cz(2, 3)
# qc.h(0)
# qc.measure(0, c0[0])
# qc.x(qr[1]).c_if(c0, 1)
# qc.h(1)
# qc.measure(1, c1[0])
# qc.x(qr[2]).c_if(c1, 1)
# print(qc.draw())
