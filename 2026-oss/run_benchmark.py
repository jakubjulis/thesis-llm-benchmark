#!/usr/bin/env python3
"""
Round 2 — Open-source LLM Benchmark (2026)
Unified benchmark script for all providers.

Usage:
    python run_benchmark.py --model glm-5
    python run_benchmark.py --model glm-5-thinking
    python run_benchmark.py --all
    python run_benchmark.py --list
"""

import argparse
import json
import os
import re
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROUND_DIR = Path(__file__).resolve().parent
DATASET_PATH = ROUND_DIR / "dataset.json"
RESULTS_DIR = ROUND_DIR / "results"
REQUEST_TIMEOUT_SECONDS = 180.0

load_dotenv(ROUND_DIR.parent / ".env")
from models import ModelConfig, build_models

MODELS: dict[str, ModelConfig] = build_models()


def build_prompt(question: dict) -> str:
    """Format the single user prompt used in both rounds (no system prompt)."""
    options_text = "\n".join(
        f"{opt['id']}) {opt['text']}" for opt in question["options"]
    )
    return f"{question['question_text']}\n\nOptions:\n{options_text}\n\nAnswer:"


def extract_answer(response) -> str:
    """Extract the model's answer text from the API response."""
    msg = response.choices[0].message
    content = msg.content or ""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        text_blocks = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                text = block.get("text")
                if isinstance(text, str):
                    text_blocks.append(text)
        return "\n".join(text_blocks).strip()
    return ""


def natural_sort_key(value: str):
    """Sort strings alphabetically while comparing embedded numbers numerically."""
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", value)]


def run_benchmark(model_key: str) -> None:
    """Run the full benchmark for a single model configuration."""
    cfg = MODELS[model_key]

    api_key = os.getenv(cfg.env_key)
    if not api_key:
        print(f"[SKIP] {model_key}: env var {cfg.env_key} not set.", flush=True)
        return

    # Handle base_url that might already be resolved from env
    base_url = cfg.base_url

    client = OpenAI(api_key=api_key, base_url=base_url, timeout=REQUEST_TIMEOUT_SECONDS)

    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        questions = json.load(f)

    results = []
    total = len(questions)
    print(f"\n{'='*60}", flush=True)
    print(f"  {model_key}  ({cfg.model_id})", flush=True)
    temperature_label = cfg.temperature if cfg.temperature is not None else "provider default"
    max_tokens_label = cfg.max_tokens if cfg.max_tokens is not None else "provider default"
    print(
        f"  {total} questions | temperature={temperature_label} | max_tokens={max_tokens_label}",
        flush=True,
    )
    print(f"{'='*60}\n", flush=True)

    for i, q in enumerate(questions, 1):
        prompt = build_prompt(q)

        # Build API kwargs
        kwargs = {
            "model": cfg.model_id,
            # Preserve Round 1 parity by sending only one user message.
            "messages": [{"role": "user", "content": prompt}],
        }
        if cfg.max_tokens is not None:
            kwargs["max_tokens"] = cfg.max_tokens
        if cfg.temperature is not None:
            kwargs["temperature"] = cfg.temperature
        if cfg.extra_body:
            kwargs["extra_body"] = cfg.extra_body

        try:
            response = client.chat.completions.create(**kwargs)
            answer = extract_answer(response)
            print(f"  [{i}/{total}] Question {q['id']} — OK", flush=True)
        except Exception as e:
            answer = f"[ERROR] {e}"
            print(f"  [{i}/{total}] Question {q['id']} — ERROR: {e}", flush=True)

        results.append({
            "id": q["id"],
            "prompt": prompt,
            "model_answer": answer,
        })

        time.sleep(cfg.request_delay_seconds)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RESULTS_DIR / cfg.output_file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n  Done! {len(results)} results saved to {output_path.name}\n", flush=True)


def main():
    parser = argparse.ArgumentParser(description="Round 2 — Open-source LLM Benchmark")
    parser.add_argument("--model", type=str, help="Model key to benchmark (see --list)")
    parser.add_argument("--all", action="store_true", help="Run all models sequentially")
    parser.add_argument("--list", action="store_true", help="List available model keys")
    args = parser.parse_args()

    if args.list:
        print("\nAvailable models:\n", flush=True)
        for key in sorted(MODELS, key=natural_sort_key):
            cfg = MODELS[key]
            tag = " 💡" if cfg.thinking else ""
            print(f"  {key:<35} → {cfg.model_id}{tag}", flush=True)
        print(flush=True)
        return

    if args.all:
        for key in sorted(MODELS, key=natural_sort_key):
            run_benchmark(key)
        return

    if args.model:
        if args.model not in MODELS:
            print(f"Unknown model: {args.model}", flush=True)
            print("Use --list to show available model keys.", flush=True)
            return
        run_benchmark(args.model)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
