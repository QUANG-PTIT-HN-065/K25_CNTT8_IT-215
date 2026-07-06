"""
1) Phân tích lỗi
Trace luồng xử lý /getStudents:
Client gửi GET /getStudents.
FastAPI gọi get_students().
Hàm trả về chuỗi "Danh sach sinh vien: ['An', 'Binh', 'Cuong']".
Client nhận string, không phải JSON array.

- không nên trả về string
  + API REST nên trả về JSON để client dễ xử lý.
  + String khó parse, không đúng chuẩn dữ liệu API.

- Lỗi thiết kế REST endpoint:
  + Không dùng động từ (getStudents).
  + Nên dùng danh từ số nhiều: /students.
"""

from fastapi import FastAPI

app = FastAPI()

students = ["An", "Binh", "Cuong"]

@app.get("/students")
def get_students():
    return students