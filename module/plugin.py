import requests
from bs4 import BeautifulSoup
import re
import logging
from colorama import init, Fore, Style


init()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WordPressPluginScanner:
    def __init__(self, url):
        self.url = url
        self.plugins = set()

    def fetch_html(self, url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logging.error(f"{Fore.RED}Error connecting to {url}: {e}{Style.RESET_ALL}")
            return None

    def clean_html(self, html_content):
        """Remove unwanted HTML elements like cookie banners."""
        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove common unwanted tags (e.g., cookie banners, scripts, etc.)
        for unwanted in soup(['script', 'style', 'noscript', 'iframe', 'footer', 'div']):
            unwanted.decompose()

        return str(soup)

    def scan_code_source(self, html_content):
        plugins = set()
        if not html_content:
            return plugins

        html_content = self.clean_html(html_content)  # Clean up the HTML

        soup = BeautifulSoup(html_content, 'html.parser')

        # Look for script and link tags that may reference plugins
        for script in soup.find_all('script', src=True):
            src = script['src']
            if '/wp-content/plugins/' in src:
                plugin = re.split('/wp-content/plugins/|/', src)[-2]
                plugins.add(plugin)

        for link in soup.find_all('link', href=True):
            href = link['href']
            if '/wp-content/plugins/' in href:
                plugin = re.split('/wp-content/plugins/|/', href)[-2]
                plugins.add(plugin)

        # Detect plugins from HTML comments
        comments = re.findall(r'<!--.*?-->', html_content, re.DOTALL)
        for comment in comments:
            if 'plugin' in comment.lower():
                plugins.add('plugin_detected_in_comment')

        # General regex patterns to find plugins
        patterns = [
            r'wp-content/plugins/([^/]+)',
            r'plugins/([^/]+)'
        ]
        for pattern in patterns:
            found_plugins = re.findall(pattern, html_content)
            for plugin in found_plugins:
                plugins.add(plugin)

        return plugins

    def get_plugin_version(self, plugin_name):
        """Search for plugin version in readme.txt, main .php file, or through meta tags."""
        version_patterns = [
            r'Version:\s*([0-9\.]+)',  # Common plugin version format
            r'(\d+\.\d+(\.\d+)?)'  # General version number pattern
        ]

        possible_files = [
            f"{self.url}/wp-content/plugins/{plugin_name}/readme.txt",
            f"{self.url}/wp-content/plugins/{plugin_name}/{plugin_name}.php"
        ]

        # Try fetching from common plugin files like readme.txt or plugin-name.php
        for file_url in possible_files:
            try:
                response = requests.get(file_url, timeout=10)
                response.raise_for_status()
                content = response.text
                for pattern in version_patterns:
                    match = re.search(pattern, content)
                    if match:
                        return match.group(1)
            except requests.RequestException:
                continue

        # Check the main HTML for plugin versions in script or link tags
        main_html = self.fetch_html(self.url)
        if main_html:
            soup = BeautifulSoup(main_html, 'html.parser')
            for tag in soup.find_all(['script', 'link'], src=True, href=True):
                url = tag.get('src') or tag.get('href')
                if f'/wp-content/plugins/{plugin_name}' in url:
                    version_match = re.search(r'(\d+\.\d+(\.\d+)?)', url)
                    if version_match:
                        return version_match.group(1)

        return "Unknown"

    def get_wordpress_plugins(self):
        """Fetch and detect all plugins in use on the website."""
        plugins = set()

        # Try scanning common paths where plugins are located
        plugins_url = f"{self.url}/wp-content/plugins/"
        html_content = self.fetch_html(plugins_url)
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            for link in soup.find_all('a', href=True):
                href = link['href']
                if '/wp-content/plugins/' in href:
                    plugin = href.split('/')[-2]
                    plugins.add(plugin)

        # Scan the main site for plugin references in the code
        main_html_content = self.fetch_html(self.url)
        if main_html_content:
            code_plugins = self.scan_code_source(main_html_content)
            plugins.update(code_plugins)

        return sorted(plugins)

    def print_plugins_with_versions(self):
        """Print detected plugins along with their versions."""
        if self.plugins:
            print(f"\n{Fore.GREEN}=============================={Style.RESET_ALL}")
            print(f"{Fore.GREEN}Found Plugins with Versions:{Style.RESET_ALL}")
            print(f"{Fore.GREEN}=============================={Style.RESET_ALL}")
            for i, plugin in enumerate(self.plugins, 1):
                version = self.get_plugin_version(plugin)
                print(f"{Fore.CYAN}{i}. {plugin} - Version: {version}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}=============================={Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}No plugins found.{Style.RESET_ALL}")

def print_ascii_art():
    """Print ASCII art for tool branding."""
    ascii_art = '''
       _             _                           _ _              
      | |           (_)                         | (_)             
_ __  | |_   _  __ _ _ _ __     __ _ _ __   __ _| |_ _______ _ __ 
| '_ \| | | | |/ _` | | '_ \   / _` | '_ \ / _` | | |_  / _ \ '__|
| |_) | | |_| | (_| | | | | | | (_| | | | | (_| | | |/ /  __/ |   
| .__/|_|\__,_|\__, |_|_| |_|  \__,_|_| |_|\__,_|_|_/___\___|_|   
| |             __/ |                                             
|_|            |___/                                              
    '''
    print(Fore.YELLOW + ascii_art + Style.RESET_ALL)

def main():
    """Main function to start the WordPress plugin scanner."""
    print_ascii_art()
    url = input(f"{Fore.MAGENTA}Enter the WordPress site URL to scan (e.g., http://example.com): {Style.RESET_ALL}")
    if not url.startswith('http'):
        url = 'http://' + url

    print(f"{Fore.YELLOW}\nStarting WordPress plugin scanner...{Style.RESET_ALL}")
    scanner = WordPressPluginScanner(url)
    plugins = scanner.get_wordpress_plugins()
    scanner.plugins = plugins
    scanner.print_plugins_with_versions()
    print(f"{Fore.GREEN}\nScan completed.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
