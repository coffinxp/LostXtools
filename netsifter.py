import os
import sys
import subprocess
import time
from time import sleep
from colorama import Fore, Style, init
from rich import print as rich_print
from rich.panel import Panel

init(autoreset=True)

class Color:
    BLUE = '\033[94m'
    GREEN = '\033[1;92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    ORANGE = '\033[38;5;208m'
    BOLD = '\033[1m'
    UNBOLD = '\033[22m'
    ITALIC = '\033[3m'
    UNITALIC = '\033[23m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def loading_animation(text):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        sleep(0.01)
    print()

def display_menu():
    title = """
███╗   ██╗███████╗████████╗███████╗██╗███████╗████████╗███████╗██████╗ 
████╗  ██║██╔════╝╚══██╔══╝██╔════╝██║██╔════╝╚══██╔══╝██╔════╝██╔══██╗
██╔██╗ ██║█████╗     ██║   ███████╗██║█████╗     ██║   █████╗  ██████╔╝
██║╚██╗██║██╔══╝     ██║   ╚════██║██║██╔══╝     ██║   ██╔══╝  ██╔══██╗
██║ ╚████║███████╗   ██║   ███████║██║██║        ██║   ███████╗██║  ██║
╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚══════╝╚═╝╚═╝        ╚═╝   ╚══════╝╚═╝  ╚═╝
    """
    # Print each line with a delay
    for line in title.splitlines():
        for char in line:
            sys.stdout.write(Color.ORANGE + Style.BRIGHT + char)
            sys.stdout.flush()
            sleep(0.0040)
        print()
    
    print(Fore.WHITE + Style.BRIGHT + "─" * 65)
    border_color = Color.CYAN + Style.BRIGHT
    option_color = Fore.WHITE + Style.BRIGHT  
    
    print(border_color + "┌" + "─" * 63 + "┐")
    
    options = [
        "1]  WP Plugin Scanner",
        "2]  Path Enumeration",
        "3]  WP Enumeration",
        "4]  Emails Scanner",
        "5]  Ports Scanner",
        "6]  Subdomain Scanner",
        "7]  Wayback URLs",
        "8]  Exit"
    ]
    
    for option in options:
        # Adjust the length to fit emojis
        print(border_color + "│ " + option_color + option.ljust(60) + border_color + "│")
    
    print(border_color + "└" + "─" * 63 + "┘")
    authors = "Created by: Naho, AnonKryptiQuz, CoffinXP, HexSh1dow"
    instructions = "Select an option by entering the corresponding number:"
    
    print(Fore.WHITE + Style.BRIGHT + "─" * 65)
    print(Fore.WHITE + Style.BRIGHT + authors.center(65))
    print(Fore.WHITE + Style.BRIGHT + "─" * 65)
    print(Fore.WHITE + Style.BRIGHT + instructions.center(65))
    print(Fore.WHITE + Style.BRIGHT + "─" * 65)

def print_exit_menu():
    clear_screen()

    panel = Panel(
        """

               __       _ ______           
   ____  ___  / /______(_) __/ /____  _____
  / __ \/ _ \/ __/ ___/ / /_/ __/ _ \/ ___/
 / / / /  __/ /_(__  ) / __/ /_/  __/ /    
/_/ /_/\___/\__/____/_/_/  \__/\___/_/     
                                           

                                           
                                           
  Credit - Naho x AnonKryptiQuz x Coffinxp x Hexsh1dow 
        """,
        style="bold green",
        border_style="blue",
        expand=False
    )
    rich_print(panel)
    print(Color.RED + "\n\nSession Off ...\n")
    exit()

def handle_selection(selection):
    if selection == '3':
        clear_screen()
        print("\033[92m[+] Launching WP Enumeration...\033[0m") 
        WP_enum = "python3 module/WPenum.py"
        subprocess.run(WP_enum, shell=True)

    elif selection == '5':
        clear_screen()
        print(Color.GREEN + "[+] Launching Ports Scanner...")
        WP_enum = "python3 module/ports.py"
        subprocess.run(WP_enum, shell=True)

    elif selection == '6':
        clear_screen()
        print(Color.GREEN + "[+] Launching Subdomain Scanner...")
        WP_enum = "python3 module/subdomi.py"
        subprocess.run(WP_enum, shell=True)

    elif selection == '7':
        clear_screen()
        print(Color.GREEN + "[+] Launching Wayback URLs...")
        WP_enum = "python3 module/wayback.py"
        subprocess.run(WP_enum, shell=True)

    elif selection == '2':
        clear_screen()
        print(Color.GREEN + "[+] Launching Path Enumeration...")
        WP_enum = "python3 module/path.py"
        subprocess.run(WP_enum, shell=True)

    elif selection == '1':
        clear_screen()
        print(Color.GREEN + "[+] Launching WP Plugin Scanner...")
        WP_enum = "python3 module/plugin.py"
        subprocess.run(WP_enum, shell=True)

    elif selection == '4':
        clear_screen()
        print(Color.GREEN + "[+] Launching Emails Scanner...")
        WP_enum = "python3 module/emails.py"
        subprocess.run(WP_enum, shell=True)

    elif selection == '8':
        clear_screen()
        print_exit_menu()
        
    else:
        print(Color.RED + "[!] Invalid selection, try again...")

def main():
    clear_screen()
    sleep(1)
    clear_screen()

    while True:
        display_menu()
        choice = input(f"\n{Fore.CYAN}[?] Select an option (0-8): {Style.RESET_ALL}").strip()
        handle_selection(choice)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_exit_menu()
        sys.exit(0)
