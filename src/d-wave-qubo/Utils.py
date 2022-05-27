import SetCover, BinaryLinearProgramming
import numpy as np


def mapSC2BLP(sc: SetCover) -> BinaryLinearProgramming:
    """
    Map a SC problem to a BLP problem.
    construct
    """
    A = np.zeros((sc.m, sc.n))
    label_map = dict()

    i = 0
    for u in sc.U:
        label_map[u] = i
        i += 1

    i = 0
    for v in sc.V.values():
        for u in v:
            A[label_map[u], i] = 1
        i += 1

    return BinaryLinearProgramming(A,
                                   np.ones(sc.m),
                                   np.ones(sc.n))