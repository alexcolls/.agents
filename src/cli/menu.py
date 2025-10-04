"""
CLI Interactive Menu System

Provides questionary-based interactive menus with retro styling, keyboard
navigation, and user-friendly prompts for agent configuration and management.

Functions:
    main_menu: Display main menu with agent operations
    confirm: Ask yes/no confirmation
    text_input: Get text input with validation
    password_input: Get password with masking
    select: Single selection from options
    multiselect: Multiple selection from options
    agent_form: Interactive form for creating/editing agents
"""

from typing import Optional, List, Dict, Any, Callable
from pathlib import Path

import questionary
from questionary import Style

from src.utils.constants import SUPPORTED_PLATFORMS, Messages
from src.utils.validators import (
    validate_agent_name,
    validate_username,
    validate_password,
    validate_platform,
)
from src.cli.theme import ThemeColors


# Custom questionary style matching our retro theme
RETRO_STYLE = Style([
    ('qmark', f'fg:{ThemeColors.NEON_BLUE} bold'),           # Question mark
    ('question', f'fg:{ThemeColors.NEON_PINK} bold'),        # Question text
    ('answer', f'fg:{ThemeColors.SUCCESS} bold'),            # Answer text
    ('pointer', f'fg:{ThemeColors.RETRO_AMBER} bold'),       # Selection pointer
    ('highlighted', f'fg:{ThemeColors.NEON_BLUE} bold'),     # Highlighted option
    ('selected', f'fg:{ThemeColors.SUCCESS}'),               # Selected items
    ('separator', f'fg:{ThemeColors.MUTED}'),                # Separators
    ('instruction', f'fg:{ThemeColors.INFO}'),               # Instructions
    ('text', f'fg:{ThemeColors.PRIMARY}'),                   # Regular text
    ('disabled', f'fg:{ThemeColors.MUTED} italic'),          # Disabled options
])


class MenuChoice:
    """Menu choice with title, value, and optional metadata"""
    
    def __init__(
        self,
        title: str,
        value: Any,
        description: Optional[str] = None,
        disabled: bool = False,
    ):
        """
        Initialize menu choice
        
        Args:
            title: Display title
            value: Return value when selected
            description: Optional description
            disabled: Whether choice is disabled
        """
        self.title = title
        self.value = value
        self.description = description
        self.disabled = disabled
    
    def __str__(self) -> str:
        """String representation for questionary"""
        if self.description:
            return f"{self.title} - {self.description}"
        return self.title


def main_menu() -> str:
    """
    Display main menu and get user choice
    
    Returns:
        Selected menu action
    """
    choices = [
        MenuChoice("📝 Create New Agent", "create", "Set up a new automation agent"),
        MenuChoice("📋 List Agents", "list", "View all configured agents"),
        MenuChoice("▶️  Start Agent", "start", "Start monitoring and posting"),
        MenuChoice("⏹️  Stop Agent", "stop", "Stop a running agent"),
        MenuChoice("✏️  Edit Agent", "edit", "Modify agent configuration"),
        MenuChoice("🗑️  Delete Agent", "delete", "Remove an agent"),
        MenuChoice("📊 View Status", "status", "Check agent status and logs"),
        MenuChoice("⚙️  Settings", "settings", "Configure global settings"),
        MenuChoice("❓ Help", "help", "View documentation"),
        MenuChoice("🚪 Exit", "exit", "Quit .agents"),
    ]
    
    answer = questionary.select(
        "What would you like to do?",
        choices=[str(choice) for choice in choices],
        style=RETRO_STYLE,
        use_shortcuts=True,
        use_arrow_keys=True,
    ).ask()
    
    # Find matching choice value
    for choice in choices:
        if str(choice) == answer:
            return choice.value
    
    return "exit"


def confirm(
    message: str,
    default: bool = False,
    auto_enter: bool = True,
) -> bool:
    """
    Ask yes/no confirmation
    
    Args:
        message: Confirmation message
        default: Default value if user presses enter
        auto_enter: Whether pressing enter accepts default
        
    Returns:
        True if confirmed, False otherwise
    """
    return questionary.confirm(
        message,
        default=default,
        auto_enter=auto_enter,
        style=RETRO_STYLE,
    ).ask()


def text_input(
    message: str,
    default: str = "",
    validator: Optional[Callable[[str], bool]] = None,
    validate_message: Optional[str] = None,
    multiline: bool = False,
) -> Optional[str]:
    """
    Get text input with validation
    
    Args:
        message: Input prompt message
        default: Default value
        validator: Optional validation function
        validate_message: Error message for validation failure
        multiline: Whether to allow multiline input
        
    Returns:
        User input or None if cancelled
    """
    # Create validator wrapper if provided
    questionary_validator = None
    if validator:
        def validate_wrapper(text: str) -> bool:
            try:
                return validator(text)
            except Exception:
                return False
        
        questionary_validator = lambda x: (
            validate_wrapper(x) or (validate_message or "Invalid input")
        )
    
    result = questionary.text(
        message,
        default=default,
        validate=questionary_validator,
        multiline=multiline,
        style=RETRO_STYLE,
    ).ask()
    
    return result


