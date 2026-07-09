from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(title="Student Management API")

students = {
    1: {
        "id": 1,
        "code": "SV001",
        "name": "Nguyen Van A",
        "email": "a@gmail.com",
        "age": 20
    },
    2: {
        "id": 2,
        "code": "SV002",
        "name": "Tran Thi B",
        "email": "b@gmail.com",
        "age": 22
    },
    3: {
        "id": 3,
        "code": "SV003",
        "name": "Le Van C",
        "email": "c@gmail.com",
        "age": 18
    }
}


class Student(BaseModel):
    code: str
    name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=1)
    age: int = Field(..., gt=0)


@app.post("/students")
def create_student(student: Student):

    for item in students.values():
        if item["code"].lower() == student.code.lower():
            raise HTTPException(
                status_code=400,
                detail="Student code already exists"
            )

    new_id = max(students.keys(), default=0) + 1

    new_student = {
        "id": new_id,
        **student.model_dump()
    }

    students[new_id] = new_student

    return {
        "message": "Student created successfully",
        "student": new_student
    }


@app.get("/students")
def get_students(
    keyword: str | None = Query(None),
    min_age: int | None = Query(None, gt=0),
    max_age: int | None = Query(None, gt=0)
):

    result = list(students.values())

    if keyword:
        keyword = keyword.lower()

        result = [
            student
            for student in result
            if keyword in student["name"].lower()
            or keyword in student["code"].lower()
            or keyword in student["email"].lower()
        ]


    if min_age is not None:
        result = [
            student
            for student in result
            if student["age"] >= min_age
        ]

    if max_age is not None:
        result = [
            student
            for student in result
            if student["age"] <= max_age
        ]

    return {
        "total": len(result),
        "students": result
    }


@app.get("/students/{student_id}")
def get_student(student_id: int):

    student = students.get(student_id)

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    updated_student: Student
):

    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    for item in students.values():
        if (
            item["id"] != student_id
            and item["code"].lower() == updated_student.code.lower()
        ):
            raise HTTPException(
                status_code=400,
                detail="Student code already exists"
            )

    students[student_id].update(
        updated_student.model_dump()
    )

    return {
        "message": "Student updated successfully",
        "student": students[student_id]
    }


@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    deleted_student = students.pop(student_id)

    return {
        "message": "Student deleted successfully",
        "student": deleted_student
    }

@app.get("/")
def home():
    return {
        "message": "Student Management API is running"
    }