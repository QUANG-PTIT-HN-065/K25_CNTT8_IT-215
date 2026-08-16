from sqlalchemy.orm import Session
from CNTT8_Session14_Ex01.app.models.product import Product
from CNTT8_Session14_Ex01.app.schemas.product import ProductCreate


def get_products(db: Session):
    return db.query(Product).all()


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def create_product(db: Session, product: ProductCreate):
    new_product = Product(name=product.name, price=product.price)

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


def update_product(db: Session, product_id: int, product: ProductCreate):
    existing_product = get_product(db, product_id)

    if not existing_product:
        return None

    existing_product.name = product.name  # type: ignore
    existing_product.price = product.price  # type: ignore

    db.commit()
    db.refresh(existing_product)

    return existing_product


def delete_product(db: Session, product_id: int):
    existing_product = get_product(db, product_id)

    if not existing_product:
        return None

    db.delete(existing_product)
    db.commit()

    return existing_product
