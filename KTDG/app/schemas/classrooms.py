from pydantic import BaseModel 

class CreateClass(BaseModel):
    class_code:str
    class_name : str
    
    