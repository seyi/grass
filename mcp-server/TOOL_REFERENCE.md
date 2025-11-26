# GRASS GIS MCP Server - Complete Tool Reference

**Version:** Phase 2A+B
**Total Tools:** 17 (8 core + 3 visualization + 5 advanced + 1 universal)
**GRASS Commands Accessible:** 500+

---

## Quick Reference

| Category | Tools | Coverage |
|----------|-------|----------|
| Core Operations | 8 | Essential GIS functions |
| Visualization | 3 | Map rendering & export |
| Advanced Analysis | 5 | Hydrology, visibility, classification |
| Universal Access | 1 | ALL 500+ GRASS commands |

---

## Core Tools (8)

### grass_raster_info
**Purpose:** Get metadata about raster maps

**Parameters:**
- `map_name` (required): Name of raster map
- `gisdbase` (required): Path to GRASS database
- `location` (required): GRASS location name
- `mapset` (optional): Mapset name (default: PERMANENT)

**Returns:** Raster dimensions, resolution, extent, data type, value range

**Example:**
```
"Get information about the elevation raster"
→ Returns: rows, cols, north, south, east, west, resolution, min, max
```

---

### grass_vector_info
**Purpose:** Get metadata about vector maps

**Parameters:**
- `map_name` (required): Name of vector map
- `gisdbase` (required): Path to GRASS database
- `location` (required): GRASS location name
- `mapset` (optional): Mapset name (default: PERMANENT)

**Returns:** Number of features, feature types, extent, attribute information

**Example:**
```
"Get information about the roads vector map"
→ Returns: points, lines, areas, extent, attributes
```

---

### grass_raster_univar
**Purpose:** Calculate statistics for raster maps

**Parameters:**
- `map_name` (required): Name of raster map
- `gisdbase` (required): Path to GRASS database
- `location` (required): GRASS location name
- `mapset` (optional): Mapset name (default: PERMANENT)
- `extended` (optional): Calculate extended statistics (default: false)

**Returns:** min, max, mean, stddev, variance, and optionally quartiles, percentiles

**Example:**
```
"Calculate statistics for the elevation map"
→ Returns: min=55.58, max=156.33, mean=110.38, stddev=20.27
```

---

### grass_list_maps
**Purpose:** List all maps in a location/mapset

**Parameters:**
- `gisdbase` (required): Path to GRASS database
- `location` (required): GRASS location name
- `mapset` (optional): Mapset name (default: PERMANENT)
- `map_type` (optional): Filter by type (raster, vector, raster_3d, all)

**Returns:** List of map names

**Example:**
```
"List all raster maps in the location"
→ Returns: elevation, slope, aspect, landuse, ...
```

---

### grass_mapcalc
**Purpose:** Perform raster map algebra

**Parameters:**
- `expression` (required): Map algebra expression
- `gisdbase` (required): Path to GRASS database
- `location` (required): GRASS location name
- `mapset` (optional): Mapset name (default: PERMANENT)

**Returns:** Confirmation message

**Example:**
```
"Create a new map that's elevation in feet"
→ expression: "elevation_feet = elevation * 3.28084"
```

---

### grass_slope_aspect
**Purpose:** Calculate slope and aspect from DEM

**Parameters:**
- `elevation` (required): Input elevation raster
- `slope` (required): Output slope map name
- `aspect` (optional): Output aspect map name
- `gisdbase` (required): Path to GRASS database
- `location` (required): GRASS location name
- `mapset` (optional): Mapset name (default: PERMANENT)

**Returns:** Confirmation message

**Example:**
```
"Calculate slope from elevation"
→ Creates slope map in degrees
```

---

### grass_buffer
**Purpose:** Create buffer around vector features

**Parameters:**
- `input_map` (required): Input vector map
- `output_map` (required): Output buffer map name
- `distance` (required): Buffer distance in map units
- `gisdbase` (required): Path to GRASS database
- `location` (required): GRASS location name
- `mapset` (optional): Mapset name (default: PERMANENT)

