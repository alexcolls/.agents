"""
ASCII art and banners for retro terminal interface.

Provides vintage-style ASCII art for the CLI.
"""

from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from agents.utils.constants import PROJECT_NAME, VERSION


# Main application logo - Clean and modern
LOGO = r"""
             █████╗  ██████╗ ███████╗███╗   ██╗████████╗███████╗
            ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝██╔════╝
     ▄██▄   ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║   ███████╗
     ████   ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║   ╚════██║
     ▀██▀   ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║   ███████║
            ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝
"""

# Alternative compact logo
LOGO_COMPACT = r"""
  ▄█▄  ▄▀█ █▀▀ █▀▀ █▄░█ ▀█▀ █▀
  ███  █▀█ █▄█ ██▄ █░▀█ ░█░ ▄█
  ▀█▀
"""

# Ultra minimal logo
LOGO_MINIMAL = r"""
  ·AGENTS
"""

# Welcome banner
WELCOME_BANNER = r"""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║              Welcome to .AGENTS v{version}                              ║
║                                                                   ║
║       Social Media Automation • WhatsApp → Instagram             ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
"""

# Success ASCII art
SUCCESS_ART = r"""
   █████╗  ██████╗ ███████╗███╗   ██╗████████╗
  ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝
  ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║   
  ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║   
  ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║   
  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝   
                                                
   ██████╗██████╗ ███████╗ █████╗ ████████╗███████╗██████╗ ██╗
  ██╔════╝██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔════╝██╔══██╗██║
  ██║     ██████╔╝█████╗  ███████║   ██║   █████╗  ██║  ██║██║
  ██║     ██╔══██╗██╔══╝  ██╔══██║   ██║   ██╔══╝  ██║  ██║╚═╝
  ╚██████╗██║  ██║███████╗██║  ██║   ██║   ███████╗██████╔╝██╗
   ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═════╝ ╚═╝
"""

# Simple success checkmark
SUCCESS_SIMPLE = r"""
      ✓
   SUCCESS!
"""

# Error/Warning ASCII art
ERROR_ART = r"""
  ███████╗██████╗ ██████╗  ██████╗ ██████╗ 
  ██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔══██╗
  █████╗  ██████╔╝██████╔╝██║   ██║██████╔╝
  ██╔══╝  ██╔══██╗██╔══██╗██║   ██║██╔══██╗
  ███████╗██║  ██║██║  ██║╚██████╔╝██║  ██║
  ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝
"""

# Loading spinner frames
SPINNER_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

# Progress bar characters
PROGRESS_BAR_FULL = "█"
PROGRESS_BAR_EMPTY = "░"
PROGRESS_BAR_PARTIAL = ["▏", "▎", "▍", "▌", "▋", "▊", "▉"]

# Decorative boxes
BOX_DOUBLE = {
    "top_left": "╔",
    "top_right": "╗",
    "bottom_left": "╚",
    "bottom_right": "╝",
    "horizontal": "═",
    "vertical": "║",
    "top_join": "╦",
    "bottom_join": "╩",
    "left_join": "╠",
    "right_join": "╣",
    "cross": "╬",
}

BOX_SINGLE = {
    "top_left": "┌",
    "top_right": "┐",
    "bottom_left": "└",
    "bottom_right": "┘",
    "horizontal": "─",
    "vertical": "│",
    "top_join": "┬",
    "bottom_join": "┴",
    "left_join": "├",
    "right_join": "┤",
    "cross": "┼",
}

BOX_ROUNDED = {
    "top_left": "╭",
    "top_right": "╮",
    "bottom_left": "╰",
    "bottom_right": "╯",
    "horizontal": "─",
    "vertical": "│",
}

# Platform icons (text-based)
PLATFORM_ICONS = {
    "instagram": "📸",
    "tiktok": "🎵",
    "youtube": "🎥",
    "linkedin": "💼",
    "whatsapp": "💬",
}

