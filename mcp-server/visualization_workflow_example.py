#!/usr/bin/env python3
"""
Example: GRASS GIS Visualization Workflow for MCP Server

This script demonstrates how the MCP server would handle visualization requests.
"""

def grass_visualize_raster(map_name, output_path, gisdbase, location):
    """
    Visualize a GRASS raster map.

    Workflow:
    1. Export GRASS raster to GeoTIFF
    2. Read with rasterio/GDAL
    3. Render with matplotlib
    4. Add cartographic elements (legend, scale, north arrow)
    5. Save to PNG
    """
    import subprocess

    # Step 1: Export from GRASS
    temp_tif = "/tmp/temp_export.tif"
    cmd = ["grass", f"{gisdbase}/{location}/PERMANENT", "--exec",
           "r.out.gdal", f"input={map_name}", f"output={temp_tif}",
           "format=GTiff", "--overwrite"]
    subprocess.run(cmd, check=True)

    # Step 2-5: Visualization (requires matplotlib/rasterio)
    # See grass_visualization_addon.py for full implementation

    return f"Visualization saved to {output_path}"


def grass_create_interactive_map(map_name, output_path, gisdbase, location):
    """
    Create an interactive HTML map.

    Workflow:
    1. Export GRASS raster to GeoTIFF
    2. Get bounds and reproject to WGS84
    3. Create Folium map
    4. Add data extent rectangle
    5. Add interactive controls
    6. Save to HTML
    """
    import subprocess

    # Step 1: Export from GRASS
    temp_tif = "/tmp/temp_export.tif"
    cmd = ["grass", f"{gisdbase}/{location}/PERMANENT", "--exec",
           "r.out.gdal", f"input={map_name}", f"output={temp_tif}",
           "format=GTiff", "--overwrite"]
    subprocess.run(cmd, check=True)

    # Steps 2-6: Interactive map creation
    # See grass_visualization_addon.py for full implementation

    return f"Interactive map saved to {output_path}"


# Example usage in MCP server:
if __name__ == "__main__":
    # When Claude asks: "Create a visualization of elevation"
    result = grass_visualize_raster(
        map_name="elevation",
        output_path="/tmp/elevation_viz.png",
        gisdbase="/home/user/grassdata",
        location="nc_spm_08_grass7"
    )
    print(result)

    # When Claude asks: "Create an interactive map of landuse"
    result = grass_create_interactive_map(
        map_name="landuse96_28m",
        output_path="/tmp/landuse.html",
        gisdbase="/home/user/grassdata",
        location="nc_spm_08_grass7"
    )
    print(result)
