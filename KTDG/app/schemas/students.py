from pydantic import BaseModel 

class CreateStudents(BaseModel):
    student_code :str
    full_name : str
    email : str
    class_id : str