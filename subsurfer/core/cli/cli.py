#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CLI utilities module
"""

import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.box import ROUNDED

console = Console()

def is_cli_mode():
    """Check if running in CLI mode"""
    return sys.stdin.isatty()

def print_banner(force=False):
    """Print banner only in CLI mode unless forced"""
    if not is_cli_mode() and not force:
        return
        
    banner = r"""
    🏄‍♂️  SubSurfer  🌊 
    ----------------------
     _____         _      _____                __             
    /  ___|       | |    /  ___|              / _|            
    \ `--.  _   _ | |__  \ `--.  _   _  _ __ | |_   ___  _ __ 
     `--. \| | | || '_ \  `--. \| | | || '__||  _| / _ \| '__|
    /\__/ /| |_| || |_) |/\__/ /| |_| || |   | |  |  __/| |   
    \____/  \__,_||_.__/ \____/  \__,_||_|   |_|   \___||_|   v0.2
    """
    
    # 배너 패널 생성
    banner_panel = Panel(
        banner,
        title="[bold cyan]Red Teaming and Web Bug Bounty Fast Asset Identification Tool[/]",
        subtitle="[bold blue]by. arrester (https://github.com/arrester/subsurfer)[/]",
        style="bold blue",
        box=ROUNDED
    )
    console.print(banner_panel)

def print_usage():
    """Print usage information"""
    usage_table = Table(
        title="[bold cyan]SubSurfer Usage Guide[/]",
        box=ROUNDED,
        show_header=True,
        header_style="bold magenta"
    )
    
    # 테이블 컬럼 설정
    usage_table.add_column("Command", style="cyan", justify="left")
    usage_table.add_column("Description", style="white", justify="left")
    usage_table.add_column("Example", style="green", justify="left")
    
    # 사용법 추가
    usage_table.add_row(
        "subsurfer -t <domain>",
        "Scan single domain",
        "subsurfer -t vulnweb.com"
    )
    usage_table.add_row(
        "subsurfer -t <domain> -o <file>",
        "Save results to file",
        "subsurfer -t vulnweb.com -o results.txt"
    )
    usage_table.add_row(
        "subsurfer -t <domain> -a",
        "Enable active scanning",
        "subsurfer -t vulnweb.com -a"
    )
    usage_table.add_row(
        "subsurfer -t <domain> -v",
        "Increase output verbosity",
        "subsurfer -t vulnweb.com -v"
    )
    
    # 옵션 테이블 생성
    options_table = Table(
        title="[bold cyan]Available Options[/]",
        box=ROUNDED,
        show_header=True,
        header_style="bold magenta"
    )
    
    # 옵션 테이블 컬럼 설정
    options_table.add_column("Option", style="cyan", justify="left")
    options_table.add_column("Description", style="white", justify="left")
    
    # 옵션 추가 (현재 구현된 옵션들만)
    options_table.add_row("-h, --help", "Show this help message")
    options_table.add_row("-t, --target", "Target domain (e.g. vulnweb.com)")
    options_table.add_row("-o, --output", "Output file to save results")
    options_table.add_row("-v, --verbose", "Increase output verbosity (-v, -vv, -vvv)")
    options_table.add_row("-a, --active", "Enable active scanning (default: passive only)")
    options_table.add_row("-dp, --default-ports", "Scan default ports")
    options_table.add_row("-p, --port", "Custom port range (e.g. 1-65535)")
    options_table.add_row("-pipeweb", "Output web server results for pipeline")
    options_table.add_row("-pipesub", "Output subdomain results for pipeline")
    options_table.add_row("-pipeact", "Output webserver + not webserver activate server results for pipeline")
    options_table.add_row("-pipewsub", "Output subdomain webserver host results for pipeline")
    options_table.add_row("-to, --takeover", "[Coming Soon] Subdomain takeover detection")
    
    # 출력
    console.print("\n[bold cyan]Description:[/]")
    console.print("SubSurfer is a fast subdomain enumeration tool that combines both passive and active scanning techniques to discover subdomains of a target domain.\n")
    
    console.print(usage_table)
    console.print("\n")
    console.print(options_table)
    console.print("\n[bold cyan]Note:[/] Some scanners may require API keys. Configure them in config.yaml")
    console.print("[bold yellow]Coming Soon:[/] Subdomain takeover detection will be available in the next version!\n")

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
    
    # 상태 아이콘 추가
    icons = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌"
    }
    
    console.print(f"[bold {colors[status]}]{icons[status]} {message}[/]")

def main():
    """Main entry point for CLI"""
    if len(sys.argv) == 1:
        print_banner(force=True)
        print_usage()
        sys.exit(0)

if __name__ == "__main__":
    main()