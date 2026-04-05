# thesis-llm-benchmark

A two-part LLM benchmark study built on the same 100-question Slovak multiple-choice dataset.
It covers mathematics, spatial and temporal reasoning, social reasoning, and trick questions.
Originally conducted as part of a thesis, now replicated in 2026 using exclusively open-source models.

The repository keeps both a corrected post-submission Round 1 snapshot and a
sanitized archival copy of the originally submitted 2025 materials.
`2025-thesis` should be treated as the primary Round 1 directory for browsing
results and code, while `2025-thesis-archive` is included only for transparency,
preserving the originally submitted state before post-submission fixes and cleanup.

## Table of contents

- [Dataset](#dataset)
- [Round 1 — thesis benchmark (2025)](#round-1--thesis-benchmark-2025)
- [Round 2 — open-source benchmark (2026)](#round-2--open-source-benchmark-2026)
- [Methodology notes](#methodology-notes)
- [API / inference settings](#api-settings)
- [Reproducibility](#reproducibility)
- [Structure](#structure)

*💡 Reasoning models are indicated by a lightbulb icon.*

---

## Dataset

100 multiple-choice questions in Slovak, used identically across both rounds to ensure comparability.
The dataset draws from three sources:

- **[SimpleBench](https://github.com/simple-bench/SimpleBench)** — a subset of questions from the [public dataset](https://github.com/simple-bench/SimpleBench/blob/main/simple_bench_public.json), translated into Slovak and slightly modified
- **Math Kangaroo-style problems** — non-standard reasoning problems adapted from a Czech worksheet collection drawing on the international Math Kangaroo competition and related educational publications, including *Počítejte s klokanem 1995–1999* (Prodos, ISBN 80-7230-068-7, ISBN 80-7230-077-6)
- **Original questions** — authored specifically for this benchmark

Each question in `dataset.json` includes a `category` and `origin` field for full traceability.

The dataset covers five question categories:

| Category (English) | Count |
|--------------------|-------|
| Mathematics        | 39    |
| Trick questions    | 36    |
| Spatial reasoning  | 13    |
| Temporal reasoning | 7     |
| Social reasoning   | 5     |

The dataset is included in both `dataset.json` and `dataset.csv` for each round.
`dataset.json` is the canonical machine-readable source used by the benchmark scripts
and for reproducibility; `dataset.csv` is a human-readable export included for easier
browsing on GitHub or in spreadsheet tools.

---

## Round 1 — Thesis Benchmark (2025)

All models in this round are proprietary, with the exception of the two
DeepSeek models, which are MIT licensed and have a reported size of
`671B (37B active)`.

| Model                          | Creator    | API Model ID                 |
|--------------------------------|------------|------------------------------|
| ChatGPT 4o                     | OpenAI     | `gpt-4o-2024-08-06`          |
| ChatGPT o1 💡                  | OpenAI     | `o1-2024-12-17`              |
| Claude 3.7 Sonnet              | Anthropic  | `claude-3-7-sonnet-20250219` |
| Claude 3.7 Sonnet Thinking 💡  | Anthropic  | `claude-3-7-sonnet-20250219` |
| DeepSeek-V3                    | DeepSeek   | `deepseek-chat` (V3-0324)    |
| DeepSeek-R1 💡                 | DeepSeek   | `deepseek-reasoner`          |
| Gemini 2.0 Flash               | Google     | `gemini-2.0-flash`           |
| Gemini 2.5 Pro Experimental 💡 | Google     | `gemini-2.5-pro-exp-03-25`   |
| Perplexity Sonar               | Perplexity | `sonar-pro`                  |
| Perplexity Sonar Pro 💡        | Perplexity | `sonar-reasoning-pro`        |
| Grok 3                         | xAI        | N/A (tested via web UI)      |
| Grok 3 Thinking 💡             | xAI        | N/A (tested via web UI)      |

> **Note on Grok 3:** xAI did not release an API for Grok 3 for over 40 days after
> the model's release. Both Grok 3 variants were tested manually via the web UI,
> so their results are not directly comparable to the API-based runs.

### Results

*💡 Reasoning models are indicated by a lightbulb icon.*

| Model                              | Score   |
|------------------------------------|---------|
| Gemini 2.5 Pro Experimental 💡     | 84/100  |
| Claude 3.7 Sonnet Thinking 💡      | 84/100  |
| ChatGPT o1 💡                      | 84/100  |
| DeepSeek-R1 💡                     | 83/100  |
| Grok 3 Thinking 💡                 | 79/100  |
| Grok 3                             | 74/100  |
| Claude 3.7 Sonnet                  | 72/100  |
| Perplexity Sonar Pro 💡            | 71/100  |
| DeepSeek-V3                        | 70/100  |
| ChatGPT 4o                         | 68/100  |
| Gemini 2.0 Flash                   | 65/100  |
| Perplexity Sonar                   | 58/100  |

Per-question breakdown available in [`2025-thesis/results.csv`](2025-thesis/results.csv).

---

## Round 2 — Open-source Benchmark (2026)

Replication of the original benchmark using open-source models only.

| Model               | Creator     | License      | Parameters        |
|---------------------|-------------|--------------|-------------------|
| DeepSeek V3.2       | DeepSeek    | MIT          | 685B (37B active) |
| DeepSeek V3.2 💡    | DeepSeek    | MIT          | 685B (37B active) |
| GLM-5               | Z.ai        | MIT          | 744B (40B active) |
| GLM-5 💡            | Z.ai        | MIT          | 744B (40B active) |
| Kimi K2.5           | Moonshot AI | Modified MIT | 1T (32B active)   |
| Kimi K2.5 💡        | Moonshot AI | Modified MIT | 1T (32B active)   |
| MiMo-V2-Flash 💡    | Xiaomi      | MIT          | 309B (15B active) |
| Mistral Large 3     | Mistral AI  | Apache       | 675B (41B active) |
| Mistral Small 4     | Mistral AI  | Apache       | 119B (6B active)  |
| Mistral Small 4 💡  | Mistral AI  | Apache       | 119B (6B active)  |
| Nemotron 3 Super    | NVIDIA      | MIT          | 120B (12B active) |
| Nemotron 3 Super 💡 | NVIDIA      | MIT          | 120B (12B active) |
| Qwen 3.5 27B        | Alibaba     | Apache       | 27B               |
| Qwen 3.5 27B 💡     | Alibaba     | Apache       | 27B               |
| Qwen 3.5 35B A3B    | Alibaba     | Apache       | 35B (3B active)   |
| Qwen 3.5 35B A3B 💡 | Alibaba     | Apache       | 35B (3B active)   |
| Qwen 3.5 122B A10B  | Alibaba     | Apache       | 122B (10B active) |
| Qwen 3.5 122B A10B 💡 | Alibaba   | Apache       | 122B (10B active) |
| Qwen 3.5 397B A17B  | Alibaba     | Apache       | 397B (17B active) |
| Qwen 3.5 397B A17B 💡 | Alibaba   | Apache       | 397B (17B active) |

> **Note on Nemotron 3 Super:** NVIDIA's official model card lists the supported
> languages as English, French, German, Italian, Japanese, Spanish, and Chinese.
> Despite Slovak not being listed, both Nemotron variants performed competitively
> in this benchmark, including ahead of some substantially larger models.

### Results

*💡 Reasoning models are indicated by a lightbulb icon.*

| Model                    | Score |
|--------------------------|-------|
| Qwen 3.5 122B A10B 💡    | 88/100 |
| Qwen 3.5 27B 💡          | 88/100 |
| Qwen 3.5 397B A17B       | 87/100 |
| GLM-5 💡                 | 86/100 |
| Qwen 3.5 397B A17B 💡    | 85/100 |
| Qwen 3.5 122B A10B       | 84/100 |
| DeepSeek V3.2 💡         | 82/100 |
| Qwen 3.5 35B A3B 💡      | 82/100 |
| Qwen 3.5 27B             | 81/100 |
| Kimi K2.5 💡             | 81/92* |
| Kimi K2.5                | 79/100 |
| DeepSeek V3.2            | 79/100 |
| MiMo-V2-Flash 💡         | 78/100 |
| Qwen 3.5 35B A3B         | 77/100 |
| Nemotron 3 Super 💡      | 75/100 |
| Mistral Small 4 💡       | 73/100 |
| Nemotron 3 Super        | 72/100 |
| GLM-5                    | 67/100 |
| Mistral Large 3          | 64/100 |
| Mistral Small 4          | 50/100 |

Per-question breakdown available in [`2026-oss/results.csv`](2026-oss/results.csv).

> *Moonshot AI had by far the least reliable API infrastructure in this benchmark.
> `Kimi K2.5 💡` still had 8 unresolved questions
> after 4 helper-script retry runs spread across several hours, with repeated
> `Request timed out` and `engine_overloaded_error` failures.

---

## Methodology notes

- Same 100-question dataset used in both rounds
- **Both rounds conducted entirely in Slovak** — all questions are in Slovak
- One API call per question
- **No system prompt used in either round** — models received a single user prompt per question, with no additional system instruction layer
- **Zero-shot evaluation** — one run per question, no examples or additional context provided
- **`top_p` is never set explicitly** — it is left at each provider's default, since common API guidance recommends adjusting either `temperature` or `top_p`, but not both simultaneously
- Results stored as JSON per model, summarized in `results.csv`

> **On zero-shot evaluation:** Round 1 used a single zero-shot run per question —
> what the thesis described as the most "bare" view of model performance. A more
> robust approach (used by benchmarks like SimpleBench) averages results across
> 5 runs or uses majority voting across 5 attempts. Round 2 intentionally preserves
> the single zero-shot run to maintain direct comparability with Round 1, with the
> understanding that this is a known limitation of both rounds. The setup is
> deliberately lean and transparent rather than built around heavyweight benchmark
> infrastructure.

---

## API Settings

### Round 1

Settings used per model during thesis testing:

| Model                          | Model ID                       | temperature | max_tokens |
|--------------------------------|--------------------------------|-------------|------------|
| ChatGPT 4o                     | `gpt-4o-2024-08-06`            | `1.0`       | default    |
| ChatGPT o1 💡                  | `o1-2024-12-17`                | `1.0`       | default    |
| Claude 3.7 Sonnet              | `claude-3-7-sonnet-20250219`   | `1.0`       | `1024`     |
| Claude 3.7 Sonnet Thinking 💡  | `claude-3-7-sonnet-20250219`   | `1.0`       | `8000`     |
| DeepSeek-V3                    | `deepseek-chat`                | `1.0`       | default    |
| DeepSeek-R1 💡                 | `deepseek-reasoner`            | `1.0`       | default    |
| Gemini 2.0 Flash               | `gemini-2.0-flash`             | `1.0`       | default    |
| Gemini 2.5 Pro Experimental 💡 | `gemini-2.5-pro-exp-03-25`     | `1.0`       | default    |
| Perplexity Sonar               | `sonar-pro`                    | `1.0`       | default    |
| Perplexity Sonar Pro 💡        | `sonar-reasoning-pro`          | `1.0`       | default    |
| Grok 3                         | N/A (tested via web UI)        | —           | —          |
| Grok 3 Thinking 💡             | N/A (tested via web UI)        | —           | —          |

#### Notes

- Claude 3.7 Sonnet Thinking 💡 used extended thinking with `budget_tokens: 6000`.
- Gemini 2.0 Flash and Gemini 2.5 Pro Experimental 💡 were tested via the `google-generativeai` SDK, with generation settings left at their defaults.
- Grok 3 and Grok 3 Thinking 💡 were tested manually via the web UI because xAI did not provide an API for more than 40 days after release.

### Round 2

| Model                  | Model ID                            | temperature   |
|------------------------|-------------------------------------|---------------|
| DeepSeek-V3.2          | `deepseek-chat`                     | `1.0`         |
| DeepSeek-V3.2 💡       | `deepseek-reasoner`                 | not supported |
| GLM-5                  | `glm-5`                             | `1.0`         |
| GLM-5 💡               | `glm-5`                             | `1.0`         |
| Kimi K2.5              | `kimi-k2.5`                         | `0.6`         |
| Kimi K2.5 💡           | `kimi-k2.5`                         | `1.0`         |
| MiMo-V2-Flash 💡       | `mimo-v2-flash`                     | `0.8`         |
| Mistral Large 3        | `mistral-large-2512`                | `0.3`         |
| Mistral Small 4        | `mistral-small-2603`                | `0.3`         |
| Mistral Small 4 💡     | `mistral-small-2603`                | `0.7`         |
| Nemotron 3 Super       | `nvidia/nemotron-3-super-120b-a12b` | `1.0`         |
| Nemotron 3 Super 💡    | `nvidia/nemotron-3-super-120b-a12b` | `1.0`         |
| Qwen 3.5 27B           | `qwen3.5-27b`                       | `0.7`         |
| Qwen 3.5 27B 💡        | `qwen3.5-27b`                       | `1.0`         |
| Qwen 3.5 35B A3B       | `qwen3.5-35b-a3b`                   | `0.7`         |
| Qwen 3.5 35B A3B 💡    | `qwen3.5-35b-a3b`                   | `1.0`         |
| Qwen 3.5 122B A10B     | `qwen3.5-122b-a10b`                 | `0.7`         |
| Qwen 3.5 122B A10B 💡  | `qwen3.5-122b-a10b`                 | `1.0`         |
| Qwen 3.5 397B A17B     | `qwen3.5-397b-a17b`                 | `0.7`         |
| Qwen 3.5 397B A17B 💡  | `qwen3.5-397b-a17b`                 | `0.6`         |

`max_tokens` was left at the provider default for every Round 2 model except
`Nemotron 3 Super` and `Nemotron 3 Super 💡`, where the script explicitly set
`16000`.

Where provider documentation or model cards specified recommended `temperature`
values, those recommendations were followed.

#### Configuration notes

- `DeepSeek-V3.2 💡` does not support `temperature`.
- `GLM-5` and `Kimi K2.5` use explicit `thinking` on/off switches for standard vs reasoning runs.
- `MiMo-V2-Flash 💡` enables thinking via `chat_template_kwargs`.
- `Mistral Small 4 💡` sets `reasoning_effort="high"`.
- `Nemotron 3 Super` uses explicit `enable_thinking` on/off control; the thinking variant also sets `reasoning_budget: 4096`.
- `Qwen 3.5` models use hybrid thinking mode by default, so standard runs explicitly disable thinking and reasoning runs explicitly enable it.


---

## Reproducibility

The actively maintained runner in this repository is the open-source Round 2
benchmark. The `2025-thesis` and `2025-thesis-archive` directories are kept
mainly as historical Round 1 materials.

### Environment setup

Requires Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
```

Then add the required provider API keys to `.env`.

### Running the benchmark

List available models:

```bash
cd 2026-oss
python run_benchmark.py --list
```

Run a single model:

```bash
cd 2026-oss
python run_benchmark.py --model <model-key>
```

Run the full suite:

```bash
cd 2026-oss
python run_benchmark.py --all
```

Outputs are written to the Round 2 `results/` directory as one JSON file per
model.

---

## Structure

- `2025-thesis-archive` — historical archive of the original 2025 materials
- `2025-thesis` — corrected Round 1 benchmark
- `2026-oss` — open-source Round 2 benchmark

Each round directory contains the dataset, raw model outputs, benchmark code,
and a score summary.

---

## License

[MIT](https://choosealicense.com/licenses/mit/)
