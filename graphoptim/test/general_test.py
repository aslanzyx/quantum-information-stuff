# # from MeasurementBase import MeasurementBase
# # from Node import Node
# from graphoptim.graph_state.Node import Node
# from graphoptim.graph_state.MeasurementBase import MeasurementBase
#
#
# def test_is_pauli():
#     assert not MeasurementBase([1, 1, 1]).is_pauli()
#     print("pass case: not pauli")
#     assert MeasurementBase([1, 0, 0]).is_pauli()
#     print("pass case: indeed pauli")
#     assert MeasurementBase([-1, 0, 0]).is_pauli()
#     print("pass case: negative direction")
#
#
# def test_to_pauli_base():
#     # assert MeasurementBase([1, 1, 1])
#     pass
#
#
# def test_rotation():
#     measurement_base = MeasurementBase([1, 1, 1])
#     measurement_base.rotate_x()
#     assert measurement_base.vector == [1, -1, -1]
#     print("pass case: x rotation")
#     measurement_base.rotate_y()
#     assert measurement_base.vector == [-1, -1, 1]
#     print("pass case: y rotation")
#     measurement_base.rotate_z()
#     assert measurement_base.vector == [1, 1, 1]
#     print("pass case: z rotation")
#
#     measurement_base.rotate_sqrt_x(1)
#     assert measurement_base.vector == [1, 1, -1]
#     print("pass case: positive sqrt x rotation")
#     measurement_base.rotate_sqrt_x(-1)
#     assert measurement_base.vector == [1, 1, 1]
#     print("pass case: negative sqrt x rotation")
#     measurement_base.rotate_sqrt_y(1)
#     assert measurement_base.vector == [-1, 1, 1]
#     print("pass case: positive sqrt y rotation")
#     measurement_base.rotate_sqrt_y(-1)
#     assert measurement_base.vector == [1, 1, 1]
#     print("pass case: negative sqrt y rotation")
#     measurement_base.rotate_sqrt_z(-1)
#     assert measurement_base.vector == [-1, 1, 1]
#     print("pass case: negative sqrt z rotation")
#     measurement_base.rotate_sqrt_z(1)
#     assert measurement_base.vector == [1, 1, 1]
#     print("pass case: positive sqrt z rotation")
#
#
#
#
#
# def stabilizer_generator():
#     links = [
#         {1, 2},
#         {0, 2},
#         {0, 1}
#     ]
#
#     measurements = [
#         (1, 0, 0),
#         (0, 1, 0),
#         (1, 1, 0),
#     ]
#
#
#
#
# def main():
#     test_is_pauli()
#     test_rotation()
#     test_node()
#
#
# main()
#
# # f = open("teleportation.qasm")
# # a = f.read().splitlines()
# # f.close()
# # print(a)
# #
# # _b = np.zeros((5, 2))
# # _b[1, 1] += 4
# # print(np.sign(_b))
#
# # from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
# #
# # qr = QuantumRegister(4)
# # c0 = ClassicalRegister(1)
# # c1 = ClassicalRegister(1)
# # qc = QuantumCircuit(qr, c0, c1)
# #
# # qc.h([0, 1, 2, 3])
# # qc.cz(0, 1)
# # qc.cz(1, 2)
# # qc.cz(2, 3)
# # qc.h(0)
# # qc.measure(0, c0[0])
# # qc.x(qr[1]).c_if(c0, 1)
# # qc.h(1)
# # qc.measure(1, c1[0])
# # qc.x(qr[2]).c_if(c1, 1)
# # print(qc.draw())

from graphoptim.graph_state import *

input0 = Node(MeasurementBase([1, 1, 0]))
input1 = Node(MeasurementBase([1, 1, 0]))
output0 = Node(MeasurementBase([1, 1, 0]))
output1 = Node(MeasurementBase([1, 1, 0]))

h00 = Node(MeasurementBase([0, 1, 0]))
h01 = Node(MeasurementBase([0, 1, 0]))
h02 = Node(MeasurementBase([0, 1, 0]))
h10 = Node(MeasurementBase([0, 1, 0]))
h11 = Node(MeasurementBase([0, 1, 0]))
h12 = Node(MeasurementBase([0, 1, 0]))
h20 = Node(MeasurementBase([0, 1, 0]))
h21 = Node(MeasurementBase([0, 1, 0]))
h22 = Node(MeasurementBase([0, 1, 0]))
h30 = Node(MeasurementBase([0, 1, 0]))
h31 = Node(MeasurementBase([0, 1, 0]))
h32 = Node(MeasurementBase([0, 1, 0]))
t0 = Node(MeasurementBase([1, 1, 0]))
t1 = Node(MeasurementBase([1, 1, 0]))

x0 = Node(MeasurementBase([1, 0, 0]))
x1 = Node(MeasurementBase([1, 0, 0]))

input0.link(h00)
h00.link(h01)
h01.link(h02)
h02.link(t0)
# t0.link(h20)

t0.link(x0)
x0.link(x1)
x1.link(h20)

h20.link(h21)
h21.link(h22)
h22.link(output0)

input1.link(h10)
h10.link(h11)
h11.link(h12)
h12.link(t1)
t1.link(h30)
h30.link(h31)
h31.link(h32)
h32.link(output1)

graph_state = GraphState()

# nodes = [input0, input1, h00, h01, h02,
#          h10, h11, h12, output0, output1]
#
# for i in range(10):
#     graph_state.nodes[i] = nodes[i]

graph_state.nodes = {
    "input 0": input0,
    "input 1": input0,
    "output 0": input0,
    "output 1": input0,
    "h00": h00,
    "h01": h01,
    "h02": h02,
    "h10": h10,
    "h11": h11,
    "h12": h12,
    "h20": h20,
    "h21": h21,
    "h22": h22,
    "h30": h30,
    "h31": h31,
    "h32": h32,
    "t0": t0,
    "t1": t1,
}

graph_state.eliminate_pauli()
graph_state.render()
