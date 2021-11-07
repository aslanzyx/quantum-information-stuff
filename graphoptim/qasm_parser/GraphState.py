from graphoptim.graph_state.MeasurementBase import MeasurementBase
from typing import List, Set, Dict
from graphoptim.graph_state.Node import Node


class GraphState:
    def __init__(self):
        self.nodes: Dict[any:Node] = dict()
        self.size = 0

    @staticmethod
    def parse_dag(links: List[Set[int]], measurement_bases: List[(int, int, int)]):
        graph_state = GraphState()
        nodes = [Node(MeasurementBase(measurement_base)) for measurement_base in measurement_bases]
        n = len(links)
        for i in range(n):
            for j in links[i]:
                nodes[i].link(j)
            graph_state.nodes[i] = nodes[i]
        return graph_state

    def local_complementation(self, label: any):
        self.nodes[label].local_complementation()

    def cut_off(self, label: any):
        self.nodes[label].disconnect()

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