**Returns:** Confirmation message

**Example:**
```
"Create 100-meter buffer around roads"
→ distance: 100
```

---

### grass_region_info
**Purpose:** Get computational region information

**Parameters:**
- `gisdbase` (required): Path to GRASS database
- `location` (required): GRASS location name
- `mapset` (optional): Mapset name (default: PERMANENT)

**Returns:** Extent, resolution, rows/columns

**Example:**
```
"Show the current computational region"
→ Returns: north, south, east, west, nsres, ewres, rows, cols
```

---

## Visualization Tools (3) - Phase 1

### grass_visualize_raster
**Purpose:** Create PNG visualization of raster map

**Parameters:**
- `map_name` (required): Raster map to visualize
- `output_path` (required): Output PNG file path
- `width` (optional): Image width in pixels (default: 800)
- `height` (optional): Image height in pixels (default: 600)
- `style` (optional): Visualization style (simple, hillshade, terrain, classified)
- `add_legend` (optional): Add legend (default: true)
- `add_scalebar` (optional): Add scale bar (default: true)
- `add_north_arrow` (optional): Add north arrow (default: true)
- `gisdbase` (required): Path to GRASS database
- `location` (required): GRASS location name
- `mapset` (optional): Mapset name (default: PERMANENT)

**Returns:** PNG file path

**Example:**
```
"Create a visualization of elevation with legend and scale bar"
→ Creates professional map with cartographic elements
```

---

### grass_create_composite
**Purpose:** Create hillshade composite visualization

**Parameters:**
- `base_map` (required): Base elevation map
- `overlay_map` (optional): Optional overlay map
- `output_path` (required): Output PNG file path
- `gisdbase` (required): Path to GRASS database
- `location` (required): GRASS location name

**Returns:** PNG file path

**Example:**
```
"Create terrain visualization with hillshade"
→ Combines colored elevation with hillshade relief
```

---

### grass_create_interactive_map
**Purpose:** Create interactive HTML map

**Parameters:**
- `map_name` (required): Raster map to visualize
- `output_path` (required): Output HTML file path
- `gisdbase` (required): Path to GRASS database
- `location` (required): GRASS location name

**Returns:** HTML file path

**Example:**
```
"Create interactive map of landuse"
→ Creates zoomable, pannable HTML map
```

---

## Advanced Analysis Tools (5) - Phase 2A

### grass_watershed
**Purpose:** Watershed analysis and stream extraction

**Parameters:**
- `elevation` (required): Input DEM
- `accumulation` (optional): Output flow accumulation map
- `drainage` (optional): Output drainage direction map
- `basin` (optional): Output watershed basins map
- `stream` (optional): Output stream network map
- `threshold` (optional): Minimum flow for streams (default: 1000)
- `gisdbase` (required): Path to GRASS database
- `location` (required): GRASS location name
- `mapset` (optional): Mapset name (default: PERMANENT)

**Returns:** List of created outputs

**Example:**
```
"Perform watershed analysis and extract streams"
→ Creates flow accumulation, watersheds, stream networks
```

**Use Cases:**
- Hydrology modeling
- Stream network extraction
- Watershed delineation
- Flow path analysis

---

### grass_viewshed
**Purpose:** Calculate viewshed (visible areas)

**Parameters:**
- `input` (required): Input elevation raster
- `output` (required): Output viewshed map
- `coordinates` (required): Observer coordinates (x,y or easting,northing)
- `observer_elevation` (optional): Observer height above ground (default: 1.75m)
- `target_elevation` (optional): Target height above ground (default: 0m)
- `max_distance` (optional): Maximum visibility distance (default: -1 = infinity)
- `gisdbase` (required): Path to GRASS database
- `location` (required): GRASS location name
- `mapset` (optional): Mapset name (default: PERMANENT)

**Returns:** Viewshed raster (1 = visible, 0 = not visible)

