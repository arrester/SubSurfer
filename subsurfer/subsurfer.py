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
    
    # 파이프라인 모드 확인
    is_pipeline = any([args.pipeweb, args.pipesub, args.pipeact, args.pipewsub])
    
    if not is_pipeline:
        print_banner()
    
    if not args.target:
        if not is_pipeline:
            print_usage()
            print_status("Please specify the target domain.", "error")
        sys.exit(1)
        
    if not is_pipeline:
        print_status(f"Target Domain: {args.target}", "info")
    
    # 컨트롤러 초기화 및 실행
    controller = SubSurferController(
        target=args.target,
        verbose=0 if is_pipeline else args.verbose,  # 파이프라인 모드에서는 verbose 비활성화
        active=args.active,
        silent=is_pipeline  # 파이프라인 모드에서는 silent 모드 활성화
    )
    
    if args.active and not is_pipeline:
        print_status("Active scan mode is enabled.", "warning")
    
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
    output_path = controller.get_output_path(args.output) if args.output else controller.get_output_path()
    results_dict = {
        'subdomains': all_subdomains,
        'web_services': web_services.get('web_services', {}),
        'web_servers': web_services.get('web_servers', set()),
        'enabled_services': web_services.get('enabled_services', set()),
        'all_urls': web_services.get('all_urls', {})
    }
    
    controller.save_results(results_dict, output_path)
    
    # 결과 출력 모드 설정
    output_mode = None
    if args.pipeweb:
        output_mode = "web"
    elif args.pipesub:
        output_mode = "sub"
    elif args.pipeact:
        output_mode = "act"
    elif args.pipewsub:
        output_mode = "wsub"
        
    controller.print_results(results_dict, output_mode, output_path)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
