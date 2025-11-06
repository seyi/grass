# Map Visualization for GRASS GIS MCP Server
## Recommendations and Implementation Guide

---

## Executive Summary

**TL;DR:** For the GRASS GIS MCP server, I recommend **Option 2: Integrated Visualization using matplotlib/rasterio** as the primary approach, with **Option 5: Interactive Folium maps** as a secondary feature for exploration.

**Do NOT create a separate QGIS MCP server** unless you have specific professional cartography requirements that GRASS + Python visualization cannot meet.

---

## Option Comparison

### Option 1: GRASS Native (d.* commands + Cairo)
```
Complexity:    ⭐⭐⭐
Quality:       ⭐⭐⭐
Flexibility:   ⭐⭐
Integration:   ⭐⭐⭐⭐⭐
```
**Verdict:** ❌ Not recommended
- Requires display server configuration
- Limited styling control
- Complex Cairo driver setup
- Better alternatives available

### Option 2: matplotlib + rasterio (RECOMMENDED)
```
Complexity:    ⭐⭐
Quality:       ⭐⭐⭐⭐
Flexibility:   ⭐⭐⭐⭐⭐
Integration:   ⭐⭐⭐⭐⭐
```
**Verdict:** ✅ PRIMARY RECOMMENDATION
- **Pros:**
  - Lightweight dependencies
  - Full control over styling
  - Easy to integrate into existing MCP server
  - Works headless (no display required)
  - Publication-quality output
  - Python native (matches GRASS Python API)

- **Cons:**
  - Need to export rasters temporarily
  - Manual implementation of cartographic elements

- **Perfect for:**
  - Static map images (PNG, PDF)
  - Quick terrain visualizations
  - Analysis result documentation
  - Embedding in reports

### Option 3: Separate QGIS MCP Server
```
Complexity:    ⭐⭐⭐⭐⭐
Quality:       ⭐⭐⭐⭐⭐
Flexibility:   ⭐⭐⭐⭐
Integration:   ⭐⭐
```
**Verdict:** ⚠️ ONLY IF NEEDED
- **Pros:**
  - Professional cartographic output
  - Rich styling and symbology
  - Print layout capabilities
  - Can read GRASS data directly

- **Cons:**
  - **Heavy dependency** (entire QGIS + Qt)
  - **Complex setup** (separate MCP server)
  - **Maintenance burden** (two servers to manage)
  - **Redundancy** (duplicates functionality)
  - Overkill for most use cases

- **Only use if:**
  - You need professional print layouts
  - Complex multi-layer compositions required
  - Specific QGIS plugins needed
  - Client specifically requests QGIS output

### Option 4: grass.jupyter
```
Complexity:    ⭐⭐
Quality:       ⭐⭐⭐
Flexibility:   ⭐⭐⭐
Integration:   ⭐⭐⭐⭐
```
**Verdict:** ✅ Good alternative for GRASS 8+
- **Pros:**
  - Native GRASS Python API
  - Designed for programmatic use
  - No external dependencies
  - Easy to use

- **Cons:**
  - Requires GRASS 8.0+ (check version)
  - Less flexible than matplotlib
  - Limited to GRASS styling

- **Use if:**
  - You're on GRASS 8.0+
  - Want simplest possible solution
  - Don't need custom styling

### Option 5: Folium (Interactive HTML)
```
Complexity:    ⭐⭐
Quality:       ⭐⭐⭐⭐
Flexibility:   ⭐⭐⭐⭐
Integration:   ⭐⭐⭐⭐
```
**Verdict:** ✅ SECONDARY RECOMMENDATION
- **Pros:**
  - Interactive (pan, zoom, click)
  - Shareable HTML files
  - Great for exploration
  - Mobile-friendly

- **Cons:**
  - HTML output (not image)
  - Large rasters need tiling
  - Requires reprojection to WGS84

- **Perfect for:**
  - Data exploration
  - Sharing with non-GIS users
  - Web presentations
  - Location overview maps

---

## Recommended Architecture

### Single Integrated MCP Server (RECOMMENDED)

