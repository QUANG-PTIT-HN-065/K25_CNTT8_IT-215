from fastapi import FastAPI
from K25_CNTT8_FastAPI_Session03_Ex01 import books

app = FastAPI()

@app.get("/books/available")
def get_available_books():
    available_books = [book for book in books if book["is_available"]== True]
    if not available_books:
        return {"messager: không có sách có thể mượn"}
    return {"messager": "sách có thể mượn",
            "data": available_books}
    
@app.get("/books/borrowed")
def get_available_books():
    unavailable_books = [book for book in books if book["is_available"]== False]
    if not unavailable_books:
        return {"messager: không có sách có thể mượn"}
    return {"messager": "Không có sách có thể mượn",
            "data": unavailable_books}
    