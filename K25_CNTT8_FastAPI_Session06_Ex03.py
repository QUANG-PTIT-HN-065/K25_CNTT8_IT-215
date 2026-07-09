from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
rooms = [
    {
        "id": 1,
        "code": "R101",
        "name": "Room 101",
        "capacity": 30,
        "status": "AVAILABLE",
    },
    {
        "id": 2,
        "code": "R102",
        "name": "Room 102",
        "capacity": 20,
        "status": "AVAILABLE",
    },
    {
        "id": 3,
        "code": "R103",
        "name": "Room 103",
        "capacity": 40,
        "status": "MAINTENANCE",
    },
]

room_bookings = [
    {
        "id": 1,
        "room_id": 1,
        "class_name": "Python Basic",
        "student_count": 25,
        "date": "2026-07-01",
        "slot": "MORNING",
    }
]

class RoomModel(BaseModel):
    code: str
    name: str
    capacity: int
    status: str = "AVAILABLE"


class BookingModel(BaseModel):
    room_id: int
    class_name: str
    student_count: int
    date: str
    slot: str

@app.post("/rooms")
def create_room(room: RoomModel):
    if room.capacity <= 0:
        raise HTTPException(status_code=400, detail="Capacity must be > 0")
    if not room.name:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    if room.status not in ["AVAILABLE", "IN_USE", "MAINTENANCE"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    if any(r["code"] == room.code for r in rooms):
        raise HTTPException(status_code=400, detail="Room code already exists")

    new_room = {"id": len(rooms) + 1, **room.dict()}
    rooms.append(new_room)
    return new_room


@app.get("/rooms")
def get_rooms(
    keyword: Optional[str] = None,
    status: Optional[str] = None,
    min_capacity: Optional[int] = None,
):
    result = rooms
    if keyword:
        result = [
            r
            for r in result
            if keyword.lower() in r["code"].lower()
            or keyword.lower() in r["name"].lower()
        ]
    if status:
        result = [r for r in result if r["status"] == status]
    if min_capacity:
        result = [r for r in result if r["capacity"] >= min_capacity]
    return result


@app.get("/rooms/{room_id}")
def get_room(room_id: int):
    for r in rooms:
        if r["id"] == room_id:
            return r
    raise HTTPException(status_code=404, detail="Room not found")


@app.put("/rooms/{room_id}")
def update_room(room_id: int, room: RoomModel):
    for r in rooms:
        if r["id"] == room_id:
            if room.capacity <= 0:
                raise HTTPException(status_code=400, detail="Capacity must be > 0")
            r.update(room.dict())
            return r
    raise HTTPException(status_code=404, detail="Room not found")


@app.delete("/rooms/{room_id}")
def delete_room(room_id: int):
    for i, r in enumerate(rooms):
        if r["id"] == room_id:
            rooms.pop(i)
            return {"detail": "Deleted successfully"}
    raise HTTPException(status_code=404, detail="Room not found")


@app.post("/room-bookings")
def create_booking(booking: BookingModel):
    target_room = next((r for r in rooms if r["id"] == booking.room_id), None)
    if not target_room:
        raise HTTPException(status_code=404, detail="Room not found")

    if target_room["status"] != "AVAILABLE":
        raise HTTPException(status_code=400, detail="Room is not AVAILABLE")
    if booking.student_count <= 0:
        raise HTTPException(status_code=400, detail="Student count must be > 0")
    if booking.student_count > target_room["capacity"]:
        raise HTTPException(
            status_code=400, detail="Student count exceeds room capacity"
        )
    if booking.slot not in ["MORNING", "AFTERNOON", "EVENING"]:
        raise HTTPException(status_code=400, detail="Invalid slot")

    for b in room_bookings:
        if (
            b["room_id"] == booking.room_id
            and b["date"] == booking.date
            and b["slot"] == booking.slot
        ):
            raise HTTPException(
                status_code=400, detail="Room is already booked for this date and slot"
            )

    new_booking = {"id": len(room_bookings) + 1, **booking.dict()}
    room_bookings.append(new_booking)
    return new_booking


@app.get("/room-bookings")
def get_bookings():
    return room_bookings
