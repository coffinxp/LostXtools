#!/usr/bin/python3

import requests
import re
import random


colors = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "purple": "\033[35m",
    "cyan": "\033[36m",
    "orange": "\033[38;5;214m",  # Added orange color
    "bold": "\033[1m",
    "underline": "\033[4m",
    "reset": "\033[0m",
}


def random_color():
    return random.choice(list(colors.values())[:-1])  


def show_banner():
    art = f"""
             a          a
             aaa        aaa
            aaaaaaaaaaaaaaaa
           aaaaaaaaaaaaaaaaaa
          aaaaafaaaaaaafaaaaaa
          aaaaaaaaaaaaaaaaaaaa
           aaaaaaaaaaaaaaaaaa
            aaaaaaa  aaaaaaa
             aaaaaaaaaaaaaa
  a         aaaaaaaaaaaaaaaa
 aaa       aaaaaaaaaaaaaaaaaa
 aaa      aaaaaaaaaaaaaaaaaaaa
 aaa     aaaaaaaaaaaaaaaaaaaaaa
 aaa    aaaaaaaaaaaaaaaaaaaaaaaa
  aaa   aaaaaaaaaaaaaaaaaaaaaaaa
  aaa   aaaaaaaaaaaaaaaaaaaaaaaa
  aaa    aaaaaaaaaaaaaaaaaaaaaa
   aaa    aaaaaaaaaaaaaaaaaaaa
    aaaaaaaaaaaaaaaaaaaaaaaaaa
     aaaaaaaaaaaaaaaaaaaaaaaaa
    """
    print(f"{random_color()}{art}{colors['reset']}")
    print(f"{colors['cyan']}{colors['bold']}Coded by: {colors['orange']}teamLost{colors['reset']}\n")
    print(f"{colors['purple']}{colors['bold']}miau, miau miau!{colors['reset']}\n")


found_subdomains = []


def handle_response(api_name, response, extract_subdomains):
    try:
        if api_name == "HackerTarget":
            results = response.text.split()
            for entry in results:
                found_subdomains.append(entry.split(",")[0])
        elif api_name == "AlienVault":
            data = response.json()["passive_dns"]
            for item in data:
                found_subdomains.append(item["hostname"])
        elif api_name == "Urlscan":
            data = response.json()["results"]
            for res in data:
                found_subdomains.append(res["task"]["domain"])
        elif api_name == "crt.sh":
            data = response.json()
            for entry in data:
                found_subdomains.append(entry["common_name"])
                found_subdomains.append(entry["name_value"])
    except Exception as e:
        print(f"{colors['red']}Error processing data from {api_name} API: {e}{colors['reset']}")


def fetch_subdomains(api_name, url, extract_subdomains):
    try:
        response = requests.get(url)
        handle_response(api_name, response, extract_subdomains)
    except requests.RequestException as e:
        print(f"{colors['red']}Request failed for {api_name}: {e}{colors['reset']}")


def run_subdomain_scan(target_domain):
    print(f"{colors['cyan']}{colors['bold']}Scanning subdomains for: {colors['underline']}{target_domain}{colors['reset']}\n")

   
    urls = {
        "HackerTarget": f"https://api.hackertarget.com/hostsearch/?q={target_domain}",
        "AlienVault": f"https://otx.alienvault.com/api/v1/indicators/domain/{target_domain}/passive_dns",
        "Urlscan": f"https://urlscan.io/api/v1/search/?q=domain:{target_domain}",
        "crt.sh": f"https://crt.sh/?q={target_domain}&output=json"
    }

    
    for api_name, url in urls.items():
        fetch_subdomains(api_name, url, None)

    
    clean_subdomains = list(set([sub.lower().strip() for sub in found_subdomains if sub.endswith(target_domain)]))

   
    print(f"\n{colors['yellow']}{colors['bold']}Subdomains found:{colors['reset']}\n")
    if clean_subdomains:
        for sub in clean_subdomains:
            print(f"{colors['green']}{sub}{colors['reset']}")
    else:
        print(f"{colors['red']}No subdomains found.{colors['reset']}")


if __name__ == "__main__":
    
    show_banner()

   
    domain = input(f"{colors['bold']}{colors['orange']}Enter the domain to scan: {colors['reset']}")

    
    run_subdomain_scan(domain)
