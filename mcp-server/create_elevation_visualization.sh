#!/bin/bash
# Create Elevation Visualization - Run this on your local machine
#
# Prerequisites:
# 1. GRASS GIS installed: sudo apt-get install grass (Ubuntu/Debian)
# 2. North Carolina sample dataset downloaded and extracted to ~/grassdata/

echo "================================================================"
echo "GRASS GIS Elevation Visualization Script"
echo "================================================================"
echo ""

# Configuration
GISDBASE="$HOME/grassdata"
LOCATION="nc_spm_08_grass7"
MAPSET="PERMANENT"
OUTPUT_FILE="$HOME/elevation_map.png"

# Check if GRASS is installed
if ! command -v grass &> /dev/null; then
    echo "❌ ERROR: GRASS GIS is not installed"
    echo ""
    echo "To install:"
    echo "  Ubuntu/Debian: sudo apt-get install grass"
    echo "  macOS:         brew install grass"
    echo "  Windows:       Download from https://grass.osgeo.org/download/"
    exit 1
fi

echo "✓ GRASS GIS found: $(grass --version | head -1)"
echo ""

# Check if dataset exists
if [ ! -d "$GISDBASE/$LOCATION" ]; then
    echo "❌ ERROR: North Carolina dataset not found at: $GISDBASE/$LOCATION"
    echo ""
    echo "To download:"
    echo "  1. Download from: https://grass.osgeo.org/sampledata/north_carolina/nc_spm_08_grass7.zip"
    echo "  2. Extract to: $GISDBASE/"
    echo ""
    echo "Or run:"
    echo "  mkdir -p $GISDBASE"
    echo "  cd $GISDBASE"
    echo "  wget https://grass.osgeo.org/sampledata/north_carolina/nc_spm_08_grass7.zip"
    echo "  unzip nc_spm_08_grass7.zip"
    exit 1
fi

echo "✓ Dataset found: $GISDBASE/$LOCATION"
echo ""

# Create visualization
echo "Creating elevation visualization..."
echo "Output file: $OUTPUT_FILE"
echo ""

# Method 1: Using r.out.png (simplest - just the colored raster)
grass "$GISDBASE/$LOCATION/$MAPSET" --exec bash -c "
    # Set region to elevation map
    g.region raster=elevation

    # Apply elevation color table
    r.colors map=elevation color=elevation

    # Export to PNG with colors
    r.out.png input=elevation output='$OUTPUT_FILE' --overwrite

    echo '✓ Visualization created!'
"

# Check if file was created
if [ -f "$OUTPUT_FILE" ]; then
    echo ""
    echo "================================================================"
    echo "SUCCESS! Elevation map created"
    echo "================================================================"
    echo ""
    echo "File location: $OUTPUT_FILE"
    echo "File size: $(du -h "$OUTPUT_FILE" | cut -f1)"
    echo ""
    echo "To view:"
    echo "  - macOS:   open $OUTPUT_FILE"
    echo "  - Linux:   xdg-open $OUTPUT_FILE"
    echo "  - Windows: start $OUTPUT_FILE"
    echo ""
else
    echo ""
    echo "❌ ERROR: Visualization file was not created"
    echo "Check the error messages above"
    exit 1
fi

# Optional: Create enhanced version with cartographic elements
read -p "Create enhanced version with legend and scale? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    ENHANCED_FILE="$HOME/elevation_map_enhanced.png"

    grass "$GISDBASE/$LOCATION/$MAPSET" --exec bash -c "
        export GRASS_RENDER_IMMEDIATE=png
        export GRASS_RENDER_FILE='$ENHANCED_FILE'
        export GRASS_RENDER_WIDTH=1400
        export GRASS_RENDER_HEIGHT=1000

        g.region raster=elevation
        r.colors map=elevation color=elevation

        d.mon start=png --overwrite
        d.rast map=elevation
        d.legend raster=elevation at=10,90,85,89 fontsize=12 title='Elevation (m)'
        d.barscale length=5000 at=5,12 bgcolor=white fontsize=11
        d.northarrow at=93,92 fill_color=black
        d.text text='Elevation Map - North Carolina' at=50,96 size=5 color=black align=cc
        d.mon stop=png

        echo '✓ Enhanced visualization created!'
    "

    if [ -f "$ENHANCED_FILE" ]; then
        echo ""
        echo "Enhanced version: $ENHANCED_FILE"
    fi
fi

echo ""
echo "Done!"
