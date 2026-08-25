from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas import (
    ResourceCreate,
    ResourcePublishUpdate,
    ResourceResponse,
    TokenResponse,
    UserResponse,
)
from services import create_access_token, get_current_user, require_admin

router = APIRouter()


@router.get("/health", tags=["Public"])
def health_check():
    return {"status": "UP"}


@router.post("/auth/login", response_model=TokenResponse, tags=["Auth"])
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User).filter(models.User.username == form_data.username).first()
    )

    if not user or user.hashed_password != form_data.password:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is locked/inactive",
        )

    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=UserResponse, tags=["Users"])
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@router.get("/resources", response_model=List[ResourceResponse], tags=["Resources"])
def get_resources(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(models.Resource)

    if current_user.role != "admin":  # type: ignore
        query = query.filter(models.Resource.is_published == True)

    return query.all()


@router.get(
    "/resources/{resource_id}", response_model=ResourceResponse, tags=["Resources"]
)
def get_resource_detail(
    resource_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    resource = (
        db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    )

    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found"
        )

    if current_user.role != "admin" and not resource.is_published:  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found"
        )

    return resource


@router.post(
    "/resources",
    response_model=ResourceResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Resources"],
)
def create_resource(
    resource_in: ResourceCreate,
    admin_user: models.User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    new_resource = models.Resource(
        title=resource_in.title,
        description=resource_in.description,
        url=resource_in.url,
        is_published=resource_in.is_published,
        created_by=admin_user.username,
    )
    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)
    return new_resource


@router.patch(
    "/resources/{resource_id}/publish",
    response_model=ResourceResponse,
    tags=["Resources"],
)
def publish_resource(
    resource_id: int,
    publish_in: ResourcePublishUpdate,
    admin_user: models.User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    resource = (
        db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    )
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found"
        )

    resource.is_published = publish_in.is_published  # type: ignore
    db.commit()
    db.refresh(resource)
    return resource


@router.delete("/resources/{resource_id}", tags=["Resources"])
def delete_resource(
    resource_id: int,
    admin_user: models.User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    resource = (
        db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    )
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found"
        )

    db.delete(resource)
    db.commit()
    return {"message": f"Resource {resource_id} deleted successfully"}
