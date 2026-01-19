# Build stage - install dependencies
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .

# Install to user directory (not system-wide)
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage - final image
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Make sure Python can find packages installed to /root/.local
ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
