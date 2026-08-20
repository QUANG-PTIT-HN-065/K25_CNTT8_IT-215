from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.students import CreateStudents
from app.services.students import *
router = APIRouter(prefix="/students", tags=["Students"])

@router.post("", status_code=status.HTTP_201_CREATED)
def create_item(data: CreateStudents, db: Session = Depends(get_db)):
    return create(db, data)

@router.get("",)
def get_all_items(db: Session = Depends(get_db)):
    return get_all(db)
