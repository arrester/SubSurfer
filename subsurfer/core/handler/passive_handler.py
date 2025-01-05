#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
패시브 방식으로 서브도메인을 수집하는 핸들러 모듈
"""

import asyncio
from typing import Set
import sys
import os
from rich.console import Console

# 상위 디렉토리를 모듈 검색 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from subsurfer.core.handler.passive.crtsh import CrtshScanner
from subsurfer.core.handler.passive.abuseipdb import AbuseIPDBScanner
from subsurfer.core.handler.passive.anubisdb import AnubisDBScanner
from subsurfer.core.handler.passive.digitorus import DigitorusScanner
from subsurfer.core.handler.passive.bufferover import BufferOverScanner

console = Console()

class PassiveHandler:
    """패시브 서브도메인 수집을 처리하는 핸들러 클래스"""
    
    def __init__(self, domain: str):
        """
        Args:
            domain (str): 대상 도메인 (예: example.com)
        """
        self.domain = domain
        self.subdomains: Set[str] = set()
        
    async def collect(self) -> Set[str]:
        """
        여러 패시브 스캐너를 사용하여 서브도메인 수집
        
        Returns:
            Set[str]: 수집된 고유한 서브도메인 목록
        """
        try:
            # crt.sh 스캔
            try:
                console.print("[bold blue][*][/] [white]crt.sh 스캔 시작...[/]")
                crtsh = CrtshScanner(self.domain)
                crtsh_results = await crtsh.scan()
                self.subdomains.update(crtsh_results)
                console.print(f"[bold green][+][/] [white]crt.sh 스캔 완료: {len(crtsh_results)}개 발견[/]")
            except Exception as e:
                console.print(f"[bold red][-][/] [white]crt.sh 스캔 중 오류 발생: {str(e)}[/]")
            
            # AbuseIPDB 스캔
            try:
                console.print("[bold blue][*][/] [white]AbuseIPDB 스캔 시작...[/]")
                abuseipdb = AbuseIPDBScanner(self.domain)
                abuseipdb_results = abuseipdb.scan()
                self.subdomains.update(abuseipdb_results)
                console.print(f"[bold green][+][/] [white]AbuseIPDB 스캔 완료: {len(abuseipdb_results)}개 발견[/]")
            except Exception as e:
                console.print(f"[bold red][-][/] [white]AbuseIPDB 스캔 중 오류 발생: {str(e)}[/]")

            # AnubisDB 스캔
            try:
                console.print("[bold blue][*][/] [white]AnubisDB 스캔 시작...[/]")
                anubisdb = AnubisDBScanner(self.domain)
                anubisdb_results = await anubisdb.scan()
                self.subdomains.update(anubisdb_results)
                console.print(f"[bold green][+][/] [white]AnubisDB 스캔 완료: {len(anubisdb_results)}개 발견[/]")
            except Exception as e:
                console.print(f"[bold red][-][/] [white]AnubisDB 스캔 중 오류 발생: {str(e)}[/]")

            # Digitorus 스캔
            try:
                console.print("[bold blue][*][/] [white]Digitorus 스캔 시작...[/]")
                digitorus = DigitorusScanner(self.domain)
                digitorus_results = await digitorus.scan()
                self.subdomains.update(digitorus_results)
                console.print(f"[bold green][+][/] [white]Digitorus 스캔 완료: {len(digitorus_results)}개 발견[/]")
            except Exception as e:
                console.print(f"[bold red][-][/] [white]Digitorus 스캔 중 오류 발생: {str(e)}[/]")

            # BufferOver 스캔
            try:
                console.print("[bold blue][*][/] [white]BufferOver 스캔 시작...[/]")
                bufferover = BufferOverScanner(self.domain)
                bufferover_results = await bufferover.scan()
                self.subdomains.update(bufferover_results)
                console.print(f"[bold green][+][/] [white]BufferOver 스캔 완료: {len(bufferover_results)}개 발견[/]")
            except Exception as e:
                console.print(f"[bold red][-][/] [white]BufferOver 스캔 중 오류 발생: {str(e)}[/]")
                
            return self.subdomains
            
        except Exception as e:
            console.print(f"[bold red][-][/] [white]서브도메인 수집 중 오류 발생: {str(e)}[/]")
            return set()

async def main():
    """테스트용 메인 함수"""
    try:
        domain = "verily.com"
        handler = PassiveHandler(domain)
        results = await handler.collect()
        
        print(f"\n[*] 총 {len(results)}개의 서브도메인을 찾았습니다.")
        print("\n".join(sorted(results)))
        
    except Exception as e:
        print(f"메인 함수 실행 중 오류 발생: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
