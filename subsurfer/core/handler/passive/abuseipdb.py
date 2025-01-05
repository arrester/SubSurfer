import requests
from bs4 import BeautifulSoup
import re

class AbuseIPDBScanner:
    def __init__(self, domain: str):
        self.domain = domain
        self.headers = {
            'cookie': 'XSRF-TOKEN=',
            'user-agent': 'Mozilla/5.0 (Macintosh; Isntel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }

    def scan(self):
        # 요청할 URL 
        url = f'https://www.abuseipdb.com/whois/{self.domain}'

        # GET 요청 보내기
        response = requests.get(url, headers=self.headers)

        # 응답 인코딩 설정
        response.encoding = 'utf-8'

        # HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # Subdomains 섹션 찾기
        subdomains_section = soup.find('h4', text='Subdomains')
        current_section = soup.find('h2', text='Current DNS Records')

        # 서브도메인 추출
        subdomains = []
        if subdomains_section and current_section:
            # Subdomains와 Current 섹션 사이의 모든 li 태그 찾기
            for li in subdomains_section.find_next('div').find_all('li'):
                subdomain = li.get_text().strip()
                if subdomain and subdomain not in subdomains:  # 중복 제거
                    subdomains.append(f"{subdomain}.{self.domain}")

        return subdomains

    def save_results(self, subdomains, filename="abuseipdb_result.txt"):
        with open(filename, "w") as f:
            f.write("\n".join(subdomains))

if __name__ == "__main__":
    domain = "verily.com"
    scanner = AbuseIPDBScanner(domain)
    subdomains = scanner.scan()
    
    print(f"총 {len(subdomains)}개의 서브도메인을 찾았습니다.")
    print("\n".join(subdomains))
    
    scanner.save_results(subdomains)
