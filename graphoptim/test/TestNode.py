import unittest
from graphoptim.graph_state import Node, MeasurementBase


class TestNode(unittest.TestCase):
    def test_node(self):
        n0 = Node(MeasurementBase([1, 0, 0]))
        n1 = Node(MeasurementBase([0, 1, 0]))
        n2 = Node(MeasurementBase([1, 1, 0]))
        n3 = Node(MeasurementBase([-1, 0, 0]))
        n0.link(n1)
        n1.link(n2)
        assert n0.neighbours == {n1}
        assert n1.neighbours == {n0, n2}
        assert n2.neighbours == {n1}
        n1.local_complementation()
        print("pass case: link")
        assert n0.neighbours == {n1, n2}
        assert n1.neighbours == {n0, n2}
        assert n2.neighbours == {n0, n1}
        print("pass case: local complementation 3 nodes")
        n1.link(n3)
        n1.local_complementation()
        assert n0.neighbours == {n1, n3}
        assert n1.neighbours == {n0, n2, n3}
        assert n2.neighbours == {n1, n3}
        assert n3.neighbours == {n0, n1, n2}
        print("pass case: local complementation 4 nodes")
        n1.unlink(n3)
        assert n1.neighbours == {n0, n2}
        print("pass case: unlink node")
