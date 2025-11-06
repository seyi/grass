#!/usr/bin/env python3
"""
Demo: How the grass_list_maps tool works

This demonstrates what happens when Claude receives the request:
"List all raster maps in my GRASS location at /home/user/grassdata/nc_spm_08"
"""

import json

# This is what the MCP tool definition looks like
tool_definition = {
    "name": "grass_list_maps",
    "description": "List all maps in a GRASS GIS location",
    "inputSchema": {
        "type": "object",
        "properties": {
            "gisdbase": {
                "type": "string",
                "description": "Path to GRASS GIS database directory"
            },
            "location": {
                "type": "string",
                "description": "Name of the GRASS location"
            },
            "mapset": {
                "type": "string",
                "description": "Name of the mapset",
                "default": "PERMANENT"
            },
            "map_type": {
                "type": "string",
                "description": "Type of maps to list: 'raster', 'vector', 'raster_3d', or 'all'",
                "enum": ["raster", "vector", "raster_3d", "all"],
                "default": "all"
            }
        },
        "required": ["gisdbase", "location"]
    }
}

# This is how Claude would call the tool
tool_call = {
    "tool": "grass_list_maps",
    "arguments": {
        "gisdbase": "/home/user/grassdata",
        "location": "nc_spm_08",
        "mapset": "PERMANENT",
        "map_type": "raster"
    }
}

# This is the GRASS command that would be executed
grass_command = [
    "g.list",
    "type=raster",
    "mapset=PERMANENT",
    "-m"  # Show fully qualified map names
]

# This is what the output might look like from a real GRASS location
sample_output = """elevation@PERMANENT
aspect@PERMANENT
slope@PERMANENT
basin_50K@PERMANENT
boundary_county_500m@PERMANENT
elevation_shade@PERMANENT
geology_30m@PERMANENT
landclass96@PERMANENT
landcover_1m@PERMANENT
landuse96_28m@PERMANENT
lsat7_2002_10@PERMANENT
lsat7_2002_20@PERMANENT
lsat7_2002_30@PERMANENT
lsat7_2002_40@PERMANENT
lsat7_2002_50@PERMANENT
lsat7_2002_61@PERMANENT
lsat7_2002_62@PERMANENT
lsat7_2002_70@PERMANENT
lsat7_2002_80@PERMANENT
ortho_2001_t792_1m@PERMANENT
soilsID@PERMANENT
soils_Kfactor@PERMANENT
urban@PERMANENT
zipcodes@PERMANENT"""

# This is how the MCP server would format the response
mcp_response = {
    "content": [
        {
            "type": "text",
            "text": f"""Found {len(sample_output.split())} raster maps in location 'nc_spm_08':

{sample_output}

These maps include:
- Digital Elevation Models (elevation, aspect, slope)
- Satellite imagery (lsat7_2002_*)
- Land cover/use classifications (landcover_1m, landuse96_28m)
- Ortho photos (ortho_2001_t792_1m)
- Soil and geology data
- Administrative boundaries"""
        }
    ]
}

print("=" * 70)
print("DEMONSTRATION: grass_list_maps Tool")
print("=" * 70)
print()

print("1. USER REQUEST:")
print("   'List all raster maps in my GRASS location at /home/user/grassdata/nc_spm_08'")
print()

print("2. MCP TOOL CALLED:")
print(f"   Tool: {tool_call['tool']}")
print(f"   Arguments: {json.dumps(tool_call['arguments'], indent=6)}")
print()

print("3. GRASS COMMAND EXECUTED:")
print(f"   {' '.join(grass_command)}")
print()

print("4. SAMPLE OUTPUT (from North Carolina sample dataset):")
print("-" * 70)
print(sample_output)
print("-" * 70)
print()

print("5. FORMATTED RESPONSE TO CLAUDE:")
print("-" * 70)
print(mcp_response['content'][0]['text'])
print("-" * 70)
print()

print("=" * 70)
print("How to actually use this:")
print("=" * 70)
print("""
1. Install GRASS GIS:
   - Ubuntu/Debian: sudo apt-get install grass
   - macOS: brew install grass
   - Windows: Download from https://grass.osgeo.org/download/

2. Download sample data (North Carolina dataset):
   https://grass.osgeo.org/sampledata/north_carolina/nc_spm_08_grass7.zip
   Extract to ~/grassdata/

3. Configure Claude Desktop with this MCP server
   (See QUICKSTART.md for instructions)

4. Simply ask Claude:
   "List all raster maps in my GRASS location at /home/user/grassdata/nc_spm_08"

   Claude will automatically:
   - Select the grass_list_maps tool
   - Fill in the correct arguments
   - Execute the GRASS command
   - Format and return the results
""")
