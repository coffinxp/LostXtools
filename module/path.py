# This program was created by: Naho, AnonKryptiQuz, Coffinxp and Hexsh1dow 

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from colorama import init, Fore, Style

init(autoreset=True)

def get_paths_html(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        paths = set()

        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(url, href)
            parsed_url = urlparse(full_url)

            if parsed_url.netloc == urlparse(url).netloc:
                paths.add(parsed_url.path)

        return paths
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error fetching HTML paths: {e}")
        return set()

def get_paths_sitemap(url):
    sitemap_url = urljoin(url, '/sitemap.xml')
    try:
        response = requests.get(sitemap_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'xml')
        paths = set()

        for loc in soup.find_all('loc'):
            full_url = loc.text
            parsed_url = urlparse(full_url)
            paths.add(parsed_url.path)

        return paths
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error fetching sitemap: {e}")
        return set()

def get_paths_robots(url):
    robots_url = urljoin(url, '/robots.txt')
    try:
        response = requests.get(robots_url, timeout=10)
        response.raise_for_status()
        paths = set()
        for line in response.text.splitlines():
            if line.startswith('Disallow:'):
                path = line.split(':')[1].strip()
                paths.add(path)
        return paths
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error fetching robots.txt: {e}")
        return set()

def get_all_paths(url):
    print(Fore.CYAN + Style.BRIGHT + "\n🔍 Starting path enumeration...\n")

    paths_html = get_paths_html(url)
    paths_sitemap = get_paths_sitemap(url)
    paths_robots = get_paths_robots(url)

    all_paths = paths_html.union(paths_sitemap).union(paths_robots)

    if all_paths:
        print(Fore.GREEN + Style.BRIGHT + "✨ Paths found:")
        for path in all_paths:
            print(Fore.BLUE + f"  ➡ {path}")
    else:
        print(Fore.RED + "❌ No paths found on the website.")

def main():
    print(Fore.BLUE + Style.BRIGHT + """
              _   _                                  
             | | | |                                 
  _ __   __ _| |_| |__     ___ _ __  _   _ _ __ ___  
 | '_ \ / _` | __| '_ \   / _ \ '_ \| | | | '_ ` _ \ 
 | |_) | (_| | |_| | | | |  __/ | | | |_| | | | | | |
 | .__/ \__,_|\__|_| |_|  \___|_| |_|\__,_|_| |_| |_|
 | |                                                 
 |_|                                                 

    """)

    url = input(Fore.YELLOW + Style.BRIGHT + "🌐 Enter the website URL: ").strip()

    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    get_all_paths(url)

    print(Fore.CYAN + "\n🎯 Finished.")
    print(Fore.CYAN + "Created by Naho, AnonKryptiQuz, Coffinxp and Hexsh1dow")

if __name__ == "__main__":
    main()
