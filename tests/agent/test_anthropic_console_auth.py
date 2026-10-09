"""Console API keys must not acquire Claude Code OAuth identity (#133856)."""

import pytest

from agent.anthropic_adapter import build_anthropic_client
from agent.anthropic_credentials import _is_oauth_token, anthropic_route_is_oauth


@pytest.mark.parametrize("prefix", ["sk-ant-api03-", "sk-ant-usr-"])
def test_console_keys_use_api_auth_without_claude_code_identity(prefix):
    key = prefix + "test-not-a-real-credential"
    base_url = "https://api.anthropic.com"
    assert not _is_oauth_token(key)
    assert not anthropic_route_is_oauth(base_url, key, provider="anthropic")
    client = build_anthropic_client(key, base_url)
    try:
        headers = client.default_headers
        assert headers["X-Api-Key"] == key
        assert "claude-code-20250219" not in headers.get("anthropic-beta", "")
        assert "oauth-2025-04-20" not in headers.get("anthropic-beta", "")
    finally:
        client.close()


@pytest.mark.parametrize("key", ["sk-ant-oat01-test", "eyJtest", "cc-test"])
def test_existing_oauth_credentials_keep_oauth_identity(key):
    assert _is_oauth_token(key)
    assert anthropic_route_is_oauth("https://api.anthropic.com", key, provider="anthropic")
