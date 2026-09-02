# ==============================================================================
# Enterprise B2B Lead Extractor - Elite Hardened Dockerfile
# ==============================================================================

# --- Stage 1: Build Environment ---
FROM python:3.11-slim AS builder

# Set Python optimization environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies required for compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create and populate an isolated Python virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install pinned requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# --- Stage 2: Secure Production Runtime ---
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Copy the pre-built virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Create a non-root system user and group for maximum container security
RUN groupadd -g 1000 appgroup && \
    useradd -u 1000 -g appgroup -ms /bin/bash appuser

# Copy application code and assign ownership to the non-root user
COPY --chown=appuser:appgroup . /app

# Switch context to the non-root user
USER appuser

# Define default execution command for the scraping pipeline
CMD ["python", "lead_extractor.py"]
