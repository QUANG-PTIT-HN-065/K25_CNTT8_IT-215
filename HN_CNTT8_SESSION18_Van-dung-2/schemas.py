from pydantic import BaseModel, ConfigDict, Field 
from typing import List


class ClassroomCreate(BaseModel):
    class_name: str
    status: str
    capacity: int


class StudentCreate(BaseModel):
    student_code: str
    full_name: str
    classroom_id: int


class TransferClassRequest(BaseModel):
    new_classroom_id: int


class StudentResponse(BaseModel):
    id: int
    student_code: str
    full_name: str
    classroom_id: int

    model_config = ConfigDict(from_attributes=True)


class ClassroomDetailResponse(BaseModel):
    id: int
    class_name: str
    status: str
    capacity: int

    students: List[StudentResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)