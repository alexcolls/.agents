"""
Encryption and decryption for sensitive data.

Uses Fernet (symmetric encryption) with AES-256 in CBC mode.
The encryption key is derived from the MASTER_PASSWORD using PBKDF2.
"""

import base64
import hashlib
import json
from typing import Any, Optional

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2

from agents.utils.constants import ENCRYPTION_ALGORITHM, ErrorMessages
from agents.utils.logger import get_logger

logger = get_logger(__name__)


class EncryptionError(Exception):
    """Raised when encryption or decryption fails."""
    pass


class Encryptor:
    """
    Handles encryption and decryption of sensitive data.
    
    Uses Fernet (AES-256) with a key derived from the master password.
    """
    
    # Salt for key derivation (should be constant for this application)
    # In production, you might want to generate this per installation
    SALT = b"agents_encryption_salt_v1_do_not_change"
    
    # Number of iterations for PBKDF2 (higher = more secure but slower)
    ITERATIONS = 480000  # OWASP recommendation for 2023
    
    def __init__(self, master_password: str):
        """
        Initialize encryptor with master password.
        
        Args:
            master_password: Master password for encryption
            
        Raises:
            EncryptionError: If password is invalid or key derivation fails
        """
        if not master_password:
            raise EncryptionError("Master password cannot be empty")
        
        self.master_password = master_password
        self._fernet: Optional[Fernet] = None
        
        try:
            self._derive_key()
        except Exception as e:
            logger.error(f"Failed to derive encryption key: {e}")
            raise EncryptionError(f"Failed to initialize encryption: {e}")
    
    def _derive_key(self) -> None:
        """
        Derive encryption key from master password using PBKDF2.
        
        This ensures the actual encryption key is never stored,
        only derived from the password when needed.
        """
        # Derive key using PBKDF2
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,  # 256 bits for AES-256
            salt=self.SALT,
            iterations=self.ITERATIONS,
        )
        
        # Convert password to bytes
        password_bytes = self.master_password.encode("utf-8")
        
        # Derive the key
        key = kdf.derive(password_bytes)
        
        # Fernet requires base64-encoded key
        key_base64 = base64.urlsafe_b64encode(key)
        
        # Initialize Fernet
        self._fernet = Fernet(key_base64)
        
        logger.debug("Encryption key derived successfully")
    
    def encrypt(self, data: str) -> str:
        """
        Encrypt a string.
        
        Args:
            data: Plain text string to encrypt
            
        Returns:
            str: Encrypted data as base64 string
            
        Raises:
            EncryptionError: If encryption fails
            
        Examples:
            >>> encryptor = Encryptor("my-secret-password")
            >>> encrypted = encryptor.encrypt("sensitive data")
            >>> encrypted.startswith("gAAAAA")  # Fernet tokens start with this
            True
        """
        if not data:
            return ""
        
        try:
            # Convert to bytes
            data_bytes = data.encode("utf-8")
            
            # Encrypt
            encrypted_bytes = self._fernet.encrypt(data_bytes)
            
            # Return as string
            return encrypted_bytes.decode("utf-8")
            
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise EncryptionError(f"{ErrorMessages.ENCRYPTION_FAILED}: {e}")
    
    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypt an encrypted string.
        
        Args:
            encrypted_data: Encrypted data as base64 string
            
        Returns:
            str: Decrypted plain text string
            
        Raises:
            EncryptionError: If decryption fails (wrong password, corrupted data)
            
        Examples:
            >>> encryptor = Encryptor("my-secret-password")
            >>> encrypted = encryptor.encrypt("sensitive data")
            >>> decrypted = encryptor.decrypt(encrypted)
            >>> decrypted
            'sensitive data'
        """
        if not encrypted_data:
            return ""
        
        try:
            # Convert to bytes
            encrypted_bytes = encrypted_data.encode("utf-8")
            
            # Decrypt
            decrypted_bytes = self._fernet.decrypt(encrypted_bytes)
            
            # Return as string
            return decrypted_bytes.decode("utf-8")
            
        except InvalidToken:
            logger.error("Decryption failed: Invalid token (wrong password or corrupted data)")
            raise EncryptionError(
                f"{ErrorMessages.ENCRYPTION_FAILED}: Invalid token. "
                "This usually means the MASTER_PASSWORD is wrong or the data is corrupted."
            )
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise EncryptionError(f"{ErrorMessages.ENCRYPTION_FAILED}: {e}")
    
    def encrypt_dict(self, data: dict[str, Any]) -> str:
        """
        Encrypt a dictionary by converting to JSON first.
        
        Args:
            data: Dictionary to encrypt
            
        Returns:
            str: Encrypted JSON as base64 string
            
        Examples:
            >>> encryptor = Encryptor("my-secret-password")
            >>> data = {"username": "john", "password": "secret"}
            >>> encrypted = encryptor.encrypt_dict(data)
            >>> len(encrypted) > 0
            True
        """
        try:
            # Convert dict to JSON string
            json_str = json.dumps(data, ensure_ascii=False)
            
            # Encrypt the JSON string
            return self.encrypt(json_str)
            
        except Exception as e:
            logger.error(f"Failed to encrypt dictionary: {e}")
            raise EncryptionError(f"Failed to encrypt dictionary: {e}")
    
    def decrypt_dict(self, encrypted_data: str) -> dict[str, Any]:
        """
        Decrypt an encrypted dictionary.
        
        Args:
            encrypted_data: Encrypted JSON as base64 string
            
        Returns:
            dict: Decrypted dictionary
            
        Examples:
            >>> encryptor = Encryptor("my-secret-password")
            >>> data = {"username": "john", "password": "secret"}
            >>> encrypted = encryptor.encrypt_dict(data)
            >>> decrypted = encryptor.decrypt_dict(encrypted)
            >>> decrypted == data
            True
        """
        try:
            # Decrypt to JSON string
            json_str = self.decrypt(encrypted_data)
            
            # Parse JSON
            return json.loads(json_str)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse decrypted JSON: {e}")
            raise EncryptionError(f"Decrypted data is not valid JSON: {e}")
        except Exception as e:
            logger.error(f"Failed to decrypt dictionary: {e}")
            raise EncryptionError(f"Failed to decrypt dictionary: {e}")
    
    def encrypt_credentials(self, username: str, password: str) -> dict[str, str]:
        """
        Encrypt username and password.
        
        Args:
            username: Username (not encrypted for easier searching)
            password: Password to encrypt
            
        Returns:
            dict: Dictionary with plain username and encrypted password
            
        Examples:
            >>> encryptor = Encryptor("my-secret-password")
            >>> creds = encryptor.encrypt_credentials("john", "secret123")
            >>> creds["username"]
            'john'
            >>> creds["password"].startswith("gAAAAA")
            True
        """
        return {
            "username": username,  # Username not encrypted for easier management
            "password": self.encrypt(password),
        }
    
    def decrypt_credentials(self, encrypted_creds: dict[str, str]) -> tuple[str, str]:
        """
        Decrypt credentials.
        
        Args:
            encrypted_creds: Dictionary with username and encrypted password
            
        Returns:
            tuple: (username, password)
            
        Examples:
            >>> encryptor = Encryptor("my-secret-password")
            >>> creds = encryptor.encrypt_credentials("john", "secret123")
            >>> username, password = encryptor.decrypt_credentials(creds)
            >>> username
            'john'
            >>> password
            'secret123'
        """
        username = encrypted_creds.get("username", "")
        encrypted_password = encrypted_creds.get("password", "")
        
        if not username or not encrypted_password:
            raise EncryptionError("Invalid credentials format")
        
        password = self.decrypt(encrypted_password)
        
        return username, password


def generate_encryption_key_hash(password: str) -> str:
    """
    Generate a hash of the encryption key for verification.
    
    This can be used to verify if the correct password is being used
    without storing the password itself.
    
    Args:
        password: Master password
        
    Returns:
        str: SHA-256 hash of the password
        
    Examples:
        >>> hash1 = generate_encryption_key_hash("password123")
        >>> hash2 = generate_encryption_key_hash("password123")
        >>> hash1 == hash2
        True
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_encryption_key(password: str, stored_hash: str) -> bool:
    """
    Verify if a password matches the stored hash.
    
    Args:
        password: Password to verify
        stored_hash: Previously stored hash
        
    Returns:
        bool: True if password matches, False otherwise
        
    Examples:
        >>> password = "my-secret"
        >>> hash_value = generate_encryption_key_hash(password)
        >>> verify_encryption_key("my-secret", hash_value)
        True
        >>> verify_encryption_key("wrong-password", hash_value)
        False
    """
    return generate_encryption_key_hash(password) == stored_hash


