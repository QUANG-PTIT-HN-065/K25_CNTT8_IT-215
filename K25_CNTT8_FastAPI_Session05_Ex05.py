"""
1. Luồng xử lý

Khi client gửi request:

PATCH /products/2

Hệ thống xử lý theo các bước:

Client gửi request PATCH /products/{product_id}.
FastAPI nhận request và lấy product_id.
Tìm sản phẩm trong danh sách products.
Nếu không tìm thấy → trả về 404 Product not found.
Nếu tìm thấy nhưng is_active = False → trả về 400 Product already inactive.

Nếu sản phẩm đang hoạt động (is_active = True) → cập nhật:

is_active = False
Trả về thông báo thành công cùng thông tin sản phẩm sau khi cập nhật.
"""


from fastapi import FastAPI, HTTPException, status

app = FastAPI()

products = {
    1: {"code": "SP001", "name": "Keyboard", "price": 500000, "is_active": True},
    2: {"code": "SP002", "name": "Mouse", "price": 300000, "is_active": True},
    3: {"code": "SP003", "name": "Monitor", "price": 2500000, "is_active": False},
}

@app.patch("/products/{product_id}")
def update_status(product_id: int):

    current_product = products.get(product_id)

    if current_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    if not current_product["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product already inactive"
        )

    current_product["is_active"] = False

    return {
        "message": "Product deactivated successfully",
        "data": current_product
    }