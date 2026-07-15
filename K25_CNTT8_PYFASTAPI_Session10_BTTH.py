from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os

load_dotenv()
password = quote_plus(os.getenv("PASS_WORD", ""))

app = FastAPI()

DATABASE_URL = f"mysql+pymysql://root:{password}@localhost:3306/PYfatsAPI"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class ShipmentModel(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String(50), unique=True, nullable=False)
    status = Column(String(50), default="PREPARING")


class CreateShipment(BaseModel):
    tracking_number: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/shipments", status_code=status.HTTP_201_CREATED)
def create_shipment(shipment: CreateShipment, db: Session = Depends(get_db)):
    exist = (
        db.query(ShipmentModel)
        .filter(ShipmentModel.tracking_number == shipment.tracking_number)
        .first()
    )

    if exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mã vận đơn này đã được khởi tạo trước đó",
        )

    new_shipment = ShipmentModel(tracking_number=shipment.tracking_number)

    db.add(new_shipment)
    db.commit()
    db.refresh(new_shipment)

    return {"message": "Đăng ký mã vận đơn thành công", "data": new_shipment}


@app.get("/shipments")
def get_all_shipments(db: Session = Depends(get_db)):
    shipments = db.query(ShipmentModel).all()

    return {"message": "Lấy danh sách vận đơn thành công", "data": shipments}
