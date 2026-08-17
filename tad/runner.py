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

import json
import logging
import os
import time
from typing import Dict, Optional

from dotenv import load_dotenv
from huggingface_hub import login

from tad.attribution import SpikeAttributor
from tad.config import HOMOLOGY_DIMENSIONS, MIN_GROUPING_LOGS, AttributionConfig
from tad.model import DEVICE, load_model
from tad.prompts import reconstruct_prompt
from tad.reporting import auto_output_name

logger = logging.getLogger("tad")


def _authenticate() -> None:
    load_dotenv()
    if hf_token := os.getenv("HF_TOKEN"):
        login(token=hf_token)


def _load_dataset(path: str) -> Dict:
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Dataset not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc


def _save_results(results: Dict, path: str) -> None:
    try:
        with open(path, "w") as f:
            json.dump(results, f, indent=2)
    except OSError as exc:
        raise OSError(f"Failed to write results to {path}: {exc}") from exc


def run(
    model_name: str,
    dataset_path: str,
    homology: str = "h0",
    output_path: Optional[str] = None,
    device: str = DEVICE,
    max_response_tokens: Optional[int] = None,
    verbose: bool = True,
    last_k_layers: Optional[int] = None,
    n_groups: Optional[int] = None,
    force_linear: bool = False,
) -> Dict:
    logger.setLevel(logging.INFO if verbose else logging.WARNING)
    _authenticate()

    try:
        dimensions = HOMOLOGY_DIMENSIONS[homology]
    except KeyError as exc:
        raise ValueError(
            f"Unknown homology {homology!r}; choose from {sorted(HOMOLOGY_DIMENSIONS)}"
        ) from exc

    config = AttributionConfig(
        dimensions=dimensions,
        max_response_tokens=max_response_tokens,
        last_k_layers=last_k_layers,
        n_groups=n_groups,
        force_linear=force_linear,
    )
    output_path = output_path or auto_output_name(model_name, homology)
    dataset = _load_dataset(dataset_path)

    groups_desc = str(n_groups) if n_groups else "ceil(sqrt(N))"
    logger.info("Loading model %s...", model_name)
    if force_linear:
        logger.info("Mode: per-log linear ablation (partitioning disabled)")
    else:
        logger.info(
            "Mode: k-way screen-then-confirm (%s groups, prune cold, confirm hot; "
            "falls back to per-log linear below %d logs)", groups_desc, MIN_GROUPING_LOGS,
        )
    logger.info("Spike detection: largest gap in the sorted removal changes")

    load_start = time.time()
    model, tokenizer = load_model(model_name, device)
    model_load_time = time.time() - load_start
    logger.info("Model loaded in %.1fs", model_load_time)

    attributor = SpikeAttributor(model, tokenizer, device, config)

    experiment_start = time.time()
    results: Dict = {
        "metadata": dataset.get("metadata", {}),
        "analysis_info": {
            "type": "tad_spike_attribution",
            "description": (
                "Wasserstein change when a log is removed = higher attribution. "
                "Spikes flagged by cutting the sorted changes at their largest gap."
            ),
            "model": model_name,
            "dimensions": [f"H{d}" for d in dimensions],
            "homology": homology,
            "max_response_tokens": max_response_tokens,
            "last_k_layers": last_k_layers,
            "search_type": (
                "linear (forced)" if force_linear
                else "adaptive (k-way with per-log linear fallback)"
            ),
            "n_groups": n_groups,
            "model_load_seconds": round(model_load_time, 2),
        },
        "windows": [],
    }

    for win_idx, window in enumerate(dataset.get("windows", []), start=1):
        window_start = time.time()
        window_id = window.get("window_id", win_idx)
        query = window.get("query", "")
        chunks = window.get("chunks", [])
        ground_truth_indices = window.get("ground_truth_log_indices", [])

        logger.info("\n[Window %s] %d chunk(s)", window_id, len(chunks))
        if ground_truth_indices:
            logger.info("  Ground truth log numbers (1-indexed): %s", ground_truth_indices)

        window_result: Dict = {
            "window_id": window_id,
            "start": window.get("start", ""),
            "end": window.get("end", ""),
            "ground_truth_log_indices": ground_truth_indices,
            "chunks": [],
        }

        for chunk in chunks:
            prompt = reconstruct_prompt(
                query=query,
                formatted_logs=chunk.get("formatted_logs", ""),
                response=chunk.get("response", ""),
                task_reminder=chunk.get("task_reminder", ""),
            )
            mode_used, result = attributor.analyze(prompt, ground_truth_indices)

            chunk_result: Dict = {
                "mode_used": mode_used,
                "reconstructed_prompt": prompt,
            }
            if result.get("error"):
                logger.info("    Error: %s", result["error"])
                chunk_result["error"] = result["error"]
            else:
                chunk_result.update(result)

            window_result["chunks"].append(chunk_result)

        window_elapsed = time.time() - window_start
        window_result["elapsed_seconds"] = round(window_elapsed, 2)
        logger.info("  Window %s completed in %.1fs", window_id, window_elapsed)
        results["windows"].append(window_result)

    total_elapsed = time.time() - experiment_start
    results["analysis_info"]["total_elapsed_seconds"] = round(total_elapsed, 2)
    results["analysis_info"]["total_elapsed_formatted"] = (
        f"{int(total_elapsed // 60)}m {int(total_elapsed % 60)}s"
    )

    _save_results(results, output_path)

    logger.info("\n%s", "=" * 50)
    logger.info(
        "Experiment completed in %s (%.1fs)",
        results["analysis_info"]["total_elapsed_formatted"], total_elapsed,
    )
    logger.info("Saved results to %s", output_path)
    return results
