from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ModelConfig:
    env_key: str
    base_url: str
    model_id: str
    temperature: float | None
    max_tokens: int | None
    request_delay_seconds: float = 1.0
    extra_body: dict[str, Any] = field(default_factory=dict)
    output_file: str = ""
    thinking: bool = False


def build_models() -> dict[str, ModelConfig]:
    """Return the Round 2 model registry with provider-specific settings."""
    dashscope_base_url = os.getenv(
        "DASHSCOPE_BASE_URL",
        "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
    )

    return {
        "deepseek-v3.2": ModelConfig(
            env_key="DEEPSEEK_API_KEY",
            base_url="https://api.deepseek.com",
            model_id="deepseek-chat",
            temperature=1.0,
            max_tokens=None,
            output_file="deepseek-v3.2.json",
        ),
        "deepseek-v3.2-thinking": ModelConfig(
            env_key="DEEPSEEK_API_KEY",
            base_url="https://api.deepseek.com",
            model_id="deepseek-reasoner",
            temperature=None,  # not supported for reasoner
            max_tokens=None,
            output_file="deepseek-v3.2-thinking.json",
            thinking=True,
        ),
        "glm-5": ModelConfig(
            env_key="ZAI_API_KEY",
            base_url="https://api.z.ai/api/paas/v4/",
            model_id="glm-5",
            temperature=1.0,
            max_tokens=None,
            extra_body={"thinking": {"type": "disabled"}},
            output_file="glm-5.json",
        ),
        "glm-5-thinking": ModelConfig(
            env_key="ZAI_API_KEY",
            base_url="https://api.z.ai/api/paas/v4/",
            model_id="glm-5",
            temperature=1.0,
            max_tokens=None,
            extra_body={"thinking": {"type": "enabled"}},
            output_file="glm-5-thinking.json",
            thinking=True,
        ),
        "kimi-k2.5": ModelConfig(
            env_key="MOONSHOT_API_KEY",
            base_url="https://api.moonshot.ai/v1",
            model_id="kimi-k2.5",
            temperature=0.6,
            max_tokens=None,
            request_delay_seconds=5.0,
            extra_body={"thinking": {"type": "disabled"}},
            output_file="kimi-k2.5.json",
        ),
        "kimi-k2.5-thinking": ModelConfig(
            env_key="MOONSHOT_API_KEY",
            base_url="https://api.moonshot.ai/v1",
            model_id="kimi-k2.5",
            temperature=1.0,
            max_tokens=None,
            request_delay_seconds=5.0,
            extra_body={"thinking": {"type": "enabled"}},
            output_file="kimi-k2.5-thinking.json",
            thinking=True,
        ),
        "qwen3.5-397b": ModelConfig(
            env_key="DASHSCOPE_API_KEY",
            base_url=dashscope_base_url,
            model_id="qwen3.5-397b-a17b",
            temperature=0.7,
            max_tokens=None,
            extra_body={"enable_thinking": False},
            output_file="qwen3.5-397b-a17b.json",
        ),
        "qwen3.5-397b-thinking": ModelConfig(
            env_key="DASHSCOPE_API_KEY",
            base_url=dashscope_base_url,
            model_id="qwen3.5-397b-a17b",
            temperature=0.6,
            max_tokens=None,
            extra_body={"enable_thinking": True},
            output_file="qwen3.5-397b-a17b-thinking.json",
            thinking=True,
        ),
        "qwen3.5-122b": ModelConfig(
            env_key="DASHSCOPE_API_KEY",
            base_url=dashscope_base_url,
            model_id="qwen3.5-122b-a10b",
            temperature=0.7,
            max_tokens=None,
            extra_body={"enable_thinking": False},
            output_file="qwen3.5-122b-a10b.json",
        ),
        "qwen3.5-122b-thinking": ModelConfig(
            env_key="DASHSCOPE_API_KEY",
            base_url=dashscope_base_url,
            model_id="qwen3.5-122b-a10b",
            temperature=1.0,
            max_tokens=None,
            extra_body={"enable_thinking": True},
            output_file="qwen3.5-122b-a10b-thinking.json",
            thinking=True,
        ),
        "qwen3.5-35b": ModelConfig(
            env_key="DASHSCOPE_API_KEY",
            base_url=dashscope_base_url,
            model_id="qwen3.5-35b-a3b",
            temperature=0.7,
            max_tokens=None,
            extra_body={"enable_thinking": False},
            output_file="qwen3.5-35b-a3b.json",
        ),
        "qwen3.5-35b-thinking": ModelConfig(
            env_key="DASHSCOPE_API_KEY",
            base_url=dashscope_base_url,
            model_id="qwen3.5-35b-a3b",
            temperature=1.0,
            max_tokens=None,
            extra_body={"enable_thinking": True},
            output_file="qwen3.5-35b-a3b-thinking.json",
            thinking=True,
        ),
        "qwen3.5-27b": ModelConfig(
            env_key="DASHSCOPE_API_KEY",
            base_url=dashscope_base_url,
            model_id="qwen3.5-27b",
            temperature=0.7,
            max_tokens=None,
            extra_body={"enable_thinking": False},
            output_file="qwen3.5-27b.json",
        ),
        "qwen3.5-27b-thinking": ModelConfig(
            env_key="DASHSCOPE_API_KEY",
            base_url=dashscope_base_url,
            model_id="qwen3.5-27b",
            temperature=1.0,
            max_tokens=None,
            extra_body={"enable_thinking": True},
            output_file="qwen3.5-27b-thinking.json",
            thinking=True,
        ),
        "mistral-large-3": ModelConfig(
            env_key="MISTRAL_API_KEY",
            base_url="https://api.mistral.ai/v1",
            model_id="mistral-large-2512",
            temperature=0.3,
            max_tokens=None,
            output_file="mistral-large-3.json",
        ),
        "mistral-small-4": ModelConfig(
            env_key="MISTRAL_API_KEY",
            base_url="https://api.mistral.ai/v1",
            model_id="mistral-small-2603",
            temperature=0.3,
            max_tokens=None,
            output_file="mistral-small-4.json",
        ),
        "mistral-small-4-thinking": ModelConfig(
            env_key="MISTRAL_API_KEY",
            base_url="https://api.mistral.ai/v1",
            model_id="mistral-small-2603",
            temperature=0.7,
            max_tokens=None,
            extra_body={"reasoning_effort": "high"},
            output_file="mistral-small-4-thinking.json",
            thinking=True,
        ),
        "mimo-v2-flash-thinking": ModelConfig(
            env_key="XIAOMI_MIMO_API_KEY",
            base_url="https://api.xiaomimimo.com/v1",
            model_id="mimo-v2-flash",
            temperature=0.8,
            max_tokens=None,
            extra_body={"chat_template_kwargs": {"enable_thinking": True}},
            output_file="mimo-v2-flash-thinking.json",
            thinking=True,
        ),
        "nemotron-3-super": ModelConfig(
            env_key="NVIDIA_API_KEY",
            base_url="https://integrate.api.nvidia.com/v1",
            model_id="nvidia/nemotron-3-super-120b-a12b",
            temperature=1.0,
            max_tokens=16000,
            extra_body={"chat_template_kwargs": {"enable_thinking": False}},
            output_file="nemotron-3-super.json",
        ),
        "nemotron-3-super-thinking": ModelConfig(
            env_key="NVIDIA_API_KEY",
            base_url="https://integrate.api.nvidia.com/v1",
            model_id="nvidia/nemotron-3-super-120b-a12b",
            temperature=1.0,
            max_tokens=16000,
            extra_body={
                "chat_template_kwargs": {"enable_thinking": True},
                "reasoning_budget": 4096,
            },
            output_file="nemotron-3-super-thinking.json",
            thinking=True,
        ),
    }
