# TAD (Topological Attribution Distance)
# Copyright (C) 2026 TAD Reza Fayyazi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

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
