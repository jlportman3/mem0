# Stage 1: Builder stage for installing dependencies
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04 as builder

WORKDIR /app

# Install Python and pip, and git
RUN apt-get update && apt-get install -y python3 python3-pip git

# Create models directory and download the embedding model with proper cleanup
RUN mkdir -p /models && \
    git config --global http.postBuffer 524288000 && \
    git clone --depth 1 https://huggingface.co/BAAI/bge-large-en-v1.5 /models/bge-large-en-v1.5 && \
    cd /models/bge-large-en-v1.5 && \
    rm -rf .git

# Copy only the requirements file to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final application stage
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

WORKDIR /app

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Copy installed packages from the builder stage
COPY --from=builder /usr/local/lib/python3.10/dist-packages /usr/local/lib/python3.10/dist-packages
COPY --from=builder /usr/bin/python3 /usr/bin/python3
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the downloaded model from the builder stage
COPY --from=builder /models /models

# Copy the application code
COPY . .
COPY jmemory /app/jmemory

# Expose the port and run the application
EXPOSE 8000
VOLUME /models
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
