#!/usr/bin/env python3
"""
GRASS GIS MCP Server - Visualization Add-on

This module extends the GRASS GIS MCP server with map visualization capabilities.
It can be integrated into the main server or used as a separate visualization service.

Author: Claude
Date: 2025-11-06
"""

from mcp.server import Server
from mcp.types import Tool, TextContent
import subprocess
import os
import tempfile
from pathlib import Path


# =============================================================================
# Visualization Tool Definitions
# =============================================================================

VISUALIZATION_TOOLS = [
    Tool(
        name="grass_visualize_raster",
        description=(
            "Create a visualization (PNG image) of a GRASS raster map. "
            "Exports the map with optional styling, legend, scale bar, and north arrow."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "map_name": {
                    "type": "string",
                    "description": "Name of the raster map to visualize",
                },
                "output_path": {
                    "type": "string",
                    "description": "Path where the PNG image should be saved",
                },
                "width": {
                    "type": "integer",
                    "description": "Image width in pixels (default: 800)",
                    "default": 800,
                },
                "height": {
                    "type": "integer",
                    "description": "Image height in pixels (default: 600)",
                    "default": 600,
                },
                "style": {
                    "type": "string",
                    "description": "Visualization style",
                    "enum": ["simple", "hillshade", "terrain", "classified"],
                    "default": "simple",
                },
                "add_legend": {
                    "type": "boolean",
                    "description": "Add color legend (default: true)",
                    "default": True,
                },
                "add_scalebar": {
                    "type": "boolean",
                    "description": "Add scale bar (default: true)",
                    "default": True,
                },
                "add_north_arrow": {
                    "type": "boolean",
                    "description": "Add north arrow (default: true)",
                    "default": True,
                },
                "gisdbase": {
                    "type": "string",
                    "description": "Path to GRASS GIS database directory",
                },
                "location": {
                    "type": "string",
                    "description": "GRASS location name",
                },
                "mapset": {
                    "type": "string",
                    "description": "GRASS mapset name (default: PERMANENT)",
                    "default": "PERMANENT",
                },
            },
            "required": ["map_name", "output_path", "gisdbase", "location"],
        },
    ),
    Tool(
        name="grass_create_composite",
        description=(
            "Create a composite visualization combining multiple raster layers "
            "(e.g., elevation with hillshade overlay)."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "base_map": {
                    "type": "string",
                    "description": "Base raster map (e.g., elevation)",
                },
                "overlay_map": {
                    "type": "string",
                    "description": "Optional overlay map (e.g., hillshade)",
                },
                "output_path": {
                    "type": "string",
                    "description": "Output PNG path",
                },
                "gisdbase": {"type": "string"},
                "location": {"type": "string"},
            },
            "required": ["base_map", "output_path", "gisdbase", "location"],
        },
    ),
    Tool(
        name="grass_create_interactive_map",
        description=(
            "Create an interactive HTML map that can be opened in a web browser. "
            "Allows pan, zoom, and layer toggling."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "map_name": {
                    "type": "string",
                    "description": "Raster map to visualize",
                },
                "output_path": {
                    "type": "string",
                    "description": "Output HTML file path",
                },
                "gisdbase": {"type": "string"},
                "location": {"type": "string"},
            },
            "required": ["map_name", "output_path", "gisdbase", "location"],
        },
    ),
]


# =============================================================================
# Helper Functions
# =============================================================================

def run_grass_command(cmd, gisdbase, location, mapset="PERMANENT", timeout=60):
    """Execute a GRASS command in the specified location."""
    grass_cmd = ["grass", f"{gisdbase}/{location}/{mapset}", "--exec"] + cmd
    result = subprocess.run(
        grass_cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        env=dict(os.environ, GRASS_BATCH_JOB="1")
    )
    if result.returncode != 0:
        raise Exception(f"GRASS command failed: {result.stderr}")
    return result.stdout


# =============================================================================
# Visualization Implementations
# =============================================================================

