from typing import List, Set, Dict

from graphoptim.graph_state import Node, BlochSphere
import networkx as nx
import numpy as np


class GraphState:
    def __init__(self, G, dag, pos, bases):
        self.G: nx.Graph = G
        self.dag: nx.DiGraph = dag
        self.pos: Dict[any, (int, int)] = pos
        self.bases: Dict[any, Node] = bases
        self.corrections: Dict[any, Set[BlochSphere]] = dict()

    def local_complement(self, label: any, direction: int):
        """
        Perform local complementation
        """
        # Update Geometry
        neighbours = list(self.G.neighbors(label))
        edges = self.G.edges()
        for i in range(len(neighbours)):
            ni = neighbours[i]
            for j in range(i + 1, len(neighbours)):
                nj = neighbours[j]
                if (ni, nj) in edges or (nj, ni) in edges:
                    self.G.remove_edge(ni, nj)
                else:
                    self.G.add_edge(ni, nj)
        # Merge measurement bases
        self.bases[label].merge_sqrt_x(direction)
        for ni in neighbours:
            self.bases[ni].merge_sqrt_z(-direction)

    def x_measurement(self, label: any, direction: int, b: any = None) -> None:
        """
        Perform X-based measurement on given node
        """

        # select b
        if b is None:
            neighbours = list(self.G.neighbors(label))
            # In case current node is disconnected
            if len(neighbours) == 0:
                self.z_measurement(label, direction)
                return
            neighbours.sort()
            b = neighbours[0]
        self.local_complement(b, direction)
        self.y_measurement(label, direction)

    def y_measurement(self, label: int, direction: int) -> None:
        """
        Perform Y-based measurement on given node
        """
        self.local_complement(label, -direction)
        self.z_measurement(label, direction)

    def z_measurement(self, label: any, direction: int) -> None:
        """
        Perform Z-based measurement on given node
        """
        if direction == -1:
            for ni in self.G.neighbors(label):
                self.bases[ni].merge_z()
        # Remove the node
        self.G.remove_node(label)
        self.bases.pop(label)
        self.dag.remove_node(label)

    def draw(self) -> None:
        labels = {ni: self.bases[ni].__repr__() for ni in self.G.nodes()}
        # nx.draw(self.G, pos=self.pos, labels=labels,
                # node_color='w', node_size=1e3, edgecolors='k')
        nx.draw(self.G, pos=self.pos,
                node_color='w', node_size=1e1, edgecolors='k')

    def draw_circular(self) -> None:
        labels = {ni: self.bases[ni].__repr__() for ni in self.G.nodes()}
        nx.draw_circular(self.G, labels=labels,
                         node_color='w', node_size=1e3, edgecolors='k')

    def measure(self, label: int) -> None:
        base, direction = self.bases[label].base.to_pauli()
        base = base.lower()
        if base == 'x':
            self.x_measurement(label, direction)
        elif base == 'y':
            self.y_measurement(label, direction)
        elif base == 'z':
            self.z_measurement(label, direction)

    def extract_edge_matrix(self) -> (np.ndarray, List[any]):
        """
        Extract the edge matrix of the graph state.
        :return: nxn matrix, label register
        """
        n: int = self.G.size()
        retval: np.ndarray = np.zeros((n, n))
        label2idx: Dict[any, int] = dict()
        label_reg: List[any] = list()
        i = 0
        for node in self.G.nodes():
            label2idx[node] = i
            label_reg.append(node)
            i += 1
        for u, v in self.G.edges():
            u = label2idx[u]
            v = label2idx[v]
            retval[u][v] = 1
            retval[v][u] = 1
        return retval, label_reg

    def eliminate_pauli(self) -> None:
        """
        Eliminate all pauli-based measurements
        """
        nodes = list(self.bases.items())
        nodes.sort()
        for label, node in nodes:
            if node.base.is_pauli():
                self.measure(label)

    # def extract_dag(self) -> Dict[any, Set[any]]:
    #     edges: Dict[any, Set[any]] = dict()
    #     for curr, node in self.nodes.items():
    #         for prev in node.corrections.keys():
    #             if prev in edges:
    #                 edges[prev] = set()
    #             edges[prev].add(curr)
    #     return edges
    #
    # def partition(self):
    #     todo = set(self.nodes.keys())
    #     partition = dict()
    #     while len(todo) > 0:
    #         for label in list(todo):
    #             flag = True
    #             set_id = 0
    #             for source in self.nodes[label].corrections.keys():
    #                 if source not in partition:
    #                     flag = False
    #                     break
    #                 set_id = max(partition[source] + 1, set_id)
    #             if flag:
    #                 partition[label] = set_id
    #                 todo.remove(label)
    #     return partition
    #
    # def minimize_edge(self, max_out=100):
    #     counter = 0
    #     flag = True
    #     min_label = None
    #     min_num = self.count_edge_num()
    #     while counter < max_out and flag:
    #         flag = False
    #         for label in self.nodes.keys():
    #             self.local_complement(label, 1)
    #             num = self.count_edge_num()
    #             if min_num is None or num < min_num:
    #                 min_num = num
    #                 min_label = label
    #                 flag = True
    #             self.local_complement(label, 1)
    #         if flag:
    #             self.local_complement(min_label, 1)
    #         counter += 1
    #
    # def count_edge_num(self):
    #     num = 0
    #     for links in self.edges.values():
    #         num += len(links)
    #     return num
    #
    # def extract_topological_order(self) -> List[any]:
    #     order = []
    #     todo = set(self.nodes.keys())
    #     while len(todo) > 0:
    #         stack = [todo.pop()]
    #         while len(stack) > 0:
    #             curr = stack[-1]
    #             flag = True
    #             for prev in self.nodes[curr].corrections.keys():
    #                 if prev in todo:
    #                     stack.append(prev)
    #                     flag = False
    #                     todo.remove(prev)
    #             if flag:
    #                 order.append(stack.pop())
    #     return order
