# seed_data.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import SessionLocal, engine, Base
from models import Product, Order, Fleet, Driver, Report, Route, Shipment
from datetime import datetime, timedelta
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
                vehicle_type=random.choice(["Truck", "Motorcycle", "Car", "Airplane"])
            )
            for i in range(4)
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
        
        months = ["June 2025", "May 2025", "April 2025", "March 2025"]
        titles = [
            "Revenue, Deliveries, Fleet usage",
            "Delivery insights, Operational cost",
            "Performance metrics, Routes summary",
            "Customer satisfaction, Fuel efficiency"
        ]
        file_urls = [
            "/reports/june2025.pdf",
            "/reports/may2025.pdf",
            "/reports/april2025.pdf",
            "/reports/march2025.pdf"
        ]

        reports = [
            Report(
                month=random.choice(months),
                title=random.choice(titles),
                file_url=random.choice(file_urls),
                created_at=datetime.utcnow()
            )
            for _ in range(6)
        ]

        db.add_all(reports)
        db.commit()

        print("✅ Database seeded successfully!")
    
        ROUTES = [
            "Lagos → Abuja",
            "Lagos → Port Harcourt",
            "Abuja → Kano",
            "Onitsha → Enugu",
            "Ibadan → Ilorin",
            "Owerri → Uyo",
        ]

        CUSTOMERS = [
            "Oluchi Nwankwo", "Tunde Benedicta", "Grace Miller",
            "Killerman Sage", "Joseph Edem", "Amina Bello", "Samuel Nwachukwu"
        ]

        STATUSES = ["pending", "shipped", "delivered", "delayed"]

        def random_date_within_last_months(months_back=6):
            # pick random day in last `months_back` months
            now = datetime.utcnow()
            days_back = random.randint(0, months_back * 30)
            return now - timedelta(days=days_back)
        
        try:
            routes = [
                Route(name=name)
                for name in ROUTES
            ]

            db.add_all(routes)
            db.commit()
            
            route_objs = []
            for r in ROUTES:
                obj = db.query(Route).filter(Route.name == r).first()
                if not obj:
                    obj = Route(name=r)
                    db.add(obj)
                    try:
                        db.commit()
                    except IntegrityError:
                        db.rollback()
                        obj = db.query(Route).filter(Route.name == r).first()
                route_objs.append(obj)

            # create shipments
            shipments = []
            for i in range(60):  # create 60 sample shipments
                route = random.choice(route_objs)
                status = random.choices(STATUSES, weights=[0.25, 0.25, 0.4, 0.1])[0]
                shipped_at = random_date_within_last_months(6) if status != "pending" else None
                tracking_id = f"TRK{random.randint(1000,9999)}"
                s = Shipment(
                    tracking_id=tracking_id,
                    customer_name=random.choice(CUSTOMERS),
                    route_id=route.id,
                    status=status,
                    revenue=round(random.uniform(50, 500), 2),
                    shipped_at=shipped_at
                )
                shipments.append(s)

            db.add_all(shipments)
            db.commit()
            print("Seeded routes & shipments")
        except Exception as e:
            db.rollback()
            print("Seeding failed:", e)
        finally:
            db.close()

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
