#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Command line argument parser module
"""

import argparse

def create_parser():
    """Create and return argument parser"""
    parser = argparse.ArgumentParser(
        description='SubSurfer - Red Teaming and Web Bug Bounty Fast Asset Identification Tool'
    )
    
    parser.add_argument('-t', '--target', 
                      help='Target domain (e.g. example.com)')
    parser.add_argument('-dp', '--default-ports',
                      dest='default_ports',
                      action='store_true',
                      help='Scan default ports')
    parser.add_argument('-p', '--port',
                      dest='port',
                      help='Custom port range (e.g. 1-65535)') 
    parser.add_argument('-v', '--verbose',
                      action='count',
                      default=0,
                      help='Increase output verbosity (-v, -vv, -vvv)')
    parser.add_argument('-to', '--takeover',
                      action='store_true', 
                      help='Verify subdomain takeover')
    parser.add_argument('-o', '--output',
                      help='Output file path')
    parser.add_argument('-pipeweb', action='store_true',
                      help='Output web server results for pipeline')
    parser.add_argument('-pipesub', action='store_true',
                      help='Output subdomain results for pipeline')
    parser.add_argument('-a', '--active',
                      action='store_true',
                      help='Enable active scanning (default: passive only)')
                      
    return parser

def parse_args():
    """Parse and return command line arguments"""
    parser = create_parser()
    return parser.parse_args()
