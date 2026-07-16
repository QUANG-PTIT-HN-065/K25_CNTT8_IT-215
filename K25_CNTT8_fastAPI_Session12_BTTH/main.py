from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from model import CreateDocument
from service import (
    get_all_documents,
    create_document,
    delete_document
)

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Learning Document API"}


@app.get("/documents")
def get_documents(db: Session = Depends(get_db)):
    return get_all_documents(db)


@app.post("/documents")
def add_document(
    document: CreateDocument,
    db: Session = Depends(get_db)
):
    return create_document(document, db)


@app.delete("/documents/{document_id}")
def remove_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    return delete_document(document_id, db)