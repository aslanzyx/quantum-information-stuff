from math import pi
from qiskit import QuantumCircuit
import matplotlib.pyplot as plt

def qft(input_circuit: QuantumCircuit, size: int) -> None:
    input_circuit.barrier()
    for i in range(size):
        input_circuit.h(i)
        for j in range(i+1, size):
            input_circuit.crz(2**(i-j)*pi, j, i)
    print("finished")
    input_circuit.draw(output="mpl")
    plt.show()

def qft_dagger(input_circuit: QuantumCircuit):
    return NotImplementedError()

