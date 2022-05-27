from .BinaryLinearProgramming import BinaryLinearProgramming

class SetCover:
    """
    SetCover(SC):
    solve for a set of sets S s.t.
    S subseteq V
    forall u in U, exists s in S, u in s

    Note: SC is reducable to BLP in poly-time
    Note: V is assumed to hold no repeating sets, because at most one of the repeating sets could be chosen
    """

    def __init__(self, U: set[any], V: dict[any, set[any]]):
        self.U = U
        self.V = V
        self.m = len(U)
        self.n = len(V)

    def assertFeasible(self) -> bool:
        """
        Check if sets in V covers all elements in U.
        """
        traversed = set()
        for v in self.V.values():
            traversed = traversed.union(v)
        feasible = True
        for u in self.U:
            feasible ^= u in traversed
        return feasible

    def greedySolution(self) -> set[any] or None:
        """
        A greedy solution runs in poly-time.

        Note: this greedy algorithm provides a log(n)-approximation
        """
        residualU = set.copy(self.U)
        residualV = dict.copy(self.V)
        chosen = set()
        while len(residualU) > 0:
            # Chose the set covers the most in the residial universe
            chosen_label = None
            chosen_coverage = 0
            for l, v in residualV.items():
                coverage = len(v.intersection(residualU))
                if coverage > chosen_coverage:
                    chosen_label = l
                    chosen_coverage = coverage

            # Remove the covered elements
            residualU = residualU.difference(residualV[chosen_label])
            residualV.pop(chosen_label)
            chosen.add(chosen_label)

            # Check if infeasible
            if len(residualV) == 0:
                return None  # infeasible

        return chosen