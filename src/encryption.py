from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64
import os
from config import AES_KEY  

def encrypt_password(password: str) -> str:
    """Encrypts a password using AES encryption."""
    try:
        password_bytes = password.encode()

        # Generate a random IV (Initialization Vector)
        iv = os.urandom(16)

        # Create AES cipher
        cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv))
        encryptor = cipher.encryptor()

        # Pad password to be multiple of block size (16 bytes)
        padding_length = 16 - (len(password_bytes) % 16)
        padded_password = password_bytes + bytes([padding_length] * padding_length)

        # Encrypt
        encrypted_password = encryptor.update(padded_password) + encryptor.finalize()

        # Encode as Base64 for storage
        encrypted_data = base64.b64encode(iv + encrypted_password).decode()
        return encrypted_data
    
    except Exception as e:
        return f"⚠️ Encryption Error: {str(e)}"

def decrypt_password(encrypted_data: str) -> str:
    """Decrypts an AES-encrypted password."""
    try:
        encrypted_data_bytes = base64.b64decode(encrypted_data)

        # Extract IV and encrypted password
        iv = encrypted_data_bytes[:16]
        encrypted_password = encrypted_data_bytes[16:]

        # Create AES cipher
        cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv))
        decryptor = cipher.decryptor()

        # Decrypt
        decrypted_padded_password = decryptor.update(encrypted_password) + decryptor.finalize()

        # Remove padding
        padding_length = decrypted_padded_password[-1]
        decrypted_password = decrypted_padded_password[:-padding_length]

        return decrypted_password.decode()
    
    except Exception as e:
        return f"⚠️ Decryption Error: {str(e)}"
