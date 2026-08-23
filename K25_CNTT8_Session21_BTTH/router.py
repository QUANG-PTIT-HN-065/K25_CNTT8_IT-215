from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from sqlalchemy.orm import Session

from database import get_db
from schemas import (
    RegisterRequest,
    LoginRequest,
    UserResponse,
    TokenResponse
)
from services import (
    get_user_by_email,
    create_user,
    verify_password,
    create_access_token,
    decode_access_token
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

security = HTTPBearer()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):
    existing_user = get_user_by_email(
        db,
        data.email
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    user = create_user(
        db,
        data.email,
        data.password
    )

    return user


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = get_user_by_email(
        db,
        data.email
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        data.password,
        user.password_hash # type: ignore
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(user)

    return {
        "access_token": token,
        "token_type": "bearer"
    }


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = decode_access_token(token)

        email = payload.get("sub")
        user_id = payload.get("user_id")

        if not email or not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        user = get_user_by_email(db, email)

        if not user:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )

        if user.id != user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return user

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token is invalid or expired"
        )


@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user=Depends(get_current_user)
):
    return current_user