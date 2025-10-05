#!/usr/bin/env python3
"""
🤖 .agents - WhatsApp to Social Media Automation
Main entry point for the application
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent
sys.path.insert(0, str(src_dir))


def main():
    """Main entry point for the .agents application"""
    from src.cli.main import main as cli_main
    return cli_main()


if __name__ == "__main__":
    sys.exit(main())

