import pytest
import asyncio
from typing import Set
from subsurfer.core.handler.active_handler import ActiveHandler
from subsurfer.core.handler.active.zone import ZoneScanner
from subsurfer.core.handler.active.srv import SRVScanner
from subsurfer.core.handler.active.sweep import SweepScanner

TEST_DOMAIN = "example.com"

@pytest.fixture
def active_handler():
    return ActiveHandler(TEST_DOMAIN)

@pytest.mark.asyncio
async def test_zone_scanner():
    """Zone Transfer Scanner Test"""
    scanner = ZoneScanner(TEST_DOMAIN)
    results = await scanner.scan()
    assert isinstance(results, set)
    assert all(isinstance(subdomain, str) for subdomain in results)
    assert all(TEST_DOMAIN in subdomain for subdomain in results)

@pytest.mark.asyncio
async def test_srv_scanner():
    """SRV Record Scanner Test"""
    scanner = SRVScanner(TEST_DOMAIN)
    results = await scanner.scan()
    assert isinstance(results, set)
    assert all(isinstance(subdomain, str) for subdomain in results)
    assert all(TEST_DOMAIN in subdomain for subdomain in results)

@pytest.mark.asyncio
async def test_sweep_scanner():
    """IP Sweep Scanner Test"""
    scanner = SweepScanner(TEST_DOMAIN)
    results = await scanner.scan()
    assert isinstance(results, set)
    assert all(isinstance(subdomain, str) for subdomain in results)
    assert all(TEST_DOMAIN in subdomain for subdomain in results)

@pytest.mark.asyncio
async def test_active_handler_collect(active_handler):
    """ActiveHandler collect Method Test"""
    results = await active_handler.collect()
    
    # Basic Check
    assert isinstance(results, set)
    
    if len(results) > 0:
        # 모든 결과가 문자열이고 대상 도메인을 포함하는지 검증
        assert all(isinstance(subdomain, str) for subdomain in results)
        assert all(TEST_DOMAIN in subdomain for subdomain in results)

@pytest.mark.asyncio
async def test_active_handler_error_handling(active_handler):
    """ActiveHandler Error Test"""
    # 잘못된 도메인으로 테스트
    handler = ActiveHandler("this-domain-does-not-exist.com")
    results = await handler.collect()
    
    # 에러가 발생해도 빈 set을 반환해야 함
    assert isinstance(results, set)
    assert len(results) == 0

@pytest.mark.asyncio
async def test_active_handler_concurrent_scans(active_handler):
    """ActiveHandler concurrent Test"""
    # 여러 번의 동시 스캔 실행
    tasks = [active_handler.collect() for _ in range(3)]
    results = await asyncio.gather(*tasks)
    
    # 모든 결과가 set이어야 함
    assert all(isinstance(result, set) for result in results)
    
    # 모든 결과가 동일해야 함
    assert len(set(map(frozenset, results))) == 1
