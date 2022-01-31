from math import pi
from typing import List, Set, Dict
import networkx as nx
import numpy as np

from .BlochSphere import BlochSphere
from .Utils import is_pauli_angle


class ClusterState:
    """
    Cluster state
    Data Struct:
        array of stacks to store single rotation gates
        set to store CNOT-edges
    TODO: test corrections
    TODO: implement corrections for cnot
    """

    def __init__(self, size):
        self.size = size
        self.cluster_stacks: List[List[float]] = [[]] * size
        self.stack_ptrs: List[int] = [0] * size
        self.cnot_edges: Set[((int, int), (int, int))] = set()
        self.corrections: List[Set[(BlochSphere, (int, int))]] = [set()] * size
        self.dependencies: Dict[(int, int), Set[(int, int)]] = dict()

        self._finalized = False

    def add_rotation_sequence(self, wire_id: int, angles: List[float]) -> None:
        for angle in angles:
            self.cluster_stacks[wire_id].append(angle)
            # Process corrections
            if is_pauli_angle(angle):
                # Propagate corrections if Pauli
                for correction, _ in self.corrections[wire_id]:
                    correction.rotate_z(-angle)
                    correction.rotate_h()
            else:
                # Add dependencies if non-Pauli
                for correction, source in self.corrections[wire_id]:
                    if correction.pauli_base() != 'z':
                        self.dependencies[source].add((wire_id, self.stack_ptrs[wire_id]))
                # Add new correction source
                new_source = (wire_id, self.stack_ptrs[wire_id])
                self.corrections[wire_id].add((BlochSphere(), new_source))
                self.dependencies[new_source] = set()
            # Update stack pointer
            self.stack_ptrs[wire_id] += 1

    def cnot(self, control_id: int, target_id: int) -> None:
        # Add cnot edge
        self.cnot_edges.add(
            ((control_id, self.stack_ptrs[control_id]),
             (target_id, self.stack_ptrs[target_id] - 1))
        )
        # Process corrections
        for correction, source in self.corrections[control_id]:
            if correction.pauli_base() != 'z':
                self.corrections[target_id].add((
                    BlochSphere(np.array([1, 0, 0])), source))
        for correction, source in self.corrections[target_id]:
            if correction.pauli_base() != 'x':
                self.corrections[control_id].add((BlochSphere(), source))

    def rx(self, wire_id: int, angle: float) -> None:
        self.add_rotation_sequence(wire_id, [0, angle])

    def rz(self, wire_id: int, angle: float) -> None:
        self.add_rotation_sequence(wire_id, [angle, 0])

    def x(self, wire_id: int) -> None:
        self.rx(wire_id, pi)

    def z(self, wire_id: int) -> None:
        self.rz(wire_id, pi)

    def s(self, wire_id: int) -> None:
        self.rz(wire_id, pi / 2)

    def t(self, wire_id: int) -> None:
        self.rz(wire_id, pi / 4)

    def h(self, wire_id: int) -> None:
        self.add_rotation_sequence(wire_id, [0])

    def add_outputs(self) -> None:
        if self._finalized:
            print("Output layer has already been added.")
        else:
            for i in range(self.size):
                # Add output node
                self.cluster_stacks[i].append(0)
                # Process measurement dependencies
                for correction, source in self.corrections[i]:
                    if correction.pauli_base() != 'z':
                        self.dependencies[source].add((i, self.stack_ptrs[i]))
                self._finalized = True

    def to_graph_state(self):
        # Create variables for constructing graph state
        geometry_graph = nx.Graph()
        dependency_graph = nx.DiGraph()
        angle_map: Dict[(int, int), float] = dict()
        # Finalize the cluster state
        self.add_outputs()
        # Add wires
        for i in range(self.size):
            for j in range(self.stack_ptrs[i]):
                geometry_graph.add_edge((i, j), (i, j + 1))
                angle_map[(i, j)] = self.cluster_stacks[i][j]
        # Add CNOT-edges
        for u, v in self.cnot_edges:
            geometry_graph.add_edge(u, v)
        # Construct dependency graph
        for source, targets in self.dependencies.items():
            for target in targets:
                dependency_graph.add_edge(source, target)
