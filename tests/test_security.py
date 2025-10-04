"""
Tests for security modules (encryption and validators)
"""

import pytest
from pathlib import Path

from src.security.encryption import EncryptionManager
from src.security.validators import (
    validate_agent_name,
    validate_username,
    validate_password,
    validate_email,
    validate_url,
    validate_platform,
    validate_video_file,
    sanitize_input,
    sanitize_path,
)


class TestEncryption:
    """Test encryption functionality"""
    
    def test_encryption_manager_init(self):
        """Test EncryptionManager initialization"""
        manager = EncryptionManager("test_password_123")
        assert manager is not None
    
    def test_encrypt_decrypt_string(self):
        """Test string encryption and decryption"""
        manager = EncryptionManager("test_password_123")
        original = "secret_data"
        
        encrypted = manager.encrypt_string(original)
        decrypted = manager.decrypt_string(encrypted)
        
        assert encrypted != original
        assert decrypted == original
    
    def test_encrypt_decrypt_dict(self):
        """Test dictionary encryption and decryption"""
        manager = EncryptionManager("test_password_123")
        original = {"key": "value", "number": 42}
        
        encrypted = manager.encrypt_dict(original)
        decrypted = manager.decrypt_dict(encrypted)
        
        assert encrypted != original
        assert decrypted == original
    
    def test_encrypt_decrypt_credentials(self):
        """Test credentials encryption"""
        manager = EncryptionManager("test_password_123")
        credentials = {
            "username": "testuser",
            "password": "testpass123"
        }
        
        encrypted = manager.encrypt_credentials(credentials)
        decrypted = manager.decrypt_credentials(encrypted)
        
        assert decrypted["username"] == credentials["username"]
        assert decrypted["password"] == credentials["password"]
    
    def test_password_hashing(self):
        """Test password hash generation and verification"""
        manager = EncryptionManager("test_password_123")
        password = "mypassword"
        
        hash1 = manager.hash_password(password)
        hash2 = manager.hash_password(password)
        
        # Different salts should produce different hashes
        assert hash1 != hash2
        
        # But both should verify correctly
        assert manager.verify_password(password, hash1)
        assert manager.verify_password(password, hash2)
    
    def test_wrong_password_fails_verification(self):
        """Test wrong password fails verification"""
        manager = EncryptionManager("test_password_123")
        password = "correct_password"
        wrong = "wrong_password"
        
        hash_value = manager.hash_password(password)
        assert not manager.verify_password(wrong, hash_value)


class TestValidators:
    """Test validation functions"""
    
    def test_validate_agent_name_valid(self):
        """Test valid agent names"""
        assert validate_agent_name("my-agent") is True
        assert validate_agent_name("agent_123") is True
        assert validate_agent_name("test") is True
    
    def test_validate_agent_name_invalid(self):
        """Test invalid agent names"""
        assert validate_agent_name("") is False
        assert validate_agent_name("ab") is False  # Too short
        assert validate_agent_name("agent with spaces") is False
        assert validate_agent_name("agent@special") is False
    
    def test_validate_username_valid(self):
        """Test valid usernames"""
        assert validate_username("user123") is True
        assert validate_username("test_user") is True
        assert validate_username("user.name") is True
    
    def test_validate_username_invalid(self):
        """Test invalid usernames"""
        assert validate_username("") is False
        assert validate_username("ab") is False  # Too short
        assert validate_username("user@name") is False
    
    def test_validate_password_valid(self):
        """Test valid passwords"""
        assert validate_password("password123") is True
        assert validate_password("MyP@ssw0rd!") is True
    
    def test_validate_password_invalid(self):
        """Test invalid passwords"""
        assert validate_password("") is False
        assert validate_password("short") is False  # Too short
    
    def test_validate_email_valid(self):
        """Test valid emails"""
        assert validate_email("user@example.com") is True
        assert validate_email("test.user@domain.co.uk") is True
    
    def test_validate_email_invalid(self):
        """Test invalid emails"""
        assert validate_email("notanemail") is False
        assert validate_email("user@") is False
        assert validate_email("@domain.com") is False
    
    def test_validate_url_valid(self):
        """Test valid URLs"""
        assert validate_url("https://example.com") is True
        assert validate_url("http://example.com/path") is True
    
    def test_validate_url_invalid(self):
        """Test invalid URLs"""
        assert validate_url("notaurl") is False
        assert validate_url("ftp://example.com") is False  # Not http/https
    
    def test_validate_platform_valid(self):
        """Test valid platforms"""
        assert validate_platform("instagram") is True
        assert validate_platform("tiktok") is True
    
    def test_validate_platform_invalid(self):
        """Test invalid platforms"""
        assert validate_platform("invalid_platform") is False
        assert validate_platform("") is False
    
    def test_validate_video_file(self, temp_dir):
        """Test video file validation"""
        # Create a dummy file
        video_file = temp_dir / "test.mp4"
        video_file.write_text("dummy video content")
        
        assert validate_video_file(video_file) is True
        assert validate_video_file(temp_dir / "nonexistent.mp4") is False


class TestSanitization:
    """Test input sanitization"""
    
    def test_sanitize_input_basic(self):
        """Test basic input sanitization"""
        result = sanitize_input("normal text")
        assert result == "normal text"
    
    def test_sanitize_input_removes_html(self):
        """Test HTML removal"""
        result = sanitize_input("<script>alert('xss')</script>")
        assert "<script>" not in result
    
    def test_sanitize_input_removes_sql(self):
        """Test SQL injection prevention"""
        result = sanitize_input("user' OR '1'='1")
        # Should not contain dangerous SQL patterns
        assert result != "user' OR '1'='1"
    
    def test_sanitize_path_prevents_traversal(self):
        """Test path traversal prevention"""
        result = sanitize_path("../../../etc/passwd")
        assert ".." not in result
        assert result == "etc/passwd" or "passwd" in result
    
    def test_sanitize_path_absolute(self):
        """Test absolute path handling"""
        result = sanitize_path("/absolute/path/file.txt")
        # Should not start with /
        assert not result.startswith("/")


@pytest.mark.unit
class TestSecuritySmokeTests:
    """Smoke tests for security modules"""
    
    def test_encryption_module_importable(self):
        """Test encryption module can be imported"""
        from src.security import encryption
        assert hasattr(encryption, 'EncryptionManager')
    
    def test_validators_module_importable(self):
        """Test validators module can be imported"""
        from src.security import validators
        assert hasattr(validators, 'validate_agent_name')
        assert hasattr(validators, 'validate_username')
        assert hasattr(validators, 'sanitize_input')
