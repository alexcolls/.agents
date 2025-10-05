"""
Agent Management Core

Handles creation, storage, and lifecycle management of automation agents.
Agents are stored as encrypted JSON files with credentials secured using
the encryption module.

Classes:
    AgentStatus: Agent status enum
    Agent: Main agent class with configuration and state
    AgentManager: Manages multiple agents, CRUD operations
    
Functions:
    load_agent: Load agent from file
    save_agent: Save agent to file
    list_agents: Get all configured agents
"""

import json
from enum import Enum
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
from dataclasses import dataclass, field, asdict

from src.utils.config import get_config
from src.utils.constants import AGENTS_DIR
from src.utils.logger import get_logger, LoggerMixin
from src.utils.helpers import generate_password, sanitize_filename
from src.security.validators import InputValidator
from src.security.encryption import Encryptor


logger = get_logger(__name__)


class AgentStatus(str, Enum):
    """Agent status states"""
    
    STOPPED = "stopped"
    RUNNING = "running"
    PAUSED = "paused"
    ERROR = "error"
    STARTING = "starting"
    STOPPING = "stopping"


@dataclass
class AgentConfig:
    """Agent configuration"""
    
    # Identity
    name: str
    description: str = ""
    
    # WhatsApp configuration
    whatsapp_phone: str = ""
    whatsapp_groups: List[str] = field(default_factory=list)
    
    # Target platforms and credentials (encrypted)
    platforms: Dict[str, Dict[str, str]] = field(default_factory=dict)
    
    # Posting configuration
    auto_caption: bool = True
    default_caption: str = ""
    hashtags: List[str] = field(default_factory=list)
    
    # Scheduling
    check_interval_minutes: int = 5
    
    # Metadata
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentConfig":
        """Create from dictionary"""
        return cls(**data)
    
    def update_timestamp(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow().isoformat()


class Agent(LoggerMixin):
    """
    Automation Agent
    
    Represents a configured automation agent with WhatsApp monitoring
    and social media posting capabilities.
    """
    
    def __init__(
        self,
        config: AgentConfig,
        encryption_manager: Optional[Encryptor] = None,
    ):
        """
        Initialize agent
        
        Args:
            config: Agent configuration
            encryption_manager: Optional encryption manager (created if not provided)
        """
        self.config = config
        self.status = AgentStatus.STOPPED
        self.encryption_manager = encryption_manager
        
        # Runtime state
        self.pid: Optional[int] = None
        self.last_check: Optional[datetime] = None
        self.last_post: Optional[datetime] = None
        self.total_posts: int = 0
        self.errors: List[str] = []
        
        # Validate configuration
        self._validate_config()
        
        self.log_info(f"Agent '{self.config.name}' initialized")
    
    def _validate_config(self):
        """Validate agent configuration"""
        try:
            InputValidator.validate_agent_name(self.config.name)
        except Exception as e:
            raise ValueError(f"Invalid agent name: {self.config.name} - {e}")
        
        for platform in self.config.platforms.keys():
            try:
                InputValidator.validate_platform(platform)
            except Exception as e:
                raise ValueError(f"Invalid platform: {platform} - {e}")
    
    @property
    def name(self) -> str:
        """Get agent name"""
        return self.config.name
    
    @property
    def is_running(self) -> bool:
        """Check if agent is running"""
        return self.status == AgentStatus.RUNNING
    
    @property
    def is_stopped(self) -> bool:
        """Check if agent is stopped"""
        return self.status == AgentStatus.STOPPED
    
    def get_credentials(self, platform: str) -> Optional[Dict[str, str]]:
        """
        Get decrypted credentials for platform
        
        Args:
            platform: Platform name
            
        Returns:
            Decrypted credentials or None
        """
        if platform not in self.config.platforms:
            return None
        
        encrypted_creds = self.config.platforms[platform]
        
        if self.encryption_manager:
            try:
                return self.encryption_manager.decrypt_credentials(encrypted_creds)
            except Exception as e:
                self.log_error(f"Failed to decrypt {platform} credentials: {e}")
                return None
        
        return encrypted_creds
    
    def set_credentials(self, platform: str, username: str, password: str):
        """
        Set encrypted credentials for platform
        
        Args:
            platform: Platform name
            username: Username
            password: Password
        """
        try:
            InputValidator.validate_platform(platform)
        except Exception as e:
            raise ValueError(f"Invalid platform: {platform} - {e}")
        
        credentials = {
            "username": username,
            "password": password,
        }
        
        if self.encryption_manager:
            try:
                encrypted_creds = self.encryption_manager.encrypt_credentials(credentials)
                self.config.platforms[platform] = encrypted_creds
                self.log_info(f"Encrypted credentials set for {platform}")
            except Exception as e:
                self.log_error(f"Failed to encrypt {platform} credentials: {e}")
                raise
        else:
            self.config.platforms[platform] = credentials
            self.log_warning(f"Credentials for {platform} stored unencrypted!")
        
        self.config.update_timestamp()
    
    def remove_platform(self, platform: str):
        """
        Remove platform from agent
        
        Args:
            platform: Platform name
        """
        if platform in self.config.platforms:
            del self.config.platforms[platform]
            self.config.update_timestamp()
            self.log_info(f"Removed platform: {platform}")
    
    def start(self):
        """Start agent (to be implemented in orchestrator)"""
        self.log_info(f"Starting agent '{self.name}'")
        self.status = AgentStatus.STARTING
    
    def stop(self):
        """Stop agent (to be implemented in orchestrator)"""
        self.log_info(f"Stopping agent '{self.name}'")
        self.status = AgentStatus.STOPPING
    
    def pause(self):
        """Pause agent"""
        if self.is_running:
            self.log_info(f"Pausing agent '{self.name}'")
            self.status = AgentStatus.PAUSED
    
    def resume(self):
        """Resume agent"""
        if self.status == AgentStatus.PAUSED:
            self.log_info(f"Resuming agent '{self.name}'")
            self.status = AgentStatus.RUNNING
    
    def add_error(self, error: str):
        """Add error to agent error log"""
        self.errors.append(f"{datetime.utcnow().isoformat()}: {error}")
        self.log_error(error)
    
    def clear_errors(self):
        """Clear error log"""
        self.errors.clear()
    
    def to_dict(self, include_credentials: bool = False) -> Dict[str, Any]:
        """
        Convert agent to dictionary
        
        Args:
            include_credentials: Whether to include credentials (encrypted)
            
        Returns:
            Agent data dictionary
        """
        data = {
            "config": self.config.to_dict(),
            "status": self.status,
            "pid": self.pid,
            "last_check": self.last_check.isoformat() if self.last_check else None,
            "last_post": self.last_post.isoformat() if self.last_post else None,
            "total_posts": self.total_posts,
            "errors": self.errors[-10:],  # Last 10 errors only
        }
        
        if not include_credentials:
            # Remove credentials from platforms
            config_copy = data["config"].copy()
            config_copy["platforms"] = {
                platform: {"username": creds.get("username", "")}
                for platform, creds in config_copy["platforms"].items()
            }
            data["config"] = config_copy
        
        return data
    
    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
        encryption_manager: Optional[Encryptor] = None,
    ) -> "Agent":
        """
        Create agent from dictionary
        
        Args:
            data: Agent data dictionary
            encryption_manager: Optional encryption manager
            
        Returns:
            Agent instance
        """
        config = AgentConfig.from_dict(data["config"])
        agent = cls(config, encryption_manager)
        
        # Restore runtime state
        agent.status = AgentStatus(data.get("status", AgentStatus.STOPPED))
        agent.pid = data.get("pid")
        agent.total_posts = data.get("total_posts", 0)
        agent.errors = data.get("errors", [])
        
        if data.get("last_check"):
            agent.last_check = datetime.fromisoformat(data["last_check"])
        if data.get("last_post"):
            agent.last_post = datetime.fromisoformat(data["last_post"])
        
        return agent


