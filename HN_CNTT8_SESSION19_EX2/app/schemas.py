from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ClinicCreate(BaseModel):
    clinic_name: str = Field(..., min_length=1, max_length=100)

    specialty: str = Field(..., min_length=1, max_length=100)


class DoctorResponse(BaseModel):
    id: int
    doctor_code: str
    salary: float
    clinic_id: int

    model_config = ConfigDict(from_attributes=True)


class DoctorUpdate(BaseModel):
    doctor_code: Optional[str] = None
    salary: Optional[float] = None
    clinic_id: Optional[int] = None


class ClinicDetailResponse(BaseModel):
    id: int
    clinic_name: str
    specialty: str

    doctors: List[DoctorResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class LicenseResponse(BaseModel):
    id: int
    license_number: str
    issue_by: str
    doctor_id: int

    model_config = ConfigDict(from_attributes=True)
