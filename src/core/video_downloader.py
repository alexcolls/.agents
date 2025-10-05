"""
Video Downloader

Downloads videos from URLs using yt-dlp with progress tracking,
format selection, and quality optimization for social media.

Classes:
    VideoQuality: Video quality presets
    DownloadProgress: Progress tracking callback
    VideoDownloader: Main downloader class
    
Functions:
    download_video: Quick download function
    get_video_info: Extract video metadata
"""

import os
import re
from enum import Enum
from pathlib import Path
from typing import Optional, Dict, Any, Callable
from dataclasses import dataclass

import yt_dlp

from src.utils.config import get_config
from src.utils.logger import get_logger, LoggerMixin
from src.utils.helpers import sanitize_filename, format_size
from src.security.validators import InputValidator


logger = get_logger(__name__)


class VideoQuality(str, Enum):
    """Video quality presets for social media"""
    
    LOW = "low"           # 480p, smaller file size
    MEDIUM = "medium"     # 720p, balanced quality
    HIGH = "high"         # 1080p, best quality
    AUTO = "auto"         # Let yt-dlp choose best


# Quality to yt-dlp format mapping
QUALITY_FORMATS = {
    VideoQuality.LOW: "bestvideo[height<=480]+bestaudio/best[height<=480]",
    VideoQuality.MEDIUM: "bestvideo[height<=720]+bestaudio/best[height<=720]",
    VideoQuality.HIGH: "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    VideoQuality.AUTO: "bestvideo+bestaudio/best",
}


@dataclass
class VideoInfo:
    """Video metadata"""
    
    url: str
    title: str
    duration: int  # seconds
    thumbnail: Optional[str] = None
    description: Optional[str] = None
    uploader: Optional[str] = None
    upload_date: Optional[str] = None
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    
    @property
    def duration_str(self) -> str:
        """Format duration as HH:MM:SS"""
        hours = self.duration // 3600
        minutes = (self.duration % 3600) // 60
        seconds = self.duration % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return f"{minutes:02d}:{seconds:02d}"


class DownloadProgress:
    """Progress tracking for video downloads"""
    
    def __init__(self, on_progress: Optional[Callable[[Dict[str, Any]], None]] = None):
        """
        Initialize progress tracker
        
        Args:
            on_progress: Optional callback for progress updates
        """
        self.on_progress = on_progress
        self.total_bytes = 0
        self.downloaded_bytes = 0
        self.status = "starting"
        self.filename = ""
    
    def __call__(self, d: Dict[str, Any]):
        """
        yt-dlp progress hook
        
        Args:
            d: Progress dictionary from yt-dlp
        """
        self.status = d.get("status", "unknown")
        
        if self.status == "downloading":
            self.total_bytes = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
            self.downloaded_bytes = d.get("downloaded_bytes", 0)
            self.filename = d.get("filename", "")
            
            # Calculate percentage
            if self.total_bytes > 0:
                percent = (self.downloaded_bytes / self.total_bytes) * 100
            else:
                percent = 0
            
            # Call custom callback if provided
            if self.on_progress:
                self.on_progress({
                    "status": "downloading",
                    "filename": self.filename,
                    "total_bytes": self.total_bytes,
                    "downloaded_bytes": self.downloaded_bytes,
                    "percent": percent,
                    "speed": d.get("speed", 0),
                    "eta": d.get("eta", 0),
                })
        
        elif self.status == "finished":
            self.filename = d.get("filename", "")
            
            if self.on_progress:
                self.on_progress({
                    "status": "finished",
                    "filename": self.filename,
                })


