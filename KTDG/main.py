from fastapi import FastAPI
from app.database import Base, engine
from app.routers.Students import router
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Student Management API"
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Student Management API"
    }