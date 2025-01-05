#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Command line argument parser module
"""

import argparse

def create_parser():
    """Create and return argument parser"""
    parser = argparse.ArgumentParser(
        description='SubSurfer - Fast web bug bounty asset identification tool'
    )
    
    parser.add_argument('-t', '--target', 
                      help='Target domain (e.g. example.com)')
    parser.add_argument('-dp', '--default-ports',
                      action='store_true',
                      help='Scan default ports')
    parser.add_argument('-p', '--ports',
                      help='Custom port range (e.g. 1-65535)') 
    parser.add_argument('-v', '--verify',
                      action='store_true', 
                      help='Verify subdomain takeover')
    parser.add_argument('-o', '--output',
                      help='Output file path')
    parser.add_argument('-pipeweb', action='store_true',
                      help='Output web server results for pipeline')
    parser.add_argument('-pipesub', action='store_true',
                      help='Output subdomain results for pipeline')
                      
    return parser

def parse_args():
    """Parse and return command line arguments"""
    parser = create_parser()
    return parser.parse_args()
