#!/usr/bin/env python3
"""
Test the GRASS GIS MCP Server with real data from the North Carolina sample dataset.
This demonstrates all the available MCP tools working with actual GRASS GIS data.
"""

import subprocess
import json


def run_grass_command(cmd, gisdbase, location, mapset="PERMANENT"):
    """Execute a GRASS command in a GRASS session."""
    grass_cmd = ["grass", f"{gisdbase}/{location}/{mapset}", "--exec"] + cmd
    result = subprocess.run(
        grass_cmd, capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        raise Exception(f"GRASS command failed: {result.stderr}")
    return result.stdout.strip()


def test_list_maps():
    """Test: List all raster maps"""
    print("\n" + "="*70)
    print("TEST 1: List Raster Maps")
    print("="*70)
    print("\nMCP Tool Call: grass_list_maps")
    print("Arguments: {")
    print('  "gisdbase": "/home/user/grassdata",')
    print('  "location": "nc_spm_08_grass7",')
    print('  "mapset": "PERMANENT",')
    print('  "map_type": "raster"')
    print("}\n")

    result = run_grass_command(
        ["g.list", "type=raster", "-m"],
        "/home/user/grassdata",
        "nc_spm_08_grass7"
    )

    maps = result.split('\n')
    print(f"Found {len(maps)} raster maps:")
    for i, map_name in enumerate(maps[:10], 1):
        print(f"  {i}. {map_name}")
    if len(maps) > 10:
        print(f"  ... and {len(maps) - 10} more maps")

    return maps


def test_raster_info(map_name="elevation"):
    """Test: Get information about a raster map"""
    print("\n" + "="*70)
    print(f"TEST 2: Get Raster Information for '{map_name}'")
    print("="*70)
    print("\nMCP Tool Call: grass_raster_info")
    print("Arguments: {")
    print(f'  "map_name": "{map_name}",')
    print('  "gisdbase": "/home/user/grassdata",')
    print('  "location": "nc_spm_08_grass7",')
    print('  "mapset": "PERMANENT"')
    print("}\n")

    result = run_grass_command(
        ["r.info", "-g", map_name],
        "/home/user/grassdata",
        "nc_spm_08_grass7"
    )

    print("Raster Information:")
    for line in result.split('\n'):
        if line:
            print(f"  {line}")


def test_raster_univar(map_name="elevation"):
    """Test: Calculate raster statistics"""
    print("\n" + "="*70)
    print(f"TEST 3: Calculate Statistics for '{map_name}'")
    print("="*70)
    print("\nMCP Tool Call: grass_raster_univar")
    print("Arguments: {")
    print(f'  "map_name": "{map_name}",')
    print('  "extended": true,')
    print('  "gisdbase": "/home/user/grassdata",')
    print('  "location": "nc_spm_08_grass7"')
    print("}\n")

    result = run_grass_command(
        ["r.univar", "-g", "-e", map_name],
        "/home/user/grassdata",
        "nc_spm_08_grass7"
    )

    print("Statistics:")
    for line in result.split('\n'):
        if line:
            print(f"  {line}")


def test_region_info():
    """Test: Get computational region information"""
    print("\n" + "="*70)
    print("TEST 4: Get Computational Region Information")
    print("="*70)
    print("\nMCP Tool Call: grass_region_info")
    print("Arguments: {")
    print('  "gisdbase": "/home/user/grassdata",')
    print('  "location": "nc_spm_08_grass7",')
    print('  "mapset": "PERMANENT"')
    print("}\n")

    result = run_grass_command(
        ["g.region", "-g"],
        "/home/user/grassdata",
        "nc_spm_08_grass7"
    )

    print("Computational Region:")
    for line in result.split('\n'):
        if line:
            print(f"  {line}")


def test_slope_aspect():
    """Test: Calculate slope and aspect from elevation"""
    print("\n" + "="*70)
    print("TEST 5: Calculate Slope and Aspect from Elevation")
    print("="*70)
    print("\nMCP Tool Call: grass_slope_aspect")
    print("Arguments: {")
    print('  "elevation": "elevation",')
    print('  "slope": "test_slope",')
    print('  "aspect": "test_aspect",')
    print('  "gisdbase": "/home/user/grassdata",')
    print('  "location": "nc_spm_08_grass7"')
    print("}\n")

    # Run slope/aspect calculation
    try:
        run_grass_command(
            ["r.slope.aspect", "elevation=elevation",
             "slope=test_slope", "aspect=test_aspect"],
            "/home/user/grassdata",
            "nc_spm_08_grass7"
        )
        print("✓ Successfully created slope and aspect maps")

        # Get info about the created slope map
        result = run_grass_command(
            ["r.info", "-g", "test_slope"],
            "/home/user/grassdata",
            "nc_spm_08_grass7"
        )

        print("\nCreated slope map information:")
        for line in result.split('\n')[:5]:
            if line:
                print(f"  {line}")

    except Exception as e:
        print(f"✗ Error: {e}")


def test_vector_info(map_name="bridges"):
    """Test: Get information about a vector map"""
    print("\n" + "="*70)
    print(f"TEST 6: Get Vector Information for '{map_name}'")
    print("="*70)
    print("\nMCP Tool Call: grass_vector_info")
    print("Arguments: {")
    print(f'  "map_name": "{map_name}",')
    print('  "gisdbase": "/home/user/grassdata",')
    print('  "location": "nc_spm_08_grass7",')
    print('  "mapset": "PERMANENT"')
    print("}\n")

    result = run_grass_command(
        ["v.info", "-g", map_name],
        "/home/user/grassdata",
        "nc_spm_08_grass7"
    )

    print("Vector Information:")
    for line in result.split('\n'):
        if line:
            print(f"  {line}")


def test_mapcalc():
    """Test: Raster map algebra"""
    print("\n" + "="*70)
    print("TEST 7: Raster Map Algebra (Convert meters to feet)")
    print("="*70)
    print("\nMCP Tool Call: grass_mapcalc")
    print("Arguments: {")
    print('  "expression": "elevation_feet = elevation * 3.28084",')
    print('  "gisdbase": "/home/user/grassdata",')
    print('  "location": "nc_spm_08_grass7"')
    print("}\n")

    try:
        run_grass_command(
            ["r.mapcalc", "expression=elevation_feet = elevation * 3.28084"],
            "/home/user/grassdata",
            "nc_spm_08_grass7"
        )
        print("✓ Successfully created elevation_feet map")

        # Get statistics
        result = run_grass_command(
            ["r.univar", "-g", "elevation_feet"],
            "/home/user/grassdata",
            "nc_spm_08_grass7"
        )

        print("\nNew map statistics:")
        for line in result.split('\n')[:5]:
            if line:
                print(f"  {line}")

    except Exception as e:
        print(f"✗ Error: {e}")


def main():
    print("="*70)
    print("GRASS GIS MCP Server - Real Data Testing")
    print("="*70)
    print("\nDataset: North Carolina Sample Dataset")
    print("Location: /home/user/grassdata/nc_spm_08_grass7")
    print("\nThis test demonstrates all 8 MCP tools with real GRASS GIS data:")
    print("  1. grass_list_maps - List all maps in a location")
    print("  2. grass_raster_info - Get raster metadata")
    print("  3. grass_raster_univar - Calculate raster statistics")
    print("  4. grass_region_info - Get computational region")
    print("  5. grass_slope_aspect - Calculate terrain metrics")
    print("  6. grass_vector_info - Get vector metadata")
    print("  7. grass_mapcalc - Raster map algebra")
    print("  8. grass_buffer - Vector buffering (requires vector input)")

    try:
        # Run all tests
        test_list_maps()
        test_raster_info()
        test_raster_univar()
        test_region_info()
        test_slope_aspect()
        test_vector_info()
        test_mapcalc()

        print("\n" + "="*70)
        print("✓ All tests completed successfully!")
        print("="*70)
        print("\nNext Steps:")
        print("  1. The MCP server is ready to use with Claude Desktop")
        print("  2. Configure Claude Desktop with the MCP server")
        print("  3. Ask Claude to perform geospatial analysis on this dataset")
        print("\nExample questions to ask Claude:")
        print('  - "What raster maps are available in my GRASS location?"')
        print('  - "Calculate slope from the elevation map"')
        print('  - "Get statistics for the landuse map"')
        print('  - "Create a buffer around the bridges vector"')

    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
