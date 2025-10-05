"""
Instagram Platform Integration

Handles Instagram authentication, video uploads, and story posting
using instagrapi library with session persistence and error handling.

Classes:
    InstagramClient: Main Instagram client class
    PostResult: Upload result with metadata
    
Functions:
    upload_video: Quick upload function
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime

from instagrapi import Client
from instagrapi.exceptions import (
    LoginRequired,
    ChallengeRequired,
    TwoFactorRequired,
    PleaseWaitFewMinutes,
)

from src.utils.config import get_config
from src.utils.logger import get_logger, LoggerMixin
from src.utils.helpers import sanitize_filename
from src.security.validators import InputValidator


logger = get_logger(__name__)


@dataclass
class PostResult:
    """Instagram post result"""
    
    success: bool
    media_id: Optional[str] = None
    url: Optional[str] = None
    error: Optional[str] = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()


class InstagramClient(LoggerMixin):
    """
    Instagram client for video uploads
    
    Uses instagrapi for Instagram API access with session persistence
    to avoid repeated login challenges.
    """
    
    def __init__(
        self,
        username: str,
        password: str,
        session_dir: Optional[Path] = None,
    ):
        """
        Initialize Instagram client
        
        Args:
            username: Instagram username
            password: Instagram password
            session_dir: Directory to store session files
        """
        if not validate_username(username):
            raise ValueError(f"Invalid username: {username}")
        
        self.username = username
        self.password = password
        
        config = get_config()
        self.session_dir = session_dir or Path(config.BUILD_DIR) / "instagram_sessions"
        self.session_dir.mkdir(parents=True, exist_ok=True)
        
        self.client = Client()
        self._configure_client()
        
        self.logged_in = False
        
        self.log_info(f"InstagramClient initialized for @{username}")
    
    def _configure_client(self):
        """Configure client settings"""
        # Set delay between requests to avoid rate limiting
        self.client.delay_range = [1, 3]
        
        # Set user agent to appear as mobile app
        # This is more stable than web version
        self.client.set_device({
            "app_version": "269.0.0.18.75",
            "android_version": 26,
            "android_release": "8.0.0",
            "dpi": "480dpi",
            "resolution": "1080x1920",
            "manufacturer": "OnePlus",
            "device": "OnePlus6",
            "model": "OnePlus6",
            "cpu": "qcom",
        })
    
    def _get_session_file(self) -> Path:
        """Get session file path for this user"""
        safe_username = sanitize_filename(self.username)
        return self.session_dir / f"{safe_username}.json"
    
    def _save_session(self):
        """Save session to file"""
        session_file = self._get_session_file()
        
        try:
            settings = self.client.get_settings()
            
            with open(session_file, "w") as f:
                json.dump(settings, f, indent=2)
            
            self.log_info(f"Session saved: {session_file.name}")
            
        except Exception as e:
            self.log_error(f"Failed to save session: {e}")
    
    def _load_session(self) -> bool:
        """
        Load session from file
        
        Returns:
            True if session loaded successfully
        """
        session_file = self._get_session_file()
        
        if not session_file.exists():
            self.log_info("No existing session found")
            return False
        
        try:
            with open(session_file, "r") as f:
                settings = json.load(f)
            
            self.client.set_settings(settings)
            self.client.login(self.username, self.password)
            
            # Verify session is valid
            user_id = self.client.user_id
            if user_id:
                self.logged_in = True
                self.log_info(f"Session loaded successfully (user_id: {user_id})")
                return True
            
            return False
            
        except Exception as e:
            self.log_warning(f"Failed to load session: {e}")
            return False
    
    def login(self, force: bool = False) -> bool:
        """
        Login to Instagram
        
        Args:
            force: Force new login even if session exists
            
        Returns:
            True if login successful
        """
        if self.logged_in and not force:
            self.log_info("Already logged in")
            return True
        
        # Try to load existing session first
        if not force and self._load_session():
            return True
        
        self.log_info(f"Logging in as @{self.username}")
        
        try:
            self.client.login(self.username, self.password)
            self.logged_in = True
            
            # Save session for future use
            self._save_session()
            
            self.log_info("Login successful")
            return True
            
        except TwoFactorRequired:
            self.log_error("Two-factor authentication required. Please disable 2FA or use session file.")
            return False
            
        except ChallengeRequired as e:
            self.log_error(f"Challenge required: {e}")
            self.log_info("Try logging in manually and then export session.")
            return False
            
        except LoginRequired as e:
            self.log_error(f"Login required: {e}")
            return False
            
        except PleaseWaitFewMinutes:
            self.log_error("Instagram rate limit hit. Please wait a few minutes.")
            return False
            
        except Exception as e:
            self.log_error(f"Login failed: {e}")
            return False
    
    def logout(self):
        """Logout from Instagram"""
        if not self.logged_in:
            return
        
        try:
            self.client.logout()
            self.logged_in = False
            self.log_info("Logged out")
            
        except Exception as e:
            self.log_error(f"Logout failed: {e}")
    
    def upload_video(
        self,
        video_path: Path,
        caption: str = "",
        thumbnail_path: Optional[Path] = None,
        to_story: bool = False,
    ) -> PostResult:
        """
        Upload video to Instagram
        
        Args:
            video_path: Path to video file
            caption: Video caption (hashtags, mentions, etc.)
            thumbnail_path: Optional custom thumbnail
            to_story: Post as story instead of feed post
            
        Returns:
            PostResult with upload details
        """
        if not self.logged_in:
            if not self.login():
                return PostResult(
                    success=False,
                    error="Not logged in and login failed"
                )
        
        # Validate video file
        if not video_path.exists():
            error = f"Video file not found: {video_path}"
            self.log_error(error)
            return PostResult(success=False, error=error)
        
        if not validate_video_file(video_path):
            error = f"Invalid video file: {video_path}"
            self.log_error(error)
            return PostResult(success=False, error=error)
        
        self.log_info(f"Uploading video: {video_path.name}")
        
        try:
            if to_story:
                # Upload as story
                media = self.client.video_upload_to_story(
                    str(video_path),
                    caption=caption,
                )
            else:
                # Upload as feed post
                media = self.client.video_upload(
                    str(video_path),
                    caption=caption,
                    thumbnail=str(thumbnail_path) if thumbnail_path else None,
                )
            
            if media:
                media_id = str(media.pk)
                media_url = f"https://www.instagram.com/p/{media.code}/"
                
                self.log_info(f"Upload successful: {media_url}")
                
                return PostResult(
                    success=True,
                    media_id=media_id,
                    url=media_url,
                )
            else:
                error = "Upload returned no media object"
                self.log_error(error)
                return PostResult(success=False, error=error)
                
        except PleaseWaitFewMinutes:
            error = "Instagram rate limit hit. Please wait."
            self.log_error(error)
            return PostResult(success=False, error=error)
            
        except Exception as e:
            error = f"Upload failed: {e}"
            self.log_error(error)
            return PostResult(success=False, error=error)
    
    def upload_video_with_retry(
        self,
        video_path: Path,
        caption: str = "",
        thumbnail_path: Optional[Path] = None,
        max_retries: int = 3,
    ) -> PostResult:
        """
        Upload video with automatic retry on failure
        
        Args:
            video_path: Path to video file
            caption: Video caption
            thumbnail_path: Optional thumbnail
            max_retries: Maximum retry attempts
            
        Returns:
            PostResult
        """
        import time
        
        for attempt in range(max_retries):
            result = self.upload_video(
                video_path,
                caption=caption,
                thumbnail_path=thumbnail_path,
            )
            
            if result.success:
                return result
            
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 30  # 30, 60, 90 seconds
                self.log_warning(f"Retry {attempt + 1}/{max_retries} in {wait_time}s")
                time.sleep(wait_time)
        
        return result
    
    def get_user_info(self, username: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get user information
        
        Args:
            username: Username to query (default: self)
            
        Returns:
            User info dict or None
        """
        if not self.logged_in:
            if not self.login():
                return None
        
        try:
            username = username or self.username
            user_id = self.client.user_id_from_username(username)
            user_info = self.client.user_info(user_id)
            
            return {
                "user_id": str(user_info.pk),
                "username": user_info.username,
                "full_name": user_info.full_name,
                "biography": user_info.biography,
                "follower_count": user_info.follower_count,
                "following_count": user_info.following_count,
                "media_count": user_info.media_count,
                "is_verified": user_info.is_verified,
                "is_private": user_info.is_private,
            }
            
        except Exception as e:
            self.log_error(f"Failed to get user info: {e}")
            return None
    
    def get_recent_posts(self, count: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent posts from user
        
        Args:
            count: Number of posts to retrieve
            
        Returns:
            List of post info dicts
        """
        if not self.logged_in:
            if not self.login():
                return []
        
        try:
            user_id = self.client.user_id
            medias = self.client.user_medias(user_id, count)
            
            posts = []
            for media in medias:
                posts.append({
                    "media_id": str(media.pk),
                    "code": media.code,
                    "url": f"https://www.instagram.com/p/{media.code}/",
                    "caption": media.caption_text,
                    "like_count": media.like_count,
                    "comment_count": media.comment_count,
                    "media_type": media.media_type,
                    "timestamp": media.taken_at.isoformat(),
                })
            
            return posts
            
        except Exception as e:
            self.log_error(f"Failed to get recent posts: {e}")
            return []
    
    def delete_post(self, media_id: str) -> bool:
        """
        Delete a post
        
        Args:
            media_id: Media ID to delete
            
        Returns:
            True if deleted successfully
        """
        if not self.logged_in:
            if not self.login():
                return False
        
        try:
            result = self.client.media_delete(media_id)
            self.log_info(f"Deleted post: {media_id}")
            return result
            
        except Exception as e:
            self.log_error(f"Failed to delete post: {e}")
            return False


# Convenience functions

def upload_video(
    username: str,
    password: str,
    video_path: Path,
    caption: str = "",
    session_dir: Optional[Path] = None,
) -> PostResult:
    """
    Quick video upload function
    
    Args:
        username: Instagram username
        password: Instagram password
        video_path: Path to video
        caption: Video caption
        session_dir: Optional session directory
        
    Returns:
        PostResult
    """
    client = InstagramClient(username, password, session_dir)
    
    if not client.login():
        return PostResult(success=False, error="Login failed")
    
    return client.upload_video(video_path, caption)


# Export public API
__all__ = [
    "InstagramClient",
    "PostResult",
    "upload_video",
]
