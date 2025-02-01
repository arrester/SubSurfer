#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Web Archive API를 사용하여 서브도메인을 수집하는 스캐너 모듈
"""

import aiohttp
from typing import Set
from rich.console import Console

console = Console()

class WebArchiveScanner:
    """Web Archive API를 통한 서브도메인 스캐너"""
    
    def __init__(self, domain: str, silent: bool = False):
        """
        Args:
            domain (str): 대상 도메인 (예: example.com)
        """
        self.domain = domain
        self.base_url = "https://web.archive.org/cdx/search/cdx"
        self.subdomains = set()
        self.silent = silent
        
    async def scan(self) -> Set[str]:
        """
        Web Archive API를 통해 서브도메인 스캔 수행
        
        Returns:
            Set[str]: 수집된 고유한 서브도메인 목록
        """
        try:
            params = {
                'matchType': 'domain',
                'fl': 'original',
                'output': 'json',
                'collapse': 'urlkey',
                'url': self.domain
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status != 200:
                        return set()
                        
                    data = await response.json()
                    
                    if not data or len(data) < 2:  # 첫 번째 행은 컬럼명
                        return set()
                        
                    for entry in data[1:]:  # 첫 번째 행 제외
                        try:
                            url = entry[0]  # original URL
                            # URL에서 도메인 추출
                            domain = url.split('/')[2].split(':')[0].lower()
                            if domain.endswith(f".{self.domain}"):
                                self.subdomains.add(domain)
                        except:
                            continue
                            
            return self.subdomains
            
        except Exception as e:
            if not self.silent:
                console.print(f"[bold red][-][/] Error while scanning Web Archive: {str(e)}")
            return set()

if __name__ == "__main__":
    import asyncio
    
    async def main():
        """테스트용 메인 함수"""
        try:
            domain = "vulnweb.com"
            scanner = WebArchiveScanner(domain)
            results = await scanner.scan()
            
            console.print(f"\n[bold green][*] 총 {len(results)}개의 서브도메인을 찾았습니다.[/]")
            if results:
                for subdomain in sorted(results):
                    console.print(f"[cyan]{subdomain}[/]")
            
        except Exception as e:
            console.print(f"[bold red][-] 메인 함수 실행 중 오류 발생: {str(e)}[/]")
            
    asyncio.run(main())