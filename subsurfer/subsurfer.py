#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SubSurfer - Fast Web Bug Bounty Asset Identification Tool
"""

import sys
from subsurfer.core.cli.cli import print_banner, print_status, print_usage
from subsurfer.core.cli.parser import parse_args
from subsurfer.core.controller.controller import SubSurferController

async def main():
    """메인 함수"""
    args = parse_args()
    
    # 배너는 항상 출력
    print_banner()
    
    if not args.target:
        print_usage()  # 사용법 출력
        print_status("대상 도메인을 지정해주세요.", "error")
        sys.exit(1)
        
    print_status(f"대상 도메인: {args.target}", "info")
    
    # 컨트롤러 초기화 및 실행
    controller = SubSurferController(
        target=args.target,
        verbose=args.verbose,
        active=args.active
    )
    
    if args.active:
        print_status("액티브 스캔 모드가 활성화되었습니다.", "warning")
    
    # 서브도메인 수집
    all_subdomains = await controller.collect_subdomains()
    
    # 포트 범위 설정
    ports = None
    if args.default_ports:
        ports = controller.parse_ports()
    elif args.port:
        ports = controller.parse_ports(args.port)
        
    # 웹 서비스 스캔
    web_services = await controller.scan_web_services(all_subdomains, ports)
    
    # 결과 저장
    output_path = args.output or controller.get_output_path()
    results_dict = {
        'subdomains': all_subdomains,
        'web_services': web_services.get('web_services', {}),
        'web_servers': web_services.get('web_servers', set()),
        'enabled_services': web_services.get('enabled_services', set()),
        'all_urls': web_services.get('all_urls', {})
    }
    
    controller.save_results(results_dict, output_path)
    
    # 결과 출력
    output_mode = "web" if args.pipeweb else "sub" if args.pipesub else None
    controller.print_results(results_dict, output_mode, output_path)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
