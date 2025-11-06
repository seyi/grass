# Map Visualization Options for GRASS GIS MCP Server

## Overview
This document explores options for adding map visualization capabilities to the GRASS GIS MCP server, including QGIS integration, GRASS native tools, and Python-based solutions.

---

## Option 1: GRASS Native Visualization (d.* commands)

### Approach: Use GRASS's built-in rendering to PNG/image files

**Advantages:**
- No additional dependencies
- Direct integration with existing GRASS session
- Leverages GRASS's native rendering engine

**Disadvantages:**
- Requires Cairo driver setup
- Limited interactivity
- Styling can be complex

**Implementation Example:**

```python
def grass_render_map(map_name, output_png, map_type="raster"):
    """Render a GRASS map to PNG file"""
    commands = [
        # Set up Cairo PNG driver
        f"export GRASS_RENDER_IMMEDIATE=png",
        f"export GRASS_RENDER_FILE={output_png}",
        f"export GRASS_RENDER_WIDTH=800",
        f"export GRASS_RENDER_HEIGHT=600",

        # Render the map
        f"d.mon start=png",
        f"d.{'rast' if map_type == 'raster' else 'vect'} map={map_name}",
        f"d.legend raster={map_name}" if map_type == "raster" else "",
        f"d.barscale",
        f"d.northarrow",
        f"d.mon stop=png"
    ]
    # Execute commands...
```

**Status:** ✅ Feasible, moderate complexity

---

## Option 2: GRASS Python grass.jupyter Module

### Approach: Use grass.jupyter for programmatic map creation

**Advantages:**
- Modern Python API
- Designed for programmatic use
- Good for static images
- Already part of GRASS 8+

**Disadvantages:**
- Requires GRASS 8.0+
- Limited interactivity

**Implementation Example:**

```python
import grass.jupyter as gj

def create_visualization(map_name, output_path):
    """Create map visualization using grass.jupyter"""
    # Create a Map object
    map_viz = gj.Map()
    map_viz.d_rast(map=map_name)
    map_viz.d_legend(raster=map_name)
    map_viz.d_barscale()

    # Save to file
    map_viz.save(output_path)

    return output_path
```

**Status:** ✅✅ Recommended for GRASS-only solution

---

## Option 3: Separate QGIS MCP Server

### Approach: Create dedicated MCP server using PyQGIS

**Advantages:**
- Professional cartographic output
- Rich styling capabilities
- Can work with GRASS data via GRASS provider
- Extensive plugin ecosystem

**Disadvantages:**
- Separate MCP server to maintain
- Heavier dependencies
- More complex setup

**Architecture:**

```
┌─────────────────┐
│  Claude Desktop │
└────────┬────────┘
         │
    ┌────┴─────┐
    │   MCP    │
    └────┬─────┘
         │
    ┌────┴──────────────┐
    │                   │
┌───▼──────┐    ┌──────▼─────┐
│  GRASS   │    │    QGIS    │
│   MCP    │    │    MCP     │
│  Server  │    │   Server   │
└──────────┘    └────────────┘
```

**Implementation Sketch:**

```python
# qgis_mcp_server.py
from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsRasterLayer,
    QgsVectorLayer,
    QgsMapSettings,
    QgsMapRendererCustomPainterJob
)
from PyQt5.QtGui import QImage, QPainter

class QGISMCPServer:
    def __init__(self):
        # Initialize QGIS
        QgsApplication.setPrefixPath("/usr", True)
        self.qgs = QgsApplication([], False)
        self.qgs.initQgis()

    def render_grass_raster(self, grass_layer_path, output_png):
        """Render GRASS raster using QGIS"""
        # Load GRASS raster
        layer = QgsRasterLayer(grass_layer_path, "grass_layer", "grass")

        if not layer.isValid():
            raise Exception("Layer failed to load")

        # Setup rendering
        settings = QgsMapSettings()
        settings.setLayers([layer])
        settings.setExtent(layer.extent())
        settings.setOutputSize(QSize(800, 600))

        # Render to image
        image = QImage(800, 600, QImage.Format_ARGB32)
        painter = QPainter(image)
        job = QgsMapRendererCustomPainterJob(settings, painter)
        job.start()
        job.waitForFinished()
        painter.end()

        image.save(output_png)
```

**Status:** ✅✅✅ Best for professional cartography

---

## Option 4: Python Visualization Libraries (matplotlib/rasterio)

### Approach: Use Python geospatial stack for visualization

**Advantages:**
- Lightweight
- Full control over styling
- Easy to customize
- Can be integrated into existing MCP server

**Disadvantages:**
- Limited cartographic features
- Manual implementation of common map elements
- Basic styling compared to GIS software

**Implementation Example:**

```python
import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

def visualize_grass_raster(grass_map, output_png):
    """Visualize GRASS raster using matplotlib"""
    # Export GRASS raster to GeoTIFF temporarily
    temp_tif = "/tmp/temp_export.tif"
    run_grass_command(
        ["r.out.gdal", f"input={grass_map}",
         f"output={temp_tif}", "format=GTiff", "--overwrite"]
    )

    # Read and plot with rasterio
    with rasterio.open(temp_tif) as src:
        data = src.read(1)

        fig, ax = plt.subplots(figsize=(10, 8))

        # Plot raster
        im = ax.imshow(data, cmap='terrain')

        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Elevation (m)')

        # Add title
        ax.set_title(f'GRASS Raster: {grass_map}')

        # Save
        plt.savefig(output_png, dpi=300, bbox_inches='tight')
        plt.close()
```

