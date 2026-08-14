<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="License">
  <img src="https://img.shields.io/github/stars/s1d9e/d2ath?style=flat-square" alt="Stars">
  <img src="https://img.shields.io/github/forks/s1d9e/d2ath?style=flat-square" alt="Forks">
  <img src="https://img.shields.io/badge/Version-2.0.0-blue?style=flat-square" alt="Version">
</p>

<p align="center">
  <b>All-in-one offensive & defensive security framework for Linux.</b><br>
  <i>External dependencies: none (Python standard library only).</i>
</p>

---

## ⚠️ Disclaimer

> **IMPORTANT**: This project is provided for **educational purposes only**.
> The author **accepts no responsibility** for any misuse of this tool.
> Any action performed without explicit consent is **illegal**.

---

## 📋 Table of contents

- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Structure](#-structure)
- [Development](#-development)
- [Requirements](#-requirements)
- [Legal notice](#-legal-notice)
- [License](#-license)

---

## 🔧 Features

| Category | Description |
|-----------|-------------|
| **Reconnaissance** | Parallel port scanning, ping scan, DNS, Whois, GeoIP, Traceroute |
| **Network** | Public/local IP, interfaces, gateway, port check, ping, subnet calculator, netdiscover, tshark |
| **Cryptography** | Strong password generator, hashing (MD5/SHA1/SHA256), Base64, URL encode/decode |
| **System** | System information, directory listing |
| **Exploitation** | Reverse shells, payload encode/decode, HTTP server, download & execute, msfvenom |
| **Audit** | Nmap, Masscan, Aircrack-ng, Nikto, Hydra, John, Hashcat, SQLMap |

### Highlights (v2.0)

- **Full CLI**: every tool can be invoked directly from the command line.
- **Package architecture** (`src/d2ath`): per-category modules, declarative registry, type hints, logging.
- **Zero third-party dependencies**: Python standard library only.
- **Parallel scans** (ports, ping) using `ThreadPoolExecutor`.
- **pytest tests** and **GitHub Actions CI** (ruff + multi-version tests).
- **`NO_COLOR` support**, typed errors, standard exit codes.

---

## 💻 Installation

```bash
# Option 1: pip install (recommended)
python3 -m venv .venv && . .venv/bin/activate
pip install -e .

# Option 2: without installation, from the repo
cd src && python3 -m d2ath --help

# Verify
d2ath --version
```

### Optional system tools

Some audit tools rely on system binaries (`nmap`, `hydra`, `sqlmap`, `whois`, …).
`d2ath` detects them and offers to install them automatically in interactive mode.

```bash
# Ubuntu / Debian (including Kali)
sudo apt install whois nmap masscan netdiscover tshark tcpdump nikto hydra john sqlmap

# Arch Linux
sudo pacman -S whois nmap masscan netdiscover wireshark-cli tcpdump nikto hydra john sqlmap

# Fedora
sudo dnf install nmap masscan netdiscover wireshark-cli tcpdump nikto hydra john sqlmap
```

---

## 🖥️ Usage

### Interactive menu

```bash
d2ath
```

### Command line

```bash
# List all tools
d2ath --list

# Invoke a tool directly
d2ath ports --target 192.168.1.1
d2ath ports --target 192.168.1.1 --start 1 --end 10000
d2ath password --length 20 --special true
d2ath netcalc --ip 192.168.1.37 --cidr 24
d2ath hashcat
```

Missing required parameters are asked interactively:

```bash
$ d2ath whois
[?] IP or domain: example.com
```

### Exit codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Execution failure |
| `2` | Usage error (missing/invalid argument) |
| `130` | Interrupted (Ctrl+C) |

---

## 📂 Structure

```
d2ath/
├── pyproject.toml            # Packaging, scripts, ruff/pytest config
├── src/d2ath/
│   ├── __init__.py           # Version
│   ├── __main__.py           # python -m d2ath
│   ├── cli.py                # argparse + entry point
│   ├── app.py                # Interactive TUI loop
│   ├── colors.py             # ANSI colors + NO_COLOR
│   ├── context.py            # Tool context (unified prompt / CLI)
│   ├── errors.py             # Typed exceptions
│   ├── registry.py           # Declarative tool registry
│   ├── ui.py                 # Banner and menus
│   ├── utils.py              # Network, subnet math, subprocess, packages
│   └── tools/
│       ├── recon.py          # Reconnaissance
│       ├── network.py        # Network
│       ├── crypto.py         # Cryptography
│       ├── system.py         # System
│       ├── exploit.py        # Exploitation (educational)
│       └── audit.py          # Audit
├── tests/                    # pytest tests
├── .github/workflows/ci.yml  # CI (ruff + pytest)
└── LICENSE                   # MIT License
```

---

## 🧪 Development

```bash
pip install -e ".[dev]"

# Lint
ruff check .

# Tests
pytest
```

---

## 📌 Requirements

- **Python 3.9+**
- **Operating system**: Linux (optimized for Kali, Ubuntu, Debian, Arch)
- **Permissions**: root/sudo required for some tools (netdiscover, aircrack-ng, masscan)

---

## ⚠️ Legal notice

**This program is intended for:**
- ✅ Authorized penetration testing
- ✅ Educational computer security
- ✅ Personal use on your own systems
- ✅ Cybersecurity research

**This program must not be used for:**
- ❌ Accessing systems without authorization
- ❌ Illegal or malicious activities
- ❌ Any other unethical or unlawful use

**The author cannot be held responsible for any inappropriate use.**

---

## 📄 License

This project is licensed under the **MIT** License. See the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <b>Made with ❤️ by <a href="https://github.com/s1d9e">s1d9e</a></b>
</p>
