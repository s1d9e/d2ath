# ██╗███╗   ██╗██╗  ██╗██╗   ██╗███████╗
# ██║████╗  ██║██║ ██╔╝██║   ██║██╔════╝
# ██║██╔██╗ ██║█████╔╝ ██║   ██║███████╗
# ██║██║╚██╗██║██╔═██╗ ██║   ██║╚════██║
# ██║██║ ╚████║██║  ██╗╚██████╔╝███████║
# ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
# ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="License">
  <img src="https://img.shields.io/github/stars/s1d9e/d2ath?style=flat-square" alt="Stars">
  <img src="https://img.shields.io/github/forks/s1d9e/d2ath?style=flat-square" alt="Forks">
</p>

<p align="center">
  <b>Framework de sécurité ofensiva et défensiva tout-en-un pour Linux.</b>
</p>

---

## ⚠️ Avertissement

> **IMPORTANT** : Ce projet est fourni à des fins **éducatives uniquement**. 
> L'auteur **décline toute responsabilité** en cas de mauvaise utilisation de cet outil.
> Toute action interdite sans consentement explicite est **illégale**.

---

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Installation](#-installation)
- [Capture d'écran](#-capture-décran)
- [Structure](#-structure)
- [Prérequis](#-prérequis)
- [Avertissement](#-avertissement)
- [Licence](#-licence)

---

## 🔧 Fonctionnalités

### 📁 Structure par catégorie

| Catégorie | Description |
|-----------|-------------|
| **Reconnaissance** | Scan de ports, ping scan, DNS lookup, Whois, GeoIP, Traceroute |
| **Réseau** | Mon IP, IP locale, Netdiscover, Wireshark, Ping, Vérification de port |
| **Cryptographie** | Générateur de mots de passe, Hash (MD5, SHA256), Base64, URL encode/decode |
| **Système** | Informations système, Exploration de fichiers |
| **Exploitation** | Reverse Shell, Encoder/Decoder payloads, Serveur HTTP, Download & Execute, Metasploit |
| **Audit** | Nmap, Masscan, Aircrack-ng, Nikto, Hydra, John the Ripper, Hashcat, SQLMap |

### 🛠️ Outils intégrés

- **Scanner de ports** - Scan rapide des ports ouverts
- **Ping scan** - Découverte des hôtes actifs sur un réseau
- **DNS Lookup** - Résolution DNS et reverse lookup
- **GeoIP** - Localisation géographique d'une adresse IP
- **Netdiscover** - Scan ARP du réseau local
- **Wireshark** - Analyseur de paquets réseau (tshark/tcpdump)
- **Nmap** - Scanner de ports avancé
- **Aircrack-ng** - Suite d'outils pour attaques WiFi
- **Hydra** - Attaque par force brute sur les services de connexion
- **SQLMap** - Détection et exploitation d'injections SQL
- **Et bien plus...**

---

## 💻 Installation

```bash
# Cloner le dépôt
git clone https://github.com/s1d9e/d2ath.git

# Entrer dans le répertoire
cd d2ath

# Rendre le script exécutable
chmod +x d2ath.py

# Exécuter
python3 d2ath.py
```

### Dépendances (installation automatique si manquantes)

La plupart des dépendances sont installées automatiquement. Pour une installation manuelle :

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

## 📷 Capture d'écran

```
:::::::-.    .:::. .,::::::   :::. :::::::::::: ::   .:  
 ;;,   `';, ,;'``;.;;;;''''   ;;`;;;;;;;';;,;;   ;;, 
 `[[     [[ ''  ,[['[[cccc   ,[[ '[[,   [[    ,[[[,,,[[[ 
  $$,    $$ .c$$P'  $$""""  c$$$cc$$$c  $$    "$$$""$$$ 
 888_,o8P'd88 _,oo,888oo,__  888   888,  88,    888   "88o
  MMMMP"`  MMMUP*"^^""""YUMMMYMM   ""`  MMM    MMM    YMM 

   ┌─────────────────────────────────────────┐
   │         SÉLECTIONNER UNE CATÉGORIE          │
   └─────────────────────────────────────────┘

   ┌─[ 1 ]  ▸ RECONNAISSANCE
   └─────────────────────────────────────────────╜
   ┌─[ 2 ]  ▸ RÉSEAU
   └─────────────────────────────────────────────╜
   ┌─[ 3 ]  ▸ CRYPTOGRAPHIE
   └─────────────────────────────────────────────╜
   ┌─[ 4 ]  ▸ SYSTÈME
   └─────────────────────────────────────────────╜
   ┌─[ 5 ]  ▸ EXPLOITATION
   └─────────────────────────────────────────────╜
   ┌─[ 6 ]  ▸ AUDIT
   └─────────────────────────────────────────────╜

   ┌─[ q ]  Quitter
   └────────────────────╜
```

---

## 📂 Structure

```
d2ath/
├── d2ath.py      # Script principal
├── colors.py     # Module de couleurs (optionnel)
├── README.md     # Ce fichier
├── LICENSE       # Licence MIT
└── .github/
    └── workflows/
        └── lint.yml  # GitHub Actions
```

---

## 📌 Prérequis

- **Python 3.8+**
- **Système d'exploitation** : Linux (optimisé pour Kali, Ubuntu, Debian, Arch)
- **Permissions** : root/sudo requis pour certains outils (netdiscover, aircrack-ng, nmap)

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
- ❌ Tout autre usage非éthique ou非légal

**L'auteur ne peut être tenu responsable de toute utilisation 非appropriée.**

---

## 📄 Licence

Ce projet est sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

<p align="center">
  <b>Fait avec ❤️ par <a href="https://github.com/s1d9e">s1d9e</a></b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.0.0-blue?style=flat-square" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=flat-square" alt="Python">
</p>
