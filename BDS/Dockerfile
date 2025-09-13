FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies if needed
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements (even though we only use standard library)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 2>/dev/null || true

# Copy the unification script
COPY unify_bds_data.py .

# Create directories for data
RUN mkdir -p /app/data \
    /app/boycott.thewitness/output \
    /app/dontbuyintooccupation.org/output \
    /app/investigate.afsc.org

# Set the data directory as a volume
VOLUME ["/app/data"]

# Default command
CMD ["python", "-u", "unify_bds_data.py", "--path", "/app", "--output", "/app/data/unified_bds_data.json"]