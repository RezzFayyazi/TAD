
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

import importlib
import os

# Must be set before torch initializes CUDA; do it before anything imports torch.
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "0")

from tad.config import (
    DEFAULT_MODEL,
    HOMOLOGY_DIMENSIONS,
    MIN_GROUPING_LOGS,
    TAG,
    AttributionConfig,
    ResponseSpanError,
)
from tad.spikes import flag_spikes
from tad.topology import (
    ResponseSpan,
    ResponseTopology,
    TopologyChange,
    compute_topology_change,
    persistence_from_hidden_state,
    total_persistence,
)
from tad.prompts import (
    default_group_count,
    extract_logs,
    log_numbers,
    partition,
    reconstruct_prompt,
    remove_logs_batch,
)

# name -> submodule, imported on first attribute access (pulls in torch).
_LAZY = {
    "DEVICE": "tad.model",
    "load_model": "tad.model",
    "get_response_topology": "tad.model",
    "SpikeAttributor": "tad.attribution",
    "auto_output_name": "tad.reporting",
    "run": "tad.runner",
    "build_parser": "tad.cli",
    "main": "tad.cli",
}


def __getattr__(name: str):
    module = _LAZY.get(name)
    if module is None:
        raise AttributeError(f"module 'tad' has no attribute {name!r}")
    value = getattr(importlib.import_module(module), name)
    globals()[name] = value  # cache so subsequent lookups skip __getattr__
    return value


def __dir__():
    return sorted(__all__)


__all__ = [
    "AttributionConfig",
    "ResponseSpanError",
    "DEFAULT_MODEL",
    "HOMOLOGY_DIMENSIONS",
    "MIN_GROUPING_LOGS",
    "TAG",
    "DEVICE",
    "flag_spikes",
    "ResponseSpan",
    "ResponseTopology",
    "TopologyChange",
    "compute_topology_change",
    "persistence_from_hidden_state",
    "total_persistence",
    "reconstruct_prompt",
    "extract_logs",
    "remove_logs_batch",
    "log_numbers",
    "partition",
    "default_group_count",
    "load_model",
    "get_response_topology",
    "SpikeAttributor",
    "auto_output_name",
    "run",
    "build_parser",
    "main",
]
