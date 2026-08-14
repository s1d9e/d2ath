"""Contexte d'exécution partagé entre les outils (mode interactif et CLI)."""

from __future__ import annotations

import sys
from argparse import Namespace
from dataclasses import dataclass, field
from typing import Any, Callable, TextIO

from d2ath.colors import GRAY, WHITE
from d2ath.errors import UsageError
from d2ath.registry import Param

Validator = Callable[[str], Any]


@dataclass
class ToolContext:
    """Fournit les paramètres (prompt ou CLI) et la sortie aux outils."""

    args: Namespace
    interactive: bool = False
    out: TextIO = field(default_factory=lambda: sys.stdout)

    def say(self, text: str = "", end: str = "\n") -> None:
        """Écrit sur la sortie configurée (capturable dans les tests)."""
        print(text, end=end, file=self.out)

    def info(self, text: str) -> None:
        self.say(f"{GRAY}[*] {text}")

    def success(self, text: str) -> None:
        self.say(f"{WHITE}[+] {text}")

    def warn(self, text: str) -> None:
        self.say(f"{GRAY}[!] {text}")

    def header(self, title: str) -> None:
        self.say(f"\n{GRAY}{'─' * 50}")
        self.say(f"{WHITE}[*] {title}{GRAY}")
        self.say(f"{GRAY}{'─' * 50}")

    def ask(
        self,
        name: str,
        help_text: str,
        required: bool = False,
        default: str | None = None,
        type_: Validator = str,
        choices: tuple[str, ...] | None = None,
    ) -> Any:
        """Récupère un paramètre : prompt interactif ou option CLI."""
        if self.interactive:
            return self._prompt(name, help_text, required, default, type_, choices)
        return self._from_args(name, help_text, required, default, type_, choices)

    def ask_param(self, param: Param) -> Any:
        """Récupère un paramètre depuis sa déclaration (prompt ou CLI)."""
        return self.ask(
            param.name,
            param.help,
            required=param.required,
            default=param.default,
            type_=param.type,
            choices=param.choices,
        )

    def _prompt(
        self,
        name: str,
        help_text: str,
        required: bool,
        default: str | None,
        type_: Validator,
        choices: tuple[str, ...] | None,
    ) -> Any:
        suffix = f" (défaut: {default})" if default is not None else ""
        if choices:
            self.say(f"{GRAY}   Choix: {', '.join(choices)}{GRAY}")
        while True:
            try:
                raw = input(f"{WHITE}[?] {help_text}{suffix}: {GRAY}").strip()
            except (EOFError, KeyboardInterrupt):
                raise UsageError("Saisie annulée") from None
            if raw == "" and default is not None:
                return type_(default)
            if raw == "" and not required:
                return None
            if raw == "":
                self.warn("Champ requis.")
                continue
            try:
                value = type_(raw)
            except ValueError as exc:
                self.warn(f"Valeur invalide: {exc}")
                continue
            if choices and value not in choices:
                self.warn(f"Choix invalide (attendu: {', '.join(choices)}).")
                continue
            return value

    def _from_args(
        self,
        name: str,
        help_text: str,
        required: bool,
        default: str | None,
        type_: Validator,
        choices: tuple[str, ...] | None,
    ) -> Any:
        value = getattr(self.args, name, None)
        if value is None:
            value = default
        if value is None and required:
            raise UsageError(f"Paramètre requis: --{name} ({help_text})")
        if value is not None and choices is not None and str(value) not in choices:
            raise UsageError(f"--{name}: choix invalide (attendu: {', '.join(choices)})")
        if value is not None and type_ is not str:
            try:
                value = type_(str(value))
            except ValueError as exc:
                raise UsageError(f"--{name}: valeur invalide ({exc})") from exc
        return value
