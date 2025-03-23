#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SubdomainFinder API를 사용하여 서브도메인을 수집하는 스캐너 모듈
"""

import aiohttp
import random
import re
from typing import Set
from bs4 import BeautifulSoup
from rich.console import Console
from urllib.parse import urljoin
import hashlib
import time

console = Console()

class SubdomainFinderScanner:
    """SubdomainFinder API를 통한 서브도메인 스캐너"""
    
    def __init__(self, domain: str, silent: bool = False):
        """
        Args:
            domain (str): 대상 도메인 (예: example.com)
            silent (bool): 출력 메시지 표시 여부
        """
        self.domain = domain
        self.base_url = "https://subdomainfinder.c99.nl"
        self.subdomains = set()
        self.silent = silent
        
    def _generate_csrf_token(self) -> str:
        """CSRF 토큰 생성"""
        return "CSRF101408313"
        
    def _generate_hash_token(self, domain: str) -> str:
        """도메인에 대한 해시 토큰 생성"""
        return "1a96c949aab830f581bc60252024140d3fa61f92"
        
    async def scan(self) -> Set[str]:
        """서브도메인 스캔 수행"""
        # if not self.silent:
        #     console.print(f"[bold blue][+] SubdomainFinder 스캔 시작: {self.domain}[/]")
            
        try:
            # random User-Agent set
            user_agents = [
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
            ]
            
            headers = {
                "User-Agent": random.choice(user_agents),
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Language": "ko-KR,ko;q=0.9",
                "Origin": self.base_url,
                "Referer": self.base_url,
                "Sec-Ch-Ua": "\"Not:A-Brand\";v=\"24\", \"Chromium\";v=\"134\"",
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": "\"macOS\"",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Upgrade-Insecure-Requests": "1",
                "Cache-Control": "max-age=0"
            }
            
            csrf_token = self._generate_csrf_token()
            hash_token = self._generate_hash_token(self.domain)
            
            form_data = {
                f"CSRF9843428298797932": csrf_token,
                "jn": "JS aan, T aangeroepen, CSRF aangepast",
                "domain": self.domain,
                "lol-stop-reverse-engineering-my-source-and-buy-an-api-key": hash_token,
                "scan_subdomains": ""
            }
            
            async with aiohttp.ClientSession() as session:
                # post request - scan
                async with session.post(self.base_url, headers=headers, data=form_data, allow_redirects=False) as response:
                    if response.status != 302:
                        if not self.silent:
                            console.print(f"[bold red][-] SubdomainFinder 요청 실패: HTTP {response.status}[/]")
                        return self.subdomains
                    
                    # redirect location check
                    redirect_url = response.headers.get('Location')
                    if not redirect_url:
                        if not self.silent:
                            console.print("[bold red][-] 리다이렉트 URL을 찾을 수 없습니다.[/]")
                        return self.subdomains
                        
                    if not self.silent:
                        console.print(f"[bold blue][*] 스캔 결과 페이지로 이동: {redirect_url}[/]")
                    
                    # redirect url get request
                    async with session.get(redirect_url, headers={
                        "User-Agent": headers["User-Agent"],
                        "Accept": headers["Accept"],
                        "Referer": self.base_url
                    }) as result_response:
                        if result_response.status != 200:
                            if not self.silent:
                                console.print(f"[bold red][-] 스캔 결과 페이지 요청 실패: HTTP {result_response.status}[/]")
                            return self.subdomains
                        
                        html_content = await result_response.text()
                        
                        soup = BeautifulSoup(html_content, 'html.parser')
                        
                        # 서브도메인 추출 (테이블에서 추출)
                        table_rows = soup.find_all('tr')
                        for row in table_rows:
                            # a tag find
                            a_tag = row.find('a', class_='link sd')
                            if a_tag and a_tag.string:
                                subdomain = a_tag.string.strip().lower()
                                if subdomain.endswith(self.domain):
                                    self.subdomains.add(subdomain)
            
            # if not self.silent:
            #     console.print(f"[bold green][+] SubdomainFinder 스캔 완료: {len(self.subdomains)}개 발견[/]")
            
            return self.subdomains
            
        except Exception as e:
            if not self.silent:
                console.print(f"[bold red][-] SubdomainFinder 스캔 중 오류 발생: {str(e)}[/]")
            return self.subdomains

if __name__ == "__main__":
    import asyncio
    
    async def main():
        """테스트용 메인 함수"""
        try:
            domain = "example.com"
            scanner = SubdomainFinderScanner(domain)
            results = await scanner.scan()
            
            console.print(f"\n[bold green][*] 총 {len(results)}개의 서브도메인을 찾았습니다.[/]")
            if results:
                for subdomain in sorted(results):
                    console.print(f"[cyan]{subdomain}[/]")
                    
        except Exception as e:
            console.print(f"[bold red][-] 메인 함수 실행 중 오류 발생: {str(e)}[/]")
            
    asyncio.run(main())