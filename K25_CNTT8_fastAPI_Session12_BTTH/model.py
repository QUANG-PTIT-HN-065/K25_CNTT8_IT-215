from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from database import Base


class DocumentModel(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    subject = Column(String(100), nullable=False)
    document_type = Column(String(100), nullable=False)
    file_url = Column(String(255), nullable=False)


class CreateDocument(BaseModel):
    title: str
    subject: str
    document_type: str
    file_url: str