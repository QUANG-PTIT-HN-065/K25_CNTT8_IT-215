from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.models import Student, Course, Enrollment
from app.schemas.schemas import EnrollmentCreate


def create_enrollment(
    db: Session,
    data: EnrollmentCreate
):
    # 1. Kiểm tra Student
    student = (
        db.query(Student)
        .filter(Student.id == data.student_id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # 2. Kiểm tra Course
    course = (
        db.query(Course)
        .filter(Course.id == data.course_id)
        .first()
    )

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    # 3. Kiểm tra Student ACTIVE
    if student.status != "ACTIVE": # type: ignore
        raise HTTPException(
            status_code=400,
            detail="Student is inactive"
        )

    # 4. Kiểm tra Course OPEN
    if course.status != "OPEN": # type: ignore
        raise HTTPException(
            status_code=400,
            detail="Course is closed"
        )

    # 5. Kiểm tra đăng ký trùng
    existing_enrollment = (
        db.query(Enrollment)
        .filter(
            Enrollment.student_id == data.student_id,
            Enrollment.course_id == data.course_id
        )
        .first()
    )

    if existing_enrollment:
        raise HTTPException(
            status_code=400,
            detail="Student already enrolled in this course"
        )

    # 6. Đếm số lượng sinh viên đã đăng ký
    current_count = (
        db.query(func.count(Enrollment.id))
        .filter(
            Enrollment.course_id == data.course_id
        )
        .scalar()
    )

    if current_count >= course.max_students:
        raise HTTPException(
            status_code=400,
            detail="Course is full"
        )

    # 7. Tạo Enrollment
    enrollment = Enrollment(
        student_id=data.student_id,
        course_id=data.course_id,
        enrolled_at=datetime.utcnow()
    )

    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    return enrollment


def get_student_courses(
    db: Session,
    student_id: int
):
    # Kiểm tra Student
    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Lấy danh sách Course
    courses = (
        db.query(Course)
        .join(
            Enrollment,
            Enrollment.course_id == Course.id
        )
        .filter(
            Enrollment.student_id == student_id
        )
        .all()
    )

    return {
        "student_id": student.id,
        "full_name": student.full_name,
        "courses": courses
    }