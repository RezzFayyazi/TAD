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

import math
import re
from typing import Dict, List, Sequence

from tad.config import TAG, ResponseSpanError


def reconstruct_prompt(query: str, formatted_logs: str, response: str, task_reminder: str = "") -> str:
    return f"{query}\n\n{formatted_logs}{task_reminder}{TAG}\n{response}"


def extract_logs(text: str) -> Dict[int, str]:
    pattern = r"<<log(\d+)>>(.*?)<<log\1/>>?"
    return {int(m.group(1)): m.group(0) for m in re.finditer(pattern, text, re.DOTALL)}


def remove_logs_batch(text: str, log_nums: Sequence[int]) -> str:
    for log_num in log_nums:
        pattern = rf"<<log{log_num}>>(.*?)<<log{log_num}/>>?\s*"
        text = re.sub(pattern, "", text, flags=re.DOTALL)
    return text


def log_numbers(prompt: str) -> List[int]:
    """Return sorted <<logN>> numbers preceding the final response tag, or raise."""
    tag_pos = prompt.rfind(TAG)
    if tag_pos == -1:
        raise ResponseSpanError(f"'{TAG}' not found")
    logs = extract_logs(prompt[:tag_pos])
    if not logs:
        raise ResponseSpanError("No <<logN>>...<<logN/>> tags found")
    return sorted(logs)


def partition(items: Sequence[int], n_groups: int) -> List[List[int]]:
    """Split ``items`` into ``n_groups`` contiguous, near-equal groups."""
    n_groups = max(1, min(n_groups, len(items)))
    base, remainder = divmod(len(items), n_groups)
    groups: List[List[int]] = []
    start = 0
    for i in range(n_groups):
        size = base + (1 if i < remainder else 0)
        groups.append(list(items[start : start + size]))
        start += size
    return groups


def default_group_count(n_logs: int) -> int:
    return max(2, math.ceil(math.sqrt(n_logs)))
