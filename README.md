# CTF-Assistant

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20Mac-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)
![CTF](https://img.shields.io/badge/CTF-Beginner%20Friendly-red)

> A toolkit to help beginners solve basic CTF (Capture The Flag) challenges automatically.

## 🎯 What is CTF?

CTF (Capture The Flag) is a cybersecurity competition where participants solve challenges to find "flags" (hidden strings). This tool helps beginners understand common challenge types.

## 🎓 Learning Objectives

By using this tool, beginners can learn:

- How to decode common encodings (Base64, Hex, ROT13, Caesar)
- Basic cryptography concepts
- File forensics and analysis
- Hash cracking fundamentals
- Web parameter testing
- Pattern recognition in CTF challenges

## ✨ Features

| Category | Tools Included |
|----------|----------------|
| **🔐 Cryptography** | Base64, Base32, Hex, ROT13, Caesar Cipher, Atbash, Morse Code |
| **🔑 Hash Cracking** | MD5, SHA1, SHA256, Simple hash lookup |
| **🖼️ Steganography** | Hidden text extraction, LSB analysis (basic) |
| **📁 Forensics** | File type detection, Magic bytes analyzer, String extractor |
| **🌐 Web** | Parameter fuzzing, SQL injection test (basic) |
| **🔧 Binary** | Pattern generator (cyclic), Offset finder |
| **📝 Encoding** | URL encode/decode, HTML entities, Unicode escape |

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Core Logic | Python 3 |
| Hash Cracking | hashlib, Rainbow tables (offline) |
| Encoding | base64, codecs, binascii |
| File Analysis | python-magic, binwalk |
| Network | requests, socket |
| CLI Interface | argparse, colorama |

