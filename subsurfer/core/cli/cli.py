#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CLI utilities module
"""

import sys
from rich.console import Console
from rich.panel import Panel

console = Console()

def is_cli_mode():
    """Check if running in CLI mode"""
    return sys.stdin.isatty()

def print_banner(force=False):
    """Print banner only in CLI mode unless forced"""
    if not is_cli_mode() and not force:
        return
        
    banner = r"""
    🏄‍♂️  SubSurfer  🌊 by. arrester(https://github.com/arrester/subsurfer)
    ----------------------
     _____         _      _____                __             
    /  ___|       | |    /  ___|              / _|            
    \ `--.  _   _ | |__  \ `--.  _   _  _ __ | |_   ___  _ __ 
     `--. \| | | || '_ \  `--. \| | | || '__||  _| / _ \| '__|
    /\__/ /| |_| || |_) |/\__/ /| |_| || |   | |  |  __/| |   
    \____/  \__,_||_.__/ \____/  \__,_||_|   |_|   \___||_|   v0.1
    """
    console.print(Panel(banner, style="bold blue"))
    console.print("[bold cyan]Fast Web Bug Bounty Asset Identification Tool[/]\n")

def print_status(message, status="info", cli_only=True):
    """Print status messages with color coding"""
    if cli_only and not is_cli_mode():
        return
        
    colors = {
        "info": "blue",
        "success": "green",
        "warning": "yellow", 
        "error": "red"
    }
    console.print(f"[bold {colors[status]}]{message}[/]")