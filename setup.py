from setuptools import setup, find_packages

setup(
    name="subsurfer",
    version="0.1",
    description="Fast Web Bug Bounty Asset Identification Tool",
    author="arrester",
    packages=find_packages(),
    install_requires=[
        'rich',
        'aiohttp',
        'beautifulsoup4',
        'dnspython',
        'pyyaml',
        'asyncio'
    ],
    entry_points={
        'console_scripts': [
            'subsurfer=subsurfer.__main__:run_main',
        ],
    },
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Information Technology',
        'Topic :: Security',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
) 