# GRASS GIS MCP Server - Usage Guide

This guide provides detailed examples of using the GRASS GIS MCP Server.

## Quick Start

### 1. Verify GRASS Installation

```bash
grass --version
```

You should see output like: `GRASS GIS 8.x.x`

### 2. Set Up a GRASS Location

If you don't have a GRASS location yet, create one:

```bash
# Create a location with WGS84 (EPSG:4326)
grass -c EPSG:4326 ~/grassdata/world

# Or create with UTM Zone 17N (EPSG:32617)
grass -c EPSG:32617 ~/grassdata/utm17n

# Or use the North Carolina sample dataset
# Download from: https://grass.osgeo.org/sampledata/north_carolina/nc_spm_08_grass7.zip
# Extract to ~/grassdata/
```

### 3. Install and Run the MCP Server

```bash
cd mcp-server
pip install -r requirements.txt
python grass_mcp_server.py
```

## Common Workflows

### Workflow 1: Analyzing Digital Elevation Models

**Scenario**: You have a DEM and want to analyze terrain characteristics.

#### Step 1: Get information about your DEM

Ask the AI:
```
"Get information about the elevation raster in my North Carolina location at /home/user/grassdata/nc_spm_08"
```

The AI will use `grass_raster_info` with:
- map_name: "elevation"
- gisdbase: "/home/user/grassdata"
- location: "nc_spm_08"
- mapset: "PERMANENT"

#### Step 2: Calculate statistics

```
"Calculate extended statistics for the elevation map"
```

Uses `grass_raster_univar` with extended=true.

#### Step 3: Calculate slope and aspect

```
"Calculate slope and aspect from the elevation map, save as slope_degrees and aspect_degrees"
```

Uses `grass_slope_aspect`.

#### Step 4: Verify the results

```
"Get information about the slope_degrees map"
```

Uses `grass_raster_info` again to verify the output.

### Workflow 2: Vector Buffer Analysis

**Scenario**: Find areas within a certain distance of features.

#### Step 1: List available vector maps

```
"List all vector maps in my location"
```

Uses `grass_list_maps` with map_type="vector".

#### Step 2: Get vector information

```
"Get information about the roads vector map"
```

Uses `grass_vector_info`.

#### Step 3: Create buffer

```
"Create a 1000-meter buffer around the roads"
```

Uses `grass_buffer` with distance=1000.

### Workflow 3: Raster Map Algebra

**Scenario**: Create derived maps using mathematical operations.

#### Step 1: List available rasters

```
"Show me all raster maps"
```

#### Step 2: Create a new map with calculations

```
"Create a new raster called elevation_feet that converts elevation from meters to feet (multiply by 3.28084)"
```

Uses `grass_mapcalc` with:
- expression: "elevation_feet = elevation * 3.28084"

#### Step 3: Create a hillshade

```
"Create a hillshade from the elevation map"
```

This would require adding a new tool or using mapcalc with the appropriate formula.

### Workflow 4: Region Management

**Scenario**: Understanding and working with the computational region.

#### Step 1: Check current region

```
"What is the current computational region?"
```

Uses `grass_region_info`.

#### Step 2: Work within the region

All raster operations respect the current computational region settings (resolution, extent).

## Advanced Examples

### Example 1: Normalized Difference Vegetation Index (NDVI)

If you have multispectral imagery:

```
"Calculate NDVI using the formula (nir - red) / (nir + red) and save as ndvi_map"
```

Uses `grass_mapcalc` with:
```
expression: "ndvi_map = float(nir - red) / float(nir + red)"
```

### Example 2: Slope Classification

```
"Create a slope classification map where slopes are categorized as: flat (0-5 degrees), gentle (5-15), moderate (15-30), and steep (>30)"
```

Uses `grass_mapcalc` with conditional logic:
```
expression: "slope_class = if(slope_degrees < 5, 1, if(slope_degrees < 15, 2, if(slope_degrees < 30, 3, 4)))"
```

