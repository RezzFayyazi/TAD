# Licensed under the GNU General Public License v3.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at https://www.gnu.org/licenses/gpl-3.0.en.html


from typing import Dict, Optional, Sequence, Tuple

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from tad.config import TAG, AttributionConfig, ResponseSpanError
from tad.topology import ResponseSpan, ResponseTopology, persistence_from_hidden_state

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def load_model(model_name: str, device: str = DEVICE):
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True, use_fast=True)
    if not tokenizer.is_fast:
        raise ValueError(
            f"Tokenizer for '{model_name}' is not a fast tokenizer. A fast tokenizer is "
            "required because get_response_topology relies on return_offsets_mapping."
        )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        model_name, output_hidden_states=True, trust_remote_code=True, device_map=device, dtype=torch.bfloat16
    )
    model.eval()
    return model, tokenizer


def _locate_response_span(
    prompt: str, tokenizer, max_response_tokens: Optional[int] = None
) -> Tuple[Dict[str, torch.Tensor], ResponseSpan]:
    tag_pos = prompt.rfind(TAG)
    if tag_pos == -1:
        raise ResponseSpanError(f"{TAG!r} not found in prompt")

    enc = tokenizer(prompt, return_tensors="pt", return_offsets_mapping=True)
    offsets = enc.pop("offset_mapping")[0].tolist()

    tag_char_end = tag_pos + len(TAG)
    start = next(
        (i for i, (tok_start, _) in enumerate(offsets) if tok_start >= tag_char_end),
        None,
    )
    if start is None:
        raise ResponseSpanError("No response tokens found after tag")

    end = len(offsets)
    if max_response_tokens is not None:
        end = min(end, start + max_response_tokens)
    if end <= start:
        raise ResponseSpanError("Response span is empty")

    return enc, ResponseSpan(start, end)


def _persistence_per_layer(
    hidden_states: Sequence[torch.Tensor],
    span: ResponseSpan,
    dimensions: Sequence[int],
    last_k_layers: Optional[int] = None,
) -> Dict[int, list]:
    # Skip the embedding layer (index 0): it reflects token identity, not context.
    hidden_states = hidden_states[1:]
    if last_k_layers is not None:
        hidden_states = hidden_states[-last_k_layers:]
    diagrams: Dict[int, list] = {dim: [] for dim in dimensions}
    for layer in hidden_states:
        response_hidden = layer[0, span.start : span.end].cpu().float().numpy()
        layer_diagrams = persistence_from_hidden_state(response_hidden, dimensions)
        for dim in dimensions:
            diagrams[dim].append(layer_diagrams[dim])
    return diagrams


def get_response_topology(
    model, tokenizer, prompt: str, device: str, config: AttributionConfig
) -> ResponseTopology:
    enc, span = _locate_response_span(prompt, tokenizer, config.max_response_tokens)
    inputs = {k: v.to(device) for k, v in enc.items()}

    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True)
    try:
        diagrams = _persistence_per_layer(
            outputs.hidden_states, span, config.dimensions, config.last_k_layers
        )
        n_layers = len(next(iter(diagrams.values()))) if diagrams else 0
        return ResponseTopology(diagrams=diagrams, n_layers=n_layers, span=span)
    finally:
        del outputs, inputs
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
