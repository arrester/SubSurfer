#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ShrewdEye API를 사용하여 서브도메인을 수집하는 스캐너 모듈
"""

import aiohttp
from typing import Set
from rich.console import Console

console = Console()

class ShrewdEyeScanner:
    """ShrewdEye API를 통한 서브도메인 스캐너"""
    
    def __init__(self, domain: str, silent: bool = False):
        """
        Args:
            domain (str): 대상 도메인 (예: example.com)
        """
        self.domain = domain
        self.base_url = "https://shrewdeye.app/api/domains"
        self.subdomains = set()
        self.silent = silent
        
    async def scan(self) -> Set[str]:
        """
        ShrewdEye API를 통해 서브도메인 스캔 수행
        
        Returns:
            Set[str]: 수집된 고유한 서브도메인 목록
        """
        try:
            params = {'q': self.domain}
            
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status != 200:
                        return set()
                        
                    data = await response.json()
                    
                    for entry in data:
                        subdomain = entry.get('domain')
                        if subdomain and subdomain.endswith(f".{self.domain}"):
                            self.subdomains.add(subdomain.lower())
                            
            return self.subdomains
            
        except Exception as e:
            if not self.silent:
                console.print(f"[bold red][-][/] Error while scanning ShrewdEye: {str(e)}")
            return set()
