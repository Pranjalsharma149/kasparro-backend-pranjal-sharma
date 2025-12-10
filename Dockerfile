# Dockerfile
# Stage 1: Build Stage (using a robust base image)
FROM python:3.11-slim as builder

# Set environment variables for non-interactive commands
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the dependency files
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# --- MANDATORY P0.3: Define command to run the API service ---
# The ETL service will be triggered separately (e.g., via a scheduler or startup script)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Expose the API port
EXPOSE 8000