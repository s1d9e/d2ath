"""Boucle interactive (TUI) de navigation dans les menus."""

from __future__ import annotations

from argparse import Namespace

from d2ath import ui
from d2ath.context import ToolContext
from d2ath.errors import D2athError
from d2ath.log import get_logger
from d2ath.registry import Registry
from d2ath.tools.common import require_root

logger = get_logger()


def run_interactive(registry: Registry) -> int:
    """Lance le menu et dispatche les outils sélectionnés."""
    current_category: str | None = None

    while True:
        ui.clear()
        try:
            if current_category is None:
                choice = ui.menu_categories(registry)
                if choice == "q":
                    ui.clear()
                    print("\nAu revoir !\n")
                    return 0
                if choice in registry.categories():
                    current_category = choice
            else:
                tools = registry.by_category(current_category)
                if not tools:
                    current_category = None
                    continue
                choice = ui.menu_tools(current_category, tools)
                if choice == "0":
                    current_category = None
                    continue
                if choice.isdigit():
                    index = int(choice) - 1
                    if 0 <= index < len(tools):
                        _run_tool(registry, tools[index].key)
        except KeyboardInterrupt:
            ui.clear()
            print("\nInterrompu.\n")
            current_category = None


def _run_tool(registry: Registry, key: str) -> None:
    tool = registry.get(key)
    if tool is None:
        return
    ui.clear()
    if tool.requires_root:
        require_root(ToolContext(Namespace(), interactive=True))
    ctx = ToolContext(Namespace(), interactive=True)
    try:
        ctx.say("")
        tool.handler(ctx)
        print("\n   Appuyez sur Entrée pour continuer...", end="")
        input()
    except D2athError as exc:
        logger.error("%s", exc)
        print("\n   Appuyez sur Entrée pour continuer...", end="")
        input()
