"""Couleurs ANSI avec respect de la norme NO_COLOR et du terminal interactif."""

from __future__ import annotations

import os
import sys

_RESET = "\033[0m"


def _enabled() -> bool:
    """Active les couleurs uniquement sur un terminal interactif, sauf NO_COLOR."""
    if os.environ.get("NO_COLOR") is not None:
        return False
    return sys.stdout.isatty()


ENABLED = _enabled()


class Color:
    """Séquence ANSI composable. Retourne une chaîne vide si les couleurs sont désactivées."""

    __slots__ = ("_code", "_style")

    def __init__(self, code: str = "", style: str = "") -> None:
        self._code = code
        self._style = style

    def __str__(self) -> str:
        if not ENABLED:
            return ""
        return f"{self._style}{self._code}"

    def __bool__(self) -> bool:
        return ENABLED and bool(self._code)

    def bold(self) -> Color:
        """Retourne la même couleur en gras."""
        return Color(self._code, f"\033[1m{self._style}")

    def __add__(self, other: object) -> str:
        return f"{self}{other}"


RESET = Color(_RESET)
BOLD = Color(style="\033[1m")
DIM = Color(style="\033[2m")
UNDERLINE = Color(style="\033[4m")

FG = {
    "black": Color("\033[30m"),
    "red": Color("\033[31m"),
    "green": Color("\033[32m"),
    "yellow": Color("\033[33m"),
    "blue": Color("\033[34m"),
    "magenta": Color("\033[35m"),
    "cyan": Color("\033[36m"),
    "gray": Color("\033[90m"),
    "white": Color("\033[97m"),
}

BG = {
    "red": Color("\033[41m"),
    "green": Color("\033[42m"),
    "blue": Color("\033[44m"),
}

# Raccourcis utilisés par le reste du package.
WHITE = FG["white"]
GRAY = FG["gray"]
RED = FG["red"]
GREEN = FG["green"]
YELLOW = FG["yellow"]
CYAN = FG["cyan"]
