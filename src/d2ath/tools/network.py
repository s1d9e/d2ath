"""Outils réseau : IP, passerelle, ports, calcul réseau, netdiscover, wireshark."""

from __future__ import annotations

import socket
import sys

from d2ath.context import ToolContext
from d2ath.errors import ToolError
from d2ath.registry import Param, register
from d2ath.tools.common import require_install, require_root
from d2ath.utils import (
    get_my_ip,
    get_my_local_ip,
    http_json,
    netcalc,
    run_cmd,
    run_passthrough,
    which,
)

_PARAM_IFACE = Param("iface", "Interface réseau", default="eth0")


def _port_or_bool(value: str) -> int:
    number = int(value)
    if not 1 <= number <= 65535:
        raise ValueError("doit être entre 1 et 65535")
    return number


_PARAM_PORT = Param("port", "Port", required=True, type=_port_or_bool)
_PARAM_IP = Param("target", "IP cible", required=True)


@register("network", "myip", "Mon IP", "Afficher mon IP publique")
def tool_myip(ctx: ToolContext) -> int:
    ctx.header("Mon IP Publique")
    my_ip = get_my_ip()
    if not my_ip:
        ctx.warn("Impossible de récupérer l'IP publique (pas de réseau ?).")
        return 1
    ctx.success(f"IP Publique: {my_ip}")

    try:
        data = http_json(f"https://ipinfo.io/{my_ip}/json")
    except Exception:  # noqa: BLE001 — géoloc optionnelle
        return 0
    for label, key in (("Ville", "city"), ("Région", "region"), ("Pays", "country"), ("ISP", "org")):
        value = data.get(key)
        if value:
            ctx.success(f"{label}: {value}")
    return 0


@register("network", "iplocale", "IP Locale", "Afficher mon IP locale")
def tool_iplocale(ctx: ToolContext) -> int:
    ctx.header("Mon IP Locale")
    try:
        local = get_my_local_ip()
    except OSError as exc:
        ctx.warn(f"Erreur: {exc}")
        return 1
    ctx.success(f"IP Locale: {local}")
    try:
        ctx.success(f"Hôte: {socket.gethostname()}")
    except OSError:
        pass
    return 0


@register("network", "allips", "Toutes mes IPs", "Afficher toutes les interfaces réseau")
def tool_allips(ctx: ToolContext) -> int:
    ctx.header("Toutes mes IPs")
    try:
        result = run_cmd(["ip", "-o", "-4", "addr", "show"], timeout=5)
    except (OSError, TimeoutError) as exc:
        raise ToolError(str(exc)) from exc

    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 4:
            ctx.success(f"{parts[1]}: {parts[3]}")

    public = get_my_ip()
    if public:
        ctx.success(f"IP Publique: {public}")
    else:
        ctx.warn("IP publique indisponible.")
    return 0


@register("network", "gateway", "Passerelle", "Afficher la passerelle par défaut")
def tool_gateway(ctx: ToolContext) -> int:
    ctx.header("Passerelle (Gateway)")
    try:
        result = run_cmd(["ip", "route", "show", "default"], timeout=5)
    except (OSError, TimeoutError) as exc:
        raise ToolError(str(exc)) from exc

    fields = result.stdout.split()
    if len(fields) >= 3:
        gateway = fields[2]
        ctx.success(f"Passerelle: {gateway}")
        try:
            hostname = socket.gethostbyaddr(gateway)[0]
            ctx.success(f"DNS inverse: {hostname}")
        except (socket.herror, socket.gaierror):
            pass
    else:
        ctx.warn("Aucune route par défaut trouvée.")
        return 1
    return 0


@register(
    "network",
    "checkport",
    "Vérifier Port",
    "Vérifier si un port TCP est ouvert",
    params=(_PARAM_IP, _PARAM_PORT),
)
def tool_checkport(ctx: ToolContext) -> int:
    ctx.header("Vérifier port")
    target = ctx.ask_param(_PARAM_IP)
    port = ctx.ask_param(_PARAM_PORT)

    try:
        with socket.create_connection((target, port), timeout=2):
            ctx.success(f"Port {port} sur {target} est OUVERT.")
            return 0
    except OSError:
        ctx.warn(f"Port {port} sur {target} est FERMÉ / filtré.")
        return 1


_RAW_TARGET = Param("target", "IP ou Domaine", required=True)
_RAW_COUNT = Param("count", "Nombre de paquets", default="4")


@register(
    "network",
    "rawping",
    "Ping",
    "Ping simple d'une IP ou d'un domaine",
    params=(_RAW_TARGET, _RAW_COUNT),
)
def tool_rawping(ctx: ToolContext) -> int:
    ctx.header("Ping")
    target = ctx.ask_param(_RAW_TARGET)
    count = ctx.ask_param(_RAW_COUNT)
    param = "-n" if sys.platform == "win32" else "-c"
    return run_passthrough(["ping", param, str(count), target], timeout=30)


_CALC_IP = Param("ip", "Adresse IP (ex: 192.168.1.1)", required=True)
_CALC_CIDR = Param("cidr", "CIDR (ex: 24)", default="24")


@register(
    "network",
    "netcalc",
    "Calculatrice Réseau",
    "Calculer réseau/broadcast pour ip/cidr",
    params=(_CALC_IP, _CALC_CIDR),
)
def tool_netcalc(ctx: ToolContext) -> int:
    ctx.header("Calculatrice réseau")
    ip = ctx.ask_param(_CALC_IP)
    cidr = ctx.ask_param(_CALC_CIDR)

    try:
        plan = netcalc(ip, int(cidr))
    except ValueError as exc:
        ctx.warn(f"Erreur: {exc}")
        return 1

    for label, value in plan.display().items():
        ctx.success(f"{label}: {value}")
    return 0


@register(
    "network",
    "netdiscover",
    "Netdiscover",
    "Scanner le réseau local (ARP)",
    params=(_PARAM_IFACE,),
    requires_root=True,
)
def tool_netdiscover(ctx: ToolContext) -> int:
    ctx.header("Netdiscover")
    require_install(ctx, "netdiscover", "netdiscover")
    require_root(ctx)
    iface = ctx.ask_param(_PARAM_IFACE)
    ctx.info(f"Scan ARP sur {iface} ... (Ctrl+C pour arrêter)")
    return run_passthrough(["sudo", "netdiscover", "-i", iface, "-r", "0.0.0.0/24"], timeout=60)


@register(
    "network",
    "wireshark",
    "Wireshark",
    "Capture de paquets (tshark/tcpdump)",
    params=(_PARAM_IFACE,),
    requires_root=True,
)
def tool_wireshark(ctx: ToolContext) -> int:
    ctx.header("Wireshark / tshark")
    iface = ctx.ask_param(_PARAM_IFACE)

    if which("tshark"):
        ctx.info(f"Capture tshark sur {iface} (100 paquets) ...")
        try:
            return run_passthrough(["sudo", "tshark", "-i", iface, "-c", "100"], timeout=30)
        except ToolError:
            pass
    if which("tcpdump"):
        ctx.info(f"Capture tcpdump sur {iface} (50 paquets) ...")
        return run_passthrough(["sudo", "tcpdump", "-i", iface, "-c", "50"], timeout=30)

    raise ToolError("tshark/tcpdump non installés (apt install tshark tcpdump)")
