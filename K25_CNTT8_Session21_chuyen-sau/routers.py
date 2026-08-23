from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from jose import JWTError
from sqlalchemy.orm import Session

from database import get_db

from schemas import (
    RegisterRequest,
    LoginRequest,
    UserResponse,
    LoginResponse
)

from services import (
    get_user_by_email,
    get_user_by_id,
    create_user,
    verify_password,
    create_access_token,
    decode_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
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
            detail="Email đã được đăng ký"
        )

    try:

        user = create_user(
            db=db,
            email=data.email,
            password=data.password,
            full_name=data.full_name
        )

        return user

    except Exception:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Không thể tạo tài khoản"
        )


@router.post(
    "/login",
    response_model=LoginResponse
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
            detail="Email hoặc mật khẩu không chính xác"
        )

    if not user.is_active: # type: ignore

        raise HTTPException(
            status_code=401,
            detail="Email hoặc mật khẩu không chính xác"
        )

    if not verify_password(
        data.password,
        user.password_hash # type: ignore
    ):

        raise HTTPException(
            status_code=401,
            detail="Email hoặc mật khẩu không chính xác"
        )

    # Tạo JWT
    access_token = create_access_token(user)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }



def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    try:
        payload = decode_access_token(token)

        user_id = payload.get("user_id")

        if user_id is None:

            raise HTTPException(
                status_code=401,
                detail="Token không hợp lệ"
            )

        user = get_user_by_id(
            db,
            int(user_id)
        )

        if not user:

            raise HTTPException(
                status_code=401,
                detail="Token không hợp lệ"
            )

        if not user.is_active: # type: ignore

            raise HTTPException(
                status_code=401,
                detail="Tài khoản đã bị khóa"
            )

        return user

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Token không hợp lệ hoặc đã hết hạn"
        )


@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: UserResponse = Depends(
        get_current_user
    )
):

    return current_user