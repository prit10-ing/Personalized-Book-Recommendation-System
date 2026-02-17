# Use lightweight python
FROM python:3.12-slim

# Prevent python from buffering logs
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Flask default port
EXPOSE 5000

# Run app
CMD ["python", "app.py"]
