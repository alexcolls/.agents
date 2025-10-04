"""
CLI Theme System

Provides consistent retro-terminal styling, color schemes, and Rich console
rendering throughout the application.

Classes:
    ThemeColors: Color palette constants
    ThemeStyle: Style configuration
    ThemedConsole: Rich console wrapper with theme support
    
Functions:
    get_console: Get singleton themed console instance
    styled_text: Create styled text with theme colors
    panel: Create themed panel
    table: Create themed table
    progress_bar: Create themed progress bar
"""

from typing import Optional, Dict, Any, List
from enum import Enum
from dataclasses import dataclass

from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel
from rich.table import Table
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
)
from rich.text import Text
from rich.style import Style
from rich.box import Box, ROUNDED, DOUBLE, HEAVY, MINIMAL


class ThemeColors(str, Enum):
    """Retro terminal color palette"""
    
    # Primary colors
    PRIMARY = "cyan"
    SECONDARY = "magenta"
    ACCENT = "yellow"
    
    # Status colors
    SUCCESS = "green"
    ERROR = "red"
    WARNING = "yellow"
    INFO = "blue"
    
    # Semantic colors
    HIGHLIGHT = "bright_cyan"
    DIM = "dim white"
    MUTED = "grey50"
    
    # Platform colors
    WHATSAPP = "green"
    INSTAGRAM = "magenta"
    TIKTOK = "bright_magenta"
    YOUTUBE = "red"
    TWITTER = "bright_blue"
    FACEBOOK = "blue"
    
    # UI elements
    BORDER = "cyan"
    TITLE = "bright_cyan bold"
    SUBTITLE = "magenta"
    PROMPT = "yellow"
    INPUT = "white"
    LABEL = "cyan"
    VALUE = "white"
    
    # Special effects
    NEON_GREEN = "bright_green"
    NEON_PINK = "bright_magenta"
    NEON_BLUE = "bright_cyan"
    RETRO_AMBER = "yellow"
    RETRO_GREEN = "green"


class BoxStyle(str, Enum):
    """Box drawing styles for panels and tables"""
    
    ROUNDED = "rounded"
    DOUBLE = "double"
    HEAVY = "heavy"
    MINIMAL = "minimal"
    SIMPLE = "simple"
    SQUARE = "square"


# Map box style names to Rich box objects
BOX_STYLES: Dict[str, Box] = {
    BoxStyle.ROUNDED: ROUNDED,
    BoxStyle.DOUBLE: DOUBLE,
    BoxStyle.HEAVY: HEAVY,
    BoxStyle.MINIMAL: MINIMAL,
}


@dataclass
class ThemeStyle:
    """Theme style configuration"""
    
    # Colors
    primary: str = ThemeColors.PRIMARY
    secondary: str = ThemeColors.SECONDARY
    accent: str = ThemeColors.ACCENT
    
    # Box style
    box_style: BoxStyle = BoxStyle.ROUNDED
    
    # Effects
    use_gradient: bool = False
    use_bold_titles: bool = True
    use_dim_borders: bool = False
    
    # Animation
    typing_speed: float = 0.03  # seconds per character
    spinner_style: str = "dots"  # dots, line, arc, etc.
    
    @property
    def box(self) -> Box:
        """Get Rich box object for this theme"""
        return BOX_STYLES.get(self.box_style, ROUNDED)


# Default retro theme
DEFAULT_THEME = ThemeStyle(
    primary=ThemeColors.NEON_BLUE,
    secondary=ThemeColors.NEON_PINK,
    accent=ThemeColors.RETRO_AMBER,
    box_style=BoxStyle.ROUNDED,
    use_gradient=True,
    use_bold_titles=True,
)


# Alternative themes
CLASSIC_THEME = ThemeStyle(
    primary=ThemeColors.RETRO_GREEN,
    secondary=ThemeColors.RETRO_AMBER,
    accent=ThemeColors.PRIMARY,
    box_style=BoxStyle.DOUBLE,
    use_gradient=False,
)


NEON_THEME = ThemeStyle(
    primary=ThemeColors.NEON_PINK,
    secondary=ThemeColors.NEON_GREEN,
    accent=ThemeColors.NEON_BLUE,
    box_style=BoxStyle.HEAVY,
    use_gradient=True,
)


