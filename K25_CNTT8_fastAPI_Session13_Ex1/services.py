from sqlalchemy.orm import Session

from models import MenuItem
from schemas import MenuItemCreate, MenuItemUpdate


def create_menu_item(db: Session, data: MenuItemCreate):
    try:
        existing_item = (
            db.query(MenuItem)
            .filter(MenuItem.dish_code == data.dish_code)
            .first()
        )

        if existing_item:
            return None, "duplicate"

        new_item = MenuItem(**data.model_dump())

        db.add(new_item)
        db.commit()
        db.refresh(new_item)

        return new_item, None

    except Exception:
        db.rollback()
        raise


def get_all_menu_items(db: Session):
    return db.query(MenuItem).all()


def get_menu_item(db: Session, item_id: int):
    return (
        db.query(MenuItem)
        .filter(MenuItem.id == item_id)
        .first()
    )


def update_menu_item(
    db: Session,
    item_id: int,
    data: MenuItemUpdate
):
    try:
        item = get_menu_item(db, item_id)

        if not item:
            return None, "not_found"

        update_data = data.model_dump(exclude_unset=True)

        if "dish_code" in update_data:
            existing_item = (
                db.query(MenuItem)
                .filter(
                    MenuItem.dish_code == update_data["dish_code"],
                    MenuItem.id != item_id
                )
                .first()
            )

            if existing_item:
                return None, "duplicate"

        for key, value in update_data.items():
            setattr(item, key, value)

        db.commit()
        db.refresh(item)

        return item, None

    except Exception:
        db.rollback()
        raise


def delete_menu_item(db: Session, item_id: int):
    try:
        item = get_menu_item(db, item_id)

        if not item:
            return False

        db.delete(item)
        db.commit()

        return True

    except Exception:
        db.rollback()
        raise