#!/usr/bin/env python3
"""
Run the benchmark locally via mlx-vlm.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

try:
    from mlx_vlm import generate, load
    from mlx_vlm.prompt_utils import apply_chat_template
except ImportError as exc:  # pragma: no cover
    raise SystemExit("mlx-vlm is not installed in this environment.") from exc


BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "dataset.json"
RESULTS_DIR = BASE_DIR / "results"


def build_prompt(question: dict[str, Any]) -> str:
    options_text = "\n".join(
        f"{opt['id']}) {opt['text']}" for opt in question["options"]
    )
    return f"{question['question_text']}\n\nOptions:\n{options_text}\n\nAnswer:"


def slugify_model_id(model_id: str) -> str:
    slug = model_id.strip().replace("\\", "-").replace("/", "-")
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", slug)
    return slug.strip("-") or "local-model"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the thesis benchmark locally via mlx-vlm."
    )
    parser.add_argument(
        "--model",
        required=True,
        help="Local path or Hugging Face repo id for the MLX model.",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=1.0,
        help="Sampling temperature. Default: 1.0",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=1024,
        help="Maximum number of new tokens per answer. Default: 1024",
    )
    parser.add_argument(
        "--enable-thinking",
        action="store_true",
        help="Enable Gemma thinking mode via the chat template and generation.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Run only the first N questions for a smoke test.",
    )
    parser.add_argument(
        "--output-file",
        type=str,
        default=None,
        help="Optional output filename inside ./results.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        questions = json.load(f)

    if args.limit is not None:
        questions = questions[: args.limit]

    output_file = args.output_file or f"{slugify_model_id(args.model)}.json"
    output_path = RESULTS_DIR / output_file

    print("\n" + "=" * 60, flush=True)
    print(f"  Local MLX benchmark  ({args.model})", flush=True)
    print(
        "  "
        f"{len(questions)} questions | temperature={args.temperature} | "
        f"max_tokens={args.max_tokens}",
        flush=True,
    )
    print("=" * 60 + "\n", flush=True)

    model, processor = load(args.model)

    results: list[dict[str, Any]] = []
    total = len(questions)

    for i, question in enumerate(questions, 1):
        user_prompt = build_prompt(question)
        prompt = apply_chat_template(
            processor,
            model.config,
            user_prompt,
            num_images=0,
            num_audios=0,
            enable_thinking=args.enable_thinking,
        )

        gen_kwargs: dict[str, Any] = {
            "max_tokens": args.max_tokens,
            "temperature": args.temperature,
            "enable_thinking": args.enable_thinking,
        }

        try:
            response = generate(model, processor, prompt, **gen_kwargs)
            answer = response.text.strip()
            print(
                "  "
                f"[{i}/{total}] Question {question['id']} — OK "
                f"({response.generation_tokens} tok @ "
                f"{response.generation_tps:.1f} t/s, "
                f"peak {response.peak_memory:.2f} GB)",
                flush=True,
            )
            results.append(
                {
                    "id": question["id"],
                    "prompt": user_prompt,
                    "model_answer": answer,
                    "prompt_tokens": response.prompt_tokens,
                    "generation_tokens": response.generation_tokens,
                    "prompt_tps": response.prompt_tps,
                    "generation_tps": response.generation_tps,
                    "peak_memory_gb": response.peak_memory,
                }
            )
        except Exception as exc:
            print(
                f"  [{i}/{total}] Question {question['id']} — ERROR: {exc}",
                flush=True,
            )
            results.append(
                {
                    "id": question["id"],
                    "prompt": user_prompt,
                    "model_answer": f"[ERROR] {exc}",
                }
            )

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n  Done! {len(results)} results saved to {output_path}\n", flush=True)


if __name__ == "__main__":
    main()