```
┌─────────────────────────────────────┐
│        Claude Desktop               │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│      GRASS GIS MCP Server           │
│  ┌───────────────────────────────┐  │
│  │  Core GRASS Tools             │  │
│  │  - grass_list_maps            │  │
│  │  - grass_raster_info          │  │
│  │  - grass_slope_aspect         │  │
│  │  - etc...                     │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │  Visualization Add-on         │  │
│  │  - grass_visualize_raster     │  │
│  │  - grass_create_composite     │  │
│  │  - grass_interactive_map      │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

**Advantages:**
- ✅ Single server to maintain
- ✅ Shared configuration
- ✅ Consistent error handling
- ✅ Easier for users to configure
- ✅ Lower resource usage

### Multi-Server Architecture (NOT RECOMMENDED)

```
┌─────────────────┐
│  Claude Desktop │
└────────┬────────┘
         │
    ┌────┴──────┐
    │           │
┌───▼───┐   ┌───▼────┐
│ GRASS │   │  QGIS  │
│  MCP  │   │  MCP   │
└───────┘   └────────┘
```

**Why avoid this:**
- ❌ Two servers to configure
- ❌ Two servers to maintain
- ❌ Complex user setup
- ❌ Higher resource usage
- ❌ Potential version conflicts
- ❌ Duplicated functionality

**Only use if:** You have **specific QGIS-only requirements** that cannot be met with Python visualization.

---

## Implementation Plan

### Phase 1: Core Visualization (Week 1) ⭐ START HERE

**Goal:** Add basic static map visualization

**Tools to implement:**
1. `grass_visualize_raster` - Create PNG images
   - Uses matplotlib + rasterio
   - Options: colormap, size, legend, scalebar
   - Output: PNG file

**Implementation:**
```python
# Add to existing grass_mcp_server.py

Tool(
    name="grass_visualize_raster",
    description="Create a PNG visualization of a GRASS raster map",
    inputSchema={
        "type": "object",
        "properties": {
            "map_name": {"type": "string"},
            "output_path": {"type": "string"},
            "colormap": {
                "type": "string",
                "enum": ["terrain", "viridis", "plasma", "elevation"],
                "default": "terrain"
            },
            "gisdbase": {"type": "string"},
            "location": {"type": "string"},
        },
        "required": ["map_name", "output_path", "gisdbase", "location"]
    }
)
```

**Dependencies:**
```bash
pip install matplotlib rasterio
```

**Test:**
```
"Create a visualization of the elevation map and save it to /tmp/elevation_viz.png"
```

### Phase 2: Advanced Styling (Week 2)

**Goal:** Add hillshade, overlays, and custom styling

**New features:**
- Hillshade overlays
- Multi-layer composites
- Custom color ramps
- Classification visualization

**Example:**
```
"Create a hillshade visualization of elevation with terrain colors at /tmp/terrain.png"
```

### Phase 3: Interactive Maps (Week 3)

**Goal:** Add interactive HTML export

**Tool:**
```python
Tool(
    name="grass_create_interactive_map",
    description="Create an interactive HTML map with pan/zoom",
    ...
)
```

**Test:**
```
"Create an interactive map of landuse and save to /tmp/landuse.html"
```

### Phase 4: Advanced Features (Future)

**Consider adding:**
- Vector visualization
- Animated time-series
- 3D terrain views
- Export to multiple formats (PDF, SVG, GeoTIFF)

---

## Code Integration Example

### Step 1: Install Dependencies

```bash
pip install matplotlib rasterio folium
```

### Step 2: Add Visualization Module

Copy `grass_visualization_addon.py` to your mcp-server directory.

### Step 3: Integrate into Main Server

In `grass_mcp_server.py`:

```python
# At top of file
from grass_visualization_addon import (
    VISUALIZATION_TOOLS,
    handle_visualization_tool
)

# In list_tools handler
@server.list_tools()
async def list_tools() -> list[Tool]:
    return GRASS_TOOLS + VISUALIZATION_TOOLS

# In call_tool handler
@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    # Add before existing tool handlers
    if name in ["grass_visualize_raster", "grass_create_composite",
                "grass_create_interactive_map"]:
        return await handle_visualization_tool(name, arguments)

    # ... existing tool handlers ...
