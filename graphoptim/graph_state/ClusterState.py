from typing import List, Set, Dict
from graphoptim.graph_state import GraphState, PauliOperator, Node


class ClusterState:
    def __init__(self, size):
        self.lines: List[List[str]] = [[] for line in range(size)]
        # self.entanglement: Dict[(int, int), (int, int)] = dict()
        self.entanglement: Set[(int, int, int, int)] = set()
        # self.buffer = [(PauliOperator('z'), i, 0) for i in range(size)]
        # self.corrections = dict()
        self.corrections: Dict[(int, int), Set[(PauliOperator, (int, int))]] = dict()
        self.operator_buffer: List[List[PauliOperator]] = [[] for i in range(size)]
        self.location_buffer: List[List[(int, int)]] = [[] for i in range(size)]

    def add_x(self, reg):
        self.lines[reg].append('X')
        self.lines[reg].append('-X')
        for i in range(len(self.operator_buffer[reg])):
            self.operator_buffer[reg][i].rotate_x()

    def add_z(self, reg):
        self.lines[reg].append('-X')
        self.lines[reg].append('X')
        # self.buffer[reg].rotate_z()
        for i in range(len(self.operator_buffer[reg])):
            self.operator_buffer[reg][i].rotate_z()

    def add_y(self, reg):
        self.lines[reg].append('-X')
        self.lines[reg].append('-X')
        # self.buffer[reg].rotate_y()
        for i in range(len(self.operator_buffer[reg])):
            self.operator_buffer[reg][i].rotate_y()

    def add_t(self, reg):
        ptr = len(self.lines[reg])
        self.lines[reg].append('T')
        self.lines[reg].append('X')
        # self.corrections[(reg, len(self.lines[reg]))] = self.buffer[reg]
        if ptr > 0:
            self.corrections[(reg, ptr)] = set()
            for i in range(len(self.operator_buffer[reg])):
                if self.operator_buffer[reg][i].to_base()[0] != 'Z':
                    self.corrections[(reg, ptr)].add((PauliOperator('X'), self.location_buffer[reg][i]))
            self.operator_buffer[reg].append(PauliOperator('z'))
            self.location_buffer[reg].append((reg, ptr))
        # print(self.operator_buffer)
        # print(self.location_buffer)

    def add_h(self, reg):
        self.lines[reg].append('X')
        self.lines[reg].append('Y')
        self.lines[reg].append('Y')
        self.lines[reg].append('Y')
        # self.buffer[reg].rotate_sqrt_x(1)
        # self.buffer[reg].rotate_sqrt_z(1)
        # self.buffer[reg].rotate_sqrt_x(1)
        for i in range(len(self.operator_buffer[reg])):
            self.operator_buffer[reg][i].rotate_sqrt_x(1)
            self.operator_buffer[reg][i].rotate_sqrt_z(1)
            self.operator_buffer[reg][i].rotate_sqrt_x(1)

    def add_s(self, reg):
        self.lines[reg].append('Y')
        self.lines[reg].append('X')
        # self.buffer[reg].rotate_sqrt_z(1)
        for i in range(len(self.operator_buffer[reg])):
            self.operator_buffer[reg][i].rotate_sqrt_z(1)

    def add_cnot(self, control, target):
        self.lines[control] += ['-X', 'Y', 'Y', 'X', 'Y', 'Y']
        self.lines[target] += ['X', 'X', 'X', 'X', 'X', 'X']
        self.entanglement.add((control, len(self.lines[control]) - 3, target, len(self.lines[target]) - 3))
        # self.entanglement[(control, len(self.lines[control]) - 3)] = (target, len(self.lines[target]) - 3)
        # self.entanglement[(target, len(self.lines[target]) - 3)] = (control, len(self.lines[control]) - 3)
        # if self.buffer[target].to_base() == 'x':
        #     self.buffer[control] =
        # self.buffer[control].rotate_z()

        # Obtain control & target corrections
        control_corrections: List[(PauliOperator, (int, int))] = [
            (self.operator_buffer[control][i], self.location_buffer[control][i])
            for i in range(len(self.operator_buffer[control]))
        ]
        target_corrections: List[(PauliOperator, (int, int))] = [
            (self.operator_buffer[target][i], self.location_buffer[target][i])
            for i in range(len(self.operator_buffer[target]))
        ]
        for i in range(len(control_corrections)):
            correction, location = control_corrections[i]
            if correction.to_base() != 'Z':
                self.operator_buffer[target].append(PauliOperator('X'))
                self.location_buffer[target].append(location)

        for i in range(len(target_corrections)):
            correction, location = target_corrections[i]
            if correction.to_base() != 'X':
                self.operator_buffer[control].append(PauliOperator('Z'))
                self.location_buffer[control].append(location)

    def add_cz(self, control, target):
        self.add_h(target)
        self.add_cnot(control, target)
        self.add_h(target)

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

    def finalize_buffer(self):
        for i in range(len(self.operator_buffer)):
            location = (i, len(self.lines[i]))
            if location not in self.corrections:
                self.corrections[location] = set()
            for j in range(len(self.operator_buffer[i])):
                if self.operator_buffer[i][j].to_base()[0] != 'Z':
                    self.corrections[location].add((self.operator_buffer[i][j], self.location_buffer[i][j]))
            self.operator_buffer[i] = []
            self.location_buffer[i] = []

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
            graph_state.add_node(Node('z', acc))
            label_map[(i, len(self.lines[i]))] = acc
            acc += 1
            graph_state.set_input(label_map[(i, 0)])
            graph_state.set_output(label_map[(i, len(self.lines[i]))])
            for j in range(len(self.lines[i])):
                graph_state.add_edge(label_map[(i, j)], label_map[(i, j + 1)])
        # Create entanglement
        for i, j, k, l in self.entanglement:
            graph_state.add_edge(label_map[(i, j)], label_map[(k, l)])

        self.finalize_buffer()
        for location, corrections in self.corrections.items():
            for correction, source in corrections:
                n = graph_state.get_node(label_map[location])
                n.add_correction(correction.to_base()[0], label_map[source])
        return graph_state
        # Reason out temporal order
        # for i in range(len(self.lines)):
        #     correction = PauliOperator('Z')
        #     for j in range(len(self.lines[i])):
        #         if self.lines[i][j] == 'T':
        #             ...
        #         elif
        # for i in range(len(self.lines)):
        #     stack = [(i, 0)]
        #     while len(stack) > 0:
        #         line_id, source_ptr = stack.pop()
        #         correction = PauliOperator('Z')
        #         ptr = source_ptr + 1
        #         while ptr < len(self.lines[line_id]):
        #             if self.lines[line_id][ptr] == 'T':
        #                 label = label_map[(line_id, ptr)]
        #                 graph_state.get_node(label).add_correction(correction, label_map[(line_id, source_ptr)])
        #             if (line_id, ptr + 3) in self.entanglement.keys():
        #                 ptr += 6

    # def temporal_order(self, graph_state: GraphState, label_map: Dict[(int, int), int]):
    #     def dfs(source, correction: PauliOperator, start):
    #         idx, ptr = start
    #         line = self.lines[idx]
    #         bound = len(line)
    #         ptr += 1
    #         while ptr < bound:
    #             if line[ptr] == 'T':
    #                 graph_state.get_node(source).add_correction()
    #                 pass
    #             elif (idx, ptr + 3) in self.entanglement.keys():
    #                 ...
    #             elif line[ptr] == 'Y':
    #                 correction.rotate_sqrt_z(1)
    #             elif line[ptr] == '-X':
    #                 correction.rotate_z()
    #             else:
    #                 correction.rotate_sqrt_z(-1)
    #             ptr += 1
