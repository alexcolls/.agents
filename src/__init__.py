"""
.agents - Social Media Automation

Automate social media posting by monitoring WhatsApp groups for video links.
"""

__version__ = "0.1.0"
__author__ = "Alex Colls Outumuro"
__email__ = "alex@example.com"
__license__ = "MIT"

from src.utils.config import Config
from src.utils.logger import setup_logger

__all__ = ["Config", "setup_logger", "__version__"]