class ThemedConsole:
    """Rich console wrapper with theme support"""
    
    def __init__(self, theme: Optional[ThemeStyle] = None, **console_kwargs):
        """
        Initialize themed console
        
        Args:
            theme: Theme style configuration
            **console_kwargs: Additional Rich Console arguments
        """
        self.theme = theme or DEFAULT_THEME
        
        # Create Rich theme
        rich_theme = Theme({
            "info": ThemeColors.INFO,
            "success": ThemeColors.SUCCESS,
            "warning": ThemeColors.WARNING,
            "error": ThemeColors.ERROR,
            "primary": self.theme.primary,
            "secondary": self.theme.secondary,
            "accent": self.theme.accent,
            "highlight": ThemeColors.HIGHLIGHT,
            "dim": ThemeColors.DIM,
            "muted": ThemeColors.MUTED,
            "border": ThemeColors.BORDER,
            "title": ThemeColors.TITLE,
            "subtitle": ThemeColors.SUBTITLE,
            "prompt": ThemeColors.PROMPT,
        })
        
        # Initialize Rich console
        self.console = Console(theme=rich_theme, **console_kwargs)
    
    def print(self, *args, **kwargs):
        """Print with theme colors"""
        self.console.print(*args, **kwargs)
    
    def print_success(self, message: str, **kwargs):
        """Print success message"""
        self.console.print(f"✓ {message}", style="success", **kwargs)
    
    def print_error(self, message: str, **kwargs):
        """Print error message"""
        self.console.print(f"✗ {message}", style="error", **kwargs)
    
    def print_warning(self, message: str, **kwargs):
        """Print warning message"""
        self.console.print(f"⚠ {message}", style="warning", **kwargs)
    
    def print_info(self, message: str, **kwargs):
        """Print info message"""
        self.console.print(f"ℹ {message}", style="info", **kwargs)
    
    def panel(
        self,
        content: Any,
        title: Optional[str] = None,
        subtitle: Optional[str] = None,
        border_style: Optional[str] = None,
        **kwargs
    ) -> Panel:
        """
        Create themed panel
        
        Args:
            content: Panel content
            title: Optional title
            subtitle: Optional subtitle
            border_style: Optional border color override
            **kwargs: Additional Panel arguments
            
        Returns:
            Rich Panel object
        """
        border_style = border_style or self.theme.primary
        
        return Panel(
            content,
            title=title,
            subtitle=subtitle,
            border_style=border_style,
            box=self.theme.box,
            **kwargs
        )
    
    def table(
        self,
        title: Optional[str] = None,
        border_style: Optional[str] = None,
        header_style: Optional[str] = None,
        **kwargs
    ) -> Table:
        """
        Create themed table
        
        Args:
            title: Optional table title
            border_style: Optional border color override
            header_style: Optional header style override
            **kwargs: Additional Table arguments
            
        Returns:
            Rich Table object
        """
        border_style = border_style or self.theme.primary
        header_style = header_style or f"bold {self.theme.secondary}"
        
        return Table(
            title=title,
            border_style=border_style,
            header_style=header_style,
            box=self.theme.box,
            **kwargs
        )
    
    def progress(
        self,
        *columns,
        transient: bool = False,
        **kwargs
    ) -> Progress:
        """
        Create themed progress bar
        
        Args:
            *columns: Progress columns
            transient: Whether progress should disappear when complete
            **kwargs: Additional Progress arguments
            
        Returns:
            Rich Progress object
        """
        if not columns:
            columns = (
                SpinnerColumn(self.theme.spinner_style),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(
                    complete_style=self.theme.primary,
                    finished_style=ThemeColors.SUCCESS,
                ),
                TaskProgressColumn(),
                TimeRemainingColumn(),
            )
        
        return Progress(*columns, transient=transient, **kwargs)
    
    def styled_text(
        self,
        text: str,
        style: Optional[str] = None,
        justify: Optional[str] = None,
        **kwargs
    ) -> Text:
        """
        Create styled text
        
        Args:
            text: Text content
            style: Rich style string
            justify: Text justification
            **kwargs: Additional Text arguments
            
        Returns:
            Rich Text object
        """
        return Text(text, style=style, justify=justify, **kwargs)
    
    def rule(self, title: Optional[str] = None, **kwargs):
        """Print horizontal rule with optional title"""
        self.console.rule(title, style=self.theme.primary, **kwargs)
    
    def clear(self):
        """Clear console"""
        self.console.clear()
    
    def status(self, message: str, spinner: Optional[str] = None):
        """
        Create status context manager with spinner
        
        Args:
            message: Status message
            spinner: Spinner style (default: theme spinner)
            
        Returns:
            Rich status context manager
        """
        spinner = spinner or self.theme.spinner_style
        return self.console.status(message, spinner=spinner)


