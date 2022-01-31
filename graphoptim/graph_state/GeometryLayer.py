from typing import List, Dict

import networkx as nx
import numpy as np


class GeometryLayer:
    def __init__(self, g: nx.Graph):
        self.G: nx.Graph = g

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