# Status icons
STATUS_ICONS = {
    "active": "🟢",
    "inactive": "⚪",
    "error": "🔴",
    "paused": "🟡",
    "success": "✅",
    "warning": "⚠️",
    "info": "ℹ️",
    "question": "❓",
}


def print_logo(console: Optional[Console] = None, style: str = "default") -> None:
    """
    Print the application logo.
    
    Args:
        console: Rich console instance. If None, creates new one
        style: Logo style ('default', 'compact', 'minimal')
    """
    if console is None:
        console = Console()
    
    if style == "compact":
        logo_text = LOGO_COMPACT
    elif style == "minimal":
        logo_text = LOGO_MINIMAL
    else:
        logo_text = LOGO
    
    # Print with cyan color for retro feel
    text = Text(logo_text)
    text.stylize("bold cyan")
    console.print(text)
    console.print(f"[dim cyan]v{VERSION} • Social Media Automation[/dim cyan]", justify="center")
    console.print()


def print_welcome(console: Optional[Console] = None) -> None:
    """
    Print welcome banner.
    
    Args:
        console: Rich console instance. If None, creates new one
    """
    if console is None:
        console = Console()
    
    banner = WELCOME_BANNER.replace("{version}", VERSION)
    console.print(banner, style="bold cyan")
    console.print()


def print_success(
    message: str,
    console: Optional[Console] = None,
    show_art: bool = True,
    simple: bool = False
) -> None:
    """
    Print success message with ASCII art.
    
    Args:
        message: Success message
        console: Rich console instance
        show_art: Whether to show ASCII art
        simple: Use simple checkmark instead of full art
    """
    if console is None:
        console = Console()
    
    if show_art:
        art = SUCCESS_SIMPLE if simple else SUCCESS_ART
        text = Text(art)
        text.stylize("bold green")
        console.print(text, justify="center")
    
    console.print(f"\n[bold green]{message}[/bold green]\n", justify="center")


def print_error(
    message: str,
    console: Optional[Console] = None,
    show_art: bool = False
) -> None:
    """
    Print error message.
    
    Args:
        message: Error message
        console: Rich console instance
        show_art: Whether to show ASCII art
    """
    if console is None:
        console = Console()
    
    if show_art:
        text = Text(ERROR_ART)
        text.stylize("bold red")
        console.print(text, justify="center")
    
    console.print(f"\n[bold red]✗ {message}[/bold red]\n")


def create_box(
    content: str,
    title: Optional[str] = None,
    style: str = "double",
    width: Optional[int] = None,
) -> str:
    """
    Create a decorative box around content.
    
    Args:
        content: Content to wrap
        title: Optional title for the box
        style: Box style ('double', 'single', 'rounded')
        width: Box width. If None, auto-sizes to content
        
    Returns:
        str: Formatted box
    """
    box = BOX_DOUBLE if style == "double" else BOX_SINGLE if style == "single" else BOX_ROUNDED
    
    lines = content.split("\n")
    if width is None:
        width = max(len(line) for line in lines) + 4
    
    # Top border
    if title:
        title_padded = f" {title} "
        title_len = len(title_padded)
        left_border = box["horizontal"] * 2
        right_border = box["horizontal"] * (width - title_len - 4)
        top = f"{box['top_left']}{left_border}{title_padded}{right_border}{box['top_right']}"
    else:
        top = f"{box['top_left']}{box['horizontal'] * (width - 2)}{box['top_right']}"
    
    # Content lines
    content_lines = []
    for line in lines:
        padding = width - len(line) - 4
        content_lines.append(f"{box['vertical']} {line}{' ' * padding} {box['vertical']}")
    
    # Bottom border
    bottom = f"{box['bottom_left']}{box['horizontal'] * (width - 2)}{box['bottom_right']}"
    
    return "\n".join([top] + content_lines + [bottom])


