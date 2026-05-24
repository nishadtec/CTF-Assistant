import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font
import base64
import binascii
import hashlib
import json
import re
import urllib.parse
import html
from collections import Counter
from datetime import datetime
import threading


def b64_decode(data):
    try:
        return base64.b64decode(data).decode('utf-8', errors='ignore')
    except:
        return None

def b64_encode(data):
    return base64.b64encode(data.encode()).decode()

def hex_decode(data):
    try:
        data = re.sub(r'\s|0x|,', '', data)
        return bytes.fromhex(data).decode('utf-8', errors='ignore')
    except:
        return None

def hex_to_bytes(data):
    try:
        data = re.sub(r'\s|0x|,', '', data)
        return bytes.fromhex(data)
    except:
        return None

def hex_encode(data):
    return ' '.join([hex(ord(c))[2:].zfill(2) for c in data])

def binary_decode(data):
    try:
        data = re.sub(r'\s', '', data)
        chars = [data[i:i+8] for i in range(0, len(data), 8)]
        return ''.join([chr(int(c, 2)) for c in chars])
    except:
        return None

def binary_encode(data):
    return ' '.join([bin(ord(c))[2:].zfill(8) for c in data])

def rot13(data):
    result = []
    for c in data:
        if 'a' <= c <= 'z':
            result.append(chr((ord(c) - ord('a') + 13) % 26 + ord('a')))
        elif 'A' <= c <= 'Z':
            result.append(chr((ord(c) - ord('A') + 13) % 26 + ord('A')))
        else:
            result.append(c)
    return ''.join(result)

def rot_n(data, n):
    result = []
    for c in data:
        if 'a' <= c <= 'z':
            result.append(chr((ord(c) - ord('a') + n) % 26 + ord('a')))
        elif 'A' <= c <= 'Z':
            result.append(chr((ord(c) - ord('A') + n) % 26 + ord('A')))
        else:
            result.append(c)
    return ''.join(result)

def atbash(data):
    result = []
    for c in data:
        if 'a' <= c <= 'z':
            result.append(chr(ord('z') - (ord(c) - ord('a'))))
        elif 'A' <= c <= 'Z':
            result.append(chr(ord('Z') - (ord(c) - ord('A'))))
        else:
            result.append(c)
    return ''.join(result)

def morse_decode(data):
    morse_dict = {
        '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F', '--.': 'G',
        '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N',
        '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
        '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y', '--..': 'Z',
        '-----': '0', '.----': '1', '..---': '2', '...--': '3', '....-': '4',
        '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9',
        '.-.-.-': '.', '--..--': ',', '..--..': '?', '-.-.--': '!', '-..-.': '/',
        '-.--.': '(', '-.--.-': ')', '/': ' '
    }
    try:
        words = data.split(' / ')
        result = []
        for word in words:
            chars = word.split()
            result.append(''.join([morse_dict.get(c, '?') for c in chars]))
        return ' '.join(result)
    except:
        return None

def morse_encode(data):
    morse_dict = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.',
        'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.',
        'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
        'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
        '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
        '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
        '.': '.-.-.-', ',': '--..--', '?': '..--..', '!': '-.-.--', '/': '-..-.',
        '(': '-.--.', ')': '-.--.-', ' ': '/'
    }
    return ' '.join([morse_dict.get(c.upper(), '?') for c in data])

def url_decode(data):
    try:
        return urllib.parse.unquote(data)
    except:
        return None

def url_encode(data):
    return urllib.parse.quote(data)

def html_decode(data):
    return html.unescape(data)

def base32_decode(data):
    try:
        return base64.b32decode(data.upper()).decode('utf-8', errors='ignore')
    except:
        return None

def vigenere_decode(data, key):
    if not key:
        return None
    result = []
    key = key.upper()
    key_len = len(key)
    for i, c in enumerate(data):
        if 'a' <= c <= 'z':
            shift = ord(key[i % key_len]) - ord('A')
            result.append(chr((ord(c) - ord('a') - shift) % 26 + ord('a')))
        elif 'A' <= c <= 'Z':
            shift = ord(key[i % key_len]) - ord('A')
            result.append(chr((ord(c) - ord('A') - shift) % 26 + ord('A')))
        else:
            result.append(c)
    return ''.join(result)

def xor_brute(data):
    results = []
    for key in range(1, 256):
        result = ''.join([chr(ord(c) ^ key) for c in data])
        if re.search(r'[a-zA-Z0-9\s]{10,}', result):
            results.append((key, result[:100]))
    return results[:10]

