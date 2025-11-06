FROM python:3.11-slim

LABEL maintainer="GRASS Development Team <grass-dev@lists.osgeo.org>"
LABEL description="GRASS GIS MCP Server - Model Context Protocol server for GRASS GIS"
LABEL version="0.1.0"

# Install system dependencies and GRASS GIS
RUN apt-get update && apt-get install -y \
    grass \
    grass-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy MCP server files
COPY grass_mcp_server.py .
COPY pyproject.toml .
COPY setup.py .
COPY requirements.txt .
COPY README.md .

# Install Python dependencies and the package
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

# Create directory for GRASS data
RUN mkdir -p /grassdata

# Set environment variables
ENV GISDBASE=/grassdata \
    GRASS_VERBOSE=0 \
    PYTHONUNBUFFERED=1

# Health check (optional)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import grass_mcp_server; print('OK')" || exit 1

# Run the MCP server
ENTRYPOINT ["python", "-m", "grass_mcp_server"]

# Usage:
# Build: docker build -t grass-mcp-server .
# Run:   docker run -i grass-mcp-server
# With volume: docker run -i -v $(pwd)/grassdata:/grassdata grass-mcp-server
