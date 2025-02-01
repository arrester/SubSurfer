#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
웹 서비스 스캐너 모듈
"""
import asyncio
import aiohttp
from typing import Dict, Set, List, Tuple, Optional
from Wappalyzer import Wappalyzer, WebPage
import random
from rich.console import Console
import warnings
import socket
# Wappalyzer 경고 무시
warnings.filterwarnings('ignore', module='Wappalyzer')
console = Console()
class WebScanner:
    """웹 서비스 스캐너"""
    
    def __init__(self, domain: str, ports: List[int] = None, verbose: int = 0, silent: bool = False):
        """
        Args:
            domain (str): 대상 도메인
            ports (List[int]): 스캔할 포트 목록
            verbose (int): verbose 레벨
            silent (bool): 상태 메시지 출력 여부
        """
        self.domain = domain
        self.ports = ports  # 포트가 지정된 경우 그대로 사용
        self.default_ports = [80, 443]  # 기본 포트는 별도 저장
        self.verbose = verbose  # verbose 저장
        self.silent = silent  # silent 모드 저장
        self.wappalyzer = Wappalyzer.latest()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        ]
        self.web_servers = set()  # 웹 서버로 확인된 서브도메인
        self.enabled_services = set()  # 웹 서버는 아니지만 활성화된 서비스
        self.session = None  # aiohttp 세션
        self.all_urls = {}  # 포트 스캔으로 발견된 모든 URL 저장
        
    async def __aenter__(self):
        """비동기 컨텍스트 매니저 진입"""
        connector = aiohttp.TCPConnector(ssl=False)  # SSL 검증 비활성화
        self.session = aiohttp.ClientSession(connector=connector)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """비동기 컨텍스트 매니저 종료"""
        if self.session:
            await self.session.close()
            
    def _get_random_user_agent(self) -> str:
        """랜덤 User-Agent 반환"""
        return random.choice(self.user_agents)
        
    async def check_web_server(self, subdomain: str, port: int = None) -> Tuple[bool, str, Dict]:
        """웹 서버 여부 확인"""
        headers = {'User-Agent': self._get_random_user_agent()}
        protocols = ['https', 'http']
        
        for protocol in protocols:
            url = f"{protocol}://{subdomain}"
            if port and port not in [80, 443]:
                url = f"{url}:{port}"
                
            try:
                webpage = await WebPage.new_from_url_async(
                    url, 
                    verify=False, 
                    timeout=2,
                    aiohttp_client_session=self.session
                )
                analysis = self.wappalyzer.analyze_with_versions_and_categories(webpage)
                if port:  # 포트 스캔 결과 저장
                    self.all_urls[subdomain] = self.all_urls.get(subdomain, [])
                    self.all_urls[subdomain].append((url, port))
                return True, url, analysis
            except:
                continue
                
        return False, "", {}
        
    def _is_host_active(self, subdomain: str) -> bool:
        """호스트 활성화 여부 확인"""
        try:
            socket.gethostbyname(subdomain)
            return True
        except socket.gaierror:
            return False
            
    async def scan_subdomain(self, subdomain: str) -> Dict[str, Dict]:
        """서브도메인의 모든 포트에 대한 스캔"""
        web_services = {}
        scan_ports = self.ports if self.ports else self.default_ports
        
        if self.verbose and not self.silent:
            console.print(f"[bold blue][*][/] Scanning ports for {subdomain}: {scan_ports}")
        
        for port in scan_ports:
            is_web, url, analysis = await self.check_web_server(subdomain, port)
            if is_web:
                self.web_servers.add(subdomain)
                web_services[url] = analysis
                
        if not web_services and self._is_host_active(subdomain):
            self.enabled_services.add(subdomain)
            
        return web_services
        
    async def scan(self, subdomains: Set[str]) -> Dict[str, Dict]:
        """모든 서브도메인 스캔"""
        web_services = {}
        
        # 동시 실행할 최대 작업 수 제한
        semaphore = asyncio.Semaphore(10)  # 동시에 10개까지 실행
        
        async def scan_with_semaphore(subdomain: str):
            """세마포어를 사용한 스캔"""
            async with semaphore:
                try:
                    if not self.silent:
                        console.print(f"[bold blue][*][/] [white]Scanning: {subdomain}[/]")
                    return await self.scan_subdomain(subdomain)
                except Exception as e:
                    if not self.silent:
                        console.print(f"[bold red][-][/] [white]{subdomain} Error during scanning: {str(e)}[/]")
                    return {}
        
        # 모든 서브도메인에 대해 동시에 스캔 실행
        tasks = [scan_with_semaphore(subdomain) for subdomain in subdomains]
        results = await asyncio.gather(*tasks)
        
        # 결과 취합
        for result in results:
            if result:
                web_services.update(result)
                
        return {
            'web_services': web_services,
            'web_servers': self.web_servers,
            'enabled_services': self.enabled_services,
            'all_urls': self.all_urls  # 포트 스캔 결과 포함
        } 