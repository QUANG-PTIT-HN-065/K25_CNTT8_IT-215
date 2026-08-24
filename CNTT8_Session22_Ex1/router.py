from fastapi import APIRouter, Depends, HTTPException, status

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from jose import JWTError

from sqlalchemy.orm import Session

from database import get_db

from schemas import RegisterRequest, LoginRequest, TokenResponse, ProfileResponse

from serviecs import (
    get_user_by_username,
    create_user,
    verify_password,
    create_access_token,
    decode_access_token,
)

router = APIRouter(prefix="/api", tags=["Authentication"])

security = HTTPBearer(auto_error=False)



@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, db: Session = Depends(get_db)):

    # Kiểm tra username tồn tại
    existing_user = get_user_by_username(db, data.username)

    if existing_user:

        raise HTTPException(status_code=400, detail="Username already exists")

    try:

        user = create_user(db=db, username=data.username, password=data.password)

        return {
            "message": "Register successfully",
            "data": {"id": user.id, "username": user.username},
        }

    except Exception:

        db.rollback()

        raise HTTPException(status_code=500, detail="Could not create user")


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):

    user = get_user_by_username(db, data.username)

    if not user:

        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not verify_password(data.password, user.hashed_password): # type: ignore

        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(user.username) # type: ignore

    return {"access_token": access_token, "token_type": "bearer"}



@router.get("/profile", response_model=ProfileResponse)
def profile(credentials: HTTPAuthorizationCredentials | None = Depends(security)):

    if credentials is None:

        raise HTTPException(status_code=401, detail="Authentication required")

    token = credentials.credentials

    try:
        payload = decode_access_token(token)

        username = payload.get("sub")

        if not username:

            raise HTTPException(status_code=401, detail="Invalid token")

        return {"message": f"Welcome, {username}!"}

    except JWTError:

        raise HTTPException(status_code=401, detail="Invalid or expired token")