def password_input(
    message: str,
    validator: Optional[Callable[[str], bool]] = None,
    validate_message: Optional[str] = None,
) -> Optional[str]:
    """
    Get password input with masking
    
    Args:
        message: Input prompt message
        validator: Optional validation function
        validate_message: Error message for validation failure
        
    Returns:
        Password or None if cancelled
    """
    # Create validator wrapper if provided
    questionary_validator = None
    if validator:
        def validate_wrapper(text: str) -> bool:
            try:
                return validator(text)
            except Exception:
                return False
        
        questionary_validator = lambda x: (
            validate_wrapper(x) or (validate_message or "Invalid password")
        )
    
    result = questionary.password(
        message,
        validate=questionary_validator,
        style=RETRO_STYLE,
    ).ask()
    
    return result


def select(
    message: str,
    choices: List[Any],
    default: Optional[Any] = None,
    use_shortcuts: bool = True,
) -> Optional[Any]:
    """
    Single selection from options
    
    Args:
        message: Selection prompt message
        choices: List of choices (strings or MenuChoice objects)
        default: Default selected choice
        use_shortcuts: Whether to enable keyboard shortcuts
        
    Returns:
        Selected choice or None if cancelled
    """
    # Convert to MenuChoice if needed
    menu_choices = []
    for choice in choices:
        if isinstance(choice, MenuChoice):
            menu_choices.append(choice)
        else:
            menu_choices.append(MenuChoice(str(choice), choice))
    
    # Find default index
    default_idx = None
    if default is not None:
        for i, choice in enumerate(menu_choices):
            if choice.value == default:
                default_idx = i
                break
    
    answer = questionary.select(
        message,
        choices=[str(choice) for choice in menu_choices],
        default=str(menu_choices[default_idx]) if default_idx is not None else None,
        style=RETRO_STYLE,
        use_shortcuts=use_shortcuts,
        use_arrow_keys=True,
    ).ask()
    
    # Find matching choice value
    for choice in menu_choices:
        if str(choice) == answer:
            return choice.value
    
    return None


def multiselect(
    message: str,
    choices: List[Any],
    defaults: Optional[List[Any]] = None,
) -> Optional[List[Any]]:
    """
    Multiple selection from options
    
    Args:
        message: Selection prompt message
        choices: List of choices (strings or MenuChoice objects)
        defaults: List of default selected choices
        
    Returns:
        List of selected choices or None if cancelled
    """
    # Convert to MenuChoice if needed
    menu_choices = []
    for choice in choices:
        if isinstance(choice, MenuChoice):
            menu_choices.append(choice)
        else:
            menu_choices.append(MenuChoice(str(choice), choice))
    
    # Find default selections
    default_strs = []
    if defaults:
        for choice in menu_choices:
            if choice.value in defaults:
                default_strs.append(str(choice))
    
    answers = questionary.checkbox(
        message,
        choices=[str(choice) for choice in menu_choices],
        default=default_strs if default_strs else None,
        style=RETRO_STYLE,
    ).ask()
    
    # Find matching choice values
    selected_values = []
    for answer in answers:
        for choice in menu_choices:
            if str(choice) == answer:
                selected_values.append(choice.value)
                break
    
    return selected_values if selected_values else None


