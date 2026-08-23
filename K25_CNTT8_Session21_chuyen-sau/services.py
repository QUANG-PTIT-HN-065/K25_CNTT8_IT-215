from datetime import datetime, timedelta, timezone
import os

import bcrypt
from dotenv import load_dotenv
from jose import jwt
from sqlalchemy.orm import Session

from models import User


load_dotenv()



SECRET_KEY = os.environ["SECRET_KEY"]

ALGORITHM = os.getenv(
    "ALGORITHM",
    "HS256"
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "30"
    )
)


def get_user_by_email(
    db: Session,
    email: str
):
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def get_user_by_id(
    db: Session,
    user_id: int
):
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )



def hash_password(password: str):

    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(
    password: str,
    password_hash: str
):

    return bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash.encode("utf-8")
    )


def create_user(
    db: Session,
    email: str,
    password: str,
    full_name: str
):

    password_hash = hash_password(password)

    user = User(
        email=email,
        password_hash=password_hash,
        full_name=full_name,
        role="student",
        is_active=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def create_access_token(user: User):

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload = {
        "sub": user.email,
        "user_id": user.id,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def decode_access_token(token: str):

    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )