import pytest
import asyncio
from typing import Set
from subsurfer.core.handler.passive_handler import PassiveHandler
from subsurfer.core.handler.passive.crtsh import CrtshScanner
from subsurfer.core.handler.passive.abuseipdb import AbuseIPDBScanner
from subsurfer.core.handler.passive.anubisdb import AnubisDBScanner
from subsurfer.core.handler.passive.digitorus import DigitorusScanner
from subsurfer.core.handler.passive.bufferover import BufferOverScanner
from subsurfer.core.handler.passive.urlscan import UrlscanScanner
from subsurfer.core.handler.passive.alienvault import AlienVaultScanner
from subsurfer.core.handler.passive.hackertarget import HackerTargetScanner
from subsurfer.core.handler.passive.myssl import MySSLScanner
from subsurfer.core.handler.passive.shrewdeye import ShrewdEyeScanner
from subsurfer.core.handler.passive.subdomaincenter import SubdomainCenterScanner
from subsurfer.core.handler.passive.webarchive import WebArchiveScanner
from subsurfer.core.handler.passive.dnsarchive import DNSArchiveScanner

TEST_DOMAIN = "example.com"

@pytest.fixture
def passive_handler():
    return PassiveHandler(TEST_DOMAIN)

@pytest.mark.asyncio
async def test_crtsh_scanner():
    """crt.sh Scanner Test"""
    scanner = CrtshScanner(TEST_DOMAIN)
    results = await scanner.scan()
    assert isinstance(results, set)
    assert len(results) > 0
    assert all(isinstance(subdomain, str) for subdomain in results)
    assert all(TEST_DOMAIN in subdomain for subdomain in results)

@pytest.mark.asyncio
async def test_abuseipdb_scanner():
    """AbuseIPDB Scanner Test"""
    scanner = AbuseIPDBScanner(TEST_DOMAIN)
    results = await scanner.scan()
    assert isinstance(results, set)
    assert all(isinstance(subdomain, str) for subdomain in results)
    assert all(TEST_DOMAIN in subdomain for subdomain in results)

@pytest.mark.asyncio
async def test_anubisdb_scanner():
    """AnubisDB Scanner Test"""
    scanner = AnubisDBScanner(TEST_DOMAIN)
    results = await scanner.scan()
    assert isinstance(results, set)
    assert all(isinstance(subdomain, str) for subdomain in results)
    assert all(TEST_DOMAIN in subdomain for subdomain in results)

@pytest.mark.asyncio
async def test_digitorus_scanner():
    """Digitorus Scanner Test"""
    scanner = DigitorusScanner(TEST_DOMAIN)
    results = await scanner.scan()
    assert isinstance(results, set)
    assert all(isinstance(subdomain, str) for subdomain in results)
    assert all(TEST_DOMAIN in subdomain for subdomain in results)

@pytest.mark.asyncio
async def test_bufferover_scanner():
    """BufferOver Scanner Test"""
    scanner = BufferOverScanner(TEST_DOMAIN)
    results = await scanner.scan()
    assert isinstance(results, set)
    assert all(isinstance(subdomain, str) for subdomain in results)
    assert all(TEST_DOMAIN in subdomain for subdomain in results)

@pytest.mark.asyncio
async def test_urlscan_scanner():
    """Urlscan.io Scanner Test"""
    scanner = UrlscanScanner(TEST_DOMAIN)
    results = await scanner.scan()
    assert isinstance(results, set)
    assert all(isinstance(subdomain, str) for subdomain in results)
    assert all(TEST_DOMAIN in subdomain for subdomain in results)

@pytest.mark.asyncio
async def test_alienvault_scanner():
    """AlienVault Scanner Test"""
    scanner = AlienVaultScanner(TEST_DOMAIN)
    results = await scanner.scan()
    assert isinstance(results, set)
    assert all(isinstance(subdomain, str) for subdomain in results)
    assert all(TEST_DOMAIN in subdomain for subdomain in results)

@pytest.mark.asyncio
async def test_hackertarget_scanner():
    """HackerTarget Scanner Test"""
    scanner = HackerTargetScanner(TEST_DOMAIN)
    results = await scanner.scan()
    assert isinstance(results, set)
    assert all(isinstance(subdomain, str) for subdomain in results)
    assert all(TEST_DOMAIN in subdomain for subdomain in results)

@pytest.mark.asyncio
async def test_myssl_scanner():
    """MySSL Scanner Test"""
    scanner = MySSLScanner(TEST_DOMAIN)
    results = await scanner.scan()
    assert isinstance(results, set)
    assert all(isinstance(subdomain, str) for subdomain in results)
    assert all(TEST_DOMAIN in subdomain for subdomain in results)

@pytest.mark.asyncio
async def test_shrewdeye_scanner():
    """ShrewdEye Scanner Test"""
    scanner = ShrewdEyeScanner(TEST_DOMAIN)
    results = await scanner.scan()
    assert isinstance(results, set)
    assert all(isinstance(subdomain, str) for subdomain in results)
    assert all(TEST_DOMAIN in subdomain for subdomain in results)

