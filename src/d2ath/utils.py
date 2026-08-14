"""Utilitaires génériques : réseau, calcul réseau, sous-processus, gestion des paquets."""

from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any

from d2ath.errors import NetworkError
from d2ath.log import get_logger

logger = get_logger()


# ────────────────────────── Réseau ──────────────────────────


def http_json(url: str, timeout: int = 5) -> dict[str, Any]:
    """Récupère un document JSON via HTTPS. Lève NetworkError en cas d'échec."""
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as exc:
        raise NetworkError(f"Requête HTTP échouée: {exc}") from exc


def get_my_ip(timeout: int = 5) -> str | None:
    """Retourne l'IP publique, ou None si le réseau est indisponible."""
    for url in ("https://api.ipify.org", "http://ifconfig.me"):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as response:
                ip = response.read().decode("utf-8").strip()
                if ip:
                    return ip
        except (urllib.error.URLError, TimeoutError):
            continue
    return None


def get_my_local_ip() -> str:
    """Retourne l'IP locale de l'interface par défaut."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
        sock.close()
        return ip
    except OSError:
        return socket.gethostbyname(socket.gethostname())


@dataclass(frozen=True)
class NetworkPlan:
    """Résultat du calcul réseau."""

    network: str
    broadcast: str
    mask: str
    first_ip: str
    last_ip: str
    host_count: int

    def display(self) -> dict[str, str]:
        return {
            "Réseau": self.network,
            "Broadcast": self.broadcast,
            "Masque": self.mask,
            "Première IP": self.first_ip,
            "Dernière IP": self.last_ip,
            "Nombre d'IPs": str(self.host_count),
        }


def _to_int(ip: str) -> int:
    parts = ip.split(".")
    if len(parts) != 4:
        raise ValueError(f"Adresse IP invalide: {ip}")
    values = [int(p) for p in parts]
    if any(v < 0 or v > 255 for v in values):
        raise ValueError(f"Octet hors plage dans: {ip}")
    return (values[0] << 24) + (values[1] << 16) + (values[2] << 8) + values[3]


def _to_str(addr: int) -> str:
    return f"{(addr >> 24) & 255}.{(addr >> 16) & 255}.{(addr >> 8) & 255}.{addr & 255}"


def netcalc(ip: str, cidr: int) -> NetworkPlan:
    """Calcule le plan d'adressage réseau pour ip/cidr."""
    if not 0 <= cidr <= 32:
        raise ValueError(f"CIDR hors plage (0-32): {cidr}")
    ip_int = _to_int(ip)
    mask_int = (0xFFFFFFFF << (32 - cidr)) & 0xFFFFFFFF if cidr < 32 else 0xFFFFFFFF
    network = ip_int & mask_int
    broadcast = network | (~mask_int & 0xFFFFFFFF)
    host_count = 2 ** (32 - cidr)
    return NetworkPlan(
        network=f"{_to_str(network)}/{cidr}",
        broadcast=_to_str(broadcast),
        mask=_to_str(mask_int),
        first_ip=_to_str(network + 1),
        last_ip=_to_str(broadcast - 1),
        host_count=host_count,
    )


# ─────────────────────── Sous-processus ───────────────────────


def which(command: str) -> bool:
    """Vérifie la présence d'un binaire dans le PATH."""
    return shutil.which(command) is not None


def run_cmd(
    cmd: list[str],
    timeout: int | None = 30,
    check: bool = False,
) -> subprocess.CompletedProcess[str]:
    """Exécute une commande (sans shell) et capture sa sortie."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except FileNotFoundError as exc:
        raise OSError(f"Commande introuvable: {cmd[0]}") from exc
    except subprocess.TimeoutExpired as exc:
        raise TimeoutError(f"Commande expirée ({timeout}s): {cmd[0]}") from exc
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "code non nul"
        raise subprocess.CalledProcessError(result.returncode, cmd, output=detail)
    return result


def run_passthrough(cmd: list[str], timeout: int | None = None) -> int:
    """Exécute une commande en transmettant la sortie en direct (retourne le code)."""
    try:
        return subprocess.run(cmd, timeout=timeout).returncode
    except FileNotFoundError as exc:
        raise OSError(f"Commande introuvable: {cmd[0]}") from exc
    except subprocess.TimeoutExpired:
        raise TimeoutError(f"Commande expirée: {cmd[0]}") from None


# ─────────────────────── Gestion des paquets ───────────────────────


def distro_id() -> str | None:
    """Identifie la distribution via /etc/os-release."""
    try:
        with open("/etc/os-release", encoding="utf-8") as f:
            for line in f:
                if line.startswith("ID="):
                    return line.strip().split("=", 1)[1].strip('"')
    except OSError:
        return None
    return None


def _install_cmd(pkg: str) -> list[list[str]]:
    """Retourne les commandes d'installation pour la distribution détectée."""
    distro = distro_id()
    if distro in {"debian", "ubuntu", "linuxmint", "kali"}:
        return [["apt", "update"], ["apt", "install", "-y", pkg]]
    if distro in {"arch", "manjaro", "endeavouros"}:
        return [["pacman", "-S", "--noconfirm", pkg]]
    if distro in {"fedora"}:
        return [["dnf", "install", "-y", pkg]]
    return []


def install_pkg(pkg: str) -> bool:
    """Installe un paquet système via sudo. Retourne True en cas de succès."""
    commands = _install_cmd(pkg)
    if not commands:
        logger.error(
            "Distribution non reconnue, installez %s manuellement (apt/pacman/dnf).",
            pkg,
        )
        return False
    for cmd in commands:
        logger.info("Exécution: sudo %s", " ".join(cmd))
        result = run_passthrough(["sudo", *cmd])
        if result != 0:
            return False
    return True


# ─────────────────────── Scans concurrents ───────────────────────


def scan_ports(
    target: str,
    start: int,
    end: int,
    timeout: float = 0.3,
    workers: int = 256,
) -> list[int]:
    """Scanne une plage de ports TCP en parallèle. Retourne les ports ouverts."""
    if not 0 < timeout < 60:
        raise ValueError("Timeout invalide")

    def _probe(port: int) -> bool:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                return sock.connect_ex((target, port)) == 0
        except OSError:
            return False

    open_ports: list[int] = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(_probe, port): port for port in range(start, end + 1)}
        for future in futures:
            if future.result():
                open_ports.append(futures[future])
    return sorted(open_ports)


def ping_host(host: str, timeout: int = 2) -> bool:
    """Ping un hôte (1 paquet). Retourne True si l'hôte répond."""
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "1", host],
            capture_output=True,
            timeout=timeout,
        )
        return result.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def ping_scan(subnet: str, workers: int = 64) -> list[str]:
    """Découvre les hôtes actifs d'un /24 en parallèle."""
    hosts = [f"{subnet}.{i}" for i in range(1, 255)]

    def _probe(host: str) -> str | None:
        return host if ping_host(host) else None

    active: list[str] = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for result in pool.map(_probe, hosts):
            if result is not None:
                active.append(result)
    return active


# ─────────────────────── Divers ───────────────────────


def is_root() -> bool:
    """Indique si le processus tourne avec les droits root (Unix)."""
    return os.geteuid() == 0


def validate_ip(ip: str) -> str:
    """Valide une adresse IPv4 et la retourne."""
    try:
        socket.inet_aton(ip)
    except OSError as exc:
        raise ValueError(f"Adresse IP invalide: {ip}") from exc
    return ip
