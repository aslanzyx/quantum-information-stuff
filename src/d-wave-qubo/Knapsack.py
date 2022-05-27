from dimod import ConstrainedQuadraticModel, Integer, SampleSet
import numpy as np


class Knapsack:
    """
    Descrete Knapsack:
    for descrete variable x s.t.
    objective: max(<c,x>)
    constraint: <a,x> <= w
    bound: x <= b

    Note: Knapsack is equivalently a descrete linear programming problem
    Note: The problem if by default unbound
    """

    def __init__(self, a: np.ndarray, c: np.ndarray, w: float, b: np.ndarray = None):
        self.n = a.shape
        self.a = a
        self.b = b
        self.c = c
        self.w = w
        self.x = [Integer(f"x_{i}") for i in range(self.n)]
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
            self.model.set_objective(-np.dot(self.c, self.x))
            self.model.add_constraint(
                np.dot(self.a, self.x) <= self.w, label="cost_bound")
            if self.b is not None:
                for i in range(self.n):
                    self.model.add_constraint(self.x[i] <= self.b[i], label=f"bound_{i}")
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
