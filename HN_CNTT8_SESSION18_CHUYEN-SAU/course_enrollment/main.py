from fastapi import FastAPI

from app.database import Base, engine
from app.routers.routers import router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Course Enrollment API",
    description="API đăng ký khóa học cho sinh viên",
    version="1.0.0"
)


app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Course Enrollment API is running"
    }