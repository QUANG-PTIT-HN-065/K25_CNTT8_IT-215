"""
1. Input 
- Danh sách các quyển sách:

2. Output
- Trả về danh sách các sách có quantity <= 5.
- Nếu không có sách nào thỏa mãn:

3. Điều kiện xác định sách sắp hết hàng
Có trường quantity
quantity >= 0
quantity <= 5

Phần 2: Đề xuất 2 giải pháp
Giải pháp 1: Dùng vòng lặp for
low_stock = []

for book in books:
    if "quantity" not in book:
        continue
    if book["quantity"] < 0:
        continue
    if book["quantity"] <= 5:
        low_stock.append(book)
        
Ưu điểm
Dễ hiểu
Dễ xử lý các trường hợp đặc biệt

Giải pháp 2: Dùng List Comprehension
low_stock = [
    book
    for book in books
    if "quantity" in book
    and book["quantity"] >= 0
    and book["quantity"] <= 5
]
Ưu điểm
Ngắn gọn
Hiệu quả với danh sách đơn giản

| Tiêu chí             | Vòng lặp for | List comprehension |
| -------------------- | ------------ | ------------------ |
| Độ dễ hiểu           | Cao          | Trung bình         |
| Độ ngắn gọn          | Trung bình   |  Cao               |
| Dễ xử lý bẫy dữ liệu | Cao          | Khá                |
| Dễ bảo trì           | Cao          | Trung bình         |

Giải pháp chọn
Chọn cách 2:

Lý do:

Dễ đọc
Dễ thêm điều kiện kiểm tra
Thuận tiện khi xử lý nhiều trường hợp dữ liệu lỗi

Phần 4: Thiết kế các bước xử lý
- Khởi tạo FastAPI
- Khai báo danh sách books
- Tạo endpoint GET /books/low-stock
- Duyệt danh sách sách
- Nếu thiếu quantity -> bỏ qua
- Nếu quantity < 0 -> bỏ qua
- Nếu quantity <= 5 -> thêm vào danh sách kết quả
- Nếu danh sách kết quả rỗng -> trả về thông báo
- Nếu có kết quả -> trả về danh sách sách sắp hết hàng
"""

from fastapi import FastAPI

app = FastAPI()

books = [
    {"id": 1, "title": "Python Basic", "quantity": 12},
    {"id": 2, "title": "FastAPI Beginner", "quantity": 3},
    {"id": 3, "title": "Clean Code", "quantity": 5},
    {"id": 4, "title": "Database Design", "quantity": 0},
    {"id": 5, "title": "Web API Design", "quantity": 20}
]

@app.get("books/low-stock")
def get_low_stock_books():
    low_stock_books = [book for book in books if "quantity" in books and books["quantity"] <= 5 and books["quantity"] >= 0]
    
    if not low_stock_books:
        return {
            "message": "No low stock books found.",
            "data": []
        }
    else:
        return {
            "message": "Low stock books retrieved successfully.",
            "data": low_stock_books
        }