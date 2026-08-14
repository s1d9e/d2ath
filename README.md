<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="License">
  <img src="https://img.shields.io/github/stars/s1d9e/d2ath?style=flat-square" alt="Stars">
  <img src="https://img.shields.io/github/forks/s1d9e/d2ath?style=flat-square" alt="Forks">
  <img src="https://img.shields.io/badge/Version-2.0.0-blue?style=flat-square" alt="Version">
</p>

<p align="center">
  <b>Framework de sécurité offensiva et defensiva tout-en-un pour Linux.</b><br>
  <i>Dépendances externes : aucune (bibliothèque standard uniquement).</i>
</p>

---

## ⚠️ Avertissement

> **IMPORTANT** : Ce projet est fourni à des fins **éducatives uniquement**.
> L'auteur **décline toute responsabilité** en cas de mauvaise utilisation de cet outil.
> Toute action interdite sans consentement explicite est **illégale**.

---

## 📋 Sommaire

- [Fonctionnalités](#-fonctionnalités)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Structure](#-structure)
- [Développement](#-développement)
- [Prérequis](#-prérequis)
- [Avertissement légal](#-avertissement-légal)
- [Licence](#-licence)

---

## 🔧 Fonctionnalités

| Catégorie | Description |
|-----------|-------------|
| **Reconnaissance** | Scan de ports (parallèle), ping scan, DNS, Whois, GeoIP, Traceroute |
| **Réseau** | IP publique/locale, interfaces, passerelle, port, ping, calculatrice réseau, netdiscover, tshark |
| **Cryptographie** | Mots de passe forts, hashs (MD5/SHA1/SHA256), Base64, URL encode/decode |
| **Système** | Informations système, exploration de fichiers |
| **Exploitation** | Reverse shells, encode/décode payloads, serveur HTTP, download & execute, msfvenom |
| **Audit** | Nmap, Masscan, Aircrack-ng, Nikto, Hydra, John, Hashcat, SQLMap |

### Points forts (v2.0)

- **CLI complète** : chaque outil est appelable directement en une ligne.
- **Architecture en package** (`src/d2ath`) : modules par catégorie, registre déclaratif, types, logging.
- **Aucune dépendance tierce** : bibliothèque standard Python uniquement.
- **Scans parallèles** (ports, ping) avec `ThreadPoolExecutor`.
- **Tests pytest** et **CI GitHub Actions** (ruff + tests multi-versions).
- **`NO_COLOR` supporté**, erreurs typées, codes de sortie standard.

---

## 💻 Installation

```bash
# Option 1 : installation pip (recommandée)
python3 -m venv .venv && . .venv/bin/activate
pip install -e .

# Option 2 : sans installation, depuis le dépôt
cd src && python3 -m d2ath --help

# Vérification
d2ath --version
```

### Outils système optionnels

Certains outils d'audit s'appuient sur des binaires système (`nmap`, `hydra`, `sqlmap`, `whois`, …).
`d2ath` les détecte et propose de les installer automatiquement en mode interactif.

```bash
# Ubuntu / Debian (Kali inclus)
sudo apt install whois nmap masscan netdiscover tshark tcpdump nikto hydra john sqlmap

# Arch Linux
sudo pacman -S whois nmap masscan netdiscover wireshark-cli tcpdump nikto hydra john sqlmap

# Fedora
sudo dnf install nmap masscan netdiscover wireshark-cli tcpdump nikto hydra john sqlmap
```

---

## 🖥️ Utilisation

### Menu interactif

```bash
d2ath
```

### Ligne de commande

```bash
# Lister tous les outils
d2ath --list

# Appeler un outil directement
d2ath ports --target 192.168.1.1
d2ath ports --target 192.168.1.1 --start 1 --end 10000
d2ath password --length 20 --special true
d2ath netcalc --ip 192.168.1.37 --cidr 24
d2ath hashcat
```

Sans paramètres requis, l'outil vous les demande interactivement :

```bash
$ d2ath whois
[?] IP ou Domaine : example.com
```

### Codes de sortie

| Code | Signification |
|------|---------------|
| `0` | Succès |
| `1` | Échec d'exécution |
| `2` | Erreur d'usage (paramètre manquant/invalide) |
| `130` | Interruption (Ctrl+C) |

---

## 📂 Structure

```
d2ath/
├── pyproject.toml            # Packaging, scripts, config ruff/pytest
├── src/d2ath/
│   ├── __init__.py           # Version
│   ├── __main__.py           # python -m d2ath
│   ├── cli.py                # Argparse + point d'entrée
│   ├── app.py                # Boucle TUI interactive
│   ├── colors.py             # ANSI + NO_COLOR
│   ├── context.py            # Contexte d'outil (prompt / CLI unifiés)
│   ├── errors.py             # Exceptions typées
│   ├── registry.py           # Registre déclaratif des outils
│   ├── ui.py                 # Bannière et menus
│   ├── utils.py              # Réseau, calcul réseau, sous-processus, paquets
│   └── tools/
│       ├── recon.py          # Reconnaissance
│       ├── network.py        # Réseau
│       ├── crypto.py         # Cryptographie
│       ├── system.py         # Système
│       ├── exploit.py        # Exploitation (pédagogique)
│       └── audit.py          # Audit
├── tests/                    # Tests pytest
├── .github/workflows/ci.yml  # CI (ruff + pytest)
└── LICENSE                   # Licence MIT
```

---

## 🧪 Développement

```bash
pip install -e ".[dev]"

# Lint
ruff check .

# Tests
pytest
```

---

## 📌 Prérequis

- **Python 3.9+**
- **Système d'exploitation** : Linux (optimisé pour Kali, Ubuntu, Debian, Arch)
- **Permissions** : root/sudo requis pour certains outils (netdiscover, aircrack-ng, masscan)

---

## ⚠️ Avertissement légal

**Ce programme est destiné à :**
- ✅ Tests de pénétration autorisés
- ✅ Sécurité informatique éducative
- ✅ Usage personnel sur vos propres systèmes
- ✅ Recherche en cybersécurité

**Ce programme ne doit pas être utilisé pour :**
- ❌ Accéder à des systèmes sans autorisation
- ❌ Activités illégales ou malveillantes
- ❌ Tout autre usage non éthique ou non légal

**L'auteur ne peut être tenu responsable de toute utilisation inappropriée.**

---

## 📄 Licence

Ce projet est sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

<p align="center">
  <b>Fait avec ❤️ par <a href="https://github.com/s1d9e">s1d9e</a></b>
</p>
