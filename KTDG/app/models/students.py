from sqlalchemy import Column, Integer,String,ForeignKey
from app.database import Base

class Students(Base):
    __tablename__ = "students"
    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True,index=True)
    student_code = Column(String(100),unique=True,nullable=False)
    full_name =  Column(String(100),nullable=False)
    email  = Column(String(100),unique=True,nullable=False)
    class_id = Column(Integer,ForeignKey("classrooms.id"))