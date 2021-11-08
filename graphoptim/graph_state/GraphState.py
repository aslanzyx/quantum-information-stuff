from graphoptim.graph_state.MeasurementBase import MeasurementBase
from typing import List, Set, Dict
from graphoptim.graph_state import Node
from graph_tools import Graph
import graph_tools as gt


class GraphState:
    def __init__(self):
        self.nodes: Dict[any:Node] = dict()
        self.size = 0

    # @staticmethod
    # def parse_dag(links: List[Set[int]], measurement_bases: List[(int, int, int)]):
    #     graph_state = GraphState()
    #     nodes = [Node(MeasurementBase(measurement_base)) for measurement_base in measurement_bases]
    #     n = len(links)
    #     for i in range(n):
    #         for j in links[i]:
    #             nodes[i].link(j)
    #         graph_state.nodes[i] = nodes[i]
    #     return graph_state

    def local_complement(self, label: any):
        self.nodes[label].local_complement()

    def cut_off(self, label: any):
        self.nodes[label].disconnect()

    def x_measurement(self, label: any, direction: int):
        self.nodes[label].x_measure(direction)

    def y_measurement(self, label: int, direction: int) -> None:
        self.nodes[label].y_measure(direction)

    def z_measurement(self, label: int, direction: int) -> None:
        self.nodes[label].z_measure(direction)

    def measure(self, label: int):
        self.nodes[label].measure()

    def eliminate_pauli(self):
        to_remove = []
        for label in self.nodes.keys():
            if self.nodes[label].is_pauli():
                self.nodes[label].measure()
                to_remove.append(label)
        for label in to_remove:
            self.nodes.pop(label)

    def render(self):
        g = Graph()
        for label in self.nodes.keys():
            g.add_vertex(label)
            for other_label in self.nodes.keys():
                if self.nodes[other_label] in self.nodes[label].neighbours:
                    g.add_edge(label, other_label)
        print(g)
        bases = [(self.nodes[label].meas.vector, label) for label in g.vertices()]
        print(bases)

