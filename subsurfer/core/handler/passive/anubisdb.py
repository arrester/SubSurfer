#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AnubisDB API를 사용하여 서브도메인을 수집하는 스캐너 모듈
"""

import aiohttp
from typing import Set

class AnubisDBScanner:
    """AnubisDB API를 통한 서브도메인 스캐너"""
    
    def __init__(self, domain: str, silent: bool = False):
        """
        Args:
            domain (str): 대상 도메인 (예: example.com)
        """
        self.domain = domain
        self.base_url = "https://jonlu.ca/anubis/subdomains"
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
        """
        AnubisDB API를 통해 서브도메인 스캔 수행
        
        Returns:
            Set[str]: 수집된 고유한 서브도메인 목록
        """
        try:
            url = f"{self.base_url}/{self.domain}"
            
            data = await self.request(url)
            if not data:
                return set()
                
            # API 응답에서 서브도메인 추출
            for subdomain in data:
                if isinstance(subdomain, str):
                    if subdomain.endswith(f".{self.domain}"):
                        self.subdomains.add(subdomain.lower())
                        
            return self.subdomains
            
        except Exception as e:
            if not self.silent:
                print(f"Error while scanning AnubisDB: {str(e)}")
            return set()

if __name__ == "__main__":
    import asyncio
    
    async def main():
        """테스트용 메인 함수"""
        try:
            domain = "vulnweb.com"
            scanner = AnubisDBScanner(domain)
            results = await scanner.scan()
            
            print(f"\n[*] 총 {len(results)}개의 서브도메인을 찾았습니다.")
            print("\n".join(sorted(results)))
            
        except Exception as e:
            print(f"메인 함수 실행 중 오류 발생: {str(e)}")
            
    asyncio.run(main())
