"""
Phần 1: Thiết kế kiến trúc Routing

Chủ đề: Quản lý sách

| Method | Endpoint            | Mục đích                |
| ------ | ------------------- | ----------------------- |
| GET    | `/books`            | Lấy danh sách sách      |
| GET    | `/books/detail`     | Xem chi tiết sách       |
| POST   | `/books`            | Thêm sách mới           |
| PUT    | `/books/update`     | Cập nhật thông tin sách |
| DELETE | `/books/delete`     | Xóa sách                |
| GET    | `/books/statistics` | Xem thống kê sách       |
| GET    | `/books/newest`     | Xem sách mới nhất       |
| GET    | `/books/popular`    | Xem sách phổ biến       |

"""

from fastapi import FastAPI

app = FastAPI()

books = [
    {
        "id": 1,
        "title": "Python Basic",
        "author": "Nguyen Van A",
        "price": 150000,
        "stock": 12,
    },
    {
        "id": 2,
        "title": "FastAPI Beginner",
        "author": "Tran Thi B",
        "price": 180000,
        "stock": 5,
    },
    {
        "id": 3,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "price": 250000,
        "stock": 8,
    },
]


@app.get("/books")
def get_books():
    return {"message": "Danh sách sách", "data": books}


@app.get("/books/detail")
def get_book_detail():
    return {"message": "Chi tiết sách đầu tiên", "data": books[0]}


@app.post("/books")
def create_book():
    return {
        "message": "Thêm sách thành công",
        "data": {
            "id": 4,
            "title": "Database Design",
            "author": "Le Van C",
            "price": 220000,
            "stock": 10,
        },
    }


@app.put("/books/update")
def update_book():
    updated_book = books[0].copy()
    updated_book["price"] = 160000

    return {"message": "Cập nhật sách thành công", "data": updated_book}


@app.delete("/books/delete")
def delete_book():
    return {"message": "Xóa sách thành công", "data": books[0]}


@app.get("/books/statistics")
def get_book_statistics():
    return {
        "message": "Thống kê sách",
        "total_books": len(books),
        "total_stock": sum(book["stock"] for book in books),
    }


@app.get("/books/newest")
def get_newest_books():
    return {"message": "Sách mới nhất", "data": books[-1]}


@app.get("/books/popular")
def get_popular_books():
    return {"message": "Sách phổ biến", "data": [books[0], books[2]]}
