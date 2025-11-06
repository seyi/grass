# Claude Desktop Configuration for GRASS GIS MCP Server

## Step 1: Find Your Claude Desktop Config File

The configuration file location depends on your operating system:

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```
Or typically:
```
C:\Users\YourUsername\AppData\Roaming\Claude\claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

## Step 2: Check if the File Exists

### macOS/Linux:
```bash
# Check if file exists
ls -la ~/Library/Application\ Support/Claude/claude_desktop_config.json  # macOS
ls -la ~/.config/Claude/claude_desktop_config.json  # Linux

# If it doesn't exist, create the directory and file
mkdir -p ~/Library/Application\ Support/Claude  # macOS
mkdir -p ~/.config/Claude  # Linux
touch ~/Library/Application\ Support/Claude/claude_desktop_config.json  # macOS
touch ~/.config/Claude/claude_desktop_config.json  # Linux
```

### Windows (PowerShell):
```powershell
# Check if file exists
Test-Path "$env:APPDATA\Claude\claude_desktop_config.json"

# If it doesn't exist, create it
New-Item -ItemType Directory -Force -Path "$env:APPDATA\Claude"
New-Item -ItemType File -Force -Path "$env:APPDATA\Claude\claude_desktop_config.json"
```

## Step 3: Edit the Configuration File

### Option A: If the file is empty or doesn't exist

Add this complete configuration:

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

### Option B: If you already have other MCP servers configured

Add the grass-gis entry to your existing configuration:

```json
{
  "mcpServers": {
    "existing-server": {
      "command": "...",
      "args": ["..."]
    },
    "grass-gis": {
      "command": "python",
      "args": ["-m", "grass_mcp_server"]
    }
  }
}
```

## Step 4: Choose Your Configuration

### Configuration 1: Basic Setup (Recommended)

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

### Configuration 2: With Specific Python Path

If you installed in a virtual environment:

```json
{
  "mcpServers": {
    "grass-gis": {
      "command": "/full/path/to/venv/bin/python",
      "args": ["-m", "grass_mcp_server"]
    }
  }
}
```

**Find your Python path:**
```bash
# macOS/Linux
which python

# Windows (PowerShell)
(Get-Command python).Path
```

### Configuration 3: With Environment Variables

```json
{
  "mcpServers": {
    "grass-gis": {
      "command": "python",
      "args": ["-m", "grass_mcp_server"],
      "env": {
        "GRASS_VERBOSE": "0",
        "GISDBASE": "/path/to/your/grassdata"
      }
    }
  }
}
```

### Configuration 4: Using python3 explicitly

```json
{
  "mcpServers": {
    "grass-gis": {
      "command": "python3",
      "args": ["-m", "grass_mcp_server"]
    }
  }
}
```

### Configuration 5: With Direct Script Path

If you want to specify the script directly:

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

## Step 5: Verify Your Installation

Before configuring Claude, verify the installation works:

```bash
# Test Python can import the module
python -c "import grass_mcp_server; print('✓ OK')"

# Test the module runs
python -m grass_mcp_server --help
```

## Step 6: Quick Copy-Paste Configurations

### For macOS:

```bash
# Open config file in default editor
open ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Or use nano
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Or use VS Code
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

Paste this:
```json
{
  "mcpServers": {
    "grass-gis": {
      "command": "python3",
      "args": ["-m", "grass_mcp_server"]
    }
  }
}
```

### For Windows:

```powershell
# Open in Notepad
notepad "$env:APPDATA\Claude\claude_desktop_config.json"

# Or use VS Code
code "$env:APPDATA\Claude\claude_desktop_config.json"
```

Paste this:
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

### For Linux:

```bash
# Open in default text editor
xdg-open ~/.config/Claude/claude_desktop_config.json

# Or use nano
nano ~/.config/Claude/claude_desktop_config.json

# Or use VS Code
code ~/.config/Claude/claude_desktop_config.json
```

Paste this:
```json
{
  "mcpServers": {
    "grass-gis": {
      "command": "python3",
      "args": ["-m", "grass_mcp_server"]
    }
  }
}
```

## Step 7: Validate JSON Syntax

Before saving, validate your JSON:

1. Copy your configuration
2. Go to https://jsonlint.com/
3. Paste and validate
4. Fix any errors

Common mistakes:
- ❌ Missing commas between entries
- ❌ Extra comma after last entry
- ❌ Unmatched quotes or brackets
- ❌ Using single quotes instead of double quotes

## Step 8: Restart Claude Desktop

**Important:** You MUST completely quit and restart Claude Desktop for changes to take effect.

### macOS:
- Quit: `Cmd + Q` or Claude menu → Quit Claude
- Don't just close the window!

### Windows:
- Right-click Claude in system tray → Exit
- Or use Task Manager to ensure it's closed

### Linux:
- Quit the application completely
- Check with: `ps aux | grep -i claude`

## Step 9: Verify the Connection

After restarting Claude Desktop:

1. **Open Claude Desktop**

2. **Look for the MCP server in settings:**
   - Go to Settings (gear icon)
   - Look for MCP or Developer section
   - You should see "grass-gis" listed

3. **Test with a query:**

   In Claude Desktop, ask:
   ```
   "What MCP servers are connected?"
   ```

   You should see `grass-gis` in the list.

4. **Test the tools:**

   Ask Claude:
   ```
   "What GRASS GIS tools are available?"
   ```

   You should see 8 tools listed:
   - grass_raster_info
   - grass_vector_info
   - grass_raster_univar
   - grass_list_maps
   - grass_mapcalc
   - grass_slope_aspect
   - grass_buffer
   - grass_region_info

## Troubleshooting

### Problem 1: "Server not detected"

**Check:**
```bash
# Verify installation
python -c "import grass_mcp_server; print('OK')"

