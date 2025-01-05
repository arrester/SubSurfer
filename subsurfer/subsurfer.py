#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SubSurfer - Fast Web Bug Bounty Asset Identification Tool
"""

import sys
from subsurfer.core.cli.cli import print_banner, print_status
from subsurfer.core.cli.parser import parse_args
from subsurfer.core.controller.controller import SubSurferController

async def main():
    """메인 함수"""
    args = parse_args()
    
    if not args.target:
        print_status("대상 도메인을 지정해주세요.", "error")
        sys.exit(1)
        
    print_banner()
    print_status(f"대상 도메인: {args.target}", "info")
    
    # 컨트롤러 초기화 및 실행
    controller = SubSurferController(args.target)
    all_subdomains = await controller.collect_subdomains()
    
    # 결과 저장
    output_path = args.output or controller.get_output_path()
    results_dict = {
        'subdomains': all_subdomains,
        'web_services': [],
        'enabled_services': []
    }
    
    controller.save_results(results_dict, output_path)
    
    # 결과 출력
    output_mode = "web" if args.pipeweb else "sub" if args.pipesub else None
    controller.print_results(all_subdomains, output_mode, output_path)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
