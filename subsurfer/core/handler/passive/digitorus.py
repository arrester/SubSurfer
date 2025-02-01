#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Digitorus API를 사용하여 서브도메인을 수집하는 스캐너 모듈
"""

import aiohttp
from typing import Set
from bs4 import BeautifulSoup
from rich.console import Console

console = Console()

class DigitorusScanner:
    """Digitorus API를 통한 서브도메인 스캐너"""
    
    def __init__(self, domain: str, silent: bool = False):
        """
        Args:
            domain (str): 대상 도메인 (예: example.com)
        """
        self.domain = domain
        self.base_url = "https://certificatedetails.com"
        self.subdomains = set()
        self.silent = silent
        
    async def request(self, url: str) -> str:
        """비동기 HTTP 요청 수행"""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                return ""
                
    async def scan(self) -> Set[str]:
        """
        Digitorus API를 통해 서브도메인 스캔 수행
        
        Returns:
            Set[str]: 수집된 고유한 서브도메인 목록
        """
        try:
            url = f"{self.base_url}/{self.domain}"
            
            html = await self.request(url)
            if not html:
                return set()
                
            # HTML 파싱
            soup = BeautifulSoup(html, 'html.parser')
            
            # carousel-item 내의 모든 h5 태그에서 서브도메인 추출
            carousel_items = soup.find_all('div', class_='carousel-item')
            for item in carousel_items:
                h5_tag = item.find('h5')
                if h5_tag and h5_tag.string:
                    domain = h5_tag.string.strip().lower()
                    # 도메인이 target domain과 관련있는 경우만 추가
                    base_domain = '.'.join(self.domain.split('.')[-2:])  # example.com 형태 추출
                    if domain.endswith(base_domain):
                        self.subdomains.add(domain)
            
            # IA5String 값에서 서브도메인 추출
            ia5_strings = soup.find_all(string=lambda text: isinstance(text, str) and "IA5String" in text)
            for ia5_string in ia5_strings:
                domain = ia5_string.split("'")[1].strip().lower()
                base_domain = '.'.join(self.domain.split('.')[-2:])
                if domain.endswith(base_domain):
                    self.subdomains.add(domain)
                    
            return self.subdomains
            
        except Exception as e:
            if not self.silent:
                console.print(f"[bold red][-] Error while scanning Digitorus: {str(e)}[/]")
            return set()

if __name__ == "__main__":
    import asyncio
    
    async def main():
        """테스트용 메인 함수"""
        try:
            domain = "vulnweb.com"
            scanner = DigitorusScanner(domain)
            results = await scanner.scan()
            
            console.print(f"\n[bold green][*] 총 {len(results)}개의 서브도메인을 찾았습니다.[/]")
            if results:
                for subdomain in sorted(results):
                    console.print(f"[cyan]{subdomain}[/]")
            
        except Exception as e:
            console.print(f"[bold red][-] 메인 함수 실행 중 오류 발생: {str(e)}[/]")
            
    asyncio.run(main())
