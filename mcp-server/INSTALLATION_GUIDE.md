# GRASS GIS Installation Guide
## Complete Setup for Local Machine

This guide will walk you through installing GRASS GIS and the North Carolina sample dataset on your local machine.

---

## Step 1: Identify Your Operating System

**Which operating system are you using?**
- Ubuntu/Debian Linux
- Other Linux (Fedora, Arch, etc.)
- macOS
- Windows

---

## Installation Instructions by OS

### 🐧 Ubuntu/Debian Linux

#### Install GRASS GIS

```bash
# Update package list
sudo apt-get update

# Install GRASS GIS
sudo apt-get install grass grass-dev

# Verify installation
grass --version
```

**Expected output:** `GRASS GIS 7.x` or `GRASS GIS 8.x`

---

### 🐧 Other Linux Distributions

**Fedora:**
```bash
sudo dnf install grass
```

**Arch Linux:**
```bash
sudo pacman -S grass
```

**openSUSE:**
```bash
sudo zypper install grass
```

---

### 🍎 macOS

#### Option 1: Homebrew (Recommended)

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install GRASS GIS
brew install grass

# Verify installation
grass --version
```

#### Option 2: Download Installer

1. Visit: https://grass.osgeo.org/download/mac/
2. Download the latest `.dmg` file
3. Open the DMG and drag GRASS to Applications
4. Open Terminal and add to PATH:
   ```bash
   echo 'export PATH="/Applications/GRASS.app/Contents/MacOS:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```

---

### 🪟 Windows

#### Option 1: OSGeo4W (Recommended)

1. **Download OSGeo4W installer:**
   - Visit: https://trac.osgeo.org/osgeo4w/
   - Download `osgeo4w-setup.exe`

2. **Run installer:**
   - Choose "Express Install"
   - Select "GRASS GIS"
   - Click "Next" and complete installation

3. **Verify:**
   - Open "OSGeo4W Shell" from Start Menu
   - Type: `grass --version`

#### Option 2: Standalone Installer

1. Visit: https://grass.osgeo.org/download/windows/
2. Download the latest installer
3. Run the installer and follow prompts
4. Add to PATH (optional):
   - Search "Environment Variables" in Windows
   - Edit PATH variable
   - Add GRASS installation directory (e.g., `C:\Program Files\GRASS GIS 8.3`)

---

## Step 2: Download North Carolina Sample Dataset

This is the dataset we've been using in all our examples.

### All Operating Systems

```bash
# Create grassdata directory
mkdir -p ~/grassdata
cd ~/grassdata

# Download dataset (141 MB)
# Using wget (Linux/Mac with wget installed)
wget https://grass.osgeo.org/sampledata/north_carolina/nc_spm_08_grass7.zip

# OR using curl (Mac default)
curl -O https://grass.osgeo.org/sampledata/north_carolina/nc_spm_08_grass7.zip

# Extract
unzip nc_spm_08_grass7.zip

# Verify
ls nc_spm_08_grass7/
```

**Expected output:** Directories like `PERMANENT`, `landsat`, `user1`

### Windows Alternative

If command-line download doesn't work:

1. **Download manually:**
   - Visit: https://grass.osgeo.org/sampledata/north_carolina/nc_spm_08_grass7.zip
   - Save to `C:\Users\YourName\grassdata\`

2. **Extract:**
   - Right-click ZIP file
   - Extract All → `C:\Users\YourName\grassdata\`

---

## Step 3: Verify Installation

### Test GRASS GIS

```bash
# Check version
grass --version

# List GRASS commands
grass --help

# Try to start GRASS with sample data
grass ~/grassdata/nc_spm_08_grass7/PERMANENT --text
```

**In GRASS shell, try:**
```bash
# List raster maps
g.list type=raster

# Get elevation info
r.info elevation

# Exit GRASS
exit
```

If these work, **installation is successful!** ✅

---

## Step 4: Create Your First Visualization

Now use the script I created earlier:

```bash
# Navigate to the MCP server directory
cd ~/grass/mcp-server

# Make script executable (if needed)
chmod +x create_elevation_visualization.sh

