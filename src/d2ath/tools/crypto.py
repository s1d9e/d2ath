"""Outils cryptographie : mots de passe, hashs, encodages."""

from __future__ import annotations

import base64
import hashlib
import math
import secrets
import string
from urllib.parse import quote, unquote

from d2ath.context import ToolContext
from d2ath.errors import ToolError
from d2ath.registry import Param, register


def _length(value: str) -> int:
    number = int(value)
    if not 8 <= number <= 128:
        raise ValueError("doit être entre 8 et 128")
    return number


_PASSWORD_LEN = Param("length", "Longueur", default="16", type=_length)
_PASSWORD_SPECIAL = Param("special", "Caractères spéciaux", default="true")


@register(
    "crypto",
    "password",
    "Générateur MDP",
    "Générer un mot de passe fort",
    params=(_PASSWORD_LEN, _PASSWORD_SPECIAL),
)
def tool_password(ctx: ToolContext) -> int:
    ctx.header("Générateur de mot de passe")
    length = ctx.ask_param(_PASSWORD_LEN)
    special = ctx.ask_param(_PASSWORD_SPECIAL)

    chars = string.ascii_letters + string.digits
    if special.lower() in ("true", "o", "oui", "1"):
        chars += string.punctuation

    password = "".join(secrets.choice(chars) for _ in range(length))
    ctx.success(f"Mot de passe: {password}")

    entropy = length * math.log2(len(chars))
    if entropy < 50:
        strength = "Faible"
    elif entropy < 80:
        strength = "Moyen"
    elif entropy < 120:
        strength = "Fort"
    else:
        strength = "Très fort"
    ctx.success(f"Force: {strength} (~{entropy:.0f} bits d'entropie)")
    return 0


def _hash_tool(ctx: ToolContext, algo: str, hexdigest_fn) -> int:
    ctx.header(f"Hash {algo.upper()}")
    text = ctx.ask("text", "Texte à hasher", required=True)
    ctx.success(f"{algo.upper()}: {hexdigest_fn(text)}")
    return 0


@register(
    "crypto",
    "md5",
    "Hash MD5",
    "Hasher un texte en MD5",
    params=(Param("text", "Texte à hasher", required=True),),
)
def tool_md5(ctx: ToolContext) -> int:
    return _hash_tool(ctx, "md5", lambda t: hashlib.md5(t.encode()).hexdigest())


@register(
    "crypto",
    "sha256",
    "Hash SHA256",
    "Hasher un texte en SHA256",
    params=(Param("text", "Texte à hasher", required=True),),
)
def tool_sha256(ctx: ToolContext) -> int:
    return _hash_tool(ctx, "sha256", lambda t: hashlib.sha256(t.encode()).hexdigest())


@register(
    "crypto",
    "filehash",
    "Hash Fichier",
    "Hasher un fichier (MD5, SHA1, SHA256)",
    params=(Param("file", "Chemin du fichier", required=True),),
)
def tool_filehash(ctx: ToolContext) -> int:
    ctx.header("Hash de fichier")
    path = ctx.ask("file", "Chemin du fichier", required=True)

    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5.update(chunk)
                sha1.update(chunk)
                sha256.update(chunk)
    except OSError as exc:
        raise ToolError(f"Impossible de lire le fichier: {exc}") from exc

    ctx.success(f"Fichier: {path}")
    ctx.success(f"MD5:    {md5.hexdigest()}")
    ctx.success(f"SHA1:   {sha1.hexdigest()}")
    ctx.success(f"SHA256: {sha256.hexdigest()}")
    return 0


@register(
    "crypto",
    "b64e",
    "Base64 Encode",
    "Encoder un texte en Base64",
    params=(Param("text", "Texte à encoder", required=True),),
)
def tool_b64e(ctx: ToolContext) -> int:
    ctx.header("Base64 Encode")
    text = ctx.ask("text", "Texte à encoder", required=True)
    ctx.success(base64.b64encode(text.encode()).decode())
    return 0


@register(
    "crypto",
    "b64d",
    "Base64 Decode",
    "Décoder un texte Base64",
    params=(Param("text", "Texte à décoder", required=True),),
)
def tool_b64d(ctx: ToolContext) -> int:
    ctx.header("Base64 Decode")
    text = ctx.ask("text", "Texte à décoder", required=True)
    try:
        decoded = base64.b64decode(text.encode(), validate=True).decode()
    except (ValueError, UnicodeDecodeError) as exc:
        raise ToolError(f"Décodage Base64 impossible: {exc}") from exc
    ctx.success(decoded)
    return 0


@register(
    "crypto",
    "urle",
    "URL Encode",
    "Encoder un texte pour une URL",
    params=(Param("text", "Texte à encoder", required=True),),
)
def tool_urle(ctx: ToolContext) -> int:
    ctx.header("URL Encode")
    text = ctx.ask("text", "Texte à encoder", required=True)
    ctx.success(quote(text, safe=""))
    return 0


@register(
    "crypto",
    "urld",
    "URL Decode",
    "Décoder un texte d'URL",
    params=(Param("text", "Texte à décoder", required=True),),
)
def tool_urld(ctx: ToolContext) -> int:
    ctx.header("URL Decode")
    text = ctx.ask("text", "Texte à décoder", required=True)
    try:
        decoded = unquote(text)
    except Exception as exc:  # noqa: BLE001 — unquote lève rarement
        raise ToolError(f"Décodage impossible: {exc}") from exc
    ctx.success(decoded)
    return 0
