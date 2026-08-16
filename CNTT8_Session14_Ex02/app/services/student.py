from sqlalchemy.orm import Session

from app.models.student import Student
from app.schemas.student import StudentCreate


def get_students(db: Session):
    return db.query(Student).all()


def get_student(db: Session, student_id: int):
    return db.query(Student).filter(
        Student.id == student_id
    ).first()


def create_student(db: Session, student: StudentCreate):
    new_student = Student(
        full_name=student.full_name,
        email=student.email,
        major=student.major,
        gpa=student.gpa
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


def update_student(
    db: Session,
    student_id: int,
    student: StudentCreate
):
    existing_student = get_student(db, student_id)

    if not existing_student:
        return None

    existing_student.full_name = student.full_name # type: ignore
    existing_student.email = student.email # type: ignore
    existing_student.major = student.major # type: ignore
    existing_student.gpa = student.gpa # type: ignore

    db.commit()
    db.refresh(existing_student)

    return existing_student


def delete_student(db: Session, student_id: int):
    existing_student = get_student(db, student_id)

    if not existing_student:
        return None

    db.delete(existing_student)
    db.commit()

    return existing_student