#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DNS Archive를 사용하여 서브도메인을 수집하는 스캐너 모듈
"""

import aiohttp
from typing import Set
from rich.console import Console
from bs4 import BeautifulSoup
import re

console = Console()

class DNSArchiveScanner:
    """DNS Archive를 통한 서브도메인 스캐너"""
    
    def __init__(self, domain: str, silent: bool = False):
        """
        Args:
            domain (str): 대상 도메인 (예: example.com)
        """
        self.domain = domain
        self.base_url = "https://dnsarchive.net/search"
        self.subdomains = set()
        self.silent = silent
        
    async def scan(self) -> Set[str]:
        """
        DNS Archive를 통해 서브도메인 스캔 수행
        
        Returns:
            Set[str]: 수집된 고유한 서브도메인 목록
        """
        try:
            params = {
                'q': self.domain
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status != 200:
                        return set()
                        
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # 도메인 정보가 있는 테이블 행 찾기
                    domain_rows = soup.find_all('tr')
                    
                    for row in domain_rows:
                        domain_cell = row.find('td', {'data-label': 'Domain'})
                        if domain_cell and domain_cell.find('a'):
                            domain = domain_cell.find('a').text.strip()
                            # 도메인에서 마지막 점(.) 제거
                            if domain.endswith('.'):
                                domain = domain[:-1]
                            # 대상 도메인으로 끝나는 서브도메인만 추가
                            if domain.endswith(self.domain):
                                self.subdomains.add(domain.lower())
                            
            return self.subdomains
            
        except Exception as e:
            if not self.silent:
                console.print(f"[bold red][-][/] Error while scanning DNS Archive: {str(e)}")
            return set()

if __name__ == "__main__":
    import asyncio
    
    async def main():
        """테스트용 메인 함수"""
        try:
            domain = "vulnweb.com"
            scanner = DNSArchiveScanner(domain)
            results = await scanner.scan()
            
            console.print(f"\n[bold green][*] 총 {len(results)}개의 서브도메인을 찾았습니다.[/]")
            if results:
                for subdomain in sorted(results):
                    console.print(f"[cyan]{subdomain}[/]")
            
        except Exception as e:
            console.print(f"[bold red][-] 메인 함수 실행 중 오류 발생: {str(e)}[/]")
            
    asyncio.run(main())