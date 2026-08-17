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

import logging
from dataclasses import dataclass
from typing import Dict, List, Sequence

import gudhi as gd
import numpy as np

from tad.config import INT_MAX

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ResponseSpan:
    start: int
    end: int

    @property
    def n_tokens(self) -> int:
        return self.end - self.start


@dataclass
class ResponseTopology:
    diagrams: Dict[int, List[np.ndarray]]
    n_layers: int
    span: ResponseSpan

    @property
    def info(self) -> Dict[str, int]:
        return {"n_response_tokens": self.span.n_tokens, "n_layers": self.n_layers}


@dataclass(frozen=True)
class LayerTopologyChange:
    wasserstein: float
    persistence_change: float


@dataclass(frozen=True)
class TopologyChange:
    per_layer: List[LayerTopologyChange]

    @property
    def wasserstein_distances(self) -> List[float]:
        return [layer.wasserstein for layer in self.per_layer]

    @property
    def persistence_changes(self) -> List[float]:
        return [layer.persistence_change for layer in self.per_layer]

    @property
    def total_wasserstein(self) -> float:
        return float(sum(self.wasserstein_distances))

    def to_dict(self) -> Dict[str, object]:
        wd, pc = self.wasserstein_distances, self.persistence_changes
        return {
            "layer_wasserstein_distances": wd,
            "total_wasserstein": self.total_wasserstein,
            "mean_wasserstein": float(np.mean(wd)),
            "max_wasserstein": max(wd),
            "max_wasserstein_layer": int(np.argmax(wd)),
            "layer_persistence_changes": pc,
            "total_persistence_change": float(sum(pc)),
            "mean_persistence_change": float(np.mean(pc)),
        }


def persistence_from_hidden_state(
    hidden_state: np.ndarray, dimensions: Sequence[int] = (0,)
) -> Dict[int, np.ndarray]:
    if hidden_state.shape[0] < 2:
        return {dim: np.array([[0.0, 0.0]]) for dim in dimensions}

    rips = gd.RipsComplex(points=hidden_state, max_edge_length=np.inf)
    st = rips.create_simplex_tree(max_dimension=max(dimensions) + 1)
    st.compute_persistence()

    diagrams = {}
    for dim in dimensions:
        persistence = st.persistence_intervals_in_dimension(dim)
        persistence = np.array(persistence) if len(persistence) else np.array([[0.0, 0.0]])
        persistence[np.isinf(persistence)] = INT_MAX
        diagrams[dim] = persistence
    return diagrams


def total_persistence(pd: np.ndarray) -> float:
    pd_clean = pd.copy()
    pd_clean[pd_clean >= INT_MAX] = 0
    lifetimes = pd_clean[:, 1] - pd_clean[:, 0]
    return float(np.sum(np.maximum(lifetimes, 0)))


def _layer_change(baseline: np.ndarray, ablated: np.ndarray, layer_idx: int) -> LayerTopologyChange:
    # Imported lazily
    from gudhi.wasserstein import wasserstein_distance

    try:
        wdist = float(wasserstein_distance(baseline, ablated, order=1, internal_p=np.inf))
    except (ValueError, RuntimeError):
        logger.warning("wasserstein_distance failed at layer %d", layer_idx, exc_info=True)
        wdist = 0.0
    pchange = abs(total_persistence(ablated) - total_persistence(baseline))
    return LayerTopologyChange(wasserstein=wdist, persistence_change=float(pchange))


def compute_topology_change(
    baseline_pds: Sequence[np.ndarray], ablated_pds: Sequence[np.ndarray]
) -> TopologyChange:
    if len(baseline_pds) != len(ablated_pds):
        raise ValueError(
            f"Layer count mismatch: baseline has {len(baseline_pds)}, "
            f"ablated has {len(ablated_pds)}"
        )
    if not baseline_pds:
        raise ValueError("Cannot compute topology change for zero layers")

    return TopologyChange(
        per_layer=[
            _layer_change(baseline, ablated, i)
            for i, (baseline, ablated) in enumerate(zip(baseline_pds, ablated_pds))
        ]
    )
