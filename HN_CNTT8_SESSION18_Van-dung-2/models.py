from sqlalchemy import  Column, Integer, String, ForeignKey
from sqlalchemy.orm import   relationship
from database import Base

class Classroom(Base):
    __tablename__ = "classrooms"

    id = Column(Integer, primary_key=True, index=True)

    class_name = Column(String(100), nullable=False)

    status = Column(String(20), nullable=False)

    capacity = Column(Integer, nullable=False)

    students = relationship("Student", back_populates="classroom")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)

    student_code = Column(String(20), nullable=False)

    full_name = Column(String(100), nullable=False)

    classroom_id = Column(Integer, ForeignKey("classrooms.id"), nullable=False)

    classroom = relationship("Classroom", back_populates="students")

