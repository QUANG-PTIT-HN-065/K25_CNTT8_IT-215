from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from database import get_db
from schema import BoardingSlotCreate, BoardingSlotUpdate, BoardingSlotResponse
from sevice import (
    create_boarding_slot,
    get_all_boarding_slots,
    get_boarding_slot,
    update_boarding_slot,
    delete_boarding_slot,
)

router = APIRouter(prefix="/boarding-slots", tags=["Boarding Slots"])


def make_response(status_code: int, message: str, error, data, request: Request):
    return {
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": data,
        "path": request.url.path,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.post("")
def create_slot(
    data: BoardingSlotCreate, request: Request, db: Session = Depends(get_db)
):
    slot, error = create_boarding_slot(db, data)

    if error == "duplicate":
        raise HTTPException(status_code=400, detail="Slot number already exists")

    result = BoardingSlotResponse.model_validate(slot)

    return make_response(
        201, "Thêm khoang lưu trú thành công", None, result.model_dump(), request
    )


@router.get("")
def get_slots(request: Request, db: Session = Depends(get_db)):
    slots = get_all_boarding_slots(db)

    result = [BoardingSlotResponse.model_validate(slot).model_dump() for slot in slots]

    return make_response(200, "Lấy danh sách thành công", None, result, request)


@router.get("/{slot_id}")
def get_slot(slot_id: int, request: Request, db: Session = Depends(get_db)):
    slot = get_boarding_slot(db, slot_id)

    if not slot:
        raise HTTPException(status_code=404, detail="Boarding slot not found")

    result = BoardingSlotResponse.model_validate(slot)

    return make_response(
        200,
        "Lấy thông tin khoang lưu trú thành công",
        None,
        result.model_dump(),
        request,
    )


@router.put("/{slot_id}")
def update_slot(
    slot_id: int,
    data: BoardingSlotUpdate,
    request: Request,
    db: Session = Depends(get_db),
):
    slot, error = update_boarding_slot(db, slot_id, data)

    if error == "not_found":
        raise HTTPException(status_code=404, detail="Boarding slot not found")

    if error == "duplicate":
        raise HTTPException(status_code=400, detail="Slot number already exists")

    result = BoardingSlotResponse.model_validate(slot)

    return make_response(
        200, "Cập nhật khoang lưu trú thành công", None, result.model_dump(), request
    )


@router.delete("/{slot_id}")
def delete_slot(slot_id: int, request: Request, db: Session = Depends(get_db)):
    deleted = delete_boarding_slot(db, slot_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Boarding slot not found")

    return make_response(200, "Xóa khoang lưu trú thành công", None, None, request)
