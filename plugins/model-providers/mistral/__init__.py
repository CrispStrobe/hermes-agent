"""Mistral AI OpenAI-compatible provider profile."""

from providers import register_provider
from providers.base import ProviderProfile


mistral = ProviderProfile(
    name="mistral",
    aliases=("mistral-ai", "mistralai"),
    display_name="Mistral AI",
    description="Mistral AI — native Mistral API",
    signup_url="https://console.mistral.ai/",
    env_vars=("MISTRAL_API_KEY", "MISTRAL_BASE_URL"),
    base_url="https://api.mistral.ai/v1",
    fallback_models=(
        "mistral-large-latest",
        "mistral-medium-latest",
        "mistral-small-latest",
        "codestral-latest",
        "devstral-small-latest",
        "mistral-saba-latest",
        "ministral-8b-latest",
        "ministral-3b-latest",
    ),
)

register_provider(mistral)
