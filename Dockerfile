# Use the official Python 3.10 slim image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app:/app/proto


# Update the package list and install necessary system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    libpq-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the entire project into the container
COPY . .

# Install the Python packages from requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Compile the proto files
RUN python -m grpc_tools.protoc -I./proto --python_out=./proto --grpc_python_out=./proto ./proto/agent.proto

# Expose the application port for gRPC
EXPOSE 50051

# Command to run the application
CMD ["python", "api/rpc_protocol.py"]
