from models import User
from db_config import db
import bcrypt

def create_user(username, password):
    if User.query.filter_by(username=username).first():
        return {"error": "User already exists"}, 400

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    new_user = User(username=username, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return {"message": "User registered successfully"}, 201


def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if not user:
        return None

    if bcrypt.checkpw(password.encode("utf-8"), user.password_hash):
        return user
    return None


def get_user_by_id(user_id: int):
    return User.query.get(user_id)