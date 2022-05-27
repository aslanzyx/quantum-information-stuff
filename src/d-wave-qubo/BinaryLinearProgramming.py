from dimod import ConstrainedQuadraticModel, Binary, SampleSet
import numpy as np


class BinaryLinearProgramming:
    """
    Binary Linear Programming(BLP):
    for binary word x s.t.
    objective: min(<c,x>)
    constraint: Ax >= b

    Note: BLP is equivalently a multi-constraint knapsack
    """

    def __init__(self, A: np.ndarray, b: np.ndarray, c: np.ndarray):
        self.m, self.n = A.shape
        self.A = A
        self.b = b
        self.c = c
        self.x = [Binary(f"x_{i}") for i in range(self.n)]
        self.model = None
        self.outcome = None

        self._modelConstructed = False

    def constructCQM(self) -> ConstrainedQuadraticModel:
        """
        Construct a constraint quadratic model.
        return: the model
        """
        if not self._modelConstructed:
            self.model = ConstrainedQuadraticModel()
            self.model.set_objective(np.dot(self.c, self.x))
            constraints = self.A@self.x
            for i in range(self.m):
                self.model.add_constraint(
                    constraints[i] >= self.b[i], label=f"constraint_{i}")
            # flip the constructed flag
            self._modelConstructed = True
        return self.model

    def sample(self, sampler) -> SampleSet:
        """
        Sample the result. A model is required. Please run a construct model method before this.
        sampler: sampler object
        return: a set of feasible solution samples
        """
        if not self._modelConstructed:
            print("Warning: model not constructed")
        else:
            # Start sampling
            sampleset = sampler.sample_cqm(self.model)
            print(f"sample finished in: {sampleset.info['run_time']} ms")
            print(f"QPU access time: {sampleset.info['qpu_access_time']} ms")
            feasibleSamplesets = sampleset.filter(
                lambda sample: sample.is_feasible)
            self.outcome = feasibleSamplesets
            return feasibleSamplesets

    def processOutcome(self) -> np.ndarray:
        xp = np.zeros(self.n)
        if len(self.outcome) == 0:
            print("Warning: infeasible problem")
        else:
            for xi, val in self.outcome.first.sample.items():
                xp[int(xi[2:])] = val
        return xp
