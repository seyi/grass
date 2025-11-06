# GRASS GIS MCP Server Installation Script for Windows
# Run with: powershell -ExecutionPolicy Bypass -File install.ps1

$ErrorActionPreference = "Stop"

Write-Host "========================================"  -ForegroundColor Blue
Write-Host "GRASS GIS MCP Server Installation" -ForegroundColor Blue
Write-Host "========================================" -ForegroundColor Blue
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }

    $versionMatch = $pythonVersion -match 'Python (\d+)\.(\d+)'
    if ($versionMatch) {
        $major = [int]$matches[1]
        $minor = [int]$matches[2]

        if (($major -lt 3) -or (($major -eq 3) -and ($minor -lt 10))) {
            Write-Host "Error: Python 3.10+ required, found $pythonVersion" -ForegroundColor Red
            exit 1
        }
        Write-Host "✓ $pythonVersion found" -ForegroundColor Green
    }
} catch {
    Write-Host "Error: Python 3 is not installed" -ForegroundColor Red
    Write-Host "Please install Python 3.10 or higher from https://www.python.org/downloads/"
    exit 1
}

# Check if GRASS GIS is installed
Write-Host ""
Write-Host "Checking for GRASS GIS..." -ForegroundColor Yellow
try {
    $grassVersion = grass --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ GRASS GIS found" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠ GRASS GIS not found" -ForegroundColor Yellow
    Write-Host "The MCP server will work, but you'll need GRASS installed to use it."
    Write-Host "Download from: https://grass.osgeo.org/download/windows/"
}

# Installation method selection
Write-Host ""
Write-Host "Select installation method:"
Write-Host "  1) Install from source (current directory)"
Write-Host "  2) Install from GitHub (latest)"
Write-Host "  3) Install in development mode (editable)"
Write-Host "  4) Create virtual environment and install"
$choice = Read-Host "Enter choice [1-4]"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "Installing from source..." -ForegroundColor Yellow
        pip install .
    }
    "2" {
        Write-Host ""
        Write-Host "Installing from GitHub..." -ForegroundColor Yellow
        pip install git+https://github.com/OSGeo/grass.git#subdirectory=mcp-server
    }
    "3" {
        Write-Host ""
        Write-Host "Installing in development mode..." -ForegroundColor Yellow
        pip install -e ".[dev]"
    }
    "4" {
        Write-Host ""
        Write-Host "Creating virtual environment..." -ForegroundColor Yellow
        python -m venv grass-mcp-env
        & .\grass-mcp-env\Scripts\Activate.ps1
        Write-Host "✓ Virtual environment created and activated" -ForegroundColor Green
        Write-Host "Installing package..." -ForegroundColor Yellow
        pip install .
        $venvPath = Join-Path (Get-Location) "grass-mcp-env"
        Write-Host "✓ Installed in virtual environment" -ForegroundColor Green
        Write-Host ""
        Write-Host "To use this environment:" -ForegroundColor Blue
        Write-Host "  .\grass-mcp-env\Scripts\Activate.ps1"
    }
    default {
        Write-Host "Invalid choice" -ForegroundColor Red
        exit 1
    }
}

# Verify installation
Write-Host ""
Write-Host "Verifying installation..." -ForegroundColor Yellow
try {
    python -c "import grass_mcp_server" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Installation successful!" -ForegroundColor Green
    } else {
        throw "Import failed"
    }
} catch {
    Write-Host "✗ Installation verification failed" -ForegroundColor Red
    exit 1
}

# Show configuration instructions
Write-Host ""
Write-Host "========================================" -ForegroundColor Blue
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Blue
Write-Host ""
Write-Host "Next steps:"
Write-Host ""
Write-Host "1. Configure Claude Desktop:"
Write-Host "   Edit your Claude Desktop config file:"
$configPath = "$env:APPDATA\Claude\claude_desktop_config.json"
Write-Host "   Location: $configPath"
Write-Host ""
Write-Host "   Add this configuration:"
Write-Host '   {'
Write-Host '     "mcpServers": {'
Write-Host '       "grass-gis": {'
if ($choice -eq "4") {
    Write-Host "         `"command`": `"$venvPath\Scripts\python.exe`","
    Write-Host '         "args": ["-m", "grass_mcp_server"]'
} else {
    Write-Host '         "command": "python",'
    Write-Host '         "args": ["-m", "grass_mcp_server"]'
}
Write-Host '       }'
Write-Host '     }'
Write-Host '   }'
Write-Host ""
Write-Host "2. Restart Claude Desktop"
Write-Host ""
Write-Host "3. Test the server with a query like:"
Write-Host '   "List available tools from the GRASS GIS MCP server"'
Write-Host ""
Write-Host "For more information:"
Write-Host "  - README.md - Main documentation"
Write-Host "  - USAGE.md - Usage examples"
Write-Host "  - DEPLOYMENT.md - Deployment guide"
Write-Host ""
Write-Host "Happy geospatial computing! 🌍" -ForegroundColor Green
