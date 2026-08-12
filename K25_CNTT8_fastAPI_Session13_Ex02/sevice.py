from sqlalchemy.orm import Session

from models import BoardingSlot
from schema import BoardingSlotCreate, BoardingSlotUpdate


def create_boarding_slot(
    db: Session,
    data: BoardingSlotCreate
):
    try:
        existing_slot = (
            db.query(BoardingSlot)
            .filter(
                BoardingSlot.slot_number == data.slot_number
            )
            .first()
        )

        if existing_slot:
            return None, "duplicate"

        new_slot = BoardingSlot(
            **data.model_dump()
        )

        db.add(new_slot)
        db.commit()
        db.refresh(new_slot)

        return new_slot, None

    except Exception:
        db.rollback()
        raise


def get_all_boarding_slots(db: Session):
    return db.query(BoardingSlot).all()


def get_boarding_slot(
    db: Session,
    slot_id: int
):
    return (
        db.query(BoardingSlot)
        .filter(BoardingSlot.id == slot_id)
        .first()
    )


def update_boarding_slot(
    db: Session,
    slot_id: int,
    data: BoardingSlotUpdate
):
    try:
        slot = get_boarding_slot(db, slot_id)

        if not slot:
            return None, "not_found"

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "slot_number" in update_data:
            existing_slot = (
                db.query(BoardingSlot)
                .filter(
                    BoardingSlot.slot_number
                    == update_data["slot_number"],
                    BoardingSlot.id != slot_id
                )
                .first()
            )

            if existing_slot:
                return None, "duplicate"

        for key, value in update_data.items():
            setattr(slot, key, value)

        db.commit()
        db.refresh(slot)

        return slot, None

    except Exception:
        db.rollback()
        raise


def delete_boarding_slot(
    db: Session,
    slot_id: int
):
    try:
        slot = get_boarding_slot(db, slot_id)

        if not slot:
            return False

        db.delete(slot)
        db.commit()

        return True

    except Exception:
        db.rollback()
        raise