import requests
from bs4 import BeautifulSoup
import re
import aiohttp
from typing import Set
from rich.console import Console

console = Console()

class AbuseIPDBScanner:
    def __init__(self, domain: str, silent: bool = False):
        self.domain = domain
        self.headers = {
            'cookie': 'XSRF-TOKEN=',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        self.silent = silent

    async def scan(self) -> Set[str]:
        """서브도메인 스캔"""
        try:
            url = f'https://www.abuseipdb.com/whois/{self.domain}'
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers) as response:
                    text = await response.text()
                    
            # HTML 파싱
            soup = BeautifulSoup(text, 'html.parser')
            
            # Subdomains 섹션 찾기
            subdomains_section = soup.find('h4', text='Subdomains')
            current_section = soup.find('h2', text='Current DNS Records')
            
            # 서브도메인 추출
            subdomains = set()
            if subdomains_section and current_section:
                for li in subdomains_section.find_next('div').find_all('li'):
                    subdomain = li.get_text().strip()
                    if subdomain:  # 중복은 set()이 자동으로 처리
                        subdomains.add(f"{subdomain}.{self.domain}")
                        
            return subdomains
            
        except Exception as e:
            if not self.silent:
                console.print(f"[bold red][-][/] Error while scanning AbuseIPDB: {str(e)}")
            return set()

    def save_results(self, subdomains, filename="abuseipdb_result.txt"):
        with open(filename, "w") as f:
            f.write("\n".join(subdomains))

if __name__ == "__main__":
    domain = "vulnweb.com"
    scanner = AbuseIPDBScanner(domain)
    subdomains = scanner.scan()
    
    print(f"A total of {len(subdomains)} subdomains were found")
    print("\n".join(subdomains))
    
    scanner.save_results(subdomains)
