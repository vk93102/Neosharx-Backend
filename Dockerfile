# =============================================================================
# Dockerfile — NeoSharX Backend (Production)
#
# Multi-stage build:
#   Stage 1 (builder) — install & compile Python wheels
#   Stage 2 (runtime) — lean final image with only runtime artefacts
#
# Build:  docker build -t neosharx-backend:latest .
# Run:    docker run --env-file .env -p 8000:8000 neosharx-backend:latest
# =============================================================================

# ---------------------------------------------------------------------------
# Stage 1 — Builder
# ---------------------------------------------------------------------------
FROM python:3.11-slim AS builder

# Prevent .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

# Install build-time system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies into a target directory
COPY requirements_prod.txt .
RUN pip install --upgrade pip \
    && pip wheel --no-cache-dir --wheel-dir /build/wheels -r requirements_prod.txt


# ---------------------------------------------------------------------------
# Stage 2 — Runtime
# ---------------------------------------------------------------------------
FROM python:3.11-slim AS runtime

LABEL maintainer="NeoSharX Team <dev@neosharx.io>" \
      org.opencontainers.image.title="NeoSharX Backend" \
      org.opencontainers.image.description="Django REST API for the NeoSharX platform" \
      org.opencontainers.image.version="1.0.0"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=backend.settings \
    PORT=8000 \
    WEB_CONCURRENCY=3

# Install only runtime system deps (libpq for psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq5 \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user for security
RUN groupadd --gid 1001 appgroup \
    && useradd --uid 1001 --gid appgroup --shell /bin/bash --create-home appuser

WORKDIR /app

# Install pre-built wheels from the builder stage
COPY --from=builder /build/wheels /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels /wheels/* \
    && rm -rf /wheels

# Copy application source code
COPY --chown=appuser:appgroup . .

# Copy and make the entrypoint executable
RUN chmod +x scripts/entrypoint.sh scripts/start.sh 2>/dev/null || true

# Collect static files (whitenoise serves them)
RUN python manage.py collectstatic --noinput \
        --settings=backend.settings \
    2>/dev/null || echo "Static files collection deferred to runtime"

# Drop to non-root user
USER appuser

# Health check — hits the /healthz/ endpoint every 30s
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -fsS http://localhost:${PORT}/healthz/ || exit 1

EXPOSE ${PORT}

ENTRYPOINT ["scripts/entrypoint.sh"]
CMD ["scripts/start.sh"]
