"""
Phần 1: Luồng dữ liệu
Luồng xử lý Request/Response

1: Client gửi yêu cầu:
    - DELETE /orders/{order_id}
2: FastAPI nhận request và kiểm tra dữ liệu đầu vào.
    - Nếu order_id sai kiểu dữ liệu (ví dụ: "abc"), FastAPI phát sinh RequestValidationError.
3: API xử lý nghiệp vụ:
    - Kiểm tra đơn hàng có tồn tại hay không.
    - Nếu không tồn tại → phát sinh HTTPException(404).
    - Nếu đơn hàng đã ở trạng thái DELIVERED → phát sinh HTTPException(400).
    - Nếu đơn hàng ở trạng thái PENDING → cập nhật status = "CANCELLED" và trả về kết quả thành công.
4: Global Exception Handler (@app.exception_handler) sẽ bắt tất cả các loại lỗi:
    - RequestValidationError
    - HTTPException
    - Exception (lỗi hệ thống)
5: Global Handler chuyển mọi phản hồi (thành công hoặc lỗi) về một cấu trúc JSON thống nhất gồm 6 trường:
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from datetime import datetime

app = FastAPI()

orders_db = [
    {"id": 1, "code": "SP001", "status": "PENDING"},
    {"id": 2, "code": "SP002", "status": "DELIVERED"},
]



def api_response(status_code: int, message: str, data, error, request: Request):
    return JSONResponse(
        status_code=status_code,
        content={
            "statusCode": status_code,
            "message": message,
            "data": data,
            "error": error,
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return api_response(422, "Validation Error", None, exc.errors(), request)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return api_response(exc.status_code, exc.detail, None, exc.detail, request)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return api_response(500, "Internal Server Error", None, "Unexpected error", request)

@app.delete("/orders/{order_id}")
async def cancel_order(order_id: int, request: Request):

    for order in orders_db:

        if order["id"] == order_id:

            if order["status"] == "DELIVERED":
                raise HTTPException(
                    status_code=400, detail="Delivered order cannot be cancelled."
                )

            if order["status"] == "CANCELLED":
                raise HTTPException(
                    status_code=400, detail="Order has already been cancelled."
                )

            order["status"] = "CANCELLED"

            return api_response(
                200, "Order cancelled successfully.", order, None, request
            )

    raise HTTPException(status_code=404, detail="Order not found.")
