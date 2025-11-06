# Quick Start for Testers

Welcome! Thank you for testing the GRASS GIS MCP Server. This guide will get you up and running in minutes.

## 🚀 One-Line Installation

**Copy and paste this command:**

```bash
pip install git+https://github.com/seyi/grass.git@claude/create-geospatial-mcp-grass-011CUr9bMgUcm9QX2hz9KwdX#subdirectory=mcp-server
```

Or use the automated installer:

```bash
# Linux/macOS
curl -sSL https://raw.githubusercontent.com/seyi/grass/claude/create-geospatial-mcp-grass-011CUr9bMgUcm9QX2hz9KwdX/mcp-server/install.sh | bash

# Or download and run
wget https://raw.githubusercontent.com/seyi/grass/claude/create-geospatial-mcp-grass-011CUr9bMgUcm9QX2hz9KwdX/mcp-server/install.sh
chmod +x install.sh
./install.sh
```

**Windows (PowerShell):**
```powershell
# Download installer
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/seyi/grass/claude/create-geospatial-mcp-grass-011CUr9bMgUcm9QX2hz9KwdX/mcp-server/install.ps1" -OutFile "install.ps1"

# Run installer
powershell -ExecutionPolicy Bypass -File install.ps1
```

---

## ✅ Prerequisites

- **Python 3.10+** (Required)
- **GRASS GIS** (Optional - for actually using the tools)

**Check Python version:**
```bash
python --version  # Should be 3.10 or higher
```

