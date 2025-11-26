# GRASS GIS MCP Server

[![Testing Phase](https://img.shields.io/badge/status-testing-yellow)](TESTING_INVITATION.md)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: GPL v2+](https://img.shields.io/badge/License-GPL%20v2+-blue.svg)](LICENSE)

A Model Context Protocol (MCP) server that exposes GRASS GIS geospatial processing capabilities to AI assistants like Claude.

> **🧪 Testing Phase:** We're seeking testers! See [TESTING_INVITATION.md](TESTING_INVITATION.md) for how to participate.

## 🚀 Quick Install for Testers

```bash
pip install git+https://github.com/seyi/grass.git@claude/create-geospatial-mcp-grass-011CUr9bMgUcm9QX2hz9KwdX#subdirectory=mcp-server
```

See **[QUICKSTART.md](QUICKSTART.md)** for detailed installation instructions and testing guide.

## Overview

This MCP server provides AI assistants with access to powerful geospatial analysis tools from GRASS GIS (Geographic Resources Analysis Support System). GRASS GIS is a comprehensive open-source GIS software suite used for geospatial data management, analysis, and visualization.

## Features

The server exposes the following GRASS GIS capabilities:

### Raster Operations
- **grass_raster_info**: Get detailed information about raster maps (dimensions, resolution, extent, data type)
- **grass_raster_univar**: Calculate univariate statistics (min, max, mean, standard deviation, etc.)
- **grass_mapcalc**: Execute raster map algebra for complex mathematical operations
- **grass_slope_aspect**: Calculate slope and aspect from Digital Elevation Models (DEMs)

### Vector Operations
- **grass_vector_info**: Get information about vector maps (features, types, extent, attributes)
- **grass_buffer**: Create buffers around vector features for proximity analysis

### General Operations
- **grass_list_maps**: List all maps in a location/mapset (raster, vector, or 3D raster)
- **grass_region_info**: Get computational region information (extent, resolution, dimensions)

### Visualization (Phase 1) ✨
- **grass_visualize_raster**: Create PNG visualizations of raster maps with legends, scale bars, and north arrows
- **grass_create_composite**: Create composite visualizations combining multiple layers (e.g., elevation with hillshade)
- **grass_create_interactive_map**: Generate interactive HTML maps with pan/zoom capabilities

### Advanced Analysis (Phase 2A) ✨ NEW
- **grass_watershed**: Watershed analysis and stream extraction from DEMs
- **grass_viewshed**: Calculate viewshed (visible areas) from observer points
- **grass_reclass**: Reclassify raster values into new categories
- **grass_overlay**: Vector overlay operations (intersect, union, difference)
- **grass_import_raster**: Import raster data with automatic reprojection

### Universal Access (Phase 2B) ✨ NEW
- **grass_execute**: Execute ANY of the 500+ GRASS GIS commands with full parameter control

## Quick Start

### Option 1: Automated Installation (Recommended)

**Linux/macOS:**
```bash
cd mcp-server
./install.sh
```

**Windows (PowerShell):**
```powershell
cd mcp-server
powershell -ExecutionPolicy Bypass -File install.ps1
```

The script will guide you through the installation process.

### Option 2: Manual Installation

**Install from source:**
```bash
cd mcp-server
pip install .
```

**Or install from GitHub (once published):**
```bash
pip install git+https://github.com/OSGeo/grass.git#subdirectory=mcp-server
```

**Or from PyPI (once published):**
```bash
pip install grass-mcp-server
```

### Prerequisites

- **Python 3.10+**: Required
- **GRASS GIS**: Recommended but optional for testing
  - Ubuntu/Debian: `sudo apt-get install grass grass-dev`
  - macOS: `brew install grass`
  - Windows: Download from [GRASS GIS website](https://grass.osgeo.org/download/)
- **Visualization Dependencies** (optional, for visualization tools):
  - `pip install matplotlib rasterio folium`
  - Not required for core GRASS tools
  - Visualization tools will provide helpful error messages if dependencies are missing

### Development Installation

For development with testing and code quality tools:

```bash
cd mcp-server
pip install -e ".[dev]"
```

## Testing

The MCP server includes a comprehensive test suite with unit tests, integration tests, and mocks.

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=grass_mcp_server --cov-report=html

# Run specific test file
pytest tests/test_tools.py

# Run with verbose output
pytest -v
```

Or use the Makefile:

```bash
make test              # Run all tests
make test-coverage     # Run tests with coverage report
make test-verbose      # Run tests with verbose output
```

### Test Structure

- `tests/test_tools.py` - Tests for MCP tool definitions and schemas
- `tests/test_commands.py` - Tests for GRASS command execution
- `tests/test_mcp_server.py` - Integration tests for the MCP server
- `tests/conftest.py` - Pytest fixtures and test configuration

See [tests/README.md](tests/README.md) for detailed testing documentation.

## Configuration

### For Claude Desktop

Add this configuration to your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "grass-gis": {
      "command": "python",
      "args": ["/path/to/grass/mcp-server/grass_mcp_server.py"]
    }
  }
}
```

Replace `/path/to/grass` with the actual path to your GRASS repository.

### For Other MCP Clients

Run the server directly:

```bash
python grass_mcp_server.py
```

The server communicates via stdio and follows the MCP protocol specification.

## Usage Examples

### Example 1: Getting Raster Information

```
User: Can you get information about the elevation raster in my GRASS location?

Assistant uses:
- Tool: grass_raster_info
- Arguments:
  - map_name: "elevation"
  - gisdbase: "/home/user/grassdata"
  - location: "nc_spm_08"
  - mapset: "PERMANENT"
```

### Example 2: Calculate Terrain Slope

```
User: Calculate slope from the elevation map and save it as "slope_map"

Assistant uses:
- Tool: grass_slope_aspect
- Arguments:
  - elevation: "elevation"
  - slope: "slope_map"
  - gisdbase: "/home/user/grassdata"
  - location: "nc_spm_08"
```

### Example 3: Buffer Analysis

```
User: Create a 500-meter buffer around the "roads" vector map

Assistant uses:
- Tool: grass_buffer
- Arguments:
  - input_map: "roads"
  - output_map: "roads_buffer_500m"
  - distance: 500
  - gisdbase: "/home/user/grassdata"
  - location: "nc_spm_08"
```

### Example 4: Raster Statistics

```
User: Get detailed statistics for the "landuse" raster

Assistant uses:
- Tool: grass_raster_univar
- Arguments:
  - map_name: "landuse"
  - extended: true
  - gisdbase: "/home/user/grassdata"
  - location: "nc_spm_08"
```

### Example 5: Map Algebra

```
User: Create a new raster that's elevation multiplied by 2

Assistant uses:
- Tool: grass_mapcalc
- Arguments:
  - expression: "elevation_2x = elevation * 2"
  - gisdbase: "/home/user/grassdata"
  - location: "nc_spm_08"
```

### Example 6: Create Visualization ✨ NEW

```
User: Create a visualization of the elevation map and save it to /tmp/elevation.png

Assistant uses:
- Tool: grass_visualize_raster
- Arguments:
  - map_name: "elevation"
  - output_path: "/tmp/elevation.png"
  - width: 800
  - height: 600
  - style: "simple"
  - add_legend: true
  - add_scalebar: true
  - add_north_arrow: true
  - gisdbase: "/home/user/grassdata"
  - location: "nc_spm_08"
```

### Example 7: Create Terrain Visualization ✨ NEW

```
User: Create a hillshade visualization of elevation with terrain colors

Assistant uses:
- Tool: grass_create_composite
- Arguments:
  - base_map: "elevation"
  - output_path: "/tmp/terrain.png"
  - gisdbase: "/home/user/grassdata"
  - location: "nc_spm_08"
```

### Example 8: Interactive Map ✨

```
User: Create an interactive map of the landuse raster that I can open in a browser

Assistant uses:
- Tool: grass_create_interactive_map
- Arguments:
  - map_name: "landuse"
  - output_path: "/tmp/landuse.html"
  - gisdbase: "/home/user/grassdata"
  - location: "nc_spm_08"
```

### Example 9: Watershed Analysis ✨ NEW (Phase 2A)

```
User: Perform watershed analysis on elevation and extract stream networks

Assistant uses:
- Tool: grass_watershed
- Arguments:
  - elevation: "elevation"
  - accumulation: "flow_accum"
  - basin: "watersheds"
  - stream: "streams"
  - threshold: 10000
  - gisdbase: "/home/user/grassdata"
  - location: "nc_spm_08"
```

### Example 10: Viewshed Analysis ✨ NEW (Phase 2A)

```
User: Calculate what's visible from a viewpoint at coordinates 637500,220500

Assistant uses:
- Tool: grass_viewshed
- Arguments:
  - input: "elevation"
  - output: "viewshed"
  - coordinates: "637500,220500"
  - observer_elevation: 2.0
  - max_distance: 5000
  - gisdbase: "/home/user/grassdata"
  - location: "nc_spm_08"
```

### Example 11: Reclassify Terrain ✨ NEW (Phase 2A)

```
User: Reclassify elevation into 3 categories: low (0-100m), medium (100-200m), high (200+m)

Assistant uses:
- Tool: grass_reclass
- Arguments:
  - input: "elevation"
  - output: "elevation_classes"
  - rules: "0:100:1 = Low\n100:200:2 = Medium\n200:*:3 = High"
  - gisdbase: "/home/user/grassdata"
  - location: "nc_spm_08"
```

### Example 12: Generic Command Execution ✨ NEW (Phase 2B)

```
User: Run r.neighbors to smooth the elevation data with a 5x5 window

Assistant uses:
- Tool: grass_execute
- Arguments:
  - command: "r.neighbors"
  - parameters:
      input: "elevation"
      output: "elevation_smoothed"
      size: 5
      method: "average"
  - gisdbase: "/home/user/grassdata"
  - location: "nc_spm_08"
```

This generic wrapper provides access to ALL 500+ GRASS commands!

## GRASS GIS Concepts

### GIS Database Structure

GRASS uses a hierarchical structure:

```
GISDBASE/                (GRASS GIS database directory)
  └── LOCATION/          (Project with consistent coordinate system)
      └── MAPSET/        (Subdirectory containing maps and data)
          ├── raster/    (Raster maps)
          ├── vector/    (Vector maps)
          └── ...
```

- **GISDBASE**: Directory containing all GRASS locations
- **LOCATION**: A project area with a specific coordinate reference system (CRS)
- **MAPSET**: A subdirectory within a location for organizing data (default: PERMANENT)

### Setting Up a GRASS Location

Before using the MCP server, you need a GRASS location with data:

```bash
# Create a new location with WGS84 coordinate system
grass -c EPSG:4326 ~/grassdata/my_location

# Or use an existing sample location
grass ~/grassdata/nc_spm_08/PERMANENT
```

## Available Tools Reference

### Core Tools (8)
| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `grass_raster_info` | Get raster metadata | map_name, gisdbase, location |
| `grass_vector_info` | Get vector metadata | map_name, gisdbase, location |
| `grass_raster_univar` | Calculate raster statistics | map_name, extended |
| `grass_list_maps` | List all maps | map_type (raster/vector/all) |
| `grass_mapcalc` | Raster map algebra | expression |
| `grass_slope_aspect` | Terrain analysis | elevation, slope, aspect |
| `grass_buffer` | Vector buffering | input_map, output_map, distance |
| `grass_region_info` | Get region info | gisdbase, location |

### Visualization Tools (3) - Phase 1
| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `grass_visualize_raster` | Create PNG visualization | map_name, output_path, style |
| `grass_create_composite` | Create hillshade composite | base_map, output_path |
| `grass_create_interactive_map` | Create HTML interactive map | map_name, output_path |

### Advanced Analysis Tools (5) - Phase 2A ✨ NEW
| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `grass_watershed` | Watershed & stream extraction | elevation, basin, stream, threshold |
| `grass_viewshed` | Visibility analysis | input, output, coordinates |
| `grass_reclass` | Reclassify raster values | input, output, rules |
| `grass_overlay` | Vector overlay operations | ainput, binput, output, operator |
| `grass_import_raster` | Import raster with reprojection | input, output, resolution |

### Universal Access (1) - Phase 2B ✨ NEW
| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `grass_execute` | Execute ANY GRASS command | command, parameters, flags |

**Total: 17 tools providing access to 500+ GRASS GIS commands**

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black grass_mcp_server.py
ruff check grass_mcp_server.py
```

## Troubleshooting

### GRASS not found error

If you get "GRASS GIS not found" errors:

1. Ensure GRASS is installed: `grass --version`
2. Check that GRASS is in your PATH
3. Verify the Python grass package is accessible: `python -c "import grass.script"`

### Permission errors

Ensure you have read/write permissions for:
- The GRASS database directory (gisdbase)
- The location and mapset directories
- Any output maps you're creating

### Invalid location/mapset

Verify that:
- The gisdbase path exists and is a valid GRASS database
- The location exists within the gisdbase
- The mapset exists within the location

## Deployment Options

### Docker

**Build and run with Docker:**
```bash
docker build -t grass-mcp-server .
docker run -i grass-mcp-server
```

**Or use Docker Compose:**
```bash
docker-compose up grass-mcp
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed Docker deployment instructions.

### Distribution Methods

- **PyPI**: `pip install grass-mcp-server` (once published)
- **GitHub**: `pip install git+https://github.com/OSGeo/grass.git#subdirectory=mcp-server`
- **Virtual Environment**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **System-wide**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Conda**: See [DEPLOYMENT.md](DEPLOYMENT.md)

For comprehensive deployment instructions including:
- Publishing to PyPI
- OS-specific packages
- CI/CD automation
- Security considerations

See **[DEPLOYMENT.md](DEPLOYMENT.md)**

## Resources

- [GRASS GIS Website](https://grass.osgeo.org/)
- [GRASS GIS Documentation](https://grass.osgeo.org/grass-devel/manuals/)
- [GRASS Python API](https://grass.osgeo.org/grass-devel/manuals/libpython/index.html)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## Documentation

### Core Documentation
- **[README.md](README.md)** - This file, main documentation
- **[USAGE.md](USAGE.md)** - Detailed usage examples and workflows
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Comprehensive deployment guide
- **[TESTING_SUMMARY.md](TESTING_SUMMARY.md)** - Test suite documentation
- **[CHANGELOG.md](CHANGELOG.md)** - Version history
- **[tests/README.md](tests/README.md)** - Testing guide

### Phase 1: Visualization
- **[VISUALIZATION_OPTIONS.md](VISUALIZATION_OPTIONS.md)** - Visualization approaches analysis
- **[VISUALIZATION_RECOMMENDATION.md](VISUALIZATION_RECOMMENDATION.md)** - Implementation guide
- **[VISUALIZATION_TEST_RESULTS.md](VISUALIZATION_TEST_RESULTS.md)** - Test validation results
- **[TESTING_VISUALIZATION.md](TESTING_VISUALIZATION.md)** - Comprehensive testing guide
- **[QUICK_TEST_GUIDE.md](QUICK_TEST_GUIDE.md)** - Quick reference for testing

### Phase 2: Expansion ✨ NEW
- **[EXPANSION_STRATEGY.md](EXPANSION_STRATEGY.md)** - Complete expansion plan (11 → 500+ commands)
- **[EXPANSION_SUMMARY.md](EXPANSION_SUMMARY.md)** - Executive summary and recommendations
- **[PROJECT_DESCRIPTIONS.md](PROJECT_DESCRIPTIONS.md)** - Accurate project descriptions for different contexts

### Installation
- **[INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)** - Local installation instructions
- **[LOCAL_VISUALIZATION_GUIDE.md](LOCAL_VISUALIZATION_GUIDE.md)** - Local vs server visualization

## License

This MCP server follows the GRASS GIS license (GPL-2.0-or-later).

## Contributing

Contributions are welcome! See the main [CONTRIBUTING.md](../CONTRIBUTING.md) file for guidelines.

## Support

For issues specific to this MCP server, please open an issue on the GRASS GIS repository.
For GRASS GIS questions, visit the [GRASS community forums](https://discourse.osgeo.org/c/grass/62).
