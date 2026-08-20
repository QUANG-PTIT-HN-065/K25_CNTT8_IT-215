from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from database.database import get_db
import schema.schemas as schemas
import services.student_service as service

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("")
def get_students(
    response: Response,
    keyword: str = "",
    class_id: int = 0,
    db: Session = Depends(get_db)
):
    students, _, code = service.get_all(db, keyword, class_id)
    response.status_code = code
    
    items = [schemas.StudentResponse.model_validate(s).model_dump() for s in students]
    return {
        "message": "Lấy danh sách sinh viên thành công!",
        "data": items
    }

@router.get("/{student_id}")
def get_student_detail(student_id: int, response: Response, db: Session = Depends(get_db)):
    student, error_msg, code = service.get_by_id(db, student_id)
    response.status_code = code
    
    if error_msg != "":
        return {"message": error_msg}
        
    data = schemas.StudentResponse.model_validate(student).model_dump()
    return {
        "message": "Lấy chi tiết sinh viên thành công!",
        "data": data
    }

@router.post("")
def create_student(payload: schemas.StudentCreate, response: Response, db: Session = Depends(get_db)):
    student, error_msg, code = service.create(db, payload)
    response.status_code = code
    
    if error_msg != "":
        return {"message": error_msg}

    data = schemas.StudentResponse.model_validate(student).model_dump()
    return {
        "message": "Thêm mới sinh viên thành công!",
        "data": data
    }

@router.put("/{student_id}")
def update_student(student_id: int, payload: schemas.StudentUpdate, response: Response, db: Session = Depends(get_db)):
    student, error_msg, code = service.update(db, student_id, payload)
    response.status_code = code
    
    if error_msg != "":
        return {"message": error_msg}

    data = schemas.StudentResponse.model_validate(student).model_dump()
    return {
        "message": "Cập nhật sinh viên thành công!",
        "data": data
    }