**Example:**
```
"Calculate what's visible from a tower at 637500,220500"
→ Creates binary viewshed map
```

**Use Cases:**
- Tower placement
- Scenic view analysis
- Line-of-sight studies
- Visual impact assessment

---

### grass_reclass
**Purpose:** Reclassify raster values into categories

**Parameters:**
- `input` (required): Input raster map
- `output` (required): Output reclassified map
- `rules` (required): Reclassification rules (format: "min:max:new_value\n...")
- `gisdbase` (required): Path to GRASS database
- `location` (required): GRASS location name
- `mapset` (optional): Mapset name (default: PERMANENT)

**Returns:** Reclassified map

**Example:**
```
"Reclassify elevation into low/medium/high"
→ rules: "0:100:1 = Low\n100:200:2 = Medium\n200:*:3 = High"
```

**Use Cases:**
- Land use classification
- Risk mapping
- Suitability analysis
- Category simplification

---

### grass_overlay
**Purpose:** Vector overlay operations

**Parameters:**
- `ainput` (required): First input vector map
- `binput` (required): Second input vector map
- `output` (required): Output map name
- `operator` (optional): Overlay operator (and, or, not, xor) (default: and)
- `gisdbase` (required): Path to GRASS database
- `location` (required): GRASS location name
- `mapset` (optional): Mapset name (default: PERMANENT)

**Returns:** Overlay result map

**Example:**
```
"Find areas that are both forest AND within 500m of water"
→ operator: "and"
```

**Operators:**
- `and`: Intersection (areas in both)
- `or`: Union (areas in either)
- `not`: Difference (A minus B)
- `xor`: Exclusive or (areas in one but not both)

**Use Cases:**
- Spatial queries
- Suitability analysis
- Overlay analysis
- Feature selection

---

### grass_import_raster
**Purpose:** Import raster data with automatic reprojection

**Parameters:**
- `input` (required): Path to input raster file (GeoTIFF, etc.)
- `output` (required): Name for imported raster in GRASS
- `resolution` (optional): Resolution method (estimated, value, region) (default: estimated)
- `extent` (optional): Extent to use (input, region) (default: input)
- `gisdbase` (required): Path to GRASS database
- `location` (required): GRASS location name
- `mapset` (optional): Mapset name (default: PERMANENT)

**Returns:** Confirmation message

**Example:**
```
"Import DEM.tif and reproject to match the location"
→ Automatically handles coordinate transformation
```

**Supported Formats:**
- GeoTIFF
- ERDAS Imagine
- HDF
- NetCDF
- Many others via GDAL

---

## Universal Access (1) - Phase 2B

### grass_execute
**Purpose:** Execute ANY GRASS GIS command

**Parameters:**
- `command` (required): GRASS command name (e.g., "r.watershed", "v.overlay")
- `parameters` (required): Command parameters as key-value pairs
- `flags` (optional): Command flags (without dashes, e.g., "a" for -a)
- `stdin` (optional): Input data via stdin (for commands that read from stdin)
- `gisdbase` (required): Path to GRASS database
- `location` (required): GRASS location name
- `mapset` (optional): Mapset name (default: PERMANENT)

**Returns:** Command output

**Example 1: Neighborhood Analysis**
```
command: "r.neighbors"
parameters: {
  "input": "elevation",
  "output": "elevation_smooth",
  "size": 5,
  "method": "average"
}
```

**Example 2: Image Classification**
```
command: "i.cluster"
parameters: {
  "group": "landsat",
  "subgroup": "all_bands",
  "signaturefile": "cluster_sig",
  "classes": 5
}
```

**Example 3: Network Analysis**
```
command: "v.net.path"
parameters: {
  "input": "roads",
  "output": "shortest_path",
  "start_points": "start",
  "end_points": "end"
}
flags: "t"
```

