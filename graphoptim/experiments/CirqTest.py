from typing import List, Dict

import numpy as np
from qiskit import QuantumCircuit, transpile, ClassicalRegister, QuantumRegister
from qiskit.providers.aer import QasmSimulator
from qiskit.visualization import plot_histogram
from math import pi
import networkx as nx
import matplotlib.pyplot as plt


def demo():
    simulator = QasmSimulator()
    circuit = QuantumCircuit(2, 2)

    circuit.h([0, 1])
    circuit.cz(0, 1)
    circuit.rz(pi / 8, 0)
    circuit.measure(0, 0)
    circuit.x(1).c_if(0, 1)
    circuit.measure(1, 1)

    compiled_circuit = transpile(circuit, simulator)
    job = simulator.run(compiled_circuit, shot=1000)
    result = job.result()
    counts = result.get_counts(compiled_circuit)

    print(circuit.draw())
    plot_histogram(counts)
    plt.show()


def compile(sequence: List[any],
            geometry: nx.Graph,
            correction_mask: Dict[any, List[any]],
            correction_bases: Dict[any, str],
            measurement_planes: Dict[any, str],
            measurement_angles: Dict[any, float],
            reg_size: int, graph_size: int):
    circuit = QuantumCircuit(reg_size, graph_size)
    qreg_map = dict()
    creg_map = {sequence[i]: i for i in range(graph_size)}
    free_qubit = set(range(reg_size))
    for node in sequence:
        # Allocate memory
        if node not in qreg_map:
            qreg_map[node] = free_qubit.pop()
            circuit.h(qreg_map[node])

        # Construct partial graph state
        # print(node, list(geometry.neighbors(node)), correction_mask)
        for next_node in geometry.neighbors(node):
            if next_node not in qreg_map:
                qreg_map[next_node] = free_qubit.pop()
                circuit.h(qreg_map[next_node])
            circuit.cz(qreg_map[node], qreg_map[next_node])

        # Process correction
        correction = circuit.x if correction_bases[node] == 'x' \
            else circuit.y if correction_bases[node] == 'y' else circuit.z
        for prev_node in correction_mask[node]:
            correction(qreg_map[node]).c_if(creg_map[prev_node], 1)

        # Measure node
        if measurement_planes[node] == "xy":
            circuit.rz(measurement_angles[node], qreg_map[node])
            circuit.h(qreg_map[node])
        elif measurement_planes[node] == "zy":
            circuit.rx(-measurement_angles[node], qreg_map[node])
        else:
            circuit.ry(measurement_angles[node], qreg_map[node])
        circuit.measure(qreg_map[node], creg_map[node])

        # Deallocate memory
        reg_id = qreg_map.pop(node)
        free_qubit.add(reg_id)
        circuit.barrier()
        circuit.reset(reg_id)
        geometry.remove_node(node)
    return circuit, creg_map


def process_outcomes(outome_counts: Dict[str, int],
                     creg_map: Dict[any, int],
                     outputs: List[any]):
    output_reg = [creg_map[node] for node in outputs]
    processed_counts: Dict[str, int] = dict()
    for word, count in outome_counts.items():
        masked_word = ''
        for reg_id in output_reg:
            masked_word += word[::-1][reg_id]
        if masked_word in processed_counts:
            processed_counts[masked_word] += count
        else:
            processed_counts[masked_word] = count
    return processed_counts


def linear_wire(n, angles: List[float]):
    # Construct graph
    g = nx.Graph()
    for i in range(n):
        g.add_edge(i, i + 1)

    # compile circuit
    circuit, creg_map = compile(sequence=[i for i in range(n + 1)],
                                geometry=g,
                                correction_mask={i: list(range((i + 1) % 2, i, 2)) for i in range(n + 1)},
                                correction_bases={i: 'x' for i in range(n + 1)},
                                measurement_planes={i: "zy" if i == n else "xy" for i in range(n + 1)},
                                measurement_angles={i: 0 if i == n else angles[i] for i in range(n + 1)},
                                reg_size=2, graph_size=n + 1)

    # Get results
    print(circuit.draw())
    simulator = QasmSimulator()
    qasm_circuit = transpile(circuit, simulator)
    job = simulator.run(qasm_circuit, shot=5000)
    result = job.result()
    counts = result.get_counts(qasm_circuit)
    processed_counts = process_outcomes(counts, creg_map, [n])
    plot_histogram(processed_counts)
    plt.show()

    # Compare with the circuit implementation
    circuit = QuantumCircuit(1, 1)
    parity = 0
    circuit.h(0)
    for angle in angles:
        if parity:
            circuit.rx(angle, 0)
        else:
            circuit.rz(angle, 0)
        parity ^= 1
    circuit.measure(0, 0)
    qasm_circuit = transpile(circuit, simulator)
    job = simulator.run(qasm_circuit, shot=5000)
    result = job.result()
    counts = result.get_counts(qasm_circuit)
    plot_histogram(counts)
    plt.show()


#
# linear_wire(6, [
#     0, pi / 3, pi / 8, pi / 2, 0, pi/16
# ])


def schedule(dependencies: nx.DiGraph,
             geometry: nx.Graph):
    # Allocate space for helper data
    degrees_in, _ = degrees(dependencies)
    qreg = set()  # virtual register
    queue = set()  # measurable queue
    sequence = []  # measurement sequence
    size = 0  # qubits required

    # loop until everything is measured
    while len(set(dependencies.nodes())) > 0:
        # Search for all measurable qubit
        for node in dependencies.nodes():
            if degrees_in[node] == 0:
                queue.add(node)
        # Search for the qubit to measure
        delta = np.inf
        node_min = None
        delta_set = set()
        for node in queue:
            delta_set = set(geometry.neighbors(node)).difference(qreg)
            if len(delta_set) < delta:
                delta = len(delta_set)
                node_min = node
        # Schedule the node
        size = min(size, delta)
        sequence.append(node_min)
        # Add the node and adjacent to the virtual register
        qreg.add(node_min)
        for node in delta_set:
            qreg.add(node)
            degrees_in[node] -= 1
        dependencies.remove_node(node_min)
    return sequence, size


def degrees(dependencies: nx.DiGraph) -> \
        (Dict[any, int], Dict[any, int]):
    degrees_in = {node: 0 for node in dependencies.nodes()}
    degrees_out = {node: 0 for node in dependencies.nodes()}
    for u, v in dependencies.edges():
        degrees_in[v] += 1
        degrees_out[u] += 1
    return degrees_in, degrees_out


def degree_delta(geometry: nx.Graph):
    delta: Dict[Dict[any, int]] = {node: {n: 0 for n in geometry.neighbors(node)}
                                   for node in geometry.nodes()}


def page_rank(dependencies: nx.DiGraph) -> List[any]:
    return []


g = nx.DiGraph()
g.add_edge((0, 0), (0, 1))
g.add_edge((0, 1), (0, 2))
# g.add_edge(0, 3)
g.remove_node((0, 0))
print(set(g.neighbors((0, 1))))
print(g.degree)
nx.draw(g)
plt.show()
