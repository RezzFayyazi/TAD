
from typing import List, Sequence, Tuple

import numpy as np


def flag_spikes(values: Sequence[float]) -> Tuple[List[float], List[bool]]:

    x = np.asarray(values, dtype=float)
    n = x.size
    if n < 2:
        return [0.0] * n, [False] * n

    order = np.argsort(-x, kind="stable")
    gaps = x[order][:-1] - x[order][1:]
    cut = int(np.argmax(gaps)) + 1

    scores = np.zeros(n)
    scores[order[:-1]] = gaps

    is_spike = np.zeros(n, dtype=bool)
    if gaps[cut - 1] > 0:
        is_spike[order[:cut]] = True

    return scores.tolist(), is_spike.tolist()
