from typing import List, Set, Dict
from math import pi
import networkx as nx
from . import GraphState, Node


class ClusterState:
    """
    Cluster state
    """

    def __init__(self, size):
        # A map between locations to measurement base
        self._angle_map: Dict[(int, int), float] = dict()
        # Stack pointer
        self._stack_ptrs: List = [0]*size
        # Graph buffer object
        self._G = nx.Graph()
        self._correction_reg: List[List[int]] = [set()]*size
        # Register size
        self.size = size

    def add_rotation_sequence(self, wire_id: int, angle_arr: List[float]) -> None:
        """
        Add a series of single unitary rotations to a space-like wire
        """
        # Obtain the top pointer of the stack
        ptr = self._stack_ptrs[wire_id]
        # Add each single qubit rotation
        for angle in angle_arr:
            self._angle_map[(ptr, wire_id)] = angle
            self._G.add_edge((ptr, wire_id), (ptr+1, wire_id))
            ptr += 1
        # Update the stack pointers
        self._stack_ptrs[wire_id] = ptr

    def cnot(self, target_id: int, control_id: int) -> None:
        """
        Apply CNOT gate
        """
        # Get the stack pointers
        target_ptr = self._stack_ptrs[target_id]
        control_ptr = self._stack_ptrs[control_id]
        # Add iter-wire edge
        self._G.add_edge((target_ptr+3, target_id),
                         (control_ptr+3, control_id))
        # Add rotations
        self.add_rotation_sequence(
            target_id, [pi, pi/2, pi/2, 0, pi/2, pi/2])
        self.add_rotation_sequence(
            control_id, [0, 0, 0, 0, 0, 0])

    def x(self, wire_id) -> None:
        self.add_rotation_sequence(wire_id, [0, pi])

    def z(self, wire_id) -> None:
        self.add_rotation_sequence(wire_id, [pi, 0])

    def s(self, wire_id) -> None:
        self.add_rotation_sequence(wire_id, [pi/2, 0])

    def rx(self, wire_id, angle) -> None:
        self.add_rotation_sequence(wire_id, [0, angle])

    def rz(self, wire_id, angle) -> None:
        self.add_rotation_sequence(wire_id, [angle, 0])

    def h(self, wire_id) -> None:
        self.add_rotation_sequence(wire_id, [0, pi/2, pi/2, pi/2])

    def t(self, wire_id) -> None:
        self.add_rotation_sequence(wire_id, [pi/4, 0])

    def measurement_dependencies(self):
        corrections: Dict[(int, int), Set[(int, int)]] = dict()

    def draw(self) -> None:
        labels = {
            label: "{:.2f}".format(self._angle_map[label]) if label in self._angle_map else 'out{}'.format(label[1]) for label in self._G.nodes()}
        pos = {label: label for label in self._G.nodes()}
        nx.draw(self._G, pos=pos, labels=labels, width=1,
                node_color='w', node_size=1e3, edgecolors='k')

    def to_graph_state(self) -> GraphState:
        angles = self._angle_map
        for line in range(self.size):
            ptr = self._stack_ptrs[line]
            angles[(ptr, line)] = None

        pos = {node: node for node in self._G.nodes()}
        bases = dict()
        for ni in self._G.nodes():
            bases[ni] = Node(angles[ni], ni)
        dag = nx.DiGraph(self._G)
        return GraphState(self._G, dag, pos, bases)

    # def add_x(self, reg):
    #     self.lines[reg].append('X')
    #     self.lines[reg].append('-X')
    #     for i in range(len(self.operator_buffer[reg])):
    #         self.operator_buffer[reg][i].rotate_x()

    # def add_z(self, reg):
    #     self.lines[reg].append('-X')
    #     self.lines[reg].append('X')
    #     # self.buffer[reg].rotate_z()
    #     for i in range(len(self.operator_buffer[reg])):
    #         self.operator_buffer[reg][i].rotate_z()

    # def add_y(self, reg):
    #     self.lines[reg].append('-X')
    #     self.lines[reg].append('-X')
    #     # self.buffer[reg].rotate_y()
    #     for i in range(len(self.operator_buffer[reg])):
    #         self.operator_buffer[reg][i].rotate_y()

    # def add_t(self, reg):
    #     ptr = len(self.lines[reg])
    #     self.lines[reg].append('T')
    #     self.lines[reg].append('X')
    #     if ptr > 0:
    #         self.corrections[(reg, ptr)] = set()
    #         for i in range(len(self.operator_buffer[reg])):
    #             if self.operator_buffer[reg][i].to_base()[0] != 'Z':
    #                 self.corrections[(reg, ptr)].add(
    #                     (PauliOperator('X'), self.location_buffer[reg][i]))
    #         self.operator_buffer[reg].append(PauliOperator('z'))
    #         self.location_buffer[reg].append((reg, ptr))

    # def add_h(self, reg):
    #     self.lines[reg].append('X')
    #     self.lines[reg].append('Y')
    #     self.lines[reg].append('Y')
    #     self.lines[reg].append('Y')
    #     for i in range(len(self.operator_buffer[reg])):
    #         self.operator_buffer[reg][i].rotate_sqrt_x(1)
    #         self.operator_buffer[reg][i].rotate_sqrt_z(1)
    #         self.operator_buffer[reg][i].rotate_sqrt_x(1)

    # def add_s(self, reg):
    #     self.lines[reg].append('Y')
    #     self.lines[reg].append('X')
    #     for i in range(len(self.operator_buffer[reg])):
    #         self.operator_buffer[reg][i].rotate_sqrt_z(1)

    # def add_cnot(self, control, target):
    #     self.lines[control] += ['-X', 'Y', 'Y', 'X', 'Y', 'Y']
    #     self.lines[target] += ['X', 'X', 'X', 'X', 'X', 'X']
    #     self.entanglement.add(
    #         (control, len(self.lines[control]) - 3, target, len(self.lines[target]) - 3))
    #     # Obtain control & target corrections
    #     control_corrections: List[(PauliOperator, (int, int))] = [
    #         (self.operator_buffer[control][i],
    #          self.location_buffer[control][i])
    #         for i in range(len(self.operator_buffer[control]))
    #     ]
    #     target_corrections: List[(PauliOperator, (int, int))] = [
    #         (self.operator_buffer[target][i], self.location_buffer[target][i])
    #         for i in range(len(self.operator_buffer[target]))
    #     ]
    #     for i in range(len(control_corrections)):
    #         correction, location = control_corrections[i]
    #         if correction.to_base() != 'Z':
    #             self.operator_buffer[target].append(PauliOperator('X'))
    #             self.location_buffer[target].append(location)

    #     for i in range(len(target_corrections)):
    #         correction, location = target_corrections[i]
    #         if correction.to_base() != 'X':
    #             self.operator_buffer[control].append(PauliOperator('Z'))
    #             self.location_buffer[control].append(location)

    # def add_cz(self, control, target):
    #     self.add_h(target)
    #     self.add_cnot(control, target)
    #     self.add_h(target)

    # def truncate_wire(self):
    #     pass

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

    # def finalize_buffer(self):
    #     for i in range(len(self.operator_buffer)):
    #         location = (i, len(self.lines[i]))
    #         if location not in self.corrections:
    #             self.corrections[location] = set()
    #         for j in range(len(self.operator_buffer[i])):
    #             if self.operator_buffer[i][j].to_base()[0] != 'Z':
    #                 self.corrections[location].add(
    #                     (self.operator_buffer[i][j], self.location_buffer[i][j]))
    #         self.operator_buffer[i] = []
    #         self.location_buffer[i] = []

    # def to_graph_state(self):
    #     # Generate graph state
    #     graph_state = GraphState()
    #     # Create label to position map
    #     label_map = dict()
    #     acc = 0
    #     for i in range(len(self.lines)):
    #         for j in range(len(self.lines[i])):
    #             graph_state.add_node(Node(self.lines[i][j], acc))
    #             label_map[(i, j)] = acc
    #             acc += 1
    #         graph_state.add_node(Node('z', acc))
    #         label_map[(i, len(self.lines[i]))] = acc
    #         acc += 1
    #         graph_state.set_input(label_map[(i, 0)])
    #         graph_state.set_output(label_map[(i, len(self.lines[i]))])
    #         for j in range(len(self.lines[i])):
    #             graph_state.add_edge(label_map[(i, j)], label_map[(i, j + 1)])
    #     # Create entanglement
    #     for i, j, k, l in self.entanglement:
    #         graph_state.add_edge(label_map[(i, j)], label_map[(k, l)])

    #     self.finalize_buffer()
    #     for location, corrections in self.corrections.items():
    #         for correction, source in corrections:
    #             n = graph_state.get_node(label_map[location])
    #             n.add_correction(correction.to_base()[0], label_map[source])
    #     return graph_state
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
