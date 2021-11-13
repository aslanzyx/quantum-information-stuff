import numpy as np
from typing import List
from graphoptim.graph_state import MeasurementBase, GraphState


# X -> [+X][-X]
# Z -> [-X][+X]
# H -> [+X][+Y][+Y][+Y]
# S -> [+Y][+X]
# T -> [+T][+X]
# CNOT -> [+X][+Y][+Y][+X][+Y][+Y]
#                     ||||
#         [+X][+X][+X][+X][+X][+X]

class ClusterState:
    NAN = 0
    X_BASE = 1
    Y_BASE = 2
    T_BASE = 3
    ENTANGLE_REL = 4

    def __init__(self, reg_size: int):
        self.cluster: np.ndarray = np.zeros((reg_size, 1))
        self.line_ptrs: np.ndarray = np.zeros(reg_size)
        self.entanglement_reg: set = set()

    def add_rotation(self, operator, reg_id):
        if operator == 'x':
            self.add_x(reg_id)
        elif operator == 'z':
            self.add_z(reg_id)
        elif operator == 's':
            self.add_s(reg_id)
        elif operator == 't':
            self.add_t(reg_id)
        elif operator == 'h':
            self.add_h(reg_id)
        else:
            print("Not available")

    def add_cnot(self, control_id: int, target_id: int) -> None:
        # compute the proper location to append the gate and update the pointers
        j = max(self.line_ptrs[control_id], self.line_ptrs[target_id])
        self.line_ptrs[control_id] = j
        self.line_ptrs[target_id] = j

        self.add_sequence(control_id, [ClusterState.X_BASE, ClusterState.Y_BASE, ClusterState.Y_BASE,
                                       ClusterState.Y_BASE, ClusterState.Y_BASE, ClusterState.Y_BASE])
        self.add_sequence(target_id, [ClusterState.X_BASE, ClusterState.X_BASE, ClusterState.X_BASE,
                                      ClusterState.Y_BASE, ClusterState.X_BASE, ClusterState.X_BASE])
        self.entanglement_reg.add((control_id, target_id, j + 3))

        for i in range(control_id + 1, target_id, 2):
            self.cluster[i, j] = ClusterState.ENTANGLE_REL

    def add_h(self, reg_id: int) -> None:
        """
        Append Hadarmard gate to qubit with given index
        :param reg_id: register index of the qubit
        """
        self.add_sequence(reg_id, [ClusterState.X_BASE, ClusterState.Y_BASE,
                                   ClusterState.Y_BASE, ClusterState.Y_BASE])

    def add_x(self, reg_id: int) -> None:
        self.add_sequence(reg_id, [ClusterState.X_BASE, -ClusterState.X_BASE])

    def add_z(self, reg_id: int) -> None:
        self.add_sequence(reg_id, [-ClusterState.X_BASE, ClusterState.X_BASE])

    def add_s(self, reg_id: int) -> None:
        self.add_sequence(reg_id, [ClusterState.Y_BASE, ClusterState.X_BASE])

    def add_t(self, reg_id: int) -> None:
        self.add_sequence(reg_id, [ClusterState.T_BASE, ClusterState.X_BASE])

    def add_sequence(self, reg_id: int, sequence: List[int]) -> None:
        self.check_max_out(reg_id)
        ptr = self.line_ptrs[reg_id]
        for j in range(len(sequence)):
            self.cluster[reg_id, ptr + j] = sequence[j]
        self.line_ptrs[reg_id] += len(sequence)

    def temporal_order(self):
        pass

    def to_graph_state(self) -> GraphState:
        pass

    def to_dag(self) -> (List[List[int]], List[MeasurementBase]):
        # Truncate first to remove residual wires
        self.truncate_x()

        # Allocate space for results
        dag: List[List[int]] = []
        measurement_bases: List[MeasurementBase] = []

        # Pointer to track the start index of each line
        ptr: int = 0

        # Iterate each line
        n, m = self.cluster.shape
        for i in range(n):

            # resolve measurement bases
            for j in range(m):
                if self.cluster[i, j] != ClusterState.NAN:
                    measurement_base = {
                        -ClusterState.X_BASE: MeasurementBase([-1, 0, 0]),
                        ClusterState.X_BASE: MeasurementBase([1, 0, 0]),
                        ClusterState.Y_BASE: MeasurementBase([0, 1, 0]),
                        ClusterState.T_BASE: MeasurementBase([1, 1, 0]),
                    }[self.cluster[i, j]]
                    measurement_bases.append(measurement_base)
                    dag.append([])

            # resolve edges within current line
            while ptr < len(measurement_bases) - 1:
                dag[ptr].append(ptr + 1)
                dag[ptr + 1].append(ptr)
                ptr += 1

            # update the pointer to next line
            ptr += 1

        # Iterate on each entanglement gates
        for control_id, target_id, j in self.entanglement_reg:
            measurement_bases.append(MeasurementBase([0, 1, 1]))
            dag.append([])

        return dag, measurement_bases

    def truncate_x(self) -> None:
        """
        Truncate all the adjacent X measurement to wire as they are just wires
        """
        n, m = self.cluster.shape
        for i in range(n):
            for j in range(m - 1):
                if self.cluster[i, j] == ClusterState.X_BASE and self.cluster[i, j + 1] == ClusterState.X_BASE:
                    self.cluster[i, j] = ClusterState.NAN
                    self.cluster[i, j + 1] = ClusterState.NAN

    def check_max_out(self, ptr: int):
        n, m = self.cluster.shape
        if ptr >= m:
            self.cluster = np.hstack(self.cluster, np.zeros((n, m)))

    def remove_redundency(self):
        j_max = max(self.line_ptrs)
        self.cluster = self.cluster[:, :j_max]

    def __repr__(self) -> str:
        n, m = self.cluster.shape
        out: str = ""
        for i in range(n):
            if i % 2 == 0:
                for j in range(m):
                    out += {
                        -ClusterState.Y_BASE: '[-Y]',
                        -ClusterState.X_BASE: '[-X]',
                        ClusterState.NAN: '----',
                        ClusterState.X_BASE: '[+X]',
                        ClusterState.Y_BASE: '[+Y]',
                        ClusterState.T_BASE: '[+T]'
                    }[self.cluster[i, j]]
            else:
                for j in range(m):
                    out += {
                        ClusterState.NAN: ' ' * 4,
                        ClusterState.ENTANGLE_REL: '||||'
                    }[self.cluster[i, j]]
            out += '\n'
        return out
