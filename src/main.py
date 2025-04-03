import sys
from getpass import getpass  
from auth import register_user, login_user, delete_user_account
from database import connect_db
from encryption import encrypt_password, decrypt_password
from gui import launch_gui  # Import GUI function

def main():
    print("\n🔐 Secure Password Manager 🔐")
    print("1. Use Command Line Interface (CLI)")
    print("2. Use Graphical User Interface (GUI)")
    
    mode = input("Choose (1/2): ")
    
    if mode == "2":
        launch_gui()
        return  # Exit CLI flow if GUI is chosen
    
    while True:
        print("\n🔐 Secure Password Manager 🔐")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose (1/2/3): ")

        if choice == "1":
            username = input("Enter a new username: ")
            master_password = getpass("Set a master password: ")  # Hidden input
            register_user(username, master_password)

        elif choice == "2":
            username = input("Enter your username: ")
            master_password = getpass("Enter your master password: ")  # Hidden input
            user_id = login_user(username, master_password)

            if user_id:
                manage_passwords(user_id, username)  # Pass username for account deletion

        elif choice == "3":
            print("Exiting...")
            sys.exit()

        else:
            print("❌ Invalid choice. Try again.")

def manage_passwords(user_id, username):
    """Function to manage stored passwords after login"""
    while True:
        print("\n🔑 Password Manager Menu")
        print("1. Store a new password")
        print("2. Retrieve a stored password")
        print("3. Delete a stored password")
        print("4. Delete your account")
        print("5. Logout")

        choice = input("Choose (1/2/3/4/5): ")

        if choice == "1":
            website = input("Enter the website/app name: ")
            stored_password = getpass("Enter the password to store: ")  # Hidden input

            encrypted_password = encrypt_password(stored_password)
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO passwords (user_id, website, encrypted_password) VALUES (%s, %s, %s)",
                (user_id, website, encrypted_password),
            )
            conn.commit()
            cursor.close()
            conn.close()
            print("✅ Password stored successfully!")

        elif choice == "2":
            website = input("Enter the website/app name to retrieve password: ")

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT encrypted_password FROM passwords WHERE user_id = %s AND website = %s",
                (user_id, website),
            )
            result = cursor.fetchone()
            cursor.close()
            conn.close()

            if result:
                decrypted_password = decrypt_password(result[0])
                print(f"🔓 Password for {website}: {decrypted_password}")  
            else:
                print("❌ No password found for this website.")

        elif choice == "3":  
            website = input("Enter the website/app name to delete password: ")

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM passwords WHERE user_id = %s AND website = %s",
                (user_id, website),
            )
            conn.commit()
            cursor.close()
            conn.close()

            print(f"🗑️ Password for {website} deleted successfully!")

        elif choice == "4":
            confirm = input("⚠️ Are you sure you want to delete your account? (yes/no): ").lower()
            if confirm == "yes":
                delete_user_account(username)  
                print("Your account has been deleted. Logging out...")
                break

        elif choice == "5":
            print("Logging out...")
            break

        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
