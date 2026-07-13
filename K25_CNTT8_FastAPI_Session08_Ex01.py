from enum import Enum
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

carriers = [
    {
        "id": 1,
        "code": "GHN",
        "name": "Giao Hang Nhanh",
        "max_weight_capacity": 5000,
        "status": "ACTIVE",
    },
    {
        "id": 2,
        "code": "GHTK",
        "name": "Giao Hang Tiet Kiem",
        "max_weight_capacity": 3000,
        "status": "ACTIVE",
    },
    {
        "id": 3,
        "code": "VTP",
        "name": "Viettel Post",
        "max_weight_capacity": 10000,
        "status": "SUSPENDED",
    },
]

shipments = [
    {
        "id": 1,
        "carrier_id": 1,
        "order_reference": "ORD-2026-001",
        "total_weight": 4200,
        "dispatch_date": "2026-07-01",
        "shift": "MORNING",
    }
]


class CarrierStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"


class Shift(str, Enum):
    MORNING = "MORNING"
    AFTERNOON = "AFTERNOON"
    NIGHT = "NIGHT"


class CarrierCreate(BaseModel):
    code: str
    name: str = Field(min_length=3)
    max_weight_capacity: int = Field(gt=0)
    status: CarrierStatus


class ShipmentCreate(BaseModel):
    carrier_id: int
    order_reference: str
    total_weight: int = Field(gt=0)
    dispatch_date: str
    shift: Shift


@app.post("/carriers", status_code=201)
def create_carrier(data: CarrierCreate):
    if any(c["code"] == data.code for c in carriers):
        raise HTTPException(status_code=400, detail="Code already exists")

    new_carrier = {
        "id": max([c["id"] for c in carriers], default=0) + 1,
        **data.model_dump(),
    }

    carriers.append(new_carrier)
    return new_carrier


@app.get("/carriers")
def get_carriers(
    keyword: Optional[str] = None,
    status: Optional[CarrierStatus] = None,
    min_weight: Optional[int] = None,
):
    result = carriers

    if keyword:
        keyword = keyword.lower()
        result = [
            c
            for c in result
            if keyword in c["code"].lower() or keyword in c["name"].lower()
        ]

    if status:
        result = [c for c in result if c["status"] == status]

    if min_weight is not None:
        result = [c for c in result if c["max_weight_capacity"] >= min_weight]

    return result


@app.get("/carriers/{carrier_id}")
def get_carrier(carrier_id: int):
    for carrier in carriers:
        if carrier["id"] == carrier_id:
            return carrier
    raise HTTPException(status_code=404, detail="Carrier not found")


@app.put("/carriers/{carrier_id}")
def update_carrier(carrier_id: int, data: CarrierCreate):
    for carrier in carriers:
        if carrier["id"] != carrier_id and carrier["code"] == data.code:
            raise HTTPException(status_code=400, detail="Code already exists")

    for i, carrier in enumerate(carriers):
        if carrier["id"] == carrier_id:
            carriers[i] = {"id": carrier_id, **data.model_dump()}
            return carriers[i]

    raise HTTPException(status_code=404, detail="Carrier not found")


@app.delete("/carriers/{carrier_id}")
def delete_carrier(carrier_id: int):
    for i, carrier in enumerate(carriers):
        if carrier["id"] == carrier_id:
            carriers.pop(i)
            return {"message": "Deleted"}
    raise HTTPException(status_code=404, detail="Carrier not found")


@app.post("/shipments", status_code=201)
def create_shipment(data: ShipmentCreate):
    carrier = next((c for c in carriers if c["id"] == data.carrier_id), None)

    if not carrier:
        raise HTTPException(status_code=404, detail="Carrier not found")

    if carrier["status"] != "ACTIVE":
        raise HTTPException(status_code=400, detail="Carrier is not active")

    if data.total_weight > carrier["max_weight_capacity"]:
        raise HTTPException(status_code=400, detail="Weight exceeds carrier capacity")

    if any(
        s["carrier_id"] == data.carrier_id
        and s["dispatch_date"] == data.dispatch_date
        and s["shift"] == data.shift
        for s in shipments
    ):
        raise HTTPException(
            status_code=400, detail="Carrier already scheduled for this shift"
        )

    new_shipment = {
        "id": max([s["id"] for s in shipments], default=0) + 1,
        **data.model_dump(),
    }

    shipments.append(new_shipment)
    return new_shipment


@app.get("/shipments")
def get_shipments():
    return shipments
