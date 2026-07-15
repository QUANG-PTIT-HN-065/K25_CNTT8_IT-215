"""
Phần 1: Báo cáo phân tích bài toán
1. Phân tích Input/Output
Input

API: POST /inventories

Chỉ cho phép người dùng nhập:

- warehouse_code: Mã kho vận (duy nhất)
- location: Địa điểm kho

- Không cho phép client truyền: id

Output thành công
- HTTP Status: 201 Created

Output thất bại

Nếu mã kho đã tồn tại
- HTTP Status: 400 Bad Request

2. Thuật toán xử lý
Bước 1. Nhận dữ liệu từ Client

Bước 2. Truy vấn Database:
Bước 3.

- Nếu tìm thấy dữ liệu
    - Dừng chương trình
    - Trả về HTTPException 400

- Nếu không tìm thấy
    - Tạo đối tượng InventoryModel
    - Thêm vào Session bằng .add()
    - Gọi .commit() để lưu xuống MySQL
    - Gọi .refresh() lấy dữ liệu mới
    - Trả về kết quả thành công
"""

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os

load_dotenv()

password = quote_plus(os.getenv("PASS_WORD", ""))

DATABASE_URL = f"mysql+pymysql://root:{password}@localhost:3306/PYfatsAPI"

app = FastAPI()

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class InventoryModel(Base):
    __tablename__ = "inventories"

    id = Column(Integer, primary_key=True, index=True)
    warehouse_code = Column(String(50), unique=True, nullable=False)
    location = Column(String(100), nullable=False)

class CreateInventory(BaseModel):
    warehouse_code: str
    location: str

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Inventory API đang hoạt động!"}


@app.post("/inventories", status_code=status.HTTP_201_CREATED)
def create_inventory(inventory: CreateInventory, db: Session = Depends(get_db)):
    exist = (
        db.query(InventoryModel)
        .filter(InventoryModel.warehouse_code == inventory.warehouse_code)
        .first()
    )

    if exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mã kho vận đã tồn tại trên hệ thống, không thể tạo trùng",
        )

    new_inventory = InventoryModel(
        warehouse_code=inventory.warehouse_code, location=inventory.location
    )

    db.add(new_inventory)

    db.commit()

    db.refresh(new_inventory)

    return {"message": "Khởi tạo phiếu kho vận thành công", "data": new_inventory}
