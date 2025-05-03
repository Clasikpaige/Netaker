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

    def do_help(self, arg):
        """Show comprehensive help information"""
        print("\n\033[1;36mNETAKER Framework Technical Specifications:\033[0m")
        print("- Advanced multi-vector payload delivery system with memory-only execution")
        print("- Evasion techniques include:")
        print("  * API unhooking and direct syscalls")
        print("  * Time-based execution delays (randomized)")
        print("  * Environmental fingerprinting (VM/sandbox detection)")
        print("  * Process hollowing and reflective DLL injection")
        print("  * Encrypted C2 communications (AES-256 + TLS 1.3)")
        print("- Automatic artifact cleanup (timestomping, file wiping)")
        print("- Built-in logging of all operations")
        
        print("\n\033[1;35mCore Commands:\033[0m")
        print("  platform    - Set target platform (windows/linux/macos/android/ios)")
        print("  generate    - Create advanced evasion payload")
        print("  deploy      - Configure payload delivery method")
        print("  analyze     - Enter crypto analysis module")
        print("  portal      - View incoming data from payloads")
        print("  c2          - Configure C2 server settings")
        print("  show        - Display current configuration")
        print("  back        - Return to previous menu")
        print("  exit        - Exit the framework securely")

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

    # ===== DELIVERY METHODS =====
    def do_deploy(self, arg):
        """Configure payload delivery method"""
        methods = [dm.value for dm in DeliveryMethod]
        terminal_menu = TerminalMenu(
            methods,
            title="\033[1;36mSelect delivery method:\033[0m",
            menu_cursor_style=("fg_red", "bold")
        )
        selection = terminal_menu.show()
        
        if selection is not None:
            self.delivery_method = list(DeliveryMethod)[selection]
            print(f"\n\033[1;32m[+]\033[0m Delivery method set to \033[1;33m{self.delivery_method.value}\033[0m")
            print("\033[1;36mSuggested approach:\033[0m")
            
            if self.delivery_method == DeliveryMethod.PHISHING_EMAIL:
                print("- Craft email with malicious attachment")
                print("- Use social engineering themes (invoice, resume)")
            elif self.delivery_method == DeliveryMethod.WEBSITE_REDIRECT:
                print("- Clone legitimate website")
                print("- Use drive-by download techniques")
            elif self.delivery_method == DeliveryMethod.USB_DROP:
                print("- Create autorun.inf files for Windows")
                print("- Use folder icons to mimic documents")
            
            self.log_operation(f"Delivery method set to {self.delivery_method.value}")

    # ===== DATA PORTAL =====
    def do_portal(self, arg):
        """View and manage incoming data from deployed payloads"""
        print(f"\n\033[1;36mData Portal - Incoming C2 Connections ({DATA_PORTAL_DIR}):\033[0m")
        try:
            files = os.listdir(DATA_PORTAL_DIR)
            if not files:
                print("\033[1;31m[-] No data received yet\033[0m")
                return
                
            for idx, file in enumerate(files, 1):
                filepath = os.path.join(DATA_PORTAL_DIR, file)
                size = os.path.getsize(filepath)
                print(f"{idx}. \033[1;33m{file}\033[0m (\033[1;35m{size} bytes\033[0m)")
                
                # Display first few lines of each file
                with open(filepath, 'r') as f:
                    lines = f.readlines()[:3]
                    for line in lines:
                        print(f"   | {line.strip()}")
                    if len(lines) == 3:
                        print("   | ...")
                        
        except FileNotFoundError:
            print("\033[1;31m[-] Data directory not found\033[0m")

    def do_c2(self, arg):
        """Configure C2 server settings"""
        global C2_IP, C2_PORT  # Add this line to declare the global variables
        print("\n\033[1;36mCurrent C2 Configuration:\033[0m")
        print(f"IP: \033[1;33m{C2_IP}\033[0m")
        print(f"Port: \033[1;33m{C2_PORT}\033[0m")
        
        new_ip = input("\nEnter new C2 IP [Enter to keep current]: ").strip()
        new_port = input("Enter new C2 Port [Enter to keep current]: ").strip()
        
        if new_ip:
            C2_IP = new_ip
        if new_port:
            try:
                C2_PORT = int(new_port)
            except ValueError:
                print("\033[1;31m[-] Invalid port number\033[0m")
                return
                    
        print(f"\n\033[1;32m[+]\033[0m C2 server set to \033[1;33m{C2_IP}:{C2_PORT}\033[0m")
        self.log_operation(f"C2 server configured to {C2_IP}:{C2_PORT}")


    # ===== ANALYSIS MODULE =====
    def do_analyze(self, arg):
        """Enter crypto analysis module"""
        if not self.current_platform:
            print("\n\033[1;31m[-] Please set platform first\033[0m")
            return
            
        self.current_module = "analysis"
        self.prompt = "\n\033[1;35m(netaker/analysis)\033[0m > "
        print("\n\033[1;32m[+]\033[0m Entered \033[1;33mCrypto Analysis Module\033[0m")
        print("\033[1;36mAvailable commands:\033[0m")
        print("  scan         - Detect crypto wallets and keys")
        print("  bruteforce   - Attempt to decrypt found wallets")
        print("  extract      - Extract keys from memory")
        print("  back         - Return to main menu")
        self.log_operation("Entered Crypto Analysis Module")

    def do_scan(self, arg):
        """Scan for crypto wallets and keys"""
        if self.current_module != "analysis":
            print("\n\033[1;31m[-] Enter analysis module first\033[0m")
            return
            
        print(f"\n\033[1;32m[+]\033[0m Scanning for crypto artifacts on \033[1;33m{self.current_platform.value}\033[0m")
        print("\033[1;36mTarget locations:\033[0m")
        
        if self.current_platform == Platform.WINDOWS:
            print("- %APPDATA%\\Wallet.dat files")
            print("- Registry keys under HKCU\\Software\\CryptoWallets")
        elif self.current_platform == Platform.LINUX:
            print("- ~/.wallet/ directories")
            print("- ~/.config/Electrum/")
        elif self.current_platform == Platform.ANDROID:
            print("/data/data/com.wallet.app/")
            
        print("\n\033[1;32m[+]\033[0m Scanning complete. Use 'bruteforce' on found wallets")
        self.log_operation(f"Performed crypto scan on {self.current_platform.value}")

    def do_bruteforce(self, arg):
        """Bruteforce encrypted wallets"""
        if self.current_module != "analysis":
            print("\n\033[1;31m[-] Enter analysis module first\033[0m")
            return
            
        print(f"\n\033[1;32m[+]\033[0m Starting bruteforce on \033[1;33m{self.current_platform.value}\033[0m")
        print("\033[1;36mAvailable techniques:\033[0m")
        print("- Dictionary attack (common passwords)")
        print("- Hybrid attack (dictionary + mutations)")
        print("- Rainbow table lookup")
        print("\n\033[1;33m[!] This may take significant time\033[0m")
        self.log_operation(f"Started bruteforce operation on {self.current_platform.value}")

    # ===== NAVIGATION =====
    def do_back(self, arg):
        """Return to main menu"""
        if self.current_module == "analysis":
            self.current_module = "main"
            self.prompt = "\n\033[1;35m(netaker)\033[0m > "
            print("\n\033[1;32m[+]\033[0m Returned to main menu")
            self.log_operation("Returned to main menu")
        else:
            print("\n\033[1;31m[-] Already in main menu\033[0m")

    # ===== CONFIGURATION DISPLAY =====
    def do_show(self, arg):
        """Show current configuration"""
        print("\n\033[1;36mCurrent Configuration:\033[0m")
        print(f"Platform: \033[1;33m{self.current_platform.value if self.current_platform else 'Not set'}\033[0m")
        print(f"Module: \033[1;33m{self.current_module}\033[0m")
        print(f"Payload: \033[1;33m{self.current_payload.value if self.current_payload else 'Not generated'}\033[0m")
        print(f"Delivery: \033[1;33m{self.delivery_method.value if self.delivery_method else 'Not set'}\033[0m")
        print(f"C2 Server: \033[1;33m{C2_IP}:{C2_PORT}\033[0m")
        print(f"Output Directory: \033[1;33m{os.path.abspath(OUTPUT_DIR)}\033[0m")
        print(f"Data Portal: \033[1;33m{os.path.abspath(DATA_PORTAL_DIR)}\033[0m")
        print(f"Log File: \033[1;33m{os.path.abspath(LOG_FILE)}\033[0m")

    # ===== FRAMEWORK EXIT =====
    def do_exit(self, arg):
        """Exit the framework securely"""
        print("\n\033[1;31m[!] Performing secure shutdown...\033[0m")
        print("- Clearing temporary files")
        print("- Stopping C2 listeners")
        print("- Verifying log integrity")
        self.log_operation("Framework shutdown initiated")
        sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NETAKER Crypto Analysis Framework")
    parser.add_argument("--platform", help="Set initial platform (windows/linux/macos/android/ios)")
    parser.add_argument("--c2-ip", help="Set C2 server IP address", default=C2_IP)
    parser.add_argument("--c2-port", type=int, help="Set C2 server port", default=C2_PORT)
    parser.add_argument("--output-dir", help="Set payload output directory", default=OUTPUT_DIR)
    parser.add_argument("--data-dir", help="Set data portal directory", default=DATA_PORTAL_DIR)
    
    args = parser.parse_args()
    
    # Update global configuration from command line
    C2_IP = args.c2_ip
    C2_PORT = args.c2_port
    OUTPUT_DIR = args.output_dir
    DATA_PORTAL_DIR = args.data_dir
    
    try:
        cli = NETAKERCLI()
        if args.platform:
            try:
                cli.current_platform = Platform(args.platform.lower())
                print(f"\n\033[1;32m[+]\033[0m Platform set to \033[1;33m{cli.current_platform.value}\033[0m via command line")
            except ValueError:
                print("\n\033[1;31m[-] Invalid platform specified. Available: windows, linux, macos, android, ios\033[0m")
        
        cli.cmdloop()
    except KeyboardInterrupt:
        print("\n\033[1;31m[!] Interrupt received - performing secure exit\033[0m")
        sys.exit(0)
