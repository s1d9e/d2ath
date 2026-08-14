"""Tests du registre et du contexte (hors ligne)."""

from __future__ import annotations

from argparse import Namespace

import pytest

from d2ath.context import ToolContext
from d2ath.errors import UsageError
from d2ath.registry import Registry, load_all


def _sample_registry() -> Registry:
    registry = Registry()
    registry.add_category("test", "TEST", "white")

    @registry.register("test", "demo", "Démo", "Outil de test", params=())
    def demo(ctx):  # noqa: ARG001
        return 0

    return registry


def test_registry_register_and_get():
    registry = _sample_registry()
    assert registry.get("demo") is not None
    assert registry.by_category("test")[0].key == "demo"
    assert registry.categories()["test"]["name"] == "TEST"


def test_registry_rejects_duplicate():
    registry = _sample_registry()
    with pytest.raises(ValueError):

        @registry.register("test", "demo", "Dup", "Doublon")
        def dup(ctx):  # noqa: ARG001
            return 0


def test_load_all_registers_real_tools():
    registry = load_all()
    for key in ("ports", "password", "netcalc", "revshell", "nmap", "sysinfo"):
        assert registry.get(key) is not None, key


def test_context_ask_non_interactive_required():
    ctx = ToolContext(args=Namespace(target="8.8.8.8"), interactive=False)
    assert ctx.ask("target", "IP cible", required=True) == "8.8.8.8"


def test_context_ask_non_interactive_missing():
    ctx = ToolContext(args=Namespace(), interactive=False)
    with pytest.raises(UsageError):
        ctx.ask("target", "IP cible", required=True)


def test_context_ask_default():
    ctx = ToolContext(args=Namespace(), interactive=False)
    assert ctx.ask("length", "Longueur", default="16") == "16"


def test_context_ask_type_conversion():
    ctx = ToolContext(args=Namespace(port=443), interactive=False)
    assert ctx.ask("port", "Port", required=True, type_=int) == 443


def test_context_ask_choices():
    ctx = ToolContext(args=Namespace(service="ftp"), interactive=False)
    assert ctx.ask("service", "Service", default="ssh", choices=("ssh", "ftp")) == "ftp"


def test_context_ask_bad_choices():
    ctx = ToolContext(args=Namespace(service="telnet"), interactive=False)
    with pytest.raises(UsageError):
        ctx.ask("service", "Service", choices=("ssh", "ftp"))


def test_context_ask_bad_type():
    ctx = ToolContext(args=Namespace(port="abc"), interactive=False)
    with pytest.raises(UsageError):
        ctx.ask("port", "Port", required=True, type_=int)
