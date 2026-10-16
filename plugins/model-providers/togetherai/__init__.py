"""Together AI OpenAI-compatible provider profile."""

from providers import register_provider
from providers.base import ProviderProfile


togetherai = ProviderProfile(
    name="togetherai",
    aliases=("together", "together-ai"),
    display_name="Together AI",
    description="Together AI — OpenAI-compatible serverless inference",
    signup_url="https://api.together.ai/settings/api-keys",
    env_vars=("TOGETHER_API_KEY", "TOGETHERAI_API_KEY", "TOGETHER_BASE_URL"),
    base_url="https://api.together.xyz/v1",
    fallback_models=(
        "meta-models/Muse-Spark-Open-816B-A42B-promo",
        "meta-models/Muse-Spark-Open-816B-A42B",
        "meta-models/Muse-Glimmer-30B",
        "zai-org/GLM-5.3-FP8",
        "Qwen/Qwen3.5-122B-A10B-FP8",
        "MiniMaxAI/MiniMax-M2",
        "meta-llama/Llama-3.3-70B-Instruct-Turbo",
    ),
)

register_provider(togetherai)
