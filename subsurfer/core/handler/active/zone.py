#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DNS 스캐너 모듈 - DNS 존 전송 및 워킹을 통한 서브도메인 수집
"""

import asyncio
import dns.resolver
import dns.zone
from typing import Set, List

class ZoneScanner:
    """DNS 스캐너 클래스"""
    
    def __init__(self, domain: str):
        """
        Args:
            domain (str): 대상 도메인
        """
        self.domain = domain
        self.subdomains: Set[str] = set()
        
    async def get_nameservers(self) -> List[str]:
        """도메인의 네임서버 주소 조회"""
        try:
            ns_records = dns.resolver.resolve(self.domain, 'NS')
            nameservers = []
            
            for ns in ns_records:
                # A 레코드로 IP 주소 조회
                try:
                    answers = dns.resolver.resolve(str(ns.target), 'A')
                    nameservers.extend([str(rdata) for rdata in answers])
                except:
                    pass
                    
                # AAAA 레코드로 IPv6 주소 조회    
                try:
                    answers = dns.resolver.resolve(str(ns.target), 'AAAA')
                    nameservers.extend([str(rdata) for rdata in answers])
                except:
                    pass
                    
            return nameservers
            
        except Exception as e:
            print(f"네임서버 조회 중 오류: {str(e)}")
            return []
            
    async def zone_transfer(self, nameserver: str):
        """
        DNS 존 전송 시도
        
        Args:
            nameserver (str): 네임서버 IP 주소
        """
        try:
            zone = dns.zone.from_xfr(dns.query.xfr(nameserver, self.domain))
            for name, node in zone.nodes.items():
                subdomain = str(name) + '.' + self.domain
                if subdomain.startswith('@'):
                    subdomain = self.domain
                self.subdomains.add(subdomain)
        except:
            pass
            
    async def scan(self) -> Set[str]:
        """
        DNS 스캔 수행 - 존 전송 및 워킹
        
        Returns:
            Set[str]: 발견된 서브도메인 목록
        """
        try:
            nameservers = await self.get_nameservers()
            
            # 각 네임서버에 대해 존 전송 시도
            for ns in nameservers:
                await self.zone_transfer(ns)
                
            return self.subdomains
            
        except Exception as e:
            print(f"DNS 스캔 중 오류: {str(e)}")
            return set()

async def main():
    """테스트용 메인 함수"""
    try:
        domain = "verily.com"  # 테스트할 도메인
        scanner = ZoneScanner(domain)
        results = await scanner.scan()
        
        print(f"\n[*] DNS 스캔으로 총 {len(results)}개의 서브도메인을 찾았습니다.")
        print("\n".join(sorted(results)))
        
    except Exception as e:
        print(f"메인 함수 실행 중 오류 발생: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
