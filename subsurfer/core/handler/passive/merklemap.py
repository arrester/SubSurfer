#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import aiohttp
from typing import Set
from rich.console import Console

console = Console()

class MerkleMapScanner:
    """MerkleMap API를 통한 서브도메인 스캐너"""
    
    def __init__(self, domain: str, silent: bool = False):
        self.domain = domain
        self.base_url = "https://api.merklemap.com/v1-webui/search-noauth"
        self.subdomains = set()
        self.silent = silent
        
    async def scan(self) -> Set[str]:
        try:
            params = {
                'query': f'*.{self.domain}',
                'page': 0
            }
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
                "Accept": "*/*",
                "Origin": "https://www.merklemap.com",
                "Referer": "https://www.merklemap.com/"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params, headers=headers, ssl=False) as response:
                    if response.status != 200:
                        return set()
                        
                    data = await response.json()
                    
                    if 'results' in data and isinstance(data['results'], list):
                        for entry in data['results']:
                            hostname = entry.get('hostname', '')
                            subject_cn = entry.get('subject_common_name', '')
                            
                            for name in [hostname, subject_cn]:
                                if not name:
                                    continue
                                    
                                name = name.replace('*.', '')
                                
                                if name.endswith(f".{self.domain}") or name == self.domain:
                                    self.subdomains.add(name.lower())
                            
            return self.subdomains
            
        except Exception as e:
            if not self.silent:
                console.print(f"[bold red][-][/] Error while scanning PentestTools: {str(e)}")
            return set()