"""Registre des outils : enregistrement déclaratif et découverte."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from d2ath.context import ToolContext

ToolHandler = Callable[["ToolContext"], int]


@dataclass(frozen=True)
class Param:
    """Déclaration d'un paramètre d'outil (prompt + option CLI)."""

    name: str
    help: str
    required: bool = False
    default: str | None = None
    type: Callable[[str], Any] = str
    choices: tuple[str, ...] | None = None


@dataclass(frozen=True)
class Tool:
    """Description d'un outil enregistré."""

    key: str
    name: str
    description: str
    category: str
    handler: ToolHandler
    params: tuple[Param, ...] = ()
    requires_root: bool = False


class Registry:
    """Registre contenant tous les outils, groupés par catégorie."""

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}
        self._categories: dict[str, dict[str, str]] = {}

    def add_category(self, key: str, name: str, color: str) -> None:
        self._categories[key] = {"name": name, "color": color}

    def register(
        self,
        category: str,
        key: str,
        name: str,
        description: str,
        params: tuple[Param, ...] = (),
        requires_root: bool = False,
    ) -> Callable[[ToolHandler], ToolHandler]:
        """Décorateur enregistrant une fonction comme outil."""

        def deco(fn: ToolHandler) -> ToolHandler:
            if key in self._tools:
                raise ValueError(f"Outil en double: {key}")
            self._tools[key] = Tool(
                key=key,
                name=name,
                description=description,
                category=category,
                params=params,
                requires_root=requires_root,
                handler=fn,
            )
            return fn

        return deco

    def get(self, key: str) -> Tool | None:
        return self._tools.get(key)

    def all(self) -> list[Tool]:
        return sorted(self._tools.values(), key=lambda t: (t.category, t.key))

    def by_category(self, category: str) -> list[Tool]:
        return [t for t in self._tools.values() if t.category == category]

    def categories(self) -> dict[str, dict[str, str]]:
        return self._categories


def _build() -> Registry:
    """Construit le registre et le remplit avec les catégories."""
    registry = Registry()
    registry.add_category("recon", "RECONNAISSANCE", "gray")
    registry.add_category("network", "RÉSEAU", "white")
    registry.add_category("crypto", "CRYPTOGRAPHIE", "gray")
    registry.add_category("system", "SYSTÈME", "white")
    registry.add_category("exploit", "EXPLOITATION", "gray")
    registry.add_category("audit", "AUDIT", "gray")
    return registry


REGISTRY = _build()


def register(
    category: str,
    key: str,
    name: str,
    description: str,
    params: tuple[Param, ...] = (),
    requires_root: bool = False,
) -> Callable[[ToolHandler], ToolHandler]:
    """Raccourci vers REGISTRY.register."""
    return REGISTRY.register(category, key, name, description, params, requires_root)


def load_all() -> Registry:
    """Importe tous les modules d'outils (enregistre les outils) et retourne le registre."""
    from d2ath import tools  # noqa: F401  (effet de bord : enregistrement)

    return REGISTRY