# Check which python Claude is using
which python
which python3
```

**Solution:** Update config to use the correct Python path:
```json
{
  "mcpServers": {
    "grass-gis": {
      "command": "/usr/local/bin/python3",
      "args": ["-m", "grass_mcp_server"]
    }
  }
}
```

### Problem 2: "Module not found"

**Check:**
```bash
python -m grass_mcp_server
```

**If it fails:**
```bash
# Reinstall
pip install --force-reinstall git+https://github.com/seyi/grass.git@claude/create-geospatial-mcp-grass-011CUr9bMgUcm9QX2hz9KwdX#subdirectory=mcp-server
```

### Problem 3: "JSON syntax error"

**Validate at:** https://jsonlint.com/

**Common fixes:**
```json
// ❌ Wrong - single quotes
{
  'mcpServers': {
    'grass-gis': {}
  }
}

// ✅ Correct - double quotes
{
  "mcpServers": {
    "grass-gis": {}
  }
}

// ❌ Wrong - trailing comma
{
  "mcpServers": {
    "grass-gis": {},
  }
}

// ✅ Correct - no trailing comma
{
  "mcpServers": {
    "grass-gis": {}
  }
}
```

### Problem 4: "Changes not taking effect"

1. **Completely quit Claude Desktop** (not just close window)
2. **Wait 5 seconds**
3. **Restart Claude Desktop**
4. **Check Claude logs** (if available in settings)

### Problem 5: "Permission denied"

**On macOS/Linux:**
```bash
# Make sure you have write permissions
ls -la ~/Library/Application\ Support/Claude/  # macOS
ls -la ~/.config/Claude/  # Linux

# Fix permissions if needed
chmod 644 ~/Library/Application\ Support/Claude/claude_desktop_config.json  # macOS
chmod 644 ~/.config/Claude/claude_desktop_config.json  # Linux
```

## Complete Working Example

Here's a complete, tested configuration:

```json
{
  "mcpServers": {
    "grass-gis": {
      "command": "python3",
      "args": ["-m", "grass_mcp_server"],
      "env": {
        "GRASS_VERBOSE": "0"
      }
    }
  }
}
```

## Quick Setup Script

### macOS/Linux:

```bash
#!/bin/bash
# Quick setup for Claude Desktop

# Determine OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    CONFIG_DIR="$HOME/Library/Application Support/Claude"
else
    CONFIG_DIR="$HOME/.config/Claude"
fi

CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"

# Create directory if needed
mkdir -p "$CONFIG_DIR"

# Create or update config
cat > "$CONFIG_FILE" << 'EOF'
{
  "mcpServers": {
    "grass-gis": {
      "command": "python3",
      "args": ["-m", "grass_mcp_server"]
    }
  }
}
EOF

echo "✓ Configuration created at: $CONFIG_FILE"
echo ""
echo "Next steps:"
echo "1. Restart Claude Desktop completely (Cmd+Q or Quit)"
echo "2. Open Claude Desktop"
echo "3. Ask: 'What GRASS GIS tools are available?'"
```

Save as `setup-claude-config.sh`, make executable, and run:
```bash
chmod +x setup-claude-config.sh
./setup-claude-config.sh
```

### Windows (PowerShell):

```powershell
# Quick setup for Claude Desktop on Windows

$configDir = "$env:APPDATA\Claude"
$configFile = "$configDir\claude_desktop_config.json"

# Create directory if needed
New-Item -ItemType Directory -Force -Path $configDir | Out-Null

# Create configuration
$config = @"
{
  "mcpServers": {
    "grass-gis": {
      "command": "python",
      "args": ["-m", "grass_mcp_server"]
    }
  }
}
"@

Set-Content -Path $configFile -Value $config

Write-Host "✓ Configuration created at: $configFile" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Completely quit Claude Desktop (right-click tray icon → Exit)"
Write-Host "2. Restart Claude Desktop"
Write-Host "3. Ask: 'What GRASS GIS tools are available?'"
```

Save as `setup-claude-config.ps1` and run:
```powershell
powershell -ExecutionPolicy Bypass -File setup-claude-config.ps1
```

## Success Checklist

- [ ] Found Claude Desktop config file location
- [ ] Created/edited config file
- [ ] Added grass-gis MCP server entry
- [ ] Validated JSON syntax
- [ ] Completely quit Claude Desktop
- [ ] Restarted Claude Desktop
- [ ] Server appears in Claude settings
- [ ] Can list GRASS GIS tools
- [ ] Tools respond correctly

## What to Test

Once configured, try these queries in Claude Desktop:

1. **List tools:**
   ```
   "What GRASS GIS tools are available?"
   ```

2. **Get tool info:**
   ```
   "Tell me about the grass_raster_info tool"
   ```

3. **Test without data:**
   ```
   "Explain what the GRASS GIS MCP server can do for geospatial analysis"
   ```

4. **With GRASS data (if you have it):**
   ```
   "List raster maps in my GRASS location at /path/to/grassdata/location"
   ```

## Need More Help?

- 📖 See [QUICKSTART.md](QUICKSTART.md) for detailed troubleshooting
- 🐛 Report issues: https://github.com/seyi/grass/issues
- 💬 Check Claude Desktop documentation for MCP setup

---

**You're all set!** Once Claude Desktop is restarted, you should see the GRASS GIS tools available. 🎉
