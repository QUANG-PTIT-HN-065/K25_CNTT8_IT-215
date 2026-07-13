from enum import Enum
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()

assets = [
    {"id": 1, "serial_number": "SN-MAC-01", "model": "MacBook Pro M3", "stock_available": 5, "status": "READY"},
    {"id": 2, "serial_number": "SN-DELL-02", "model": "Dell UltraSharp 27", "stock_available": 10, "status": "READY"},
    {"id": 3, "serial_number": "SN-THINK-03", "model": "ThinkPad X1 Carbon", "stock_available": 0, "status": "REPAIRING"}
]

allocations = [
    {
        "id": 1,
        "asset_id": 1,
        "employee_email": "dev.nguyen@company.com",
        "allocated_quantity": 1,
        "start_date": "2026-07-01",
        "duration_months": 12
    }
]


class AssetStatus(str, Enum):
    READY = "READY"
    ALLOCATED = "ALLOCATED"
    REPAIRING = "REPAIRING"
    SCRAPPED = "SCRAPPED"


class AssetCreate(BaseModel):
    serial_number: str
    model: str = Field(min_length=2, max_length=255)
    stock_available: int = Field(ge=0)
    status: AssetStatus


class AllocationCreate(BaseModel):
    asset_id: int
    employee_email: EmailStr
    allocated_quantity: int = Field(gt=0)
    start_date: str
    duration_months: int = Field(ge=1, le=12)


@app.post("/assets", status_code=201)
def create_asset(data: AssetCreate):
    if any(a["serial_number"] == data.serial_number for a in assets):
        raise HTTPException(status_code=400, detail="Serial number already exists")

    new_asset = {
        "id": max([a["id"] for a in assets], default=0) + 1,
        **data.model_dump()
    }
    assets.append(new_asset)
    return new_asset


@app.get("/assets")
def get_assets(
    keyword: Optional[str] = None,
    status: Optional[AssetStatus] = None,
    min_stock: Optional[int] = None
):
    result = assets

    if keyword:
        keyword = keyword.lower()
        result = [
            a for a in result
            if keyword in a["serial_number"].lower() or keyword in a["model"].lower()
        ]

    if status:
        result = [a for a in result if a["status"] == status]

    if min_stock is not None:
        result = [a for a in result if a["stock_available"] >= min_stock]

    return result


@app.get("/assets/{asset_id}")
def get_asset(asset_id: int):
    for asset in assets:
        if asset["id"] == asset_id:
            return asset
    raise HTTPException(status_code=404, detail="Asset not found")


@app.put("/assets/{asset_id}")
def update_asset(asset_id: int, data: AssetCreate):
    for asset in assets:
        if asset["id"] != asset_id and asset["serial_number"] == data.serial_number:
            raise HTTPException(status_code=400, detail="Serial number already exists")

    for i, asset in enumerate(assets):
        if asset["id"] == asset_id:
            assets[i] = {"id": asset_id, **data.model_dump()}
            return assets[i]

    raise HTTPException(status_code=404, detail="Asset not found")


@app.delete("/assets/{asset_id}")
def delete_asset(asset_id: int):
    for i, asset in enumerate(assets):
        if asset["id"] == asset_id:
            assets.pop(i)
            return {"message": "Deleted"}
    raise HTTPException(status_code=404, detail="Asset not found")


@app.post("/allocations", status_code=201)
def create_allocation(data: AllocationCreate):
    asset = next((a for a in assets if a["id"] == data.asset_id), None)

    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    if asset["status"] != "READY":
        raise HTTPException(status_code=400, detail="Asset is not ready")

    if data.allocated_quantity > asset["stock_available"]:
        raise HTTPException(status_code=400, detail="Not enough stock available")

    asset["stock_available"] -= data.allocated_quantity

    if asset["stock_available"] == 0:
        asset["status"] = "ALLOCATED"

    new_allocation = {
        "id": max([a["id"] for a in allocations], default=0) + 1,
        **data.model_dump()
    }

    allocations.append(new_allocation)
    return new_allocation


@app.get("/allocations")
def get_allocations():
    return allocations