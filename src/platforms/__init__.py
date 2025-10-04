"""Social media platform integrations"""

from src.platforms.instagram import InstagramClient, PostResult
from src.platforms.whatsapp import (
    WhatsAppClient,
    WhatsAppMonitor,
    WhatsAppMessage,
    MessageType,
)

__all__ = [
    "InstagramClient",
    "PostResult",
    "WhatsAppClient",
    "WhatsAppMonitor",
    "WhatsAppMessage",
    "MessageType",
]
