#!/usr/bin/env python3

import requests
import sys
import argparse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

ASCII_ART = ''' 
                   ___           __  
 _    _____ ___ __/ _ )___ _____/ /__
| |/|/ / _ `/ // / _  / _ `/ __/  '_/
|__,__/\_,_/\_, /____/\_,_/\__/_/\_\ 
           /___/                                     
'''

class TerminalColors:
    HEADER = '\033[95m'
    OK = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'
    INFO = '\033[94m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CYAN = '\033[96m'
    MAGENTA = '\033[35m'

WAYBACK_API_URL = "https://web.archive.org/cdx/search?matchType=domain&collapse=urlkey&output=text&fl=original"
SCREENSHOT_FOLDER = "screens/"

def setup_arg_parser():
    parser = argparse.ArgumentParser(
        description=TerminalColors.BOLD + TerminalColors.HEADER + "Wayback Machine URL Fetcher" + TerminalColors.RESET,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-k", "--keyword", type=str)
    parser.add_argument("-l", "--limit", type=int)
    parser.add_argument("-s", "--screenshot", action="store_true")
    parser.add_argument("-r", "--rate-limit", type=float, default=1)
    parser.add_argument("-o", "--output", type=str)
    parser.add_argument("-t", "--text-output", action="store_true")
    return parser

def take_screenshots(urls, rate_limit):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    driver.set_page_load_timeout(60)

    print(TerminalColors.INFO + TerminalColors.BOLD + "[+] Taking screenshots of URLs..." + TerminalColors.RESET)
    for i, url in enumerate(urls.split(), start=1):
        try:
            print(f"{TerminalColors.INFO}Loading URL {i}: {url}{TerminalColors.RESET}")
            driver.get(url)
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            sleep(rate_limit)
            screenshot_path = f"{SCREENSHOT_FOLDER}screen-{i}.png"
            driver.save_screenshot(screenshot_path)
            print(f"{TerminalColors.OK}Screenshot saved: {screenshot_path}{TerminalColors.RESET}")
        except Exception as e:
            print(f"{TerminalColors.FAIL}Error taking screenshot of {url}: {e}{TerminalColors.RESET}")

    driver.quit()
    print(TerminalColors.INFO + TerminalColors.BOLD + "[+] Done with screenshots!" + TerminalColors.RESET)

def fetch_urls(domain, keyword, limit):
    api_url = f"{WAYBACK_API_URL}&url={domain}"
    if keyword:
        api_url += f"&filter=urlkey:.*{keyword}"
    if limit:
        api_url += f"&limit={limit}"
    
    print(f"{TerminalColors.INFO}Fetching URLs from {api_url}{TerminalColors.RESET}")
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"{TerminalColors.FAIL}Error fetching URLs: {e}{TerminalColors.RESET}")
        return ""

def main():
    print(TerminalColors.CYAN + TerminalColors.BOLD + ASCII_ART + TerminalColors.RESET)
    print(TerminalColors.MAGENTA + TerminalColors.BOLD + "Welcome to the Wayback Machine URL Fetcher!" + TerminalColors.RESET)
    
    domain = input(TerminalColors.INFO + TerminalColors.BOLD + "Please enter the target domain (e.g., example.com): " + TerminalColors.RESET).strip()
    if not domain:
        print(TerminalColors.FAIL + "[!] No domain provided. Exiting." + TerminalColors.RESET)
        sys.exit(1)

    parser = setup_arg_parser()
    args = parser.parse_args()

    try:
        urls = fetch_urls(domain, args.keyword, args.limit)
        if args.screenshot:
            take_screenshots(urls, args.rate_limit)
        if args.output:
            with open(args.output, "w") as file:
                file.write(urls)
            print(f"{TerminalColors.OK}Output saved to: {args.output}{TerminalColors.RESET}")
        if args.text_output:
            text_file = f"{domain.replace('/', '_')}_urls.txt"
            with open(text_file, "w") as file:
                file.write(urls)
            print(f"{TerminalColors.OK}URLs saved to text file: {text_file}{TerminalColors.RESET}")
        else:
            print(urls)
    except Exception as e:
        print(TerminalColors.FAIL + f"[!] Error: {e}" + TerminalColors.RESET)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(TerminalColors.FAIL + "[!] Script canceled by user." + TerminalColors.RESET)
