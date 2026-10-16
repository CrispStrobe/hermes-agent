"""Requesty OpenAI-compatible provider profile."""

from providers import register_provider
from providers.base import ProviderProfile


requesty = ProviderProfile(
    name="requesty",
    aliases=("requesty-ai", "requesty-router"),
    display_name="Requesty",
    description="Requesty — OpenAI-compatible LLM router",
    signup_url="https://app.requesty.ai/api-keys",
    env_vars=("REQUESTY_API_KEY", "REQUESTY_BASE_URL"),
    base_url="https://router.requesty.ai/v1",
    fallback_models=(
        "fireworks/muse-spark-open",
        "together/muse-spark-open",
        "meta/muse-spark-1.3",
        "anthropic/claude-sonnet-5-5",
        "anthropic/claude-opus-5-5",
        "xai/grok-4.7",
    ),
)

register_provider(requesty)
