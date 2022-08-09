from flask_login import AnonymousUserMixin
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from init import db
from init import login_manager


class AnonymousUser(AnonymousUserMixin):
    """Anonymous user class"""

    def __init__(self):
        self.username = "guest"
        self.email = "<anonymous-user-no-email>"

    def __repr__(self):
        return f"<AnonymousUser {self.username}>"

login_manager.anonymous_user = AnonymousUser

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column(db.String(128), nullable=False)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        # the default hashing method is pbkdf2:sha256
        self._password = generate_password_hash(plaintext)

    def check_password(self, password):
        return check_password_hash(self._password, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
