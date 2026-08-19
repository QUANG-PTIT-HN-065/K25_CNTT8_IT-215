from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import *
from schemas import *
from database import get_db

app = FastAPI(title="Classroom Student API")

# CREATE CLASSROOM


@app.post("/classrooms")
def create_classroom(data: ClassroomCreate, db: Session = Depends(get_db)):
    classroom = Classroom(
        class_name=data.class_name, status=data.status, capacity=data.capacity
    )

    db.add(classroom)
    db.commit()
    db.refresh(classroom)

    return classroom

# CREATE STUDENT
@app.post("/students", response_model=StudentResponse)
def create_student(data: StudentCreate, db: Session = Depends(get_db)):

    classroom = db.query(Classroom).filter(Classroom.id == data.classroom_id).first()
    if classroom is None:
        raise HTTPException(status_code=404, detail="Lớp học không tồn tại")

    if classroom.status != "OPEN": # type: ignore
        raise HTTPException(status_code=400, detail="Lớp học đã đóng")

    current_count = (
        db.query(Student).filter(Student.classroom_id == data.classroom_id).count()
    )

    if current_count >= classroom.capacity: # type: ignore
        raise HTTPException(status_code=400, detail="Lớp học đã đủ sinh viên")

    student = Student(
        student_code=data.student_code,
        full_name=data.full_name,
        classroom_id=data.classroom_id,
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    return student


# GET CLASSROOM DETAIL

@app.get("/classrooms/{classroom_id}", response_model=ClassroomDetailResponse)
def get_classroom_detail(classroom_id: int, db: Session = Depends(get_db)):
    classroom = db.query(Classroom).filter(Classroom.id == classroom_id).first()

    if classroom is None:
        raise HTTPException(status_code=404, detail="Lớp học không tồn tại")

    students = (
        db.query(Student)
        .filter(Student.classroom_id == classroom_id)
        .order_by(Student.id)
        .all()
    )

    return {
        "id": classroom.id,
        "class_name": classroom.class_name,
        "status": classroom.status,
        "capacity": classroom.capacity,
        "students": students,
    }


# TRANSFER STUDENT
@app.put("/students/{student_id}/transfer", response_model=StudentResponse)
def transfer_student(
    student_id: int, data: TransferClassRequest, db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Sinh viên không tồn tại")
    target_classroom = (
        db.query(Classroom).filter(Classroom.id == data.new_classroom_id).first()
    )
    if target_classroom is None:
        raise HTTPException(status_code=404, detail="Lớp học đích không tồn tại")

    if target_classroom.status == "CLOSED":  # type: ignore
        raise HTTPException(status_code=400, detail="Không thể chuyển vào lớp đã đóng")

    current_count = (
        db.query(Student).filter(Student.classroom_id == data.new_classroom_id).count()
    )

    if current_count >= target_classroom.capacity:  # type: ignore
        raise HTTPException(status_code=400, detail="Lớp học đã đủ sinh viên")

    student.classroom_id = data.new_classroom_id  # type: ignore

    db.commit()
    db.refresh(student)

    return student
