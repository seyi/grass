# Test Installation Script for Windows
# Run with: powershell -ExecutionPolicy Bypass -File test-installation.ps1

$ErrorActionPreference = "Continue"

Write-Host "======================================" -ForegroundColor Blue
Write-Host "GRASS GIS MCP Server - Quick Test" -ForegroundColor Blue
Write-Host "======================================" -ForegroundColor Blue
Write-Host ""

$TestsPassed = 0
$TestsFailed = 0

# Test 1: Python version
Write-Host "1. Checking Python version..."
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match 'Python (\d+)\.(\d+)') {
        $major = [int]$matches[1]
        $minor = [int]$matches[2]

        if (($major -ge 3) -and ($minor -ge 10)) {
            Write-Host "   ✓ Python $major.$minor (OK)" -ForegroundColor Green
            $TestsPassed++
        } else {
            Write-Host "   ✗ Python $major.$minor (Need 3.10+)" -ForegroundColor Red
            $TestsFailed++
        }
    }
} catch {
    Write-Host "   ✗ Python not found" -ForegroundColor Red
    $TestsFailed++
}

# Test 2: Module import
Write-Host ""
Write-Host "2. Testing module import..."
try {
    python -c "import grass_mcp_server" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✓ Import grass_mcp_server - PASS" -ForegroundColor Green
        $TestsPassed++
    } else {
        throw "Import failed"
    }
} catch {
    Write-Host "   ✗ Import grass_mcp_server - FAIL" -ForegroundColor Red
    $TestsFailed++
}

# Test 3: MCP dependency
Write-Host ""
Write-Host "3. Testing MCP dependency..."
try {
    python -c "import mcp" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✓ Import mcp module - PASS" -ForegroundColor Green
        $TestsPassed++
    } else {
        throw "Import failed"
    }
} catch {
    Write-Host "   ✗ Import mcp module - FAIL" -ForegroundColor Red
    $TestsFailed++
}

# Test 4: Server initialization
Write-Host ""
Write-Host "4. Testing server initialization..."
try {
    python -c "import grass_mcp_server; assert grass_mcp_server.app is not None" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✓ Server object creation - PASS" -ForegroundColor Green
        $TestsPassed++
    } else {
        throw "Server init failed"
    }
} catch {
    Write-Host "   ✗ Server object creation - FAIL" -ForegroundColor Red
    $TestsFailed++
}

# Test 5: List tools
Write-Host ""
Write-Host "5. Testing tool listing..."
$toolTest = @"
import asyncio
import grass_mcp_server

async def test():
    tools = await grass_mcp_server.list_tools()
    assert len(tools) == 8, f'Expected 8 tools, got {len(tools)}'
    print('Found', len(tools), 'tools')
    for tool in tools:
        print(f'  - {tool.name}')

asyncio.run(test())
"@

try {
    $output = python -c $toolTest 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✓ Tool listing works - PASS" -ForegroundColor Green
        Write-Host $output
        $TestsPassed++
    } else {
        throw "Tool listing failed"
    }
} catch {
    Write-Host "   ✗ Tool listing - FAIL" -ForegroundColor Red
    $TestsFailed++
}

# Test 6: GRASS GIS (optional)
Write-Host ""
Write-Host "6. Checking for GRASS GIS (optional)..."
try {
    $grassVersion = grass --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✓ GRASS GIS found" -ForegroundColor Green
        $TestsPassed++
    }
} catch {
    Write-Host "   ⚠ GRASS GIS not found (optional)" -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "======================================" -ForegroundColor Blue
Write-Host "Test Summary" -ForegroundColor Blue
Write-Host "======================================" -ForegroundColor Blue
Write-Host "Passed: $TestsPassed" -ForegroundColor Green
Write-Host "Failed: $TestsFailed" -ForegroundColor Red
Write-Host ""

if ($TestsFailed -eq 0) {
    Write-Host "✓ All tests passed!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:"
    Write-Host "1. Configure Claude Desktop (see QUICKSTART.md)"
    Write-Host "2. Restart Claude Desktop"
    Write-Host "3. Ask Claude: 'List GRASS GIS tools'"
    exit 0
} else {
    Write-Host "✗ Some tests failed" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please check:"
    Write-Host "1. Python version >= 3.10"
    Write-Host "2. All dependencies installed"
    Write-Host "3. No import errors"
    Write-Host ""
    Write-Host "For help, see QUICKSTART.md or open an issue"
    exit 1
}