def xor_bytes(data1, data2):
    """XOR two byte strings"""
    min_len = min(len(data1), len(data2))
    return bytes([data1[i] ^ data2[i] for i in range(min_len)])

def freq_analysis(data):
    clean = re.sub(r'[^a-zA-Z]', '', data).lower()
    freq = Counter(clean)
    return freq.most_common(10)

def entropy_calc(data):
    freq = Counter(data)
    n = len(data)
    if n == 0:
        return 0
    entropy = -sum((count/n) * (count/n).bit_length() if count else 0 for count in freq.values())
    return round(entropy, 3)

def extract_strings(data):
    return re.findall(r'[ -~]{4,}', data)

def find_flag(data, flag_format="CTF{"):
    pattern = re.escape(flag_format) + r'[^}]+}'
    return re.findall(pattern, data, re.IGNORECASE)

def num_to_char(data):
    nums = re.findall(r'\d+', data)
    result = []
    for n in nums[:50]:
        try:
            code = int(n)
            if 32 <= code <= 126:
                result.append(chr(code))
            else:
                result.append(f'[{n}]')
        except:
            result.append('?')
    return ''.join(result)

def jwt_decode(token):
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
        payload = base64.b64decode(parts[1] + '=' * (4 - len(parts[1]) % 4))
        return json.loads(payload)
    except:
        return None

def hash_identify(hash_string):
    hash_string = hash_string.strip().lower()
    results = []
    
    if re.match(r'^[a-f0-9]{32}$', hash_string):
        results.append(('MD5', 'high'))
    if re.match(r'^[a-f0-9]{40}$', hash_string):
        results.append(('SHA-1', 'high'))
    if re.match(r'^[a-f0-9]{64}$', hash_string):
        results.append(('SHA-256', 'high'))
    if re.match(r'^[a-f0-9]{128}$', hash_string):
        results.append(('SHA-512', 'high'))
    if hash_string.startswith('$2') and '$' in hash_string:
        results.append(('bcrypt', 'high'))
    if hash_string.startswith('$1$'):
        results.append(('MD5crypt', 'high'))
    if hash_string.startswith('$6$'):
        results.append(('SHA-512crypt', 'high'))
    if re.match(r'^[a-f0-9]{8}$', hash_string):
        results.append(('CRC32', 'medium'))
    
    if not results:
        results.append(('Unknown Format', 'low'))
    
    return results

def generate_hash(text, algo):
    text_bytes = text.encode()
    if algo == 'md5':
        return hashlib.md5(text_bytes).hexdigest()
    elif algo == 'sha1':
        return hashlib.sha1(text_bytes).hexdigest()
    elif algo == 'sha256':
        return hashlib.sha256(text_bytes).hexdigest()
    elif algo == 'sha512':
        return hashlib.sha512(text_bytes).hexdigest()
    return None

class AutoCTFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoCTF - Professional Hacking Toolkit")
        self.root.geometry("1400x900")
        self.root.configure(bg='#0a0e1a')
        
        self.title_font = font.Font(family='Courier', size=12, weight='bold')
        self.mono_font = font.Font(family='Courier', size=10)
        
        self.current_data = ""
        self.flag_format = "CTF{"
        self.history = []
        
        self.library = self.load_library()
        
        self.setup_ui()
        
        self.apply_styling()
    
    def load_library(self):
        try:
            with open('ctf_library.json', 'r') as f:
                return json.load(f)
        except:
            return []
    
    def save_library(self):
        with open('ctf_library.json', 'w') as f:
            json.dump(self.library[-100:], f, indent=2)
    
    def apply_styling(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        bg_dark = '#0a0e1a'
        bg_medium = '#111520'
        bg_light = '#1a1f2e'
        fg_green = '#00ff88'
        fg_text = '#e0e0e0'
        
        style.configure('TNotebook', background=bg_dark, borderwidth=0)
        style.configure('TNotebook.Tab', background=bg_medium, foreground=fg_text, padding=[20, 8])
        style.map('TNotebook.Tab', background=[('selected', bg_light)], foreground=[('selected', fg_green)])
        
        style.configure('TFrame', background=bg_dark)
        style.configure('TLabel', background=bg_dark, foreground=fg_text)
        style.configure('TLabelframe', background=bg_dark, foreground=fg_text)
        style.configure('TLabelframe.Label', background=bg_dark, foreground=fg_green)
        
        style.configure('TButton', background=bg_medium, foreground=fg_text, borderwidth=1, padding=8)
        style.map('TButton', background=[('active', bg_light)], foreground=[('active', fg_green)])
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(header_frame, text="⚡ AutoCTF - Advanced CTF Toolkit", 
                                font=self.title_font, foreground='#00ff88')
        title_label.pack(side=tk.LEFT)
        
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.create_solver_tab()
        self.create_tools_tab()
        self.create_twotime_tab()
        self.create_hash_tab()
        self.create_bruteforce_tab()
        self.create_library_tab()
        self.create_about_tab()
    
    def create_solver_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔍 Solver")
        
        left_frame = ttk.Frame(tab)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        input_label = ttk.Label(left_frame, text="CHALLENGE INPUT / CIPHERTEXT", font=self.title_font)
        input_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.input_text = scrolledtext.ScrolledText(left_frame, height=15, font=self.mono_font,
                                                     bg='#111520', fg='#e0e0e0', insertbackground='#00ff88',
                                                     relief=tk.FLAT, borderwidth=1, highlightthickness=1,
                                                     highlightcolor='#00ff88', highlightbackground='#2a2e3f')
        self.input_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        format_frame = ttk.Frame(left_frame)
        format_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(format_frame, text="Flag Format:").pack(side=tk.LEFT)
        self.flag_format_entry = ttk.Entry(format_frame, width=20)
        self.flag_format_entry.insert(0, "CTF{")
        self.flag_format_entry.pack(side=tk.LEFT, padx=(10, 0))
        ttk.Button(format_frame, text="Set", command=self.update_flag_format).pack(side=tk.LEFT, padx=(5, 0))
        
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="▶ AUTO SOLVE", command=self.auto_solve_thread).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="🔄 DECODE", command=self.decode_current).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🗑 CLEAR", command=self.clear_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="📋 COPY", command=self.copy_output).pack(side=tk.LEFT, padx=5)
        
        right_frame = ttk.Frame(tab)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        output_label = ttk.Label(right_frame, text="OUTPUT / DECODED RESULT", font=self.title_font)
        output_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.output_text = scrolledtext.ScrolledText(right_frame, height=15, font=self.mono_font,
                                                      bg='#0a0e1a', fg='#00ff88', insertbackground='#00ff88',
                                                      relief=tk.FLAT, borderwidth=1, highlightthickness=1,
                                                      highlightcolor='#00ff88', highlightbackground='#2a2e3f')
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        self.progress = ttk.Progressbar(right_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(5, 0))
    
    def create_tools_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🛠 Tools")
        
        ttk.Label(tab, text="Input Data:", font=self.title_font).pack(anchor=tk.W, pady=(0, 5))
        self.tool_input = scrolledtext.ScrolledText(tab, height=6, font=self.mono_font,
                                                     bg='#111520', fg='#e0e0e0')
        self.tool_input.pack(fill=tk.X, pady=(0, 10))
        
        tools_frame = ttk.Frame(tab)
        tools_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        tools = [
            ("Base64 Decode", "b64d"), ("Base64 Encode", "b64e"),
            ("Hex Decode", "hexd"), ("Hex Encode", "hexe"),
            ("Binary Decode", "bind"), ("Binary Encode", "bine"),
            ("ROT13", "rot13"), ("Atbash", "atbash"),
            ("Reverse", "rev"), ("URL Decode", "url"),
            ("Morse Decode", "morse"), ("Morse Encode", "morsee"),
            ("HTML Decode", "html"), ("Base32 Decode", "b32d"),
            ("Frequency Analysis", "freq"), ("Entropy", "entropy"),
            ("Extract Strings", "strings"), ("Find Flag", "flag"),
            ("Numbers to Char", "num2char"), ("JWT Decode", "jwt")
        ]
        
        row = 0
        col = 0
        for name, cmd in tools:
            btn = ttk.Button(tools_frame, text=name, command=lambda c=cmd: self.run_tool(c),
                             width=18)
            btn.grid(row=row, column=col, padx=2, pady=2, sticky='w')
            col += 1
            if col >= 4:
                col = 0
                row += 1
        
        vigenere_frame = ttk.Frame(tab)
        vigenere_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Label(vigenere_frame, text="Vigenere Key:").pack(side=tk.LEFT)
        self.vig_key = ttk.Entry(vigenere_frame, width=20)
        self.vig_key.pack(side=tk.LEFT, padx=(5, 10))
        ttk.Button(vigenere_frame, text="Vigenere Decode", 
                   command=lambda: self.run_tool('vigenere')).pack(side=tk.LEFT)
        
        xor_frame = ttk.Frame(tab)
        xor_frame.pack(fill=tk.X, pady=(5, 0))
        ttk.Label(xor_frame, text="XOR Key (0-255):").pack(side=tk.LEFT)
        self.xor_key = ttk.Entry(xor_frame, width=10)
        self.xor_key.pack(side=tk.LEFT, padx=(5, 10))
        ttk.Button(xor_frame, text="XOR Decode", 
                   command=lambda: self.run_tool('xor_key')).pack(side=tk.LEFT)
        
        ttk.Label(tab, text="Tool Output:", font=self.title_font).pack(anchor=tk.W, pady=(10, 5))
        self.tool_output = scrolledtext.ScrolledText(tab, height=8, font=self.mono_font,
                                                      bg='#0a0e1a', fg='#00ff88')
        self.tool_output.pack(fill=tk.BOTH, expand=True)
    
    def create_twotime_tab(self):
        """Two-Time Pad Attack Tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔐 Two-Time Pad Attack")
        
        info_frame = ttk.Frame(tab)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        info_text = """Two-Time Pad Attack - When same key is reused for two messages:
        C1 = P1 ⊕ Key, C2 = P2 ⊕ Key → C1 ⊕ C2 = P1 ⊕ P2"""
        ttk.Label(info_frame, text=info_text, font=self.mono_font, foreground='#00d4ff').pack()
        
        c1_frame = ttk.LabelFrame(tab, text="Ciphertext 1 (Hex)", padding="10")
        c1_frame.pack(fill=tk.X, pady=(0, 10))
        self.c1_input = scrolledtext.ScrolledText(c1_frame, height=3, font=self.mono_font,
                                                   bg='#111520', fg='#e0e0e0')
        self.c1_input.pack(fill=tk.X)
        
        c2_frame = ttk.LabelFrame(tab, text="Ciphertext 2 (Hex)", padding="10")
        c2_frame.pack(fill=tk.X, pady=(0, 10))
        self.c2_input = scrolledtext.ScrolledText(c2_frame, height=3, font=self.mono_font,
                                                   bg='#111520', fg='#e0e0e0')
        self.c2_input.pack(fill=tk.X)
        
        options_frame = ttk.Frame(tab)
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(options_frame, text="Common Words (comma separated):").pack(side=tk.LEFT)
        self.common_words_entry = ttk.Entry(options_frame, width=50)
        self.common_words_entry.insert(0, "CTF{,flag,the ,and ,this ,is ,secret,message")
        self.common_words_entry.pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Button(tab, text="🚀 START ATTACK", command=self.twotime_attack).pack(pady=(0, 10))
        
        results_frame = ttk.LabelFrame(tab, text="Attack Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.twotime_output = scrolledtext.ScrolledText(results_frame, height=20, font=self.mono_font,
                                                         bg='#0a0e1a', fg='#00ff88')
        self.twotime_output.pack(fill=tk.BOTH, expand=True)
        
        self.twotime_progress = ttk.Progressbar(tab, mode='indeterminate')
        self.twotime_progress.pack(fill=tk.X, pady=(5, 0))
    
    def create_hash_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔑 Hash Tools")
        
        id_frame = ttk.LabelFrame(tab, text="Hash Identifier", padding="10")
        id_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(id_frame, text="Enter Hash:").pack(anchor=tk.W)
        self.hash_input = ttk.Entry(id_frame, font=self.mono_font)
        self.hash_input.pack(fill=tk.X, pady=(5, 5))
        self.hash_input.bind('<KeyRelease>', lambda e: self.identify_hash())
        
        self.hash_result = tk.Text(id_frame, height=4, bg='#111520', fg='#00ff88', font=self.mono_font)
        self.hash_result.pack(fill=tk.X, pady=(5, 0))
        
        gen_frame = ttk.LabelFrame(tab, text="Hash Generator", padding="10")
        gen_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(gen_frame, text="Text to Hash:").pack(anchor=tk.W)
        self.hash_gen_input = ttk.Entry(gen_frame, font=self.mono_font)
        self.hash_gen_input.pack(fill=tk.X, pady=(5, 5))
        
        hash_btn_frame = ttk.Frame(gen_frame)
        hash_btn_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(hash_btn_frame, text="MD5", command=lambda: self.generate_hash('md5')).pack(side=tk.LEFT, padx=2)
        ttk.Button(hash_btn_frame, text="SHA1", command=lambda: self.generate_hash('sha1')).pack(side=tk.LEFT, padx=2)
        ttk.Button(hash_btn_frame, text="SHA256", command=lambda: self.generate_hash('sha256')).pack(side=tk.LEFT, padx=2)
        ttk.Button(hash_btn_frame, text="SHA512", command=lambda: self.generate_hash('sha512')).pack(side=tk.LEFT, padx=2)
        
        self.hash_output = tk.Text(gen_frame, height=2, bg='#0a0e1a', fg='#00d4ff', font=self.mono_font)
        self.hash_output.pack(fill=tk.X, pady=(5, 0))
    
    def create_bruteforce_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="💥 Bruteforce")
        
        ttk.Label(tab, text="Target Text:", font=self.title_font).pack(anchor=tk.W, pady=(0, 5))
        self.bf_input = scrolledtext.ScrolledText(tab, height=8, font=self.mono_font, bg='#111520', fg='#e0e0e0')
        self.bf_input.pack(fill=tk.X, pady=(0, 10))
        
        options_frame = ttk.Frame(tab)
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.rot_var = tk.BooleanVar(value=True)
        self.xor_var = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(options_frame, text="ROT Brute (1-25)", variable=self.rot_var).pack(side=tk.LEFT, padx=10)
        ttk.Checkbutton(options_frame, text="XOR Brute (1-255)", variable=self.xor_var).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(tab, text="🚀 START BRUTEFORCE", command=self.bruteforce).pack(pady=(0, 10))
        
        ttk.Label(tab, text="Results:", font=self.title_font).pack(anchor=tk.W)
        self.bf_output = scrolledtext.ScrolledText(tab, height=12, font=self.mono_font, bg='#0a0e1a', fg='#00ff88')
        self.bf_output.pack(fill=tk.BOTH, expand=True)
    
    def create_library_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📚 Library")
        
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_library).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Clear Library", command=self.clear_library).pack(side=tk.LEFT, padx=2)
        
        self.lib_listbox = tk.Listbox(tab, bg='#111520', fg='#e0e0e0', font=self.mono_font, height=15)
        self.lib_listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.lib_listbox.bind('<<ListboxSelect>>', self.show_library_item)
        
        ttk.Label(tab, text="Details:", font=self.title_font).pack(anchor=tk.W)
        self.lib_detail = scrolledtext.ScrolledText(tab, height=8, font=self.mono_font, bg='#0a0e1a', fg='#00d4ff')
        self.lib_detail.pack(fill=tk.BOTH, expand=True)
        
        self.refresh_library()
    
    def create_about_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="ℹ About")
        
        about_text = """╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║                    ⚡ AutoCTF v3.0 ⚡                      ║
