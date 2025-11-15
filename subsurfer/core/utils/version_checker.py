#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SubSurfer 버전 체크 유틸리티 모듈
"""

import asyncio
import aiohttp
import re
import sys
import importlib.metadata
from bs4 import BeautifulSoup
from rich.console import Console
from concurrent.futures import ThreadPoolExecutor

console = Console()

# 현재 버전 (subsurfer/__init__.py에서 가져올 수 있음)
def get_current_version():
    """현재 설치된 버전 반환"""
    try:
        # pkg_resources 대신 importlib.metadata 사용
        return importlib.metadata.version("subsurfer")
    except importlib.metadata.PackageNotFoundError:
        # 개발 환경에서 실행 중일 때는 __init__.py에서 버전 가져오기
        try:
            from subsurfer import __version__
            return __version__
        except (ImportError, AttributeError):
            return "0.3"  # 기본 버전

def run_async_check():
    """비동기 함수를 동기적으로 실행하는 래퍼"""
    try:
        # 별도의 스레드에서 새 이벤트 루프로 비동기 함수 실행
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(_run_version_check)
            return future.result(timeout=1)
    except Exception:
        # 어떤 오류가 발생하든 기본값 반환
        return (True, get_current_version(), None)

def _run_version_check():
    """별도 스레드에서 비동기 루프 실행"""
    # 새 이벤트 루프 생성
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        # 비동기 함수 실행
        result = loop.run_until_complete(check_latest_version())
        # 이벤트 루프 정리
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        return result
    except Exception:
        if not loop.is_closed():
            loop.close()
        # 오류 발생 시 기본값 반환
        return (True, get_current_version(), None)

async def check_latest_version():
    """
    GitHub 태그 페이지에서 최신 버전 확인
    
    Returns:
        tuple: (최신 버전 여부, 현재 버전, 최신 버전)
    """
    current_version = get_current_version()
    latest_version = None
    is_latest = True
    
    # 개발 환경에서는 항상 최신 버전으로 간주
    if "dev" in current_version:
        return (True, current_version, current_version)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://github.com/arrester/SubSurfer/tags",
                timeout=1  # 타임아웃 단축
            ) as response:
                if response.status == 200:
                    html_content = await response.text()
                    
                    soup = BeautifulSoup(html_content, 'html.parser')
                    
                    # 태그 목록에서 최신 버전 찾기
                    # 페이지의 첫 번째 태그가 가장 최신 버전
                    latest_tag_element = soup.select_one('h2.f4.d-inline a.Link--primary')
                    
                    if latest_tag_element:
                        latest_version = latest_tag_element.text.strip()
                        if latest_version.startswith('v'):
                            latest_version = latest_version[1:]  # 'v' 접두사 제거
                        
                        if latest_version and latest_version != current_version:
                            try:
                                # 버전 비교 (x.y.z 형식 가정)
                                current_parts = [int(x) for x in current_version.split(".")]
                                latest_parts = [int(x) for x in latest_version.split(".")]
                                
                                # 버전 비교
                                for i in range(min(len(current_parts), len(latest_parts))):
                                    if latest_parts[i] > current_parts[i]:
                                        is_latest = False
                                        break
                                    elif current_parts[i] > latest_parts[i]:
                                        break
                                
                                # 길이가 다른 경우 (예: 1.0 vs 1.0.1)
                                if is_latest and len(latest_parts) > len(current_parts):
                                    is_latest = False
                            except (ValueError, TypeError):
                                # 버전 형식이 예상과 다를 경우 단순 문자열 비교
                                is_latest = (current_version >= latest_version)
    except Exception:
        # 연결 오류가 발생한 경우 현재 버전이 최신이라고 가정
        pass
    
    return (is_latest, current_version, latest_version)

def get_version_notification():
    """버전 알림 메시지 생성"""
    try:
        is_latest, current_version, latest_version = run_async_check()
        
        if not is_latest and latest_version:
            return f"Version Notice: Your SubSurfer version ({current_version}) is not the latest ({latest_version})."
        return None
    except Exception:
        return None 