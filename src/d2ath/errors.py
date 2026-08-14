"""Exceptions spécifiques à d2ath."""

from __future__ import annotations


class D2athError(Exception):
    """Erreur de base du package."""


class UsageError(D2athError):
    """Paramètre manquant ou invalide (code de sortie 2)."""


class ToolError(D2athError):
    """Échec d'exécution d'un outil (code de sortie 1)."""


class NetworkError(D2athError):
    """Échec d'une requête réseau."""
