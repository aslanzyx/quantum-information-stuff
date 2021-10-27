import re
from typing import List
import numpy as np

file = open("teleportation.qasm")
qreg_line = file.readline()
# Parse quantum register and generate cluster
qnum:int = 2*int(qreg_line[7]) - 1
cluster: np.ndarray = np.ones((qnum, 2))
# X -> XYXY
# Z -> YXYX
# Y -> YY
# H -> XYYY
# S -> YX
# T -> TX
# CZ ->
file.close()

# parse
class QASMParser:
    dag: List[List[int]] = []
    bases: List[int] = []
    # Store the most recent object pushed to the line in order to determine
    line_buffer: List[str] = []
    cluster: np.ndarray = None

    def parse_qasm(qasmText: str):
        pass

    def parse_line(qasmLine: str):
        pass

    def parse_reg(regLine: str):
        pass

    def parse_rotation(operator: str, qubit: int):
        # Parse the operator into measurement sequence
        QASMParser.bases.append()
        QASMParser.line_buffer[qubit] = operator
        pass

    @staticmethod
    def parse_entanglement(operator, qubit1, qubit2):
        # Parse the operator into
        pass

    @staticmethod
    def clear_cache():
        pass
