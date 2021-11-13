# from typing import Set, Tuple
# import numpy as np
# from .enum import LocalUnitary, Direction, MeasurementPlane
# from math import pi
#
#
# class GraphState:
#
#     def __init__(self, size: int, edge_config: set, measurement_config: dict):
#         self.size: int = size
#         self.metric: np.ndarray = np.zeros((size, size))
#         self.node_reg: dict = dict()
#         self.label_reg: list = []
#         self.measurement_bases: np.ndarray = np.ndarray((size))
#         # parse graph
#         self.parse_graph(edge_config, measurement_config)
#
#     def parse_graph(self, edge_config: Set[Tuple], measurement_config: dict):
#         '''
#         Parse edges and measurement bases with given configuration
#         edge_config: set of edges denoted by tuple (u, v)
#         measurement_config: dictionary maps labels to measurement bases denoted by (measurement_plane, angle)
#         '''
#         i = 0
#         # parse measurement bases
#         for label in measurement_config.keys():
#             # update the label and node registers
#             self.label_reg[i] = label
#             self.node_reg[label] = i
#             # add measurement base to class
#             self.measurement_bases[i] = MeasurementBase(
#                 measurement_config[label][0], measurement_config[label][1])
#             # accumulate index counter
#             i += 1
#         # parse edges
#         for edge in edge_config:
#             self.metric[edge[0], edge[1]] = 1
#             self.metric[edge[1], edge[0]] = 1
#
#     def local_complementation(self, label: str) -> None:
#         '''
#         Perform local complementation about a node with given label.
#         label: label of node where the local complementation is performing about.
#         '''
#         node: int = self.node_reg[label]
#         neighbours: np.ndarray = np.arange(self.size)[self.metric[node]] == 1
#         for i in neighbours:
#             for j in neighbours:
#                 if i != j:
#                     self.metric[i, j] = (self.metric[i, j] + 1) % 2
#
#     def pivot(self, edge: tuple) -> None:
#         return NotImplementedError()
#
#     def cut_off(self, label: str) -> np.ndarray:
#         '''
#         Perform cut-off on a node with given label.
#         Return the indices of nodes neighbour to the cut-off node.
#         label: the label of given node
#         '''
#         node: int = self.node_reg[label]
#         neighbours: np.ndarray = np.arange(self.size)[self.metric[node] == 1]
#         self.metric[node, :] = 0
#         self.metric[:, node] = 0
#         return neighbours
#
#     def x_measurement(self, label: str):
#         '''
#         Simulate Y-measurement on a node with given label.
#         label: the label of given node
#         direction: the direction positive/negative of measurement base
#         '''
#         node: int = self.node_reg[label]
#         b0: int = np.arange(self.size)[self.metric[node] == 1][0]
#         self.local_complementation(self.label_reg[b0])
#         self.local_complementation(label)
#         neighbours: np.ndarray = self.cut_off(label)
#         self.local_complementation(self.label_reg[b0])
#         return NotImplementedError()
#
#     def y_measurement(self, label: str, direction: int):
#         '''
#         Simulate Y-measurement on a node with given label.
#         label: the label of given node
#         direction: the direction positive/negative of measurement base
#         '''
#         self.local_complementation(label)
#         neighbours = self.cut_off(label)
#         self.measurement_bases[neighbours].rotate(
#             LocalUnitary.SQRT_Z, direction)
#
#     def z_measurement(self, label: str, direction: int) -> None:
#         '''
#         Simulate Z-measurement on a node with given label.
#         label: the label of given node
#         direction: the direction positive/negative of measurement base
#         '''
#         neighbours = self.cut_off(label)
#         if direction:
#             self.measurement_bases[neighbours].rotate(LocalUnitary.Z, 0)
#
#
# class MeasurementBase:
#     def __init__(self, plane: MeasurementPlane, angle: float) -> None:
#         self.plane = plane
#         self.angle = angle
#         pass
#
#     def is_pauli(self):
#         '''
#         Return if current measurement is in Pauli bases.
#         '''
#         return (self.angle % pi/2) == 0
#
#     def rotate(self, unitary: LocalUnitary, direction: Direction) -> None:
#         '''
#         Rotate measurement base with given local unitary.
#         Such local unitary is expected to be clifford.
#         '''
#         return NotImplementedError()
