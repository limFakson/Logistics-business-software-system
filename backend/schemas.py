from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProductBase(BaseModel):
    name: str
    quantity: int


class ProductCreate(ProductBase):
    pass


class ProductModel(ProductBase):
    id: int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    order_name: str
    customer_name: str
    destination: str
    product_id: int


class OrderCreate(OrderBase):
    pass


class OrderModel(OrderBase):
    id: int
    status: str
    fleet_id: int | None

    class Config:
        orm_mode = True


class DriverBase(BaseModel):
    name: str


class DriverCreate(DriverBase):
    pass


class DriverModel(DriverBase):
    id: int

    class Config:
        orm_mode = True


class FleetBase(BaseModel):
    name: str
    driver_id: int
    status: str
    last_maintenance: str
    vehicle_type: str


class FleetCreate(FleetBase):
    pass


class FleetModel(FleetBase):
    id: int
    driver_name: str

    class Config:
        orm_mode = True


class ReportBase(BaseModel):
    month: str
    title: str
    file_url: str


class ReportCreate(ReportBase):
    pass


class ReportModel(ReportBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class RouteModel(BaseModel):
    id: int
    name: str
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


class ShipmentBase(BaseModel):
    tracking_id: str
    customer_name: str
    route_id: int
    status: str
    revenue: Optional[float] = 0.0
    shipped_at: Optional[datetime] = None


class ShipmentCreate(ShipmentBase):
    pass


class ShipmentModel(ShipmentBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


class DashboardKPIs(BaseModel):
    totalOrders: int
    deliveries: int
    pending: int
    revenue: float


class DashboardCharts(BaseModel):
    months: list[str]
    shipmentsPerMonth: list[int]
    statusCounts: list[int]  # e.g. [delivered, delayed] or chosen mapping


class DashboardTables(BaseModel):
    recentShipments: list[ShipmentModel]
    topRoutes: list[dict]  # [{"route": "Lagos → Abuja", "count": 12}, ...]


class DashboardResponse(BaseModel):
    kpis: DashboardKPIs
    charts: DashboardCharts
    tables: DashboardTables
