from typing import Dict

import numpy as np

from .BlochSphere import BlochSphere


class MeasurementBaseLayer:
    def __init__(self, angle_map: Dict[(int, int), float]) -> None:
        self.bases: Dict[(int, int), BlochSphere] = dict()
        for label, angle in angle_map.items():
            self.bases[label] = BlochSphere(np.array([1, 0, 0]))
            self.bases[label].rotate_z(angle)

    def rotate(self, label: (int, int), angle: float, base: str) -> None:
        self.bases[label].rotate(angle, base)
