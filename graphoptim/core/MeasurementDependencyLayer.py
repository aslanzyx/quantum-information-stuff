import networkx as nx


class MeasurementDependencyLayer:
    def __init__(self, dependency_graph: nx.DiGraph):
        self.G = dependency_graph

    def measureable_nodes(self):
        pass