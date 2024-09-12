# This program was created by: Naho, AnonKryptiQuz, Coffinxp and Hexsh1dow 

import requests
import re
import sys
from colorama import init, Fore, Style

init()

def print_banner():
    banner = '''
 _   _ ___  ___ _ __    ___ _ __  _   _ _ __ ___  
| | | / __|/ _ \ '__|  / _ \ '_ \| | | | '_ ` _ \ 
| |_| \__ \  __/ |    |  __/ | | | |_| | | | | | |
 \__,_|___/\___|_|     \___|_| |_|\__,_|_| |_| |_|
    
    
    
    '''
    print(Fore.CYAN + Style.BRIGHT + banner + Style.RESET_ALL)
    print(Fore.YELLOW + Style.BRIGHT + "Created by Naho, AnonKryptiQuz, Coffinxp and Hexsh1dow\n" + Style.RESET_ALL)

def author_enum(wp_url, max_id=20):
    print(Fore.YELLOW + Style.BRIGHT + "[+] Enumerating users using ?author=ID" + Style.RESET_ALL)
    found_users = set()
    for user_id in range(1, max_id + 1):
        author_url = f"{wp_url}/?author={user_id}"
        try:
            response = requests.get(author_url, allow_redirects=True, timeout=10)
            if response.status_code == 200:
                if "/author/" in response.url:
                    username = response.url.split("/author/")[1].strip("/")
                    if username not in found_users:
                        print(Fore.GREEN + f"[+] Found user: {username} (ID: {user_id})" + Style.RESET_ALL)
                        found_users.add(username)
        except requests.RequestException as e:
            print(Fore.RED + f"[-] Error accessing ID {user_id}: {e}" + Style.RESET_ALL)
    return found_users

def rest_api_enum(wp_url):
    print(Fore.YELLOW + Style.BRIGHT + "[+] Enumerating users using REST API" + Style.RESET_ALL)
    api_url = f"{wp_url}/wp-json/wp/v2/users"
    found_users = set()
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            users = response.json()
            for user in users:
                username = user.get('name')
                if username and username not in found_users:
                    print(Fore.GREEN + f"[+] Found user: {username} (ID: {user['id']})" + Style.RESET_ALL)
                    found_users.add(username)
        else:
            print(Fore.RED + "[-] Could not retrieve users through REST API." + Style.RESET_ALL)
    except requests.RequestException as e:
        print(Fore.RED + f"[-] Error in REST API: {e}" + Style.RESET_ALL)
    return found_users

def sitemap_enum(wp_url):
    print(Fore.YELLOW + Style.BRIGHT + "[+] Trying to find users in sitemap" + Style.RESET_ALL)
    sitemap_url = f"{wp_url}/sitemap_index.xml"
    found_users = set()
    try:
        response = requests.get(sitemap_url, timeout=10)
        if response.status_code == 200:
            matches = re.findall(r'<loc>(.*?/author/.*?)</loc>', response.text)
            for author_url in matches:
                username = author_url.split("/author/")[1].strip("/")
                if username not in found_users:
                    print(Fore.GREEN + f"[+] Found user in sitemap: {username}" + Style.RESET_ALL)
                    found_users.add(username)
        else:
            print(Fore.RED + "[-] Sitemap not found on the site." + Style.RESET_ALL)
    except requests.RequestException as e:
        print(Fore.RED + f"[-] Error accessing sitemap: {e}" + Style.RESET_ALL)
    return found_users

def html_enum(wp_url):
    print(Fore.YELLOW + Style.BRIGHT + "[+] Trying to find users in HTML source code" + Style.RESET_ALL)
    found_users = set()
    try:
        response = requests.get(wp_url, timeout=10)
        if response.status_code == 200:
            matches = re.findall(r'author:(.*?)"', response.text, re.IGNORECASE)
            for match in matches:
                username = match.strip()
                if username and username not in found_users:
                    print(Fore.GREEN + f"[+] Found user in HTML source code: {username}" + Style.RESET_ALL)
                    found_users.add(username)
        else:
            print(Fore.RED + "[-] Could not access the main page." + Style.RESET_ALL)
    except requests.RequestException as e:
        print(Fore.RED + f"[-] Error accessing the main page: {e}" + Style.RESET_ALL)
    return found_users

