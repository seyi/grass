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

# Import visualization addon
try:
    from grass_visualization_addon import VISUALIZATION_TOOLS, handle_visualization_tool
    VISUALIZATION_AVAILABLE = True
except ImportError as e:
    VISUALIZATION_AVAILABLE = False
    VISUALIZATION_IMPORT_ERROR = str(e)

# Import expansion tools (Phase 2A+B)
try:
    from grass_expansion_poc import EXPANSION_TOOLS_CUSTOM, GENERIC_WRAPPER_TOOL
    EXPANSION_AVAILABLE = True
except ImportError as e:
    EXPANSION_AVAILABLE = False
    EXPANSION_IMPORT_ERROR = str(e)


# Create MCP server instance
app = Server("grass-gis")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available GRASS GIS tools."""
    # Base GRASS tools
    base_tools = [
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

    # Build complete tool list
    all_tools = base_tools.copy()

    # Add visualization tools if available
    if VISUALIZATION_AVAILABLE:
        all_tools.extend(VISUALIZATION_TOOLS)

    # Add expansion tools if available (Phase 2A+B)
    if EXPANSION_AVAILABLE:
        all_tools.extend(EXPANSION_TOOLS_CUSTOM)
        all_tools.append(GENERIC_WRAPPER_TOOL)

    return all_tools


async def run_grass_command(
    command: list[str],
    gisdbase: str,
    location: str,
    mapset: str = "PERMANENT",
    stdin_data: Optional[str] = None,
    timeout: int = 60,
) -> str:
    """
    Run a GRASS GIS command with proper environment setup (async version).

    Args:
        command: GRASS command as list of strings
        gisdbase: Path to GRASS database
        location: GRASS location name
        mapset: GRASS mapset name
        stdin_data: Optional input to pass via stdin
        timeout: Command timeout in seconds (default: 60)

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
            # Use asyncio.create_subprocess_exec for async which command
            process = await asyncio.create_subprocess_exec(
                "which", possible_grass,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=5)
            if process.returncode == 0:
                grass_bin = possible_grass
                break
        except (asyncio.TimeoutError, FileNotFoundError):
            continue

    if not grass_bin:
        # Try Python import as fallback
        try:
            import grass.script as gs
            # Use Python API directly - run in executor to avoid blocking
            loop = asyncio.get_event_loop()

            def _run_grass_script():
                if command[0] == "r.info":
                    from grass.script import raster
                    return gs.read_command(*command)
                elif command[0] == "v.info":
                    from grass.script import vector
                    return gs.read_command(*command)
                else:
                    return gs.read_command(*command)

            result = await loop.run_in_executor(None, _run_grass_script)
            return result
        except ImportError:
            raise RuntimeError(
                "GRASS GIS not found. Please install GRASS GIS or ensure it's in PATH"
            )

    # Run command through GRASS using asyncio.create_subprocess_exec
    full_command = [grass_bin, "--text", "--exec"] + command

    process = await asyncio.create_subprocess_exec(
        *full_command,
        env=env,
        stdin=asyncio.subprocess.PIPE if stdin_data else None,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    try:
        # Communicate with optional stdin input
        if stdin_data:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(input=stdin_data.encode()),
                timeout=timeout
            )
        else:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout
            )
    except asyncio.TimeoutError:
        process.kill()
        await process.wait()
        raise RuntimeError(f"GRASS command timed out after {timeout} seconds")

    if process.returncode != 0:
        raise RuntimeError(f"GRASS command failed: {stderr.decode()}")

    return stdout.decode()


# =============================================================================
# Expansion Tool Handlers (Phase 2A+B)
# =============================================================================

