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
from subsurfer.core.handler.passive.urlscan import UrlscanScanner
from subsurfer.core.handler.passive.alienvault import AlienVaultScanner
from subsurfer.core.handler.passive.hackertarget import HackerTargetScanner
from subsurfer.core.handler.passive.myssl import MySSLScanner
from subsurfer.core.handler.passive.shrewdeye import ShrewdEyeScanner
from subsurfer.core.handler.passive.subdomaincenter import SubdomainCenterScanner
from subsurfer.core.handler.passive.webarchive import WebArchiveScanner
from subsurfer.core.handler.passive.dnsarchive import DNSArchiveScanner

console = Console()

class PassiveHandler:
    """패시브 서브도메인 수집을 처리하는 핸들러 클래스"""
    
    def __init__(self, target: str, silent: bool = False):
        """
        Args:
            target (str): 대상 도메인 (예: example.com)
            silent (bool): 상태 메시지 출력 여부
        """
        self.target = target
        self.silent = silent
        self.subdomains: Set[str] = set()
        self.scanners = [
            ('crt.sh', CrtshScanner(self.target, self.silent)),
            ('AbuseIPDB', AbuseIPDBScanner(self.target, self.silent)),
            ('AnubisDB', AnubisDBScanner(self.target, self.silent)),
            ('Digitorus', DigitorusScanner(self.target, self.silent)),
            ('BufferOver', BufferOverScanner(self.target, self.silent)),
            ('Urlscan', UrlscanScanner(self.target, self.silent)),
            ('AlienVault', AlienVaultScanner(self.target, self.silent)),
            ('HackerTarget', HackerTargetScanner(self.target, self.silent)),
            ('MySSL', MySSLScanner(self.target, self.silent)),
            ('ShrewdEye', ShrewdEyeScanner(self.target, self.silent)),
            ('SubdomainCenter', SubdomainCenterScanner(self.target, self.silent)),
            ('WebArchive', WebArchiveScanner(self.target, self.silent)),
            ('DNS Archive', DNSArchiveScanner(self.target, self.silent)),
        ]
        
    async def collect(self) -> Set[str]:
        """서브도메인 수집"""
        results = set()
        for name, scanner in self.scanners:
            try:
                if not self.silent:
                    console.print(f"[blue][*][/] {name} Start Scan...")
                subdomains = await scanner.scan()
                results.update(subdomains)
                if not self.silent:
                    console.print(f"[green][+][/] {name} Scan completed: {len(subdomains)} found")
            except Exception as e:
                if not self.silent:
                    console.print(f"[red][-][/] {name} Error: {str(e)}")
                
        self.subdomains.update(results)
        return self.subdomains

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
