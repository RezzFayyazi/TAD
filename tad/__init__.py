
# Licensed under the GNU General Public License v3.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at https://www.gnu.org/licenses/gpl-3.0.en.html

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
