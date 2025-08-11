from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Order, Product, Fleet, Driver
from schemas import (
    ProductCreate,
    ProductModel,
    OrderCreate,
    OrderModel,
    FleetCreate,
    FleetModel,
    DriverCreate,
    DriverModel,
)

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",  # for dev frontend
    "http://127.0.0.1:8000",
    "*",  # <-- allow all (if you're testing, remove in prod!)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Serve static files from ./frontend
app.mount("/static", StaticFiles(directory="."), name="static")


# Serve index.html at root
@app.get("/")
def read_index():
    return FileResponse("index.html")


@app.post("/api/products/", response_model=ProductModel)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.get("/api/products/", response_model=list[ProductModel])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products


@app.post("/api/orders/webhook/", response_model=OrderModel)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@app.get("/api/orders/", response_model=list[OrderModel])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = db.query(Order).offset(skip).limit(limit).all()
    return orders


@app.post("/api/fleets/", response_model=FleetModel)
def create_fleet(fleet: FleetCreate, db: Session = Depends(get_db)):
    db_fleet = Fleet(**fleet.dict())
    db.add(db_fleet)
    db.commit()
    db.refresh(db_fleet)
    return db_fleet


@app.get("/api/fleets/", response_model=list[FleetModel])
def read_fleets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    fleets = db.query(Fleet).offset(skip).limit(limit).all()
    for fleet in fleets:
        driver_name = db.query(Driver).filter(Driver.id == fleet.driver_id).first().name
        fleet.driver_name = driver_name
    return fleets


@app.post("/api/drivers/", response_model=DriverModel)
def create_driver(driver: DriverCreate, db: Session = Depends(get_db)):
    db_driver = Driver(**driver.dict())
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    return db_driver


@app.get("/api/drivers/", response_model=list[DriverModel])
def read_drivers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    drivers = db.query(Driver).offset(skip).limit(limit).all()
    return drivers


@app.post("/api/assign_fleet/")
def assign_fleet(order_id: str, fleet_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.fleet_id = fleet_id
    order.status = "assigned"
    db.commit()
    return {"message": "Order assigned to fleet successfully"}


@app.post("/api/update_status/")
def update_status(order_id: str, status: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = status
    db.commit()
    return {"message": "Order status updated successfully"}
