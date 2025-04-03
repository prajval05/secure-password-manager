from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, 
    QMessageBox, QInputDialog, QTableWidget, QTableWidgetItem
)
from auth import register_user, login_user
from database import add_password, get_passwords, delete_password, delete_user
from encryption import encrypt_password, decrypt_password
import sys

class PasswordManagerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.user_id = None
        self.table_window = None  # Store reference for password retrieval window
        self.init_login_screen()

    def clear_layout(self):
        """Clears the existing layout to prevent multiple layouts on the same widget."""
        if self.layout():
            QWidget().setLayout(self.layout())

    def init_login_screen(self):
        """Initializes the login screen."""
        self.setWindowTitle("🔐 Secure Password Manager - Login")
        self.setGeometry(100, 100, 400, 300)
        self.clear_layout()

        layout = QVBoxLayout()
        
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Enter Username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter Master Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def login(self):
        """Handles user login."""
        username = self.username_input.text()
        password = self.password_input.text()
        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Username and password cannot be empty.")
            return
        
        user = login_user(username, password)
        if user:
            self.user_id = user[0]  # Retrieve user_id correctly
            self.init_dashboard()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    def register(self):
        """Handles user registration."""
        username = self.username_input.text()
        password = self.password_input.text()
        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Username and password cannot be empty.")
            return
        
        if register_user(username, password):
            QMessageBox.information(self, "Success", "Registration successful. You can now log in.")
        else:
            QMessageBox.warning(self, "Error", "Username already exists.")

    def init_dashboard(self):
        """Initializes the dashboard."""
        self.setWindowTitle("🔑 Password Manager Dashboard")
        self.setGeometry(100, 100, 500, 400)
        self.clear_layout()

        layout = QVBoxLayout()

        store_btn = QPushButton("Store a New Password", self)
        store_btn.clicked.connect(self.store_password)
        layout.addWidget(store_btn)

        retrieve_btn = QPushButton("Retrieve a Stored Password", self)
        retrieve_btn.clicked.connect(self.retrieve_password)
        layout.addWidget(retrieve_btn)

        delete_btn = QPushButton("Delete a Stored Password", self)
        delete_btn.clicked.connect(self.delete_password)
        layout.addWidget(delete_btn)

        delete_acc_btn = QPushButton("Delete Your Account", self)
        delete_acc_btn.clicked.connect(self.delete_account)
        layout.addWidget(delete_acc_btn)

        logout_btn = QPushButton("Logout", self)
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)

        self.setLayout(layout)

    def store_password(self):
        """Stores an encrypted password."""
        website, ok = QInputDialog.getText(self, "Store Password", "Enter Website:")
        if ok and website:
            password, ok = QInputDialog.getText(self, "Store Password", "Enter Password:")
            if ok and password:
                encrypted_password = encrypt_password(password)
                if add_password(self.user_id, website, encrypted_password):
                    QMessageBox.information(self, "Success", "Password stored successfully!")
                else:
                    QMessageBox.warning(self, "Error", "Failed to store password.")

    def retrieve_password(self):
        """Retrieves stored passwords and displays them in a table."""
        passwords = get_passwords(self.user_id)
        if not passwords:
            QMessageBox.information(self, "No Data", "No passwords stored.")
            return

        self.table_window = QWidget()
        self.table_window.setWindowTitle("Stored Passwords")
        self.table_window.setGeometry(150, 150, 400, 300)

        layout = QVBoxLayout()

        table = QTableWidget()
        table.setRowCount(len(passwords))
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Website", "Decrypted Password"])

        for row, (website, enc_password) in enumerate(passwords):
            decrypted_pass = decrypt_password(enc_password)
            table.setItem(row, 0, QTableWidgetItem(website))
            table.setItem(row, 1, QTableWidgetItem(decrypted_pass))

        layout.addWidget(table)
        self.table_window.setLayout(layout)
        self.table_window.show()

    def delete_password(self):
        """Deletes a stored password."""
        website, ok = QInputDialog.getText(self, "Delete Password", "Enter Website to delete:")
        if ok and website:
            if delete_password(self.user_id, website):
                QMessageBox.information(self, "Success", "Password deleted successfully!")
            else:
                QMessageBox.warning(self, "Error", "Password not found.")

    def delete_account(self):
        """Deletes the user's account."""
        confirm = QMessageBox.question(
            self, "Delete Account", "Are you sure? This cannot be undone!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            if delete_user(self.user_id):
                QMessageBox.information(self, "Deleted", "Account deleted successfully!")
                self.logout()
            else:
                QMessageBox.warning(self, "Error", "Failed to delete account.")

    def logout(self):
        """Logs out the user."""
        self.user_id = None
        self.init_login_screen()

def launch_gui():
    """Launches the GUI application."""
    app = QApplication(sys.argv)
    window = PasswordManagerGUI()
    window.show()
    sys.exit(app.exec())

# Allow direct execution of this script
if __name__ == "__main__":
    launch_gui()
