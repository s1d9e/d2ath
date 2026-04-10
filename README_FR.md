# d2ath - Framework de Sécurité

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="License">
  <img src="https://img.shields.io/github/stars/s1d9e/d2ath?style=flat-square" alt="Stars">
  <img src="https://img.shields.io/github/forks/s1d9e/d2ath?style=flat-square" alt="Forks">
</p>

<p align="center">
  <b>Framework de sécurité offensive et défensive tout-en-un pour Linux.</b>
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

### Dépendances

```bash
# Ubuntu / Debian
sudo apt update && sudo apt install python3 python3-pip whois curl nmap masscan netdiscover wireshark tshark tcpdump nikto hydra john sqlmap

# Arch Linux
sudo pacman -S python python-pip whois nmap masscan netdiscover wireshark-cli tcpdump nikto hydra john sqlmap
```

---

## ⚠️ Avertissement légal

**Usage autorisé :**
- ✅ Tests de pénétration autorisés
- ✅ Sécurité informatique éducative
- ✅ Usage personnel sur vos propres systèmes

**Usage interdit :**
- ❌ Accès non autorisé à des systèmes
- ❌ Activités illégales ou malveillantes

---

## 📄 Licence

Ce projet est sous licence **MIT**. Voir [LICENSE](LICENSE).

---

<p align="center">
  Créé avec ❤️ par <a href="https://github.com/s1d9e">s1d9e</a>
</p>