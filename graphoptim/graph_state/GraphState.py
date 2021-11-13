from typing import List, Set, Dict
from graphoptim.graph_state import Node
import graphviz


class GraphState:
    def __init__(self):
        self.nodes: Dict[any, Node] = dict()
        self.edges: Dict[any, Set[any]] = dict()
        self.input: List[any] = []
        self.output: Set[any] = set()
        self.size = 0

    def set_input(self, label):
        self.input.append(label)

    def is_input(self, label):
        return label in self.input

    def set_output(self, label):
        self.output.add(label)

    def is_output(self, label):
        return label in self.output

    def get_node(self, label):
        return self.nodes[label]

    def add_node(self, node: Node):
        self.nodes[node.label] = node
        self.edges[node.label] = set()

    def remove_node(self, label: any) -> None:
        neighbours = self.edges.pop(label)
        for neighbour in neighbours:
            self.edges[neighbour].remove(label)

    def add_edge(self, label_u: any, label_v: any):
        self.edges[label_u].add(label_v)
        self.edges[label_v].add(label_u)

    def local_complement(self, label: any, rotate: int = 0):
        neighbours = self.edges[label]
        for neighbour in neighbours:
            for other_neighbour in neighbours:
                if neighbour != other_neighbour:
                    if other_neighbour in self.edges[neighbour]:
                        self.edges[neighbour].remove(other_neighbour)
                    else:
                        self.edges[neighbour].add(other_neighbour)
        if rotate != 0:
            self.nodes[label].merge_sqrt_x(rotate)
            for node in neighbours:
                self.nodes[node].merge_sqrt_z(rotate)

    def x_measurement(self, label: any, direction: int, b: any = None):
        if b is None:
            b = self.edges[label].pop()
            self.edges[label].add(b)
        self.nodes[b].merge_sqrt_y(-direction)
        if direction == 1:
            for node in self.edges[label].difference(self.edges[b]).difference({b}):
                self.nodes[node].merge_z()
        else:
            for node in self.edges[b].difference(self.edges[label]).difference({label}):
                self.nodes[node].merge_z()
        self.local_complement(b)
        self.local_complement(label)
        self.remove_node(label)
        self.local_complement(b)

    def y_measurement(self, label: int, direction: int) -> None:
        for node in self.edges[label]:
            self.nodes[node].merge_sqrt_z(direction)
        self.local_complement(label)
        self.remove_node(label)

    def z_measurement(self, label: any, direction: int) -> None:
        if direction == -1:
            for node in self.edges[label]:
                self.nodes[node].merge_z()
        self.remove_node(label)

    def measure(self, label: int):
        base, direction = self.nodes[label].base.to_pauli()
        base = base.lower()
        if base == 'x':
            self.x_measurement(label, direction)
        elif base == 'y':
            self.y_measurement(label, direction)
        elif base == 'z':
            self.z_measurement(label, direction)

    def eliminate_pauli(self):
        for label, node in self.nodes.items():
            if label not in self.input and label not in self.output and node.base.is_pauli():
                self.measure(label)

    def extract_dag(self) -> Dict[any, Set[any]]:
        edges: Dict[any, Set[any]] = dict()
        for curr, node in self.nodes.items():
            for prev in node.corrections.keys():
                if prev in edges:
                    edges[prev] = set()
                edges[prev].add(curr)
        return edges

    def extract_temporal_order(self):
        edges = self.extract_dag()
        order = []
        visited = set()
        todo = set(self.nodes.keys())
        node = todo.pop()
        stack = []
        for next in edges[node]:
            if next not in edges and next not in visited:
                pass
        return order.reverse()

    def extact_parallel_measurements(self):
        pass

    def dfs(self, edges: Dict, node: any, func):
        if node:
            for next in edges[node]:
                self.dfs(edges, next, func)
                func(next)

    def render(self, filename="demo", **config):
        visited_edge: Set[(any, any)] = set()
        g = graphviz.Graph()
        for label, node in self.nodes.items():
            g.node(label, label=node.__repr__())
            for other_label in self.edges[label]:
                if (other_label, label) not in visited_edge:
                    g.edge(label, other_label)
                    visited_edge.add((label, other_label))
        g.render(filename, view=True)
