"""
Phần 1: Phân tích & Đề xuất giải pháp
1. Phân tích Input/Output

Input:

product_id trên URL.
Body gồm:
code
name
price
stock

Output thành công:

HTTP 200.
Trả về thông tin sản phẩm sau khi cập nhật.

Output thất bại:

404 Product not found nếu không tìm thấy product_id.
400 Product code already exists nếu code bị trùng.
422 Unprocessable Entity nếu dữ liệu không hợp lệ (ví dụ price <= 0, stock < 0, name rỗng).
2. Hai giải pháp
Giải pháp 1: Duyệt list
Duyệt danh sách để tìm sản phẩm theo id.
Tiếp tục duyệt để kiểm tra code có bị trùng hay không.
Nếu hợp lệ thì cập nhật dữ liệu.

Ưu điểm: Đơn giản, dễ hiểu.

Nhược điểm: Tìm kiếm chậm khi dữ liệu lớn (O(n)).

Giải pháp 2: Dùng dict
Lưu dữ liệu với id làm key.
Tìm sản phẩm bằng products.get(product_id).
Kiểm tra trùng code.
Cập nhật dữ liệu.

Ưu điểm: Tìm kiếm nhanh (O(1)).

Nhược điểm: Tốn bộ nhớ hơn và vẫn phải duyệt để kiểm tra code.

| Tiêu chí         | Duyệt list    | Dùng dict      |
| ---------------- | ------------- | -------------- |
| Tốc độ tìm kiếm  | Chậm (`O(n)`) | Nhanh (`O(1)`) |
| Bộ nhớ           | Ít            | Nhiều hơn      |
| Dễ hiểu          | Dễ            | Dễ             |
| Dễ bảo trì       | Khá           | Tốt            |
| Bối cảnh phù hợp | Dữ liệu nhỏ   | Dữ liệu lớn    |

Kết luận

Nên chọn dict vì tìm kiếm theo id nhanh hơn, giúp API hoạt động hiệu quả hơn khi số lượng sản phẩm lớn. Với dữ liệu nhỏ hoặc bài tập cơ bản, list vẫn là lựa chọn phù hợp vì đơn giản và dễ triển khai.

"""

from fastapi import FastAPI,HTTPException , status
from pydantic import BaseModel, Field

app = FastAPI()

products = {
    1: {"code": "SP001", "name": "Keyboard", "price": 500000, "stock": 10},
    2: {"code": "SP002", "name": "Mouse", "price": 300000, "stock": 5},
}


class Products(BaseModel):
    code : str = Field(...)
    name : str = Field(..., min_length=3)
    price: float = Field(...,gt=0)
    stock : int = Field(...,ge= 0)
    
@app.put("/products/{product_id}")
def Update_product(product_id: int, product: Products):
    
    current_product = products.get(product_id)
    
    if not current_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "Product not found"
        )
        
    if not product.name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product name cannot be empty"
        )
        
    for id, p in products.items():
        if id != product_id and p["code"] == product.code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= "Product code already exists"
            )
            
    products[product_id] = {
        "code": product.code,
        "name": product.name,
        "price": product.price,
        "stock": product.stock,
    }

    return {
        "message": "Product updated successfully",
        "data": products[product_id]
    }