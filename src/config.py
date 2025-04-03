import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Database Configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "your_mysql_password"),
    "database": os.getenv("DB_NAME", "password_manager")
}

# AES Encryption Key (Should be securely stored and not hardcoded)
AES_KEY = os.getenv("AES_KEY")

# Validate AES_KEY
if not AES_KEY or len(AES_KEY) != 32:
    raise ValueError("Invalid or missing AES_KEY in environment variables. Please set a secure 32-byte key in the .env file.")

AES_KEY = AES_KEY.encode()
