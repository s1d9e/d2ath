"""Interface en ligne de commande (argparse)."""

from __future__ import annotations

import argparse
import sys
from argparse import Namespace

from d2ath import __version__, ui
from d2ath.context import ToolContext
from d2ath.errors import D2athError, UsageError
from d2ath.log import get_logger, set_verbose
from d2ath.registry import Registry, Tool, load_all

logger = get_logger()


def build_parser(registry: Registry) -> argparse.ArgumentParser:
    """Construit le parseur avec un sous-commande par outil enregistré."""
    parser = argparse.ArgumentParser(
        prog="d2ath",
        description="Framework de sécurité offensiva et defensiva pour Linux.",
        epilog="Sans sous-commande, d2ath lance le menu interactif.",
    )
    parser.add_argument("--version", action="version", version=f"d2ath {__version__}")
    parser.add_argument("-v", "--verbose", action="store_true", help="journal détaillé (DEBUG)")
    parser.add_argument("-l", "--list", action="store_true", help="liste tous les outils")

    subparsers = parser.add_subparsers(dest="tool_key", metavar="OUTIL")
    for tool in registry.all():
        sub = subparsers.add_parser(
            tool.key,
            help=f"[{tool.category}] {tool.name} — {tool.description}",
        )
        for param in tool.params:
            kwargs: dict = {"help": param.help, "type": param.type}
            if param.choices:
                kwargs["choices"] = list(param.choices)
            if param.default is not None and not param.required:
                kwargs["default"] = param.default
            sub.add_argument(f"--{param.name}", **kwargs)
    return parser


def _run(registry: Registry, tool: Tool, args: Namespace) -> int:
    ctx = ToolContext(args, interactive=sys.stdin.isatty())
    logger.debug("Exécution de l'outil %s (interactif=%s)", tool.key, ctx.interactive)
    return tool.handler(ctx)


def main(argv: list[str] | None = None) -> int:
    """Point d'entrée principal. Retourne le code de sortie."""
    registry = load_all()
    parser = build_parser(registry)
    args = parser.parse_args(argv)
    set_verbose(args.verbose)

    if args.list:
        ui.show_tool_list(registry)
        return 0

    if args.tool_key:
        tool = registry.get(args.tool_key)
        if tool is None:
            parser.error(f"outil inconnu: {args.tool_key}")
        try:
            return _run(registry, tool, args)
        except UsageError as exc:
            logger.error("%s", exc)
            return 2
        except D2athError as exc:
            logger.error("%s", exc)
            return 1
        except (OSError, TimeoutError) as exc:
            logger.error("%s", exc)
            return 1
        except KeyboardInterrupt:
            logger.warning("Interrompu.")
            return 130

    return ui_mode(registry)


def ui_mode(registry: Registry) -> int:
    """Délègue au menu interactif (réimporté ici pour éviter une dépendance circulaire)."""
    from d2ath.app import run_interactive

    return run_interactive(registry)
