#!/usr/bin/env python3
"""Create small JSONL subsets for Wanqing fine-tuning smoke tests."""

from __future__ import annotations

import argparse
import glob
import os
import random
from pathlib import Path


PRESETS = {
    "recommend": ["dataset/懂推荐*.jsonl"],
    "material": ["dataset/懂物料part*.jsonl"],
    "user": ["dataset/懂用户.jsonl"],
    "all": ["dataset/*.jsonl"],
}


def expand_inputs(preset: str, inputs: list[str]) -> list[Path]:
    patterns = inputs or PRESETS[preset]
    paths: list[Path] = []
    for pattern in patterns:
        paths.extend(Path(p) for p in glob.glob(pattern))
    unique = sorted(set(paths), key=lambda p: str(p))
    if not unique:
        raise SystemExit(f"No input files matched: {patterns}")
    return unique


def count_lines(paths: list[Path]) -> int:
    total = 0
    for path in paths:
        with path.open("r", encoding="utf-8") as f:
            for _ in f:
                total += 1
    return total


def sample_head(paths: list[Path], size: int) -> list[str]:
    rows: list[str] = []
    for path in paths:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                rows.append(line)
                if len(rows) >= size:
                    return rows
    return rows


def sample_random(paths: list[Path], size: int, seed: int) -> list[str]:
    rng = random.Random(seed)
    reservoir: list[str] = []
    seen = 0
    for path in paths:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                seen += 1
                if len(reservoir) < size:
                    reservoir.append(line)
                else:
                    j = rng.randrange(seen)
                    if j < size:
                        reservoir[j] = line
    return reservoir


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preset", choices=sorted(PRESETS), default="recommend")
    parser.add_argument("--input", action="append", default=[], help="Input glob. Can be repeated.")
    parser.add_argument("--size", type=int, default=100, help="Number of JSONL rows to output.")
    parser.add_argument("--mode", choices=["random", "head"], default="random")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out-dir", default="dataset_subsets")
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    if args.size <= 0:
        raise SystemExit("--size must be positive")

    paths = expand_inputs(args.preset, args.input)
    total = count_lines(paths)
    size = min(args.size, total)

    if args.mode == "head":
        rows = sample_head(paths, size)
    else:
        rows = sample_random(paths, size, args.seed)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    output = Path(args.output) if args.output else out_dir / f"{args.preset}_{size}_{args.mode}_seed{args.seed}.jsonl"
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", encoding="utf-8") as f:
        f.writelines(rows)

    input_names = ", ".join(os.fspath(p) for p in paths)
    print(f"inputs: {input_names}")
    print(f"available rows: {total}")
    print(f"written rows: {len(rows)}")
    print(f"output: {output}")


if __name__ == "__main__":
    main()
