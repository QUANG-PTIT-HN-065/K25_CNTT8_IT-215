from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, field_validator
from typing import Any
from datetime import datetime, timezone

app = FastAPI()

tickets_db = {
    1: {
        "id": 1,
        "movie_name": "Doctor Strange 3",
        "room_code": "IMAX-01",
        "quantity": 2,
        "status": "confirmed",
    },
    2: {
        "id": 2,
        "movie_name": "Avatar 3",
        "room_code": "PREMIUM-02",
        "quantity": 1,
        "status": "confirmed",
    },
}


class Tickets(BaseModel):
    movie_name: str = Field(..., min_length=1)
    room_code: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=1, le=10)
    status : str = Field(default="confirmed")

    @field_validator("movie_name", "room_code")
    @classmethod
    def validate_not_blank(cls, value):
        if not value.strip():
            raise ValueError("Không được để trống.")
        return value


def unified_response(
    request: Request,
    status_code: int,
    message: str,
    data: Any = None,
    error: Any = None,
) -> JSONResponse:

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    content = {
        "statusCode": status_code,
        "message": message,
        "data": data,
        "error": error,
        "timestamp": timestamp,
        "path": request.url.path,
    }

    return JSONResponse(status_code=status_code, content=content)



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return unified_response(
        request=request,
        status_code=422,
        message="Dữ liệu không hợp lệ!",
        data=None,
        error=exc.errors(),
    )


@app.get("/tickets")
def get_tickets(request: Request):
    return unified_response(
        request,
        200,
        "Lấy danh sách vé thành công!",
        data=list(tickets_db.values()),
    )


@app.post("/tickets")
def add_tickets(request: Request, ticket: Tickets):
    for item in tickets_db.values():
        if (
            item["movie_name"].lower() == ticket.movie_name.lower()
            and item["room_code"].lower() == ticket.room_code.lower()
        ):
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Lỗi: Vé xem phim tại phòng chiếu này đã được đặt!",
                    "error": "ERR-CINE-01: Ticket conflict for movie and room combination.",
                },
            )

    new_id = max(tickets_db.keys(), default=0) + 1

    new_ticket = {
        "id": new_id,
        **ticket.model_dump()
    }

    tickets_db[new_id] = new_ticket

    return unified_response(
        request,
        201,
        "Đặt vé thành công!",
        data=new_ticket,
    )


@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int, request: Request):

    if ticket_id not in tickets_db:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Lỗi: Không tìm thấy mã vé yêu cầu!",
                "error": "ERR-CINE-02: Ticket ID does not exist.",
            },
        )

    del tickets_db[ticket_id]

    return unified_response(
        request,
        200,
        "Hủy vé thành công!",
        data=None,
    )
