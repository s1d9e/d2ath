"""Interface TUI : bannière, menus et navigation."""

from __future__ import annotations

import os

from d2ath.colors import BOLD, GRAY, RESET, WHITE
from d2ath.registry import Registry, Tool

TITLE = [
    f"{WHITE}:::::::-.    .:::. .,::::::   :::. :::::::::::: ::   .:  {RESET}",
    f"{GRAY} ;;,   `';, ,;'``;.;;;;''''   ;;`;;;;;;;';;,;;   ;;, {RESET}",
    f"{GRAY} `[[     [[ ''  ,[['[[cccc   ,[[ '[[,   [[    ,[[[,,,[[[ {RESET}",
    f'{WHITE}  $$,    $$ .c$$P\'  $$""""  c$$$cc$$$c  $$    "$$$"""$$$ {RESET}',
    f"{GRAY} 888_,o8P'd88 _,oo,888oo,__ 888   888, 88,    888   \"88o{RESET}",
    f'{WHITE}  MMMMP"`  MMMUP*"^^""""YUMMMYMM   ""`  MMM    MMM    YMM {RESET}',
]

_BAR = "─" * 45


def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def banner() -> None:
    print()
    for line in TITLE:
        print(line)
    print()


def menu_categories(registry: Registry) -> str:
    """Affiche le menu des catégories et retourne le choix (q pour quitter)."""
    banner()
    print(f"{BOLD}   ┌─────────────────────────────────────────┐{RESET}")
    print(f"{BOLD}   │{RESET}         {WHITE}SÉLECTIONNER UNE CATÉGORIE{RESET}          {BOLD}│{RESET}")
    print(f"{BOLD}   └─────────────────────────────────────────┘{RESET}\n")

    for key, meta in registry.categories().items():
        count = len(registry.by_category(key))
        label = f"{BOLD}┌─[{WHITE} {key} {GRAY}]{RESET}  "
        label += f"{WHITE}▸ {meta['name']}{GRAY} ({count} outils){RESET}"
        print(f"   {label}")
        print(f"   {GRAY}└{'─' * 45}╜{RESET}")

    print(f"\n   {BOLD}┌─[{WHITE} q {GRAY}]{RESET}  {WHITE}Quitter{RESET}")
    print(f"   {GRAY}└{'─' * 20}╜{RESET}\n")
    return _prompt("└─>")


def menu_tools(category: str, tools: list[Tool]) -> str:
    """Affiche les outils d'une catégorie et retourne le choix (0 = retour)."""
    banner()
    print(f"{BOLD}   ╔{'═' * 45}╗{RESET}")
    print(f"{BOLD}   ║{RESET}  {WHITE}▸ {category.upper()}{RESET}")
    print(f"{BOLD}   ╚{'═' * 45}╝{RESET}\n")

    for i, tool in enumerate(tools, 1):
        print(f"   {BOLD}┌─{GRAY}[{WHITE}{i}{GRAY}]{RESET}  {WHITE}{tool.name}{RESET}")
        print(f"   {GRAY}│   {tool.description}{RESET}")
        print(f"   {GRAY}└{_BAR}╜{RESET}\n")

    print(f"   {BOLD}┌─{GRAY}[{WHITE}0{GRAY}]{RESET}  {WHITE}← Retour{RESET}")
    print(f"   {GRAY}└{'─' * 20}╜{RESET}\n")
    return _prompt("└─>")


def show_tool_list(registry: Registry) -> None:
    """Affiche la liste complète des outils groupés par catégorie."""
    print()
    for key, meta in registry.categories().items():
        tools = registry.by_category(key)
        if not tools:
            continue
        print(f"{WHITE}▸ {meta['name']}{RESET}")
        for tool in tools:
            root = " (root)" if tool.requires_root else ""
            print(f"   d2ath {tool.key}{GRAY} — {tool.description}{root}{RESET}")
    print()


def _prompt(symbol: str) -> str:
    try:
        return input(f"{WHITE}{symbol}{GRAY} ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        return "q"
