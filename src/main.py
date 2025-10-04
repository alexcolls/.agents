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
    try:
        # Try to import rich for beautiful terminal output
        from rich.console import Console
        from rich.panel import Panel
        from rich.text import Text
        
        console = Console()
        
        # Welcome banner
        welcome_text = Text()
        welcome_text.append("🤖 Welcome to ", style="bold cyan")
        welcome_text.append(".agents", style="bold magenta")
        welcome_text.append("\n\n", style="")
        welcome_text.append("WhatsApp to Social Media Automation Tool\n", style="cyan")
        welcome_text.append("Version 0.1.0\n\n", style="dim")
        welcome_text.append("⚠️  This is a development preview\n", style="yellow")
        welcome_text.append("The full CLI interface is coming soon!", style="green")
        
        console.print(Panel(
            welcome_text,
            border_style="cyan",
            padding=(1, 2)
        ))
        
        console.print("\n[bold cyan]Quick Start:[/bold cyan]")
        console.print("  1. Make sure your [yellow].env[/yellow] file is configured")
        console.print("  2. Set a strong [yellow]MASTER_PASSWORD[/yellow]")
        console.print("  3. The full CLI interface is under development\n")
        
        console.print("[dim]For more information, visit: https://github.com/alexcolls/.agents[/dim]\n")
        
    except ImportError:
        # Fallback if rich is not installed
        print("=" * 70)
        print("🤖 .agents - WhatsApp to Social Media Automation")
        print("=" * 70)
        print("\nWelcome to .agents!")
        print("Version 0.1.0 (Development Preview)")
        print("\n⚠️  The full CLI interface is coming soon!")
        print("\nQuick Start:")
        print("  1. Make sure your .env file is configured")
        print("  2. Set a strong MASTER_PASSWORD")
        print("  3. The full CLI interface is under development")
        print("\nFor more information, visit: https://github.com/alexcolls/.agents")
        print("=" * 70)


if __name__ == "__main__":
    main()

