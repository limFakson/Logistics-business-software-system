from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, unique=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
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

    driver = relationship("Driver", back_populates="fleets")
    orders = relationship("Order", back_populates="fleet")


class Driver(Base):
    __tablename__ = "drivers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    fleets = relationship("Fleet", back_populates="driver")