**Provides Access To:**
- 167 raster operations (r.*)
- 126 vector operations (v.*)
- 50 image processing commands (i.*)
- 51 temporal commands (t.*)
- 43 display commands (d.*)
- 27 3D raster commands (r3.*)
- 27 general utilities (g.*)
- 18 database commands (db.*)

**Total: 500+ GRASS GIS commands**

---

## Tool Selection Guide

### When to use what:

**For common operations:** Use dedicated tools
- Terrain analysis → `grass_slope_aspect`
- Statistics → `grass_raster_univar`
- Visualization → `grass_visualize_raster`
- Watershed → `grass_watershed`

**For advanced/specialized operations:** Use `grass_execute`
- Neighborhood analysis → `r.neighbors`
- Cost surface → `r.cost`
- Network routing → `v.net.*`
- Image classification → `i.cluster`, `i.maxlik`
- Temporal analysis → `t.*` commands

**Advantages of dedicated tools:**
- ✅ Tailored schemas with clear parameters
- ✅ Built-in validation
- ✅ Better error messages
- ✅ Easier for AI to understand

**Advantages of grass_execute:**
- ✅ Access to ALL 500+ commands
- ✅ No waiting for new tools to be added
- ✅ Maximum flexibility
- ✅ Can use latest GRASS features

---

## Common Workflows

### Terrain Analysis Workflow
```
1. grass_raster_info → Get elevation extent
2. grass_slope_aspect → Calculate slope & aspect
3. grass_watershed → Extract watersheds
4. grass_visualize_raster → Create visualization
```

### Land Suitability Workflow
```
1. grass_reclass → Classify elevation
2. grass_reclass → Classify slope
3. grass_overlay → Combine criteria (operator: and)
4. grass_visualize_raster → Map results
```

### Visibility Analysis Workflow
```
1. grass_viewshed → Calculate visible areas
2. grass_mapcalc → Combine multiple viewsheds
3. grass_raster_univar → Statistics on visibility
4. grass_create_composite → Visualization
```

### Import and Analyze Workflow
```
1. grass_import_raster → Import external data
2. grass_region_info → Verify region
3. grass_raster_univar → Check data quality
4. grass_execute(r.neighbors) → Smooth if needed
5. grass_watershed → Perform analysis
```

---

## Error Handling

All tools provide:
- ✅ Clear error messages
- ✅ Helpful suggestions
- ✅ Graceful degradation
- ✅ Timeout protection

Common errors and solutions:
- "Map not found" → Check map name and mapset
- "Location not found" → Verify gisdbase and location paths
- "Command timed out" → Large datasets may need longer processing
- "Permission denied" → Check file/directory permissions

---

## Performance Notes

**Typical execution times (NC sample dataset):**
- `grass_raster_info`: < 1 second
- `grass_slope_aspect`: 2-5 seconds
- `grass_watershed`: 10-30 seconds
- `grass_viewshed`: 5-15 seconds
- `grass_visualize_raster`: 3-10 seconds

**Timeout limits:**
- Default commands: 60 seconds
- Watershed analysis: 300 seconds
- Import operations: 600 seconds
- Generic execute: 600 seconds

---

## Further Reading

- **GRASS GIS Manual:** https://grass.osgeo.org/grass-devel/manuals/
- **Raster commands:** https://grass.osgeo.org/grass-devel/manuals/raster.html
- **Vector commands:** https://grass.osgeo.org/grass-devel/manuals/vector.html
- **Image processing:** https://grass.osgeo.org/grass-devel/manuals/imagery.html

---

## Summary

**17 tools organized in 4 categories:**

1. **Core (8):** Essential GIS operations
2. **Visualization (3):** Map rendering and export
3. **Advanced (5):** Specialized analysis (hydrology, visibility, classification)
4. **Universal (1):** Access to ALL 500+ GRASS commands

**Coverage:**
- Direct: 17 specialized tools for common operations
- Universal: 500+ commands via `grass_execute`
- Total: Complete GRASS GIS functionality

**Best Practice:** Use dedicated tools when available, `grass_execute` for everything else.
