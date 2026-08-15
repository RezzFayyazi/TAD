
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
