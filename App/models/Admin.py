from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from .user import User

class Admin(User):
    def __init__(self, username, email, password):
        super().__init__(username, email, password)

    def __repr__(self):
        return f"<Admin {self.username}>"