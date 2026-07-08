from fastapi import FastAPI , status
from pydantic import BaseModel, EmailStr, Field, ConfigDict

app = FastAPI()

class Student_Create(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    full_name:str = Field(...,min_length=3)
    email:EmailStr 
    age : int = Field(..., ge=15 , le = 60)
    phone: str = Field(..., pattern=r"^\d{10,11}$")
    course: str  
    note:str|None = Field(default=None , max_length=200)
    
@app.post("/students/register", status_code=status.HTTP_201_CREATED)
def create_students_register(student: Student_Create):
    return {
         "message": "Đăng ký học viên thành công",
         "data" : {
            "full_name": student.full_name.title(),
            "email": student.email,
            "age": student.age,
            "phone": student.phone,
            "course": student.course.lower(),
            "note": student.note.lower() if student.note else None
         }
    }