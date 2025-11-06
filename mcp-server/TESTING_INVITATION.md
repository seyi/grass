# 🧪 Help Test the GRASS GIS MCP Server!

Thank you for your interest in testing the GRASS GIS MCP Server - a new way to use GRASS GIS geospatial analysis tools with AI assistants like Claude!

## What is This?

The GRASS GIS MCP Server exposes powerful geospatial processing capabilities through the Model Context Protocol (MCP), allowing AI assistants to help you with:

- 🗺️ **Raster analysis** - DEM processing, terrain analysis, map algebra
- 📍 **Vector operations** - Buffer analysis, spatial queries
- 📊 **Statistical analysis** - Univariate statistics, data summaries
- 🌍 **Geospatial workflows** - Complete GIS analysis pipelines

## 🚀 Quick Install (2 minutes)

**Just run this one command:**

```bash
pip install git+https://github.com/seyi/grass.git@claude/create-geospatial-mcp-grass-011CUr9bMgUcm9QX2hz9KwdX#subdirectory=mcp-server
```

**Then configure Claude Desktop** (add to config file):

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

**Config file locations:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

Restart Claude Desktop and you're ready!

## ✅ Requirements

- **Python 3.10+** (check with `python --version`)
- **Claude Desktop** (or another MCP client)
- **GRASS GIS** (optional but recommended) - [Download here](https://grass.osgeo.org/download/)

## 🧪 What to Test

### Basic Testing (No GRASS GIS needed)
1. Does installation work smoothly?
2. Does Claude Desktop detect the server?
3. Can you list available tools?
4. Are error messages helpful?

Try asking Claude:
- "What GRASS GIS tools are available?"
- "Tell me about the GRASS GIS MCP server capabilities"

### Advanced Testing (With GRASS GIS installed)
1. Can you query your GRASS data?
2. Do the tools work correctly?
3. Are results accurate?

Try asking Claude:
- "List raster maps in my GRASS location"
- "Get information about my elevation raster"
- "Calculate slope from my DEM"

## 📋 Testing Checklist

- [ ] Installation completed without errors
- [ ] Claude Desktop shows the MCP server
- [ ] Can list 8 available tools
- [ ] Tool descriptions are clear
- [ ] (Optional) Successfully queried GRASS data
- [ ] (Optional) Performed geospatial analysis

## 🐛 Found a Bug?

Please report it! Create an issue here:
👉 **https://github.com/seyi/grass/issues/new/choose**

Select "Bug Report" and fill in the details.

## 💬 Have Feedback?

We want to hear from you! Create an issue:
👉 **https://github.com/seyi/grass/issues/new/choose**

Select "Tester Feedback" and share your experience.

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Detailed installation guide
- **[README.md](README.md)** - Full documentation
- **[USAGE.md](USAGE.md)** - Usage examples and workflows

## 🧰 Test Scripts

Verify your installation:

```bash
# Linux/macOS
./test-installation.sh

# Windows (PowerShell)
.\test-installation.ps1
```

## ❓ Need Help?

**Troubleshooting:** See [QUICKSTART.md](QUICKSTART.md#troubleshooting)

**Questions:** Open an issue or reach out to the maintainer

**Documentation:** Check the docs in the repository

## 🎯 Testing Goals

Help us ensure:
1. ✅ Installation is smooth on all platforms
2. ✅ Documentation is clear and complete
3. ✅ Tools work reliably
4. ✅ Integration with Claude Desktop is seamless
5. ✅ Error messages are helpful

## 🙏 Thank You!

Your testing helps make geospatial AI tools accessible to everyone. Every bug report, suggestion, and piece of feedback makes this project better!

**Questions?** Comment on this issue or open a new one.

---

## Version Information

- **Repository:** https://github.com/seyi/grass
- **Branch:** `claude/create-geospatial-mcp-grass-011CUr9bMgUcm9QX2hz9KwdX`
- **Version:** 0.1.0 (Beta - Testing Phase)
- **Status:** Seeking testers

**Testing Period:** Now - ongoing

**Note:** This is beta software. Features may change based on your feedback!

---

### Quick Links

- 📦 **Installation:** [QUICKSTART.md](QUICKSTART.md)
- 📖 **Documentation:** [README.md](README.md)
- 🐛 **Report Bug:** [New Issue](https://github.com/seyi/grass/issues/new?labels=bug,mcp-server-test)
- 💡 **Give Feedback:** [New Issue](https://github.com/seyi/grass/issues/new?labels=feedback,mcp-server-test)
- ✨ **Request Feature:** [New Issue](https://github.com/seyi/grass/issues/new?labels=enhancement,mcp-server-test)

---

**Happy Testing! 🎉**
