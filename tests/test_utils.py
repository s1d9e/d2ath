"""Tests des utilitaires génériques (hors ligne)."""

from __future__ import annotations

import pytest

from d2ath.utils import _to_int, scan_ports, which


def test_to_int():
    assert _to_int("192.168.1.1") == 0xC0A80101


def test_which_known_command():
    assert which("python3") is True


def test_which_unknown_command():
    assert which("aucune-commande-de-test-xyz") is False


def test_scan_ports_rejects_bad_timeout():
    with pytest.raises(ValueError):
        scan_ports("127.0.0.1", 1, 5, timeout=0)


def test_scan_ports_empty_range():
    # plage de 1 port sur une adresse sans écoute → aucune exception, liste vide ou non
    result = scan_ports("127.0.0.1", 1, 1, timeout=0.05)
    assert isinstance(result, list)
