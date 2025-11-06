#!/usr/bin/env python3
"""
GRASS GIS MCP Server

A Model Context Protocol (MCP) server that exposes GRASS GIS geospatial
processing capabilities as tools that can be used by AI assistants.

This server provides tools for:
- Raster data analysis and processing
- Vector data operations
- Spatial analysis
- Terrain analysis
- Map calculations
"""

import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


# Create MCP server instance
app = Server("grass-gis")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available GRASS GIS tools."""
    return [
        Tool(
            name="grass_raster_info",
            description=(
                "Get information about a raster map including dimensions, "
                "resolution, extent, and data type. Requires a GRASS location "
                "and mapset to be set up."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "map_name": {
                        "type": "string",
                        "description": "Name of the raster map",
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
                "required": ["map_name", "gisdbase", "location"],
            },
        ),
        Tool(
            name="grass_vector_info",
            description=(
                "Get information about a vector map including number of features, "
                "feature types, extent, and attribute table information."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "map_name": {
                        "type": "string",
                        "description": "Name of the vector map",
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
                "required": ["map_name", "gisdbase", "location"],
            },
        ),
        Tool(
            name="grass_raster_univar",
            description=(
                "Calculate univariate statistics for a raster map including "
                "min, max, mean, standard deviation, and other statistical measures."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "map_name": {
                        "type": "string",
                        "description": "Name of the raster map",
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
                    "extended": {
                        "type": "boolean",
                        "description": "Calculate extended statistics",
                        "default": False,
                    },
                },
                "required": ["map_name", "gisdbase", "location"],
            },
        ),
        Tool(
            name="grass_list_maps",
            description=(
                "List all maps in a GRASS location/mapset. Can filter by type "
                "(raster, vector, raster3d, etc.)"
            ),
            inputSchema={
                "type": "object",
                "properties": {
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
                    "map_type": {
                        "type": "string",
                        "description": "Type of maps to list",
                        "enum": ["raster", "vector", "raster_3d", "all"],
                        "default": "all",
                    },
                },
                "required": ["gisdbase", "location"],
            },
        ),
        Tool(
            name="grass_mapcalc",
            description=(
                "Execute raster map algebra calculations using r.mapcalc. "
                "Allows complex mathematical operations on raster maps."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": (
                            "Map algebra expression (e.g., 'result = elevation * 2 + 100')"
                        ),
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
                "required": ["expression", "gisdbase", "location"],
            },
        ),
        Tool(
            name="grass_slope_aspect",
            description=(
                "Calculate slope and aspect from a DEM (Digital Elevation Model). "
                "Useful for terrain analysis."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "elevation": {
                        "type": "string",
                        "description": "Name of input elevation raster map",
                    },
                    "slope": {
                        "type": "string",
                        "description": "Name for output slope map",
                    },
                    "aspect": {
                        "type": "string",
                        "description": "Name for output aspect map (optional)",
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
                "required": ["elevation", "slope", "gisdbase", "location"],
            },
        ),
        Tool(
            name="grass_buffer",
            description=(
                "Create a buffer around vector features at a specified distance. "
                "Useful for proximity analysis."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "input_map": {
                        "type": "string",
                        "description": "Name of input vector map",
                    },
                    "output_map": {
                        "type": "string",
                        "description": "Name for output buffer map",
                    },
                    "distance": {
                        "type": "number",
                        "description": "Buffer distance in map units",
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
                "required": ["input_map", "output_map", "distance", "gisdbase", "location"],
            },
        ),
        Tool(
            name="grass_region_info",
            description=(
                "Get current computational region information including extent, "
                "resolution, and number of rows/columns."
            ),
            inputSchema={
                "type": "object",
                "properties": {
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
                "required": ["gisdbase", "location"],
            },
        ),
    ]


def run_grass_command(
    command: list[str],
    gisdbase: str,
    location: str,
    mapset: str = "PERMANENT",
) -> str:
    """
    Run a GRASS GIS command with proper environment setup.

    Args:
        command: GRASS command as list of strings
        gisdbase: Path to GRASS database
        location: GRASS location name
        mapset: GRASS mapset name

    Returns:
        Command output as string
    """
    # Set up GRASS environment
    env = os.environ.copy()
    env["GISDBASE"] = gisdbase
    env["LOCATION_NAME"] = location
    env["MAPSET"] = mapset

    # Try to find GRASS installation
    grass_bin = None
    for possible_grass in ["grass", "grass80", "grass82", "grass83", "grass84"]:
        try:
            result = subprocess.run(
                ["which", possible_grass],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                grass_bin = possible_grass
                break
        except (subprocess.TimeoutExpired, FileNotFoundError):
            continue

    if not grass_bin:
        # Try Python import as fallback
        try:
            import grass.script as gs
            # Use Python API directly
            if command[0] == "r.info":
                from grass.script import raster
                result = gs.read_command(*command)
                return result
            elif command[0] == "v.info":
                from grass.script import vector
                result = gs.read_command(*command)
                return result
            else:
                result = gs.read_command(*command)
                return result
        except ImportError:
            raise RuntimeError(
                "GRASS GIS not found. Please install GRASS GIS or ensure it's in PATH"
            )

    # Run command through GRASS
    full_command = [grass_bin, "--text", "--exec"] + command

    result = subprocess.run(
        full_command,
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )

    if result.returncode != 0:
        raise RuntimeError(f"GRASS command failed: {result.stderr}")

    return result.stdout


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""
    try:
        if name == "grass_raster_info":
            output = run_grass_command(
                ["r.info", "-g", f"map={arguments['map_name']}"],
                arguments["gisdbase"],
                arguments["location"],
                arguments.get("mapset", "PERMANENT"),
            )
            return [TextContent(type="text", text=output)]

        elif name == "grass_vector_info":
            output = run_grass_command(
                ["v.info", "-g", f"map={arguments['map_name']}"],
                arguments["gisdbase"],
                arguments["location"],
                arguments.get("mapset", "PERMANENT"),
            )
            return [TextContent(type="text", text=output)]

        elif name == "grass_raster_univar":
            flags = "-g"
            if arguments.get("extended", False):
                flags += "e"
            output = run_grass_command(
                ["r.univar", flags, f"map={arguments['map_name']}"],
                arguments["gisdbase"],
                arguments["location"],
                arguments.get("mapset", "PERMANENT"),
            )
            return [TextContent(type="text", text=output)]

        elif name == "grass_list_maps":
            map_type = arguments.get("map_type", "all")
            if map_type == "all":
                commands = [
                    ["g.list", "type=raster", "-m"],
                    ["g.list", "type=vector", "-m"],
                    ["g.list", "type=raster_3d", "-m"],
                ]
                outputs = []
                for cmd in commands:
                    try:
                        out = run_grass_command(
                            cmd,
                            arguments["gisdbase"],
                            arguments["location"],
                            arguments.get("mapset", "PERMANENT"),
                        )
                        outputs.append(out)
                    except Exception:
                        pass
                output = "\n".join(outputs)
            else:
                type_map = {
                    "raster": "raster",
                    "vector": "vector",
                    "raster_3d": "raster_3d",
                }
                output = run_grass_command(
                    ["g.list", f"type={type_map[map_type]}", "-m"],
                    arguments["gisdbase"],
                    arguments["location"],
                    arguments.get("mapset", "PERMANENT"),
                )
            return [TextContent(type="text", text=output)]

        elif name == "grass_mapcalc":
            output = run_grass_command(
                ["r.mapcalc", f"expression={arguments['expression']}"],
                arguments["gisdbase"],
                arguments["location"],
                arguments.get("mapset", "PERMANENT"),
            )
            return [TextContent(type="text", text=f"Map calculation completed: {output}")]

        elif name == "grass_slope_aspect":
            cmd = [
                "r.slope.aspect",
                f"elevation={arguments['elevation']}",
                f"slope={arguments['slope']}",
            ]
            if "aspect" in arguments:
                cmd.append(f"aspect={arguments['aspect']}")

            output = run_grass_command(
                cmd,
                arguments["gisdbase"],
                arguments["location"],
                arguments.get("mapset", "PERMANENT"),
            )
            return [TextContent(type="text", text=f"Slope/aspect calculated: {output}")]

        elif name == "grass_buffer":
            output = run_grass_command(
                [
                    "v.buffer",
                    f"input={arguments['input_map']}",
                    f"output={arguments['output_map']}",
                    f"distance={arguments['distance']}",
                ],
                arguments["gisdbase"],
                arguments["location"],
                arguments.get("mapset", "PERMANENT"),
            )
            return [TextContent(type="text", text=f"Buffer created: {output}")]

        elif name == "grass_region_info":
            output = run_grass_command(
                ["g.region", "-p"],
                arguments["gisdbase"],
                arguments["location"],
                arguments.get("mapset", "PERMANENT"),
            )
            return [TextContent(type="text", text=output)]

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
