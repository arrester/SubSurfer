#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AlienVault API를 사용하여 서브도메인을 수집하는 스캐너 모듈
"""

import aiohttp
from typing import Set
from rich.console import Console

console = Console()

class AlienVaultScanner:
    """AlienVault API를 통한 서브도메인 스캐너"""
    
    def __init__(self, domain: str):
        """
        Args:
            domain (str): 대상 도메인 (예: example.com)
        """
        self.domain = domain
        self.base_url = "https://otx.alienvault.com/api/v1/indicators/domain"
        self.subdomains = set()
        
    async def scan(self) -> Set[str]:
        """
        AlienVault API를 통해 서브도메인 스캔 수행
        
        Returns:
            Set[str]: 수집된 고유한 서브도메인 목록
        """
        try:
            url = f"{self.base_url}/{self.domain}/passive_dns"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        return set()
                        
                    data = await response.json()
                    
                    for entry in data.get('passive_dns', []):
                        hostname = entry.get('hostname', '')
                        if hostname and hostname.endswith(f".{self.domain}"):
                            self.subdomains.add(hostname.lower())
                            
            return self.subdomains
            
        except Exception as e:
            console.print(f"[bold red][-][/] AlienVault 스캔 중 오류 발생: {str(e)}")
            return set()
