"""
CLI Main Entry Point

Main entry point for the .agents CLI application.
Handles argument parsing, banner display, and command routing.
"""

import sys
import argparse
from pathlib import Path

from src.cli.ascii_art import AgentsLogo
from src.cli.theme import get_console
from src.cli.menu import main_menu
from src.cli.commands import (
    create_agent_command,
    list_agents_command,
    edit_agent_command,
    delete_agent_command,
    start_agent_command,
    stop_agent_command,
    status_command,
)
from src.utils.constants import VERSION, PROJECT_NAME
from src.utils.logger import get_logger


logger = get_logger(__name__)
console = get_console()


def show_banner():
    """Display ASCII banner"""
    logo = AgentsLogo()
    console.print(logo.get_logo())
    console.print()


def show_help():
    """Show help information"""
    show_banner()
    
    help_text = f"""
[bold cyan]{PROJECT_NAME}[/bold cyan] - Social Media Automation via WhatsApp

[bold yellow]Usage:[/bold yellow]
  agents              Launch interactive menu
  agents create       Create a new agent
  agents list         List all agents
  agents start        Start an agent
  agents stop         Stop an agent
  agents status       Show agent status
  agents --version    Show version
  agents --help       Show this help

[bold yellow]Interactive Menu:[/bold yellow]
  The interactive menu provides a user-friendly interface to:
  - Create and configure agents
  - Start/stop automation
  - View status and statistics
  - Manage agent settings

[bold yellow]Quick Start:[/bold yellow]
  1. Run 'agents' to launch the interactive menu
  2. Select "Create New Agent"
  3. Configure WhatsApp groups and social media platforms
  4. Start the agent to begin monitoring

For more information, visit: https://github.com/alexcolls/.agents
"""
    
    console.print(help_text)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        prog="agents",
        description=f"{PROJECT_NAME} - Social Media Automation",
        add_help=False,  # We'll handle help ourselves
    )
    
    parser.add_argument(
        "command",
        nargs="?",
        choices=["create", "list", "edit", "delete", "start", "stop", "status", "help"],
        help="Command to execute"
    )
    
    parser.add_argument(
        "--version", "-v",
        action="store_true",
        help="Show version"
    )
    
    parser.add_argument(
        "--help", "-h",
        action="store_true",
        help="Show help"
    )
    
    args = parser.parse_args()
    
    # Handle version
    if args.version:
        console.print(f"{PROJECT_NAME} v{VERSION}")
        return 0
    
    # Handle help
    if args.help or args.command == "help":
        show_help()
        return 0
    
    # Show banner
    show_banner()
    
    # Direct command execution
    if args.command:
        try:
            if args.command == "create":
                create_agent_command()
            elif args.command == "list":
                list_agents_command()
            elif args.command == "edit":
                edit_agent_command()
            elif args.command == "delete":
                delete_agent_command()
            elif args.command == "start":
                start_agent_command()
            elif args.command == "stop":
                stop_agent_command()
            elif args.command == "status":
                status_command()
            
            return 0
            
        except KeyboardInterrupt:
            console.print()
            console.print_warning("Operation cancelled by user")
            return 130
        except Exception as e:
            console.print_error(f"Command failed: {e}")
            logger.error(f"Command '{args.command}' failed", exc_info=True)
            return 1
    
    # Interactive menu mode
    try:
        while True:
            console.print()
            action = main_menu()
            
            if action == "exit":
                console.print()
                console.print("👋 Goodbye!")
                break
            
            console.print()
            
            # Execute action
            if action == "create":
                create_agent_command()
            elif action == "list":
                list_agents_command()
            elif action == "edit":
                edit_agent_command()
            elif action == "delete":
                delete_agent_command()
            elif action == "start":
                start_agent_command()
            elif action == "stop":
                stop_agent_command()
            elif action == "status":
                status_command()
            elif action == "settings":
                console.print_info("Settings not implemented yet")
            elif action == "help":
                show_help()
            
            # Pause before showing menu again
            console.print()
            input("Press Enter to continue...")
            console.clear()
            show_banner()
        
        return 0
        
    except KeyboardInterrupt:
        console.print()
        console.print()
        console.print("👋 Goodbye!")
        return 0
    except Exception as e:
        console.print_error(f"Unexpected error: {e}")
        logger.error("Unexpected error in main loop", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