**Status:** ✅✅ Good balance of simplicity and functionality

---

## Option 5: Web-Based Interactive Maps (Folium/Leaflet)

### Approach: Generate HTML maps with Leaflet/Folium

**Advantages:**
- Interactive (pan, zoom, click)
- Can be opened in browser
- Shareable
- Works with GeoJSON, raster tiles

**Disadvantages:**
- Requires raster tiling for large datasets
- HTML output (not image)
- Limited by browser capabilities

**Implementation Example:**

```python
import folium
import rasterio
from rasterio.warp import calculate_default_transform, reproject

def create_interactive_map(grass_map, output_html):
    """Create interactive Leaflet map"""
    # Export to GeoTIFF
    temp_tif = "/tmp/temp_map.tif"
    run_grass_command([
        "r.out.gdal", f"input={grass_map}",
        f"output={temp_tif}", "--overwrite"
    ])

    # Get center and bounds
    with rasterio.open(temp_tif) as src:
        bounds = src.bounds
        center = [(bounds.bottom + bounds.top)/2,
                  (bounds.left + bounds.right)/2]

    # Create folium map
    m = folium.Map(location=center, zoom_start=12)

    # Add raster overlay (simplified)
    # In practice, you'd generate tiles or use a tile server
    folium.raster_layers.ImageOverlay(
        image=temp_tif,
        bounds=[[bounds.bottom, bounds.left],
                [bounds.top, bounds.right]],
        opacity=0.7
    ).add_to(m)

    # Save
    m.save(output_html)
```

**Status:** ✅✅ Excellent for interactive exploration

---

## Option 6: Hybrid Approach - Integrated into GRASS MCP

### Approach: Add visualization tools to existing GRASS MCP server

**Advantages:**
- Single MCP server
- Seamless integration
- Choose visualization backend per use case

**Implementation:**

```python
# Add to existing grass_mcp_server.py

Tool(
    name="grass_visualize_raster",
    description="Create a visualization of a GRASS raster map",
    inputSchema={
        "type": "object",
        "properties": {
            "map_name": {"type": "string"},
            "output_path": {"type": "string"},
            "style": {
                "type": "string",
                "enum": ["simple", "hillshade", "classified"],
                "default": "simple"
            },
            "format": {
                "type": "string",
                "enum": ["png", "html", "pdf"],
                "default": "png"
            },
            "gisdbase": {"type": "string"},
            "location": {"type": "string"},
        },
        "required": ["map_name", "output_path", "gisdbase", "location"]
    }
)
```

**Status:** ✅✅✅ Recommended starting point

---

## Comparison Matrix

| Option | Complexity | Quality | Interactive | Dependencies | Integration |
|--------|-----------|---------|-------------|--------------|-------------|
| GRASS d.* | Medium | Good | No | None | Excellent |
| grass.jupyter | Low | Good | No | None | Excellent |
| QGIS MCP | High | Excellent | No | QGIS | Separate |
| matplotlib | Low | Good | No | Python libs | Excellent |
| Folium | Medium | Good | Yes | Python libs | Excellent |
| Hybrid | Medium | Variable | Optional | Minimal | Excellent |

---

## Recommended Implementation Strategy

### Phase 1: Quick Win (Week 1)
**Use grass.jupyter for static maps**
- Add `grass_create_map` tool
- Output PNG files
- Basic styling (colormap, legend, scale)

### Phase 2: Enhanced Visualization (Week 2-3)
**Add matplotlib-based rendering**
- Custom colormaps
- Multiple layers
- Annotations
- Export to PNG/PDF

### Phase 3: Interactive Maps (Week 3-4)
**Implement Folium/Leaflet export**
- HTML output
- Interactive pan/zoom
- Click for attribute info
- Layer toggling

### Phase 4: Professional Output (Future)
**Consider QGIS MCP server**
- For publication-quality maps
- Advanced cartography
- Print layouts
- When needed by users

---

## Technical Considerations

### 1. File Paths and Access
- Where should generated visualizations be saved?
- `/tmp/` directory?
- User-specified path?
- Temporary files with expiration?

### 2. Performance
- Raster visualization can be slow for large datasets
- Consider downsampling for previews
- Implement caching

### 3. Styling
- Provide preset styles (terrain, elevation, classified)
- Allow custom colormaps
- Support transparency and overlays

### 4. Output Format
- PNG for static images
- HTML for interactive
- PDF for print
- GeoTIFF for further processing

---

## Proof of Concept Code

See accompanying file: `visualization_poc.py`

This implements a working example using:
1. grass.jupyter for quick renders
2. matplotlib for custom styling
3. Folium for interactive maps

---

## Next Steps

1. **Choose primary approach** based on requirements
2. **Implement basic MCP tool** for visualization
3. **Test with North Carolina dataset**
4. **Gather user feedback**
5. **Iterate and enhance**

## Questions to Consider

1. What's the primary use case? (Quick preview vs. publication quality)
2. Is interactivity required?
3. What output formats are preferred?
4. Should this be one MCP server or multiple?
5. What's the acceptable complexity/maintenance burden?
