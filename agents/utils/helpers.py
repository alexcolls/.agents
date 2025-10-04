"""
Common utility functions for .agents application.
"""

import hashlib
import json
import re
import secrets
import string
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse

from agents.utils.constants import (
    EMAIL_PATTERN,
    GENERATED_PASSWORD_CHARS,
    GENERATED_PASSWORD_LENGTH,
    SUPPORTED_VIDEO_EXTENSIONS,
    USERNAME_PATTERN,
    VIDEO_URL_PATTERNS,
)


def generate_password(length: int = GENERATED_PASSWORD_LENGTH) -> str:
    """
    Generate a secure random password.
    
    Args:
        length: Length of password (default: 55)
        
    Returns:
        str: Randomly generated password
        
    Examples:
        >>> password = generate_password()
        >>> len(password)
        55
        >>> password = generate_password(20)
        >>> len(password)
        20
    """
    return "".join(secrets.choice(GENERATED_PASSWORD_CHARS) for _ in range(length))


def validate_username(username: str) -> bool:
    """
    Validate username format.
    
    Usernames must be:
    - 1-30 characters long
    - Alphanumeric with dots and underscores
    
    Args:
        username: Username to validate
        
    Returns:
        bool: True if valid, False otherwise
        
    Examples:
        >>> validate_username("john_doe")
        True
        >>> validate_username("user.123")
        True
        >>> validate_username("invalid!")
        False
    """
    return bool(USERNAME_PATTERN.match(username))


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if valid, False otherwise
        
    Examples:
        >>> validate_email("user@example.com")
        True
        >>> validate_email("invalid-email")
        False
    """
    return bool(EMAIL_PATTERN.match(email))


def extract_video_urls(text: str) -> dict[str, list[str]]:
    """
    Extract video URLs from text grouped by platform.
    
    Args:
        text: Text containing potential video URLs
        
    Returns:
        dict: Dictionary with platform names as keys and lists of URLs as values
        
    Examples:
        >>> text = "Check out https://instagram.com/p/ABC123/"
        >>> extract_video_urls(text)
        {'instagram': ['https://instagram.com/p/ABC123/']}
    """
    results: dict[str, list[str]] = {}
    
    for platform, pattern in VIDEO_URL_PATTERNS.items():
        matches = pattern.findall(text)
        if matches:
            # Reconstruct full URLs from matches
            if platform == "instagram":
                urls = [f"https://instagram.com/p/{match}/" for match in matches]
            elif platform == "tiktok":
                urls = [f"https://tiktok.com/@user/video/{match}" for match in matches]
            elif platform == "youtube":
                urls = [f"https://youtube.com/watch?v={match}" for match in matches]
            else:
                urls = matches
            
            results[platform] = urls
    
    return results


def is_video_file(file_path: Path) -> bool:
    """
    Check if file is a supported video format.
    
    Args:
        file_path: Path to file
        
    Returns:
        bool: True if file is a video, False otherwise
        
    Examples:
        >>> is_video_file(Path("video.mp4"))
        True
        >>> is_video_file(Path("image.jpg"))
        False
    """
    return file_path.suffix.lower() in SUPPORTED_VIDEO_EXTENSIONS


def get_file_size_mb(file_path: Path) -> float:
    """
    Get file size in megabytes.
    
    Args:
        file_path: Path to file
        
    Returns:
        float: File size in MB
        
    Examples:
        >>> size = get_file_size_mb(Path("video.mp4"))
        >>> size > 0
        True
    """
    if not file_path.exists():
        return 0.0
    return file_path.stat().st_size / (1024 * 1024)


def generate_file_hash(file_path: Path, algorithm: str = "sha256") -> str:
    """
    Generate hash of file contents.
    
    Useful for detecting duplicate files.
    
    Args:
        file_path: Path to file
        algorithm: Hash algorithm (sha256, md5, etc.)
        
    Returns:
        str: Hex digest of file hash
        
    Examples:
        >>> hash_value = generate_file_hash(Path("video.mp4"))
        >>> len(hash_value)
        64
    """
    hash_obj = hashlib.new(algorithm)
    
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_obj.update(chunk)
    
    return hash_obj.hexdigest()


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        str: Sanitized filename
        
    Examples:
        >>> sanitize_filename("my video!@#$.mp4")
        'my_video_.mp4'
        >>> sanitize_filename("file/with\\slashes.txt")
        'file_with_slashes.txt'
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', "_", filename)
    
    # Remove leading/trailing dots and spaces
    filename = filename.strip(". ")
    
    # Replace multiple underscores with single
    filename = re.sub(r"_+", "_", filename)
    
    return filename or "untitled"


def format_duration(seconds: int) -> str:
    """
    Format duration in seconds to human-readable string.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        str: Formatted duration (e.g., "1h 23m 45s")
        
    Examples:
        >>> format_duration(90)
        '1m 30s'
        >>> format_duration(3665)
        '1h 1m 5s'
    """
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")
    
    return " ".join(parts)


def format_size(bytes_size: int) -> str:
    """
    Format byte size to human-readable string.
    
    Args:
        bytes_size: Size in bytes
        
    Returns:
        str: Formatted size (e.g., "1.5 MB")
        
    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536000)
        '1.5 MB'
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} PB"


