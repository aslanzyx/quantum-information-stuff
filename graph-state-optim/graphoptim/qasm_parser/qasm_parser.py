import enum
from typing import List, Set
import numpy as np
from math import pi


# parse
def parse_qasm(qasmText: str):
    pass


def parse_line(qasmLine: str):
    pass


def parse_reg(regLine: str):
    pass


def parse_rotation(operator):
    pass


def parse_entanglement(operator):
    pass


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
        self.plane = plane
        self.angle: (int, int) = angle

    def rotate(self, unitary: LocalUnitary, direction: DIRECTION):
        """
        Update measurement base with rotation gate
        [SQRT_X](X,Y,a) -> (Z,X,a+pi/2)
        [SQRT_Y](X,Y,a) -> (Y,Z,pi/2-a)
        [SQRT_Z](X,Y,a) -> (X,Y,a-pi/2)

        [SQRT_X](Y,Z,a) -> (Y,Z,a-pi/2)
        [SQRT_Y](Y,Z,a) -> (X,Y,a+pi/2)
        [SQRT_Z](Y,Z,a) -> (Z,X,pi/2-a)

        [SQRT_X](Z,X,a) -> (X,Y,pi/2-a)
        [SQRT_Y](Z,X,a) -> (Z,X,a-pi/2)
        [SQRT_Z](Z,X,a) -> (Y,Z,a+pi/2)

        [Z](X,Y,a) -> (X,Y,a+pi)
        [Z](Y,Z,a) -> (Y,Z,pi-a)
        [Z](Z,X,a) -> (Z,X,-a)
        """
        if unitary == LocalUnitary.Z:
            if self.plane == MeasurementPlane.XY_PLANE:
                self.angle += pi
            elif self.plane == MeasurementPlane.YZ_PLANE:
                self.angle = pi-self.angle
            else:
                self.angle = -self.angle

        pass


class Node:
    """
    Node in graph state
    """

    def __init__(self, base: MeasurementBase):
        self.meas: MeasurementBase = base
        self.neighbours: Set[Node] = set()

    def add_neighbours(self, node: Node):
        """
        add neighbour node
        """
        self.neighbours.add(node)

    def complement(self, other: Node):
        """
        Complement this node with some other node
        Remove the nodes neighbour to both this and the other node
        Add the nodes neighbour to the other node but not neighbour to this node
        other: the node being complement about
        """
        intersected_nodes = self.neighbours.intersection(other.neighbours)
        disjointed_nodes = self.neighbours.difference(other.neighbours)
        for node in disjointed_nodes:
            self.neighbours.add(node)
        for node in intersected_nodes:
            self.neighbours.remove(node)


class GraphState:
    def __init__(self):
        self.nodes: List[Node] = []

    def add_node(self, node: Node):
        pass

    @staticmethod
    def parse_dag(dag: List[List[int]], measurement_bases: List[MeasurementBase]):
        graph_state = GraphState()
        for measurement_base in measurement_bases:
            graph_state.nodes.append(Node(measurement_base))
        for i in range(len(dag)):
            for j in dag[i]:
                graph_state.nodes[i].add_neighbours(graph_state.nodes[j])
                graph_state.nodes[j].add_neighbours(graph_state.nodes[i])
        return graph_state

    def local_complementation(self, node_idx: int):
        """
        Perform local complementation about node with given id
        NOTE: This is only a graph operation
        """
        for node in self.nodes[node_idx].neighbours:
            node.complement(self.nodes[node_idx])

    def cut_off(self, node_idx: int):
        """
        Cut off node
        NOTE: This is only a graph operation
        """
        neighbours = self.nodes[node_idx].neighbours
        self.nodes.pop(node_idx)
        for node in neighbours:
            node.neighbours.remove(self.nodes[node_idx])

    def x_measurement(self, node_idx: int):
        """
        Perform X-measurement on the node with given id
        """
        a = self.nodes[node_idx]
        b = list(self.nodes[node_idx].neighbours)[0]
        self.local_complementation(b)
        self.local_complementation(a)
        self.cut_off(a)
        self.local_complementation(b)

    def z_measurement(self, node_idx: int):
        """
        Perform Z-measurement on the node with given id
        """
        to_update = self.nodes[node_idx].neighbours
        self.cut_off(node_idx)


class ClusterState:
    '''
    Cluster state
    '''

    def __init__(self, size):
        self.reg: List[np.ndarray] = []
        self.size: int = size

    def add_node(self, operation, data):
        '''
        add node based on the given operation
        '''

    def fillup_line(self, line):
        '''
        fill up line using X-measurement
        '''

    def to_graph(self):
        '''
        Parse to graph state
        '''
        return NotImplementedError()