async def handle_expansion_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle expansion tool calls (Phase 2A+B)."""
    try:
        if name == "grass_watershed":
            # r.watershed - Watershed and stream extraction
            cmd = ["r.watershed", f"elevation={arguments['elevation']}"]

            # Add optional outputs
            if "accumulation" in arguments:
                cmd.append(f"accumulation={arguments['accumulation']}")
            if "drainage" in arguments:
                cmd.append(f"drainage={arguments['drainage']}")
            if "basin" in arguments:
                cmd.append(f"basin={arguments['basin']}")
            if "stream" in arguments:
                cmd.append(f"stream={arguments['stream']}")

            # Add threshold
            threshold = arguments.get("threshold", 1000)
            cmd.append(f"threshold={threshold}")

            await run_grass_command(
                cmd,
                arguments["gisdbase"],
                arguments["location"],
                arguments.get("mapset", "PERMANENT"),
                timeout=300  # Longer timeout for watershed
            )

            outputs = []
            if "accumulation" in arguments:
                outputs.append(f"flow accumulation: {arguments['accumulation']}")
            if "basin" in arguments:
                outputs.append(f"watersheds: {arguments['basin']}")
            if "stream" in arguments:
                outputs.append(f"streams: {arguments['stream']}")

            return [TextContent(
                type="text",
                text=f"Watershed analysis complete. Created: {', '.join(outputs)}"
            )]

        elif name == "grass_viewshed":
            # r.viewshed - Viewshed analysis
            cmd = [
                "r.viewshed",
                f"input={arguments['input']}",
                f"output={arguments['output']}",
                f"coordinates={arguments['coordinates']}",
                f"observer_elevation={arguments.get('observer_elevation', 1.75)}",
                f"target_elevation={arguments.get('target_elevation', 0)}",
            ]

            if arguments.get("max_distance", -1) > 0:
                cmd.append(f"max_distance={arguments['max_distance']}")

            await run_grass_command(
                cmd,
                arguments["gisdbase"],
                arguments["location"],
                arguments.get("mapset", "PERMANENT"),
                timeout=300
            )

            return [TextContent(
                type="text",
                text=f"Viewshed analysis complete. Created: {arguments['output']}"
            )]

        elif name == "grass_reclass":
            # r.reclass - Reclassification (reads rules from stdin)
            await run_grass_command(
                ["r.reclass", f"input={arguments['input']}", f"output={arguments['output']}"],
                arguments["gisdbase"],
                arguments["location"],
                arguments.get("mapset", "PERMANENT"),
                stdin_data=arguments["rules"]
            )

            return [TextContent(
                type="text",
                text=f"Reclassification complete. Created: {arguments['output']}"
            )]

        elif name == "grass_overlay":
            # v.overlay - Vector overlay
            cmd = [
                "v.overlay",
                f"ainput={arguments['ainput']}",
                f"binput={arguments['binput']}",
                f"output={arguments['output']}",
                f"operator={arguments.get('operator', 'and')}",
            ]

            await run_grass_command(
                cmd,
                arguments["gisdbase"],
                arguments["location"],
                arguments.get("mapset", "PERMANENT"),
                timeout=180
            )

            return [TextContent(
                type="text",
                text=f"Vector overlay complete. Created: {arguments['output']}"
            )]

        elif name == "grass_import_raster":
            # r.import - Import raster with reprojection
            cmd = [
                "r.import",
                f"input={arguments['input']}",
                f"output={arguments['output']}",
                f"resolution={arguments.get('resolution', 'estimated')}",
                f"extent={arguments.get('extent', 'input')}",
            ]

            await run_grass_command(
                cmd,
                arguments["gisdbase"],
                arguments["location"],
                arguments.get("mapset", "PERMANENT"),
                timeout=600  # Longer timeout for imports
            )

            return [TextContent(
                type="text",
                text=f"Raster import complete. Created: {arguments['output']}"
            )]

        elif name == "grass_execute":
            # Generic wrapper - Execute any GRASS command
            command = arguments["command"]
            parameters = arguments["parameters"]
            flags = arguments.get("flags", "")
            stdin_data = arguments.get("stdin")

            # Build command
            cmd = [command]

            # Add flags
            if flags:
                cmd.append(f"-{flags}")

            # Add parameters
            for key, value in parameters.items():
                if value is not None:
                    cmd.append(f"{key}={value}")

            result = await run_grass_command(
                cmd,
                arguments["gisdbase"],
                arguments["location"],
                arguments.get("mapset", "PERMANENT"),
                stdin_data=stdin_data,
                timeout=600  # Longer timeout for generic commands
            )

            return [TextContent(
                type="text",
                text=f"Command '{command}' executed successfully.\n\nOutput:\n{result}"
            )]

        else:
            return [TextContent(type="text", text=f"Unknown expansion tool: {name}")]

    except Exception as e:
        return [TextContent(type="text", text=f"Error in {name}: {str(e)}")]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""
    try:
        # Route visualization tool calls
        if VISUALIZATION_AVAILABLE and name in ["grass_visualize_raster", "grass_create_composite", "grass_create_interactive_map"]:
            return await handle_visualization_tool(name, arguments)

        # Route expansion tool calls (Phase 2A+B)
        if EXPANSION_AVAILABLE and name in ["grass_watershed", "grass_viewshed", "grass_reclass",
                                             "grass_overlay", "grass_import_raster", "grass_execute"]:
            return await handle_expansion_tool(name, arguments)

        if name == "grass_raster_info":
            output = await run_grass_command(
                ["r.info", "-g", f"map={arguments['map_name']}"],
                arguments["gisdbase"],
                arguments["location"],
                arguments.get("mapset", "PERMANENT"),
            )
            return [TextContent(type="text", text=output)]

        elif name == "grass_vector_info":
            output = await run_grass_command(
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
            output = await run_grass_command(
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
                        out = await run_grass_command(
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
                output = await run_grass_command(
                    ["g.list", f"type={type_map[map_type]}", "-m"],
                    arguments["gisdbase"],
                    arguments["location"],
                    arguments.get("mapset", "PERMANENT"),
                )
            return [TextContent(type="text", text=output)]

        elif name == "grass_mapcalc":
            output = await run_grass_command(
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

            output = await run_grass_command(
                cmd,
                arguments["gisdbase"],
                arguments["location"],
                arguments.get("mapset", "PERMANENT"),
            )
            return [TextContent(type="text", text=f"Slope/aspect calculated: {output}")]

        elif name == "grass_buffer":
            output = await run_grass_command(
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
            output = await run_grass_command(
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
