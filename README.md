# Logistics Business Software System

A comprehensive FastAPI backend system designed for managing logistics business operations including products, orders, fleet management, and driver coordination.

## 🚀 Overview

This software system provides a robust solution for logistics businesses to streamline their operations. It offers a RESTful API built with FastAPI that handles product inventory, order management, fleet tracking, driver assignments, and real-time status updates.

## ✨ Features

- **Product Management**: Create and manage product inventory
- **Order Processing**: Handle order creation and tracking via webhooks
- **Fleet Management**: Track and manage delivery vehicles
- **Driver Coordination**: Manage driver information and assignments
- **Fleet Assignment**: Automatically assign available fleets to orders
- **Status Tracking**: Real-time order status updates
- **RESTful API**: Clean and documented API endpoints
- **High Performance**: Built with FastAPI for optimal speed

## 🛠️ Tech Stack

- **Backend Framework**: FastAPI
- **Language**: Python 3.7+
- **API Documentation**: Automatic OpenAPI/Swagger documentation
- **Architecture**: RESTful API design

## 📋 Prerequisites

Before running this application, make sure you have:

- Python 3.7 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## 🚀 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/limFakson/Logistics-business-software-system.git
   cd Logistics-business-software-system
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**

   ```bash
   uvicorn main:app --reload
   ```

5. **Access the API**
   - API Base URL: `http://localhost:8000`
   - Interactive Documentation: `https://logitrack-w83a.onrender.com/docs`
   - Alternative Docs: `https://logitrack-w83a.onrender.com/redoc`

## 📚 API Documentation

### Products Management

| Method | Endpoint     | Description                       |
| ------ | ------------ | --------------------------------- |
| POST   | `/products/` | Create a new product              |
| GET    | `/products/` | List all products with pagination |

**Create Product Example:**

```json
{
  "name": "Laptop",
  "quantity": 10
}
```

**Query Parameters for GET:**

- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Maximum records to return (default: 100)

### Order Management

| Method | Endpoint           | Description                    |
| ------ | ------------------ | ------------------------------ |
| POST   | `/orders/webhook/` | Create a new order via webhook |
| GET    | `/orders/`         | List all orders                |

**Create Order Example:**

```json
{
  "order_name": "Order-123",
  "destination": "New York",
  "product_id": 1
}
```

### Fleet Management

| Method | Endpoint   | Description        |
| ------ | ---------- | ------------------ |
| POST   | `/fleets/` | Create a new fleet |
| GET    | `/fleets/` | List all fleets    |

**Create Fleet Example:**

```json
{
  "name": "Fleet-A",
  "driver_id": 1,
  "status": "available",
  "last_maintenance": "2025-08-01"
}
```

### Driver Management

| Method | Endpoint    | Description         |
| ------ | ----------- | ------------------- |
| POST   | `/drivers/` | Create a new driver |
| GET    | `/drivers/` | List all drivers    |

**Create Driver Example:**

```json
{
  "name": "John Doe"
}
```

### Fleet Assignment

| Method | Endpoint         | Description                |
| ------ | ---------------- | -------------------------- |
| POST   | `/assign_fleet/` | Assign a fleet to an order |

**Request Example:**

```json
{
  "order_id": "Order-123",
  "fleet_id": 1
}
```

**Response:**

```json
{
  "message": "Order assigned to fleet successfully"
}
```

### Status Updates

| Method | Endpoint          | Description         |
| ------ | ----------------- | ------------------- |
| POST   | `/update_status/` | Update order status |

**Request Example:**

```json
{
  "order_id": "Order-123",
  "status": "delivered"
}
```

**Response:**

```json
{
  "message": "Order status updated successfully"
}
```

## 📁 Project Structure

```
Logistics-business-software-system/
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
├── models/              # Database models
├── routers/             # API route handlers
├── services/            # Business logic
└── README.md           # Project documentation
```

## 🔄 Usage Examples

### Creating a Complete Logistics Workflow

1. **Create a Driver**

   ```bash
   curl -X POST "https://logitrack-w83a.onrender.com/drivers/" \
        -H "Content-Type: application/json" \
        -d '{"name": "John Smith"}'
   ```

2. **Create a Fleet**

   ```bash
   curl -X POST "https://logitrack-w83a.onrender.com/fleets/" \
        -H "Content-Type: application/json" \
        -d '{
          "name": "Delivery Truck 01",
          "driver_id": 1,
          "status": "available",
          "last_maintenance": "2025-08-01"
        }'
   ```

3. **Create a Product**

   ```bash
   curl -X POST "https://logitrack-w83a.onrender.com/products/" \
        -H "Content-Type: application/json" \
        -d '{"name": "Electronics Package", "quantity": 50}'
   ```

4. **Create an Order**

   ```bash
   curl -X POST "https://logitrack-w83a.onrender.com/orders/webhook/" \
        -H "Content-Type: application/json" \
        -d '{
          "order_name": "ORD-2025-001",
          "destination": "Lagos, Nigeria",
          "product_id": 1
        }'
   ```

5. **Assign Fleet to Order**

   ```bash
   curl -X POST "https://logitrack-w83a.onrender.com/assign_fleet/" \
        -H "Content-Type: application/json" \
        -d '{"order_id": "ORD-2025-001", "fleet_id": 1}'
   ```

6. **Update Order Status**
   ```bash
   curl -X POST "https://logitrack-w83a.onrender.com/update_status/" \
        -H "Content-Type: application/json" \
        -d '{"order_id": "ORD-2025-001", "status": "in_transit"}'
   ```

## 🔧 Configuration

The application can be configured through environment variables:

- `DATABASE_URL`: Database connection string
- `API_HOST`: Host address (default: localhost)
- `API_PORT`: Port number (default: 8000)
- `DEBUG`: Enable debug mode (default: False)

## 🧪 Testing

Run the test suite:

```bash
pytest tests/
```

For test coverage:

```bash
pytest --cov=app tests/
```

## 🚀 Deployment

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Setup

```bash
# Install production ASGI server
pip install gunicorn

# Run with Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 API Response Formats

All API responses follow a consistent format:

**Success Response:**

```json
{
  "status": "success",
  "data": {...},
  "message": "Operation completed successfully"
}
```

**Error Response:**

```json
{
  "status": "error",
  "error": "Error description",
  "detail": "Detailed error information"
}
```

## 📊 Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

## 🛡️ Security

- Input validation on all endpoints
- CORS configuration for web applications
- Rate limiting (configurable)
- Authentication middleware ready

## 📈 Performance

- Asynchronous request handling
- Database connection pooling
- Efficient pagination
- Response compression
- Request/Response logging

## 📞 Support

For support and questions:

- Create an issue on GitHub
- Contact: [Repository Owner](https://github.com/limFakson)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔄 Changelog

### v1.0.0

- Initial release
- Basic CRUD operations for all entities
- Fleet assignment functionality
- Order status management
- Webhook integration for orders

---

**Built with ❤️ using FastAPI**
