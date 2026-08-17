# 1. Quan hệ Database

# Đây là quan hệ N-N:

# Course
# Một Student đăng ký nhiều Course
# Một Course có nhiều Student
# Enrollment là bảng trung gian
# Enrollment.student_id -> students.id
# Enrollment.course_id -> courses.id

from fastapi import FastAPI

from app.database import Base, engine
from app.models import Student, Course, Enrollment
from app.schemas import (
    EnrollmentCreate,
    EnrollmentResponse,
    StudentCoursesResponse
)


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Course Management API"
)


@app.get("/")
def root():
    return {
        "message": "Course Management API"
    }


@app.post(
    "/enrollments",
    response_model=EnrollmentResponse,
    status_code=201
)
def create_enrollment(data: EnrollmentCreate):
    pass


@app.get(
    "/students/{student_id}/courses",
    response_model=StudentCoursesResponse
)
def get_student_courses(student_id: int):
    pass