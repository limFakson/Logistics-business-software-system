from pydantic import BaseModel


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
    order_id: str
    product_id: int


class OrderCreate(OrderBase):
    pass


class OrderModel(OrderBase):
    id: int
    status: str
    fleet_id: int | None

    class Config:
        orm_mode = True


class FleetBase(BaseModel):
    name: str
    driver_id: int


class FleetCreate(FleetBase):
    pass


class FleetModel(FleetBase):
    id: int

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
