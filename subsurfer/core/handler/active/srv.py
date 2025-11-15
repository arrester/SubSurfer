#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SRV 스캐너 모듈 - SRV 레코드를 통한 서브도메인 수집
"""

import asyncio
import dns.resolver
from typing import Set
from rich.console import Console

console = Console()

class SRVScanner:
    """SRV 스캐너 클래스"""
    
    def __init__(self, domain: str, silent: bool = False):
        """
        Args:
            domain (str): 대상 도메인
            silent (bool): 상태 메시지 출력 여부
        """
        self.domain = domain
        self.silent = silent
        self.subdomains = set()
        
        # SRV 레코드 목록
        self.srv_records = [
            "_afs3-kaserver._tcp", "_afs3-kaserver._udp", "_afs3-prserver._tcp",
            "_afs3-prserver._udp", "_afs3-vlserver._tcp", "_afs3-vlserver._udp",
            "_autodiscover._tcp", "_caldav._tcp", "_caldavs._tcp", "_carddav._tcp",
            "_carddavs._tcp", "_certificates._tcp", "_collab-edge._tls",
            "_ftp._tcp", "_gc._tcp", "_http._tcp", "_https._tcp", "_imap._tcp",
            "_imaps._tcp", "_jabber._tcp", "_ldap._tcp", "_ldaps._tcp",
            "_matrix._tcp", "_minecraft._tcp", "_sip._tcp", "_sips._tcp",
            "_smtp._tcp", "_ssh._tcp", "_xmpp-client._tcp", "_xmpp-server._tcp"
        ]

    async def scan(self) -> Set[str]:
        """
        SRV 스캔 수행
        
        Returns:
            Set[str]: 발견된 서브도메인 목록
        """
        try:
            for service in self.srv_records:
                try:
                    answers = dns.resolver.resolve(f"_{service}._tcp.{self.domain}", 'SRV')
                    for rdata in answers:
                        target = str(rdata.target).rstrip('.')
                        if target.endswith(self.domain):
                            self.subdomains.add(target)
                except:
                    continue
            return self.subdomains
            
        except Exception as e:
            if not self.silent:
                console.print(f"[bold red][-][/] Error in SRV scan: {str(e)}")
            return set()

async def main():
    """테스트용 메인 함수"""
    try:
        domain = "vulnweb.com"  # 테스트할 도메인
        scanner = SRVScanner(domain)
        results = await scanner.scan()
        
        print(f"\n[*] SRV 스캔으로 총 {len(results)}개의 서브도메인을 찾았습니다.")
        print("\n".join(sorted(results)))
        
    except Exception as e:
        print(f"메인 함수 실행 중 오류 발생: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