def create_progress_bar(
    current: int,
    total: int,
    width: int = 40,
    show_percentage: bool = True,
) -> str:
    """
    Create a progress bar.
    
    Args:
        current: Current progress value
        total: Total value
        width: Width of progress bar
        show_percentage: Whether to show percentage
        
    Returns:
        str: Formatted progress bar
        
    Examples:
        >>> create_progress_bar(50, 100, width=20)
        '██████████░░░░░░░░░░ 50%'
    """
    if total == 0:
        percentage = 0
    else:
        percentage = (current / total) * 100
    
    filled = int((current / total) * width) if total > 0 else 0
    empty = width - filled
    
    bar = PROGRESS_BAR_FULL * filled + PROGRESS_BAR_EMPTY * empty
    
    if show_percentage:
        return f"{bar} {percentage:.0f}%"
    return bar


def create_table_row(
    columns: list[str],
    widths: list[int],
    alignment: list[str] = None,
) -> str:
    """
    Create a table row.
    
    Args:
        columns: Column values
        widths: Column widths
        alignment: Column alignments ('left', 'center', 'right')
        
    Returns:
        str: Formatted table row
    """
    if alignment is None:
        alignment = ["left"] * len(columns)
    
    cells = []
    for col, width, align in zip(columns, widths, alignment):
        if align == "center":
            cell = col.center(width)
        elif align == "right":
            cell = col.rjust(width)
        else:
            cell = col.ljust(width)
        cells.append(cell)
    
    return "│ " + " │ ".join(cells) + " │"


def create_separator(widths: list[int], position: str = "middle") -> str:
    """
    Create a table separator line.
    
    Args:
        widths: Column widths
        position: Position ('top', 'middle', 'bottom')
        
    Returns:
        str: Formatted separator
    """
    if position == "top":
        left, middle, right = "┌", "┬", "┐"
    elif position == "bottom":
        left, middle, right = "└", "┴", "┘"
    else:
        left, middle, right = "├", "┼", "┤"
    
    parts = [("─" * (w + 2)) for w in widths]
    return left + middle.join(parts) + right


def print_menu_header(title: str, console: Optional[Console] = None) -> None:
    """
    Print a menu header with decorative borders.
    
    Args:
        title: Menu title
        console: Rich console instance
    """
    if console is None:
        console = Console()
    
    width = 60
    
    panel = Panel(
        f"[bold cyan]{title}[/bold cyan]",
        width=width,
        border_style="cyan",
        padding=(1, 2),
    )
    
    console.print()
    console.print(panel)
    console.print()


def animate_typing(text: str, console: Optional[Console] = None, delay: float = 0.03) -> None:
    """
    Print text with typing animation effect.
    
    Args:
        text: Text to print
        console: Rich console instance
        delay: Delay between characters (seconds)
    """
    import time
    
    if console is None:
        console = Console()
    
    for char in text:
        console.print(char, end="")
        time.sleep(delay)
    console.print()


# Example usage
if __name__ == "__main__":
    console = Console()
    
    # Test all logo styles
    console.print("[bold]Default Logo:[/bold]")
    print_logo(console, style="default")
    
    console.print("\n[bold]Compact Logo:[/bold]")
    print_logo(console, style="compact")
    
    console.print("\n[bold]Minimal Logo:[/bold]")
    print_logo(console, style="minimal")
    
    # Test welcome
    print_welcome(console)
    
    # Test success
    print_success("Agent created successfully!", console, show_art=True, simple=False)
    
    # Test simple success
    print_success("Configuration saved!", console, show_art=True, simple=True)
    
    # Test box
    box_content = create_box(
        "This is a test message\nWith multiple lines\nInside a box",
        title="Test Box",
        style="double",
    )
    console.print(box_content, style="cyan")
    
    # Test progress bar
    console.print("\n[bold]Progress Bar Examples:[/bold]")
    console.print(create_progress_bar(25, 100))
    console.print(create_progress_bar(50, 100))
    console.print(create_progress_bar(75, 100))
    console.print(create_progress_bar(100, 100))
    
    # Test menu header
    print_menu_header(".AGENTS Main Menu", console)
