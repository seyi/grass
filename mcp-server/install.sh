#!/bin/bash
# GRASS GIS MCP Server Installation Script

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}GRASS GIS MCP Server Installation${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    echo "Please install Python 3.10 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
PYTHON_MAJOR=$(python3 -c 'import sys; print(sys.version_info.major)')
PYTHON_MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)')

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
    echo -e "${RED}Error: Python 3.10+ required, found $PYTHON_VERSION${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"

# Check if GRASS GIS is installed (optional but recommended)
echo ""
echo -e "${YELLOW}Checking for GRASS GIS...${NC}"
if command -v grass &> /dev/null; then
    GRASS_VERSION=$(grass --version 2>&1 | head -n1)
    echo -e "${GREEN}✓ $GRASS_VERSION found${NC}"
else
    echo -e "${YELLOW}⚠ GRASS GIS not found${NC}"
    echo "The MCP server will work, but you'll need GRASS installed to use it."
    echo "Install instructions:"
    echo "  - Ubuntu/Debian: sudo apt-get install grass"
    echo "  - macOS: brew install grass"
    echo "  - Windows: https://grass.osgeo.org/download/"
fi

# Determine installation method
echo ""
echo "Select installation method:"
echo "  1) Install from source (current directory)"
echo "  2) Install from GitHub (latest)"
echo "  3) Install in development mode (editable)"
echo "  4) Create virtual environment and install"
read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        echo ""
        echo -e "${YELLOW}Installing from source...${NC}"
        pip3 install .
        ;;
    2)
        echo ""
        echo -e "${YELLOW}Installing from GitHub...${NC}"
        pip3 install git+https://github.com/OSGeo/grass.git#subdirectory=mcp-server
        ;;
    3)
        echo ""
        echo -e "${YELLOW}Installing in development mode...${NC}"
        pip3 install -e ".[dev]"
        ;;
    4)
        echo ""
        echo -e "${YELLOW}Creating virtual environment...${NC}"
        python3 -m venv grass-mcp-env
        source grass-mcp-env/bin/activate
        echo -e "${GREEN}✓ Virtual environment created and activated${NC}"
        echo -e "${YELLOW}Installing package...${NC}"
        pip install .
        VENV_PATH=$(pwd)/grass-mcp-env
        echo -e "${GREEN}✓ Installed in virtual environment${NC}"
        echo ""
        echo -e "${BLUE}To use this environment:${NC}"
        echo "  source $VENV_PATH/bin/activate"
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

# Verify installation
echo ""
echo -e "${YELLOW}Verifying installation...${NC}"
if python3 -c "import grass_mcp_server" 2>/dev/null; then
    echo -e "${GREEN}✓ Installation successful!${NC}"
else
    echo -e "${RED}✗ Installation verification failed${NC}"
    exit 1
fi

# Show configuration instructions
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Installation Complete!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "Next steps:"
echo ""
echo "1. Configure Claude Desktop:"
echo "   Edit your Claude Desktop config file:"
if [[ "$OSTYPE" == "darwin"* ]]; then
    CONFIG_PATH="~/Library/Application Support/Claude/claude_desktop_config.json"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    CONFIG_PATH="~/.config/Claude/claude_desktop_config.json"
else
    CONFIG_PATH="%APPDATA%\\Claude\\claude_desktop_config.json"
fi
echo "   Location: $CONFIG_PATH"
echo ""
echo "   Add this configuration:"
echo '   {'
echo '     "mcpServers": {'
echo '       "grass-gis": {'
if [ $choice -eq 4 ]; then
    echo "         \"command\": \"$VENV_PATH/bin/python\","
    echo '         "args": ["-m", "grass_mcp_server"]'
else
    echo '         "command": "python3",'
    echo '         "args": ["-m", "grass_mcp_server"]'
fi
echo '       }'
echo '     }'
echo '   }'
echo ""
echo "2. Restart Claude Desktop"
echo ""
echo "3. Test the server with a query like:"
echo '   "List available tools from the GRASS GIS MCP server"'
echo ""
echo "For more information:"
echo "  - README.md - Main documentation"
echo "  - USAGE.md - Usage examples"
echo "  - DEPLOYMENT.md - Deployment guide"
echo ""
echo -e "${GREEN}Happy geospatial computing! 🌍${NC}"
