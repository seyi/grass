# Local Visualization Guide

## Why You Can't See /tmp/my_map.png

### The Situation

When you run `cp /tmp/my_map.png ~/`, you get an error because the file exists in **my environment** (the server/container where I execute GRASS GIS), not on **your local machine**.

```
┌─────────────────────┐         ┌──────────────────────┐
│   Your Machine      │         │   My Environment     │
│                     │         │   (Claude's Server)  │
│   YOU are here -->  │         │   <-- I am here      │
│                     │         │                      │
│   No files          │  <--X-- │   /tmp/my_map.png ✓  │
│                     │         │   All GRASS data ✓   │
└─────────────────────┘         └──────────────────────┘
```

### Why This Happens

- **I run GRASS GIS commands** in a container/server environment
- **The files I create** stay in that environment
- **You cannot directly access** those files from your machine
- **Solution:** Run GRASS GIS on your own machine

---

## How to Create Visualizations on YOUR Machine

### Option 1: Run the Provided Script (Easiest)

I've created a script that will generate the same visualization on your machine:

**Location:** `mcp-server/create_elevation_visualization.sh`

**To use:**

```bash
cd ~/grass/mcp-server
./create_elevation_visualization.sh
```

**Output:** `~/elevation_map.png`

### Option 2: Manual Commands

If you have GRASS GIS and the NC dataset installed:

```bash
# Basic visualization
grass ~/grassdata/nc_spm_08_grass7/PERMANENT --exec bash -c '
  g.region raster=elevation
  r.colors map=elevation color=elevation
  r.out.png input=elevation output=~/elevation_map.png --overwrite
'
```

### Option 3: Use MCP Server with Claude Desktop (Future)

Once you integrate the GRASS MCP server with Claude Desktop on your machine:

1. **Claude Desktop runs locally** on your machine
2. **MCP server accesses local GRASS** installation
3. **Files are created locally** on your machine
4. **You can see and access** all outputs directly

**Usage:**
```
"Create a visualization of elevation and save to ~/Downloads/my_map.png"
```

The file will appear in your Downloads folder!

---

## Prerequisites for Local Visualization

### 1. Install GRASS GIS

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install grass
```

**macOS:**
```bash
brew install grass
```

**Windows:**
Download from https://grass.osgeo.org/download/

### 2. Download North Carolina Sample Dataset

```bash
# Create directory
mkdir -p ~/grassdata
cd ~/grassdata

# Download (141 MB)
wget https://grass.osgeo.org/sampledata/north_carolina/nc_spm_08_grass7.zip

# Extract
unzip nc_spm_08_grass7.zip
```

### 3. Verify Installation

```bash
grass --version
ls ~/grassdata/nc_spm_08_grass7/
```

You should see:
- GRASS GIS version (8.x or 7.x)
- Dataset directories (PERMANENT, landsat, user1)

---

## Quick Test

Run this to test your setup:

```bash
grass ~/grassdata/nc_spm_08_grass7/PERMANENT --exec r.info elevation
```

If you see elevation map information, you're ready to create visualizations!

---

## What I Can Do vs What You Can Do

| Action | I Can Do (Server) | You Can Do (Local) |
|--------|------------------|-------------------|
| Run GRASS commands | ✅ Yes | ✅ Yes (if installed) |
| Create visualizations | ✅ Yes | ✅ Yes (if installed) |
| Show you the results | ✅ Via images in chat | ✅ Open files directly |
| Save to your machine | ❌ No | ✅ Yes |
| Access your files | ❌ No | ✅ Yes |

---

## Examples of What Works

### ✅ What I CAN Show You:

1. **Display visualizations** - I create them on my server and show you the image
2. **Run analysis** - Calculate statistics, perform operations
3. **Generate code** - Provide scripts you can run locally
4. **Test workflows** - Validate that commands work

### ❌ What I CANNOT Do:

1. **Create files on your machine** - No direct file system access
2. **Install software** - You need to install GRASS locally
3. **Access your data** - Can't read files from your machine

---

## The Future: MCP Server Integration

Once you integrate the GRASS MCP server with Claude Desktop:

**Architecture:**
```
┌─────────────────────────────────────┐
│      Your Local Machine             │
│                                     │
│  ┌──────────────────────────────┐  │
│  │    Claude Desktop (GUI)      │  │
│  └──────────┬───────────────────┘  │
│             │                       │
│  ┌──────────▼───────────────────┐  │
│  │    GRASS GIS MCP Server      │  │
│  │    (runs locally)            │  │
│  └──────────┬───────────────────┘  │
│             │                       │
│  ┌──────────▼───────────────────┐  │
│  │    GRASS GIS Installation    │  │
│  │    ~/grassdata/              │  │
│  └──────────────────────────────┘  │
│                                     │
│  All files saved to YOUR machine!   │
└─────────────────────────────────────┘
```

**Then you can:**
- Ask Claude to create visualizations
- Files appear directly on your machine
- No manual commands needed
- Full integration with your local GRASS installation

---

## Summary

**Current Situation:**
- I create visualizations on my server
- You can SEE them in our conversation (if images display)
- You CANNOT access the files directly
- You need to run GRASS locally to create files on your machine

**Solution:**
1. Use the provided script: `create_elevation_visualization.sh`
2. Or install GRASS + NC dataset and run commands manually
3. Future: MCP server integration = automatic local file creation

**Script Location:** `mcp-server/create_elevation_visualization.sh`

**Questions?** Just ask! I can help you set up GRASS GIS locally or troubleshoot any issues.
