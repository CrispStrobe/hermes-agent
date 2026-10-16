"""Groq OpenAI-compatible provider profile."""

from providers import register_provider
from providers.base import ProviderProfile


groq = ProviderProfile(
    name="groq",
    aliases=("groq-cloud", "groqcloud"),
    display_name="Groq",
    description="Groq — low-latency OpenAI-compatible inference",
    signup_url="https://console.groq.com/keys",
    env_vars=("GROQ_API_KEY", "GROQ_BASE_URL"),
    base_url="https://api.groq.com/openai/v1",
    fallback_models=(
        "openai/gpt-oss-120b",
        "qwen/qwen3.8-27b",
        "openai/gpt-oss-20b",
    ),
)

register_provider(groq)
