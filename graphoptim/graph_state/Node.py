from typing import Set

from graphoptim.graph_state.MeasurementBase import MeasurementBase


class Node:
    """
    Node in graph state
    """

    def __init__(self, base: MeasurementBase):
        self.meas: MeasurementBase = base
        self.neighbours: Set[Node] = set()

    def link(self, node):
        self.neighbours.add(node)
        node.neighbours.add(self)

    def unlink(self, node):
        self.neighbours.remove(node)
        node.neighbours.remove(self)

    def local_complementation(self):
        for node in self.neighbours:
            for other in self.neighbours:
                if other in node.neighbours:
                    node.neighbours.remove(other)
                elif node is not other:
                    node.neighbours.add(other)

    def disconnect(self):
        for node in self.neighbours:
            self.unlink(node)

    def is_pauli(self):
        return self.meas.is_pauli()

    def measure(self):
        base, direction = self.meas.to_pauli()
        if base == "x":
            self.x_measure(direction)
        elif base == "y":
            self.y_measure(direction)
        elif base == "z":
            self.z_measure(direction)
        else:
            pass

    def x_measure(self, direction):
        b = self.neighbours.pop()
        self.neighbours.add(b)
        b.meas.rotate_sqrt_y(direction)
        if direction == 1:
            for node in b.neighbours.difference(self.neighbours):
                node.meas.rotate_z()
        else:
            for node in self.neighbours.difference(b.neighbours):
                node.meas.rotate_z()
        b.local_complementation()
        self.local_complementation()
        self.disconnect()
        b.local_complementation()
        pass

    def y_measure(self, direction):
        for node in self.neighbours:
            node.meas.rotate_sqrt_z(direction)
        self.local_complementation()
        self.disconnect()

    def z_measure(self, flag):
        if flag:
            for node in self.neighbours:
                node.meas.rotate_z()
        self.disconnect()

    # def complement(self, other):
    #     """
    #     Complement this node with some other node
    #     Remove the nodes neighbour to both this and the other node
    #     Add the nodes neighbour to the other node but not neighbour to this node
    #     other: the node being complement about
    #     """
    #     intersected_nodes = self.neighbours.intersection(other.neighbours)
    #     disjointed_nodes = self.neighbours.difference(other.neighbours)
    #     for node in disjointed_nodes:
    #         self.neighbours.add(node)
    #     for node in intersected_nodes:
    #         self.neighbours.remove(node)
