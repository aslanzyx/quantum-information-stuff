from typing import List, Set, Dict

import numpy as np

from graphoptim.graph_state import Node
import networkx as nx
import matplotlib.pyplot as plt


class GraphState:
    def __init__(self, G, dag, pos, bases):
        self.G: nx.Graph = G
        self.dag: nx.DiGraph = dag
        self.pos: Dict[any, (int, int)] = pos
        self.bases: Dict[any, Node] = bases

    def local_complement(self, label: any, direction: int):
        """
        Perform loca complementation
        """
        # Update Geometry
        neighbours = list(self.G.neighbors(label))
        edges = self.G.edges()
        for i in range(len(neighbours)):
            ni = neighbours[i]
            for j in range(i+1, len(neighbours)):
                nj = neighbours[j]
                if (ni, nj) in edges or (nj, ni) in edges:
                    self.G.remove_edge(ni, nj)
                else:
                    self.G.add_edge(ni, nj)
        # Merge measurement bases
        self.bases[label].merge_sqrt_x(direction)
        for ni in neighbours:
            self.bases[ni].merge_sqrt_z(-direction)

    def x_measurement(self, label: any, direction: int, b: any = None):
        """
        Perform X-based measurment on given node
        """
        # select b
        neighb = list(self.G.neighbors(label))
        neighb.sort()
        b = neighb[0]
        self.local_complement(b, direction)
        self.y_measurement(label, direction)

    def y_measurement(self, label: int, direction: int) -> None:
        """
        Perform Y-based measurment on given node
        """
        self.local_complement(label, -direction)
        self.z_measurement(label, direction)

    def z_measurement(self, label: any, direction: int) -> None:
        """
        Perform Z-based measurment on given node
        """
        if direction == -1:
            for ni in self.G.neighbors(label):
                self.bases[ni].merge_z()
        # Remove the node
        self.G.remove_node(label)
        self.bases.pop(label)
        self.dag.remove_node(label)

    def draw(self):
        labels = {ni: self.bases[ni].__repr__() for ni in self.G.nodes()}
        nx.draw(self.G, pos=self.pos, labels=labels,
                node_color='w', node_size=1e3, edgecolors='k')

    def draw_circular(self):
        labels = {ni: self.bases[ni].__repr__() for ni in self.G.nodes()}
        nx.draw_circular(self.G, labels=labels,
                         node_color='w', node_size=1e3, edgecolors='k')

    def measure(self, label: int):
        base, direction = self.bases[label].base.to_pauli()
        base = base.lower()
        if base == 'x':
            self.x_measurement(label, direction)
        elif base == 'y':
            self.y_measurement(label, direction)
        elif base == 'z':
            self.z_measurement(label, direction)

    def eliminate_pauli(self):
        nodes = list(self.bases.items())
        nodes.sort()
        #  for label, node in list(self.bases.items()):
        for label, node in nodes:
            if node.base.is_pauli():
                self.measure(label)
            #  self.draw()
            #  plt.show()

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
        # g.view()
        g = nx.DiGraph()
        for label, node in self.nodes.items():
            for source in node.corrections.keys():
                g.add_edge(source, label)
        # nx.draw_circular(g, node_color='k', node_size=100,
        #                  connectionstyle='arc3, rad = 0.1')
        # plt.show()
        return g

    def render(self, **config):
        # visited_edge: Set[(any, any)] = set()
        # g = graphviz.Graph(format='png')

        # with g.subgraph() as c:
        #     c.attr("node", shape="box")
        #     c.attr(rank="same")
        #     for label in self.input:
        #         c.node(str(label), label=self.nodes[label].__repr__())
        #     c.attr(label='input')

        # with g.subgraph() as c:
        #     c.attr("node", shape="box")
        #     c.attr(rank="same")
        #     for label in self.output:
        #         c.node(str(label), label=self.nodes[label].__repr__())
        #     c.attr(label='output')

        # with g.subgraph() as c:
        #     c.attr("node", shape="box")
        #     for label, node in self.nodes.items():
        #         if label not in self.input and label not in self.output:
        #             c.node(str(label), label=node.__repr__())
        #     c.attr(label='intermediate')

        # for label, node in self.nodes.items():
        #     for other_label in self.edges[label]:
        #         if (other_label, label) not in visited_edge:
        #             g.edge(str(label), str(other_label))
        #             visited_edge.add((label, other_label))
        # g.view(filename="demo_circ", directory="./../cache")

        g = nx.Graph()
        labels = dict()
        for label in self.edges.keys():
            labels[label] = self.nodes[label].__repr__()
            g.add_node(label)
            for other_label in self.edges[label]:
                g.add_edge(label, other_label)
        # nx.draw(g, node_color='k', node_size=100, pos=nx.circular_layout(g))
        # plt.show()
        return g
