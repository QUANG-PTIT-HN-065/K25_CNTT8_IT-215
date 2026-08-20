from sqlalchemy.orm import Session
from app.models.students import Students
from app.schemas.students import CreateStudents


def get_all(db: Session):
    return db.query(Students).all()


def get_detail(db: Session, id: int):
    return db.query(Students).filter(Students.id == id).first()


def create(db: Session, data: CreateStudents):
    existing_student = db.query(Students).filter(Students.email == data.email or Students.student_code == data.student_code).first()

    if existing_student:
        return None  

    new_student = Students(**data.model_dump())

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student
