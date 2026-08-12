from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from database import get_db
from schemas import (
    MenuItemCreate,
    MenuItemUpdate,
    MenuItemResponse
)
from services import (
    create_menu_item,
    get_all_menu_items,
    get_menu_item,
    update_menu_item,
    delete_menu_item
)

router = APIRouter(
    prefix="/menu-items",
    tags=["Menu Items"]
)


def make_response(
    status_code: int,
    message: str,
    error,
    data,
    request: Request
):
    return {
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": data,
        "path": request.url.path,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@router.post("")
def create_item(
    data: MenuItemCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    item, error = create_menu_item(db, data)

    if error == "duplicate":
        raise HTTPException(
            status_code=400,
            detail="Dish code already exists"
        )

    result = MenuItemResponse.model_validate(item)

    return make_response(
        201,
        "Thêm món ăn thành công",
        None,
        result.model_dump(),
        request
    )


@router.get("")
def get_items(
    request: Request,
    db: Session = Depends(get_db)
):
    items = get_all_menu_items(db)

    result = [
        MenuItemResponse.model_validate(item).model_dump()
        for item in items
    ]

    return make_response(
        200,
        "Lấy danh sách món ăn thành công",
        None,
        result,
        request
    )


@router.get("/{item_id}")
def get_item(
    item_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    item = get_menu_item(db, item_id)

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Menu item not found"
        )

    result = MenuItemResponse.model_validate(item)

    return make_response(
        200,
        "Lấy thông tin món ăn thành công",
        None,
        result.model_dump(),
        request
    )


@router.put("/{item_id}")
def update_item(
    item_id: int,
    data: MenuItemUpdate,
    request: Request,
    db: Session = Depends(get_db)
):
    item, error = update_menu_item(
        db,
        item_id,
        data
    )

    if error == "not_found":
        raise HTTPException(
            status_code=404,
            detail="Menu item not found"
        )

    if error == "duplicate":
        raise HTTPException(
            status_code=400,
            detail="Dish code already exists"
        )

    result = MenuItemResponse.model_validate(item)

    return make_response(
        200,
        "Cập nhật món ăn thành công",
        None,
        result.model_dump(),
        request
    )


@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    deleted = delete_menu_item(db, item_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Menu item not found"
        )

    return make_response(
        200,
        "Xóa món ăn thành công",
        None,
        None,
        request
    )