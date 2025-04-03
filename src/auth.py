import bcrypt
from database import connect_db

def hash_password(password: str) -> str:
    """Hashes a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()

def verify_password(password: str, hashed_password: str) -> bool:
    """Verifies if the entered password matches the hashed password."""
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

def register_user(username: str, master_password: str):
    """Registers a new user with a hashed master password."""
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        # Check if username already exists
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return "❌ Username already exists. Try a different one."
        
        # Hash the master password before storing
        hashed_password = hash_password(master_password)

        # Insert new user into the database
        cursor.execute("INSERT INTO users (username, master_password_hash) VALUES (%s, %s)", 
                    (username, hashed_password))
        conn.commit()

        return f"✅ User '{username}' registered successfully!"

    except Exception as e:
        return f"⚠️ Error: {str(e)}"
    
    finally:
        cursor.close()
        conn.close()

def login_user(username: str, master_password: str):
    """Logs in a user by verifying the master password."""
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        # Fetch user details from the database
        cursor.execute("SELECT id, master_password_hash FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            user_id, stored_hashed_password = user
            if verify_password(master_password, stored_hashed_password):
                return user_id, f"✅ Login successful! Welcome, {username}."
            else:
                return None, "❌ Incorrect username or password."
        else:
            return None, "❌ Incorrect username or password."

    except Exception as e:
        return None, f"⚠️ Error: {str(e)}"
    
    finally:
        cursor.close()
        conn.close()

def delete_user_account(username: str):
    """Deletes a user account and all stored passwords."""
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        # Delete passwords first (to maintain database integrity)
        cursor.execute("DELETE FROM passwords WHERE user_id = (SELECT id FROM users WHERE username = %s)", (username,))
        
        # Now delete the user
        cursor.execute("DELETE FROM users WHERE username = %s", (username,))
        
        conn.commit()
        
        return f"🗑️ Account '{username}' and all stored passwords deleted successfully!"

    except Exception as e:
        return f"⚠️ Error: {str(e)}"
    
    finally:
        cursor.close()
        conn.close()

def change_master_password(username: str, old_password: str, new_password: str):
    """Allows a user to change their master password after verification."""
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        # Fetch current hashed password
        cursor.execute("SELECT master_password_hash FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        if user:
            stored_hashed_password = user[0]
            if verify_password(old_password, stored_hashed_password):
                # Hash the new password
                new_hashed_password = hash_password(new_password)
                cursor.execute("UPDATE users SET master_password_hash = %s WHERE username = %s", 
                               (new_hashed_password, username))
                conn.commit()
                return "🔑 Password changed successfully!"
            else:
                return "❌ Incorrect old password."

        return "❌ Username not found."

    except Exception as e:
        return f"⚠️ Error: {str(e)}"
    
    finally:
        cursor.close()
        conn.close()
