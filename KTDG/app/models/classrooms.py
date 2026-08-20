from sqlalchemy import Column, Integer,String
from app.database import Base

class ClassRooms(Base):
    __tablename__ = "classrooms"
    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True,index=True)
    class_code = Column(String(100),unique=True,nullable=False)
    class_name = Column(String(100),unique=True,nullable=False)