```

### Step 4: Test

```bash
# Test the server
python grass_mcp_server.py
```

```
# In Claude Desktop, ask:
"Create a visualization of the elevation map in the North Carolina location"
```

---

## Cost-Benefit Analysis

### Option A: Integrated Python Visualization
```
Setup Time:      2-4 hours
Maintenance:     Low
Quality:         High
Cost:           $0 (open source)
Flexibility:     Very High
```
**ROI:** ⭐⭐⭐⭐⭐

### Option B: Separate QGIS MCP Server
```
Setup Time:      2-3 days
Maintenance:     High
Quality:         Very High
Cost:           $0 (but time-intensive)
Flexibility:     High (but complex)
```
**ROI:** ⭐⭐ (only for specific use cases)

---

## Decision Matrix

| Requirement | matplotlib | QGIS | Recommendation |
|-------------|-----------|------|----------------|
| Quick previews | ✅ | ❌ | matplotlib |
| Static maps | ✅ | ✅ | matplotlib |
| Interactive maps | ✅ (Folium) | ❌ | Folium |
| Print layouts | ⚠️ | ✅ | QGIS (if critical) |
| Custom styling | ✅ | ✅ | matplotlib |
| Easy setup | ✅ | ❌ | matplotlib |
| Low maintenance | ✅ | ❌ | matplotlib |
| Publication quality | ✅ | ✅✅ | matplotlib (usually) |

---

## When to Use QGIS MCP Server

Create a separate QGIS MCP server **ONLY IF**:

1. ✅ You need **print layouts** with complex cartography
2. ✅ Client specifically requires **QGIS-rendered output**
3. ✅ You need **QGIS-specific plugins** (e.g., network analysis, specific symbology)
4. ✅ You're already maintaining QGIS infrastructure
5. ✅ Team has QGIS expertise but not Python visualization

**Do NOT use QGIS MCP server if:**

- ❌ Just want "better looking maps" (matplotlib can do this)
- ❌ Haven't tried Python visualization first
- ❌ Want to avoid learning matplotlib
- ❌ Think QGIS is "more professional" (it's not always)

---

## Final Recommendation

### Primary Approach: Integrated Visualization

**Use:** matplotlib + rasterio for PNG outputs
**Use:** Folium for interactive HTML maps
**Integrate:** Into existing GRASS GIS MCP server

**Why:**
- ✅ Simplest to implement and maintain
- ✅ Meets 95% of visualization needs
- ✅ Lightweight and fast
- ✅ Fully programmable
- ✅ No display server needed
- ✅ Works in containers/cloud

### When to Add QGIS

**Only add QGIS MCP server when:**
- You have a **specific, demonstrated need**
- Python visualization is **insufficient**
- You've **already implemented** matplotlib approach
- You have **capacity for maintenance**

### Implementation Priority

1. **Now:** Add matplotlib-based `grass_visualize_raster`
2. **Next:** Add Folium-based `grass_create_interactive_map`
3. **Later:** Add advanced styling options
4. **Maybe:** Consider QGIS server if specific need arises

---

## Getting Started

### Quick Start (30 minutes)

```bash
# 1. Install dependencies
pip install matplotlib rasterio folium

# 2. Copy add-on to your server directory
cp grass_visualization_addon.py /path/to/your/mcp-server/

# 3. Integrate (see example above)
# Edit grass_mcp_server.py to import and use visualization tools

# 4. Test
python grass_mcp_server.py

# 5. Use in Claude Desktop
"Create a visualization of elevation and save to /tmp/test.png"
```

### Files Provided

- ✅ `VISUALIZATION_OPTIONS.md` - Comprehensive overview
- ✅ `grass_visualization_addon.py` - Ready-to-use implementation
- ✅ `visualization_poc.py` - Proof of concept examples
- ✅ `VISUALIZATION_RECOMMENDATION.md` - This document

---

## Conclusion

**Start with integrated Python visualization.** It's simpler, lighter, and sufficient for most needs. You can always add QGIS later if you discover a genuine requirement.

**Don't over-engineer.** The best solution is the simplest one that meets your needs.

**Remember:** GRASS GIS itself is already a professional GIS. Combined with Python's visualization ecosystem, you have everything needed for high-quality map output.