class AgentManager(LoggerMixin):
    """
    Manages multiple agents
    
    Provides CRUD operations for agents with encrypted storage.
    """
    
    def __init__(
        self,
        storage_dir: Optional[Path] = None,
        encryption_manager: Optional[Encryptor] = None,
    ):
        """
        Initialize agent manager
        
        Args:
            storage_dir: Directory to store agent files
            encryption_manager: Encryption manager for credentials
        """
        self.storage_dir = storage_dir or AGENTS_DIR
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        self.encryption_manager = encryption_manager
        self.agents: Dict[str, Agent] = {}
        
        self.log_info(f"AgentManager initialized with storage: {self.storage_dir}")
    
    def _get_agent_file(self, name: str) -> Path:
        """
        Get agent file path
        
        Args:
            name: Agent name
            
        Returns:
            Path to agent file
        """
        safe_name = sanitize_filename(name)
        return self.storage_dir / f"{safe_name}.json"
    
    def create_agent(self, config: AgentConfig) -> Agent:
        """
        Create new agent
        
        Args:
            config: Agent configuration
            
        Returns:
            Created agent
        """
        if self.agent_exists(config.name):
            raise ValueError(f"Agent '{config.name}' already exists")
        
        agent = Agent(config, self.encryption_manager)
        self.agents[config.name] = agent
        
        self.save_agent(agent)
        
        self.log_info(f"Created agent: {config.name}")
        return agent
    
    def load_agent(self, name: str) -> Optional[Agent]:
        """
        Load agent from file
        
        Args:
            name: Agent name
            
        Returns:
            Loaded agent or None if not found
        """
        agent_file = self._get_agent_file(name)
        
        if not agent_file.exists():
            self.log_warning(f"Agent file not found: {agent_file}")
            return None
        
        try:
            with open(agent_file, "r") as f:
                data = json.load(f)
            
            agent = Agent.from_dict(data, self.encryption_manager)
            self.agents[name] = agent
            
            self.log_info(f"Loaded agent: {name}")
            return agent
            
        except Exception as e:
            self.log_error(f"Failed to load agent '{name}': {e}")
            return None
    
    def save_agent(self, agent: Agent):
        """
        Save agent to file
        
        Args:
            agent: Agent to save
        """
        agent_file = self._get_agent_file(agent.name)
        
        try:
            # Update timestamp
            agent.config.update_timestamp()
            
            # Save with credentials
            data = agent.to_dict(include_credentials=True)
            
            with open(agent_file, "w") as f:
                json.dump(data, f, indent=2)
            
            self.log_info(f"Saved agent: {agent.name}")
            
        except Exception as e:
            self.log_error(f"Failed to save agent '{agent.name}': {e}")
            raise
    
    def delete_agent(self, name: str) -> bool:
        """
        Delete agent
        
        Args:
            name: Agent name
            
        Returns:
            True if deleted, False if not found
        """
        agent_file = self._get_agent_file(name)
        
        if not agent_file.exists():
            self.log_warning(f"Agent not found: {name}")
            return False
        
        try:
            # Remove from memory
            if name in self.agents:
                del self.agents[name]
            
            # Delete file
            agent_file.unlink()
            
            self.log_info(f"Deleted agent: {name}")
            return True
            
        except Exception as e:
            self.log_error(f"Failed to delete agent '{name}': {e}")
            raise
    
    def list_agents(self) -> List[Agent]:
        """
        List all agents
        
        Returns:
            List of all agents
        """
        # Load all agent files
        for agent_file in self.storage_dir.glob("*.json"):
            name = agent_file.stem
            if name not in self.agents:
                self.load_agent(name)
        
        return list(self.agents.values())
    
    def get_agent(self, name: str) -> Optional[Agent]:
        """
        Get agent by name
        
        Args:
            name: Agent name
            
        Returns:
            Agent or None if not found
        """
        if name in self.agents:
            return self.agents[name]
        
        return self.load_agent(name)
    
    def agent_exists(self, name: str) -> bool:
        """
        Check if agent exists
        
        Args:
            name: Agent name
            
        Returns:
            True if agent exists
        """
        return self._get_agent_file(name).exists()
    
    def get_running_agents(self) -> List[Agent]:
        """
        Get all running agents
        
        Returns:
            List of running agents
        """
        return [
            agent for agent in self.list_agents()
            if agent.is_running
        ]
    
    def stop_all_agents(self):
        """Stop all running agents"""
        for agent in self.get_running_agents():
            agent.stop()
            self.save_agent(agent)
        
        self.log_info("Stopped all agents")


# Convenience functions

def create_agent_from_form_data(
    form_data: Dict[str, Any],
    encryption_manager: Optional[Encryptor] = None,
) -> Agent:
    """
    Create agent from menu form data
    
    Args:
        form_data: Form data from agent_form()
        encryption_manager: Optional encryption manager
        
    Returns:
        Created agent
    """
    # Build config
    config = AgentConfig(
        name=form_data["name"],
        description=form_data.get("description", ""),
        whatsapp_phone=form_data["whatsapp"]["phone"],
        whatsapp_groups=form_data["whatsapp"]["groups"],
        auto_caption=form_data.get("auto_caption", True),
        default_caption=form_data.get("default_caption", ""),
        hashtags=form_data.get("hashtags", []),
        check_interval_minutes=form_data.get("check_interval_minutes", 5),
    )
    
    # Create agent
    agent = Agent(config, encryption_manager)
    
    # Set credentials
    for platform, creds in form_data["platforms"].items():
        if "password" in creds:
            agent.set_credentials(
                platform,
                creds["username"],
                creds["password"],
            )
    
    return agent


# Export public API
__all__ = [
    "AgentStatus",
    "AgentConfig",
    "Agent",
    "AgentManager",
    "create_agent_from_form_data",
]
