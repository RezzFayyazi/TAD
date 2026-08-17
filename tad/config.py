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

from dataclasses import dataclass, field
from typing import List, Optional, Sequence

INT_MAX = 2147483647
DEFAULT_MODEL = "meta-llama/Llama-3.2-3B-Instruct"
TAG = "<<Response>>"

# Below this many logs, k-way grouping isn't worthwhile; use per-log linear ablation.
MIN_GROUPING_LOGS = 9

HOMOLOGY_DIMENSIONS = {"h0": [0], "h1": [1], "h2": [2], "h3": [3], "both": [0, 1]}


class ResponseSpanError(ValueError):
    """Raised when the response span cannot be located in a prompt."""


@dataclass(frozen=True)
class AttributionConfig:
    dimensions: Sequence[int] = field(default_factory=lambda: [0])
    max_response_tokens: Optional[int] = None
    last_k_layers: Optional[int] = None
    n_groups: Optional[int] = None
    min_grouping_logs: int = MIN_GROUPING_LOGS
    force_linear: bool = False
