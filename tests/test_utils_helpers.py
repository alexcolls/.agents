"""
Tests for utils/helpers module
"""

import pytest
from pathlib import Path

from src.utils.helpers import (
    generate_secure_password,
    sanitize_filename,
    extract_video_urls,
    format_file_size,
    retry_on_failure,
)


class TestPasswordGeneration:
    """Test password generation functions"""
    
    def test_generate_secure_password_default_length(self):
        """Test default password length"""
        password = generate_secure_password()
        assert len(password) >= 16
    
    def test_generate_secure_password_custom_length(self):
        """Test custom password length"""
        password = generate_secure_password(length=32)
        assert len(password) >= 32
    
    def test_generate_secure_password_contains_mixed_chars(self):
        """Test password contains different character types"""
        password = generate_secure_password(length=20)
        assert any(c.isupper() for c in password)
        assert any(c.islower() for c in password)
        assert any(c.isdigit() for c in password)


class TestFilenameUtils:
    """Test filename utility functions"""
    
    def test_sanitize_filename_basic(self):
        """Test basic filename sanitization"""
        result = sanitize_filename("test file.txt")
        assert result == "test_file.txt"
    
    def test_sanitize_filename_special_chars(self):
        """Test sanitization of special characters"""
        result = sanitize_filename("test/file:name?.txt")
        assert "/" not in result
        assert ":" not in result
        assert "?" not in result
    
    def test_sanitize_filename_unicode(self):
        """Test sanitization of unicode characters"""
        result = sanitize_filename("tëst_fîlé.txt")
        assert result.isascii()


class TestVideoURLExtraction:
    """Test video URL extraction"""
    
    def test_extract_youtube_url(self):
        """Test YouTube URL extraction"""
        text = "Check out this video: https://www.youtube.com/watch?v=ABC123"
        urls = extract_video_urls(text)
        assert len(urls) == 1
        assert "youtube.com" in urls[0]
    
    def test_extract_instagram_url(self):
        """Test Instagram URL extraction"""
        text = "Look at https://www.instagram.com/p/ABC123/ amazing!"
        urls = extract_video_urls(text)
        assert len(urls) == 1
        assert "instagram.com" in urls[0]
    
    def test_extract_multiple_urls(self):
        """Test extracting multiple URLs"""
        text = """
        Check these out:
        https://www.youtube.com/watch?v=ABC123
        https://www.instagram.com/p/XYZ789/
        """
        urls = extract_video_urls(text)
        assert len(urls) >= 2
    
    def test_extract_no_urls(self):
        """Test text with no URLs"""
        text = "This is just regular text without URLs"
        urls = extract_video_urls(text)
        assert len(urls) == 0


class TestFileUtils:
    """Test file utility functions"""
    
    def test_format_file_size_bytes(self):
        """Test formatting bytes"""
        assert "B" in format_file_size(512)
    
    def test_format_file_size_kilobytes(self):
        """Test formatting kilobytes"""
        result = format_file_size(1024)
        assert "KB" in result or "KiB" in result
    
    def test_format_file_size_megabytes(self):
        """Test formatting megabytes"""
        result = format_file_size(1024 * 1024)
        assert "MB" in result or "MiB" in result
    
    def test_format_file_size_gigabytes(self):
        """Test formatting gigabytes"""
        result = format_file_size(1024 * 1024 * 1024)
        assert "GB" in result or "GiB" in result


class TestRetryLogic:
    """Test retry decorator"""
    
    def test_retry_success_first_attempt(self):
        """Test successful function on first attempt"""
        call_count = [0]
        
        @retry_on_failure(max_attempts=3)
        def succeed():
            call_count[0] += 1
            return "success"
        
        result = succeed()
        assert result == "success"
        assert call_count[0] == 1
    
    def test_retry_success_after_failures(self):
        """Test successful function after retries"""
        call_count = [0]
        
        @retry_on_failure(max_attempts=3, delay=0.1)
        def fail_twice():
            call_count[0] += 1
            if call_count[0] < 3:
                raise ValueError("Not yet")
            return "success"
        
        result = fail_twice()
        assert result == "success"
        assert call_count[0] == 3
    
    def test_retry_exhausted(self):
        """Test retry exhaustion"""
        @retry_on_failure(max_attempts=2, delay=0.1)
        def always_fail():
            raise ValueError("Always fails")
        
        with pytest.raises(ValueError):
            always_fail()


@pytest.mark.unit
class TestHelpersSmokeTests:
    """Smoke tests for helpers module"""
    
    def test_all_functions_importable(self):
        """Test all main functions can be imported"""
        from src.utils import helpers
        assert hasattr(helpers, 'generate_secure_password')
        assert hasattr(helpers, 'sanitize_filename')
        assert hasattr(helpers, 'extract_video_urls')
        assert hasattr(helpers, 'format_file_size')
