#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SubSurfer main entry point
"""

from subsurfer.subsurfer import main
import asyncio

def run_main():
    """Wrapper function to run the async main"""
    asyncio.run(main())

if __name__ == "__main__":
    run_main() 