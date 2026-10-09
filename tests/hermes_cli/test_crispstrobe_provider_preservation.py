"""Fork provider compatibility through upstream's plugin discovery (offline)."""

import pytest

from hermes_cli import providers as provider_defs
from hermes_cli.auth import PROVIDER_REGISTRY, resolve_api_key_provider_credentials, resolve_provider
from hermes_cli.model_normalize import normalize_model_for_provider
from hermes_cli.models import (
    CANONICAL_PROVIDERS,
    _PROVIDER_ALIASES,
    _PROVIDER_LABELS,
    normalize_provider,
    provider_model_ids,
)
from providers import get_provider_profile


CASES = [
    ("mistral", "Mistral AI", ("MISTRAL_API_KEY",), "MISTRAL_BASE_URL",
     "https://api.mistral.ai/v1", ("mistral-ai", "mistralai")),
    ("scaleway", "Scaleway Generative APIs", ("SCALEWAY_API_KEY", "SCW_SECRET_KEY"),
     "SCALEWAY_BASE_URL", "https://api.scaleway.ai/v1", ("scw", "scaleway-ai")),
    ("nebius-token-factory", "Nebius Token Factory",
     ("NEBIUS_API_KEY", "NEBIUS_TOKEN_FACTORY_API_KEY"), "NEBIUS_BASE_URL",
     "https://api.tokenfactory.nebius.com/v1", ("nebius", "nebius-ai", "nebius-studio")),
]


@pytest.fixture(autouse=True)
def offline_catalog(monkeypatch):
    # Exercise the Hermes-only overlay path even on a machine with a warm catalog.
    monkeypatch.setattr("agent.models_dev.get_provider_info", lambda *a, **kw: None)
    monkeypatch.setattr("agent.models_dev.list_agentic_models", lambda *a, **kw: [])
    for _, _, keys, url_env, _, _ in CASES:
        for key in (*keys, url_env):
            monkeypatch.delenv(key, raising=False)


@pytest.mark.parametrize("slug,label,keys,url_env,url,aliases", CASES)
def test_profile_registry_picker_and_overlay_without_models_dev(slug, label, keys, url_env, url, aliases):
    profile = get_provider_profile(slug)
    assert profile is not None
    assert profile.display_name == label
    assert profile.base_url == url
    assert profile.env_vars == (*keys, url_env)
    assert profile.fallback_models
    assert profile.api_mode == "chat_completions"

    registry = PROVIDER_REGISTRY[slug]
    assert registry.name == label
    assert registry.auth_type == "api_key"
    assert registry.api_key_env_vars == keys
    assert registry.base_url_env_var == url_env
    assert registry.inference_base_url == url
    assert [p.slug for p in CANONICAL_PROVIDERS].count(slug) == 1
    assert _PROVIDER_LABELS[slug] == label

    overlay = provider_defs.HERMES_OVERLAYS[slug]
    assert overlay.base_url_override == url
    assert overlay.base_url_env_var == url_env
    assert overlay.transport == "openai_chat"
    definition = provider_defs.get_provider(slug, allow_network=False)
    assert definition.name == label
    assert definition.api_key_env_vars == keys
    assert definition.base_url == url
    assert provider_defs.get_label(slug) == label
    assert provider_defs.determine_api_mode(slug, url) == "chat_completions"


@pytest.mark.parametrize("slug,label,keys,url_env,url,aliases", CASES)
def test_legacy_aliases_across_resolution_surfaces(monkeypatch, slug, label, keys, url_env, url, aliases):
    monkeypatch.setenv(keys[0], "test-provider-key")
    profile = get_provider_profile(slug)
    assert profile is not None
    model = profile.fallback_models[0]
    for alias in aliases:
        assert get_provider_profile(alias) is profile
        assert resolve_provider(alias) == slug
        assert normalize_provider(alias) == slug
        assert _PROVIDER_ALIASES[alias] == slug
        assert provider_defs.ALIASES[alias] == slug
        assert provider_defs.normalize_provider(alias) == slug
        assert provider_defs.get_provider(alias).id == slug
        assert normalize_model_for_provider(f"{alias}/{model}", alias) == model


@pytest.mark.parametrize("slug,label,keys,url_env,url,aliases", CASES)
def test_credentials_and_base_url_override(monkeypatch, slug, label, keys, url_env, url, aliases):
    monkeypatch.setenv(keys[0], "test-primary-key")
    creds = resolve_api_key_provider_credentials(slug)
    assert creds["api_key"] == "test-primary-key"
    assert creds["base_url"] == url
    monkeypatch.setenv(url_env, "https://override.example/v1")
    creds = resolve_api_key_provider_credentials(slug)
    assert creds["provider"] == slug
    assert creds["base_url"] == "https://override.example/v1"


def test_scaleway_legacy_secret_key_fallback_and_primary_precedence(monkeypatch):
    monkeypatch.setenv("SCW_SECRET_KEY", "test-legacy-key")
    creds = resolve_api_key_provider_credentials("scaleway")
    assert creds["api_key"] == "test-legacy-key"
    assert creds["source"] == "SCW_SECRET_KEY"
    monkeypatch.setenv("SCALEWAY_API_KEY", "test-primary-key")
    creds = resolve_api_key_provider_credentials("scaleway")
    assert creds["api_key"] == "test-primary-key"
    assert creds["source"] == "SCALEWAY_API_KEY"


@pytest.mark.parametrize("slug,label,keys,url_env,url,aliases", CASES)
def test_offline_picker_uses_profile_fallbacks(monkeypatch, slug, label, keys, url_env, url, aliases):
    profile = get_provider_profile(slug)
    assert profile is not None
    monkeypatch.setattr(profile, "fetch_models", lambda **kwargs: None)
    result = provider_model_ids(aliases[-1])
    assert result
    assert result == list(profile.fallback_models)


@pytest.mark.parametrize("slug,label,keys,url_env,url,aliases", CASES[:2])
def test_live_model_discovery_receives_resolved_override(monkeypatch, slug, label, keys, url_env, url, aliases):
    profile = get_provider_profile(slug)
    assert profile is not None
    monkeypatch.setenv(keys[0], "test-discovery-key")
    monkeypatch.setenv(url_env, "https://override.example/v1")
    calls = []

    def fetch_models(**kwargs):
        calls.append(kwargs)
        return [profile.fallback_models[0], "new-live-model"]

    monkeypatch.setattr(profile, "fetch_models", fetch_models)
    result = provider_model_ids(slug)
    assert calls
    assert calls[0]["api_key"] == "test-discovery-key"
    assert calls[0]["base_url"] == "https://override.example/v1"
    assert result == [*profile.fallback_models, "new-live-model"]
