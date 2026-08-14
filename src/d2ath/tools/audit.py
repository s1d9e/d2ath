"""Outils d'audit : nmap, masscan, aircrack, nikto, hydra, john, hashcat, sqlmap."""

from __future__ import annotations

import sys

from d2ath.context import ToolContext
from d2ath.registry import Param, register
from d2ath.tools.common import require_install, require_root
from d2ath.utils import run_passthrough

_PARAM_TARGET = Param("target", "Cible (IP / plage / URL)", required=True)


def _ssh_service(value: str) -> str:
    value = value.lower()
    if value not in ("ssh", "ftp", "http", "https", "rdp", "mysql", "smb", "pop3", "imap"):
        raise ValueError(f"service non supporté: {value}")
    return value


_HYDRA_SERVICE = Param(
    "service",
    "Service (ssh, ftp, http, rdp, mysql...)",
    default="ssh",
    type=_ssh_service,
    choices=("ssh", "ftp", "http", "https", "rdp", "mysql", "smb", "pop3", "imap"),
)
_HYDRA_USER = Param("user", "Utilisateur (ou -P pour wordlist)", default="admin")
_HYDRA_WORDLIST = Param("wordlist", "Wordlist", default="/usr/share/wordlists/rockyou.txt")
_MASS_PORTS = Param("ports", "Ports (ex: 1-1000 ou all)", default="1-1000")


@register(
    "audit",
    "nmap",
    "Nmap",
    "Scanner de ports avancé",
    params=(_PARAM_TARGET,),
)
def tool_nmap(ctx: ToolContext) -> int:
    ctx.header("Nmap")
    require_install(ctx, "nmap", "nmap")
    target = ctx.ask_param(_PARAM_TARGET)

    scans = {
        "1": ["nmap", "-F", target],
        "2": ["nmap", "-A", target],
        "3": ["nmap", "-sS", target],
        "4": ["nmap", "-sU", target],
    }
    ctx.info("Type de scan: [1] rapide  [2] complet -A  [3] SYN -sS  [4] UDP -sU")
    choice = _menu_choice(ctx, "1", "4")
    cmd = scans.get(choice, ["nmap", "-F", target])

    ctx.info(" ".join(cmd))
    return run_passthrough(["sudo", *cmd] if not sys.platform.startswith("win") else cmd, timeout=120)


@register(
    "audit",
    "masscan",
    "Masscan",
    "Scan massif ultra-rapide",
    params=(_PARAM_TARGET, _MASS_PORTS),
)
def tool_masscan(ctx: ToolContext) -> int:
    ctx.header("Masscan")
    require_install(ctx, "masscan", "masscan")
    require_root(ctx)
    target = ctx.ask_param(_PARAM_TARGET)
    ports = ctx.ask_param(_MASS_PORTS)
    ctx.info(f"Scan massif de {target} ports {ports} ...")
    return run_passthrough(
        ["sudo", "masscan", "-p", ports, target, "--rate", "1000"],
        timeout=120,
    )


@register("audit", "aircrack", "Aircrack-ng", "Suite d'attaques WiFi", requires_root=True)
def tool_aircrack(ctx: ToolContext) -> int:
    ctx.header("Aircrack-ng")
    require_install(ctx, "aircrack-ng", "aircrack-ng")
    require_root(ctx)

    ctx.info("[1] airmon-ng  [2] airodump-ng  [3] aireplay-ng  [4] aircrack-ng")
    choice = _menu_choice(ctx, "1", "4")

    if choice == "1":
        iface = input("  Interface WiFi (ex: wlan0) : ").strip()
        return run_passthrough(["sudo", "airmon-ng", "start", iface], timeout=30) if iface else 1
    if choice == "2":
        iface = input("  Interface (ex: wlan0mon) : ").strip() or "wlan0mon"
        return run_passthrough(["sudo", "airodump-ng", iface], timeout=60)
    if choice == "3":
        return run_passthrough(["sudo", "aireplay-ng", "--help"], timeout=15)
    capfile = input("  Fichier de capture (.cap) : ").strip()
    wordlist = input("  Wordlist (défaut rockyou.txt) : ").strip() or "/usr/share/wordlists/rockyou.txt"
    if not capfile:
        return 1
    return run_passthrough(["sudo", "aircrack-ng", "-w", wordlist, capfile], timeout=120)


