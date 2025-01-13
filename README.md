# 🏄‍♂️ SubSurfer

![Python Version](https://img.shields.io/badge/python-3.13%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-0.1-orange)

SubSurfer는 빠르고 효율적인 서브도메인 열거 및 웹 자산 식별 도구입니다.

<br>

## 🌟 특징
- **레드팀/버그바운티 지원**: 레드팀 작전과 웹 버그바운티 프로젝트 모두에서 활용 가능
- **고성능 스캔**: 비동기 및 병렬 처리를 통한 빠른 서브도메인 수집
- **포트 스캔**: 사용자 정의 포트 범위로 자산 스캔 범위 확장
- **웹 서비스 식별**: 웹 서버, 기술 스택 등 환경 정보 수집
- **파이프라인 지원**: `-pipeweb`, `-pipesub` 옵션으로 다른 도구와의 연계 가능
- **모듈형 설계**: Python 모듈로 import하여 사용 가능
- **지속적 업데이트**: 새로운 passive/active 모듈 지속 추가 예정

<br>

## 🚀 설치
<b>bash</b>
```bash
git clone https://github.com/arrester/subsurfer.git
cd subsurfer
```

or <br>

<b>Python</b>
```bash
pip install -r requirements.txt
```

<br>

## 📖 사용법
### CLI 모드
<b>기본 스캔</b><br>
`subsurfer -t vulnweb.com`

<b>액티브 스캔 활성화</b><br>
`subsurfer -t vulnweb.com -a`

<b>포트 스캔 포함</b><br>
`subsurfer -t vulnweb.com -dp` # 기본 포트 <br>
`subsurfer -t vulnweb.com -p 80,443,8080-8090` # 사용자 정의 포트

<b>파이프라인 출력</b><br>
`subsurfer -t vulnweb.com -pipeweb` # 웹 서버 결과만 출력 <br>
`subsurfer -t vulnweb.com -pipesub` # 서브도메인 결과만 출력

### Python 모듈로 사용
<b>Subdomain Scan</b><br>
```python
from subsurfer.core.controller.controller import SubSurferController
import asyncio

async def main():
    controller = SubSurferController(
        target="vulnweb.com",
        verbose=1,
        active=False            # Active Scan Option
    )
    
    # 서브도메인 수집
    subdomains = await controller.collect_subdomains()
    
    # 결과 출력
    print(f"발견된 서브도메인: {len(subdomains)}개")
    for subdomain in sorted(subdomains):
        print(subdomain)

if __name__ == "__main__":
    asyncio.run(main())
```

<br>

<b>Port Scan</b><br>
```python
from subsurfer.core.controller.controller import SubSurferController
import asyncio

async def main():
    controller = SubSurferController(
        target="vulnweb.com",
        verbose=1
    )
    
    # 서브도메인 수집
    subdomains = await controller.collect_subdomains()
    
    # 기본 80, 443 스캔 설정
    ports = None

    # 포트 스캔 설정
    # ports = controller.parse_ports()  # 기본 포트
    # 또는 사용자 지정 포트
    # ports = controller.parse_ports("80,443,8080-8090")
    
    # 웹 서비스 스캔
    web_services = await controller.scan_web_services(subdomains, ports)
    
    # 웹 서버 출력
    print("\n웹 서버:")
    for server in sorted(web_services['web_servers']):
        print(f"https://{server}")
    
    # 활성화된 서비스 출력    
    print("\n활성화된 서비스:")
    for service in sorted(web_services['enabled_services']):
        print(service)
        
    # URL과 포트 정보 출력
    print("\n발견된 URL:")
    for subdomain, urls in web_services['all_urls'].items():
        for url, port in urls:
            print(f"{url}:{port}")

if __name__ == "__main__":
    asyncio.run(main())
```

<br>

<b>Result Save</b><br>
```python
from subsurfer.core.controller.controller import SubSurferController
import asyncio

async def main():
    controller = SubSurferController("vulnweb.com")
    
    # 서브도메인 수집 및 웹 서비스 스캔
    subdomains = await controller.collect_subdomains()
    web_services = await controller.scan_web_services(subdomains)
    
    # 결과 저장
    results_dict = {
        'subdomains': subdomains,
        'web_services': web_services.get('web_services', {}),
        'web_servers': web_services.get('web_servers', set()),
        'enabled_services': web_services.get('enabled_services', set()),
        'all_urls': web_services.get('all_urls', {})  # URL과 포트 정보 포함
    }
    
    # 기본 결과 파일 경로 생성 (results 디렉토리에 저장)
    output_path = controller.get_output_path()
    controller.save_results(results_dict, output_path)

if __name__ == "__main__":
    asyncio.run(main())
```

<br>

## 🧪 테스트
### 패시브 핸들러 테스트
`pytest tests/handlers/test_passive_handler.py -v`

<br>

### 액티브 핸들러 테스트
`pytest tests/handlers/test_active_handler.py -v`

<br>

## 🗺️ ToDo
### 0.2 버전
- 새로운 패시브 모듈 추가

### 0.3 버전
- JSON 결과 출력 옵션 추가
- 새로운 패시브 모듈 추가
- 기타 기능 업데이트

### 0.4 버전
- 새로운 패시브 모듈 추가
- 서브도메인 탈취 검사 기능

### 0.5 버전
- 새로운 패시브 모듈 추가
- 새로운 액티브 모듈 추가

## 📋 요구사항

- Python 3.13.0 이상 권장
- aiohttp
- rich
- pytest (테스트용)

## 📝 라이선스
MIT License

## 🤝 기여
Bug Report, Feature Suggestions, Pull Request