# Run the script
./create_elevation_visualization.sh
```

**Output:** `~/elevation_map.png`

**To view:**
```bash
# macOS
open ~/elevation_map.png

# Linux
xdg-open ~/elevation_map.png

# Windows
start %USERPROFILE%\elevation_map.png
```

---

## Troubleshooting

### Issue: "grass: command not found"

**Linux/Mac:**
```bash
# Find where GRASS is installed
which grass

# If not found, add to PATH
# For example, if installed at /usr/local/bin/grass
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**Windows:**
- Use "OSGeo4W Shell" instead of Command Prompt
- Or add GRASS to system PATH (see Windows installation above)

### Issue: "Cannot find location"

Make sure the path is correct:
```bash
# Check if dataset exists
ls ~/grassdata/nc_spm_08_grass7/

# If on Windows, use full path
ls C:\Users\YourName\grassdata\nc_spm_08_grass7\
```

### Issue: "Permission denied"

```bash
# Make script executable
chmod +x ~/grass/mcp-server/create_elevation_visualization.sh

# Or run with bash
bash ~/grass/mcp-server/create_elevation_visualization.sh
```

### Issue: Dataset download fails

**Alternative download methods:**

1. **Browser:** Visit link directly and download manually
   - https://grass.osgeo.org/sampledata/north_carolina/nc_spm_08_grass7.zip

2. **Alternative mirror:** Try OSGeo4W mirror
   - https://download.osgeo.org/grass/

3. **Smaller test dataset:** If bandwidth is limited
   - https://grass.osgeo.org/sampledata/north_carolina/nc_basic_spm_grass7.zip (50 MB)

---

## Quick Reference Card

### Essential Commands

```bash
# Start GRASS with GUI
grass

# Start GRASS in text mode
grass ~/grassdata/nc_spm_08_grass7/PERMANENT --text

# Execute single command
grass ~/grassdata/nc_spm_08_grass7/PERMANENT --exec r.info elevation

# List raster maps
g.list type=raster

# List vector maps
g.list type=vector

# Get map info
r.info map_name      # for raster
v.info map_name      # for vector

# Set computational region
g.region raster=elevation

# Display commands
d.rast map_name      # display raster
d.vect map_name      # display vector

# Export
r.out.gdal input=elevation output=~/elevation.tif
r.out.png input=elevation output=~/elevation.png
```

---

## Next Steps After Installation

1. ✅ **Test basic commands** (see Step 3 above)
2. ✅ **Create first visualization** (see Step 4 above)
3. 📚 **Explore tutorials:** https://grass.osgeo.org/learn/tutorials/
4. 🔧 **Integrate MCP server** with Claude Desktop (coming next!)

---

## System Requirements

**Minimum:**
- 2 GB RAM
- 500 MB disk space (+ space for data)
- Any modern CPU

**Recommended:**
- 4+ GB RAM
- 2+ GB disk space
- Multi-core CPU for faster processing

---

## Getting Help

**Official Resources:**
- Documentation: https://grass.osgeo.org/learn/
- Tutorials: https://grass.osgeo.org/learn/tutorials/
- Community: https://grass.osgeo.org/support/
- Mailing list: https://lists.osgeo.org/mailman/listinfo/grass-user

**For MCP Server Questions:**
- Check: `mcp-server/README.md`
- Review: `VISUALIZATION_OPTIONS.md`
- See: `LOCAL_VISUALIZATION_GUIDE.md`

---

## Installation Checklist

Use this to track your progress:

- [ ] GRASS GIS installed
- [ ] `grass --version` works
- [ ] grassdata directory created (`~/grassdata/`)
- [ ] NC dataset downloaded
- [ ] NC dataset extracted
- [ ] Test: `grass ~/grassdata/nc_spm_08_grass7/PERMANENT --text`
- [ ] Test: `g.list type=raster` shows maps
- [ ] Test: `r.info elevation` shows info
- [ ] Visualization script executed successfully
- [ ] Can view `~/elevation_map.png`

**All checked?** You're ready to use GRASS GIS! 🎉

---

## What's Your Operating System?

**Reply with your OS and I'll give you the specific commands to run!**

1. Ubuntu/Debian
2. macOS
3. Windows
4. Other Linux

I'll guide you through each step interactively!
