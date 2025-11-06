#!/bin/bash
# Demo: Testing the GRASS GIS MCP Server

echo "=========================================="
echo "GRASS GIS MCP Server - Interactive Demo"
echo "=========================================="
echo ""

# Check if GRASS is installed
echo "1. Checking for GRASS GIS installation..."
if command -v grass &> /dev/null; then
    echo "   ✓ GRASS GIS is installed"
    grass --version
else
    echo "   ✗ GRASS GIS is not installed"
    echo ""
    echo "   To install:"
    echo "   - Ubuntu/Debian: sudo apt-get install grass"
    echo "   - macOS: brew install grass"
    echo "   - Windows: Download from https://grass.osgeo.org/download/"
    echo ""
    echo "   You can still test the MCP server with mocked data!"
fi
echo ""

# Check if Python is available
echo "2. Checking Python installation..."
if command -v python3 &> /dev/null; then
    echo "   ✓ Python is installed"
    python3 --version
else
    echo "   ✗ Python3 is required"
    exit 1
fi
echo ""

# Check if the MCP server is installed
echo "3. Checking MCP server installation..."
if python3 -c "import grass_mcp_server" 2>/dev/null; then
    echo "   ✓ MCP server module is installed"
else
    echo "   ✗ MCP server not installed"
    echo "   Installing..."
    pip install -e .
fi
echo ""

# Run the demo script
echo "4. Running demonstration..."
echo ""
python3 demo_list_maps.py
echo ""

# Show how to run tests
echo "=========================================="
echo "Running Test Suite"
echo "=========================================="
echo ""
echo "Running MCP server tests..."
python3 -m pytest tests/ -v --tb=short || echo "Some tests may require GRASS GIS installation"
echo ""

echo "=========================================="
echo "Next Steps"
echo "=========================================="
echo ""
echo "To use with Claude Desktop:"
echo ""
echo "1. Add this to your Claude Desktop config:"
echo "   File: ~/Library/Application Support/Claude/claude_desktop_config.json (macOS)"
echo "   File: %APPDATA%\\Claude\\claude_desktop_config.json (Windows)"
echo "   File: ~/.config/Claude/claude_desktop_config.json (Linux)"
echo ""
echo '   {'
echo '     "mcpServers": {'
echo '       "grass-gis": {'
echo '         "command": "python",'
echo '         "args": ["-m", "grass_mcp_server"]'
echo '       }'
echo '     }'
echo '   }'
echo ""
echo "2. Restart Claude Desktop"
echo ""
echo "3. Ask Claude:"
echo '   "What GRASS GIS tools are available?"'
echo '   "List all raster maps in my location"'
echo '   "Calculate slope from elevation map"'
echo ""
echo "=========================================="