@register(
    "audit",
    "nikto",
    "Nikto",
    "Scanner de vulnérabilités web",
    params=(_PARAM_TARGET,),
)
def tool_nikto(ctx: ToolContext) -> int:
    ctx.header("Nikto")
    require_install(ctx, "nikto", "nikto")
    target = ctx.ask_param(_PARAM_TARGET)
    ctx.info(f"Scan web de {target} ...")
    code = run_passthrough(["nikto", "-h", target, "-o", "nikto_scan.txt"], timeout=180)
    if code == 0:
        ctx.success("Résultat sauvegardé dans nikto_scan.txt")
    return code


@register(
    "audit",
    "hydra",
    "Hydra",
    "Attaque par force brute sur les services",
    params=(_PARAM_TARGET, _HYDRA_SERVICE, _HYDRA_USER, _HYDRA_WORDLIST),
)
def tool_hydra(ctx: ToolContext) -> int:
    ctx.header("Hydra")
    require_install(ctx, "hydra", "hydra")
    target = ctx.ask_param(_PARAM_TARGET)
    service = ctx.ask_param(_HYDRA_SERVICE)
    user = ctx.ask_param(_HYDRA_USER)
    wordlist = ctx.ask_param(_HYDRA_WORDLIST)

    cmd = ["hydra", "-l", user, "-P", wordlist, target, service]
    ctx.info(" ".join(cmd))
    return run_passthrough(cmd, timeout=180)


@register("audit", "john", "John the Ripper", "Cracker de mots de passe")
def tool_john(ctx: ToolContext) -> int:
    ctx.header("John the Ripper")
    require_install(ctx, "john", "john")

    ctx.info("[1] Crack hash  [2] Crack shadow  [3] Show")
    choice = _menu_choice(ctx, "1", "3")

    if choice == "1":
        hash_val = input("  Hash à cracker : ").strip()
        wordlist = input("  Wordlist (défaut rockyou.txt) : ").strip() or "/usr/share/wordlists/rockyou.txt"
        if not hash_val:
            return 1
        return run_passthrough(["john", f"--wordlist={wordlist}", "--format=raw-md5", hash_val], timeout=120)
    if choice == "2":
        shadow = input("  Fichier /etc/shadow (root requis) : ").strip()
        return run_passthrough(["sudo", "john", shadow], timeout=120) if shadow else 1
    hash_file = input("  Fichier de hash : ").strip()
    return run_passthrough(["john", "--show", hash_file], timeout=60) if hash_file else 1


@register("audit", "hashcat", "Hashcat", "Cracking GPU (hashcat)")
def tool_hashcat(ctx: ToolContext) -> int:
    ctx.header("Hashcat")
    require_install(ctx, "hashcat", "hashcat")

    modes = {"0": "MD5", "1000": "NTLM", "1800": "sha512crypt", "22000": "WPA-PBKDF2"}
    ctx.info("Mode: " + "  ".join(f"{k}={v}" for k, v in modes.items()))
    mode = input("  Mode hash (défaut 0) : ").strip() or "0"
    hash_file = input("  Fichier de hash : ").strip()
    wordlist = input("  Wordlist (défaut rockyou.txt) : ").strip() or "/usr/share/wordlists/rockyou.txt"
    if not hash_file:
        return 1
    return run_passthrough(["hashcat", "-m", mode, "-a", "0", hash_file, wordlist, "--force"], timeout=120)


@register(
    "audit",
    "sqlmap",
    "SQLMap",
    "Détection et exploitation d'injections SQL",
    params=(_PARAM_TARGET,),
)
def tool_sqlmap(ctx: ToolContext) -> int:
    ctx.header("SQLMap")
    require_install(ctx, "sqlmap", "sqlmap")
    target = ctx.ask_param(_PARAM_TARGET)

    ctx.info("[1] Détection  [2] Bases  [3] Tables  [4] Dump")
    choice = _menu_choice(ctx, "1", "4")

    cmd = ["sqlmap", "-u", target]
    if choice == "2":
        cmd.append("--dbs")
    elif choice == "3":
        db = input("  Nom de la base : ").strip()
        cmd.extend(["-D", db, "--tables"])
    elif choice == "4":
        db = input("  Base de données : ").strip()
        table = input("  Table : ").strip()
        cmd.extend(["-D", db, "-T", table, "--dump"])

    ctx.info(" ".join(cmd))
    return run_passthrough(cmd, timeout=180)


def _menu_choice(ctx: ToolContext, low: str, high: str) -> str:
    """Demande un choix de menu interactif (ou retourne le défaut en CLI)."""
    if not ctx.interactive:
        return low
    while True:
        choice = input("  Choix : ").strip()
        if low <= choice <= high:
            return choice
        ctx.warn(f"Choix invalide (attendu {low}-{high}).")
