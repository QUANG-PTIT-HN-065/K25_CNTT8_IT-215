"""
PHẦN 1. PHÁT HIỆN LỖ HỔNG
1. Vị trí dòng code gây lỗi chính

Khối code trong hàm get_current_user

try:

    payload = jwt.get_unverified_claims(token)
except Exception:

Đọc dữ liệu token nhưng không kiểm tra chữ ký và thời hạn

lý do get_unverified_claims() không an toàn

- Không kiểm tra chữ ký (Signature): Hàm get_unverified_claims() chỉ đơn thuần thực hiện base64 decode chuỗi JWT để đọc dữ liệu JSON bên trong mà không đối chiếu với SECRET_KEY
  Hacker có thể tự chỉnh sửa payload (chẳng hạn đổi "sub": "alice" thành "sub": "admin") mà không cần biết secret key, hệ thống vẫn chấp nhận

- Không kiểm tra thời gian hết hạn (exp claim): Do không decode và verify đúng quy chuẩn, trường exp bị bỏ qua hoàn toàn. Dù token đã hết hạn 1 ngày hay 1 năm, hàm vẫn coi là hợp lệ

- Bỏ qua kiểm tra trạng thái is_active: Code chưa có logic check xem tài khoản user["is_active"] có bằng True hay không

Mô tả các Test Case:

1: Token hợp lệ
- Token sinh ra từ /issue-token/alice (expired=False). 200 OK (Trả về thông tin Alice)
- Kết quả mong đợi: 200 OK
=> Luồng xử lý bình thường.

2: Token hết hạn
- Token sinh ra từ /issue-token/alice?expired=True. 200 OK (Vẫn trả về thông tin Alice)
- Kết quả mong đợi: 401 Unauthorized
=> jwt.get_unverified_claims() bỏ qua việc validate trường exp

3: Tài khoản bị khóa
- Token sinh ra từ /issue-token/bob (is_active=False). 200 OK (Trả về thông tin Bob)
- Kết quả mong đợi: 403 Forbidden
=> Trong code hoàn toàn thiếu câu lệnh kiểm tra user["is_active"]
"""

from datetime import datetime, timedelta, timezone
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

app = FastAPI()

SECRET_KEY = "training-secret-key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

USERS = {
    "alice": {
        "username": "alice",
        "full_name": "Alice Nguyen",
        "role": "user",
        "is_active": True,
    },
    "bob": {
        "username": "bob",
        "full_name": "Bob Tran",
        "role": "user",
        "is_active": False,
    },
}


@app.get("/issue-token/{username}")
def issue_token(username: str, expired: bool = False):
    if username not in USERS:
        raise HTTPException(status_code=404, detail="User not found")

    expires_at = datetime.now(timezone.utc) + timedelta(minutes=-5 if expired else 30)

    token = jwt.encode(
        {
            "sub": username,
            "exp": expires_at,
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username: str = payload.get("sub")  # type: ignore
        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = USERS.get(username)
    if user is None:
        raise credentials_exception

    if not user.get("is_active", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user account",
        )

    return user


@app.get("/users/me")
def read_current_user(current_user: dict = Depends(get_current_user)):
    return current_user
