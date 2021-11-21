# from typing import List, Set
#
# import numpy as np
#
#
# class StabilizerGenerator:
#     def __init__(self, size):
#         self.generator = np.zeros((size, 2 * size))
#         self.correction = np.zeros((size, 2 * size))
#         self.measurement_bases = np.zeros((size, 3))
#         pass
#
#     @staticmethod
#     def parse_graph(links: List[Set[int]], measurement_base: List[(int, int, int)]):
#         n = len(measurement_base)
#         stabilizer_generator = StabilizerGenerator(n)
#         for i in range(n):
#             stabilizer_generator.generator[i, 2 * n + i] = 1
#             for j in links[i]:
#                 stabilizer_generator.generator[i, j] = 1
#             stabilizer_generator.correction[i, i] = 1
#             stabilizer_generator.measurement_bases[i, :] = measurement_base[i]
