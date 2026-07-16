from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from model import DocumentModel, CreateDocument


def get_all_documents(db: Session):
    documents = db.query(DocumentModel).all()

    return {
        "message": "Lấy danh sách tài liệu thành công",
        "data": documents
    }


def create_document(document: CreateDocument, db: Session):

    new_document = DocumentModel(
        title=document.title,
        subject=document.subject,
        document_type=document.document_type,
        file_url=document.file_url
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return {
        "message": "Thêm tài liệu thành công",
        "data": new_document
    }


def delete_document(document_id: int, db: Session):

    document = (
        db.query(DocumentModel)
        .filter(DocumentModel.id == document_id)
        .first()
    )

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy tài liệu"
        )

    db.delete(document)
    db.commit()

    return {
        "message": "Xóa tài liệu thành công",
        "data": document
    }