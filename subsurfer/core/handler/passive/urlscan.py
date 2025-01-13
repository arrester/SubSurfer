#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Urlscan.io API를 사용하여 서브도메인을 수집하는 스캐너 모듈
"""

import aiohttp
from typing import Set
from rich.console import Console

console = Console()

class UrlscanScanner:
    """Urlscan.io API를 통한 서브도메인 스캐너"""
    
    def __init__(self, domain: str):
        """
        Args:
            domain (str): 대상 도메인 (예: example.com)
        """
        self.domain = domain
        self.base_url = "https://urlscan.io/api/v1/search"
        self.subdomains = set()
        
    async def scan(self) -> Set[str]:
        """
        Urlscan.io API를 통해 서브도메인 스캔 수행
        
        Returns:
            Set[str]: 수집된 고유한 서브도메인 목록
        """
        try:
            params = {
                'q': f'page.domain:{self.domain}',
                'size': 10000
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params, ssl=False) as response:
                    if response.status != 200:
                        return set()
                        
                    data = await response.json()
                    
                    for result in data.get('results', []):
                        subdomain = result.get('page', {}).get('domain')
                        if subdomain and subdomain.endswith(f".{self.domain}"):
                            self.subdomains.add(subdomain.lower())
                            
            return self.subdomains
            
        except Exception as e:
            console.print(f"[bold red][-][/] Urlscan 스캔 중 오류 발생: {str(e)}")
            return set()
