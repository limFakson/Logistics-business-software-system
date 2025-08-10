# seed_data.py
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Product, Order, Fleet, Driver
import random

# Create all tables if they don't exist yet
Base.metadata.create_all(bind=engine)


def seed_data():
    db: Session = SessionLocal()

    try:
        # Clear existing data (optional)
        db.query(Order).delete()
        db.query(Fleet).delete()
        db.query(Product).delete()
        db.query(Driver).delete()
        db.commit()

        # Seed Drivers
        driver_names = ["John Doe", "Jane Smith", "Michael Johnson", "Alice Brown"]
        drivers = [Driver(name=name) for name in driver_names]
        db.add_all(drivers)
        db.commit()

        # Seed Fleets
        fleets = [
            Fleet(
                name=f"Fleet {i+1}",
                driver_id=random.choice(drivers).id,
                status=random.choice(["active", "maintenance", "inactive"]),
                last_maintenance="2025-08-01",
            )
            for i in range(3)
        ]
        db.add_all(fleets)
        db.commit()

        # Seed Products
        product_names = ["Laptop", "Phone", "Tablet", "Headphones"]
        products = [
            Product(name=name, quantity=random.randint(5, 20)) for name in product_names
        ]
        db.add_all(products)
        db.commit()

        # Seed Orders
        destinations = ["New York", "Los Angeles", "Chicago", "Houston"]
        customer_name = ["Killerman Sage", "Oluchi Nwankwo", "Tunde Benedicta", "Grace Miller"]
        orders = [
            Order(
                order_name=f"Order {i+1}",
                product_id=random.choice(products).id,
                destination=random.choice(destinations),
                customer_name=random.choice(customer_name),
                status=random.choice(["pending", "shipped", "delivered"]),
                fleet_id=random.choice(fleets).id,
            )
            for i in range(5)
        ]
        db.add_all(orders)
        db.commit()

        print("✅ Database seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
