"""Helpers partagés entre les modules d'outils."""

from __future__ import annotations

from d2ath.context import ToolContext
from d2ath.errors import ToolError
from d2ath.utils import install_pkg, is_root, which


def require_install(ctx: ToolContext, binary: str, pkg: str) -> None:
    """Vérifie qu'un binaire est présent ; propose l'installation en interactif."""
    if which(binary):
        return
    ctx.warn(f"'{binary}' n'est pas installé.")
    if ctx.interactive and input("  [o/n] Installer ? ").strip().lower() == "o":
        if install_pkg(pkg):
            ctx.success("Installation terminée.")
            return
        raise ToolError("Installation échouée.")
    raise ToolError(f"'{binary}' n'est pas installé (apt/pacman/dnf install {pkg})")


def require_root(ctx: ToolContext) -> None:
    """Signale quand les droits root sont requis."""
    if not is_root():
        ctx.warn("Cette opération nécessite les droits root (sudo).")
