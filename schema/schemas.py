from pydantic import BaseModel, EmailStr, Field
from typing import Literal

class ClassroomResponse(BaseModel):
    id: int
    class_code: str
    class_name: str
    status: str

    class Config:
        from_attributes = True

class StudentCreate(BaseModel):
    student_code: str = Field(..., min_length=3, max_length=20)
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=16, le=60)
    gender: Literal["male", "female", "other"]
    class_id: int = Field(..., ge=1)

class StudentUpdate(BaseModel):
    student_code: str = Field(..., min_length=3, max_length=20)
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=16, le=60)
    gender: Literal["male", "female", "other"]
    class_id: int = Field(..., ge=1)

class StudentResponse(BaseModel):
    id: int
    student_code: str
    full_name: str
    email: str
    age: int
    gender: str
    classroom: ClassroomResponse

    class Config:
        from_attributes = True