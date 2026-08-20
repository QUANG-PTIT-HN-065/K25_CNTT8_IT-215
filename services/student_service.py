from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.models import Student, Classroom
from schema.schemas import StudentCreate, StudentUpdate

def get_all(db: Session, keyword: str = "", class_id: int = 0):
    query = db.query(Student)
    
    if keyword != "":
        kw = f"%{keyword}%"
        query = query.filter(
            or_(
                Student.full_name.ilike(kw),
                Student.student_code.ilike(kw),
                Student.email.ilike(kw)
            )
        )
        
    if class_id != 0:
        query = query.filter(Student.class_id == class_id)
    
    return query.all(), "", 200


def get_by_id(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        return False, "Không tìm thấy sinh viên!", 404
    return student, "", 200


def create(db: Session, payload: StudentCreate):
    classroom = db.query(Classroom).filter(Classroom.id == payload.class_id).first()
    if not classroom:
        return False, "Lớp học không tồn tại!", 404
    if classroom.status.lower() != "active":
        return False, "Lớp học không ở trạng thái hoạt động!", 409
        
    count = db.query(Student).filter(Student.class_id == classroom.id).count()
    if count >= classroom.max_students:
        return False, "Lớp học đã đủ số lượng sinh viên!", 409

    if db.query(Student).filter(Student.student_code == payload.student_code).first():
        return False, "Mã sinh viên đã tồn tại!", 409
    if db.query(Student).filter(Student.email == payload.email).first():
        return False, "Email đã tồn tại!", 409

    new_student = Student(**payload.model_dump())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student, "", 201


def update(db: Session, student_id: int, payload: StudentUpdate):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        return False, "Không tìm thấy sinh viên!", 404

    if db.query(Student).filter(Student.student_code == payload.student_code, Student.id != student_id).first():
        return False, "Mã sinh viên đã được sử dụng bởi sinh viên khác!", 409
    if db.query(Student).filter(Student.email == payload.email, Student.id != student_id).first():
        return False, "Email đã được sử dụng bởi sinh viên khác!", 409

    if student.class_id != payload.class_id:
        new_class = db.query(Classroom).filter(Classroom.id == payload.class_id).first()
        if not new_class:
            return False, "Lớp mới không tồn tại!", 404
        if new_class.status.lower() != "active":
            return False, "Lớp mới không hoạt động!", 409
        count = db.query(Student).filter(Student.class_id == new_class.id).count()
        if count >= new_class.max_students:
            return False, "Lớp mới đã đầy!", 409

    for key, value in payload.model_dump().items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)
    return student, "", 200