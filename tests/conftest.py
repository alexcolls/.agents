"""
Pytest configuration and fixtures
"""

import os
import sys
import tempfile
from pathlib import Path
from typing import Generator

import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create temporary directory for tests"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_env(monkeypatch, temp_dir):
    """Mock environment variables for testing"""
    monkeypatch.setenv("MASTER_PASSWORD", "test_password_123")
    monkeypatch.setenv("BASE_DIR", str(temp_dir))
    monkeypatch.setenv("AGENTS_DIR", str(temp_dir / "agents"))
    monkeypatch.setenv("LOGS_DIR", str(temp_dir / "logs"))
    monkeypatch.setenv("TMP_DIR", str(temp_dir / "tmp"))
    monkeypatch.setenv("BUILD_DIR", str(temp_dir / "build"))
    
    # Create directories
    (temp_dir / "agents").mkdir(exist_ok=True)
    (temp_dir / "logs").mkdir(exist_ok=True)
    (temp_dir / "tmp").mkdir(exist_ok=True)
    (temp_dir / "build").mkdir(exist_ok=True)
    
    return temp_dir


@pytest.fixture
def sample_video_url():
    """Sample video URL for testing"""
    return "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


@pytest.fixture
def sample_instagram_url():
    """Sample Instagram URL for testing"""
    return "https://www.instagram.com/p/ABC123/"


@pytest.fixture
def sample_agent_config():
    """Sample agent configuration"""
    return {
        "name": "test-agent",
        "description": "Test agent description",
        "whatsapp_phone": "+1234567890",
        "whatsapp_groups": ["Test Group 1", "Test Group 2"],
        "platforms": {
            "instagram": {
                "username": "testuser",
                "password": "testpass123",
            }
        },
        "auto_caption": True,
        "hashtags": ["test", "automation"],
        "check_interval_minutes": 5,
    }
