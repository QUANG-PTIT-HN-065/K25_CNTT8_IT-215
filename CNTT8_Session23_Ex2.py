"""
PHẦN 1. PHÁT HIỆN LỖ HỔNG
1. Lỗi phân quyền Admin trong require_admin()

if current_user["role"] == "admin" or current_user["is_active"]:
    return current_user

Nguyên nhân: Biểu thức logic dùng toán tử or. Bất kỳ tài khoản nào đang hoạt động (is_active == True) đều thỏa mãn điều kiện và vượt qua lớp kiểm tra, dù role chỉ là "user".

2. Lỗi Middleware chặn API công khai /health và Request preflight OPTIONS
@app.middleware("http")
async def authentication_middleware(request, call_next):
    if "authorization" not in request.headers:
        return JSONResponse(status_code=401, content={"detail": "Authorization header is required"})

Nguyên nhân: Middleware này kiểm tra header Authorization trên tất cả các request đi vào hệ thống mà không ngoại trừ:

Path công khai như /health

Phương thức OPTIONS (CORS preflight request do trình duyệt tự động gửi trước khi gọi API thực sự, không bao giờ chứa header Authorization)

3. Lỗi cấu hình CORS quá rộng rãi

allow_origins=["*"]

Nguyên nhân: Việc đặt allow_origins=["*"] cho phép bất kỳ domain/website lạ nào cũng có thể truy xuất API và đọc dữ liệu, vi phạm chính sách bảo mật CORS và yêu cầu nghiệp vụ.

4. Lỗi thiếu kiểm tra trạng thái tài khoản bị khóa (is_active) trong get_current_user
Hàm get_current_user() chỉ lấy user từ dict TOKENS mà không kiểm tra trường is_active


"""

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

TOKENS = {
    "admin-token": {
        "username": "admin01",
        "role": "admin",
        "is_active": True,
    },
    "user-token": {
        "username": "student01",
        "role": "user",
        "is_active": True,
    },
    "locked-token": {
        "username": "locked01",
        "role": "user",
        "is_active": False,
    },
}


@app.middleware("http")
async def authentication_middleware(request: Request, call_next):
    if request.method == "OPTIONS" or request.url.path == "/health":
        response = await call_next(request)
        response.headers["X-System-Name"] = "Learning Management System"
        return response

    if "authorization" not in request.headers:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Authorization header is required"},
        )

    response = await call_next(request)
    response.headers["X-System-Name"] = "Learning Management System"
    return response


def get_current_user(token: str = Depends(oauth2_scheme)):
    user = TOKENS.get(token)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    if not user.get("is_active", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is locked",
        )

    return user


def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") == "admin" and current_user.get("is_active", False):
        return current_user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Admin permission required",
    )


@app.get("/health")
def health_check():
    return {"status": "UP"}


@app.get("/courses")
def get_courses(current_user: dict = Depends(get_current_user)):
    return {
        "items": [
            {"id": 1, "name": "FastAPI Basic"},
            {"id": 2, "name": "FastAPI Security"},
        ]
    }


@app.delete("/admin/courses/{course_id}")
def delete_course(
    course_id: int,
    current_user: dict = Depends(require_admin),
):
    return {
        "message": f"Course {course_id} has been deleted",
        "deleted_by": current_user["username"],
    }
