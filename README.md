# 🏄‍♂️ SubSurfer

![Python Version](https://img.shields.io/badge/python-3.13%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-0.2-orange)

SubSurfer is a fast and efficient subdomain enumeration and web property identification tool.
![alt text](image.png)

<br>

## 🌟 Features
- **Red Team/Bug Bounty Support**: Useful for both red team operations and web bug bounty projects
- **High-Performance Scanning**: Fast subdomain enumeration using asynchronous and parallel processing
- **Port Scanning**: Expand asset scanning range with customizable port selection
- **Web Service Identification**: Gather environmental details such as web servers and technology stacks
- **Pipeline Integration**: Supports integration with other tools using `-pipeweb` and `-pipesub` options
- **Modular Design**: Can be imported and used as a Python module
- **Continuous Updates**: - **Continuous Updates**: New passive/active modules will continue to be added

<br>

## 🚀 Installation
<b>bash</b>
```bash
git clone https://github.com/arrester/subsurfer.git
cd subsurfer
```

or <br>

<b>Python</b>
```bash
pip install subsurfer
```

<br>

## 📖 Usage
### CLI Mode
<b>Basic Scan</b><br>
`subsurfer -t vulnweb.com`

<b>Enable Active Scanning</b><br>
`subsurfer -t vulnweb.com -a`

<b>Include Port Scanning</b><br>
`subsurfer -t vulnweb.com -dp` # Default Port <br>
`subsurfer -t vulnweb.com -p 80,443,8080-8090` # Custom ports

<b>Pipeline Output</b><br>
`subsurfer -t vulnweb.com -pipeweb` # Output only web server <br>
`subsurfer -t vulnweb.com -pipesub` # Output only subdomain results

### Using as a Python Module
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
    
    # Collect subdomains
    subdomains = await controller.collect_subdomains()
    
    # Print results
    print(f"Discovered Subdomains: {len(subdomains)}개")
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
    
    # Collect subdomains
    subdomains = await controller.collect_subdomains()
    
    # Default ports (80, 443)
    ports = None

    # Set port scan options
    # ports = controller.parse_ports()  # Default ports
    # Or specify custom ports
    # ports = controller.parse_ports("80,443,8080-8090")
    
    # Web service scanning
    web_services = await controller.scan_web_services(subdomains, ports)
    
    # Print web servers
    print("\n웹 서버:")
    for server in sorted(web_services['web_servers']):
        print(f"https://{server}")
    
    # Print active services
    print("\n활성화된 서비스:")
    for service in sorted(web_services['enabled_services']):
        print(service)
        
    # Print discovered URLs and ports
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
    
    # Collect subdomains and scan web services
    subdomains = await controller.collect_subdomains()
    web_services = await controller.scan_web_services(subdomains)
    
    # Save results
    results_dict = {
        'subdomains': subdomains,
        'web_services': web_services.get('web_services', {}),
        'web_servers': web_services.get('web_servers', set()),
        'enabled_services': web_services.get('enabled_services', set()),
        'all_urls': web_services.get('all_urls', {})  # Includes URL and port information
    }
    
    # Generate default result file path (stored in the "results" directory)
    output_path = controller.get_output_path()
    controller.save_results(results_dict, output_path)

if __name__ == "__main__":
    asyncio.run(main())
```

<br>

## 🧪 Testing
### Passive Handler Test
`pytest tests/handlers/test_passive_handler.py -v`

<br>

### Active Handler Test
`pytest tests/handlers/test_active_handler.py -v`

<br>

## 🗺️ To-Do List
### Version 0.3
- Add JSON output option
- Add new passive modules
- Additional etc feature updates

### Version 0.4
- Add new passive modules
- Implement subdomain takeover detection

### Version 0.5
- Add new passive modules
- Add new active modules

## 📋 Requirements
- Recommended: Python 3.13.0 or later
- aiohttp
- rich
- pytest (for testing)

## 📝 License
MIT License

## 🤝 Contributions
Bug Report, Feature Suggestions, Issue Report