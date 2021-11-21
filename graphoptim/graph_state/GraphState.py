from typing import List, Set, Dict

import numpy as np

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
        self.nodes.pop(label)
        if label in self.input:
            self.input.remove(label)
        if label in self.output:
            self.output.remove(label)

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
        if len(self.edges[label]) > 0:
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
        else:
            self.remove_node(label)

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
        for label, node in list(self.nodes.items()):
            if len(node.corrections.keys()) == 0 and node.base.is_pauli():
                self.measure(label)

    def extract_dag(self) -> Dict[any, Set[any]]:
        edges: Dict[any, Set[any]] = dict()
        for curr, node in self.nodes.items():
            for prev in node.corrections.keys():
                if prev in edges:
                    edges[prev] = set()
                edges[prev].add(curr)
        return edges

    def partition(self):
        todo = set(self.nodes.keys())
        partition = dict()
        while len(todo) > 0:
            for label in list(todo):
                # if len(self.nodes[label].corrections.keys()) == 0:
                #     partition[label] = 0
                #     todo.remove(label)
                flag = True
                set_id = 0
                for source in self.nodes[label].corrections.keys():
                    if source not in partition:
                        flag = False
                        break
                    set_id = max(partition[source] + 1, set_id)
                if flag:
                    partition[label] = set_id
                    todo.remove(label)
        return partition

    def render_partition(self):
        p = self.partition().items()
        # g = graphviz.Digraph()
        g = graphviz.Graph(format="png")
        i = 0
        todo = set(self.nodes.keys())
        g.attr("node", shape="box")
        while len(todo) > 0:
            # name = f'cluster_{i}'
            with g.subgraph() as c:
                c.attr(rank=f'same')
                for label, part in p:
                    if part == i:
                        c.node(str(label), label=self.nodes[label].__repr__())
                        todo.remove(label)
                c.attr(label=f'cluster #{i}')
            i += 1
        visited_edges = set()
        for label, nexts in self.edges.items():
            for next_label in nexts:
                if (next_label, label) not in visited_edges:
                    g.edge(str(label), str(next_label))
                    visited_edges.add((label, next_label))
        # for label, node in self.nodes.items():
        #     for source in node.corrections.keys():
        #         g.edge(str(source), str(label))
        g.view(filename="demo_circ", directory="./../cache", cleanup=True)

    def minimize_edge(self, max_out=100):
        counter = 0
        flag = True
        min_label = None
        min_num = self.count_edge_num()
        while counter < max_out and flag:
            flag = False
            for label in self.nodes.keys():
                self.local_complement(label, 1)
                num = self.count_edge_num()
                if min_num is None or num < min_num:
                    min_num = num
                    min_label = label
                    flag = True
                self.local_complement(label, 1)
            if flag:
                self.local_complement(min_label, 1)
            counter += 1

    def count_edge_num(self):
        num = 0
        for links in self.edges.values():
            num += len(links)
        return num

    def extract_topological_order(self) -> List[any]:
        order = []
        todo = set(self.nodes.keys())
        while len(todo) > 0:
            stack = [todo.pop()]
            while len(stack) > 0:
                curr = stack[-1]
                flag = True
                for prev in self.nodes[curr].corrections.keys():
                    if prev in todo:
                        stack.append(prev)
                        flag = False
                        todo.remove(prev)
                if flag:
                    order.append(stack.pop())
        return order

    def render_temporal_order(self):
        g = graphviz.Digraph()
        with g.subgraph(name='cluster_0') as c:
            c.attr("node", shape="box")
            for label in self.input:
                c.node(str(label), label=self.nodes[label].__repr__())
            c.attr(label='input')
        with g.subgraph(name='cluster_1') as c:
            c.attr("node", shape="box")
            for label in self.output:
                c.node(str(label), label=self.nodes[label].__repr__())
            c.attr(label='output')

        with g.subgraph(name='cluster_2') as c:
            c.attr("node", shape="box")
            for label, node in self.nodes.items():
                if label not in self.input and label not in self.output:
                    c.node(str(label), label=node.__repr__())
            c.attr(label='intermediate')
        for label, node in self.nodes.items():
            for source, operator in node.corrections.items():
                g.edge(str(source), str(label))
        g.view()

    def render(self, **config):
        visited_edge: Set[(any, any)] = set()
        g = graphviz.Graph(format='png')

        with g.subgraph() as c:
            c.attr("node", shape="box")
            c.attr(rank="same")
            for label in self.input:
                c.node(str(label), label=self.nodes[label].__repr__())
            c.attr(label='input')

        with g.subgraph() as c:
            c.attr("node", shape="box")
            c.attr(rank="same")
            for label in self.output:
                c.node(str(label), label=self.nodes[label].__repr__())
            c.attr(label='output')

        with g.subgraph() as c:
            c.attr("node", shape="box")
            for label, node in self.nodes.items():
                if label not in self.input and label not in self.output:
                    c.node(str(label), label=node.__repr__())
            c.attr(label='intermediate')

        for label, node in self.nodes.items():
            for other_label in self.edges[label]:
                if (other_label, label) not in visited_edge:
                    g.edge(str(label), str(other_label))
                    visited_edge.add((label, other_label))
        g.view(filename="demo_circ", directory="./../cache")