║                                                           ║
║         Professional CTF (Capture The Flag) Toolkit       ║
║                                                           ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Features:                                                ║
║  • Multi-format Encoding/Decoding (Base64, Hex, Binary)   ║
║  • Classical Ciphers (ROT13, Atbash, Vigenere, Morse)     ║
║  • XOR & ROT Bruteforce Attacks                           ║
║  • TWO-TIME PAD ATTACK                                     ║
║  • Hash Identification & Generation (MD5, SHA1, SHA256)   ║
║  • Frequency Analysis & Entropy Calculator                ║
║  • JWT Decoder & String Extractors                        ║
║  • Built-in Library to Save Challenges                    ║
║                                                           ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Created with ❤ for CTF Players                          ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝"""
        
        about_label = ttk.Label(tab, text=about_text, font=self.mono_font, justify=tk.LEFT)
        about_label.pack(padx=20, pady=20)
    
    def update_flag_format(self):
        self.flag_format = self.flag_format_entry.get()
        self.append_output(f"[+] Flag format set to: {self.flag_format}")
    
    def append_output(self, text, color='#00ff88'):
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)
    
    def clear_all(self):
        self.input_text.delete(1.0, tk.END)
        self.output_text.delete(1.0, tk.END)
        self.current_data = ""
    
    def copy_output(self):
        content = self.output_text.get(1.0, tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        self.append_output("[+] Copied to clipboard!")
    
    def decode_current(self):
        data = self.input_text.get(1.0, tk.END).strip()
        if not data:
            self.append_output("[-] No input provided!", '#ff4444')
            return
        
        self.current_data = data
        
        self.append_output("\n[+] Attempting automatic decoding...")
        
        decoders = [
            ('Base64', b64_decode), ('Hex', hex_decode), ('Binary', binary_decode),
            ('Base32', base32_decode), ('ROT13', rot13), ('Atbash', atbash),
            ('Reverse', lambda x: x[::-1]), ('URL', url_decode), ('HTML', html_decode)
        ]
        
        for name, decoder in decoders:
            try:
                result = decoder(data)
                if result and result != data and len(result) > 2:
                    self.append_output(f"\n[{name}] {result[:200]}")
            except:
                pass
    
    def auto_solve_thread(self):
        thread = threading.Thread(target=self.auto_solve)
        thread.daemon = True
        thread.start()
    
    def auto_solve(self):
        data = self.input_text.get(1.0, tk.END).strip()
        if not data:
            self.append_output("[-] No input provided!", '#ff4444')
            return
        
        self.current_data = data
        self.progress.start()
        self.append_output("\n" + "="*50)
        self.append_output("[*] Starting Auto-Solver...")
        
        decoders = [
            ('Base64', b64_decode), ('Hex', hex_decode), ('Binary', binary_decode),
            ('Base32', base32_decode), ('ROT13', rot13), ('Atbash', atbash),
            ('Reverse', lambda x: x[::-1]), ('URL', url_decode), ('HTML', html_decode),
            ('Morse', morse_decode)
        ]
        
        found = False
        for name, decoder in decoders:
            try:
                result = decoder(data)
                if result and result != data and len(result) > 3:
                    self.append_output(f"\n[+] {name}: {result[:150]}")
                    if self.flag_format in result or 'flag' in result.lower():
                        self.append_output(f"[!!!] ⚑ FLAG FOUND via {name}: {result}", '#00ff88')
                        found = True
                        self.save_to_library('solved', data, result)
            except:
                pass
        
        self.append_output("\n[*] ROT Bruteforce (1-25):")
        for i in range(1, 26):
            result = rot_n(data, i)
            if self.flag_format in result or 'flag' in result.lower():
                self.append_output(f"[!!!] ⚑ FLAG FOUND via ROT{i}: {result}", '#00ff88')
                found = True
            elif i <= 3 or i >= 23:
                self.append_output(f"    ROT{i:2d}: {result[:80]}")
        
        self.append_output("\n[*] XOR Bruteforce (1-255):")
        xor_results = xor_brute(data)
        for key, result in xor_results[:5]:
            if self.flag_format in result or 'flag' in result.lower():
                self.append_output(f"[!!!] ⚑ FLAG FOUND via XOR key {key}: {result}", '#00ff88')
                found = True
            else:
                self.append_output(f"    XOR Key 0x{key:02x}: {result[:80]}")
        
        if not found:
            self.append_output("\n[-] No flag found. Try manual analysis.", '#ffaa00')
        
        self.progress.stop()
        self.append_output("\n" + "="*50)
    
    def run_tool(self, tool):
        data = self.tool_input.get(1.0, tk.END).strip()
        if not data:
            self.tool_output.insert(tk.END, "[-] No input provided!\n")
            return
        
        self.tool_output.delete(1.0, tk.END)
        
        if tool == 'b64d':
            result = b64_decode(data)
        elif tool == 'b64e':
            result = b64_encode(data)
        elif tool == 'hexd':
            result = hex_decode(data)
        elif tool == 'hexe':
            result = hex_encode(data)
        elif tool == 'bind':
            result = binary_decode(data)
        elif tool == 'bine':
            result = binary_encode(data)
        elif tool == 'rot13':
            result = rot13(data)
        elif tool == 'atbash':
            result = atbash(data)
        elif tool == 'rev':
            result = data[::-1]
        elif tool == 'url':
            result = url_decode(data)
        elif tool == 'morse':
            result = morse_decode(data)
        elif tool == 'morsee':
            result = morse_encode(data)
        elif tool == 'html':
            result = html_decode(data)
        elif tool == 'b32d':
            result = base32_decode(data)
        elif tool == 'freq':
            result = freq_analysis(data)
            self.tool_output.insert(tk.END, "Frequency Analysis:\n")
            for char, count in result:
                self.tool_output.insert(tk.END, f"  '{char}': {count}\n")
            return
        elif tool == 'entropy':
            result = f"Entropy: {entropy_calc(data)} bits/char"
        elif tool == 'strings':
            result = extract_strings(data)
            self.tool_output.insert(tk.END, "Extracted Strings:\n")
            for s in result[:20]:
                self.tool_output.insert(tk.END, f"  {s}\n")
            return
        elif tool == 'flag':
            result = find_flag(data, self.flag_format)
            self.tool_output.insert(tk.END, "Flags Found:\n")
            for f in result:
                self.tool_output.insert(tk.END, f"  ⚑ {f}\n")
            return
        elif tool == 'num2char':
            result = num_to_char(data)
        elif tool == 'jwt':
            result = jwt_decode(data)
            if result:
                result = json.dumps(result, indent=2)
        elif tool == 'vigenere':
            key = self.vig_key.get()
            result = vigenere_decode(data, key)
        elif tool == 'xor_key':
            try:
                key = int(self.xor_key.get())
                result = ''.join([chr(ord(c) ^ key) for c in data])
            except:
                result = "Invalid key"
        else:
            result = "Unknown tool"
        
        if result:
            self.tool_output.insert(tk.END, str(result))
        else:
            self.tool_output.insert(tk.END, "[-] Decoding failed")
    
    def twotime_attack(self):
        """Perform two-time pad attack - FIXED VERSION"""
        try:
            c1 = self.c1_input.get(1.0, tk.END).strip()
            c2 = self.c2_input.get(1.0, tk.END).strip()
            
            if not c1 or not c2:
                self.twotime_output.insert(tk.END, "[-] Please enter both ciphertexts!\n")
                return
            
            self.twotime_output.delete(1.0, tk.END)
            self.twotime_output.insert(tk.END, "="*70 + "\n")
            self.twotime_output.insert(tk.END, "🔐 TWO-TIME PAD ATTACK IN PROGRESS...\n")
            self.twotime_output.insert(tk.END, "="*70 + "\n\n")
            self.twotime_output.update()
            
            self.twotime_progress.start()
            
            common_words_str = self.common_words_entry.get().strip()
            common_words = [w.encode() for w in common_words_str.split(',') if w.strip()]
            
            def hex_to_bytes(hex_str):
                try:
                    hex_str = re.sub(r'\s|0x|,', '', hex_str)
                    return bytes.fromhex(hex_str)
                except:
                    return None
            
            c1_bytes = hex_to_bytes(c1)
            c2_bytes = hex_to_bytes(c2)
            
            if c1_bytes is None or c2_bytes is None:
                self.twotime_output.insert(tk.END, "[-] Invalid hex strings!\n")
                self.twotime_progress.stop()
                return
            
            min_len = min(len(c1_bytes), len(c2_bytes))
            xor_result = bytes([c1_bytes[i] ^ c2_bytes[i] for i in range(min_len)])
            
            self.twotime_output.insert(tk.END, "📊 STEP 1: XOR OF CIPHERTEXTS (P1 ⊕ P2)\n")
            self.twotime_output.insert(tk.END, "-"*70 + "\n")
            self.twotime_output.insert(tk.END, f"Hex: {xor_result.hex()}\n")
            self.twotime_output.insert(tk.END, f"Length: {len(xor_result)} bytes\n\n")
            self.twotime_output.update()
            
            self.twotime_output.insert(tk.END, "🏁 STEP 2: LOOKING FOR CTF{ PATTERN\n")
            self.twotime_output.insert(tk.END, "-"*70 + "\n")
            
            flag_pattern = b"CTF{"
            found_any = False
            
            for pos in range(len(xor_result) - len(flag_pattern) + 1):
                p2_candidate = bytes([xor_result[pos + i] ^ flag_pattern[i] for i in range(len(flag_pattern))])
                if all(32 <= b <= 126 or b == 9 or b == 10 for b in p2_candidate):
                    self.twotime_output.insert(tk.END, 
                        f"  Position {pos}: CTF{{...}} in P1 → '{p2_candidate.decode(errors='replace')}' in P2\n")
                    found_any = True
                    self.twotime_output.update()
            
            if not found_any:
                self.twotime_output.insert(tk.END, "  No CTF{ pattern found.\n")
            
            self.twotime_output.insert(tk.END, "\n🔍 STEP 3: TRYING COMMON WORDS\n")
            self.twotime_output.insert(tk.END, "-"*70 + "\n")
            
            found_word = False
            for word in common_words:
                for pos in range(len(xor_result) - len(word) + 1):
                    # Guess in P1
                    p2_candidate = bytes([xor_result[pos + i] ^ word[i] for i in range(len(word))])
                    if all(32 <= b <= 126 for b in p2_candidate):
                        self.twotime_output.insert(tk.END,
                            f"  '{word.decode()}' at pos {pos} (in P1) → P2: '{p2_candidate.decode(errors='replace')}'\n")
                        found_word = True
                        self.twotime_output.update()
                    
                    p1_candidate = bytes([xor_result[pos + i] ^ word[i] for i in range(len(word))])
                    if all(32 <= b <= 126 for b in p1_candidate):
                        self.twotime_output.insert(tk.END,
                            f"  '{word.decode()}' at pos {pos} (in P2) → P1: '{p1_candidate.decode(errors='replace')}'\n")
                        found_word = True
                        self.twotime_output.update()
            
            if not found_word:
                self.twotime_output.insert(tk.END, "  No readable words found.\n")
            
            self.twotime_output.insert(tk.END, "\n📝 STEP 4: XOR RESULT AS CHARACTERS\n")
            self.twotime_output.insert(tk.END, "-"*70 + "\n")
            
            line = ""
            for i, b in enumerate(xor_result):
                if 32 <= b <= 126:
                    line += chr(b)
                else:
                    line += "."
                if len(line) >= 32:
                    self.twotime_output.insert(tk.END, f"{line}\n")
                    line = ""
            if line:
                self.twotime_output.insert(tk.END, f"{line}\n")
            
            self.twotime_output.insert(tk.END, "\n" + "="*70 + "\n")
            self.twotime_output.insert(tk.END, "✅ Attack completed!\n")
            self.twotime_output.update()
            
        except Exception as e:
            self.twotime_output.insert(tk.END, f"\n[-] Error: {str(e)}\n")
            import traceback
            self.twotime_output.insert(tk.END, traceback.format_exc())
        finally:
            self.twotime_progress.stop()
    
    def bruteforce(self):
        data = self.bf_input.get(1.0, tk.END).strip()
        if not data:
            self.bf_output.insert(tk.END, "[-] No input provided!\n")
            return
        
        self.bf_output.delete(1.0, tk.END)
        self.bf_output.insert(tk.END, "="*60 + "\n")
        self.bf_output.insert(tk.END, "[*] Bruteforce Attack Started\n")
        self.bf_output.insert(tk.END, "="*60 + "\n\n")
        
        if self.rot_var.get():
            self.bf_output.insert(tk.END, "--- ROT Bruteforce (1-25) ---\n")
            for i in range(1, 26):
                result = rot_n(data, i)
                if self.flag_format in result or 'flag' in result.lower():
                    self.bf_output.insert(tk.END, f"[!!!] FLAG! ROT{i}: {result}\n")
                else:
                    self.bf_output.insert(tk.END, f"ROT{i:2d}: {result[:80]}\n")
            self.bf_output.insert(tk.END, "\n")
        
        if self.xor_var.get():
            self.bf_output.insert(tk.END, "--- XOR Bruteforce (1-255) ---\n")
            results = xor_brute(data)
            for key, result in results:
                if self.flag_format in result or 'flag' in result.lower():
                    self.bf_output.insert(tk.END, f"[!!!] FLAG! XOR Key {key}: {result}\n")
                else:
                    self.bf_output.insert(tk.END, f"XOR 0x{key:02x}: {result}\n")
        
        self.bf_output.insert(tk.END, "\n[*] Bruteforce Complete\n")
    
    def identify_hash(self):
        hash_val = self.hash_input.get().strip()
        if not hash_val:
            return
        
        results = hash_identify(hash_val)
        self.hash_result.delete(1.0, tk.END)
        for name, confidence in results:
            self.hash_result.insert(tk.END, f"[{confidence.upper()}] {name}\n")
    
    def generate_hash(self, algo):
        text = self.hash_gen_input.get().strip()
        if not text:
            return
        
        result = generate_hash(text, algo)
        if result:
            self.hash_output.delete(1.0, tk.END)
            self.hash_output.insert(tk.END, result)
    
    def save_to_library(self, typ, data, result=None):
        entry = {
            'type': typ,
            'timestamp': datetime.now().isoformat(),
            'data': data[:200],
            'result': result[:200] if result else None
        }
        self.library.append(entry)
        self.save_library()
    
    def refresh_library(self):
        self.lib_listbox.delete(0, tk.END)
        for i, entry in enumerate(self.library[-50:]):
            display = f"[{entry['type']}] {entry['timestamp'][:19]}"
            self.lib_listbox.insert(tk.END, display)
    
    def show_library_item(self, event):
        selection = self.lib_listbox.curselection()
        if selection:
            idx = selection[0]
            entry = self.library[-(len(self.library[-50:]) - idx)]
            self.lib_detail.delete(1.0, tk.END)
            self.lib_detail.insert(tk.END, f"Type: {entry['type']}\n")
            self.lib_detail.insert(tk.END, f"Time: {entry['timestamp']}\n")
            self.lib_detail.insert(tk.END, f"\nData:\n{entry['data']}\n")
            if entry.get('result'):
                self.lib_detail.insert(tk.END, f"\nResult:\n{entry['result']}\n")
    
    def clear_library(self):
        if messagebox.askyesno("Clear Library", "Delete all saved challenges?"):
            self.library = []
            self.save_library()
            self.refresh_library()
            self.lib_detail.delete(1.0, tk.END)


def main():
    root = tk.Tk()
    app = AutoCTFApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
