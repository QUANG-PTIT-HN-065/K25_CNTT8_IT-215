from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from model import ShipmentUpdate
from service import update_shipment_service

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "Shipment API đang hoạt động!"
    }


@app.put("/shipments/{shipment_id}")
def update_shipment(
    shipment_id: int,
    shipment_update: ShipmentUpdate,
    db: Session = Depends(get_db)
):

    shipment = update_shipment_service(
        db,
        shipment_id,
        shipment_update
    )

    return {
        "message": "Cập nhật đơn giao hàng thành công",
        "data": shipment
    }