from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from fastapi import FastAPI, Depends, HTTPException, status, Request
from pydantic import BaseModel, Field
from typing import Literal
from dotenv import load_dotenv
from urllib.parse import quote_plus
from datetime import datetime
import os

load_dotenv()

password = quote_plus(os.getenv("PASS_WORD", ""))

DATABASE_URL = f"mysql+pymysql://root:{password}@localhost:3306/PYfatsAPI"

app = FastAPI()

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class MedicalDevice(Base):
    __tablename__ = "medical_devices"

    id = Column(Integer, primary_key=True, index=True)
    device_code = Column(String(50), unique=True, nullable=False)
    device_name = Column(String(255), nullable=False)
    department = Column(String(100), nullable=False)
    status = Column(String(20), default="ACTIVE")



class CreateDevice(BaseModel):
    device_code: str
    device_name: str = Field(..., min_length=3)
    department: str
    status: Literal["ACTIVE", "INACTIVE"] = "ACTIVE"


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def response(status_code: int, message: str, error, data, path: str):
    return {
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


@app.get("/")
def home():
    return {"message": "Medical Device API"}



@app.post("/devices", status_code=status.HTTP_201_CREATED)
def create_device(
    device: CreateDevice, request: Request, db: Session = Depends(get_db)
):

    exist = (
        db.query(MedicalDevice)
        .filter(MedicalDevice.device_code == device.device_code)
        .first()
    )

    if exist:
        raise HTTPException(status_code=400, detail="Device Code already exists")

    try:

        new_device = MedicalDevice(
            device_code=device.device_code,
            device_name=device.device_name,
            department=device.department,
            status=device.status,
        )

        db.add(new_device)

        db.commit()

        db.refresh(new_device)

        return response(
            201, "Thêm thiết bị y tế thành công", None, new_device, request.url.path
        )

    except Exception:

        db.rollback()

        raise HTTPException(status_code=500, detail="Lỗi hệ thống")


@app.get("/devices")
def get_all_devices(request: Request, db: Session = Depends(get_db)):

    devices = db.query(MedicalDevice).all()

    return response(
        200, "Lấy danh sách thiết bị thành công", None, devices, request.url.path
    )

@app.get("/devices/{device_id}")
def get_device(device_id: int, request: Request, db: Session = Depends(get_db)):

    device = db.query(MedicalDevice).filter(MedicalDevice.id == device_id).first()

    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")

    return response(
        200, "Lấy chi tiết thiết bị thành công", None, device, request.url.path
    )
