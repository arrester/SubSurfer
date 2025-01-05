#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sweep 스캐너 모듈 - 리버스 DNS 스캔을 통한 서브도메인 수집
"""

import asyncio
import dns.resolver
import ipaddress
from typing import Set

class SweepScanner:
    """Sweep 스캐너 클래스"""
    
    def __init__(self, domain: str):
        """
        Args:
            domain (str): 대상 도메인
        """
        self.domain = domain
        self.subdomains: Set[str] = set()

    async def reverse_lookup(self, ip: str) -> Set[str]:
        """
        IP 주소에 대한 리버스 DNS 조회 수행
        
        Args:
            ip (str): 조회할 IP 주소
            
        Returns:
            Set[str]: 발견된 서브도메인 목록
        """
        try:
            answers = dns.resolver.resolve_address(ip)
            domains = set()
            for rdata in answers:
                name = str(rdata.target).rstrip('.')
                if name.endswith(self.domain):
                    domains.add(name)
            return domains
        except:
            return set()

    async def get_domain_ips(self) -> Set[str]:
        """
        도메인의 IP 주소 조회
        
        Returns:
            Set[str]: IP 주소 목록
        """
        try:
            ips = set()
            # A 레코드 조회
            try:
                answers = dns.resolver.resolve(self.domain, 'A')
                ips.update([str(rdata) for rdata in answers])
            except:
                pass
                
            # AAAA 레코드 조회
            try:
                answers = dns.resolver.resolve(self.domain, 'AAAA') 
                ips.update([str(rdata) for rdata in answers])
            except:
                pass
                
            return ips
        except:
            return set()

    async def scan(self) -> Set[str]:
        """
        Sweep 스캔 수행 - IP 주소 범위에 대한 리버스 DNS 조회
        
        Returns:
            Set[str]: 발견된 서브도메인 목록
        """
        try:
            # 도메인의 IP 주소 조회
            ips = await self.get_domain_ips()
            
            # 각 IP 주소에 대해 리버스 DNS 조회
            for ip in ips:
                try:
                    # IP 주소를 기반으로 /24 범위 생성
                    ip_obj = ipaddress.ip_address(ip)
                    if isinstance(ip_obj, ipaddress.IPv4Address):
                        network = ipaddress.ip_network(f"{ip_obj}/24", strict=False)
                    else:
                        network = ipaddress.ip_network(f"{ip_obj}/120", strict=False)
                        
                    # 범위 내 각 IP에 대해 리버스 DNS 조회
                    for addr in network:
                        domains = await self.reverse_lookup(str(addr))
                        self.subdomains.update(domains)
                except:
                    continue
                    
            return self.subdomains
            
        except Exception as e:
            print(f"Sweep 스캔 중 오류: {str(e)}")
            return set()

async def main():
    """테스트용 메인 함수"""
    try:
        domain = "verily.com"  # 테스트할 도메인
        scanner = SweepScanner(domain)
        results = await scanner.scan()
        
        print(f"\n[*] Sweep 스캔으로 총 {len(results)}개의 서브도메인을 찾았습니다.")
        print("\n".join(sorted(results)))
        
    except Exception as e:
        print(f"메인 함수 실행 중 오류 발생: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
