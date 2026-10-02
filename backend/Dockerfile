FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend files into a `backend` folder inside /app
COPY . /app/backend

# Set the python path so the backend module can be found
ENV PYTHONPATH=/app

# Run with Uvicorn using the module path (backend.main:app)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
