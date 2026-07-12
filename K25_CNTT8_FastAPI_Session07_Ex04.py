"""
Phần 1: Phân tích & Đề xuất đa giải pháp
1. Phân tích Input/Output
Input
API: GET /orders/{order_id}/payment
Phương thức: GET
Tham số đầu vào:
order_id (kiểu int): Mã đơn hàng cần tra cứu

Output thành công

Điều kiện:

order_id tồn tại trong hệ thống.

HTTP Status: 200 OK

Output thất bại

Trường hợp 1: Không tìm thấy đơn hàng

Điều kiện:

order_id không tồn tại : 404 Not Found

Trường hợp 2: Lỗi hệ thống

Điều kiện:

Xuất hiện lỗi ngoài ý muốn (ví dụ: lỗi logic, lỗi ép kiểu,...)

HTTP Status: 500 Internal Server Error

2. Đề xuất các giải pháp
Giải pháp 1: Lưu dữ liệu bằng List
Ý tưởng

Lưu toàn bộ đơn hàng trong một danh sách (List). Khi cần tìm kiếm, duyệt từng phần tử và so sánh id với order_id

Ưu điểm
- Dễ hiểu, dễ cài đặt.
- Phù hợp với dữ liệu nhỏ.
- Không cần thay đổi cấu trúc dữ liệu.
Nhược điểm
- Phải duyệt lần lượt từng phần tử (Linear Search).
- Độ phức tạp tìm kiếm là O(n).
- Khi số lượng đơn hàng tăng lên hàng chục nghìn hoặc hàng triệu bản ghi, tốc độ tra cứu sẽ chậm


Giải pháp 2: Lưu dữ liệu bằng Dict
Ý tưởng

Chuyển id của đơn hàng thành Key trong Dict để có thể truy cập trực tiếp

Ưu điểm
- Tra cứu trực tiếp theo khóa (Key).
- Tốc độ tìm kiếm trung bình O(1).
- Phù hợp với hệ thống có dữ liệu lớn.
- Giảm độ trễ khi API được gọi nhiều lần.
Nhược điểm
- Tiêu tốn bộ nhớ nhiều hơn do sử dụng cấu trúc bảng băm (Hash Table).
- Cần chuyển đổi dữ liệu từ List sang Dict nếu dữ liệu ban đầu ở dạng List.

"""

from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Any
from pydantic import BaseModel

app = FastAPI()

orders = {
    1: {"id": 1, "code": "SP001", "payment_status": "PAID", "method": "BANK_TRANSFER"},
    2: {"id": 2, "code": "SP002", "payment_status": "UNPAID", "method": "NONE"},
}

def create_response(
    request: Request,
    status_code: int,
    message: str,
    data: Any = None,
    error: str | None = None,
):
    return JSONResponse(
        status_code=status_code,
        content={
            "statusCode": status_code,
            "message": message,
            "data": data,
            "error": error,
            "timestamp": datetime.now().isoformat(),
            "path": request.url.path,
        },
    )


@app.get("/orders/{order_id}/payment")
def get_payment(order_id: int, request: Request):

    if order_id not in orders:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    order = orders[order_id]

    return create_response(
        request=request,
        status_code=status.HTTP_200_OK,
        message="Lấy dữ liệu thành công",
        data={
            "order_id": order["id"],
            "payment_status": order["payment_status"],
            "method": order["method"],
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return create_response(
        request=request,
        status_code=exc.status_code,
        message="Request failed",
        error=exc.detail,
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return create_response(
        request=request,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="Internal Server Error",
        error="Please try again later.",
    )
