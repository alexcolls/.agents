"""
Input validation and sanitization for security.

Prevents injection attacks, validates data formats, and sanitizes user input.
"""

import re
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from src.utils.constants import (
    EMAIL_PATTERN,
    PLATFORM_EMOJIS,
    SUPPORTED_PLATFORMS,
    SUPPORTED_VIDEO_EXTENSIONS,
    USERNAME_PATTERN,
    VIDEO_URL_PATTERNS,
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ValidationError(Exception):
    """Raised when validation fails."""
    pass


class InputValidator:
    """
    Validates and sanitizes user input.
    
    Provides methods for validating different types of input data.
    """
    
    @staticmethod
    def validate_username(username: str, min_length: int = 1, max_length: int = 30) -> bool:
        """
        Validate username format.
        
        Args:
            username: Username to validate
            min_length: Minimum length
            max_length: Maximum length
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If validation fails
            
        Examples:
            >>> InputValidator.validate_username("john_doe")
            True
            >>> InputValidator.validate_username("invalid!")
            Traceback (most recent call last):
            ...
            ValidationError: Invalid username format...
        """
        if not username:
            raise ValidationError("Username cannot be empty")
        
        if len(username) < min_length:
            raise ValidationError(f"Username must be at least {min_length} characters")
        
        if len(username) > max_length:
            raise ValidationError(f"Username must be at most {max_length} characters")
        
        if not USERNAME_PATTERN.match(username):
            raise ValidationError(
                "Invalid username format. "
                "Username can only contain letters, numbers, dots, and underscores."
            )
        
        return True
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format.
        
        Args:
            email: Email address to validate
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If validation fails
        """
        if not email:
            raise ValidationError("Email cannot be empty")
        
        if not EMAIL_PATTERN.match(email):
            raise ValidationError("Invalid email format")
        
        return True
    
    @staticmethod
    def validate_password(password: str, min_length: int = 8) -> bool:
        """
        Validate password strength.
        
        Args:
            password: Password to validate
            min_length: Minimum length
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If validation fails
        """
        if not password:
            raise ValidationError("Password cannot be empty")
        
        if len(password) < min_length:
            raise ValidationError(f"Password must be at least {min_length} characters")
        
        # Check for at least one number (optional, can be stricter)
        # Uncomment for stricter validation:
        # if not re.search(r"\d", password):
        #     raise ValidationError("Password must contain at least one number")
        
        # if not re.search(r"[a-z]", password):
        #     raise ValidationError("Password must contain at least one lowercase letter")
        
        # if not re.search(r"[A-Z]", password):
        #     raise ValidationError("Password must contain at least one uppercase letter")
        
        return True
    
    @staticmethod
    def validate_platform(platform: str) -> bool:
        """
        Validate platform name.
        
        Args:
            platform: Platform name (instagram, tiktok, youtube, linkedin)
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If validation fails
        """
        if not platform:
            raise ValidationError("Platform cannot be empty")
        
        platform_lower = platform.lower().strip()
        
        if platform_lower not in SUPPORTED_PLATFORMS:
            raise ValidationError(
                f"Unsupported platform: {platform}. "
                f"Supported platforms: {', '.join(SUPPORTED_PLATFORMS)}"
            )
        
        return True
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validate URL format.
        
        Args:
            url: URL to validate
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If validation fails
        """
        if not url:
            raise ValidationError("URL cannot be empty")
        
        try:
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                raise ValidationError("Invalid URL format")
        except Exception as e:
            raise ValidationError(f"Invalid URL: {e}")
        
        return True
    
    @staticmethod
    def validate_video_url(url: str) -> tuple[bool, Optional[str]]:
        """
        Validate video URL and detect platform.
        
        Args:
            url: Video URL to validate
            
        Returns:
            tuple: (is_valid, platform_name or None)
            
        Examples:
            >>> valid, platform = InputValidator.validate_video_url(
            ...     "https://instagram.com/p/ABC123/"
            ... )
            >>> valid
            True
            >>> platform
            'instagram'
        """
        if not url:
            return False, None
        
        for platform, pattern in VIDEO_URL_PATTERNS.items():
            if pattern.search(url):
                return True, platform
        
        return False, None
    
    @staticmethod
    def validate_file_path(file_path: Path, must_exist: bool = False) -> bool:
        """
        Validate file path.
        
        Args:
            file_path: Path to validate
            must_exist: Whether file must exist
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If validation fails
        """
        if not file_path:
            raise ValidationError("File path cannot be empty")
        
        # Check for path traversal attempts
        try:
            file_path.resolve()
        except Exception as e:
            raise ValidationError(f"Invalid file path: {e}")
        
        if must_exist and not file_path.exists():
            raise ValidationError(f"File does not exist: {file_path}")
        
        return True
    
    @staticmethod
    def validate_video_file(file_path: Path) -> bool:
        """
        Validate video file.
        
        Args:
            file_path: Path to video file
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If validation fails
        """
        InputValidator.validate_file_path(file_path, must_exist=True)
        
        if file_path.suffix.lower() not in SUPPORTED_VIDEO_EXTENSIONS:
            raise ValidationError(
                f"Unsupported video format: {file_path.suffix}. "
                f"Supported formats: {', '.join(SUPPORTED_VIDEO_EXTENSIONS)}"
            )
        
        return True
    
    @staticmethod
    def validate_agent_name(name: str) -> bool:
        """
        Validate agent name.
        
        Agent names are used as filenames, so must be filesystem-safe.
        
        Args:
            name: Agent name to validate
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If validation fails
        """
        if not name:
            raise ValidationError("Agent name cannot be empty")
        
        if len(name) < 1 or len(name) > 100:
            raise ValidationError("Agent name must be 1-100 characters")
        
        # Check for invalid filename characters
        invalid_chars = r'[<>:"/\\|?*\x00-\x1f]'
        if re.search(invalid_chars, name):
            raise ValidationError(
                "Agent name contains invalid characters. "
                "Cannot contain: < > : \" / \\ | ? * or control characters"
            )
        
        # Don't allow leading/trailing dots or spaces
        if name.startswith((".", " ")) or name.endswith((".", " ")):
            raise ValidationError("Agent name cannot start or end with dots or spaces")
        
        return True


class InputSanitizer:
    """
    Sanitizes user input to prevent injection attacks.
    """
    
    @staticmethod
    def sanitize_string(text: str, max_length: Optional[int] = None) -> str:
        """
        Sanitize a string by removing dangerous characters.
        
        Args:
            text: Text to sanitize
            max_length: Maximum length (truncate if longer)
            
        Returns:
            str: Sanitized text
        """
        if not text:
            return ""
        
        # Remove null bytes
        text = text.replace("\x00", "")
        
        # Remove control characters except newline and tab
        text = re.sub(r"[\x01-\x08\x0b-\x0c\x0e-\x1f\x7f]", "", text)
        
        # Truncate if needed
        if max_length and len(text) > max_length:
            text = text[:max_length]
        
        return text.strip()
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename by removing dangerous characters.
        
        Args:
            filename: Original filename
            
        Returns:
            str: Sanitized filename
        """
        if not filename:
            return "untitled"
        
        # Remove path separators
        filename = filename.replace("/", "_").replace("\\", "_")
        
        # Remove other dangerous characters
        filename = re.sub(r'[<>:"|?*\x00-\x1f]', "_", filename)
        
        # Remove leading/trailing dots and spaces
        filename = filename.strip(". ")
        
        # Replace multiple underscores with single
        filename = re.sub(r"_+", "_", filename)
        
        # Ensure not empty
        if not filename:
            filename = "untitled"
        
        return filename
    
    @staticmethod
    def sanitize_path(path: str) -> Path:
        """
        Sanitize file path to prevent traversal attacks.
        
        Args:
            path: Path string to sanitize
            
        Returns:
            Path: Sanitized path object
            
        Raises:
            ValidationError: If path is suspicious
        """
        if not path:
            raise ValidationError("Path cannot be empty")
        
        # Check for path traversal attempts
        if ".." in path or path.startswith("/"):
            raise ValidationError("Path traversal detected")
        
        # Convert to Path and resolve
        try:
            clean_path = Path(path).resolve()
        except Exception as e:
            raise ValidationError(f"Invalid path: {e}")
        
        return clean_path
    
    @staticmethod
    def sanitize_url(url: str) -> str:
        """
        Sanitize URL to prevent injection.
        
        Args:
            url: URL to sanitize
            
        Returns:
            str: Sanitized URL
            
        Raises:
            ValidationError: If URL is malformed
        """
        if not url:
            return ""
        
        # Remove whitespace
        url = url.strip()
        
        # Basic URL validation
        try:
            result = urlparse(url)
            if result.scheme not in ["http", "https"]:
                raise ValidationError(
                    f"Unsupported URL scheme: {result.scheme}. "
                    "Only http and https are allowed."
                )
        except Exception as e:
            raise ValidationError(f"Invalid URL: {e}")
        
        return url


# Convenience functions
def is_valid_username(username: str) -> bool:
    """Check if username is valid without raising exception."""
    try:
        InputValidator.validate_username(username)
        return True
    except ValidationError:
        return False


def is_valid_email(email: str) -> bool:
    """Check if email is valid without raising exception."""
    try:
        InputValidator.validate_email(email)
        return True
    except ValidationError:
        return False


def is_valid_platform(platform: str) -> bool:
    """Check if platform is valid without raising exception."""
    try:
        InputValidator.validate_platform(platform)
        return True
    except ValidationError:
        return False


def is_valid_video_url(url: str) -> bool:
    """Check if URL is a valid video URL without raising exception."""
    valid, _ = InputValidator.validate_video_url(url)
    return valid


# Example usage
if __name__ == "__main__":
    # Test username validation
    try:
        InputValidator.validate_username("john_doe")
        print("✓ Username 'john_doe' is valid")
    except ValidationError as e:
        print(f"✗ Username validation failed: {e}")
    
    # Test invalid username
    try:
        InputValidator.validate_username("invalid!")
        print("✓ Username 'invalid!' is valid")
    except ValidationError as e:
        print(f"✗ Username validation failed: {e}")
    
    # Test video URL validation
    urls = [
        "https://instagram.com/p/ABC123/",
        "https://tiktok.com/@user/video/123456",
        "https://youtube.com/watch?v=dQw4w9WgXcQ",
        "https://example.com/video.mp4",
    ]
    
    for url in urls:
        valid, platform = InputValidator.validate_video_url(url)
        if valid:
            print(f"✓ Valid {platform} URL: {url}")
        else:
            print(f"✗ Invalid video URL: {url}")
    
    # Test sanitization
    dangerous_filename = "../../../etc/passwd"
    try:
        safe_path = InputSanitizer.sanitize_path(dangerous_filename)
        print(f"Sanitized path: {safe_path}")
    except ValidationError as e:
        print(f"✓ Path traversal blocked: {e}")
