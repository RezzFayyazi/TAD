
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Screen-then-confirm topological spike attribution engine."""

from typing import Dict, List, Optional, Sequence, Tuple

from tad.config import AttributionConfig, ResponseSpanError
from tad.model import get_response_topology
from tad.prompts import default_group_count, log_numbers, partition, remove_logs_batch
from tad.reporting import report_chunk_header, report_confirm, report_screen
from tad.spikes import flag_spikes
from tad.topology import ResponseTopology, compute_topology_change


def _ground_truth_recall(
    found_logs: Sequence[int], ground_truth_log_numbers: Optional[Sequence[int]]
) -> Tuple[List[int], List[int], Optional[float]]:
    if not ground_truth_log_numbers:
        return [], [], None
    gt_log_nums = list(ground_truth_log_numbers)
    gt_found = [gt for gt in gt_log_nums if gt in found_logs]
    gt_missed = [gt for gt in gt_log_nums if gt not in found_logs]
    return gt_found, gt_missed, len(gt_found) / len(gt_log_nums)


def _result_scaffold(
    log_nums: List[int], search_type: str, ground_truth_log_numbers: Optional[Sequence[int]]
) -> Dict:
    return {
        "logs_found": log_nums,
        "num_logs": len(log_nums),
        "search_type": search_type,
        "ground_truth_log_numbers": list(ground_truth_log_numbers) if ground_truth_log_numbers else [],
        "dimensions": {},
    }


class SpikeAttributor:

    def __init__(self, model, tokenizer, device: str, config: AttributionConfig):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device
        self.config = config

    def analyze(
        self, prompt: str, ground_truth_log_numbers: Optional[Sequence[int]] = None
    ) -> Tuple[str, Dict]:
        try:
            log_nums = log_numbers(prompt)
        except ResponseSpanError as exc:
            return "none", {"error": str(exc)}

        use_linear = self.config.force_linear or len(log_nums) < self.config.min_grouping_logs
        search_type = "linear" if use_linear else "k-way"
        results = _result_scaffold(log_nums, search_type, ground_truth_log_numbers)
        report_chunk_header(log_nums, ground_truth_log_numbers or [], search_type)

        cache: Dict[str, ResponseTopology] = {}
        baseline = self._topology(prompt, cache)
        for dim in self.config.dimensions:
            results["dimensions"][f"H{dim}"] = self._attribute_dim(
                dim, log_nums, prompt, baseline, cache, ground_truth_log_numbers, use_linear
            )
        return search_type, results

    def _topology(self, prompt: str, cache: Dict[str, ResponseTopology]) -> ResponseTopology:
        if prompt not in cache:
            cache[prompt] = get_response_topology(
                self.model, self.tokenizer, prompt, self.device, self.config
            )
        return cache[prompt]

    def _attribute_dim(
        self, dim, log_nums, prompt, baseline, cache, ground_truth_log_numbers, use_linear
    ) -> Dict:
        dim_key = f"H{dim}"
        search_type = "linear" if use_linear else "k-way"
        baseline_pds = baseline.diagrams[dim]
        passes_before = len(cache)

        def change_for(removed: Sequence[int]) -> float:
            ablated = self._topology(remove_logs_batch(prompt, removed), cache)
            return compute_topology_change(baseline_pds, ablated.diagrams[dim]).total_wasserstein

        def screen(round_idx: int, pool: Sequence[int], n_groups: int):
            groups = partition(pool, n_groups)
            changes = [change_for(grp) for grp in groups]
            grp_gaps, grp_hot = flag_spikes(changes)
            rows = [
                {"round": round_idx, "group": grp, "removal_change": chg,
                 "gap": float(gap), "is_hot": bool(hot)}
                for grp, chg, gap, hot in zip(groups, changes, grp_gaps, grp_hot)
            ]
            report_screen(dim_key, search_type, round_idx, len(groups), rows)
            hot = [grp for grp, is_hot in zip(groups, grp_hot) if is_hot]
            return rows, hot

        screen_results: List[Dict] = []
        if use_linear:
            # Each log is its own group; every log is confirmed (a full ranking).
            rows, hot_groups = screen(1, log_nums, len(log_nums))
            screen_results = rows
            first_n_groups = len(rows)
            confirm_logs: List[int] = list(log_nums)
        else:
            pool = list(log_nums)
            hot_groups: List[List[int]] = []
            first_n_groups = 0
            round_idx = 0
            while True:
                round_idx += 1
                g = (self.config.n_groups if round_idx == 1 else 0) or default_group_count(len(pool))
                rows, hot_groups = screen(round_idx, pool, g)
                screen_results.extend(rows)
                if round_idx == 1:
                    first_n_groups = len(rows)
                hot_logs = [n for grp in hot_groups for n in grp]
                # Re-screen whenever the surviving hot pool is still large enough
                if len(hot_logs) >= self.config.min_grouping_logs:
                    pool = hot_logs
                    continue
                break
            confirm_logs = hot_logs

        confirm_results = [{"log": n, "total_wasserstein": change_for([n])} for n in confirm_logs]

        spike_logs, masked = self._localize(confirm_results, screen_results, use_linear)
        gt_found, gt_missed, recall = _ground_truth_recall(spike_logs, ground_truth_log_numbers)

        result = {
            "baseline_info": baseline.info,
            "search_type": search_type,
            "n_groups": first_n_groups,
            "screen_results": screen_results,
            "confirm_results": confirm_results,
            "hot_groups": hot_groups,
            "spike_logs": spike_logs,
            "top_attributed_logs": spike_logs,
            "masked": masked,
            "forward_passes": len(cache) - passes_before,
            "ground_truth_found": gt_found,
            "ground_truth_missed": gt_missed,
            "ground_truth_recall": recall,
        }
        report_confirm(dim_key, result, ground_truth_log_numbers or [])
        return result

    def _localize(
        self, confirm_results: List[Dict], screen_results: List[Dict], use_linear: bool
    ) -> Tuple[List[int], bool]:
        """Attach normalized attribution + spike flags; return (spike_logs, masked)."""
        if not confirm_results:
            return [], False

        total_impact = sum(c["total_wasserstein"] for c in confirm_results) + 1e-8
        for c in confirm_results:
            c["normalized_attribution"] = c["total_wasserstein"] / total_impact
        confirm_results.sort(key=lambda c: c["total_wasserstein"], reverse=True)

        if len(confirm_results) == 1 and not use_linear:
            hot_gap = max((s["gap"] for s in screen_results if s["is_hot"]), default=0.0)
            confirm_results[0]["gap"] = float(hot_gap)
            confirm_results[0]["is_spike"] = True
        else:
            conf_gaps, conf_spike = flag_spikes(
                [c["total_wasserstein"] for c in confirm_results]
            )
            for c, gap, spike in zip(confirm_results, conf_gaps, conf_spike):
                c["gap"] = float(gap)
                c["is_spike"] = bool(spike)

        spike_logs = [c["log"] for c in confirm_results if c["is_spike"]]
        masked = not use_linear and not spike_logs
        return spike_logs, masked
