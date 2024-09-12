import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re
import os
import time
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import init, Fore, Style

init(autoreset=True)

image_ext = (".jpeg", ".jpg", ".exif", ".tif", ".tiff", ".gif", ".bmp", ".png", ".ppm",
             ".pgm", ".pbm", ".pnm", ".webp", ".hdr", ".heif", ".bat", ".bpg", ".cgm", ".svg")
ua = UserAgent()

def menu():
    try:
        clear()
        print(Fore.CYAN + Style.BRIGHT + """
   1 - Search in a URL
   9 - Exit
""")

        option = input(Fore.YELLOW + "Enter option: ").strip()
        if option == "1":
            url = input(Fore.YELLOW + "Enter URL (Example: http://www.pythondaily.com): ").strip()
            asyncio.run(extract_url(url))
        elif option == "9":
            exit(0)
        else:
            print(Fore.RED + "Invalid option. Please try again.")
            time.sleep(2)
            menu()
    
    except KeyboardInterrupt:
        input(Fore.RED + "Interrupted. Press Enter to continue...")
        menu()
    except Exception as e:
        print(Fore.RED + f"Error: {e}")
        input(Fore.RED + "Press Enter to continue...")
        menu()

async def fetch_url(url, session):
    try:
        async with session.get(url, headers={'User-Agent': ua.random}, timeout=10) as response:
            if response.status == 200 and response.content_type != "audio/mpeg":
                return await response.text()
    except (asyncio.TimeoutError, aiohttp.ClientError):
        return None

async def extract_url(url):
    print(Fore.CYAN + """
Searching emails... Please wait
This may take a few minutes
""")

    try:
        count = 0
        list_url = []

        async with aiohttp.ClientSession() as session:
            html = await fetch_url(url, session)
            if not html:
                print(Fore.RED + "Failed to retrieve or unsupported URL.")
                input(Fore.RED + "Press Enter to continue...")
                menu()
                return

            emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", html)

            for email in emails:
                if email not in list_url and not email.endswith(image_ext):
                    count += 1
                    print(Fore.GREEN + f"{count} - {email}")
                    list_url.append(email)

            soup = BeautifulSoup(html, "lxml")
            links = [tag.get('href') for tag in soup.find_all('a') if tag.get('href') and tag.get('href').startswith('http')]

            print(Fore.CYAN + f"{len(links)} URLs will be analyzed...")
            time.sleep(2)

            tasks = []
            for link in links:
                tasks.append(fetch_url(link, session))

            for task in asyncio.as_completed(tasks):
                html = await task
                if html:
                    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", html)
                    for email in emails:
                        if email not in list_url and not email.endswith(image_ext):
                            count += 1
                            print(Fore.GREEN + f"{count} - {email}")
                            list_url.append(email)

        print("\n" + Fore.CYAN + f"Extraction Complete\nTotal Emails Found: {count}")
        input(Fore.YELLOW + "Press Enter to continue...")
        menu()

    except KeyboardInterrupt:
        input(Fore.RED + "Interrupted. Press Enter to continue...")
        menu()
    except Exception as e:
        print(Fore.RED + f"Error: {e}")
        input(Fore.RED + "Press Enter to continue...")
        menu()

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def main():
    clear()
    menu()

if __name__ == "__main__":
    main()
