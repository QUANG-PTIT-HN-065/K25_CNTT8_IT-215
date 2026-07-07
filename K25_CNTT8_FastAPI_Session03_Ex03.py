from fastapi import FastAPI
from K25_CNTT8_FastAPI_Session03_Ex01 import books

app = FastAPI()


@app.get("/books/statistics")
def get_statistics_books():
    available_count = sum(book["is_available"] for book in books)
    unavailable_count = len(books) - available_count

    return {
        "total_books": len(books),
        "available_books": available_count,
        "borrowed_books": unavailable_count,
    }

@app.get("/books/categories")
def get_categories_books():
    categories = []

    for book in books:
        if book["category"] not in categories:
            categories.append(book["category"])

    return {
        "categories": categories
    }
    
@app.get("/books/latest")
def get_latest_book():
    if not books:
        return {
            "message": "No books available"
        }

    latest_book = max(books, key=lambda book:book["year"])

    return latest_book