#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
액티브 방식으로 서브도메인을 수집하는 핸들러 모듈
"""

import asyncio
import sys
import os
from typing import Set
from rich.console import Console

# 상위 디렉토리를 모듈 검색 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from subsurfer.core.handler.active.zone import ZoneScanner
from subsurfer.core.handler.active.srv import SRVScanner 
from subsurfer.core.handler.active.sweep import SweepScanner

console = Console()

class ActiveHandler:
    """액티브 서브도메인 수집을 처리하는 핸들러 클래스"""
    
    def __init__(self, domain: str):
        """
        Args:
            domain (str): 대상 도메인 (예: example.com)
        """
        self.domain = domain
        self.subdomains: Set[str] = set()
        
    async def collect(self) -> Set[str]:
        """서브도메인 수집 실행"""
        try:
            # 모든 스캐너 초기화
            scanners = [
                ('DNS 존 전송', ZoneScanner(self.domain)),
                ('SRV 레코드', SRVScanner(self.domain)),
                ('리버스 DNS Sweep', SweepScanner(self.domain))
            ]
            
            # 동시 실행할 최대 작업 수 제한
            semaphore = asyncio.Semaphore(2)  # DNS 쿼리이므로 2개로 제한
            
            async def run_scanner_with_semaphore(name: str, scanner) -> Set[str]:
                """세마포어를 사용한 스캐너 실행"""
                async with semaphore:
                    try:
                        console.print(f"[bold blue][*][/] [white]{name} 스캔 시작...[/]")
                        results = await scanner.scan()
                        console.print(f"[bold green][+][/] [white]{name} 스캔 완료: {len(results)}개 발견[/]")
                        return results
                    except Exception as e:
                        console.print(f"[bold red][-][/] [white]{name} 스캔 중 오류 발생: {str(e)}[/]")
                        return set()

            # 모든 스캐너 동시 실행
            tasks = [run_scanner_with_semaphore(name, scanner) for name, scanner in scanners]
            results = await asyncio.gather(*tasks)
            
            # 결과 취합
            for result in results:
                self.subdomains.update(result)
                
            return self.subdomains
            
        except Exception as e:
            console.print(f"[bold red][-][/] [white]서브도메인 수집 중 오류 발생: {str(e)}[/]")
            return set()

async def main():
    """테스트용 메인 함수"""
    try:
        domain = "verily.com"
        handler = ActiveHandler(domain)
        results = await handler.collect()
        
        console.print(f"\n[bold green][*] 총 {len(results)}개의 서브도메인을 찾았습니다.[/]")
        for subdomain in sorted(results):
            console.print(f"[cyan]{subdomain}[/]")
        
    except Exception as e:
        console.print(f"[bold red][-] 메인 함수 실행 중 오류 발생: {str(e)}[/]")

if __name__ == "__main__":
    asyncio.run(main())
