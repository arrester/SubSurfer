#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SubSurfer - Fast Web Bug Bounty Asset Identification Tool
"""

import sys
import json
from subsurfer.core.cli.cli import print_banner, print_status, print_usage
from subsurfer.core.cli.parser import parse_args
from subsurfer.core.controller.controller import SubSurferController
from subsurfer.core.utils.version_checker import get_version_notification

async def main():
    """메인 함수"""
    # 파싱된 인자 가져오기
    args = parse_args()
    
    # 파이프라인 모드 확인
    is_pipeline = any([args.pipeweb, args.pipesub, args.pipeact, args.pipewsub, args.pipejson])
    
    # 배너 출력 (파이프라인 모드가 아닐 때)
    if not is_pipeline:
        print_banner()
    
    # 인자가 없을 때 (help 또는 --help 플래그를 포함하지 않는 경우)
    if len(sys.argv) == 1:
        print_usage()
        
        # 인자가 없을 때 타겟 도메인 필요 메시지 표시
        if not is_pipeline:
            print_status("Please specify the target domain.", "error")
            
            # 버전 알림을 맨 마지막에 표시
            version_notification = get_version_notification()
            if version_notification:
                print()
                print_status(version_notification, "warning")
        
        sys.exit(1)
    
    # 타겟 도메인이 지정되지 않았을 때 오류 메시지 출력
    if not args.target:
        if not is_pipeline:
            print_usage()
            print_status("Please specify the target domain.", "error")
            
            # 버전 알림을 맨 마지막에 표시
            version_notification = get_version_notification()
            if version_notification:
                print()
                print_status(version_notification, "warning")
                
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
    elif args.pipejson:
        output_mode = "json"
        
    if args.pipejson:
        json_results = {
            'subdomains': list(results_dict['subdomains']),
            'web_servers': list(results_dict['web_servers']),
            'enabled_services': list(results_dict['enabled_services']),
            'all_urls': {k: list(v) for k, v in results_dict['all_urls'].items()}
        }
        print(json.dumps(json_results, indent=None))
    else:
        controller.print_results(results_dict, output_mode, output_path)
    
    # 스캔 완료 후 버전 알림 출력 (파이프라인 모드가 아닐 때만)
    if not is_pipeline:
        version_notification = get_version_notification()
        if version_notification:
            print()
            print_status(version_notification, "warning")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