def rss_enum(wp_url):
    print(Fore.YELLOW + Style.BRIGHT + "[+] Trying to find users in RSS feed" + Style.RESET_ALL)
    rss_url = f"{wp_url}/feed/"
    found_users = set()
    try:
        response = requests.get(rss_url, timeout=10)
        if response.status_code == 200:
            matches = re.findall(r'<dc:creator>(.*?)</dc:creator>', response.text, re.IGNORECASE)
            for user in matches:
                if user and user not in found_users:
                    print(Fore.GREEN + f"[+] Found user in RSS: {user}" + Style.RESET_ALL)
                    found_users.add(user)
        else:
            print(Fore.RED + "[-] Could not access RSS feed." + Style.RESET_ALL)
    except requests.RequestException as e:
        print(Fore.RED + f"[-] Error accessing RSS feed: {e}" + Style.RESET_ALL)
    return found_users

def login_page_enum(wp_url):
    print(Fore.YELLOW + Style.BRIGHT + "[+] Trying to find users on the login page (wp-login.php)" + Style.RESET_ALL)
    login_url = f"{wp_url}/wp-login.php"
    found_users = set()
    try:
        response = requests.get(login_url, timeout=10)
        if response.status_code == 200:
            matches = re.findall(r'username=(.*?)"', response.text, re.IGNORECASE)
            for match in matches:
                username = match.strip()
                if username and username not in found_users:
                    print(Fore.GREEN + f"[+] Found user on wp-login.php: {username}" + Style.RESET_ALL)
                    found_users.add(username)
        else:
            print(Fore.RED + "[-] Could not access the login page." + Style.RESET_ALL)
    except requests.RequestException as e:
        print(Fore.RED + f"[-] Error accessing the login page: {e}" + Style.RESET_ALL)
    return found_users

def robots_enum(wp_url):
    print(Fore.YELLOW + Style.BRIGHT + "[+] Trying to find information in robots.txt" + Style.RESET_ALL)
    robots_url = f"{wp_url}/robots.txt"
    found_users = set()
    try:
        response = requests.get(robots_url, timeout=10)
        if response.status_code == 200:
            matches = re.findall(r'(?i)/author/(\w+)', response.text)
            for match in matches:
                username = match.strip()
                if username and username not in found_users:
                    print(Fore.GREEN + f"[+] Found user in robots.txt: {username}" + Style.RESET_ALL)
                    found_users.add(username)
        else:
            print(Fore.RED + "[-] Could not access robots.txt." + Style.RESET_ALL)
    except requests.RequestException as e:
        print(Fore.RED + f"[-] Error accessing robots.txt: {e}" + Style.RESET_ALL)
    return found_users

def enumerate_users(wp_url, max_id=20):
    users = set()
    users.update(author_enum(wp_url, max_id))
    users.update(rest_api_enum(wp_url))
    users.update(sitemap_enum(wp_url))
    users.update(html_enum(wp_url))
    users.update(rss_enum(wp_url))
    users.update(login_page_enum(wp_url))
    users.update(robots_enum(wp_url))

    if users:
        print(Fore.CYAN + Style.BRIGHT + f"\n[+] Enumeration completed. Found {len(users)} users:" + Style.RESET_ALL)
        for user in users:
            print(Fore.YELLOW + f" - {user}" + Style.RESET_ALL)
    else:
        print(Fore.RED + "[-] No users found using the applied techniques." + Style.RESET_ALL)

if __name__ == "__main__":
    print_banner()
    wp_url = input(Fore.GREEN + "Enter a URL (with https://): " + Style.RESET_ALL).strip()
    if not wp_url:
        print(Fore.RED + "[-] The URL cannot be empty." + Style.RESET_ALL)
        sys.exit(1)

    enumerate_users(wp_url, max_id=20)
