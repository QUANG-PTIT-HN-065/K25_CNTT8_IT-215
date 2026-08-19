from sqlalchemy.orm import Session

from app.model import Clinic, Doctor, License


def create_clinic(db: Session, clinic_data):
    try:
        clinic = Clinic(**clinic_data.model_dump())

        db.add(clinic)
        db.commit()
        db.refresh(clinic)

        return clinic

    except Exception:
        db.rollback()
        raise


def get_clinic_detail(db: Session, clinic_id: int):
    clinic = db.query(Clinic).filter(Clinic.id == clinic_id).first()

    return clinic


def update_doctor(db: Session, doctor_id: int, doctor_data):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if doctor is None:
        return None

    try:
        update_data = doctor_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(doctor, key, value)

        db.commit()
        db.refresh(doctor)

        return doctor

    except Exception:
        db.rollback()
        raise


def delete_license(db: Session, license_id: int):
    license = db.query(License).filter(License.id == license_id).first()

    if license is None:
        return None

    try:
        db.delete(license)
        db.commit()

        return license

    except Exception:
        db.rollback()
        raise
