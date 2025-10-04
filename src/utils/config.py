"""
Configuration management for .agents application.

Loads and validates environment variables from .env file.
"""

import os
from pathlib import Path
from typing import Any, Optional

from dotenv import load_dotenv

from src.utils.constants import (
    BASE_DIR,
    DEFAULT_CHECK_INTERVAL_MINUTES,
    DEFAULT_INSTAGRAM_REQUEST_DELAY,
    DEFAULT_INSTAGRAM_UPLOAD_TIMEOUT,
    DEFAULT_INSTAGRAM_VERIFICATION_METHOD,
    DEFAULT_KEEP_ORIGINAL_VIDEOS,
    DEFAULT_LOG_BACKUP_COUNT,
    DEFAULT_LOG_FORMAT,
    DEFAULT_LOG_LEVEL,
    DEFAULT_LOG_MAX_SIZE_MB,
    DEFAULT_MAX_CONCURRENT_UPLOADS,
    DEFAULT_MAX_RETRY_ATTEMPTS,
    DEFAULT_MAX_VIDEO_SIZE_MB,
    DEFAULT_NETWORK_TIMEOUT,
    DEFAULT_TIKTOK_REQUEST_DELAY,
    DEFAULT_TIKTOK_UPLOAD_TIMEOUT,
    DEFAULT_USER_AGENT,
    DEFAULT_VIDEO_QUALITY,
    DEFAULT_YOUTUBE_UPLOAD_TIMEOUT,
    PASSWORD_MIN_LENGTH,
)


class ConfigError(Exception):
    """Raised when configuration is invalid or missing."""
    pass


