"""Tests du calcul réseau (purs, hors ligne)."""

from __future__ import annotations

import pytest

from d2ath.utils import netcalc


def test_class_c():
    plan = netcalc("192.168.1.37", 24)
    assert plan.network == "192.168.1.0/24"
    assert plan.broadcast == "192.168.1.255"
    assert plan.mask == "255.255.255.0"
    assert plan.first_ip == "192.168.1.1"
    assert plan.last_ip == "192.168.1.254"
    assert plan.host_count == 256


def test_slash_32():
    plan = netcalc("10.0.0.5", 32)
    assert plan.network == "10.0.0.5/32"
    assert plan.mask == "255.255.255.255"
    assert plan.host_count == 1


def test_slash_8():
    plan = netcalc("10.1.2.3", 8)
    assert plan.network == "10.0.0.0/8"
    assert plan.broadcast == "10.255.255.255"
    assert plan.mask == "255.0.0.0"


def test_invalid_cidr():
    with pytest.raises(ValueError):
        netcalc("10.0.0.1", 33)


def test_invalid_ip():
    with pytest.raises(ValueError):
        netcalc("999.1.1.1", 24)
    with pytest.raises(ValueError):
        netcalc("1.2.3", 24)
