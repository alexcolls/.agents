"""
Application constants and configuration defaults.
"""

import re
from pathlib import Path
from typing import Final

# ============================================================================
# PROJECT METADATA
# ============================================================================

PROJECT_NAME: Final[str] = ".agents"
VERSION: Final[str] = "0.1.0"
AUTHOR: Final[str] = "Alex Colls Outumuro"
DESCRIPTION: Final[str] = "Automate social media by monitoring WhatsApp groups"

# ============================================================================
# PATHS
# ============================================================================

# Base directory (project root)
BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent.parent

# Agent storage directory
AGENTS_DIR: Final[Path] = BASE_DIR / ".agents"
AGENTS_TMP_DIR: Final[Path] = AGENTS_DIR / "tmp"
AGENTS_BUILD_DIR: Final[Path] = AGENTS_DIR / "build"
AGENTS_LOGS_DIR: Final[Path] = AGENTS_DIR / "logs"
AGENTS_SESSIONS_DIR: Final[Path] = AGENTS_DIR / "sessions"

# Create directories if they don't exist
for directory in [AGENTS_DIR, AGENTS_TMP_DIR, AGENTS_BUILD_DIR, AGENTS_LOGS_DIR, AGENTS_SESSIONS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# ============================================================================
# SUPPORTED PLATFORMS
# ============================================================================

class Platform:
    """Social media platform identifiers."""
    INSTAGRAM: Final[str] = "instagram"
    TIKTOK: Final[str] = "tiktok"
    YOUTUBE: Final[str] = "youtube"
    LINKEDIN: Final[str] = "linkedin"

SUPPORTED_PLATFORMS: Final[list[str]] = [
    Platform.INSTAGRAM,
    Platform.TIKTOK,
    Platform.YOUTUBE,
    Platform.LINKEDIN,
]

PLATFORM_EMOJIS: Final[dict[str, str]] = {
    Platform.INSTAGRAM: "📸",
    Platform.TIKTOK: "🎵",
    Platform.YOUTUBE: "🎥",
    Platform.LINKEDIN: "💼",
}

# Platforms currently implemented
IMPLEMENTED_PLATFORMS: Final[list[str]] = [
    Platform.INSTAGRAM,
]

# ============================================================================
# VIDEO LINK PATTERNS
# ============================================================================

# Regex patterns for detecting video URLs in messages
VIDEO_URL_PATTERNS: Final[dict[str, re.Pattern]] = {
    Platform.INSTAGRAM: re.compile(
        r"(?:https?://)?(?:www\.)?instagram\.com/(?:p|reel|tv)/([A-Za-z0-9_-]+)/?",
        re.IGNORECASE
    ),
    Platform.TIKTOK: re.compile(
        r"(?:https?://)?(?:www\.)?tiktok\.com/@[\w.-]+/video/(\d+)",
        re.IGNORECASE
    ),
    Platform.YOUTUBE: re.compile(
        r"(?:https?://)?(?:www\.)?(?:youtube\.com/(?:watch\?v=|shorts/)|youtu\.be/)([\w-]+)",
        re.IGNORECASE
    ),
    Platform.LINKEDIN: re.compile(
        r"(?:https?://)?(?:www\.)?linkedin\.com/posts/[\w-]+-\d+-[\w]+",
        re.IGNORECASE
    ),
}

# ============================================================================
# FILE EXTENSIONS
# ============================================================================

SUPPORTED_VIDEO_EXTENSIONS: Final[tuple[str, ...]] = (
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
    ".webm",
    ".flv",
    ".m4v",
)

SUPPORTED_IMAGE_EXTENSIONS: Final[tuple[str, ...]] = (
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
)

# ============================================================================
# DEFAULT CONFIGURATION VALUES
# ============================================================================

DEFAULT_CHECK_INTERVAL_MINUTES: Final[int] = 5
DEFAULT_MAX_CONCURRENT_UPLOADS: Final[int] = 3
DEFAULT_MAX_RETRY_ATTEMPTS: Final[int] = 3
DEFAULT_NETWORK_TIMEOUT: Final[int] = 30
DEFAULT_MAX_VIDEO_SIZE_MB: Final[int] = 100
DEFAULT_VIDEO_QUALITY: Final[str] = "high"
DEFAULT_KEEP_ORIGINAL_VIDEOS: Final[bool] = False

# Instagram defaults
DEFAULT_INSTAGRAM_REQUEST_DELAY: Final[int] = 2
DEFAULT_INSTAGRAM_UPLOAD_TIMEOUT: Final[int] = 120
DEFAULT_INSTAGRAM_VERIFICATION_METHOD: Final[str] = "sms"

# TikTok defaults
DEFAULT_TIKTOK_REQUEST_DELAY: Final[int] = 3
DEFAULT_TIKTOK_UPLOAD_TIMEOUT: Final[int] = 180

# YouTube defaults
DEFAULT_YOUTUBE_UPLOAD_TIMEOUT: Final[int] = 300

# Logging defaults
DEFAULT_LOG_LEVEL: Final[str] = "INFO"
DEFAULT_LOG_MAX_SIZE_MB: Final[int] = 10
DEFAULT_LOG_BACKUP_COUNT: Final[int] = 5
DEFAULT_LOG_FORMAT: Final[str] = "detailed"

# ============================================================================
# AGENT STATUS
# ============================================================================

class AgentStatus:
    """Agent operational status."""
    ACTIVE: Final[str] = "active"
    INACTIVE: Final[str] = "inactive"
    ERROR: Final[str] = "error"
    PAUSED: Final[str] = "paused"

# ============================================================================
# ENCRYPTION
# ============================================================================

ENCRYPTION_ALGORITHM: Final[str] = "AES256"
PASSWORD_MIN_LENGTH: Final[int] = 20

# Generated password specifications (for auto-generated passwords)
GENERATED_PASSWORD_LENGTH: Final[int] = 55
GENERATED_PASSWORD_CHARS: Final[str] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!;,?._ "

# ============================================================================
# CLI/UI
# ============================================================================

# Retro terminal color schemes
class RetroColors:
    """Vintage terminal color schemes."""
    AMBER: Final[str] = "#FFB000"
    GREEN_PHOSPHOR: Final[str] = "#00FF00"
    WHITE: Final[str] = "#FFFFFF"
    CYAN: Final[str] = "#00FFFF"
    MAGENTA: Final[str] = "#FF00FF"

# Menu options
class MenuOption:
    """Main menu options."""
    ADD_AGENT: Final[str] = "🤖 Add AGENT"
    CONFIG_AGENT: Final[str] = "⚙️  Config AGENT"
    SEE_ACCOUNTS: Final[str] = "📊 See ACCOUNTS"
    EXIT: Final[str] = "🚪 Exit"

MAIN_MENU_OPTIONS: Final[list[str]] = [
    MenuOption.ADD_AGENT,
    MenuOption.CONFIG_AGENT,
    MenuOption.SEE_ACCOUNTS,
    MenuOption.EXIT,
]

# ============================================================================
# RATE LIMITING
# ============================================================================

# Rate limits to avoid platform bans (requests per hour)
RATE_LIMITS: Final[dict[str, int]] = {
    Platform.INSTAGRAM: 200,  # Conservative limit
    Platform.TIKTOK: 150,
    Platform.YOUTUBE: 100,
    Platform.LINKEDIN: 100,
}

# ============================================================================
# ERROR MESSAGES
# ============================================================================

class ErrorMessages:
    """Common error messages."""
    INVALID_CONFIG: Final[str] = "Invalid configuration"
    NETWORK_ERROR: Final[str] = "Network connection error"
    AUTHENTICATION_FAILED: Final[str] = "Authentication failed"
    RATE_LIMIT_EXCEEDED: Final[str] = "Rate limit exceeded"
    VIDEO_TOO_LARGE: Final[str] = "Video file too large"
    UNSUPPORTED_PLATFORM: Final[str] = "Platform not supported yet"
    AGENT_NOT_FOUND: Final[str] = "Agent not found"
    INVALID_VIDEO_URL: Final[str] = "Invalid video URL"
    DOWNLOAD_FAILED: Final[str] = "Failed to download video"
    UPLOAD_FAILED: Final[str] = "Failed to upload video"
    ENCRYPTION_FAILED: Final[str] = "Encryption/decryption failed"

# ============================================================================
# SUCCESS MESSAGES
# ============================================================================

class SuccessMessages:
    """Common success messages."""
    AGENT_CREATED: Final[str] = "✅ Agent created successfully!"
    AGENT_UPDATED: Final[str] = "✅ Agent updated successfully!"
    AGENT_DELETED: Final[str] = "✅ Agent deleted successfully!"
    VIDEO_DOWNLOADED: Final[str] = "✅ Video downloaded successfully!"
    VIDEO_UPLOADED: Final[str] = "✅ Video uploaded successfully!"
    ACCOUNT_CONNECTED: Final[str] = "✅ Account connected successfully!"

# ============================================================================
# VALIDATION PATTERNS
# ============================================================================

# Username validation (alphanumeric, dots, underscores)
USERNAME_PATTERN: Final[re.Pattern] = re.compile(r"^[a-zA-Z0-9._]{1,30}$")

# Email validation (basic)
EMAIL_PATTERN: Final[re.Pattern] = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

# ============================================================================
# HTTP HEADERS
# ============================================================================

DEFAULT_USER_AGENT: Final[str] = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

DEFAULT_HEADERS: Final[dict[str, str]] = {
    "User-Agent": DEFAULT_USER_AGENT,
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

# ============================================================================
# API ENDPOINTS (Placeholders for future use)
# ============================================================================

class ApiEndpoints:
    """API endpoint placeholders."""
    # These would be defined when implementing official APIs
    INSTAGRAM_GRAPH_API: Final[str] = "https://graph.instagram.com"
    YOUTUBE_API: Final[str] = "https://www.googleapis.com/youtube/v3"
    LINKEDIN_API: Final[str] = "https://api.linkedin.com/v2"
