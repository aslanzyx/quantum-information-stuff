from typing import List, Set, Dict

import networkx as nx
import numpy as np

from graphoptim.core import GeometryLayer, GraphState


# TODO:
# Optimize performance
class GeometryOptimizer:
    def __init__(self, geometry: GeometryLayer, max_depth: int = 100):

        self.optimized_idx = 0
        self.minimax_degree = np.inf

        self.max_depth = max_depth
        self.depth = 0

        self.current_graph_idx = 0
        self.current_geometry = geometry

        self.graph_traversed: List[nx.Graph] = []
        self.lc_map: List[(int, any)] = []

    def has_isomorphic(self):
        for H in self.graph_traversed:
            if self.current_geometry.is_isomorphic(H):
                return True
        return False

    def lc_delta(self, node: any) -> (Dict[any, int], Set[any], int):

        search_set = self.current_geometry.neighbours(node)
        delta: Dict[any, int] = {node: degree for node, degree in
                                 self.current_geometry.nodes(search_set)}
        self.current_geometry.local_complement(node)
        for node, degree in self.current_geometry.nodes(search_set):
            delta[node] = degree - delta[node]
        self.current_geometry.local_complement(node)

        return delta, self.current_geometry.max_degree_nodes(self.current_geometry.G, search_set)

    def execute(self):
        """
        Traverse through nodes
        :return:
        """

        max_degree_nodes, max_degree = self.current_geometry.max_degree_nodes()
        # lc_nodes_todo = self.current_geometry.boundary_nodes(max_degree_nodes)
        lc_nodes_todo = list(self.current_geometry.nodes())
        cur_id = len(self.lc_map) - 1

        if max_degree < self.minimax_degree:
            self.optimized_idx = cur_id
            self.minimax_degree = max_degree

        # Compute metadata for LC graphs on each node
        metadata: List[(any, int)] = []
        for node in lc_nodes_todo:
            self.current_geometry.local_complement(node)
            _, degree = self.current_geometry.max_degree_nodes()
            self.current_geometry.local_complement(node)
            # if degree < max_degree:
            metadata.append((node, degree))

        metadata.sort(key=lambda meta: meta[1])

        self.depth += 1
        if self.depth == 500:
            return

        for node, _ in metadata:
            self.current_geometry.local_complement(node)
            if not self.has_isomorphic() and self.depth < self.max_depth:
                # DP: record current geometry
                self.lc_map.append((cur_id, node))
                self.graph_traversed.append(nx.Graph.copy(self.current_geometry.G))

                # DFS recursion
                self.execute()
            self.current_geometry.local_complement(node)

    def optimized_lc_sequence(self) -> List[any]:
        ptr: int = self.optimized_idx
        sequence: List[any] = []

        while ptr >= 0:
            ptr, node = self.lc_map[ptr]
            sequence.append(node)

        return sequence[::-1]
