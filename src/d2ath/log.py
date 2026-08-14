"""Configuration du journal d'événements (logging)."""

from __future__ import annotations

import logging

_LOGGER_NAME = "d2ath"
_LOGGER: logging.Logger | None = None

FORMAT = "[%(levelname)s] %(message)s"


def get_logger() -> logging.Logger:
    """Retourne le logger principal du package (créé une seule fois)."""
    global _LOGGER
    if _LOGGER is None:
        _LOGGER = logging.getLogger(_LOGGER_NAME)
        _LOGGER.setLevel(logging.INFO)
        if not _LOGGER.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter(FORMAT))
            _LOGGER.addHandler(handler)
        _LOGGER.propagate = False
    return _LOGGER


def set_verbose(verbose: bool) -> logging.Logger:
    """Passe le logger en mode DEBUG (verbose) ou INFO."""
    logger = get_logger()
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    return logger
