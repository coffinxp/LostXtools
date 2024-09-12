# This program was created by: Naho, AnonKryptiQuz, Coffinxp and Hexsh1dow 

import socket
from urllib.parse import urlparse
from colorama import Fore, Style, init

init(autoreset=True)

def get_public_ip(host):
    try:
        public_ip = socket.gethostbyname(host)
        return public_ip
    except socket.gaierror:
        return None

def print_banner():
    banner = Fore.CYAN + '''
  _                             
 (_)                            
  _ _ __    ___  ___ __ _ _ __  
 | | '_ \  / __|/ __/ _` | '_ \ 
 | | |_) | \__ \ (_| (_| | | | |
 |_| .__/  |___/\___\__,_|_| |_|
   | |                          
   |_|                          
    '''
    print(banner)


if __name__ == "__main__":
    print_banner()
    domain = input(Fore.YELLOW + "Enter the domain to resolve the IP: " + Style.RESET_ALL)
    parsed_url = urlparse(domain)
    if parsed_url.scheme:
        domain = parsed_url.netloc

    public_ip = get_public_ip(domain)
    
    if public_ip:
        print(f"\n{Fore.GREEN}Public IP Address of {domain}: {Fore.WHITE}{public_ip}")
    else:
        print(f"\n{Fore.RED}Could not resolve the public IP address of {domain}.")

    print(f"\n{Fore.CYAN}Created by Naho, AnonKryptiQuz, Coffinxp and Hexsh1dow {Style.RESET_ALL}")
