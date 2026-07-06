"""
Phần 1: Báo cáo phân tích

1. Input
- Danh sách sinh viên

2. Output
- API trả về danh sách sinh viên có status = "active".
- Nếu không có sinh viên đang học, trả về = []

3. điều kiện 

- Active students:status = "active"

4. Các bước xử lý API GET /students/active
- Nhận yêu cầu GET /students/active.
- Lọc các sinh viên có status == "active".
- Nếu danh sách rỗng, trả về thông báo không có sinh viên đang học.
- Nếu có dữ liệu, trả về thông báo và danh sách sinh viên đang học.

"""

from fastapi import FastAPI

app = FastAPI()

students = [
    {"id": 1, "name": "An", "status": "active"},
    {"id": 2, "name": "Binh", "status": "inactive"},
    {"id": 3, "name": "Cuong", "status": "active"},
    {"id": 4, "name": "Dung", "status": "pending"}
]

@app.get("/students/active")
def get_active_students():
    active_students = [student for student in students if student["status"] == "active"]
    
    if not active_students:
        return {
            "message": "No active students found.",
            "data":[]
            }
    else:
        return {
            "message": "Active students retrieved successfully.",
            "data": active_students
        }
        