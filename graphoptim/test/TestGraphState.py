# import unittest
# from graphoptim.graph_state import GraphState, Node, MeasurementBase
#
#
# class TestGraphState(unittest.TestCase):
#
#     def setUp(self) -> None:
#         self.input0 = Node(MeasurementBase([1, 1, 0]))
#         self.input1 = Node(MeasurementBase([1, 1, 0]))
#         self.output0 = Node(MeasurementBase([1, 1, 0]))
#         self.output1 = Node(MeasurementBase([1, 1, 0]))
#         self.h00 = Node(MeasurementBase([0, 1, 0]))
#         self.h01 = Node(MeasurementBase([0, 1, 0]))
#         self.h02 = Node(MeasurementBase([0, 1, 0]))
#         self.h10 = Node(MeasurementBase([0, 1, 0]))
#         self.h11 = Node(MeasurementBase([0, 1, 0]))
#         self.h12 = Node(MeasurementBase([0, 1, 0]))
#         self.input0.link(self.h00)
#         self.h00.link(self.h01)
#         self.h01.link(self.h02)
#         self.h02.link(self.output0)
#         self.input1.link(self.h10)
#         self.h10.link(self.h11)
#         self.h11.link(self.h12)
#         self.h12.link(self.output1)
#         self.graph_state = GraphState()
#         self.graph_state.nodes = {self.input0, self.input1, self.h00, self.h01, self.h02,
#                                   self.h10, self.h11, self.h12, self.output0, self.output1}
#
#     def test_simulation(self):
#         self.graph_state.eliminate_pauli()
#         self.graph_state.render()
#         self.assertTrue(True)
