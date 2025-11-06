#!/bin/bash
# Quick Test Script for GRASS GIS MCP Server
# This script tests the basic functionality of the MCP server

set -e

echo "======================================"
echo "GRASS GIS MCP Server - Quick Test"
echo "======================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run test
run_test() {
    local test_name="$1"
    local test_command="$2"

    echo -n "Testing: $test_name... "

    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Test 1: Python version
echo "1. Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 10 ]; then
    echo -e "   ${GREEN}✓${NC} Python $PYTHON_VERSION (OK)"
    ((TESTS_PASSED++))
else
    echo -e "   ${RED}✗${NC} Python $PYTHON_VERSION (Need 3.10+)"
    ((TESTS_FAILED++))
fi

# Test 2: Module import
echo ""
echo "2. Testing module import..."
run_test "Import grass_mcp_server" "python3 -c 'import grass_mcp_server'"

# Test 3: MCP dependency
echo ""
echo "3. Testing MCP dependency..."
run_test "Import mcp module" "python3 -c 'import mcp'"

# Test 4: Server initialization
echo ""
echo "4. Testing server initialization..."
run_test "Server object creation" "python3 -c 'import grass_mcp_server; assert grass_mcp_server.app is not None'"

# Test 5: List tools
echo ""
echo "5. Testing tool listing..."
if python3 -c "
import asyncio
import grass_mcp_server

async def test():
    tools = await grass_mcp_server.list_tools()
    assert len(tools) == 8, f'Expected 8 tools, got {len(tools)}'
    print('Found', len(tools), 'tools')
    for tool in tools:
        print(f'  - {tool.name}')

asyncio.run(test())
" 2>&1; then
    echo -e "   ${GREEN}✓${NC} Tool listing works"
    ((TESTS_PASSED++))
else
    echo -e "   ${RED}✗${NC} Tool listing failed"
    ((TESTS_FAILED++))
fi

# Test 6: GRASS GIS (optional)
echo ""
echo "6. Checking for GRASS GIS (optional)..."
if command -v grass &> /dev/null; then
    GRASS_VERSION=$(grass --version 2>&1 | head -n1)
    echo -e "   ${GREEN}✓${NC} $GRASS_VERSION found"
    ((TESTS_PASSED++))
else
    echo -e "   ${YELLOW}⚠${NC} GRASS GIS not found (optional, but needed for full functionality)"
fi

# Test 7: Run basic tool test
echo ""
echo "7. Testing tool execution (mock)..."
if python3 -c "
import asyncio
from unittest.mock import Mock, patch
import grass_mcp_server

async def test():
    with patch('grass_mcp_server.run_grass_command') as mock_run:
        mock_run.return_value = 'north=100\nsouth=0'
        result = await grass_mcp_server.call_tool(
            'grass_raster_info',
            {
                'map_name': 'test',
                'gisdbase': '/tmp',
                'location': 'test'
            }
        )
        assert len(result) > 0
        print('Tool execution successful')

asyncio.run(test())
" 2>&1; then
    echo -e "   ${GREEN}✓${NC} Tool execution works"
    ((TESTS_PASSED++))
else
    echo -e "   ${RED}✗${NC} Tool execution failed"
    ((TESTS_FAILED++))
fi

# Summary
echo ""
echo "======================================"
echo "Test Summary"
echo "======================================"
echo -e "Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Configure Claude Desktop (see QUICKSTART.md)"
    echo "2. Restart Claude Desktop"
    echo "3. Ask Claude: 'List GRASS GIS tools'"
    exit 0
else
    echo -e "${RED}✗ Some tests failed${NC}"
    echo ""
    echo "Please check:"
    echo "1. Python version >= 3.10"
    echo "2. All dependencies installed"
    echo "3. No import errors"
    echo ""
    echo "For help, see QUICKSTART.md or open an issue"
    exit 1
fi
