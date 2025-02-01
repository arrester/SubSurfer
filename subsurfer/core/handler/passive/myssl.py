#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MySSL API를 사용하여 서브도메인을 수집하는 스캐너 모듈
"""

import aiohttp
import random
from typing import Set
from rich.console import Console

console = Console()

class MySSLScanner:
    """MySSL API를 통한 서브도메인 스캐너"""
    
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/120.0.6099.119 Mobile/15E148 Safari/604.1"
    ]
    
    def __init__(self, domain: str, silent: bool = False):
        """
        Args:
            domain (str): 대상 도메인 (예: example.com)
        """
        self.domain = domain
        self.base_url = "https://myssl.com/api/v1/discover_sub_domain"
        self.subdomains = set()
        self.silent = silent
        
    def get_random_user_agent(self) -> str:
        """랜덤 User-Agent 반환"""
        return random.choice(self.USER_AGENTS)
        
    async def scan(self) -> Set[str]:
        """
        MySSL API를 통해 서브도메인 스캔 수행
        
        Returns:
            Set[str]: 수집된 고유한 서브도메인 목록
        """
        try:
            params = {'domain': self.domain}
            headers = {
                "User-Agent": self.get_random_user_agent()
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params, headers=headers, ssl=False) as response:
                    if response.status != 200:
                        return set()
                        
                    data = await response.json()
                    
                    if 'data' in data and isinstance(data['data'], list):
                        for entry in data['data']:
                            subdomain = entry.get('domain')
                            if subdomain and subdomain.endswith(f".{self.domain}"):
                                self.subdomains.add(subdomain.lower())
                            
            return self.subdomains
            
        except Exception as e:
            if not self.silent:
                console.print(f"[bold red][-][/] Error while scanning MySSL: {str(e)}")
            return set()