def visualize_raster_simple(map_name, output_path, gisdbase, location,
                            width=800, height=600, add_legend=True,
                            add_scalebar=True, add_north_arrow=True):
    """
    Create a simple raster visualization using matplotlib.
    This is the most reliable cross-platform approach.
    """
    try:
        import matplotlib.pyplot as plt
        import rasterio
        from rasterio.plot import show
        import numpy as np
    except ImportError as e:
        return f"Required package not available: {e}. Install with: pip install matplotlib rasterio"

    # Export to temporary GeoTIFF
    with tempfile.NamedTemporaryFile(suffix='.tif', delete=False) as tmp:
        temp_tif = tmp.name

    try:
        # Export GRASS raster
        run_grass_command(
            ["r.out.gdal", f"input={map_name}", f"output={temp_tif}",
             "format=GTiff", "--overwrite"],
            gisdbase, location
        )

        # Read and visualize
        with rasterio.open(temp_tif) as src:
            data = src.read(1, masked=True)
            bounds = src.bounds

            # Create figure
            fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)

            # Plot raster
            im = show(src, ax=ax, cmap='terrain')

            # Add colorbar/legend
            if add_legend:
                cbar = plt.colorbar(ax.images[0], ax=ax, fraction=0.046)
                cbar.set_label(map_name, rotation=270, labelpad=15)

            # Add scale bar (simplified)
            if add_scalebar:
                scalebar_len = (bounds.right - bounds.left) / 5
                ax.plot([bounds.left + 100, bounds.left + 100 + scalebar_len],
                       [bounds.bottom + 100, bounds.bottom + 100],
                       'k-', linewidth=3)
                ax.text(bounds.left + 100 + scalebar_len/2, bounds.bottom + 200,
                       f'{scalebar_len:.0f} m', ha='center')

            # Add north arrow
            if add_north_arrow:
                ax.annotate('N', xy=(0.95, 0.95), xytext=(0.95, 0.90),
                           xycoords='axes fraction', ha='center',
                           arrowprops=dict(arrowstyle='->', lw=2),
                           fontsize=14, weight='bold')

            # Title
            ax.set_title(f'GRASS Raster: {map_name}', fontsize=12, pad=10)

            # Save
            plt.tight_layout()
            plt.savefig(output_path, dpi=100, bbox_inches='tight')
            plt.close()

            return f"Successfully created visualization: {output_path}"

    finally:
        # Cleanup
        if os.path.exists(temp_tif):
            os.unlink(temp_tif)


def visualize_with_hillshade(elevation_map, output_path, gisdbase, location):
    """Create terrain visualization with hillshade overlay."""
    try:
        import matplotlib.pyplot as plt
        import rasterio
        import numpy as np
    except ImportError as e:
        return f"Required package not available: {e}"

    # Create temporary hillshade
    hillshade_name = f"_temp_hillshade_{os.getpid()}"

    try:
        # Generate hillshade
        run_grass_command(
            ["r.relief", f"input={elevation_map}", f"output={hillshade_name}",
             "--overwrite"],
            gisdbase, location
        )

        # Export both to GeoTIFFs
        with tempfile.TemporaryDirectory() as tmpdir:
            elev_tif = os.path.join(tmpdir, "elev.tif")
            hs_tif = os.path.join(tmpdir, "hillshade.tif")

            run_grass_command(
                ["r.out.gdal", f"input={elevation_map}", f"output={elev_tif}",
                 "--overwrite"],
                gisdbase, location
            )
            run_grass_command(
                ["r.out.gdal", f"input={hillshade_name}", f"output={hs_tif}",
                 "--overwrite"],
                gisdbase, location
            )

            # Visualize with matplotlib
            with rasterio.open(elev_tif) as elev_src, \
                 rasterio.open(hs_tif) as hs_src:

                elev_data = elev_src.read(1, masked=True)
                hs_data = hs_src.read(1)
                bounds = elev_src.bounds

                fig, ax = plt.subplots(figsize=(12, 10))

                # Plot hillshade
                ax.imshow(hs_data, cmap='gray', alpha=0.5,
                         extent=[bounds.left, bounds.right,
                                bounds.bottom, bounds.top])

                # Plot elevation with transparency
                im = ax.imshow(elev_data, cmap='terrain', alpha=0.7,
                              extent=[bounds.left, bounds.right,
                                     bounds.bottom, bounds.top])

                # Colorbar
                cbar = plt.colorbar(im, ax=ax)
                cbar.set_label('Elevation (m)', rotation=270, labelpad=15)

                ax.set_title(f'Terrain: {elevation_map} with Hillshade')
                plt.tight_layout()
                plt.savefig(output_path, dpi=300, bbox_inches='tight')
                plt.close()

        return f"Created hillshade visualization: {output_path}"

    finally:
        # Cleanup temporary hillshade
        try:
            run_grass_command(
                ["g.remove", "type=raster", f"name={hillshade_name}", "-f"],
                gisdbase, location
            )
        except:
            pass


