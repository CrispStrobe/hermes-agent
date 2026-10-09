"""Scaleway Generative APIs OpenAI-compatible provider profile."""

from providers import register_provider
from providers.base import ProviderProfile


scaleway = ProviderProfile(
    name="scaleway",
    aliases=("scw", "scaleway-ai"),
    display_name="Scaleway Generative APIs",
    description="Scaleway Generative APIs — OpenAI-compatible inference",
    signup_url="https://console.scaleway.com/",
    env_vars=("SCALEWAY_API_KEY", "SCW_SECRET_KEY", "SCALEWAY_BASE_URL"),
    base_url="https://api.scaleway.ai/v1",
    fallback_models=(
        "llama-3.3-70b-instruct",
        "llama-3.1-8b-instruct",
        "mistral-nemo-instruct-2407",
        "qwen2.5-coder-32b-instruct",
        "deepseek-r1",
        "deepseek-r1-distill-llama-70b",
        "phi-4",
    ),
)

register_provider(scaleway)