### Example 3: Proximity Analysis

```
"Create buffers at 100, 500, and 1000 meters around water features"
```

Would use `grass_buffer` multiple times with different distances.

## Tool-Specific Details

### grass_raster_info

**Returns**:
- north, south, east, west (extent)
- nsres, ewres (resolution)
- rows, cols (dimensions)
- min, max (data range)
- datatype (cell type)

**Example output**:
```
north=228500
south=215000
east=645000
west=630000
nsres=10
ewres=10
rows=1350
cols=1500
min=55.5787925720215
max=156.3299102783203
datatype=FCELL
```

### grass_vector_info

**Returns**:
- num_points, num_lines, num_boundaries, num_centroids, num_areas
- north, south, east, west (extent)
- map_3d (whether map is 3D)
- num_dblinks (database connections)

### grass_mapcalc

**Supports**:
- Arithmetic: +, -, *, /, %
- Functions: sqrt(), log(), exp(), sin(), cos(), etc.
- Conditionals: if(condition, true_value, false_value)
- Logical: &&, ||, !
- Comparison: <, >, <=, >=, ==, !=

**Syntax**: `output = expression`

**Examples**:
```
"result = (a + b) / 2"                    # Average of two maps
"high_elev = if(elevation > 1000, 1, 0)"  # Binary classification
"normalized = (map - 100) / 50"           # Normalization
```

### grass_buffer

**Distance units**: Same as the location's coordinate system
- For lat/lon (EPSG:4326): degrees
- For projected (e.g., UTM): meters

**Note**: For lat/lon, consider using a projected CRS for accurate distance buffers.

## Tips and Best Practices

### 1. Use Consistent Paths

Always use absolute paths for gisdbase to avoid confusion:
```
✓ "/home/user/grassdata"
✗ "~/grassdata"
✗ "../grassdata"
```

### 2. Check Map Existence First

Before operating on maps, list them or get info to verify they exist:
```
"List all raster maps in my location"
"Get info about elevation"
```

### 3. Understand Your Coordinate System

Different operations make sense in different coordinate systems:
- **Lat/lon (degrees)**: Good for global data, bad for distance calculations
- **Projected (meters/feet)**: Good for local analysis, distance calculations
- **UTM**: Good compromise for regional analysis

### 4. Start with Info Commands

When exploring new data:
1. `grass_list_maps` - See what's available
2. `grass_region_info` - Understand the computational area
3. `grass_raster_info` or `grass_vector_info` - Examine specific maps

### 5. Verify Results

After creating new maps, check them:
```
"After creating slope_map, get its information"
"Calculate statistics for the new buffer map"
```

## Troubleshooting

### "Map not found" errors

1. Verify the map exists: `grass_list_maps`
2. Check you're using the correct mapset
3. Ensure map name is spelled correctly (case-sensitive)

### "Cannot open database" errors

1. Verify gisdbase path exists
2. Check location name is correct
3. Ensure mapset exists (default: PERMANENT)
4. Check read/write permissions

### Unexpected results with buffers

1. Check your coordinate system (g_region_info)
2. For lat/lon, use small distance values (degrees)
3. For meters, ensure your location is projected

### Map algebra errors

1. Verify all input maps exist
2. Check map names don't contain special characters
3. Ensure mathematical operations are valid for data types
4. Use float() for division to avoid integer division

## Next Steps

1. **Explore Sample Data**: Download the North Carolina sample dataset
2. **Learn GRASS Commands**: Visit https://grass.osgeo.org/grass-devel/manuals/
3. **Extend the Server**: Add more tools by editing grass_mcp_server.py
4. **Automate Workflows**: Chain multiple tools together for complex analyses

## Resources

- GRASS Tutorials: https://grass.osgeo.org/learn/tutorials/
- GRASS Wiki: https://grasswiki.osgeo.org/
- MCP Documentation: https://modelcontextprotocol.io/
