#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FreecampDev API를 사용하여 서브도메인을 수집하는 스캐너 모듈
"""

import aiohttp
import json
from typing import Set
from rich.console import Console

console = Console()

class FreecampDevScanner:
    """FreecampDev API를 통한 서브도메인 스캐너"""
    
    def __init__(self, domain: str, silent: bool = False):
        """
        Args:
            domain (str): 대상 도메인 (예: example.com)
            silent (bool): 출력 메시지 표시 여부
        """
        self.domain = domain
        self.base_url = "https://freecamp.dev/api/tools/network/subdomains/"
        self.subdomains = set()
        self.silent = silent
        
    async def scan(self) -> Set[str]:
        """
        FreecampDev API를 통해 서브도메인 스캔 수행
        
        Returns:
            Set[str]: 수집된 고유한 서브도메인 목록
        """
        try:
            # POST 요청 데이터
            data = {"domain": self.domain}
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.base_url, data=data, ssl=False) as response:
                    if response.status != 200:
                        if not self.silent:
                            console.print(f"[bold red][-][/] FreecampDev 요청 실패: HTTP {response.status}")
                        return self.subdomains
                        
                    json_content = await response.text()
                    
                    # JSON 파싱
                    try:
                        data = json.loads(json_content)
                        results = data.get("results", [])
                        
                        # 결과 처리
                        for result in results:
                            subdomain = result.get("subdomain", "")
                            if subdomain and subdomain.endswith(f".{self.domain}"):
                                self.subdomains.add(subdomain.lower())
                    except json.JSONDecodeError as e:
                        if not self.silent:
                            console.print(f"[bold red][-][/] JSON 파싱 오류: {str(e)}")
                        
            return self.subdomains
            
        except Exception as e:
            if not self.silent:
                console.print(f"[bold red][-][/] Error while scanning FreecampDev: {str(e)}")
            return self.subdomains

if __name__ == "__main__":
    import asyncio
    
    async def main():
        """테스트용 메인 함수"""
        try:
            domain = "vulnweb.com"
            scanner = FreecampDevScanner(domain)
            results = await scanner.scan()
            
            console.print(f"\n[bold green][*] 총 {len(results)}개의 서브도메인을 찾았습니다.[/]")
            if results:
                for subdomain in sorted(results):
                    console.print(f"[cyan]{subdomain}[/]")
            
        except Exception as e:
            console.print(f"[bold red][-] 메인 함수 실행 중 오류 발생: {str(e)}[/]")
            
    asyncio.run(main())