**Install GRASS GIS (recommended):**
- **Ubuntu/Debian:** `sudo apt-get install grass`
- **macOS:** `brew install grass`
- **Windows:** [Download from GRASS GIS](https://grass.osgeo.org/download/)

---

## 📦 Installation Options

### Option 1: Quick Install (Recommended for Testing)

```bash
pip install git+https://github.com/seyi/grass.git@claude/create-geospatial-mcp-grass-011CUr9bMgUcm9QX2hz9KwdX#subdirectory=mcp-server
```

### Option 2: Clone and Install

```bash
# Clone the repository
git clone https://github.com/seyi/grass.git
cd grass
git checkout claude/create-geospatial-mcp-grass-011CUr9bMgUcm9QX2hz9KwdX
cd mcp-server

# Install
pip install .
```

### Option 3: Virtual Environment (Cleanest)

```bash
# Create virtual environment
python -m venv grass-test-env
source grass-test-env/bin/activate  # Windows: grass-test-env\Scripts\activate

# Install
pip install git+https://github.com/seyi/grass.git@claude/create-geospatial-mcp-grass-011CUr9bMgUcm9QX2hz9KwdX#subdirectory=mcp-server
```

### Option 4: Docker (No Python Setup Needed)

```bash
# Clone repository
git clone https://github.com/seyi/grass.git
cd grass/mcp-server
git checkout claude/create-geospatial-mcp-grass-011CUr9bMgUcm9QX2hz9KwdX

# Build and run
docker build -t grass-mcp-test .
docker run -i grass-mcp-test
```

---

## 🔧 Configure Claude Desktop

1. **Verify installation:**
   ```bash
   python -c "import grass_mcp_server; print('✓ Installation successful!')"
   ```

2. **Find your Claude Desktop config file:**
   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux:** `~/.config/Claude/claude_desktop_config.json`

3. **Add this configuration:**
   ```json
   {
     "mcpServers": {
       "grass-gis-test": {
         "command": "python",
         "args": ["-m", "grass_mcp_server"]
       }
     }
   }
   ```

4. **Restart Claude Desktop**

---

## 🧪 Test the Server

### Quick Test 1: List Available Tools

In Claude Desktop, ask:
```
"What tools are available from the grass-gis-test MCP server?"
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

### Quick Test 2: Test Without GRASS Data

```
"Tell me about the GRASS GIS MCP tools and what they can do"
```

The server should respond with descriptions of available geospatial operations.

### Quick Test 3: With GRASS Data (If You Have It)

If you have GRASS GIS installed with sample data:

```
"List all raster maps in my GRASS location at /path/to/grassdata/location"
```

Replace `/path/to/grassdata/location` with your actual GRASS database path.

---

## 📋 What to Test

Please test the following and report any issues:

### Installation Testing
- [ ] Installation completes without errors
- [ ] `import grass_mcp_server` works
- [ ] Version information is accessible

### Configuration Testing
- [ ] Claude Desktop detects the MCP server
- [ ] Server appears in Claude Desktop settings
- [ ] No connection errors in Claude logs

### Functionality Testing
- [ ] Can list available tools
- [ ] Tool descriptions are clear
- [ ] Error messages are helpful

### With GRASS GIS Installed (Optional)
- [ ] Can query raster information
- [ ] Can query vector information
- [ ] Can list maps
- [ ] Can get region information

### Platform Testing
Please indicate your platform:
- [ ] Linux (which distribution?)
- [ ] macOS (which version?)
- [ ] Windows (which version?)

---

## 🐛 Reporting Issues

If you encounter any problems, please provide:

1. **Your Environment:**
   - Operating System & Version
   - Python Version (`python --version`)
   - GRASS GIS Version (`grass --version`) if installed
   - Installation method used

2. **What Happened:**
   - Command you ran
   - Error message (full text)
   - Screenshot (if relevant)

3. **Expected Behavior:**
   - What you expected to happen

**Report issues:**
- Create an issue at: https://github.com/seyi/grass/issues
- Include label: `mcp-server-test`
- Use the provided issue template

Or provide feedback directly to the repository maintainer.

---

## 💬 Providing Feedback

We'd love to hear:

### Installation Experience
- Was installation easy?
- Did instructions work?
- Any confusing steps?

### Documentation
- Is documentation clear?
- Missing information?
- Confusing explanations?

### Features
- Which tools did you use?
- What worked well?
- What didn't work?

### Suggestions
- Missing features?
- Improvement ideas?
- Use case scenarios?

**Feedback form:** [Create an issue](https://github.com/seyi/grass/issues/new) with label `feedback`

---

## 🔄 Updating the Test Version

To get the latest test version:

```bash
pip install --upgrade --force-reinstall git+https://github.com/seyi/grass.git@claude/create-geospatial-mcp-grass-011CUr9bMgUcm9QX2hz9KwdX#subdirectory=mcp-server
```

---

## 🆘 Troubleshooting

### "Module not found" Error

```bash
# Ensure pip install completed
pip list | grep grass-mcp-server

# Try reinstalling
pip install --force-reinstall git+https://github.com/seyi/grass.git@claude/create-geospatial-mcp-grass-011CUr9bMgUcm9QX2hz9KwdX#subdirectory=mcp-server
```

### "GRASS GIS not found" Warning

This is OK! The server will work, but you'll need GRASS GIS installed to actually process geospatial data. You can still:
- List available tools
- See tool descriptions
- Test the MCP protocol integration

### Claude Desktop Not Detecting Server

1. Check config file location
2. Verify JSON syntax (use https://jsonlint.com/)
3. Restart Claude Desktop completely (quit and reopen)
4. Check Claude Desktop logs for errors

### Permission Errors

```bash
# Don't use sudo with pip
# Instead, use virtual environment:
python -m venv test-env
source test-env/bin/activate
pip install git+...
```

---

## 📚 Additional Resources

- **Full Documentation:** See [README.md](README.md)
- **Usage Examples:** See [USAGE.md](USAGE.md)
- **Deployment Options:** See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Test Suite:** See [TESTING_SUMMARY.md](TESTING_SUMMARY.md)

---

## 🙏 Thank You!

Your testing and feedback are invaluable in making this MCP server better for everyone. Thank you for participating!

**Questions?** Open an issue or reach out to the repository maintainer.

---

## Test Version Information

- **Branch:** `claude/create-geospatial-mcp-grass-011CUr9bMgUcm9QX2hz9KwdX`
- **Version:** 0.1.0 (Beta)
- **Status:** Testing Phase
- **Repository:** https://github.com/seyi/grass

**Note:** This is a test version. Features and APIs may change based on feedback.
