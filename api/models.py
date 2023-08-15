import os
import base64
import hashlib

from sqlalchemy import Column, Integer, String, DateTime
from api.database import Base
import flask_login

from .database import db_session

class User(Base, flask_login.UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True)
    salt = Column(String(4))

    # Password hashed using the sha256 algorithm
    password = Column(String(64))

    def __init__(self, email=None, password=None):
        self.email = email

        # Use a 3 character salt
        self.salt = base64.b64encode(os.urandom(2)).decode('ascii')[:3]
        self.password = self.hash_password(password, self.salt)

    @classmethod
    def hash_password(cls, password, salt):
        hashed_password = hashlib.sha256(password.encode()).digest()
        second_hash = hashlib.sha256(hashed_password + salt.encode())

        return second_hash.hexdigest()

    def __repr__(self):
        return f'<User {self.email!r}>'
