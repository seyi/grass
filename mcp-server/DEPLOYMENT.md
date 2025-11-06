# GRASS GIS MCP Server - Deployment Guide

This guide covers different deployment methods for the GRASS GIS MCP server.

## Table of Contents

1. [Quick Install (Recommended)](#quick-install-recommended)
2. [Installation Methods](#installation-methods)
3. [Configuration](#configuration)
4. [Deployment Options](#deployment-options)
5. [Publishing to PyPI](#publishing-to-pypi)
6. [Docker Deployment](#docker-deployment)
7. [Troubleshooting](#troubleshooting)

---

## Quick Install (Recommended)

### For End Users

**Option 1: Install from PyPI (once published)**
```bash
pip install grass-mcp-server
```

**Option 2: Install from GitHub**
```bash
pip install git+https://github.com/OSGeo/grass.git#subdirectory=mcp-server
```

**Option 3: Install from local clone**
```bash
git clone https://github.com/OSGeo/grass.git
cd grass/mcp-server
pip install .
```

### Configure Claude Desktop

1. **Find your config file:**
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. **Add the MCP server:**

   **If installed via pip:**
   ```json
   {
     "mcpServers": {
       "grass-gis": {
         "command": "grass-mcp-server"
       }
     }
   }
   ```

   **If running from source:**
   ```json
   {
     "mcpServers": {
       "grass-gis": {
         "command": "python",
         "args": ["-m", "grass_mcp_server"]
       }
     }
   }
   ```

3. **Restart Claude Desktop**

---

## Installation Methods

### Method 1: PyPI (Python Package Index)

**When published to PyPI:**

```bash
# Standard installation
pip install grass-mcp-server

# With development tools
pip install grass-mcp-server[dev]

# Upgrade to latest version
pip install --upgrade grass-mcp-server
```

### Method 2: From GitHub

**Direct installation:**
```bash
pip install git+https://github.com/OSGeo/grass.git#subdirectory=mcp-server
```

**Specific branch or tag:**
```bash
# From a specific branch
pip install git+https://github.com/OSGeo/grass.git@branch-name#subdirectory=mcp-server

# From a specific tag
pip install git+https://github.com/OSGeo/grass.git@v0.1.0#subdirectory=mcp-server
```

### Method 3: Local Development

**For developers or contributors:**

```bash
# Clone the repository
git clone https://github.com/OSGeo/grass.git
cd grass/mcp-server

# Install in editable mode
pip install -e .

# Or with development dependencies
pip install -e ".[dev]"
```

### Method 4: Using uv (Fast Python Package Manager)

```bash
# Install with uv
uv pip install grass-mcp-server

# From GitHub
uv pip install git+https://github.com/OSGeo/grass.git#subdirectory=mcp-server
```

---

## Configuration

### Claude Desktop Configuration

**Full configuration example:**

```json
{
  "mcpServers": {
    "grass-gis": {
      "command": "grass-mcp-server",
      "env": {
        "GRASS_VERBOSE": "0",
        "GISDBASE": "/home/user/grassdata"
      }
    }
  }
}
```

**Configuration options:**

- `command`: The command to run the server
- `args`: Additional command-line arguments (if needed)
- `env`: Environment variables
  - `GRASS_VERBOSE`: Set verbosity level (0-3)
  - `GISDBASE`: Default GRASS database path
  - `GRASS_ADDON_PATH`: Path to GRASS addons

### Other MCP Clients

**Generic MCP client configuration:**

```json
{
  "servers": {
    "grass-gis": {
      "type": "stdio",
      "command": ["grass-mcp-server"],
      "protocol": "mcp"
    }
  }
}
```

### Testing the Installation

```bash
# Test that the module can be imported
python -c "import grass_mcp_server; print('OK')"

# Test the server startup (Ctrl+C to exit)
grass-mcp-server

# Run tests to verify installation
python -m pytest /path/to/grass/mcp-server/tests
```

---

## Deployment Options

### Option 1: System-Wide Installation

**For single-user systems:**

```bash
pip install grass-mcp-server
```

**For multi-user systems (requires sudo):**

```bash
sudo pip install grass-mcp-server
```

**Using pipx (isolated environment):**

```bash
# Install pipx if not already installed
pip install pipx
pipx ensurepath

# Install grass-mcp-server in isolated environment
pipx install grass-mcp-server
```

### Option 2: Virtual Environment

**Recommended for development:**

```bash
# Create virtual environment
python -m venv grass-mcp-env
source grass-mcp-env/bin/activate  # On Windows: grass-mcp-env\Scripts\activate

# Install
pip install grass-mcp-server

# Configure Claude Desktop to use venv python
# In claude_desktop_config.json:
{
  "mcpServers": {
    "grass-gis": {
      "command": "/path/to/grass-mcp-env/bin/python",
      "args": ["-m", "grass_mcp_server"]
    }
  }
}
```

### Option 3: Docker Container

**See [Docker Deployment](#docker-deployment) section below**

### Option 4: Conda Environment

```bash
# Create conda environment
conda create -n grass-mcp python=3.11
conda activate grass-mcp

# Install
pip install grass-mcp-server

# Configure Claude Desktop
{
  "mcpServers": {
    "grass-gis": {
      "command": "/path/to/miniconda3/envs/grass-mcp/bin/python",
      "args": ["-m", "grass_mcp_server"]
    }
  }
}
```

---

## Publishing to PyPI

### For Maintainers

**Prerequisites:**
```bash
pip install build twine
```

**Build and publish:**

```bash
# Navigate to mcp-server directory
cd mcp-server

# Build distribution packages
python -m build

# Check the built packages
twine check dist/*

# Upload to TestPyPI (for testing)
twine upload --repository testpypi dist/*

# Upload to PyPI (production)
twine upload dist/*
```

**Install from TestPyPI:**
```bash
pip install --index-url https://test.pypi.org/simple/ grass-mcp-server
```

---

## Docker Deployment

### Using Docker

**Create a Dockerfile:**

```dockerfile
FROM python:3.11-slim

# Install GRASS GIS dependencies
RUN apt-get update && apt-get install -y \
    grass \
    grass-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install MCP server
COPY mcp-server /app/mcp-server
WORKDIR /app/mcp-server

RUN pip install --no-cache-dir .

# Set entrypoint
ENTRYPOINT ["python", "-m", "grass_mcp_server"]
```

**Build and run:**

```bash
# Build image
docker build -t grass-mcp-server .

# Run container
docker run -i grass-mcp-server
```

### Docker Compose

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  grass-mcp:
    image: grass-mcp-server:latest
    stdin_open: true
    tty: true
    volumes:
      - ./grassdata:/grassdata
    environment:
      - GISDBASE=/grassdata
      - GRASS_VERBOSE=0
```

**Usage:**
```bash
docker-compose up grass-mcp
```

### Pre-built Docker Image

**Once published to Docker Hub:**

```bash
# Pull the image
docker pull osgeo/grass-mcp-server:latest

# Run
docker run -i osgeo/grass-mcp-server:latest
```

---

## Distribution Methods

### GitHub Releases

1. **Tag a release:**
   ```bash
   git tag -a v0.1.0 -m "Release version 0.1.0"
   git push origin v0.1.0
   ```

2. **Create GitHub Release:**
   - Go to repository releases
   - Create new release from tag
   - Add release notes
   - Attach built distributions

3. **Users can install:**
   ```bash
   pip install https://github.com/OSGeo/grass/releases/download/v0.1.0/grass_mcp_server-0.1.0-py3-none-any.whl
   ```

### OS-Specific Packages

**Debian/Ubuntu (.deb):**
```bash
# Build with stdeb
pip install stdeb
python setup.py --command-packages=stdeb.command bdist_deb
```

**RPM-based (Fedora/RHEL):**
```bash
# Build with bdist_rpm
python setup.py bdist_rpm
```

**macOS (Homebrew):**
Create a Homebrew formula in a tap.

**Windows Installer:**
Use PyInstaller to create standalone executable.

---

## Automated Deployment

### GitHub Actions CI/CD

**Deploy on release (.github/workflows/release.yml):**

```yaml
name: Release

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install build twine

    - name: Build package
      working-directory: mcp-server
      run: python -m build

    - name: Publish to PyPI
      working-directory: mcp-server
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

---

## Troubleshooting

### Common Issues

**1. "grass-mcp-server: command not found"**

- Ensure pip bin directory is in PATH
- Try: `python -m grass_mcp_server` instead
- Check installation: `pip show grass-mcp-server`

**2. "ModuleNotFoundError: No module named 'mcp'"**

- Install dependencies: `pip install -r requirements.txt`
- Or reinstall: `pip install --force-reinstall grass-mcp-server`

**3. "GRASS GIS not found"**

- Install GRASS GIS on your system
- Ubuntu/Debian: `sudo apt-get install grass`
- macOS: `brew install grass`
- Windows: Download from https://grass.osgeo.org/download/

**4. Claude Desktop not detecting the server**

- Verify config file location
- Check JSON syntax is valid
- Restart Claude Desktop completely
- Check logs in Claude Desktop settings

**5. Permission errors**

- Don't use sudo with pip (use virtual environments instead)
- Check file permissions on GRASS database directories
- Ensure user has access to specified GISDBASE

### Debug Mode

**Run with verbose output:**

```bash
# Set environment variable
export GRASS_VERBOSE=3

# Run server
grass-mcp-server
```

**Check logs:**
- Claude Desktop logs: Check application settings for log location
- MCP server logs: stderr output from the server

### Getting Help

- **Issues**: https://github.com/OSGeo/grass/issues
- **Discussions**: https://discourse.osgeo.org/c/grass/62
- **Documentation**: See README.md and USAGE.md

---

## Version Management

### Semantic Versioning

The project follows [SemVer](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Upgrading

```bash
# Check current version
pip show grass-mcp-server

# Upgrade to latest
pip install --upgrade grass-mcp-server

# Install specific version
pip install grass-mcp-server==0.1.0
```

### Pinning Versions

**In requirements.txt:**
```
grass-mcp-server==0.1.0  # Exact version
grass-mcp-server>=0.1.0,<0.2.0  # Compatible versions
grass-mcp-server~=0.1.0  # Patch updates only
```

---

## Security Considerations

### Installation Security

- Always verify package signatures when available
- Use official distribution channels (PyPI, GitHub releases)
- Check SHA256 hashes of downloaded packages
- Keep dependencies updated

### Runtime Security

- Run with minimal required permissions
- Don't expose GRASS database to untrusted users
- Use separate GRASS locations for different projects
- Keep GRASS GIS software updated

### Network Security

- MCP server communicates via stdio only (no network exposure)
- No external API calls or data transmission
- All processing is local to the machine

---

## Next Steps

After deployment:

1. ✅ Verify installation: `grass-mcp-server --help`
2. ✅ Configure Claude Desktop
3. ✅ Test with a simple query: "List available maps in my GRASS location"
4. ✅ Read USAGE.md for usage examples
5. ✅ Join the community on GRASS Discourse

For more information, see:
- [README.md](README.md) - Main documentation
- [USAGE.md](USAGE.md) - Usage examples and workflows
- [TESTING_SUMMARY.md](TESTING_SUMMARY.md) - Testing information
