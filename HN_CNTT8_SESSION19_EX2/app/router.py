from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ClinicCreate, ClinicDetailResponse, DoctorUpdate, DoctorResponse
from app.service import *

router = APIRouter()


@router.post(
    "/clinics", response_model=ClinicDetailResponse, status_code=status.HTTP_201_CREATED
)
def create(data: ClinicCreate, db: Session = Depends(get_db)):
    return create_clinic(db, data)


@router.get("/clinics/{clinic_id}", response_model=ClinicDetailResponse)
def get_clinic(clinic_id: int, db: Session = Depends(get_db)):
    clinic = get_clinic_detail(db, clinic_id)

    if clinic is None:
        raise HTTPException(status_code=404, detail="Phòng khám không tồn tại")

    return clinic


@router.patch("/doctors/{doctor_id}", response_model=DoctorResponse)
def edit_doctor(doctor_id: int, data: DoctorUpdate, db: Session = Depends(get_db)):
    doctor = update_doctor(db, doctor_id, data)

    if doctor is None:
        raise HTTPException(status_code=404, detail="Bác sĩ không tồn tại")

    return doctor


@router.delete("/licenses/{license_id}")
def delete(license_id: int, db: Session = Depends(get_db)):
    license = delete_license(db, license_id)

    if license is None:
        raise HTTPException(status_code=404, detail="Chứng chỉ hành nghề không tồn tại")

    return {"message": "Xóa chứng chỉ hành nghề thành công", "license_id": license_id}
