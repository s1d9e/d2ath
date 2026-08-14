"""Tests des outils cryptographie via leur contexte (hors ligne)."""

from __future__ import annotations

import hashlib
from argparse import Namespace
from io import StringIO

import pytest

from d2ath.context import ToolContext
from d2ath.tools import crypto


def make_ctx(**kwargs) -> tuple[ToolContext, StringIO]:
    out = StringIO()
    ctx = ToolContext(args=Namespace(**kwargs), interactive=False, out=out)
    return ctx, out


def test_md5_vector():
    ctx, _ = make_ctx(text="hello")
    assert crypto.tool_md5(ctx) == 0
    assert hashlib.md5(b"hello").hexdigest() in ctx.out.getvalue()


def test_sha256_vector():
    ctx, out = make_ctx(text="hello")
    assert crypto.tool_sha256(ctx) == 0
    assert hashlib.sha256(b"hello").hexdigest() in out.getvalue()


def test_base64_roundtrip():
    ctx, out = make_ctx(text="salut toi!")
    assert crypto.tool_b64e(ctx) == 0
    assert "c2FsdXQgdG9pIQ==" in out.getvalue()


def test_url_roundtrip():
    ctx, out = make_ctx(text="a b&c=d")
    crypto.tool_urle(ctx)
    encoded_line = out.getvalue()
    assert "a%20b%26c%3Dd" in encoded_line

    ctx2, out2 = make_ctx(text="a%20b%26c%3Dd")
    crypto.tool_urld(ctx2)
    assert "a b&c=d" in out2.getvalue()


def test_password_length_and_charset():
    ctx, out = make_ctx(length="16", special="true")
    assert crypto.tool_password(ctx) == 0
    line = [ln for ln in out.getvalue().splitlines() if "Mot de passe" in ln][0]
    password = line.split(":", 1)[1].strip()
    assert len(password) == 16
    assert any(c in "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~" for c in password)


def test_password_rejects_short():
    from d2ath.errors import UsageError

    ctx, _ = make_ctx(length="4", special="true")
    with pytest.raises(UsageError):
        crypto.tool_password(ctx)


def test_filehash(tmp_path):
    f = tmp_path / "data.bin"
    f.write_bytes(b"abc")
    ctx, out = make_ctx(file=str(f))
    assert crypto.tool_filehash(ctx) == 0
    content = out.getvalue()
    assert hashlib.md5(b"abc").hexdigest() in content
    assert hashlib.sha256(b"abc").hexdigest() in content
