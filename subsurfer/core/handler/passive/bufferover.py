#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import aiohttp
from typing import Set
import os
import yaml
import json

class BufferOverScanner:
    """BufferOver API를 사용한 서브도메인 스캐너"""
    
    def __init__(self, domain: str):
        self.domain = domain
        self.base_url = "https://tls.bufferover.run"
        self.subdomains = set()
        self.api_key = self._load_api_key()
        
    def _load_api_key(self) -> str:
        """config.yaml에서 API 키 로드"""
        try:
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                                     'config', 'config.yaml')
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                return config.get('bufferover', [''])[0]
        except:
            return ''
            
    async def request(self, url: str) -> dict:
        """비동기 HTTP 요청 수행"""
        headers = {
            'x-api-key': self.api_key
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response_text = await response.text()
                
                # JSON 파싱 시도
                try:
                    return json.loads(response_text)
                except json.JSONDecodeError:
                    # 일반 텍스트 응답인 경우
                    if response.status == 200:
                        lines = response_text.strip().split('\n')
                        return {'Results': lines}
                    return {}
                
    async def scan(self) -> Set[str]:
        """BufferOver API를 통한 서브도메인 스캔"""
        try:
            if not self.api_key:
                return set()
                
            url = f"{self.base_url}/dns?q=.{self.domain}"
            data = await self.request(url)
            
            # Results 데이터 처리
            if data and isinstance(data.get('Results'), list):
                for record in data['Results']:
                    try:
                        if isinstance(record, str):
                            parts = record.split(',')
                            if len(parts) >= 4:  # IP,hash,empty,domain 형식 확인
                                subdomain = parts[-1].strip().lower()  # 마지막 부분이 도메인
                                # *. 로 시작하는 와일드카드 도메인 처리
                                if subdomain.startswith('*.'):
                                    subdomain = subdomain[2:]
                                if subdomain.endswith(f".{self.domain}") or subdomain == self.domain:
                                    self.subdomains.add(subdomain)
                            elif len(parts) == 1:  # 단일 도메인 형식인 경우
                                subdomain = parts[0].strip().lower()
                                if subdomain.endswith(f".{self.domain}") or subdomain == self.domain:
                                    self.subdomains.add(subdomain)
                    except Exception as e:
                        print(f"레코드 처리 중 오류 발생: {str(e)}")
                        continue
                        
            return self.subdomains
            
        except Exception as e:
            print(f"BufferOver 스캔 중 오류 발생: {str(e)}")
            return set()

if __name__ == "__main__":
    import asyncio
    
    async def main():
        domain = "verily.com"
        scanner = BufferOverScanner(domain)
        subdomains = await scanner.scan()
        
        print(f"\n총 {len(subdomains)}개의 서브도메인을 찾았습니다.")
        if subdomains:
            print("\n발견된 서브도메인:")
            print("\n".join(sorted(subdomains)))
            
    asyncio.run(main())
