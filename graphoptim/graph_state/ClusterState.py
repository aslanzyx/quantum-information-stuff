from typing import List, Set, Dict
from graphoptim.graph_state import GraphState, PauliOperator, Node


class ClusterState:
    def __init__(self, size):
        self.lines: List[List[str]] = [[] for line in range(size)]
        self.entanglement: Set[(int, int, int, int)] = set()

    def add_x(self, reg):
        self.lines[reg].append('X')
        self.lines[reg].append('-X')

    def add_z(self, reg):
        self.lines[reg].append('-X')
        self.lines[reg].append('X')

    def add_y(self, reg):
        self.lines[reg].append('-X')
        self.lines[reg].append('-X')

    def add_t(self, reg):
        self.lines[reg].append('T')
        self.lines[reg].append('X')

    def add_h(self, reg):
        self.lines[reg].append('X')
        self.lines[reg].append('Y')
        self.lines[reg].append('Y')
        self.lines[reg].append('Y')

    def add_s(self, reg):
        self.lines[reg].append('Y')
        self.lines[reg].append('X')

    def add_cont(self, control, target):
        self.lines[control] += ['-X', 'Y', 'Y', 'X', 'Y', 'Y']
        self.lines[target] += ['X', 'X', 'X', 'X', 'X', 'X']
        self.entanglement.add((control, len(self.lines[control]) - 3, target, len(self.lines[target]) - 3))

    def truncate_wire(self):
        pass

    # def temporal_order(self):
    #     corrections: Dict[(int, int), Set[(int, int)]] = dict()
    #     stack = []
    #     ptr = 0
    #     correction = PauliOperator('Z')
    #     corrections[(0, 0)] = set()
    #     for i in range(len(self.lines)):
    #         for j in range(len(self.lines[i])):
    #             if node == 'X':
    #                 continue
    #             elif node == 'Y':
    #                 ...
    #             elif node == 'T':
    #                 corrections[(ptr, 0)].add(())

    def to_graph_state(self):
        # Generate graph state
        graph_state = GraphState()
        # Create label to position map
        label_map = dict()
        acc = 0
        for i in range(len(self.lines)):
            for j in range(len(self.lines[i])):
                graph_state.add_node(Node(self.lines[i][j], acc))
                label_map[(i, j)] = acc
                acc += 1
            graph_state.set_input(label_map[(i, 0)])
            graph_state.set_input(label_map[(i, len(self.lines[i]) - 1)])
            for j in range(len(self.lines[i]) - 1):
                graph_state.add_edge(label_map[(i, j)], label_map[(i, j + 1)])
        # Create entanglement
        for i, j, k, l in self.entanglement:
            graph_state.add_edge(label_map[(i, j)], label_map[(k, l)])
        # Reason out temporal order
        # for i in range(len(self.lines)):
        #     correction = PauliOperator('Z')
        #     for j in range(len(self.lines[i])):
        #         if self.lines[i][j] == 'T':
        #             ...
        #         elif
