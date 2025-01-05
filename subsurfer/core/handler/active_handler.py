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
        """
        여러 액티브 스캐너를 사용하여 서브도메인 수집
        
        Returns:
            Set[str]: 수집된 고유한 서브도메인 목록
        """
        try:
            # DNS 존 전송 스캔
            try:
                console.print("[bold blue][*][/] [white]DNS 존 전송 스캔 시작...[/]")
                zone_scanner = ZoneScanner(self.domain)
                zone_results = await zone_scanner.scan()
                self.subdomains.update(zone_results)
                console.print(f"[bold green][+][/] [white]DNS 존 전송 스캔 완료: {len(zone_results)}개 발견[/]")
            except Exception as e:
                console.print(f"[bold red][-][/] [white]DNS 존 전송 스캔 중 오류 발생: {str(e)}[/]")
            
            # SRV 레코드 스캔
            try:
                console.print("[bold blue][*][/] [white]SRV 레코드 스캔 시작...[/]")
                srv_scanner = SRVScanner(self.domain)
                srv_results = await srv_scanner.scan()
                self.subdomains.update(srv_results)
                console.print(f"[bold green][+][/] [white]SRV 레코드 스캔 완료: {len(srv_results)}개 발견[/]")
            except Exception as e:
                console.print(f"[bold red][-][/] [white]SRV 레코드 스캔 중 오류 발생: {str(e)}[/]")

            # 리버스 DNS Sweep 스캔
            try:
                console.print("[bold blue][*][/] [white]리버스 DNS Sweep 스캔 시작...[/]")
                sweep_scanner = SweepScanner(self.domain)
                sweep_results = await sweep_scanner.scan()
                self.subdomains.update(sweep_results)
                console.print(f"[bold green][+][/] [white]리버스 DNS Sweep 스캔 완료: {len(sweep_results)}개 발견[/]")
            except Exception as e:
                console.print(f"[bold red][-][/] [white]리버스 DNS Sweep 스캔 중 오류 발생: {str(e)}[/]")
                
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
