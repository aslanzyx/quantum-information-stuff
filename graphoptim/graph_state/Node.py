from typing import Dict

from graphoptim.graph_state import MeasurementBase
from .PauliOperator import PauliOperator


class Node:

    def __init__(self, base: any, label: any):
        self.label = label
        self.base: MeasurementBase = MeasurementBase(base)
        self.corrections: Dict[any, PauliOperator] = dict()
        # self.neighbours: Set[Node] = set()

    def add_correction(self, base, label: any):
        self.corrections[label] = PauliOperator(base)

    def merge_z(self):
        for correction in self.corrections.values():
            correction.rotate_z()
        self.base.rotate_z()

    def merge_sqrt_x(self, direction):
        for correction in self.corrections.values():
            correction.rotate_sqrt_x(direction)
        self.base.rotate_sqrt_x(direction)

    def merge_sqrt_z(self, direction):
        for correction in self.corrections.values():
            correction.rotate_sqrt_z(direction)
        self.base.rotate_sqrt_z(direction)

    def merge_sqrt_y(self, direction):
        for correction in self.corrections.values():
            correction.rotate_sqrt_y(direction)
        self.base.rotate_sqrt_y(direction)

    def __repr__(self):
        retval = "{}:M({})".format(self.label, self.base.__repr__())
        for label, correction in self.corrections.items():
            retval += "{}({})".format(correction.to_base()[0], label)
        return retval

    # def link(self, node):
    #     self.neighbours.add(node)
    #     node.neighbours.add(self)
    #
    # def unlink(self, node):
    #     self.neighbours.remove(node)
    #     node.neighbours.remove(self)
    #
    # def local_complement(self):
    #     for node in self.neighbours:
    #         for other in self.neighbours:
    #             if other in node.neighbours:
    #                 # node.neighbours.remove(other)
    #                 node.unlink(other)
    #             elif node is not other:
    #                 # node.neighbours.add(other)
    #                 other.unlink(node)
    #
    # def disconnect(self):
    #     for node in self.neighbours:
    #         node.neighbours.remove(self)
    #     self.neighbours = set()
    #
    # def is_pauli(self):
    #     return self.base.is_pauli()
    #
    # def measure(self):
    #     base, direction = self.base.to_pauli()
    #     if base == "x":
    #         self.x_measure(direction)
    #     elif base == "y":
    #         self.y_measure(direction)
    #     elif base == "z":
    #         self.z_measure(direction)
    #     else:
    #         pass
    #
    # def x_measure(self, direction):
    #     b = self.neighbours.pop()
    #     self.neighbours.add(b)
    #     b.meas.rotate_sqrt_y(-direction)
    #     if direction == 1:
    #         for node in self.neighbours.difference(b.neighbours).difference({b}):
    #             node.meas.rotate_z()
    #     else:
    #         for node in b.neighbours.difference(self.neighbours).difference({self}):
    #             node.meas.rotate_z()
    #     b.local_complement()
    #     self.local_complement()
    #     self.disconnect()
    #     b.local_complement()
    #     pass
    #
    # def y_measure(self, direction):
    #     for node in self.neighbours:
    #         node.meas.rotate_sqrt_z(direction)
    #     self.local_complement()
    #     self.disconnect()
    #
    # def z_measure(self, direction):
    #     if direction == -1:
    #         for node in self.neighbours:
    #             node.meas.rotate_z()
    #     self.disconnect()

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
