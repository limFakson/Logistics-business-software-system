# Logistics-business-software-system
Software system for better run of  a logistics business service

# 🚚 Fleet & Order Management API

A **FastAPI** backend for managing **products**, **orders**, **fleets**, and **drivers**, including endpoints to assign fleets and update order statuses.

---

## 📦 Base URL
http://localhost:8000/api
 

---

## 📑 Endpoints

### 🛒 Products
| Method | Endpoint       | Description        |
|--------|----------------|--------------------|
| `POST` | `/products/`   | Create a product   |
| `GET`  | `/products/`   | List all products  |

**POST Request Body Example:**
```json
{
  "name": "Laptop",
  "quantity": 10
}
```

### GET Query Parameters

- skip (int) – Number of records to skip (default 0)

- limit (int) – Max records to return (default 100)

## 📦 Orders

| Method | Endpoint           | Description     |
| ------ | ------------------ | --------------- |
| `POST` | `/orders/webhook/` | Create an order |
| `GET`  | `/orders/`         | List all orders |

### POST Request Body Example
```json
{
  "order_name": "Order-123",
  "destination": "New York",
  "product_id": 1
}
```

### 🚛 Fleets
| Method | Endpoint   | Description    |
| ------ | ---------- | -------------- |
| `POST` | `/fleets/` | Create a fleet |
| `GET`  | `/fleets/` | List fleets    |

### POST Request Body Example
```json
{
  "name": "Fleet-A",
  "driver_id": 1,
  "status": "available",
  "last_maintenance": "2025-08-01"
}
```

## 👨‍✈️ Drivers
| Method | Endpoint    | Description     |
| ------ | ----------- | --------------- |
| `POST` | `/drivers/` | Create a driver |
| `GET`  | `/drivers/` | List drivers    |

### POST Request Body Example
```json
{
  "name": "John Doe"
}
```
## 🔄 Assign Fleet to Order
| Method | Endpoint         | Description                |
| ------ | ---------------- | -------------------------- |
| `POST` | `/assign_fleet/` | Assign a fleet to an order |

### Request Body Example
```json
{
  "order_id": "Order-123",
  "fleet_id": 1
}
```

### Response
```json
{
  "message": "Order assigned to fleet successfully"
}
```

## 📌 Update Order Status
| Method | Endpoint          | Description              |
| ------ | ----------------- | ------------------------ |
| `POST` | `/update_status/` | Update an order's status |

### Request Body Example
```json
{
  "order_id": "Order-123",
  "status": "delivered"
}
```

### Response
```json
{
  "message": "Order status updated successfully"
}
```

## 📌 Notes
### All POST endpoints require a JSON request body.

### skip and limit parameters allow pagination for GET endpoints.

### Ensure that order_id exists when calling /assign_fleet/ and /update_status/.

## 🔍 API Documentation
### When the server is running, interactive API docs are available at:

### Swagger UI → http://localhost:8000/docs

### ReDoc → http://localhost:8000/redoc