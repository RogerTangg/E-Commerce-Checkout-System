#!/usr/bin/env python
"""
E-Commerce Checkout System - Application Entry Point
應用程式入口點

Usage:
    python run.py [--host HOST] [--port PORT] [--debug]

Examples:
    python run.py                    # Run on localhost:5000
    python run.py --port 8080        # Run on localhost:8080
    python run.py --host 0.0.0.0     # Run on all interfaces
"""

import argparse
import sys
import os

# 將 src 目錄加入 Python 路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.app import app


def parse_args():
    """解析命令列參數"""
    parser = argparse.ArgumentParser(
        description='E-Commerce Checkout System Server'
    )
    parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='Host to bind (default: 127.0.0.1)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=5000,
        help='Port to bind (default: 5000)'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║         E-Commerce Checkout System                           ║
║         電商結帳系統                                           ║
╠══════════════════════════════════════════════════════════════╣
║  Server:     http://{args.host}:{args.port}                        
║  Dashboard:  http://{args.host}:{args.port}/dashboard/              
║  Debug Mode: {args.debug}                                         
╚══════════════════════════════════════════════════════════════╝
    """)
    
    app.run(
        host=args.host,
        port=args.port,
        debug=args.debug
    )
