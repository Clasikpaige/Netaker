#!/usr/bin/env python3
"""
\033[91m
███╗   ██╗███████╗████████╗ █████╗ ██╗  ██╗███████╗██████╗ 
████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██║ ██╔╝██╔════╝██╔══██╗
██╔██╗ ██║█████╗     ██║   ███████║█████╔╝ █████╗  ██████╔╝
██║╚██╗██║██╔══╝     ██║   ██╔══██║██╔═██╗ ██╔══╝  ██╔══██╗
██║ ╚████║███████╗   ██║   ██║  ██║██║  ██╗███████╗██║  ██║
╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

 ██████╗██████╗ ██╗   ██╗██████╗ ████████╗ ██████╗     █████╗ ███╗   ██╗ █████╗ ██╗     ██╗███████╗███████╗
██╔════╝██╔══██╗██║   ██║██╔══██╗╚══██╔══╝██╔═══██╗   ██╔══██╗████╗  ██║██╔══██╗██║     ██║██╔════╝██╔════╝
██║     ██████╔╝██║   ██║██║  ██║   ██║   ██║   ██║   ███████║██╔██╗ ██║███████║██║     ██║█████╗  █████╗  
██║     ██╔═══╝ ██║   ██║██║  ██║   ██║   ██║   ██║   ██╔══██║██║╚██╗██║██╔══██║██║     ██║██╔══╝  ██╔══╝  
╚██████╗██║     ╚██████╔╝██████╔╝   ██║   ╚██████╔╝   ██║  ██║██║ ╚████║██║  ██║███████╗██║██║     ███████╗
 ╚═════╝╚═╝      ╚═════╝ ╚═════╝    ╚═╝    ╚═════╝    ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝     ╚══════╝
\033[0m
"""

Modern Red Team Framework - Multi-Vector Delivery & EDR Evation
Created by: clasikpaige | GitHub: github.com/clasikpaige
For authorized security research only
"""

import argparse
import sys
from cmd import Cmd
from pyfiglet import Figlet
from simple_term_menu import TerminalMenu

class RedTeamCLI(Cmd):
    prompt = "\n(redteam) > "
    intro = """
    Select an option from the menu below:
    [Type 'help' for commands]
    """

    def __init__(self):
        super().__init__()
        self.current_payload = None
        self.show_banner()

    def show_banner(self):
        f = Figlet(font='slant')
        print(f.renderText('REDTEAM'))
        print("""\033[91m
   _____
  /     \\
 | () () |
  \\  ^  /
   |||||
   |||||
\033[0m""")
        print("v2.1 | Created by clasikpaige | github.com/clasikpaige\n")

    def do_generate(self, arg):
        """Generate payload: generate [type]"""
        types = ["macro_doc", "lnk_file", "hta_app"]
        terminal_menu = TerminalMenu(types, title="Select payload type:")
        selection = terminal_menu.show()
        
        if selection is not None:
            self.current_payload = types[selection]
            print(f"\n[+] Generated {types[selection]} payload")
            print("[!] Use 'show options' to configure before delivery")

    def do_show(self, arg):
        """Show current configuration: show [options|payload]"""
        if arg == "options":
            print("\nCurrent Configuration:")
            print(f"  C2 Server: {C2_SERVER}")
            print(f"  Beacon Interval: {C2_INTERVAL}s")
        elif arg == "payload":
            print(f"\nCurrent Payload: {self.current_payload}")
        else:
            print("\n[!] Available show commands:")
            print("  show options - Display current config")
            print("  show payload - Display current payload")

    def do_set(self, arg):
        """Set configuration: set [option] [value]"""
        args = arg.split()
        if len(args) != 2:
            print("\n[!] Usage: set [option] [value]")
            print("Available options: C2_SERVER, C2_INTERVAL")
            return
        
        option, value = args
        if option == "C2_SERVER":
            globals()["C2_SERVER"] = value
            print(f"[+] C2 Server set to {value}")
        elif option == "C2_INTERVAL":
            globals()["C2_INTERVAL"] = int(value)
            print(f"[+] Beacon interval set to {value}s")
        else:
            print("\n[!] Invalid option")

    def do_deliver(self, arg):
        """Deliver current payload"""
        if not self.current_payload:
            print("\n[!] No payload generated - use 'generate' first")
            return
            
        print(f"\n[+] Delivering {self.current_payload}...")
        print("[*] Simulating delivery via:")
        print("  - Phishing email template")
        print("  - USB drop routine")
        print("  - Network propagation\n")

    def do_exit(self, arg):
        """Exit the framework"""
        print("\n[!] Cleaning up artifacts...")
        sys.exit(0)

if __name__ == "__main__":
    # Default configuration
    C2_SERVER = "https://your-c2-domain.com"
    C2_INTERVAL = 60
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--c2", help="Set C2 server address")
    parser.add_argument("--interval", type=int, help="Set beacon interval")
    args = parser.parse_args()
    
    if args.c2:
        C2_SERVER = args.c2
    if args.interval:
        C2_INTERVAL = args.interval
    
    try:
        RedTeamCLI().cmdloop()
    except KeyboardInterrupt:
        print("\n[!] Ctrl+C detected - exiting cleanly")
        sys.exit(0)
