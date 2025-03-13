from setuptools import setup, find_namespace_packages

setup(
    name="subsurfer",
    version="0.2.7",
    description="Red Teaming and Web Bug Bounty Fast Asset Identification Tool",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="arrester",
    author_email="arresterloyal@gmail.com",
    url="https://github.com/arrester/subsurfer",
    packages=find_namespace_packages(include=['subsurfer*']),
    package_data={
        'subsurfer': ['core/config/*.yaml'],
    },
    include_package_data=True,
    install_requires=[
        'rich>=13.7.0',
        'aiohttp>=3.9.1',
        'beautifulsoup4>=4.12.2',
        'dnspython>=2.4.2',
        'pyyaml>=6.0.1',
        'asyncio>=3.4.3',
        'pytest>=7.4.3',
        'pytest-asyncio>=0.23.2',
        'python-Wappalyzer>=0.3.1',
        'setuptools>=75.6.0'
    ],
    entry_points={
        'console_scripts': [
            'subsurfer=subsurfer.__main__:run_main',
        ],
    },
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Topic :: Security',
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.13',
        'Operating System :: OS Independent',
    ],
    keywords='security, subdomain enumeration, bug bounty, red team, web security',
    project_urls={
        'Bug Reports': 'https://github.com/arrester/subsurfer/issues',
        'Source': 'https://github.com/arrester/subsurfer',
        'Documentation': 'https://github.com/arrester/subsurfer#readme',
    },
) 