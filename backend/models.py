from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    order_name = Column(String, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    customer_name = Column(String, index=True)
    destination = Column(String, index=True)
    status = Column(String, default="pending")
    fleet_id = Column(Integer, ForeignKey("fleets.id"))

    product = relationship("Product", back_populates="orders")
    fleet = relationship("Fleet", back_populates="orders")


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Integer, default=0)

    orders = relationship("Order", back_populates="product")


class Fleet(Base):
    __tablename__ = "fleets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"))
    status = Column(String, index=True)
    vehicle_type = Column(String, index=True)
    last_maintenance = Column(String, index=True)

    driver = relationship("Driver", back_populates="fleets")
    orders = relationship("Order", back_populates="fleet")


class Driver(Base):
    __tablename__ = "drivers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    fleets = relationship("Fleet", back_populates="driver")


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    month = Column(String, index=True, nullable=False)  # e.g. "June 2025"
    title = Column(String, nullable=False)  # Short summary/title
    file_url = Column(String, nullable=False)  # Path or URL to file
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Route(Base):
    __tablename__ = "routes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  # e.g. "Lagos → Abuja"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    shipments = relationship("Shipment", back_populates="route")


class Shipment(Base):
    __tablename__ = "shipments"
    id = Column(Integer, primary_key=True, index=True)
    tracking_id = Column(String, unique=True, index=True, nullable=False)
    customer_name = Column(String, nullable=False)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)
    status = Column(
        String, nullable=False
    )  # e.g. "pending", "shipped", "delivered", "delayed"
    revenue = Column(Float, default=0.0)
    shipped_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    route = relationship("Route", back_populates="shipments")
