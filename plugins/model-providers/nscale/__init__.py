"""Nscale OpenAI-compatible provider profile."""

from providers import register_provider
from providers.base import ProviderProfile


nscale = ProviderProfile(
    name="nscale",
    aliases=("nscale-ai",),
    display_name="Nscale",
    description="Nscale — serverless OpenAI-compatible inference",
    signup_url="https://console.nscale.com/",
    env_vars=("NSCALE_API_KEY", "NSCALE_TOKEN", "NSCALE_BASE_URL"),
    base_url="https://inference.api.nscale.com/v1",
    fallback_models=(
        "moonshotai/Kimi-K2.5",
        "Qwen/Qwen3-235B-A22B-Instruct-2507",
        "openai/gpt-oss-120b",
        "Qwen/Qwen3-32B",
    ),
)

register_provider(nscale)
