import mysql.connector
from config import DB_CONFIG

def connect_db():
    """Establishes a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"\u274c Database connection error: {err}")
        return None

def create_tables():
    """Creates required tables if they do not exist."""
    conn = connect_db()
    if not conn:
        return

    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            master_password_hash VARCHAR(255) NOT NULL
        )
    """
    )

    # Create passwords table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            website VARCHAR(255) NOT NULL,
            encrypted_password TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """
    )

    conn.commit()
    cursor.close()
    conn.close()
    print("\u2705 Database tables created successfully!")

def add_user(username: str, hashed_password: str):
    """Inserts a new user into the database."""
    conn = connect_db()
    if not conn:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, master_password_hash) VALUES (%s, %s)", 
                       (username, hashed_password))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"\u274c Error adding user: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

def get_user_by_username(username: str):
    """Retrieves a user by username."""
    conn = connect_db()
    if not conn:
        return None

    cursor = conn.cursor()
    cursor.execute("SELECT id, master_password_hash FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return user

def add_password(user_id: int, website: str, encrypted_password: str):
    """Stores an encrypted password in the database."""
    conn = connect_db()
    if not conn:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO passwords (user_id, website, encrypted_password) VALUES (%s, %s, %s)", 
                       (user_id, website, encrypted_password))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"\u274c Error adding password: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

def get_passwords(user_id: int):
    """Retrieves stored passwords for a given user."""
    conn = connect_db()
    if not conn:
        return []

    cursor = conn.cursor()
    cursor.execute("SELECT website, encrypted_password FROM passwords WHERE user_id = %s", (user_id,))
    passwords = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return passwords

def delete_password(user_id: int, website: str) -> bool:
    """Deletes a stored password for a specific website."""
    conn = connect_db()
    if not conn:
        return False
    
    cursor = conn.cursor()
    cursor.execute("DELETE FROM passwords WHERE user_id = %s AND website = %s", (user_id, website))
    conn.commit()
    rows_deleted = cursor.rowcount
    
    cursor.close()
    conn.close()
    return rows_deleted > 0  # Returns True if deletion was successful

def delete_user(username: str):
    """Deletes a user and their stored passwords."""
    conn = connect_db()
    if not conn:
        return False
    
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE username = %s", (username,))
        conn.commit()
        print(f"\U0001F5D1 User '{username}' and all stored passwords deleted successfully!")
        return True
    except mysql.connector.Error as err:
        print(f"\u274c Error deleting user: {err}")
        return False
    finally:
        cursor.close()
        conn.close()

# Initialize database tables if they don't exist
if __name__ == "__main__":
    create_tables()
