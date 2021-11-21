# import numpy as np
#
# # <+|Z X
# # <+|Z X
# class Correction:
#     def __init__(self, size: int):
#         self.z_dependencies = np.zeros(size, np.bool)
#         self.x_dependencies = np.zeros(size, np.bool)
#         self.sign = 1
#         pass
#
#     def merge_x(self, node_idx: int) -> None:
#         self.x_dependencies[node_idx] ^= 1
#
#     def merge_z(self, node_idx: int) -> None:
#         self.z_dependencies[node_idx] ^= 1
#         self.sign *= -1
#
#     def merge(self, operator, node_idx):
#         pass
#
#     def merge_sqrt_x(self, direction):
#         pass
#
#     def merge_sqrt_y(self, direction):
#         pass
#
#     def merge_sqrt_z(self, direction):
#         pass