def create_interactive_map(map_name, output_path, gisdbase, location):
    """Create interactive HTML map using Folium."""
    try:
        import folium
        from folium import plugins
        import rasterio
        from rasterio.warp import transform_bounds
    except ImportError as e:
        return f"Required package not available: {e}. Install: pip install folium"

    with tempfile.NamedTemporaryFile(suffix='.tif', delete=False) as tmp:
        temp_tif = tmp.name

    try:
        # Export raster
        run_grass_command(
            ["r.out.gdal", f"input={map_name}", f"output={temp_tif}",
             "format=GTiff", "--overwrite"],
            gisdbase, location
        )

        # Get bounds in WGS84
        with rasterio.open(temp_tif) as src:
            bounds = src.bounds
            src_crs = src.crs

            wgs84_bounds = transform_bounds(src_crs, 'EPSG:4326',
                                           bounds.left, bounds.bottom,
                                           bounds.right, bounds.top)

            center_lat = (wgs84_bounds[1] + wgs84_bounds[3]) / 2
            center_lon = (wgs84_bounds[0] + wgs84_bounds[2]) / 2

        # Create map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=13,
            tiles='OpenStreetMap'
        )

        # Add data extent rectangle
        folium.Rectangle(
            bounds=[[wgs84_bounds[1], wgs84_bounds[0]],
                   [wgs84_bounds[3], wgs84_bounds[2]]],
            color='red',
            fill=True,
            fill_opacity=0.2,
            popup=f'GRASS Raster: {map_name}'
        ).add_to(m)

        # Add plugins
        plugins.MousePosition().add_to(m)
        plugins.Fullscreen().add_to(m)

        # Add info box
        info_html = f'''
        <div style="position: fixed; bottom: 50px; right: 50px;
                    background-color: white; border: 2px solid grey;
                    padding: 10px; z-index: 9999;">
        <h4>GRASS GIS Map</h4>
        <p><b>Map:</b> {map_name}</p>
        <p><b>Location:</b> {location}</p>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(info_html))

        # Save
        m.save(output_path)

        return f"Created interactive map: {output_path}"

    finally:
        if os.path.exists(temp_tif):
            os.unlink(temp_tif)


# =============================================================================
# MCP Tool Handler
# =============================================================================

async def handle_visualization_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle visualization tool calls."""

    try:
        if name == "grass_visualize_raster":
            style = arguments.get("style", "simple")

            if style == "hillshade" or style == "terrain":
                result = visualize_with_hillshade(
                    arguments["map_name"],
                    arguments["output_path"],
                    arguments["gisdbase"],
                    arguments["location"]
                )
            else:
                result = visualize_raster_simple(
                    arguments["map_name"],
                    arguments["output_path"],
                    arguments["gisdbase"],
                    arguments["location"],
                    width=arguments.get("width", 800),
                    height=arguments.get("height", 600),
                    add_legend=arguments.get("add_legend", True),
                    add_scalebar=arguments.get("add_scalebar", True),
                    add_north_arrow=arguments.get("add_north_arrow", True)
                )

        elif name == "grass_create_composite":
            result = visualize_with_hillshade(
                arguments["base_map"],
                arguments["output_path"],
                arguments["gisdbase"],
                arguments["location"]
            )

        elif name == "grass_create_interactive_map":
            result = create_interactive_map(
                arguments["map_name"],
                arguments["output_path"],
                arguments["gisdbase"],
                arguments["location"]
            )

        else:
            result = f"Unknown tool: {name}"

        return [TextContent(type="text", text=result)]

    except Exception as e:
        error_msg = f"Error in {name}: {str(e)}"
        return [TextContent(type="text", text=error_msg)]


# =============================================================================
# Integration Instructions
# =============================================================================

"""
INTEGRATION INTO EXISTING GRASS MCP SERVER:

1. Add visualization tools to the tools list:

    from grass_visualization_addon import VISUALIZATION_TOOLS

    # In list_tools handler:
    return ListToolsResult(tools=GRASS_TOOLS + VISUALIZATION_TOOLS)

2. Add visualization tool handler to call_tool:

    from grass_visualization_addon import handle_visualization_tool

    # In call_tool handler:
    if name.startswith("grass_visualize") or name == "grass_create_interactive_map":
        return await handle_visualization_tool(name, arguments)

3. Install dependencies:

    pip install matplotlib rasterio folium

4. Usage examples in Claude Desktop:

    "Create a visualization of the elevation map and save it to /tmp/elevation.png"

    "Make an interactive map of the landuse raster and save as /tmp/landuse.html"

    "Create a hillshade visualization of elevation at /tmp/terrain.png"
"""

if __name__ == "__main__":
    print("GRASS GIS Visualization Add-on")
    print("=" * 60)
    print(f"Available tools: {len(VISUALIZATION_TOOLS)}")
    for tool in VISUALIZATION_TOOLS:
        print(f"  - {tool.name}")
    print("\nSee module docstring for integration instructions.")
