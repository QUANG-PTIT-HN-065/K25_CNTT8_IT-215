"""
Phần 1: Phân tích & Đề xuất đa giải pháp
1. Phân tích Input / Output
Input:

- POST /students

Output thành công

Status Code

201 Created

Response

{
    "message": "Thêm học viên thành công",
    "student": {
        "full_name": "Nguyen Van A",
        "email": "vana@gmail.com",
        "age": 20,
        "course": "python",
        "phone": "0987654321"
    }
}

Output thất bại

Thiếu trường bắt buộc

{
    "detail": [
        {
            "loc": [
                "body",
                "email"
            ],
            "msg": "Field required",
            "type": "missing"
        }
    ]
}

Email sai định dạng

{
    "detail": [
        {
            "msg": "value is not a valid email address"
        }
    ]
}

Email đã tồn tại

{
    "detail": "Email đã tồn tại trong hệ thống"
}

2. Đề xuất ít nhất 2 giải pháp
Giải pháp 1: Validate thủ công trong API
    Nhận dữ liệu dạng dict
    Dùng if để kiểm tra từng trường
    Kiểm tra email bằng Regex
    Kiểm tra email trùng bằng vòng lặp

Ưu điểm
- Dễ hiểu
- Không cần dùng Pydantic

Nhược điểm

- Viết nhiều code
- Khó bảo trì
- Dễ thiếu validate


Giải pháp 2: Sử dụng Pydantic Model (Khuyến nghị)
    Tạo StudentCreate bằng BaseModel
Dùng EmailStr để kiểm tra email
Dùng Field để kiểm tra độ dài
FastAPI tự validate request
Chỉ cần kiểm tra email trùng trong API

Ưu điểm

- Code ngắn
- Dễ đọc
- Chuẩn FastAPI
- Tự động sinh tài liệu Swagger

Nhược điểm
- Cần học Pydantic


Phần 2: So sánh & Lựa chọn
1. Bảng so sánh

| Tiêu chí         | Giải pháp 1 (Validate thủ công) | Giải pháp 2 (Pydantic) |
| ---------------- | ------------------------------- | ---------------------- |
| Độ dễ hiểu       | Trung bình                      | Dễ                     |
| Số lượng code    | Nhiều                           | Ít                     |
| Kiểm soát lỗi    | Thủ công                        | Tự động                |
| Cấu trúc dữ liệu | Không rõ ràng                   | Rõ ràng                |

2. Lựa chọn giải pháp

Em lựa chọn Giải pháp 2 (Pydantic Model).

Lý do:

Đúng chuẩn FastAPI.
Giảm số lượng code cần viết.
FastAPI tự động kiểm tra dữ liệu đầu vào.
Thông báo lỗi rõ ràng.
Dễ mở rộng khi hệ thống có thêm nhiều trường dữ liệu.
Dễ bảo trì hơn so với việc tự viết các câu lệnh if.
"""



from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(title="Student API")

students = []


class StudentsCreate(BaseModel):
    full_name:str = Field(...,min_length=3)
    email:EmailStr
    age:int = Field(..., ge=1, le=100) 
    court:str = Field(..., min_length=2)
    phone:str = Field(..., min_length=10, max_length=10)
    
@app.post("/student",status_code= status.HTTP_201_CREATED)
def create_student(Student: StudentsCreate):
    for s in students:
        if s["email"] == Student.email:
            raise HTTPException(
                status_code=400,
                detail="Email đã tồn tại trong hệ thống"
            )
    
    new_student =  Student.model_dump()
    students.append(new_student)
    return {
        "message" : "Thêm học viên mới thành công",
        "student" : new_student
    }
    