class VideoDownloader(LoggerMixin):
    """
    Video downloader using yt-dlp
    
    Supports downloading from various platforms including:
    - YouTube
    - Twitter/X
    - Facebook
    - Instagram
    - TikTok
    - And many more via yt-dlp
    """
    
    def __init__(
        self,
        output_dir: Optional[Path] = None,
        quality: VideoQuality = VideoQuality.HIGH,
        max_file_size_mb: int = 500,
    ):
        """
        Initialize video downloader
        
        Args:
            output_dir: Directory to save videos
            quality: Video quality preset
            max_file_size_mb: Maximum file size in MB
        """
        config = get_config()
        
        self.output_dir = output_dir or Path(config.TMP_DIR) / "videos"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.quality = quality
        self.max_file_size_mb = max_file_size_mb
        
        self.log_info(f"VideoDownloader initialized: {self.output_dir}")
    
    def _get_ydl_opts(
        self,
        output_template: str,
        progress_callback: Optional[Callable] = None,
    ) -> Dict[str, Any]:
        """
        Get yt-dlp options
        
        Args:
            output_template: Output filename template
            progress_callback: Optional progress callback
            
        Returns:
            yt-dlp options dict
        """
        opts = {
            "format": QUALITY_FORMATS[self.quality],
            "outtmpl": output_template,
            "restrictfilenames": True,  # ASCII only
            "noplaylist": True,  # Download single video
            "quiet": True,
            "no_warnings": True,
            "extract_flat": False,
            # Prefer MP4 format for compatibility
            "merge_output_format": "mp4",
            "postprocessors": [{
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",
            }],
        }
        
        # Add file size limit
        if self.max_file_size_mb > 0:
            opts["max_filesize"] = self.max_file_size_mb * 1024 * 1024
        
        # Add progress hook
        if progress_callback:
            opts["progress_hooks"] = [progress_callback]
        
        return opts
    
    def get_video_info(self, url: str) -> Optional[VideoInfo]:
        """
        Extract video metadata without downloading
        
        Args:
            url: Video URL
            
        Returns:
            VideoInfo or None if failed
        """
        if not validate_url(url):
            self.log_error(f"Invalid URL: {url}")
            return None
        
        try:
            with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True}) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if not info:
                    self.log_error(f"Could not extract info from {url}")
                    return None
                
                video_info = VideoInfo(
                    url=url,
                    title=info.get("title", "Unknown"),
                    duration=info.get("duration", 0),
                    thumbnail=info.get("thumbnail"),
                    description=info.get("description"),
                    uploader=info.get("uploader"),
                    upload_date=info.get("upload_date"),
                    view_count=info.get("view_count"),
                    like_count=info.get("like_count"),
                )
                
                self.log_info(f"Extracted info: {video_info.title} ({video_info.duration_str})")
                return video_info
                
        except Exception as e:
            self.log_error(f"Failed to get video info: {e}")
            return None
    
    def download(
        self,
        url: str,
        filename: Optional[str] = None,
        on_progress: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> Optional[Path]:
        """
        Download video from URL
        
        Args:
            url: Video URL
            filename: Optional output filename (without extension)
            on_progress: Optional progress callback
            
        Returns:
            Path to downloaded video or None if failed
        """
        if not validate_url(url):
            self.log_error(f"Invalid URL: {url}")
            return None
        
        self.log_info(f"Downloading video from: {url}")
        
        try:
            # Get video info first
            info = self.get_video_info(url)
            if not info:
                return None
            
            # Generate filename if not provided
            if not filename:
                filename = sanitize_filename(info.title)
            else:
                filename = sanitize_filename(filename)
            
            # Output template
            output_template = str(self.output_dir / f"{filename}.%(ext)s")
            
            # Create progress tracker
            progress_tracker = DownloadProgress(on_progress)
            
            # Download options
            ydl_opts = self._get_ydl_opts(output_template, progress_tracker)
            
            # Download video
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # Find downloaded file
            downloaded_file = None
            for ext in ["mp4", "mkv", "webm", "avi"]:
                candidate = self.output_dir / f"{filename}.{ext}"
                if candidate.exists():
                    downloaded_file = candidate
                    break
            
            if not downloaded_file or not downloaded_file.exists():
                self.log_error(f"Downloaded file not found: {filename}")
                return None
            
            # Validate video file
            if not validate_video_file(downloaded_file):
                self.log_error(f"Invalid video file: {downloaded_file}")
                downloaded_file.unlink()  # Remove invalid file
                return None
            
            file_size = format_file_size(downloaded_file.stat().st_size)
            self.log_info(f"Downloaded: {downloaded_file.name} ({file_size})")
            
            return downloaded_file
            
        except yt_dlp.utils.DownloadError as e:
            self.log_error(f"Download error: {e}")
            return None
        except Exception as e:
            self.log_error(f"Unexpected error downloading video: {e}")
            return None
    
    def download_batch(
        self,
        urls: list[str],
        on_progress: Optional[Callable[[str, Dict[str, Any]], None]] = None,
    ) -> Dict[str, Optional[Path]]:
        """
        Download multiple videos
        
        Args:
            urls: List of video URLs
            on_progress: Optional progress callback (url, progress_data)
            
        Returns:
            Dict mapping URLs to downloaded file paths
        """
        results = {}
        
        for url in urls:
            self.log_info(f"Downloading {url} ({urls.index(url) + 1}/{len(urls)})")
            
            # Wrap progress callback to include URL
            url_progress_callback = None
            if on_progress:
                url_progress_callback = lambda p: on_progress(url, p)
            
            video_path = self.download(url, on_progress=url_progress_callback)
            results[url] = video_path
        
        successful = sum(1 for p in results.values() if p is not None)
        self.log_info(f"Downloaded {successful}/{len(urls)} videos successfully")
        
        return results
    
    def cleanup_old_videos(self, max_age_hours: int = 24):
        """
        Remove old downloaded videos
        
        Args:
            max_age_hours: Maximum age in hours
        """
        import time
        
        now = time.time()
        max_age_seconds = max_age_hours * 3600
        
        removed_count = 0
        
        for video_file in self.output_dir.glob("*"):
            if not video_file.is_file():
                continue
            
            age = now - video_file.stat().st_mtime
            
            if age > max_age_seconds:
                try:
                    video_file.unlink()
                    removed_count += 1
                    self.log_info(f"Removed old video: {video_file.name}")
                except Exception as e:
                    self.log_error(f"Failed to remove {video_file.name}: {e}")
        
        if removed_count > 0:
            self.log_info(f"Cleaned up {removed_count} old videos")


# Convenience functions

def download_video(
    url: str,
    output_dir: Optional[Path] = None,
    quality: VideoQuality = VideoQuality.HIGH,
    filename: Optional[str] = None,
) -> Optional[Path]:
    """
    Quick download function
    
    Args:
        url: Video URL
        output_dir: Output directory
        quality: Video quality
        filename: Optional filename
        
    Returns:
        Path to downloaded video or None
    """
    downloader = VideoDownloader(output_dir=output_dir, quality=quality)
    return downloader.download(url, filename=filename)


def get_video_info(url: str) -> Optional[VideoInfo]:
    """
    Quick video info extraction
    
    Args:
        url: Video URL
        
    Returns:
        VideoInfo or None
    """
    downloader = VideoDownloader()
    return downloader.get_video_info(url)


# Export public API
__all__ = [
    "VideoQuality",
    "VideoInfo",
    "DownloadProgress",
    "VideoDownloader",
    "download_video",
    "get_video_info",
]
