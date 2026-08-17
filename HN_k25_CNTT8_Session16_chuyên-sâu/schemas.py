from datetime import datetime

from pydantic import BaseModel


class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int


class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrolled_at: datetime

    class Config:
        from_attributes = True


class CourseResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class StudentCoursesResponse(BaseModel):
    student_id: int
    full_name: str
    courses: list[CourseResponse]

    class Config:
        from_attributes = True