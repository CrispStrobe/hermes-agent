"""Cohere OpenAI-compatible provider profile."""

from providers import register_provider
from providers.base import ProviderProfile


cohere = ProviderProfile(
    name="cohere",
    aliases=("cohere-ai",),
    display_name="Cohere",
    description="Cohere — Compatibility API (OpenAI chat completions)",
    signup_url="https://dashboard.cohere.com/api-keys",
    env_vars=("COHERE_API_KEY", "CO_API_KEY", "COHERE_BASE_URL"),
    base_url="https://api.cohere.ai/compatibility/v1",
    fallback_models=(
        "command-a-plus-05-2026",
        "command-a-reasoning-08-2025",
        "command-a-03-2025",
        "north-mini-code-1-0",
        "command-r-plus-08-2024",
    ),
)

register_provider(cohere)