# Global encryptor instance (initialized when config is loaded)
_encryptor: Optional[Encryptor] = None


def get_encryptor(master_password: Optional[str] = None) -> Encryptor:
    """
    Get the global encryptor instance.
    
    Args:
        master_password: Master password. If None, uses password from config
        
    Returns:
        Encryptor: Global encryptor instance
        
    Raises:
        EncryptionError: If master password is not available
    """
    global _encryptor
    
    if _encryptor is None:
        if master_password is None:
            # Try to get from config
            try:
                from agents.utils.config import get_config
                config = get_config()
                master_password = config.master_password
            except Exception as e:
                raise EncryptionError(
                    f"Cannot initialize encryptor: {e}\n"
                    "Please ensure MASTER_PASSWORD is set in .env file"
                )
        
        _encryptor = Encryptor(master_password)
    
    return _encryptor


# Convenience functions for quick encryption/decryption
def encrypt(data: str) -> str:
    """
    Quick encryption using global encryptor.
    
    Args:
        data: Data to encrypt
        
    Returns:
        str: Encrypted data
    """
    return get_encryptor().encrypt(data)


def decrypt(encrypted_data: str) -> str:
    """
    Quick decryption using global encryptor.
    
    Args:
        encrypted_data: Encrypted data
        
    Returns:
        str: Decrypted data
    """
    return get_encryptor().decrypt(encrypted_data)


# Example usage and testing
if __name__ == "__main__":
    # Test encryption
    test_password = "test-master-password-12345"
    encryptor = Encryptor(test_password)
    
    # Test string encryption
    original = "This is sensitive data!"
    encrypted = encryptor.encrypt(original)
    decrypted = encryptor.decrypt(encrypted)
    
    print(f"Original: {original}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Match: {original == decrypted}")
    
    # Test dictionary encryption
    data = {
        "username": "john_doe",
        "password": "super_secret_123",
        "email": "john@example.com"
    }
    
    encrypted_dict = encryptor.encrypt_dict(data)
    decrypted_dict = encryptor.decrypt_dict(encrypted_dict)
    
    print(f"\nOriginal dict: {data}")
    print(f"Encrypted: {encrypted_dict}")
    print(f"Decrypted: {decrypted_dict}")
    print(f"Match: {data == decrypted_dict}")
    
    # Test credential encryption
    creds = encryptor.encrypt_credentials("testuser", "testpassword")
    username, password = encryptor.decrypt_credentials(creds)
    
    print(f"\nCredentials: {creds}")
    print(f"Decrypted: username={username}, password={password}")