# Singleton console instance
_console_instance: Optional[ThemedConsole] = None


def get_console(theme: Optional[ThemeStyle] = None) -> ThemedConsole:
    """
    Get singleton themed console instance
    
    Args:
        theme: Optional theme to use (only used on first call)
        
    Returns:
        Themed console instance
    """
    global _console_instance
    
    if _console_instance is None:
        _console_instance = ThemedConsole(theme=theme)
    
    return _console_instance


def set_theme(theme: ThemeStyle):
    """
    Set global theme (recreates console)
    
    Args:
        theme: New theme to use
    """
    global _console_instance
    _console_instance = ThemedConsole(theme=theme)


# Convenience functions

def styled_text(
    text: str,
    style: Optional[str] = None,
    color: Optional[str] = None,
    bold: bool = False,
    italic: bool = False,
    underline: bool = False,
) -> Text:
    """
    Create styled text with convenience options
    
    Args:
        text: Text content
        style: Complete style string (overrides other options)
        color: Text color
        bold: Make text bold
        italic: Make text italic
        underline: Underline text
        
    Returns:
        Rich Text object
    """
    if not style:
        style_parts = []
        if color:
            style_parts.append(color)
        if bold:
            style_parts.append("bold")
        if italic:
            style_parts.append("italic")
        if underline:
            style_parts.append("underline")
        
        style = " ".join(style_parts) if style_parts else None
    
    return Text(text, style=style)


def platform_icon(platform: str) -> Text:
    """
    Get colored icon for platform
    
    Args:
        platform: Platform name (whatsapp, instagram, etc.)
        
    Returns:
        Styled platform icon
    """
    icons = {
        "whatsapp": ("💬", ThemeColors.WHATSAPP),
        "instagram": ("📸", ThemeColors.INSTAGRAM),
        "tiktok": ("🎵", ThemeColors.TIKTOK),
        "youtube": ("▶️", ThemeColors.YOUTUBE),
        "twitter": ("🐦", ThemeColors.TWITTER),
        "facebook": ("👤", ThemeColors.FACEBOOK),
    }
    
    icon, color = icons.get(platform.lower(), ("📱", ThemeColors.INFO))
    return styled_text(icon, color=color)


def status_icon(status: str) -> Text:
    """
    Get colored icon for status
    
    Args:
        status: Status name (success, error, warning, info, running, stopped)
        
    Returns:
        Styled status icon
    """
    icons = {
        "success": ("✓", ThemeColors.SUCCESS),
        "error": ("✗", ThemeColors.ERROR),
        "warning": ("⚠", ThemeColors.WARNING),
        "info": ("ℹ", ThemeColors.INFO),
        "running": ("▶", ThemeColors.SUCCESS),
        "stopped": ("■", ThemeColors.ERROR),
        "paused": ("⏸", ThemeColors.WARNING),
        "pending": ("⏳", ThemeColors.INFO),
    }
    
    icon, color = icons.get(status.lower(), ("•", ThemeColors.MUTED))
    return styled_text(icon, color=color)


# Export public API
__all__ = [
    "ThemeColors",
    "BoxStyle",
    "ThemeStyle",
    "ThemedConsole",
    "DEFAULT_THEME",
    "CLASSIC_THEME",
    "NEON_THEME",
    "get_console",
    "set_theme",
    "styled_text",
    "platform_icon",
    "status_icon",
]
