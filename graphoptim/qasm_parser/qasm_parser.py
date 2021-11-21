# from typing import List
#
# # Store the most recent object pushed to the line in order to determine
#
# dag: List[List[int]] = []
# bases: List[int] = []
# line_buffer: List[str] = []
#
#
#
#
# def parse_qasm(qasm_file: str):
#     file = open(qasm_file)
#     lines = file.read().splitlines()
#     for line in lines:
#         if line != "":
#             parse_line(line)
#     file.close()
#
#
# def parse_line(qasm_line: str):
#     wds = qasm_line.split(' ')
#     if wds[0] == "qreg":
#         parse_reg(int(wds[1][2]))
#     if len(wds) == 2:
#         parse_rotation(wds[0], int(wds[1][2]))
#     else:
#         parse_entanglement(wds[0], int(wds[1][2]), int(wds[2][2]))
#
#
# def parse_reg(reg_size: int):
#     pass
#
#
# def parse_rotation(operator: str, qubit: int):
#     pass
#
#
# def parse_entanglement(operator: str, qubit1: int, qubit2: int):
#     # Parse the operator into
#     pass
#
#
# def to_graph_state():
#     pass
#
#
# def to_dag():
#     pass
#
#
# def clear_cache():
#     pass
