from App.models import User
from App.database import db
from App.models import Admin


def create_admin(username, email, password):
    new_admin = Admin(username=username, email=email, password=password)
    db.session.add(new_admin)
    db.session.commit()
    return new_admin

def get_all_admins():
    return Admin.query.all()

# Print the list of admins
admins = get_all_admins()
for admin in admins:
    print(admin)