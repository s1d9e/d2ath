"""Outils de reconnaissance : ports, ping, DNS, whois, GeoIP, traceroute."""

from __future__ import annotations

import socket
import sys

from d2ath.context import ToolContext
from d2ath.errors import ToolError
from d2ath.registry import Param, register
from d2ath.utils import (
    http_json,
    ping_scan,
    run_cmd,
    run_passthrough,
    scan_ports,
    which,
)


def _positive(value: str) -> int:
    number = int(value)
    if number < 1:
        raise ValueError("doit être ≥ 1")
    return number


_PORTS_TARGET = Param("target", "IP cible", required=True)
_PORTS_START = Param("start", "Port début", default="1", type=_positive)
_PORTS_END = Param("end", "Port fin", default="1024", type=_positive)
_PORTS_TIMEOUT = Param("timeout", "Timeout socket (s)", default="0.3", type=float)


@register(
    "recon",
    "ports",
    "Scan de ports",
    "Scanner les ports ouverts (TCP, parallèle)",
    params=(_PORTS_TARGET, _PORTS_START, _PORTS_END, _PORTS_TIMEOUT),
)
def tool_ports(ctx: ToolContext) -> int:
    ctx.header("Scan de ports")
    target = ctx.ask_param(_PORTS_TARGET)
    start = ctx.ask_param(_PORTS_START)
    end = ctx.ask_param(_PORTS_END)
    timeout = ctx.ask_param(_PORTS_TIMEOUT)

    if start > end:
        ctx.warn("Port début supérieur au port fin.")
        return 1
    end = min(end, 65535)

    ctx.info(f"Scan de {target} ports {start}-{end} ...")
    open_ports = scan_ports(target, start, end, timeout=timeout)

    if open_ports:
        ctx.success(f"{len(open_ports)} ports ouverts:")
        for port in open_ports:
            try:
                service = socket.getservbyport(port) or "?"
            except OSError:
                service = "?"
            ctx.success(f"{port:<6} {service}")
    else:
        ctx.warn("Aucun port ouvert trouvé.")
    return 0


_PING_SUBNET = Param("subnet", "Plage IP (ex: 192.168.1)", required=True)


@register(
    "recon",
    "ping",
    "Ping Scan",
    "Découverte des hôtes actifs d'un /24",
    params=(_PING_SUBNET,),
)
def tool_ping(ctx: ToolContext) -> int:
    ctx.header("Ping Scan")
    subnet = ctx.ask_param(_PING_SUBNET)

    if not subnet.replace(".", "").isdigit():
        ctx.warn("Plage invalide.")
        return 1

    ctx.info(f"Scan de {subnet}.0/24 en parallèle ...")
    active = ping_scan(subnet)

    if active:
        ctx.success(f"{len(active)} hôtes actifs:")
        for host in active:
            ctx.success(host)
    else:
        ctx.warn("Aucun hôte actif.")
    return 0


_DOMAIN = Param("domain", "Domaine", required=True)


@register(
    "recon",
    "dns",
    "DNS Lookup",
    "Résolution DNS et reverse lookup",
    params=(_DOMAIN,),
)
def tool_dns(ctx: ToolContext) -> int:
    ctx.header("DNS Lookup")
    domain = ctx.ask_param(_DOMAIN)

    try:
        ip = socket.gethostbyname(domain)
    except socket.gaierror as exc:
        ctx.warn(f"Domaine introuvable: {exc}")
        return 1

    ctx.success(f"{domain} → {ip}")

    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        ctx.success(f"Reverse: {hostname}")
    except socket.herror:
        ctx.warn("Pas de reverse DNS.")
    return 0


_TARGET = Param("target", "IP ou Domaine", required=True)


@register(
    "recon",
    "whois",
    "Whois",
    "Informations WHOIS d'un domaine ou d'une IP",
    params=(_TARGET,),
)
def tool_whois(ctx: ToolContext) -> int:
    ctx.header("Whois")
    target = ctx.ask_param(_TARGET)

    if not which("whois"):
        raise ToolError("'whois' n'est pas installé (apt/pacman/dnf install whois)")

    ctx.info(f"Recherche WHOIS sur {target} ...")
    try:
        result = run_cmd(["whois", target], timeout=15)
    except (OSError, TimeoutError) as exc:
        raise ToolError(str(exc)) from exc

    if result.returncode != 0 and not result.stdout:
        ctx.warn("Pas d'informations disponibles.")
        return 1
    ctx.say(result.stdout[:4000])
    return 0


_IP = Param("ip", "Adresse IP", required=True)


@register(
    "recon",
    "geoip",
    "GeoIP",
    "Localisation géographique d'une IP",
    params=(_IP,),
)
def tool_geoip(ctx: ToolContext) -> int:
    ctx.header("GeoIP Lookup")
    ip = ctx.ask_param(_IP)

    ctx.info(f"Localisation de {ip} ...")
    try:
        data = http_json(f"https://ipinfo.io/{ip}/json")
    except Exception as exc:  # noqa: BLE001 — erreur réseau remontée en texte
        raise ToolError(str(exc)) from exc

    if data.get("bogon"):
        ctx.warn("IP privée/bogon (non traçable).")
        return 0

    fields = {
        "IP": data.get("ip", ip),
        "Hostname": data.get("hostname", "N/A"),
        "Ville": data.get("city", "N/A"),
        "Région": data.get("region", "N/A"),
        "Pays": data.get("country", "N/A"),
        "Timezone": data.get("timezone", "N/A"),
        "ASN/ISP": data.get("org", "N/A"),
    }
    for label, value in fields.items():
        ctx.success(f"{label}: {value}")

    loc = data.get("loc", "")
    if loc and "," in loc:
        lat, lon = loc.split(",", 1)
        ctx.say(f"{' ' * 4}Maps: https://www.google.com/maps?q={lat},{lon}")
    return 0


@register(
    "recon",
    "traceroute",
    "Traceroute",
    "Chemin réseau vers une IP ou un domaine",
    params=(_TARGET,),
)
def tool_traceroute(ctx: ToolContext) -> int:
    ctx.header("Traceroute")
    target = ctx.ask_param(_TARGET)

    binary = "tracert" if sys.platform == "win32" else "traceroute"
    if not which(binary):
        raise ToolError(f"'{binary}' n'est pas installé")

    ctx.info(f"Traceroute vers {target} ...")
    try:
        code = run_passthrough([binary, target], timeout=30)
    except (OSError, TimeoutError) as exc:
        raise ToolError(str(exc)) from exc
    return code
