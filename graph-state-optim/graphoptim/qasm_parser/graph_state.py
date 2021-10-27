from .measurement_base import MeasurementBase
from typing import Set, List


class Node:
    """
    Node in graph state
    """

    def __init__(self, base: MeasurementBase):
        self.meas: MeasurementBase = base
        self.neighbours: Set[Node] = set()

    def add_neighbours(self, node):
        """
        add neighbour node
        """
        self.neighbours.add(node)

    def complement(self, other):
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
        self.size = 0

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

    def x_measurement(self, node_idx: int, direction: int):
        """
        Perform X-measurement on the node with given id
        :param node_idx: node index
        """

        # graph operation
        b = list(self.nodes[node_idx].neighbours)[0]

        # L.C. on b
        for node in b.neighbours:
            node.complement(b)
        self.local_complementation(node_idx)
        self.cut_off(node_idx)
        for node in b.neighbours:
            node.complement(b)

        # stabilizer to update
        if direction == 1:
            b.meas.rotate_sqrt_y(-1)
        else:
            b.meas.rotate_sqrt_y(1)

    def y_measurement(self, node_idx: int, direction: int) -> None:
        """
        Perform Y-measurement on the node with given id
        :param node_idx: node index
        """
        to_update = self.nodes[node_idx].neighbours
        self.local_complementation(node_idx)
        self.cut_off(node_idx)
        for node in to_update:
            node.meas.rotate_sqrt_y(direction)

    def z_measurement(self, node_idx: int, direction: int) -> None:
        """
        Perform Z-measurement on the node with given id
        :param node_idx: node index
        """
        to_update = self.nodes[node_idx].neighbours
        self.cut_off(node_idx)
        if direction == -1:
            for node in to_update:
                node.meas.rotate_z()

    def eliminate_pauli(self):
        for i in range(self.size):
            base, direction = self.nodes[i].meas.to_pauli_base()
            if base == "x":
                self.x_measurement(i, direction)
            elif base == "y":
                self.y_measurement(i, direction)
            elif base == "z":
                self.z_measurement(i, direction)
