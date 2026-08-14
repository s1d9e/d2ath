"""Outils système : informations et exploration de fichiers."""

from __future__ import annotations

import os
import platform

from d2ath.colors import GRAY
from d2ath.context import ToolContext
from d2ath.errors import ToolError
from d2ath.registry import Param, register
from d2ath.utils import run_cmd


@register("system", "sysinfo", "Info Système", "Informations système complètes")
def tool_sysinfo(ctx: ToolContext) -> int:
    ctx.header("Informations système")
    uname = platform.uname()
    ctx.success(f"Système: {uname.system} {uname.release} ({uname.machine})")
    ctx.success(f"Hôte: {uname.node}")
    ctx.success(f"Version: {uname.version}")

    for cmd, label in (
        (["df", "-h"], "Disques"),
        (["free", "-h"], "Mémoire"),
        (["uptime"], "Uptime"),
    ):
        try:
            result = run_cmd(cmd, timeout=5)
        except (OSError, TimeoutError):
            continue
        ctx.say(f"\n{GRAY}{label}:{GRAY}")
        ctx.say(result.stdout.strip())
    return 0


_PATH = Param("path", "Répertoire", default=".")


@register(
    "system",
    "lsdir",
    "Liste Fichiers",
    "Lister les fichiers d'un répertoire",
    params=(_PATH,),
)
def tool_lsdir(ctx: ToolContext) -> int:
    ctx.header("Liste fichiers")
    path = ctx.ask_param(_PATH)

    if not os.path.isdir(path):
        raise ToolError(f"Répertoire introuvable: {path}")

    total = 0
    try:
        with os.scandir(path) as entries:
            for entry in sorted(entries, key=lambda e: e.name):
                if entry.is_dir():
                    ctx.say(f"  {entry.name}/")
                else:
                    try:
                        size = entry.stat().st_size
                    except OSError:
                        size = 0
                    ctx.say(f"  {entry.name}  ({size} octets)")
                total += 1
    except OSError as exc:
        raise ToolError(f"Impossible de lire le répertoire: {exc}") from exc

    ctx.say(f"\nTotal: {total} éléments")
    return 0
