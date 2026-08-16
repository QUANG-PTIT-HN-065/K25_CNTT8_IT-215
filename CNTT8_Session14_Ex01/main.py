from fastapi import FastAPI

app = FastAPI(title="Product Management API")
from fastapi import FastAPI

from app.database import Base, engine
from app.models.product import Product
from app.routers import router

Base.metadata.create_all(bind=engine)


app = FastAPI(title="Product Management API")


app.include_router(router)


@app.get("/")
def root():
    return {"message": "Product Management API"}