class Config:
    """
    Application configuration loaded from environment variables.
    
    All configuration is loaded from the .env file at project root.
    """
    
    def __init__(self, env_file: Optional[Path] = None):
        """
        Initialize configuration.
        
        Args:
            env_file: Path to .env file. If None, uses project root .env
        """
        if env_file is None:
            env_file = BASE_DIR / ".env"
        
        if not env_file.exists():
            raise ConfigError(
                f"Configuration file not found: {env_file}\n"
                f"Please copy .env.sample to .env and configure it."
            )
        
        # Load environment variables
        load_dotenv(env_file)
        
        # Validate critical configuration
        self._validate()
    
    # ========================================================================
    # SECURITY
    # ========================================================================
    
    @property
    def master_password(self) -> str:
        """Master password for encrypting credentials."""
        password = os.getenv("MASTER_PASSWORD", "")
        if not password or password == "CHANGE_THIS_TO_A_VERY_LONG_RANDOM_PASSWORD_MINIMUM_20_CHARS":
            raise ConfigError(
                "MASTER_PASSWORD not set in .env file!\n"
                "This is required to encrypt all credentials.\n"
                "Please set a strong password (20+ characters)."
            )
        if len(password) < PASSWORD_MIN_LENGTH:
            raise ConfigError(
                f"MASTER_PASSWORD must be at least {PASSWORD_MIN_LENGTH} characters long.\n"
                f"Current length: {len(password)}"
            )
        return password
    
    @property
    def encryption_algorithm(self) -> str:
        """Encryption algorithm to use."""
        return os.getenv("ENCRYPTION_ALGORITHM", "AES256")
    
    # ========================================================================
    # APPLICATION SETTINGS
    # ========================================================================
    
    @property
    def check_interval_minutes(self) -> int:
        """How often to check WhatsApp groups for new videos (in minutes)."""
        return self._get_int("CHECK_INTERVAL_MINUTES", DEFAULT_CHECK_INTERVAL_MINUTES)
    
    @property
    def max_concurrent_uploads(self) -> int:
        """Maximum number of concurrent uploads per agent."""
        return self._get_int("MAX_CONCURRENT_UPLOADS", DEFAULT_MAX_CONCURRENT_UPLOADS)
    
    @property
    def max_retry_attempts(self) -> int:
        """Number of retry attempts for failed operations."""
        return self._get_int("MAX_RETRY_ATTEMPTS", DEFAULT_MAX_RETRY_ATTEMPTS)
    
    @property
    def network_timeout(self) -> int:
        """Timeout for network operations (in seconds)."""
        return self._get_int("NETWORK_TIMEOUT", DEFAULT_NETWORK_TIMEOUT)
    
    # ========================================================================
    # WHATSAPP CONFIGURATION
    # ========================================================================
    
    @property
    def whatsapp_session_dir(self) -> Path:
        """Directory for storing WhatsApp session data."""
        dir_str = os.getenv("WHATSAPP_SESSION_DIR", "")
        if dir_str:
            return Path(dir_str)
        return BASE_DIR / ".agents" / "whatsapp_sessions"
    
    @property
    def qr_code_timeout(self) -> int:
        """How long to wait for user to scan QR code (seconds)."""
        return self._get_int("QR_CODE_TIMEOUT", 60)
    
    # ========================================================================
    # VIDEO DOWNLOAD SETTINGS
    # ========================================================================
    
    @property
    def temp_download_dir(self) -> Path:
        """Temporary directory for downloaded videos."""
        dir_str = os.getenv("TEMP_DOWNLOAD_DIR", "")
        if dir_str:
            return Path(dir_str)
        return BASE_DIR / ".agents" / "tmp"
    
    @property
    def max_video_size_mb(self) -> int:
        """Maximum video file size in MB."""
        return self._get_int("MAX_VIDEO_SIZE_MB", DEFAULT_MAX_VIDEO_SIZE_MB)
    
    @property
    def video_quality(self) -> str:
        """Video quality preference: best, high, medium, low."""
        quality = os.getenv("VIDEO_QUALITY", DEFAULT_VIDEO_QUALITY).lower()
        if quality not in ["best", "high", "medium", "low"]:
            return DEFAULT_VIDEO_QUALITY
        return quality
    
    @property
    def keep_original_videos(self) -> bool:
        """Whether to keep original videos after upload."""
        return self._get_bool("KEEP_ORIGINAL_VIDEOS", DEFAULT_KEEP_ORIGINAL_VIDEOS)
    
    # ========================================================================
    # INSTAGRAM SETTINGS
    # ========================================================================
    
    @property
    def instagram_request_delay(self) -> int:
        """Delay between Instagram requests (seconds)."""
        return self._get_int("INSTAGRAM_REQUEST_DELAY", DEFAULT_INSTAGRAM_REQUEST_DELAY)
    
    @property
    def instagram_upload_timeout(self) -> int:
        """Instagram upload timeout (seconds)."""
        return self._get_int("INSTAGRAM_UPLOAD_TIMEOUT", DEFAULT_INSTAGRAM_UPLOAD_TIMEOUT)
    
    @property
    def instagram_verification_method(self) -> str:
        """Instagram verification method: sms or email."""
        method = os.getenv("INSTAGRAM_VERIFICATION_METHOD", DEFAULT_INSTAGRAM_VERIFICATION_METHOD).lower()
        if method not in ["sms", "email"]:
            return DEFAULT_INSTAGRAM_VERIFICATION_METHOD
        return method
    
    @property
    def instagram_use_session_cache(self) -> bool:
        """Whether to use Instagram session cache."""
        return self._get_bool("INSTAGRAM_USE_SESSION_CACHE", True)
    
    # ========================================================================
    # TIKTOK SETTINGS
    # ========================================================================
    
    @property
    def tiktok_request_delay(self) -> int:
        """Delay between TikTok requests (seconds)."""
        return self._get_int("TIKTOK_REQUEST_DELAY", DEFAULT_TIKTOK_REQUEST_DELAY)
    
    @property
    def tiktok_upload_timeout(self) -> int:
        """TikTok upload timeout (seconds)."""
        return self._get_int("TIKTOK_UPLOAD_TIMEOUT", DEFAULT_TIKTOK_UPLOAD_TIMEOUT)
    
    # ========================================================================
    # YOUTUBE SETTINGS
    # ========================================================================
    
    @property
    def youtube_api_key(self) -> Optional[str]:
        """YouTube API key."""
        return os.getenv("YOUTUBE_API_KEY") or None
    
    @property
    def youtube_client_id(self) -> Optional[str]:
        """YouTube OAuth client ID."""
        return os.getenv("YOUTUBE_CLIENT_ID") or None
    
    @property
    def youtube_client_secret(self) -> Optional[str]:
        """YouTube OAuth client secret."""
        return os.getenv("YOUTUBE_CLIENT_SECRET") or None
    
    @property
    def youtube_upload_timeout(self) -> int:
        """YouTube upload timeout (seconds)."""
        return self._get_int("YOUTUBE_UPLOAD_TIMEOUT", DEFAULT_YOUTUBE_UPLOAD_TIMEOUT)
    
    # ========================================================================
    # LINKEDIN SETTINGS
    # ========================================================================
    
    @property
    def linkedin_api_key(self) -> Optional[str]:
        """LinkedIn API key."""
        return os.getenv("LINKEDIN_API_KEY") or None
    
    @property
    def linkedin_client_id(self) -> Optional[str]:
        """LinkedIn OAuth client ID."""
        return os.getenv("LINKEDIN_CLIENT_ID") or None
    
    @property
    def linkedin_client_secret(self) -> Optional[str]:
        """LinkedIn OAuth client secret."""
        return os.getenv("LINKEDIN_CLIENT_SECRET") or None
    
    # ========================================================================
    # LOGGING CONFIGURATION
    # ========================================================================
    
    @property
    def log_level(self) -> str:
        """Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL."""
        level = os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL).upper()
        if level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            return DEFAULT_LOG_LEVEL
        return level
    
    @property
    def log_file(self) -> Path:
        """Path to log file."""
        log_file_str = os.getenv("LOG_FILE", "")
        if log_file_str:
            return Path(log_file_str)
        return BASE_DIR / ".agents" / "logs" / "agent.log"
    
    @property
    def log_max_size_mb(self) -> int:
        """Maximum log file size (MB) before rotation."""
        return self._get_int("LOG_MAX_SIZE_MB", DEFAULT_LOG_MAX_SIZE_MB)
    
    @property
    def log_backup_count(self) -> int:
        """Number of backup log files to keep."""
        return self._get_int("LOG_BACKUP_COUNT", DEFAULT_LOG_BACKUP_COUNT)
    
    @property
    def log_format(self) -> str:
        """Log format: simple, detailed, json."""
        fmt = os.getenv("LOG_FORMAT", DEFAULT_LOG_FORMAT).lower()
        if fmt not in ["simple", "detailed", "json"]:
            return DEFAULT_LOG_FORMAT
        return fmt
    
    @property
    def log_to_console(self) -> bool:
        """Whether to log to console."""
        return self._get_bool("LOG_TO_CONSOLE", True)
    
    # ========================================================================
    # DOCKER SETTINGS
    # ========================================================================
    
    @property
    def docker_registry(self) -> Optional[str]:
        """Docker registry for pushing images."""
        return os.getenv("DOCKER_REGISTRY") or None
    
    @property
    def docker_image_prefix(self) -> str:
        """Docker image prefix."""
        return os.getenv("DOCKER_IMAGE_PREFIX", "whatsapp-social-agent")
    
    @property
    def docker_network(self) -> str:
        """Docker network name."""
        return os.getenv("DOCKER_NETWORK", "agent-network")
    
    # ========================================================================
    # ADVANCED SETTINGS
    # ========================================================================
    
    @property
    def debug(self) -> bool:
        """Whether debug mode is enabled."""
        return self._get_bool("DEBUG", False)
    
    @property
    def profiling_enabled(self) -> bool:
        """Whether performance profiling is enabled."""
        return self._get_bool("PROFILING_ENABLED", False)
    
    @property
    def user_agent(self) -> str:
        """User-Agent string for web requests."""
        return os.getenv("USER_AGENT", DEFAULT_USER_AGENT)
    
    @property
    def http_proxy(self) -> Optional[str]:
        """HTTP proxy URL."""
        return os.getenv("HTTP_PROXY") or None
    
    @property
    def https_proxy(self) -> Optional[str]:
        """HTTPS proxy URL."""
        return os.getenv("HTTPS_PROXY") or None
    
    # ========================================================================
    # HELPER METHODS
    # ========================================================================
    
    def _get_int(self, key: str, default: int) -> int:
        """Get integer value from environment."""
        value = os.getenv(key)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            return default
    
    def _get_bool(self, key: str, default: bool) -> bool:
        """Get boolean value from environment."""
        value = os.getenv(key)
        if value is None:
            return default
        return value.lower() in ["true", "1", "yes", "y", "on"]
    
    def _validate(self) -> None:
        """Validate critical configuration."""
        # Validate master password
        _ = self.master_password
        
        # Ensure critical directories exist
        self.temp_download_dir.mkdir(parents=True, exist_ok=True)
        self.whatsapp_session_dir.mkdir(parents=True, exist_ok=True)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def to_dict(self) -> dict[str, Any]:
        """
        Export configuration as dictionary.
        
        Note: Sensitive values (passwords, API keys) are excluded.
        """
        return {
            "check_interval_minutes": self.check_interval_minutes,
            "max_concurrent_uploads": self.max_concurrent_uploads,
            "max_retry_attempts": self.max_retry_attempts,
            "network_timeout": self.network_timeout,
            "max_video_size_mb": self.max_video_size_mb,
            "video_quality": self.video_quality,
            "keep_original_videos": self.keep_original_videos,
            "log_level": self.log_level,
            "log_format": self.log_format,
            "debug": self.debug,
        }


# Global configuration instance
# This is initialized when first imported
_config: Optional[Config] = None


def get_config() -> Config:
    """
    Get the global configuration instance.
    
    Returns:
        Config: The global configuration object
        
    Raises:
        ConfigError: If configuration is invalid or .env file is missing
    """
    global _config
    if _config is None:
        _config = Config()
    return _config
