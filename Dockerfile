# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy backend dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend /app

# Expose port
EXPOSE 8000

# Run FastAPI (Uvicorn) and serve frontend as static files
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