def format_timestamp(dt: Optional[datetime] = None, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format datetime to string.
    
    Args:
        dt: Datetime object. If None, uses current time
        fmt: Format string
        
    Returns:
        str: Formatted timestamp
        
    Examples:
        >>> timestamp = format_timestamp()
        >>> len(timestamp) > 0
        True
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime(fmt)


def parse_timestamp(timestamp_str: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """
    Parse timestamp string to datetime.
    
    Args:
        timestamp_str: Timestamp string
        fmt: Format string
        
    Returns:
        datetime: Parsed datetime object
        
    Examples:
        >>> dt = parse_timestamp("2025-01-15 10:30:00")
        >>> dt.year
        2025
    """
    return datetime.strptime(timestamp_str, fmt)


def truncate_string(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncate string to maximum length.
    
    Args:
        text: Original text
        max_length: Maximum length
        suffix: Suffix to append if truncated
        
    Returns:
        str: Truncated string
        
    Examples:
        >>> truncate_string("This is a very long string", 10)
        'This is...'
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def load_json_file(file_path: Path) -> dict[str, Any]:
    """
    Load JSON file.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        dict: Parsed JSON data
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json_file(data: dict[str, Any], file_path: Path, indent: int = 2) -> None:
    """
    Save data to JSON file.
    
    Args:
        data: Data to save
        file_path: Path to JSON file
        indent: Indentation spaces
    """
    # Ensure directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def get_domain_from_url(url: str) -> str:
    """
    Extract domain from URL.
    
    Args:
        url: URL string
        
    Returns:
        str: Domain name
        
    Examples:
        >>> get_domain_from_url("https://www.instagram.com/p/ABC123/")
        'instagram.com'
    """
    parsed = urlparse(url)
    domain = parsed.netloc
    
    # Remove www. prefix if present
    if domain.startswith("www."):
        domain = domain[4:]
    
    return domain


def create_unique_filename(base_name: str, extension: str, directory: Path) -> str:
    """
    Create unique filename by appending number if file exists.
    
    Args:
        base_name: Base filename (without extension)
        extension: File extension (with dot)
        directory: Directory where file will be saved
        
    Returns:
        str: Unique filename
        
    Examples:
        >>> filename = create_unique_filename("video", ".mp4", Path("/tmp"))
        >>> filename.endswith(".mp4")
        True
    """
    base_name = sanitize_filename(base_name)
    filename = f"{base_name}{extension}"
    counter = 1
    
    while (directory / filename).exists():
        filename = f"{base_name}_{counter}{extension}"
        counter += 1
    
    return filename


def retry_with_backoff(func, max_attempts: int = 3, backoff_seconds: int = 1):
    """
    Retry function with exponential backoff.
    
    Args:
        func: Function to retry
        max_attempts: Maximum number of attempts
        backoff_seconds: Initial backoff duration in seconds
        
    Returns:
        Result of function if successful
        
    Raises:
        Exception: Last exception if all attempts fail
    """
    import time
    
    last_exception = None
    
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            last_exception = e
            if attempt < max_attempts - 1:
                wait_time = backoff_seconds * (2**attempt)
                time.sleep(wait_time)
    
    raise last_exception


def normalize_platform_name(name: str) -> str:
    """
    Normalize platform name to lowercase.
    
    Args:
        name: Platform name
        
    Returns:
        str: Normalized platform name
        
    Examples:
        >>> normalize_platform_name("Instagram")
        'instagram'
        >>> normalize_platform_name("TIKTOK")
        'tiktok'
    """
    return name.lower().strip()
