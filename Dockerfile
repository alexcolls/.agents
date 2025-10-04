# .agents Dockerfile
# Multi-stage build for optimized image size

FROM python:3.10-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copy Poetry files
COPY pyproject.toml poetry.lock* ./

# Install dependencies (without dev dependencies)
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Final stage
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 -s /bin/bash agents && \
    mkdir -p /app /data && \
    chown -R agents:agents /app /data

# Set working directory
WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=agents:agents . .

# Switch to non-root user
USER agents

# Create data directories
RUN mkdir -p /data/agents /data/logs /data/tmp

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import sys; sys.exit(0)"

# Expose ports (if needed for web interface in future)
# EXPOSE 8080

# Entry point
ENTRYPOINT ["python3", "-m", "src.cli.main"]

# Default command (interactive mode)
CMD []
