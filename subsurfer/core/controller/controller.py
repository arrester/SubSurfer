#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SubSurfer Controller Module
"""

import asyncio
from typing import Set, Dict, Any
from datetime import datetime
import os

from subsurfer.core.cli.cli import console, print_status
from subsurfer.core.handler.passive_handler import PassiveHandler
from subsurfer.core.handler.active_handler import ActiveHandler

class SubSurferController:
    """SubSurfer 메인 컨트롤러"""
    
    def __init__(self, target: str):
        """
        Args:
            target (str): 대상 도메인 (예: example.com)
        """
        self.target = target
        self.passive_handler = PassiveHandler(target)
        self.active_handler = ActiveHandler(target)
        
    def get_output_path(self) -> str:
        """결과 저장 경로 생성"""
        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M')
        filename = f"subsurfer_{self.target}_{timestamp}.txt"
        
        results_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'results')
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
            
        return os.path.join(results_dir, filename)
        
    def save_results(self, results: Dict[str, Any], output_path: str) -> None:
        """결과를 파일에 저장"""
        with open(output_path, 'w') as f:
            f.write("SubSurfer - subdomain\n")
            for subdomain in sorted(results['subdomains']):
                f.write(f"{subdomain}\n")
            f.write("\n")
            
            if results.get('web_services'):
                f.write("SubSurfer - subdomain-webserver\n")
                for service in results['web_services']:
                    f.write(f"{service}\n")
                f.write("\n")
                
            if results.get('enabled_services'):
                f.write("SubSurfer - subdomain-notweb-but-enable\n")
                for service in results['enabled_services']:
                    f.write(f"{service}\n")
                    
    async def collect_subdomains(self) -> Set[str]:
        """서브도메인 수집 실행"""
        results = await asyncio.gather(
            self.passive_handler.collect(),
            self.active_handler.collect()
        )
        return results[0].union(results[1])
        
    def print_results(self, subdomains: Set[str], output_mode: str = None, output_path: str = None) -> None:
        """결과 출력"""
        if output_mode == "web":
            for subdomain in sorted(subdomains):
                console.print(f"[cyan]https://{subdomain}[/]")
        elif output_mode == "sub":
            for subdomain in sorted(subdomains):
                console.print(f"[cyan]{subdomain}[/]")
        else:
            print_status(f"\n총 {len(subdomains)}개의 서브도메인을 찾았습니다.", "success")
            if output_path:
                print_status(f"결과가 {output_path}에 저장되었습니다.", "success")
