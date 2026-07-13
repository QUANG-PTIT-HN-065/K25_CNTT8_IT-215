from enum import Enum
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

desks = [
    {
        "id": 1,
        "desk_number": "DSK-A-01",
        "zone": "Zone A - Quiet Space",
        "price_per_day": 150000.0,
        "status": "AVAILABLE",
    },
    {
        "id": 2,
        "desk_number": "DSK-B-02",
        "zone": "Zone B - Creative",
        "price_per_day": 200000.0,
        "status": "AVAILABLE",
    },
    {
        "id": 3,
        "desk_number": "DSK-C-03",
        "zone": "Zone C - Panoramic",
        "price_per_day": 250000.0,
        "status": "MAINTENANCE",
    },
]

bookings = [
    {
        "id": 1,
        "desk_id": 1,
        "customer_name": "Nguyen Van A",
        "booking_date": "2026-07-01",
        "payment_status": "PAID",
    }
]


class DeskStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    MAINTENANCE = "MAINTENANCE"


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    CANCELLED = "CANCELLED"


class DeskCreate(BaseModel):
    desk_number: str
    zone: str
    price_per_day: float = Field(gt=0)
    status: DeskStatus


class BookingCreate(BaseModel):
    desk_id: int
    customer_name: str
    booking_date: str
    payment_status: PaymentStatus


@app.post("/desks", status_code=201)
def create_desk(data: DeskCreate):
    if any(d["desk_number"] == data.desk_number for d in desks):
        raise HTTPException(status_code=400, detail="Desk number already exists")

    new_desk = {"id": max([d["id"] for d in desks], default=0) + 1, **data.model_dump()}
    desks.append(new_desk)
    return new_desk


@app.get("/desks")
def get_desks(
    zone_keyword: Optional[str] = None,
    max_price: Optional[float] = None,
    status: Optional[DeskStatus] = None,
):
    result = desks

    if zone_keyword:
        result = [d for d in result if zone_keyword.lower() in d["zone"].lower()]

    if max_price is not None:
        result = [d for d in result if d["price_per_day"] <= max_price]

    if status:
        result = [d for d in result if d["status"] == status]

    return result


@app.get("/desks/{desk_id}")
def get_desk(desk_id: int):
    for desk in desks:
        if desk["id"] == desk_id:
            return desk
    raise HTTPException(status_code=404, detail="Desk not found")


@app.put("/desks/{desk_id}")
def update_desk(desk_id: int, data: DeskCreate):
    for desk in desks:
        if desk["id"] != desk_id and desk["desk_number"] == data.desk_number:
            raise HTTPException(status_code=400, detail="Desk number already exists")

    for i, desk in enumerate(desks):
        if desk["id"] == desk_id:
            desks[i] = {"id": desk_id, **data.model_dump()}
            return desks[i]

    raise HTTPException(status_code=404, detail="Desk not found")


@app.delete("/desks/{desk_id}", status_code=204)
def delete_desk(desk_id: int):
    for i, desk in enumerate(desks):
        if desk["id"] == desk_id:
            desks.pop(i)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail="Desk not found")


@app.post("/bookings", status_code=201)
def create_booking(data: BookingCreate):
    desk = next((d for d in desks if d["id"] == data.desk_id), None)

    if not desk:
        raise HTTPException(status_code=404, detail="Desk not found")

    if desk["status"] != "AVAILABLE":
        raise HTTPException(status_code=400, detail="Desk is not available")

    if any(
        b["desk_id"] == data.desk_id and b["booking_date"] == data.booking_date
        for b in bookings
    ):
        raise HTTPException(status_code=400, detail="Desk already booked for this date")

    new_booking = {
        "id": max([b["id"] for b in bookings], default=0) + 1,
        **data.model_dump(),
    }

    bookings.append(new_booking)
    return new_booking


@app.get("/bookings")
def get_bookings():
    return bookings
