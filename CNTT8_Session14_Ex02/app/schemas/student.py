from pydantic import BaseModel


class StudentCreate(BaseModel):
    full_name: str
    email: str
    major: str
    gpa: float


class StudentResponse(BaseModel):
    id: int
    full_name: str
    email: str
    major: str
    gpa: float

    class Config:
        from_attributes = True