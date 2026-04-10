# d2ath - Security Framework

```
██████╗ ███████╗███████╗██╗    ██╗ █████╗ ██╗     ██╗     ███████╗███████╗
██╔══██╗██╔════╝██╔════╝██║    ██║██╔══██╗██║     ██║     ██╔════╝██╔════╝
██████╔╝█████╗  █████╗  ██║ █╗ ██║███████║██║     ██║     █████╗  ███████╗
██╔══██╗██╔══╝  ██╔══╝  ██║███╗██║██╔══██║██║     ██║     ██╔══╝  ╚════██║
██║  ██║███████╗███████╗╚███╔███╔╝██║  ██║███████╗███████╗███████╗███████║
╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚══════╝
```

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="License">
  <img src="https://img.shields.io/github/stars/s1d9e/d2ath?style=flat-square" alt="Stars">
  <img src="https://img.shields.io/github/forks/s1d9e/d2ath?style=flat-square" alt="Forks">
</p>

<p align="center">
  <b>All-in-one offensive and defensive security framework for Linux.</b>
</p>

<p align="center">
  <b>All-in-one offensive and defensive security framework for Linux.</b>
</p>

---

## ⚠️ Disclaimer

> **IMPORTANT**: This project is provided for **educational purposes only**.
> The author **declines any responsibility** for misuse of this tool.
> Any unauthorized action without explicit consent is **illegal**.

---

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Screenshots](#-screenshots)
- [Structure](#-structure)
- [Requirements](#-requirements)
- [Disclaimer](#-disclaimer)
- [License](#-license)
- [Translations](#translations)

---

## 🔧 Features

### 📁 Categories

| Category | Description |
|----------|-------------|
| **Reconnaissance** | Port scan, ping scan, DNS lookup, Whois, GeoIP, Traceroute |
| **Network** | My IP, Local IP, Netdiscover, Wireshark, Ping, Port check |
| **Cryptography** | Password generator, Hash (MD5, SHA256), Base64, URL encode/decode |
| **System** | System info, File explorer |
| **Exploitation** | Reverse Shell, Encoder/Decoder payloads, HTTP server, Download & Execute, Metasploit |
| **Audit** | Nmap, Masscan, Aircrack-ng, Nikto, Hydra, John the Ripper, Hashcat, SQLMap |

### 🛠️ Integrated Tools

- **Port Scanner** - Fast scan of open ports
- **Ping Scan** - Discover active hosts on a network
- **DNS Lookup** - DNS resolution and reverse lookup
- **GeoIP** - Geographic location of an IP address
- **Netdiscover** - ARP scan of local network
- **Wireshark** - Network packet analyzer (tshark/tcpdump)
- **Nmap** - Advanced port scanner
- **Aircrack-ng** - WiFi attack suite
- **Hydra** - Brute force attack on login services
- **SQLMap** - Detection and exploitation of SQL injections
- **And more...**

---

## 💻 Installation

```bash
# Clone repository
git clone https://github.com/s1d9e/d2ath.git

# Enter directory
cd d2ath

# Make executable
chmod +x d2ath.py

# Run
python3 d2ath.py
```

### Dependencies (auto-installed if missing)

```bash
# Ubuntu / Debian
sudo apt update
sudo apt install python3 python3-pip whois curl nmap masscan netdiscover wireshark tshark tcpdump nikto hydra john sqlmap

# Arch Linux
sudo pacman -S python python-pip whois nmap masscan netdiscover wireshark-cli tcpdump nikto hydra john sqlmap

# Fedora
sudo dnf install python3 python3-pip nmap masscan netdiscover wireshark-cli tcpdump nikto hydra john sqlmap
```

---

## 📷 Screenshot

```
  ██████╗ ██████╗ ███╗   ██╗███████╗ ██████╗ ██╗     ███████╗███████╗
 ██╔════╝██╔═══██╗████╗  ██║██╔════╝██╔═══██╗██║     ██╔════╝██╔════╝
 ██║     ██║   ██║██╔██╗ ██║███████╗██║   ██║██║     █████╗  ███████╗
 ██║     ██║   ██║██║╚██╗██║╚════██║██║   ██║██║     ██╔══╝  ╚════██║
 ╚██████╗╚██████╔╝██║ ╚████║███████║╚██████╔╝███████╗███████╗███████║
  ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚══════╝╚══════╝╚══════╝
                                                                v2.0

    ╔════════════════════════════════════════════════════════════╗
    ║  d2ath - Security Framework                                   ║
    ║  Offensive & Defensive Security Toolkit                      ║
    ║                                                              ║
    ║     ██████╗ ██╗   ██╗██████╗ ███████╗██████╗                 ║
     ██╔═══██╗╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗                ║
    ║  ██████╔╝ ╚████╔╝ ██████╔╝█████╗  ██████╔╝                ║
    ║  ██╔═══╝   ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗                ║
    ║  ██║        ██║   ██████╔╝███████╗██║  ██║                ║
     ╚═╝         ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝                ║
    ║                                                              ║
    ║       [1] RECON    [2] NETWORK   [3] CRYPTO               ║
    ║       [4] SYSTEM   [5] EXPLOIT   [6] AUDIT               ║
    ╚════════════════════════════════════════════════════════════╝

   ┌─────────────────────────────────────────┐
   │         SELECT A CATEGORY              │
   └─────────────────────────────────────────┘

   ┌─[ 1 ]  ▸ RECONNAISSANCE
   └─────────────────────────────────────────────╜
   ┌─[ 2 ]  ▸ NETWORK
   └─────────────────────────────────────────────╜
   ┌─[ 3 ]  ▸ CRYPTOGRAPHY
   └─────────────────────────────────────────────╜
   ┌─[ 4 ]  ▸ SYSTEM
   └─────────────────────────────────────────────╜
   ┌─[ 5 ]  ▸ EXPLOITATION
   └─────────────────────────────────────────────╜
   ┌─[ 6 ]  ▸ AUDIT
   └─────────────────────────────────────────────╜

   ┌─[ q ]  Quit
   └────────────────────╜
```

---

## 📂 Structure

```
d2ath/
├── d2ath.py         # Main script
├── README.md        # English (main)
├── README_FR.md     # French
├── README_ES.md     # Spanish
├── README_DE.md     # German
├── LICENSE          # MIT License
└── .github/
    └── workflows/
        └── lint.yml
```

---

## 📌 Requirements

- **Python 3.8+**
- **OS**: Linux (optimized for Kali, Ubuntu, Debian, Arch)
- **Permissions**: root/sudo required for some tools (netdiscover, aircrack-ng, nmap)

---

## ⚠️ Legal Disclaimer

**This program is intended for:**
- ✅ Authorized penetration testing
- ✅ Educational computer security
- ✅ Personal use on your own systems
- ✅ Cybersecurity research

**This program must NOT be used for:**
- ❌ Unauthorized system access
- ❌ Illegal or malicious activities
- ❌ Any other unethical or illegal use

**The author cannot be held responsible for any inappropriate use.**

---

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 🌐 Translations

- [English](README.md) (Main)
- [Français](README_FR.md)
- [Español](README_ES.md)
- [Deutsch](README_DE.md)

---

<p align="center">
  <b>Made with ❤️ by <a href="https://github.com/s1d9e">s1d9e</a></b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-2.0-blue?style=flat-square" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=flat-square" alt="Python">
</p>