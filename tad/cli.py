
import argparse
import logging
from typing import Optional, Sequence

from tad.config import DEFAULT_MODEL, HOMOLOGY_DIMENSIONS
from tad.runner import run


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Topological Attribution Distance (TAD) with robust spike detection "
                    "using k-way screen-then-confirm search."
    )
    parser.add_argument("input", help="Path to log analysis output JSON")
    parser.add_argument("-o", "--output", default=None,
                        help="Output path (default: tad_spike_<model>_<homology>.json)")
    parser.add_argument("-m", "--model", default=DEFAULT_MODEL, help=f"Model name (default: {DEFAULT_MODEL})")
    parser.add_argument("-t", "--max-tokens", type=int, default=None,
                        help="Limit analysis to first N response tokens (default: all)")
    parser.add_argument("-k", "--last-k-layers", type=int, default=None,
                        help="Only compute topology over the last K hidden-state layers "
                             "(default: all layers)")
    parser.add_argument("--homology", choices=list(HOMOLOGY_DIMENSIONS), default="h0",
                        help="Which homology dimensions to compute (default: h0). Note: h2/h3 "
                             "build all 3-/4-simplices and can be very slow/memory-heavy on long "
                             "responses; consider capping with --max-tokens")
    parser.add_argument("--groups", type=int, default=None,
                        help="Number of groups for the k-way screen "
                             "(default: ceil(sqrt(N)) logs)")
    parser.add_argument("--linear", action="store_true",
                        help="Ablate every log individually instead of partitioning "
                             "(skips the k-way screen; ignores --groups)")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    args = build_parser().parse_args(argv)
    run(
        model_name=args.model,
        dataset_path=args.input,
        homology=args.homology,
        output_path=args.output,
        max_response_tokens=args.max_tokens,
        verbose=not args.quiet,
        last_k_layers=args.last_k_layers,
        n_groups=args.groups,
        force_linear=args.linear,
    )
