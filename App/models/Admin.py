from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from .user import User

class Admin(User):
    __tablename__ = 'admin'
    user_id = db.Column(db.String(120), unique=True)

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

    def __init__(self, user_id, username, email, password):
        super().__init__(username, email, password)  
        self.user_id = user_id

    def get_all_todos_json(self):
        users = User.query.all()
        return [users.get_json() for user in users] if users else []

    def get_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "user_id": self.user_id,
            "type": "admin"  
        }

    def __repr__(self):
        return f'<Admin {self.id} : {self.username} - {self.email}>'
