from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from collections import Counter, defaultdict
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Order, Product, Fleet, Driver, Report, Shipment, Route
from schemas import *

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*",  # <-- allow all (if you're testing, remove in prod!)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Allow cookies and other credentials to be sent with requests
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers to be sent in the request
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


@app.post("/api/reports/", response_model=ReportModel)
def create_report(report: ReportCreate, db: Session = Depends(get_db)):
    new_report = Report(**report.dict())
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report


@app.get("/api/reports/", response_model=list[ReportModel])
def get_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Report).offset(skip).limit(limit).all()


@app.get("/api/reports/{report_id}", response_model=ReportModel)
def get_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@app.delete("/api/reports/{report_id}")
def delete_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    db.delete(report)
    db.commit()
    return {"message": "Report deleted successfully"}


@app.get("/api/dashboard", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db), months_count: int = 6):
    """
    Returns:
      - KPIs (total orders, deliveries, pending, revenue)
      - Charts data (months array, shipments per month, status counts [delivered, delayed])
      - Tables: recent shipments and top routes
    """
    shipments: list[Shipment] = db.query(Shipment).order_by(Shipment.shipped_at).all()

    # KPIs
    total_orders = len(shipments)
    deliveries = sum(1 for s in shipments if s.status.lower() == "delivered")
    pending = sum(1 for s in shipments if s.status.lower() == "pending")
    revenue = sum((s.revenue or 0.0) for s in shipments)

    # Charts: last N months (includes months with 0)
    now = datetime.utcnow()
    months = []
    for i in range(months_count - 1, -1, -1):
        m = (now.replace(day=1) - __relativedelta_months(i)).strftime("%b %Y")
        months.append(m)

    # Count shipments per month:
    # map "Mon YYYY" -> count
    month_counts = defaultdict(int)
    for s in shipments:
        if s.shipped_at:
            key = s.shipped_at.strftime("%b %Y")
            month_counts[key] += 1

    shipments_per_month = [month_counts.get(m, 0) for m in months]

    # status counts: delivered vs delayed (if you want on-time vs delayed)
    delivered_count = sum(1 for s in shipments if s.status.lower() == "delivered")
    delayed_count = sum(1 for s in shipments if s.status.lower() == "delayed")
    status_counts = [delivered_count, delayed_count]

    # Recent Shipments (latest 8)
    recent_q = db.query(Shipment).order_by(Shipment.created_at.desc()).limit(8).all()
    recent_shipments = [ShipmentModel.from_orm(s) for s in recent_q]

    # Top routes
    route_counter = Counter()
    for s in shipments:
        route_name = s.route.name if s.route else "Unknown"
        route_counter[route_name] += 1
    top_routes = [{"route": r, "count": c} for r, c in route_counter.most_common(6)]

    return {
        "kpis": {
            "totalOrders": total_orders,
            "deliveries": deliveries,
            "pending": pending,
            "revenue": round(revenue, 2),
        },
        "charts": {
            "months": months,
            "shipmentsPerMonth": shipments_per_month,
            "statusCounts": status_counts,
        },
        "tables": {"recentShipments": recent_shipments, "topRoutes": top_routes},
    }


# helper to step months (small utility)
def __relativedelta_months(months: int):
    """
    returns a datetime.timedelta-like object to subtract months from a date by
    (we'll implement as a small helper that returns a replacement datetime).
    In the query usage above we just need something subtractable from a date.
    But to keep it simple/hard-coded we can implement month arithmetic here:
    """

    # We'll return a function-like object with __rsub__ support.
    class _RD:
        def __init__(self, months):
            self.months = months

        def __rsub__(self, dt):
            # dt - _RD -> result datetime
            year = dt.year
            month = dt.month - self.months
            # adjust
            while month <= 0:
                month += 12
                year -= 1
            # keep day 1
            return dt.replace(year=year, month=month, day=1)

    return _RD(months)


# Optional smaller endpoints
@app.get("/api/shipments/recent", response_model=list[ShipmentModel])
def get_recent_shipments(limit: int = 8, db: Session = Depends(get_db)):
    q = db.query(Shipment).order_by(Shipment.created_at.desc()).limit(limit).all()
    return [ShipmentModel.from_orm(s) for s in q]


@app.get("/api/routes/top")
def get_top_routes(limit: int = 6, db: Session = Depends(get_db)):
    shipments = db.query(Shipment).all()
    from collections import Counter

    counter = Counter()
    for s in shipments:
        name = s.route.name if s.route else "Unknown"
        counter[name] += 1
    return [{"route": r, "count": c} for r, c in counter.most_common(limit)]
