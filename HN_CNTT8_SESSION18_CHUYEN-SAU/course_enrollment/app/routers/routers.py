from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.schemas import (
    EnrollmentCreate,
    EnrollmentResponse,
    StudentCoursesResponse
)
from app.services.services import (
    create_enrollment,
    get_student_courses
)


router = APIRouter()


@router.post(
    "/enrollments",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_enrollment_api(
    data: EnrollmentCreate,
    db: Session = Depends(get_db)
):
    return create_enrollment(db, data)


@router.get(
    "/students/{student_id}/courses",
    response_model=StudentCoursesResponse
)
def get_student_courses_api(
    student_id: int,
    db: Session = Depends(get_db)
):
    return get_student_courses(db, student_id)