from fastapi import FastAPI

from app.database import Base, engine
from app.router import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Medical Management API")


app.include_router(router)