@pytest.mark.asyncio
async def test_subdomaincenter_scanner():
    """SubdomainCenter Scanner Test"""
    scanner = SubdomainCenterScanner(TEST_DOMAIN)
    results = await scanner.scan()
    assert isinstance(results, set)
    assert all(isinstance(subdomain, str) for subdomain in results)
    assert all(TEST_DOMAIN in subdomain for subdomain in results)

@pytest.mark.asyncio
async def test_passive_handler_collect(passive_handler):
    """PassiveHandler collect Method Test"""
    results = await passive_handler.collect()
    
    # Basic Check
    assert isinstance(results, set)
    assert len(results) > 0
    
    # 모든 결과가 문자열이고 대상 도메인을 포함하는지 검증
    assert all(isinstance(subdomain, str) for subdomain in results)
    assert all(TEST_DOMAIN in subdomain for subdomain in results)
    
    # 알려진 서브도메인이 포함되어 있는지 검증
    known_subdomains = {"www.example.com", "m.example.com"}
    assert any(known in results for known in known_subdomains)

@pytest.mark.asyncio
async def test_passive_handler_error_handling(passive_handler):
    """PassiveHandler Error Test"""
    # 잘못된 도메인으로 테스트
    handler = PassiveHandler("this-domain-does-not-exist.com")
    results = await handler.collect()
    
    # 에러가 발생해도 빈 set을 반환해야 함
    assert isinstance(results, set)
    assert len(results) == 0

@pytest.mark.asyncio
async def test_passive_handler_concurrent_scans(passive_handler):
    """PassiveHandler concurrent Test"""
    # 여러 번의 동시 스캔 실행
    tasks = [passive_handler.collect() for _ in range(3)]
    results = await asyncio.gather(*tasks)
    
    # 모든 결과가 set이어야 함
    assert all(isinstance(result, set) for result in results)
    
    # 모든 결과가 동일해야 함
    assert len(set(map(frozenset, results))) == 1

@pytest.mark.asyncio
async def test_passive_handler_rate_limiting(passive_handler):
    """PassiveHandler rate limit Test"""
    # 연속적인 스캔 실행
    start_time = asyncio.get_event_loop().time()
    results = await passive_handler.collect()
    end_time = asyncio.get_event_loop().time()
    
    # 기본 검증
    assert isinstance(results, set)
    
    # 실행 시간이 너무 짧지 않은지 확인 (최소 1초)
    assert end_time - start_time >= 1.0

@pytest.mark.asyncio
async def test_webarchive_scanner():
    """WebArchive Scanner Test"""
    domain = "vulnweb.com"
    scanner = WebArchiveScanner(domain)
    results = await scanner.scan()
    
    assert isinstance(results, set)
    assert len(results) > 0
    
    # 결과 검증
    for subdomain in results:
        assert isinstance(subdomain, str)
        assert subdomain.endswith(domain)
        assert "." in subdomain  # 서브도메인이 있는지 확인

@pytest.mark.asyncio
async def test_dnsarchive_scanner():
    """DNS Archive Scanner Test"""
    scanner = DNSArchiveScanner(TEST_DOMAIN)
    results = await scanner.scan()
    
    assert isinstance(results, set)
    assert len(results) > 0
    
    # 결과 검증
    for subdomain in results:
        assert isinstance(subdomain, str)
        assert subdomain.endswith(TEST_DOMAIN)
        assert "." in subdomain  # 서브도메인이 있는지 확인

@pytest.mark.asyncio
async def test_webarchive_scanner_invalid_domain():
    """WebArchive 스캐너 유효하지 않은 도메인 테스트"""
    domain = "this-domain-does-not-exist-123456789.com"
    scanner = WebArchiveScanner(domain)
    results = await scanner.scan()
    
    assert isinstance(results, set)
    assert len(results) == 0  # 결과가 없어야 함

@pytest.mark.asyncio
async def test_dnsarchive_scanner_invalid_domain():
    """DNS Archive 스캐너 유효하지 않은 도메인 테스트"""
    domain = "this-domain-does-not-exist-123456789.com"
    scanner = DNSArchiveScanner(domain)
    results = await scanner.scan()
    
    assert isinstance(results, set)
    assert len(results) == 0  # 결과가 없어야 함

@pytest.mark.asyncio
async def test_webarchive_scanner_connection_error():
    """WebArchive 스캐너 연결 오류 테스트"""
    scanner = WebArchiveScanner(TEST_DOMAIN)
    scanner.base_url = "https://invalid-url-that-does-not-exist.com"
    
    results = await scanner.scan()
    assert isinstance(results, set)
    assert len(results) == 0  # 오류 발생 시 빈 set 반환

@pytest.mark.asyncio
async def test_dnsarchive_scanner_connection_error():
    """DNS Archive 스캐너 연결 오류 테스트"""
    scanner = DNSArchiveScanner(TEST_DOMAIN)
    scanner.base_url = "https://invalid-url-that-does-not-exist.com"
    
    results = await scanner.scan()
    assert isinstance(results, set)
    assert len(results) == 0  # 오류 발생 시 빈 set 반환
