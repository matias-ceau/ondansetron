import os
import sys
import requests
import openai
import pytest

from ondansetron.search import (
    _perplexity_search,
    _openrouter_search,
    search,
)


class DummyResponse:
    def __init__(self, data):
        self._data = data

    def raise_for_status(self):
        pass

    def json(self):
        return self._data


@pytest.fixture(autouse=True)
def clear_env(monkeypatch):
    # Ensure no interfering env vars
    for key in ["OPENAI_API_KEY", "PERPLEXITY_API_KEY", "PERPLEXITY_API_URL",
                "OPENROUTER_API_KEY", "OPENROUTER_API_URL",
                "SEARCH_PROVIDER"]:
        monkeypatch.delenv(key, raising=False)


def test_perplexity_search_direct(monkeypatch):
    # Test low-level call uses OpenAI SDK and returns its response object
    class DummyClient:
        class chat:
            class completions:
                @staticmethod
                def create(model, messages, **kwargs):
                    return dummy

    dummy = type("Dummy", (), {})()
    dummy.choices = [{"message": {"content": {"foo": "bar"}}}]
    monkeypatch.setenv("OPENAI_API_KEY", "dummy")
    monkeypatch.setattr(openai, 'OpenAI', lambda api_key: DummyClient())
    result = _perplexity_search('q', 'key', None)
    assert result is dummy


def test_openrouter_search_direct(monkeypatch):
    dummy = {"choices": [{"message": {"content": "hi"}}]}
    monkeypatch.setattr(requests, 'post', lambda url, json, headers: DummyResponse(dummy))
    result = _openrouter_search('q', 'key', 'http://api')
    assert result == dummy


def test_search_perplexity_cli(monkeypatch, capsys):
    # Simulate full CLI for Perplexity via OpenAI SDK
    monkeypatch.setenv("OPENAI_API_KEY", "key1")
    class DummyClient:
        class chat:
            class completions:
                @staticmethod
                def create(model, messages, **kwargs):
                    return dummy

    dummy = type("Dummy", (), {})()
    dummy.choices = [{"message": {"content": "A1"}}]
    monkeypatch.setattr(openai, 'OpenAI', lambda api_key: DummyClient())
    # Run search and capture output
    search('foo')
    out = capsys.readouterr().out
    assert 'A1' in out


def test_search_openrouter_cli(monkeypatch, capsys):
    # Simulate full CLI for OpenRouter
    data = {"choices": [{"message": {"content": "OR1"}}]}
    monkeypatch.setenv("SEARCH_PROVIDER", "openrouter")
    monkeypatch.setenv("OPENROUTER_API_KEY", "key2")
    monkeypatch.setenv("OPENROUTER_API_URL", "http://api2")
    monkeypatch.setattr(requests, 'post', lambda url, json, headers: DummyResponse(data))
    search('bar')
    out = capsys.readouterr().out
    assert 'OR1' in out


def test_search_missing_key(monkeypatch, capsys):
    # No key for default provider
    monkeypatch.delenv("PERPLEXITY_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(SystemExit):
        search('x')