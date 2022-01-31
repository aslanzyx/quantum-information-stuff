import unittest
from graphoptim.graph_state import GraphState, ClusterState


class TestGraphState(unittest.TestCase):

    def setUp(self) -> None:
        c = ClusterState(2)
        c.t(0)
        c.t(1)
        c.cnot(0, 1)
        g = c.to_graph_state()

    def test_simulation(self):
        self.graph_state.eliminate_pauli()
        self.graph_state.render()
        self.assertTrue(True)
