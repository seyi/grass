#!/usr/bin/env python3
"""
Proof of Concept: Map Visualization for GRASS GIS MCP Server

This demonstrates multiple approaches to adding visualization capabilities:
1. grass.jupyter - GRASS native Python visualization
2. matplotlib + rasterio - Python geospatial stack
3. Folium - Interactive web maps
"""

import subprocess
import os
import sys
from pathlib import Path


def run_grass_command(cmd, gisdbase, location, mapset="PERMANENT"):
    """Execute a GRASS command."""
    grass_cmd = ["grass", f"{gisdbase}/{location}/{mapset}", "--exec"] + cmd
    result = subprocess.run(grass_cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        raise Exception(f"GRASS command failed: {result.stderr}")
    return result.stdout.strip()


# =============================================================================
# Approach 1: grass.jupyter (GRASS 8.0+)
# =============================================================================

def visualize_with_grass_jupyter(map_name, output_path, gisdbase, location):
    """
    Use grass.jupyter for visualization (if available).
    This is the simplest approach for GRASS 8.0+
    """
    print("\n" + "="*70)
    print("Approach 1: grass.jupyter Visualization")
    print("="*70)

    try:
        # Check if grass.jupyter is available
        import grass.script as gs
        import grass.jupyter as gj

        print(f"✓ grass.jupyter is available")
        print(f"Creating visualization of '{map_name}'...")

        # Initialize GRASS session
        # Note: This would need proper initialization in production
        os.environ['GISDBASE'] = gisdbase
        os.environ['LOCATION_NAME'] = location
        os.environ['MAPSET'] = 'PERMANENT'

        # Create map
        terrain_map = gj.Map(width=800, height=600)
        terrain_map.d_rast(map=map_name)
        terrain_map.d_legend(raster=map_name, at=(2, 30, 2, 6))
        terrain_map.d_barscale(length=1000, at=(80, 5))

        # Save
        terrain_map.save(output_path)
        print(f"✓ Saved visualization to: {output_path}")
        return output_path

    except ImportError:
        print("✗ grass.jupyter not available (requires GRASS 8.0+)")
        print("  Install with: pip install grass-session")
        return None
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


# =============================================================================
# Approach 2: matplotlib + rasterio
# =============================================================================

def visualize_with_matplotlib(map_name, output_path, gisdbase, location,
                              colormap='terrain', add_hillshade=False):
    """
    Use matplotlib and rasterio for custom visualization.
    Most flexible approach with full control.
    """
    print("\n" + "="*70)
    print("Approach 2: matplotlib + rasterio Visualization")
    print("="*70)

    try:
        import matplotlib.pyplot as plt
        import matplotlib.colors as mcolors
        from matplotlib import patheffects
        import numpy as np
        print("✓ matplotlib available")
    except ImportError:
        print("✗ matplotlib not available")
        print("  Install with: pip install matplotlib")
        return None

    try:
        import rasterio
        from rasterio.plot import show
        print("✓ rasterio available")
    except ImportError:
        print("✗ rasterio not available")
        print("  Install with: pip install rasterio")
        return None

    try:
        # Export GRASS raster to GeoTIFF
        temp_tif = "/tmp/grass_export.tif"
        print(f"Exporting '{map_name}' to GeoTIFF...")
        run_grass_command(
            ["r.out.gdal", f"input={map_name}",
             f"output={temp_tif}", "format=GTiff", "-c", "--overwrite"],
            gisdbase, location
        )

        # Optional: Create hillshade for terrain visualization
        hillshade_tif = None
        if add_hillshade:
            print("Creating hillshade...")
            hillshade_map = f"{map_name}_hillshade_temp"
            run_grass_command(
                ["r.relief", f"input={map_name}",
                 f"output={hillshade_map}", "--overwrite"],
                gisdbase, location
            )
            hillshade_tif = "/tmp/hillshade_export.tif"
            run_grass_command(
                ["r.out.gdal", f"input={hillshade_map}",
                 f"output={hillshade_tif}", "format=GTiff", "--overwrite"],
                gisdbase, location
            )

        # Read with rasterio and visualize
        print("Creating visualization...")
        with rasterio.open(temp_tif) as src:
            data = src.read(1, masked=True)
            bounds = src.bounds
            crs = src.crs

            # Create figure
            fig, ax = plt.subplots(figsize=(12, 10))

            # Add hillshade if requested
            if hillshade_tif:
                with rasterio.open(hillshade_tif) as hs_src:
                    hillshade = hs_src.read(1)
                    ax.imshow(hillshade, cmap='gray', alpha=0.3,
                             extent=[bounds.left, bounds.right,
                                    bounds.bottom, bounds.top])

            # Plot main raster
            im = ax.imshow(data, cmap=colormap, alpha=0.8 if hillshade_tif else 1.0,
                          extent=[bounds.left, bounds.right,
                                 bounds.bottom, bounds.top])

            # Add colorbar with stats
            cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
            cbar.set_label(f'{map_name}\nElevation (m)', rotation=270, labelpad=20)

            # Add statistics text
            stats_text = f"Min: {np.nanmin(data):.1f}\n"
            stats_text += f"Max: {np.nanmax(data):.1f}\n"
            stats_text += f"Mean: {np.nanmean(data):.1f}"
            ax.text(0.02, 0.98, stats_text,
                   transform=ax.transAxes,
                   verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
                   fontsize=10)

            # Add title
            title = f'GRASS GIS Raster: {map_name}'
            if add_hillshade:
                title += ' (with hillshade)'
            ax.set_title(title, fontsize=14, weight='bold', pad=20)

            # Add coordinate labels
            ax.set_xlabel(f'Easting (m) - {crs}', fontsize=10)
            ax.set_ylabel(f'Northing (m)', fontsize=10)

            # Add grid
            ax.grid(True, alpha=0.3, linestyle='--')

            # Add north arrow
            x, y = 0.95, 0.95
            arrow_props = dict(arrowstyle='->', lw=2, color='black')
            ax.annotate('N', xy=(x, y), xytext=(x, y-0.05),
                       xycoords='axes fraction',
                       ha='center', va='center',
                       fontsize=14, weight='bold',
                       arrowprops=arrow_props)

            # Save
            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            plt.close()

            print(f"✓ Saved visualization to: {output_path}")
            return output_path

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


# =============================================================================
# Approach 3: Folium for Interactive Maps
# =============================================================================

def visualize_with_folium(map_name, output_path, gisdbase, location):
    """
    Create interactive web map using Folium.
    Best for exploration and sharing.
    """
    print("\n" + "="*70)
    print("Approach 3: Folium Interactive Map")
    print("="*70)

    try:
        import folium
        from folium import plugins
        print("✓ folium available")
    except ImportError:
        print("✗ folium not available")
        print("  Install with: pip install folium")
        return None

    try:
        import rasterio
        from rasterio.warp import transform_bounds
        print("✓ rasterio available")
    except ImportError:
        print("✗ rasterio not available")
        return None

    try:
        # Export to GeoTIFF
        temp_tif = "/tmp/grass_export_folium.tif"
        print(f"Exporting '{map_name}'...")
        run_grass_command(
            ["r.out.gdal", f"input={map_name}",
             f"output={temp_tif}", "format=GTiff", "--overwrite"],
            gisdbase, location
        )

        # Get bounds and reproject to WGS84 for Leaflet
        with rasterio.open(temp_tif) as src:
            bounds = src.bounds
            src_crs = src.crs

            # Transform bounds to WGS84
            wgs84_bounds = transform_bounds(src_crs, 'EPSG:4326',
                                           bounds.left, bounds.bottom,
                                           bounds.right, bounds.top)

            # Calculate center
            center_lat = (wgs84_bounds[1] + wgs84_bounds[3]) / 2
            center_lon = (wgs84_bounds[0] + wgs84_bounds[2]) / 2

        print(f"Creating interactive map centered at ({center_lat:.4f}, {center_lon:.4f})...")

        # Create folium map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=12,
            tiles='OpenStreetMap',
            control_scale=True
        )

        # Add layer control
        folium.TileLayer('CartoDB positron', name='Light Map').add_to(m)
        folium.TileLayer('CartoDB dark_matter', name='Dark Map').add_to(m)

        # Add rectangle showing data extent
        folium.Rectangle(
            bounds=[[wgs84_bounds[1], wgs84_bounds[0]],
                   [wgs84_bounds[3], wgs84_bounds[2]]],
            color='red',
            fill=True,
            fill_opacity=0.1,
            popup=f'GRASS Raster: {map_name}',
            tooltip='Data Extent'
        ).add_to(m)

        # Add marker at center
        folium.Marker(
            [center_lat, center_lon],
            popup=f'<b>{map_name}</b><br>GRASS GIS Raster',
            tooltip='Map Center',
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)

        # Add mouse position plugin
        plugins.MousePosition().add_to(m)

        # Add fullscreen button
        plugins.Fullscreen().add_to(m)

        # Add layer control
        folium.LayerControl().add_to(m)

        # Add custom HTML for map info
        legend_html = f'''
        <div style="position: fixed;
                    bottom: 50px; right: 50px; width: 250px; height: auto;
                    background-color: white; border:2px solid grey; z-index:9999;
                    font-size:14px; padding: 10px">
        <h4 style="margin-top:0">GRASS GIS Map</h4>
        <p><b>Map:</b> {map_name}</p>
        <p><b>Location:</b> {location}</p>
        <p><b>CRS:</b> {src_crs}</p>
        <p style="font-size:10px; margin-bottom:0">
        <i>Note: Full raster rendering requires tile generation</i>
        </p>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))

        # Save
        m.save(output_path)
        print(f"✓ Saved interactive map to: {output_path}")
        print(f"  Open in browser: file://{os.path.abspath(output_path)}")
        return output_path

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


# =============================================================================
# Main Test Function
# =============================================================================

def main():
    """Test all visualization approaches."""
    print("="*70)
    print("GRASS GIS Visualization Proof of Concept")
    print("="*70)
    print("\nTesting multiple approaches for map visualization:")
    print("  1. grass.jupyter (GRASS native)")
    print("  2. matplotlib + rasterio (Python geospatial stack)")
    print("  3. Folium (Interactive web maps)")
    print()

    # Configuration
    gisdbase = "/home/user/grassdata"
    location = "nc_spm_08_grass7"
    map_name = "elevation"
    output_dir = "/tmp/grass_viz_test"

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    print(f"Dataset: {location}")
    print(f"Map: {map_name}")
    print(f"Output directory: {output_dir}\n")

    results = []

    # Test Approach 1: grass.jupyter
    output1 = os.path.join(output_dir, "elevation_grass_jupyter.png")
    result1 = visualize_with_grass_jupyter(map_name, output1, gisdbase, location)
    if result1:
        results.append(("grass.jupyter", result1))

    # Test Approach 2: matplotlib (simple)
    output2 = os.path.join(output_dir, "elevation_matplotlib_simple.png")
    result2 = visualize_with_matplotlib(map_name, output2, gisdbase, location,
                                       colormap='terrain', add_hillshade=False)
    if result2:
        results.append(("matplotlib (simple)", result2))

    # Test Approach 2b: matplotlib (with hillshade)
    output2b = os.path.join(output_dir, "elevation_matplotlib_hillshade.png")
    result2b = visualize_with_matplotlib(map_name, output2b, gisdbase, location,
                                        colormap='terrain', add_hillshade=True)
    if result2b:
        results.append(("matplotlib (hillshade)", result2b))

    # Test Approach 3: Folium
    output3 = os.path.join(output_dir, "elevation_folium_interactive.html")
    result3 = visualize_with_folium(map_name, output3, gisdbase, location)
    if result3:
        results.append(("folium (interactive)", result3))

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"\nGenerated {len(results)} visualization(s):\n")
    for i, (method, path) in enumerate(results, 1):
        print(f"  {i}. {method:25s} → {path}")

    if results:
        print("\n✓ Visualization POC successful!")
        print("\nNext Steps:")
        print("  1. Choose preferred approach(es)")
        print("  2. Integrate into GRASS MCP server as new tool")
        print("  3. Add MCP tool schema for grass_visualize_map")
        print("  4. Test with Claude Desktop")
    else:
        print("\n✗ No visualizations generated")
        print("  Install required packages:")
        print("    pip install matplotlib rasterio folium")

    return len(results) > 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
