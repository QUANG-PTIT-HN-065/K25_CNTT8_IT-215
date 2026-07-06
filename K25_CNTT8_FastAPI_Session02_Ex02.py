"""
Endpoint hiện tại là:
- GET /student

khi gọi GET /students lại bị lỗi 404 Not Found vì endpoint /student mà gọi  GET /students khồn tồn tại nên lỗi 404

return students[0] chỉ trả về 1 sinh viên đầu tiên trong danh sách nếu muốn trả về tất thì sai yêu cầu nghiệp vụ

API đúng cần sửa: GET /students
"""

from fastapi import FastAPI

app = FastAPI()

students = [
    {"id": 1, "name": "An"},
    {"id": 2, "name": "Binh"},
    {"id": 3, "name": "Cuong"},
]


@app.get("/students")
def get_students():
    return students
