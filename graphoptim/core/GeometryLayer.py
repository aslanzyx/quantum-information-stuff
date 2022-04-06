from typing import List, Dict, Set

import networkx as nx
import numpy as np


class GeometryLayer:
    def __init__(self, geometry_graph: nx.Graph):
        self.G: nx.Graph = geometry_graph

    def local_complement(self, label: any) -> None:
        """
        Local complement the graph geometry about the node with given label.
        :param label: label to perform local complementation about.
        """
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

    def cutoff(self, label: any) -> None:
        """
        Cutoff the node with given label.
        :param label: label of the node to cutoff.
        """
        self.G.remove_node(label)

    def boundary_nodes(self, nodes: Set[any]) -> Set[any]:
        boundary: Set[any] = set()
        for node in nodes:
            boundary = boundary.union(self.neighbours(node))
        return boundary

    def neighbours(self, node: any) -> Set[any]:
        return set(self.G.neighbors(node))

    def isolated(self, label):
        return len(self.neighbours(label)) == 0

    def nodes(self) -> List[any]:
        return list(self.G.nodes())

    def degree(self, nodes: any) -> any:
        return self.G.degree(nodes)

    def max_degree_nodes(self, search_set=None) -> (Set[any], int):
        nodes: Set[any] = set()
        max_degree: int = 0

        if search_set is None:
            search_set = self.nodes()

        for node in search_set:
            node_degree: int = self.degree(node)
            if node_degree > max_degree:
                max_degree = node_degree
                nodes.clear()
            if node_degree == max_degree:
                nodes.add(node)

        return nodes, max_degree

    def is_isomorphic(self, H: nx.Graph) -> bool:
        return nx.is_isomorphic(self.G, H)

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

    def draw(self):
        nx.draw(self.G, pos=nx.circular_layout(self.G),
                node_color='w', node_size=50, edgecolors='k')