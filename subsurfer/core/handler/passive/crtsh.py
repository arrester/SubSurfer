#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import aiohttp
from typing import Set

class CrtshScanner:
    """Certificate Transparency logs scanner using crt.sh"""
    
    def __init__(self, domain: str, silent: bool = False):
        self.domain = domain
        self.base_url = "https://crt.sh"
        self.subdomains = set()
        self.silent = silent
        
    async def request(self, url: str) -> dict:
        """비동기 HTTP 요청 수행"""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                return {}
        
    async def scan(self) -> Set[str]:
        """Scan crt.sh for subdomains"""
        try:
            url = f"{self.base_url}/?q=%.{self.domain}&output=json"
            
            data = await self.request(url)
            if not data:
                return set()
                
            for entry in data:
                try:
                    name = entry.get('name_value', '')
                    # Handle wildcard certs
                    if '*' in name:
                        continue
                    if name.endswith(f".{self.domain}"):
                        self.subdomains.add(name.lower())
                except:
                    continue
                    
            return self.subdomains
            
        except:
            return set()