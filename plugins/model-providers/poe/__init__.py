"""Poe OpenAI-compatible provider profile."""

from providers import register_provider
from providers.base import ProviderProfile


poe = ProviderProfile(
    name="poe",
    aliases=("poe-api", "quora-poe"),
    display_name="Poe",
    description="Poe — OpenAI-compatible API to Poe bots/models",
    signup_url="https://poe.com/api_key",
    env_vars=("POE_API_KEY", "POE_BASE_URL"),
    base_url="https://api.poe.com/v1",
    fallback_models=(
        "muse-spark-open",
        "muse-spark-1-1",
        "claude-sonnet-5.5",
        "claude-haiku-5.5",
        "gpt-5.4",
        "gemini-3.8-flash",
        "kimi-k3",
        "grok-4.7",
    ),
)

register_provider(poe)
