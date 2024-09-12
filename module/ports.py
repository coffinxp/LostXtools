# This program was created by: Naho, AnonKryptiQuz, Coffinxp and Hexsh1dow 

import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.progress import Progress
from rich.prompt import Prompt
import re
import sys
import os

ASCII_ART = """
                   _                         
                  | |                        
  _ __   ___  _ __| |_   ___  ___ __ _ _ __  
 | '_ \ / _ \| '__| __| / __|/ __/ _` | '_ \ 
 | |_) | (_) | |  | |_  \__ \ (_| (_| | | | |
 | .__/ \___/|_|   \__| |___/\___\__,_|_| |_|
 | |                                         
 |_|                                         
"""

console = Console()

def is_valid_ip(ip):
    try:
        socket.inet_pton(socket.AF_INET, ip)
        return True
    except socket.error:
        return False

def is_valid_port(port):
    return 1 <= port <= 65535

def scan_port(ip, port, timeout=1):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            result = sock.connect_ex((ip, port))
            return port, result == 0
        except (socket.error, OSError) as e:
            console.print(f"Error scanning port {port}: {e}", style="bold red")
            return port, False

def scan_ports(ip, ports, timeout=1, max_workers=100):
    open_ports = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(scan_port, ip, port, timeout): port for port in ports}
        with Progress() as progress:
            task = progress.add_task("[cyan]Scanning ports...", total=len(ports))
            for future in as_completed(futures):
                port, is_open = future.result()
                if is_open:
                    open_ports.append(port)
                progress.update(task, advance=1)
    return open_ports

def print_banner():
    console.print(ASCII_ART, style="bold cyan")

def get_ip():
    while True:
        ip = Prompt.ask("Enter the IP address to scan").strip()
        if is_valid_ip(ip):
            return ip
        else:
            console.print("Invalid IP address. Please enter a valid IP address.", style="bold red")

def get_port_range():
    while True:
        try:
            start_port = int(Prompt.ask("Enter the starting port"))
            end_port = int(Prompt.ask("Enter the ending port"))
            if is_valid_port(start_port) and is_valid_port(end_port) and start_port <= end_port:
                return range(start_port, end_port + 1)
            else:
                console.print("Invalid port range. Must be between 1 and 65535, and the starting port must be less than or equal to the ending port.", style="bold red")
        except ValueError:
            console.print("Invalid input. Please enter integer numbers for the ports.", style="bold red")

def get_timeout():
    while True:
        try:
            timeout = float(Prompt.ask("Enter the timeout in seconds (default 1)", default="1").strip())
            if timeout > 0:
                return timeout
            else:
                console.print("Timeout must be a positive number.", style="bold red")
        except ValueError:
            console.print("Invalid input. Please enter a valid number for the timeout.", style="bold red")

def get_max_workers():
    while True:
        try:
            max_workers = int(Prompt.ask("Enter the maximum number of threads (default 100)", default="100").strip())
            if 1 <= max_workers <= 500:
                return max_workers
            else:
                console.print("Number of threads must be between 1 and 500.", style="bold red")
        except ValueError:
            console.print("Invalid input. Please enter a valid integer for the number of threads.", style="bold red")

def export_results(ip, open_ports, file_format='txt'):
    file_name = f'scan_results.{file_format}'
    if file_format == 'txt':
        with open(file_name, 'w') as file:
            file.write(f"Port scan for {ip}\n")
            if open_ports:
                file.write(f"Open ports: {', '.join(map(str, open_ports))}\n")
            else:
                file.write("No open ports found.\n")
    elif file_format == 'csv':
        import csv
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['IP', 'Open Ports'])
            writer.writerow([ip, ', '.join(map(str, open_ports)) if open_ports else 'None'])
    else:
        console.print(f"File format {file_format} not supported.", style="bold red")
        return

    console.print(f"Results exported to '{file_name}'.", style="bold blue")

def main():
    print_banner()
    
    target_ip = get_ip()
    port_range = get_port_range()
    timeout = get_timeout()
    max_workers = get_max_workers()
    
    console.print(f"Scanning ports on {target_ip} with a timeout of {timeout} seconds and {max_workers} threads...", style="bold green")
    
    open_ports = scan_ports(target_ip, port_range, timeout, max_workers)
    
    if open_ports:
        console.print(f"Open ports on {target_ip}: {', '.join(map(str, open_ports))}", style="bold green")
    else:
        console.print(f"No open ports found on {target_ip}.", style="bold yellow")
    
    file_format = Prompt.ask("Enter the file format to export (txt or csv)", default="txt").strip()
    export_results(target_ip, open_ports, file_format)
    console.print("Created by Naho, AnonKryptiQuz, Coffinxp and Hexsh1dow", style="bold magenta")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        console.print(f"An unexpected error occurred: {e}", style="bold red")
        sys.exit(1)
