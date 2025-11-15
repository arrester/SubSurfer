#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import aiohttp
import json
import os
from typing import Set, List, Dict
from rich.console import Console

console = Console()

class TakeoverHandler:
    """서브도메인 Takeover 취약점 탐지 핸들러"""
    
    def __init__(self, target: str, silent: bool = False):
        self.target = target
        self.silent = silent
        self.fingerprints = self._load_fingerprints()
        self.vulnerable_domains = []
        
    def _load_fingerprints(self) -> List[Dict]:
        """fingerprints.json 파일 로드"""
        try:
            fingerprints_path = os.path.join(
                os.path.dirname(__file__),
                'fingerprints.json'
            )
            with open(fingerprints_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            if not self.silent:
                console.print(f"[red][-][/] Error loading fingerprints: {str(e)}")
            return []
    
    async def check_cname(self, domain: str) -> str:
        """DNS CNAME 레코드 조회"""
        try:
            import aiodns
            resolver = aiodns.DNSResolver()
            result = await resolver.query(domain, 'CNAME')
            return result.cname if result else None
        except:
            return None
    
    async def check_http_response(self, domain: str) -> tuple:
        """HTTP 응답 확인"""
        try:
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                for scheme in ['https', 'http']:
                    try:
                        url = f"{scheme}://{domain}"
                        async with session.get(url, ssl=False, allow_redirects=True) as response:
                            body = await response.text()
                            return response.status, body
                    except:
                        continue
            return None, None
        except:
            return None, None
    
    def match_fingerprint(self, cname: str, status: int, body: str) -> Dict:
        """fingerprint 매칭 확인"""
        if not cname or not body:
            return None
            
        for fp in self.fingerprints:
            cname_match = any(cn in cname for cn in fp.get('cname', []))
            
            if cname_match:
                status_match = status in fp.get('http_status', [])
                
                fingerprint_match = any(
                    pattern in body 
                    for pattern in fp.get('fingerprint', [])
                )
                
                if status_match and fingerprint_match:
                    return fp
        
        return None
    
    async def check_domain(self, domain: str) -> Dict:
        """개별 도메인 takeover 취약점 확인"""
        try:
            cname = await self.check_cname(domain)
            
            if not cname:
                return None
            
            status, body = await self.check_http_response(domain)
            
            if status is None:
                return None
            
            matched_fp = self.match_fingerprint(cname, status, body)
            
            if matched_fp:
                return {
                    'domain': domain,
                    'cname': cname,
                    'service': matched_fp['service'],
                    'status': status,
                    'vulnerable': True
                }
            
            return None
            
        except Exception as e:
            return None
    
    async def scan(self, subdomains: Set[str]) -> List[Dict]:
        """모든 서브도메인 takeover 스캔"""
        if not self.silent:
            console.print(f"[blue][*][/] Starting Takeover Detection Scan for {len(subdomains)} subdomains...")
        
        tasks = []
        for subdomain in subdomains:
            tasks.append(self.check_domain(subdomain))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        vulnerable = []
        for result in results:
            if result and isinstance(result, dict) and result.get('vulnerable'):
                vulnerable.append(result)
                if not self.silent:
                    console.print(
                        f"[red][!][/] VULNERABLE: {result['domain']} "
                        f"-> {result['service']} (CNAME: {result['cname']})"
                    )
        
        self.vulnerable_domains = vulnerable
        
        if not self.silent:
            console.print(f"[green][+][/] Takeover Scan completed: {len(vulnerable)} vulnerable domains found")
        
        return vulnerable