def agent_form(
    agent_data: Optional[Dict[str, Any]] = None,
    edit_mode: bool = False,
) -> Optional[Dict[str, Any]]:
    """
    Interactive form for creating/editing agents
    
    Args:
        agent_data: Existing agent data (for edit mode)
        edit_mode: Whether in edit mode
        
    Returns:
        Agent configuration dict or None if cancelled
    """
    agent_data = agent_data or {}
    config = {}
    
    # Agent name
    if not edit_mode:
        name = text_input(
            "Agent name:",
            default=agent_data.get("name", ""),
            validator=validate_agent_name,
            validate_message="Invalid agent name. Use letters, numbers, - and _",
        )
        if name is None:
            return None
        config["name"] = name
    else:
        config["name"] = agent_data.get("name")
    
    # Description
    description = text_input(
        "Agent description (optional):",
        default=agent_data.get("description", ""),
    )
    if description is None:
        return None
    config["description"] = description
    
    # WhatsApp configuration
    print("\n" + "="*50)
    print("📱 WhatsApp Configuration")
    print("="*50 + "\n")
    
    whatsapp_phone = text_input(
        "WhatsApp phone number (with country code, e.g., +1234567890):",
        default=agent_data.get("whatsapp", {}).get("phone", ""),
    )
    if whatsapp_phone is None:
        return None
    
    whatsapp_groups = text_input(
        "WhatsApp groups to monitor (comma-separated names or IDs):",
        default=", ".join(agent_data.get("whatsapp", {}).get("groups", [])),
    )
    if whatsapp_groups is None:
        return None
    
    groups_list = [g.strip() for g in whatsapp_groups.split(",") if g.strip()]
    
    config["whatsapp"] = {
        "phone": whatsapp_phone,
        "groups": groups_list,
    }
    
    # Target platforms
    print("\n" + "="*50)
    print("🎯 Target Social Media Platforms")
    print("="*50 + "\n")
    
    platform_choices = [
        MenuChoice(
            f"📸 {platform.title()}",
            platform,
            f"Post videos to {platform.title()}"
        )
        for platform in SUPPORTED_PLATFORMS
    ]
    
    selected_platforms = multiselect(
        "Select platforms to post to:",
        platform_choices,
        defaults=agent_data.get("platforms", {}).keys(),
    )
    
    if selected_platforms is None:
        return None
    
    # Platform credentials
    config["platforms"] = {}
    
    for platform in selected_platforms:
        print(f"\n📝 {platform.title()} Account Configuration")
        print("-" * 50)
        
        username = text_input(
            f"{platform.title()} username:",
            default=agent_data.get("platforms", {}).get(platform, {}).get("username", ""),
            validator=validate_username,
            validate_message="Invalid username",
        )
        if username is None:
            return None
        
        # Only ask for password if not in edit mode or if user wants to change
        password = None
        if edit_mode and agent_data.get("platforms", {}).get(platform):
            change_password = confirm(
                f"Change {platform.title()} password?",
                default=False,
            )
            if change_password:
                password = password_input(
                    f"{platform.title()} password:",
                    validator=validate_password,
                    validate_message="Password must be at least 6 characters",
                )
                if password is None:
                    return None
        else:
            password = password_input(
                f"{platform.title()} password:",
                validator=validate_password,
                validate_message="Password must be at least 6 characters",
            )
            if password is None:
                return None
        
        config["platforms"][platform] = {
            "username": username,
        }
        
        if password:
            config["platforms"][platform]["password"] = password
    
    # Posting configuration
    print("\n" + "="*50)
    print("⚙️  Posting Configuration")
    print("="*50 + "\n")
    
    auto_caption = confirm(
        "Generate automatic captions from video content?",
        default=agent_data.get("auto_caption", True),
    )
    config["auto_caption"] = auto_caption
    
    if not auto_caption:
        default_caption = text_input(
            "Default caption template (use {group_name}, {date}, etc.):",
            default=agent_data.get("default_caption", ""),
            multiline=True,
        )
        if default_caption is None:
            return None
        config["default_caption"] = default_caption
    
    hashtags = text_input(
        "Default hashtags (comma-separated):",
        default=", ".join(agent_data.get("hashtags", [])),
    )
    if hashtags is None:
        return None
    
    config["hashtags"] = [tag.strip() for tag in hashtags.split(",") if tag.strip()]
    
    # Scheduling
    check_interval = text_input(
        "Check for new videos every (minutes):",
        default=str(agent_data.get("check_interval_minutes", 5)),
    )
    if check_interval is None:
        return None
    
    try:
        config["check_interval_minutes"] = int(check_interval)
    except ValueError:
        config["check_interval_minutes"] = 5
    
    return config


def select_agent(agents: List[Dict[str, Any]]) -> Optional[str]:
    """
    Select an agent from list
    
    Args:
        agents: List of agent configurations
        
    Returns:
        Selected agent name or None if cancelled
    """
    if not agents:
        print("No agents configured yet.")
        return None
    
    choices = [
        MenuChoice(
            f"{agent['name']}",
            agent['name'],
            agent.get('description', 'No description')
        )
        for agent in agents
    ]
    
    return select(
        "Select an agent:",
        choices,
    )


def path_input(
    message: str,
    default: str = "",
    must_exist: bool = False,
) -> Optional[Path]:
    """
    Get file/directory path input
    
    Args:
        message: Input prompt message
        default: Default path
        must_exist: Whether path must exist
        
    Returns:
        Path object or None if cancelled
    """
    result = questionary.path(
        message,
        default=default,
        style=RETRO_STYLE,
    ).ask()
    
    if result is None:
        return None
    
    path = Path(result).expanduser().resolve()
    
    if must_exist and not path.exists():
        print(f"Error: Path does not exist: {path}")
        return None
    
    return path


# Export public API
__all__ = [
    "RETRO_STYLE",
    "MenuChoice",
    "main_menu",
    "confirm",
    "text_input",
    "password_input",
    "select",
    "multiselect",
    "agent_form",
    "select_agent",
    "path_input",
]
