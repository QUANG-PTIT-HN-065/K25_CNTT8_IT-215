from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(title="Course Management API")

courses = {
    1: {
        "id": 1,
        "code": "PY101",
        "name": "Python Basic",
        "duration": 30,
        "fee": 3000000
    },
    2: {
        "id": 2,
        "code": "API101",
        "name": "FastAPI Basic",
        "duration": 24,
        "fee": 2500000
    },
    3: {
        "id": 3,
        "code": "JV101",
        "name": "Java Basic",
        "duration": 40,
        "fee": 4000000
    }
}



class Course(BaseModel):
    code: str
    name: str = Field(..., min_length=1)
    duration: int = Field(..., gt=0)
    fee: float = Field(..., ge=0)


@app.post("/courses")
def create_course(course: Course):

    for item in courses.values():
        if item["code"].lower() == course.code.lower():
            raise HTTPException(
                status_code=400,
                detail="Course code already exists"
            )

    new_id = max(courses.keys(), default=0) + 1

    new_course = {
        "id": new_id,
        **course.model_dump()
    }

    courses[new_id] = new_course

    return {
        "message": "Course created successfully",
        "course": new_course
    }


@app.get("/courses")
def get_courses(
    keyword: str | None = Query(default=None),
    min_fee: float | None = Query(default=None, ge=0),
    max_fee: float | None = Query(default=None, ge=0)
):

    result = list(courses.values())

    if keyword:
        keyword = keyword.lower()

        result = [
            course
            for course in result
            if keyword in course["name"].lower()
            or keyword in course["code"].lower()
        ]

    if min_fee is not None:
        result = [
            course
            for course in result
            if course["fee"] >= min_fee
        ]

    if max_fee is not None:
        result = [
            course
            for course in result
            if course["fee"] <= max_fee
        ]

    return {
        "total": len(result),
        "courses": result
    }


@app.get("/courses/{course_id}")
def get_course(course_id: int):

    course = courses.get(course_id)

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return course


@app.put("/courses/{course_id}")
def update_course(course_id: int, updated_course: Course):

    if course_id not in courses:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    for item in courses.values():
        if (
            item["id"] != course_id
            and item["code"].lower() == updated_course.code.lower()
        ):
            raise HTTPException(
                status_code=400,
                detail="Course code already exists"
            )

    courses[course_id].update(updated_course.model_dump())

    return {
        "message": "Course updated successfully",
        "course": courses[course_id]
    }


@app.delete("/courses/{course_id}")
def delete_course(course_id: int):

    if course_id not in courses:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    deleted_course = courses.pop(course_id)

    return {
        "message": "Course deleted successfully",
        "course": deleted_course
    }

