from fastapi import FastAPI

from database import Base, engine
from models import User
from routers import router

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Student Authentication API"
)


app.include_router(router)


@app.get("/")
def root():

    return {
        "message": "Student Authentication API is running"
    }