from datetime import datetime, timedelta, timezone
import os

import bcrypt
from dotenv import load_dotenv
from jose import jwt
from sqlalchemy.orm import Session

from models import User

load_dotenv()


SECRET_KEY = os.environ["SECRET_KEY"]

ALGORITHM = os.getenv("ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def hash_password(password: str) -> str:

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:

    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_user(db: Session, username: str, password: str):

    hashed_password = hash_password(password)

    user = User(username=username, hashed_password=hashed_password)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def create_access_token(username: str):

    now = datetime.now(timezone.utc)

    expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {"sub": username, "iat": now, "exp": expire}

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return token


def decode_access_token(token: str):

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    return payload
