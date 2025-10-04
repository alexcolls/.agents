"""
Social Media Orchestrator

Coordinates WhatsApp monitoring, video downloading, and multi-platform posting.
This is the main automation engine that ties all components together.

Classes:
    OrchestrationResult: Result of orchestration cycle
    AgentOrchestrator: Main orchestrator for agent automation
    
Functions:
    run_agent: Quick function to run agent automation
"""

import time
import threading
from pathlib import Path
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, field
from datetime import datetime

from src.core.agent import Agent, AgentStatus
from src.core.video_downloader import VideoDownloader, VideoQuality
from src.platforms.whatsapp import WhatsAppMonitor, WhatsAppMessage
from src.platforms.instagram import InstagramClient, PostResult
from src.utils.config import get_config
from src.utils.logger import get_logger, LoggerMixin
from src.security.encryption import Encryptor


logger = get_logger(__name__)


@dataclass
class OrchestrationResult:
    """Result of an orchestration cycle"""
    
    success: bool
    videos_found: int = 0
    videos_downloaded: int = 0
    posts_successful: int = 0
    posts_failed: int = 0
    errors: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def add_error(self, error: str):
        """Add error to list"""
        self.errors.append(error)


class AgentOrchestrator(LoggerMixin):
    """
    Agent orchestrator
    
    Manages the complete automation workflow:
    1. Monitor WhatsApp groups for video messages
    2. Download videos from URLs
    3. Post videos to configured social media platforms
    4. Track results and handle errors
    """
    
    def __init__(
        self,
        agent: Agent,
        encryption_manager: Optional[Encryptor] = None,
    ):
        """
        Initialize orchestrator
        
        Args:
            agent: Agent to orchestrate
            encryption_manager: Encryption manager for credentials
        """
        self.agent = agent
        self.encryption_manager = encryption_manager
        
        config = get_config()
        
        # Initialize components
        self.video_downloader = VideoDownloader(
            quality=VideoQuality.HIGH,
            max_file_size_mb=500,
        )
        
        # Platform clients (initialized on demand)
        self._platform_clients: Dict[str, Any] = {}
        
        # WhatsApp monitor (initialized on start)
        self.whatsapp_monitor: Optional[WhatsAppMonitor] = None
        
        # Control flags
        self.running = False
        self.paused = False
        self._stop_event = threading.Event()
        self._worker_thread: Optional[threading.Thread] = None
        
        # Statistics
        self.total_videos_processed = 0
        self.total_posts_successful = 0
        self.total_posts_failed = 0
        
        self.log_info(f"Orchestrator initialized for agent: {agent.name}")
    
    def _get_platform_client(self, platform: str):
        """
        Get or create platform client
        
        Args:
            platform: Platform name
            
        Returns:
            Platform client instance
        """
        if platform in self._platform_clients:
            return self._platform_clients[platform]
        
        # Get credentials
        credentials = self.agent.get_credentials(platform)
        if not credentials:
            self.log_error(f"No credentials found for {platform}")
            return None
        
        # Create client based on platform
        if platform == "instagram":
            client = InstagramClient(
                username=credentials["username"],
                password=credentials["password"],
            )
            self._platform_clients[platform] = client
            return client
        
        # Add more platforms here as implemented
        # elif platform == "tiktok":
        #     client = TikTokClient(...)
        
        self.log_warning(f"Platform not implemented: {platform}")
        return None
    
    def _handle_video_found(self, group_name: str, video_urls: List[str]):
        """
        Handle video URLs found in WhatsApp
        
        Args:
            group_name: Name of group where videos were found
            video_urls: List of video URLs
        """
        if self.paused:
            self.log_info("Agent paused, skipping videos")
            return
        
        self.log_info(f"Processing {len(video_urls)} video(s) from {group_name}")
        
        for url in video_urls:
            try:
                # Download video
                self.log_info(f"Downloading: {url}")
                video_path = self.video_downloader.download(url)
                
                if not video_path:
                    error = f"Failed to download video: {url}"
                    self.log_error(error)
                    self.agent.add_error(error)
                    continue
                
                self.total_videos_processed += 1
                self.agent.last_check = datetime.utcnow()
                
                # Generate caption
                caption = self._generate_caption(group_name)
                
                # Post to all configured platforms
                for platform in self.agent.config.platforms.keys():
                    self._post_to_platform(platform, video_path, caption)
                
                # Cleanup video after posting
                try:
                    video_path.unlink()
                    self.log_info(f"Cleaned up: {video_path.name}")
                except Exception as e:
                    self.log_warning(f"Failed to delete video: {e}")
                    
            except Exception as e:
                error = f"Error processing video {url}: {e}"
                self.log_error(error)
                self.agent.add_error(error)
    
    def _generate_caption(self, group_name: str) -> str:
        """
        Generate caption for post
        
        Args:
            group_name: WhatsApp group name
            
        Returns:
            Generated caption with hashtags
        """
        if self.agent.config.auto_caption:
            # Auto-generate caption
            caption_parts = []
            
            # Add group mention if desired
            # caption_parts.append(f"From: {group_name}")
            
            # Add hashtags
            if self.agent.config.hashtags:
                hashtags = " ".join(f"#{tag}" for tag in self.agent.config.hashtags)
                caption_parts.append(hashtags)
            
            return "\n\n".join(caption_parts)
        else:
            # Use template
            caption = self.agent.config.default_caption or ""
            
            # Replace placeholders
            caption = caption.replace("{group_name}", group_name)
            caption = caption.replace("{date}", datetime.now().strftime("%Y-%m-%d"))
            
            # Add hashtags
            if self.agent.config.hashtags:
                hashtags = " ".join(f"#{tag}" for tag in self.agent.config.hashtags)
                caption = f"{caption}\n\n{hashtags}"
            
            return caption
    
    def _post_to_platform(
        self,
        platform: str,
        video_path: Path,
        caption: str,
    ) -> bool:
        """
        Post video to platform
        
        Args:
            platform: Platform name
            video_path: Path to video file
            caption: Post caption
            
        Returns:
            True if successful
        """
        client = self._get_platform_client(platform)
        
        if not client:
            error = f"Could not get client for {platform}"
            self.log_error(error)
            self.agent.add_error(error)
            self.total_posts_failed += 1
            return False
        
        self.log_info(f"Posting to {platform}: {video_path.name}")
        
        try:
            # Platform-specific upload
            if platform == "instagram":
                result = client.upload_video_with_retry(
                    video_path,
                    caption=caption,
                    max_retries=3,
                )
                
                if result.success:
                    self.log_info(f"Posted to Instagram: {result.url}")
                    self.total_posts_successful += 1
                    self.agent.total_posts += 1
                    self.agent.last_post = datetime.utcnow()
                    return True
                else:
                    error = f"Instagram upload failed: {result.error}"
                    self.log_error(error)
                    self.agent.add_error(error)
                    self.total_posts_failed += 1
                    return False
            
            # Add more platforms here
            # elif platform == "tiktok":
            #     ...
            
            else:
                error = f"Platform posting not implemented: {platform}"
                self.log_warning(error)
                self.total_posts_failed += 1
                return False
                
        except Exception as e:
            error = f"Error posting to {platform}: {e}"
            self.log_error(error)
            self.agent.add_error(error)
            self.total_posts_failed += 1
            return False
    
    def start(self) -> bool:
        """
        Start agent orchestration
        
        Returns:
            True if started successfully
        """
        if self.running:
            self.log_warning("Orchestrator already running")
            return False
        
        self.log_info(f"Starting orchestration for agent: {self.agent.name}")
        
        # Update agent status
        self.agent.status = AgentStatus.STARTING
        
        # Initialize WhatsApp monitor
        try:
            self.whatsapp_monitor = WhatsAppMonitor(
                phone_number=self.agent.config.whatsapp_phone,
                groups=self.agent.config.whatsapp_groups,
                on_video_found=self._handle_video_found,
            )
        except Exception as e:
            error = f"Failed to initialize WhatsApp monitor: {e}"
            self.log_error(error)
            self.agent.add_error(error)
            self.agent.status = AgentStatus.ERROR
            return False
        
        # Start monitoring in worker thread
        self._stop_event.clear()
        self._worker_thread = threading.Thread(
            target=self._worker_loop,
            name=f"Agent-{self.agent.name}",
            daemon=True,
        )
        self._worker_thread.start()
        
        self.running = True
        self.agent.status = AgentStatus.RUNNING
        
        self.log_info("Orchestration started successfully")
        return True
    
    def _worker_loop(self):
        """Worker thread loop for monitoring"""
        self.log_info("Worker thread started")
        
        # Start WhatsApp monitoring
        if self.whatsapp_monitor:
            self.whatsapp_monitor.start(
                poll_interval=self.agent.config.check_interval_minutes * 60
            )
        
        # Keep thread alive until stop is requested
        while not self._stop_event.is_set():
            time.sleep(1)
        
        # Cleanup
        if self.whatsapp_monitor:
            self.whatsapp_monitor.stop()
        
        self.log_info("Worker thread stopped")
    
    def stop(self):
        """Stop agent orchestration"""
        if not self.running:
            self.log_warning("Orchestrator not running")
            return
        
        self.log_info(f"Stopping orchestration for agent: {self.agent.name}")
        
        self.agent.status = AgentStatus.STOPPING
        
        # Signal worker thread to stop
        self._stop_event.set()
        
        # Wait for thread to finish
        if self._worker_thread and self._worker_thread.is_alive():
            self._worker_thread.join(timeout=10)
        
        self.running = False
        self.agent.status = AgentStatus.STOPPED
        
        # Logout from platforms
        for client in self._platform_clients.values():
            if hasattr(client, 'logout'):
                try:
                    client.logout()
                except Exception as e:
                    self.log_warning(f"Error during platform logout: {e}")
        
        self._platform_clients.clear()
        
        self.log_info("Orchestration stopped")
    
    def pause(self):
        """Pause agent orchestration"""
        if not self.running:
            self.log_warning("Cannot pause: not running")
            return
        
        self.paused = True
        self.agent.status = AgentStatus.PAUSED
        self.log_info("Orchestration paused")
    
    def resume(self):
        """Resume agent orchestration"""
        if not self.paused:
            self.log_warning("Cannot resume: not paused")
            return
        
        self.paused = False
        self.agent.status = AgentStatus.RUNNING
        self.log_info("Orchestration resumed")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get orchestration statistics
        
        Returns:
            Statistics dict
        """
        return {
            "agent_name": self.agent.name,
            "running": self.running,
            "paused": self.paused,
            "status": self.agent.status,
            "total_videos_processed": self.total_videos_processed,
            "total_posts_successful": self.total_posts_successful,
            "total_posts_failed": self.total_posts_failed,
            "last_check": self.agent.last_check.isoformat() if self.agent.last_check else None,
            "last_post": self.agent.last_post.isoformat() if self.agent.last_post else None,
        }


# Convenience function

def run_agent(
    agent: Agent,
    encryption_manager: Optional[Encryptor] = None,
) -> AgentOrchestrator:
    """
    Quick function to run agent
    
    Args:
        agent: Agent to run
        encryption_manager: Optional encryption manager
        
    Returns:
        Running orchestrator
    """
    orchestrator = AgentOrchestrator(agent, encryption_manager)
    orchestrator.start()
    return orchestrator


# Export public API
__all__ = [
    "OrchestrationResult",
    "AgentOrchestrator",
    "run_agent",
]
