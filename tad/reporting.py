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
from typing import Dict, Sequence

logger = logging.getLogger(__name__)


def auto_output_name(model_name: str, homology: str) -> str:
    return f"tad_spike_{model_name.split('/')[-1]}_{homology}.json"


def report_chunk_header(
    logs_found: Sequence[int], gt_log_nums: Sequence[int], mode_used: str
) -> None:
    logger.info("    Mode: %s", mode_used)
    logger.info("    Logs found: %s", list(logs_found))
    if gt_log_nums:
        logger.info("    Ground truth logs: %s", list(gt_log_nums))


def report_screen(
    dim_key: str, search_type: str, round_idx: int, n_groups: int, screen_results: Sequence[Dict]
) -> None:
    logger.info("    %s %s -- SCREEN round %d (%d groups):", dim_key, search_type, round_idx, n_groups)
    for s in screen_results:
        marker = "  <-- HOT" if s["is_hot"] else ""
        logger.info(
            "      screen %s: removal_change=%.4f, gap=%.2f%s",
            s["group"], s["removal_change"], s["gap"], marker,
        )


def report_confirm(dim_key: str, d: Dict, gt_log_nums: Sequence[int]) -> None:
    logger.info("      -- CONFIRM --")
    for c in d["confirm_results"]:
        marker = "  <-- SPIKE" if c.get("is_spike") else ""
        logger.info(
            "      confirm log%s: wasserstein=%.4f, gap=%.2f%s",
            c["log"], c["total_wasserstein"], c.get("gap", 0.0), marker,
        )
    if d.get("masked"):
        logger.info("      Hot group(s) found but no individual spike (masking).")

    passes = d.get("forward_passes")
    suffix = f" ({passes} forward passes)" if passes is not None else ""
    logger.info("    %s: Spike logs = %s%s", dim_key, d["spike_logs"], suffix)
    if gt_log_nums:
        logger.info(
            "      Ground truth found: %s, missed: %s",
            d.get("ground_truth_found", []), d.get("ground_truth_missed", []),
        )
        recall = d.get("ground_truth_recall")
        if recall is not None:
            logger.info("      Recall: %.2f%%", recall * 100)
