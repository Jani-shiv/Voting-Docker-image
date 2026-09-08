FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose backend port
EXPOSE 5000

# Run Flask application
CMD ["python", "app.py"]
