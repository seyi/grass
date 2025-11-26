#!/usr/bin/env python3
"""
GRASS GIS MCP Server Expansion - Proof of Concept

Demonstrates two approaches to expanding MCP server capabilities:
1. Custom tools with tailored schemas (high-priority commands)
2. Generic wrapper for all GRASS commands

This POC shows how to scale from 11 tools to 500+ commands.
"""

from mcp.types import Tool, TextContent
import subprocess
import os
import json
from typing import Any, Dict, List


# =============================================================================
# APPROACH 1: Custom High-Priority Tools
# =============================================================================

EXPANSION_TOOLS_CUSTOM = [
    # Watershed Analysis - Critical for hydrology
    Tool(
        name="grass_watershed",
        description=(
            "Perform watershed analysis and stream extraction from a DEM. "
            "Calculates flow accumulation, drainage direction, watersheds, and stream networks."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "elevation": {
                    "type": "string",
                    "description": "Input elevation raster (DEM)",
                },
                "accumulation": {
                    "type": "string",
                    "description": "Output flow accumulation map name (optional)",
                },
                "drainage": {
                    "type": "string",
                    "description": "Output drainage direction map name (optional)",
                },
                "basin": {
                    "type": "string",
                    "description": "Output watershed basins map name (optional)",
                },
                "stream": {
                    "type": "string",
                    "description": "Output stream network map name (optional)",
                },
                "threshold": {
                    "type": "integer",
                    "description": "Minimum flow accumulation for streams (default: 1000)",
                    "default": 1000,
                },
                "gisdbase": {"type": "string"},
                "location": {"type": "string"},
                "mapset": {"type": "string", "default": "PERMANENT"},
            },
            "required": ["elevation", "gisdbase", "location"],
        },
    ),

    # Viewshed Analysis - Common in visibility studies
    Tool(
        name="grass_viewshed",
        description=(
            "Calculate viewshed (visible area) from observer point(s). "
            "Useful for visibility analysis, tower placement, scenic view assessment."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "input": {
                    "type": "string",
                    "description": "Input elevation raster (DEM)",
                },
                "output": {
                    "type": "string",
                    "description": "Output viewshed raster name",
                },
                "coordinates": {
                    "type": "string",
                    "description": "Observer coordinates as 'x,y' or 'easting,northing'",
                },
                "observer_elevation": {
                    "type": "number",
                    "description": "Height of observer above ground (meters, default: 1.75)",
                    "default": 1.75,
                },
                "target_elevation": {
                    "type": "number",
                    "description": "Height of target above ground (meters, default: 0)",
                    "default": 0,
                },
                "max_distance": {
                    "type": "number",
                    "description": "Maximum visibility distance (meters, default: -1 = infinity)",
                    "default": -1,
                },
                "gisdbase": {"type": "string"},
                "location": {"type": "string"},
                "mapset": {"type": "string", "default": "PERMANENT"},
            },
            "required": ["input", "output", "coordinates", "gisdbase", "location"],
        },
    ),

    # Raster Reclassification - Essential for categorization
    Tool(
        name="grass_reclass",
        description=(
            "Reclassify raster values into new categories. "
            "Common for land use classification, risk mapping, suitability analysis."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "input": {
                    "type": "string",
                    "description": "Input raster to reclassify",
                },
                "output": {
                    "type": "string",
                    "description": "Output reclassified raster name",
                },
                "rules": {
                    "type": "string",
                    "description": (
                        "Reclassification rules as text. Format: 'min:max:new_value' "
                        "Example: '0:100:1\\n100:200:2\\n200:*:3'"
                    ),
                },
                "gisdbase": {"type": "string"},
                "location": {"type": "string"},
                "mapset": {"type": "string", "default": "PERMANENT"},
            },
            "required": ["input", "output", "rules", "gisdbase", "location"],
        },
    ),

    # Vector Overlay - Core vector analysis
    Tool(
        name="grass_overlay",
        description=(
            "Overlay vector layers with different operators (and, or, not, xor). "
            "Perform intersection, union, difference operations between vector maps."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "ainput": {
                    "type": "string",
                    "description": "First input vector map",
                },
                "binput": {
                    "type": "string",
                    "description": "Second input vector map",
                },
                "output": {
                    "type": "string",
                    "description": "Output vector map name",
                },
                "operator": {
                    "type": "string",
                    "description": "Overlay operator",
                    "enum": ["and", "or", "not", "xor"],
                    "default": "and",
                },
                "gisdbase": {"type": "string"},
                "location": {"type": "string"},
                "mapset": {"type": "string", "default": "PERMANENT"},
            },
            "required": ["ainput", "binput", "output", "gisdbase", "location"],
        },
    ),

    # Raster Import with Reprojection
    Tool(
        name="grass_import_raster",
        description=(
            "Import raster data from external files with automatic reprojection. "
            "Supports GeoTIFF, ERDAS, HDF, and many other formats via GDAL."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "input": {
                    "type": "string",
                    "description": "Path to input raster file (GeoTIFF, etc.)",
                },
                "output": {
                    "type": "string",
                    "description": "Name for output raster in GRASS",
                },
                "resolution": {
                    "type": "string",
                    "description": "Resolution for import (estimated, value, region)",
                    "enum": ["estimated", "value", "region"],
                    "default": "estimated",
                },
                "extent": {
                    "type": "string",
                    "description": "Extent for import (input, region)",
                    "enum": ["input", "region"],
                    "default": "input",
                },
                "gisdbase": {"type": "string"},
                "location": {"type": "string"},
                "mapset": {"type": "string", "default": "PERMANENT"},
            },
            "required": ["input", "output", "gisdbase", "location"],
        },
    ),
]


# =============================================================================
# APPROACH 2: Generic Wrapper for All GRASS Commands
# =============================================================================

GENERIC_WRAPPER_TOOL = Tool(
    name="grass_execute",
    description=(
        "Execute any GRASS GIS command directly with full parameter control. "
        "Use this for advanced operations not covered by specialized tools. "
        "Provides access to all 500+ GRASS commands. "
        "Requires knowledge of GRASS command syntax and parameters."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": (
                    "GRASS command name (e.g., 'r.watershed', 'v.overlay', 'i.cluster'). "
                    "See GRASS documentation for available commands."
                ),
            },
            "parameters": {
                "type": "object",
                "description": (
                    "Command parameters as key-value pairs. "
                    "Example: {'elevation': 'dem', 'accumulation': 'flow', 'threshold': 1000}"
                ),
                "additionalProperties": True,
            },
            "flags": {
                "type": "string",
                "description": (
                    "Command flags as string without dashes. "
                    "Example: 'a' for -a flag, 'ab' for -a -b flags"
                ),
                "default": "",
            },
            "stdin": {
                "type": "string",
                "description": (
                    "Input to pass via stdin (for commands that read rules/data from stdin). "
                    "Example: reclassification rules for r.reclass"
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
        "required": ["command", "parameters", "gisdbase", "location"],
    },
)


# =============================================================================
# Implementation Functions
# =============================================================================

def run_grass_command(cmd: List[str], gisdbase: str, location: str,
                     mapset: str = "PERMANENT", stdin_data: str = None,
                     timeout: int = 300) -> str:
    """Execute a GRASS command in the specified location."""
    grass_cmd = ["grass", f"{gisdbase}/{location}/{mapset}", "--exec"] + cmd

    result = subprocess.run(
        grass_cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        input=stdin_data,
        env=dict(os.environ, GRASS_BATCH_JOB="1")
    )

    if result.returncode != 0:
        raise Exception(f"GRASS command failed: {result.stderr}")

    return result.stdout


async def handle_watershed(arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle r.watershed tool."""
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

    try:
        result = run_grass_command(
            cmd,
            arguments["gisdbase"],
            arguments["location"],
            arguments.get("mapset", "PERMANENT")
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
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_viewshed(arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle r.viewshed tool."""
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

    try:
        result = run_grass_command(
            cmd,
            arguments["gisdbase"],
            arguments["location"],
            arguments.get("mapset", "PERMANENT")
        )
        return [TextContent(
            type="text",
            text=f"Viewshed analysis complete. Created: {arguments['output']}"
        )]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_reclass(arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle r.reclass tool."""
    try:
        # r.reclass reads rules from stdin
        result = run_grass_command(
            ["r.reclass", f"input={arguments['input']}",
             f"output={arguments['output']}"],
            arguments["gisdbase"],
            arguments["location"],
            arguments.get("mapset", "PERMANENT"),
            stdin_data=arguments["rules"]
        )
        return [TextContent(
            type="text",
            text=f"Reclassification complete. Created: {arguments['output']}"
        )]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_overlay(arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle v.overlay tool."""
    cmd = [
        "v.overlay",
        f"ainput={arguments['ainput']}",
        f"binput={arguments['binput']}",
        f"output={arguments['output']}",
        f"operator={arguments.get('operator', 'and')}",
    ]

    try:
        result = run_grass_command(
            cmd,
            arguments["gisdbase"],
            arguments["location"],
            arguments.get("mapset", "PERMANENT")
        )
        return [TextContent(
            type="text",
            text=f"Vector overlay complete. Created: {arguments['output']}"
        )]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_import_raster(arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle r.import tool."""
    cmd = [
        "r.import",
        f"input={arguments['input']}",
        f"output={arguments['output']}",
        f"resolution={arguments.get('resolution', 'estimated')}",
        f"extent={arguments.get('extent', 'input')}",
    ]

    try:
        result = run_grass_command(
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
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_grass_execute(arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle generic GRASS command execution."""
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

    try:
        result = run_grass_command(
            cmd,
            arguments["gisdbase"],
            arguments["location"],
            arguments.get("mapset", "PERMANENT"),
            stdin_data=stdin_data
        )

        return [TextContent(
            type="text",
            text=f"Command '{command}' executed successfully.\n\nOutput:\n{result}"
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error executing '{command}': {str(e)}"
        )]


# =============================================================================
# Tool Router
# =============================================================================

async def route_expansion_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Route tool calls to appropriate handlers."""

    handlers = {
        "grass_watershed": handle_watershed,
        "grass_viewshed": handle_viewshed,
        "grass_reclass": handle_reclass,
        "grass_overlay": handle_overlay,
        "grass_import_raster": handle_import_raster,
        "grass_execute": handle_grass_execute,
    }

    if name in handlers:
        return await handlers[name](arguments)
    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]


# =============================================================================
# Integration Instructions
# =============================================================================

"""
INTEGRATION INTO MAIN MCP SERVER:

1. Add expansion tools to list_tools():

    from grass_expansion_poc import EXPANSION_TOOLS_CUSTOM, GENERIC_WRAPPER_TOOL

    @app.list_tools()
    async def list_tools():
        return (
            BASE_TOOLS +              # Original 8 tools
            VISUALIZATION_TOOLS +     # Phase 1: 3 tools
            EXPANSION_TOOLS_CUSTOM +  # Phase 2A: 5 tools
            [GENERIC_WRAPPER_TOOL]    # Phase 2B: 1 wrapper for all
        )

2. Add router to call_tool():

    from grass_expansion_poc import route_expansion_tool

    @app.call_tool()
    async def call_tool(name: str, arguments: Any):
        # Check if expansion tool
        if name in ["grass_watershed", "grass_viewshed", "grass_reclass",
                    "grass_overlay", "grass_import_raster", "grass_execute"]:
            return await route_expansion_tool(name, arguments)

        # ... existing tool handlers ...

3. Usage Examples:

    # Custom tool (optimal UX)
    "Calculate watershed and streams from the elevation map"
    → grass_watershed(elevation="dem", stream="streams", basin="watersheds")

    # Generic wrapper (maximum flexibility)
    "Run r.cost analysis from roads to find optimal paths"
    → grass_execute(command="r.cost", parameters={
        "input": "dem",
        "output": "cost_surface",
        "start_points": "roads"
    })
"""


if __name__ == "__main__":
    print("GRASS GIS MCP Server Expansion - Proof of Concept")
    print("=" * 70)
    print(f"\nCustom Tools: {len(EXPANSION_TOOLS_CUSTOM)}")
    for tool in EXPANSION_TOOLS_CUSTOM:
        print(f"  - {tool.name}")

    print(f"\nGeneric Wrapper: 1 tool")
    print(f"  - {GENERIC_WRAPPER_TOOL.name}")

    print(f"\nTotal New Tools: {len(EXPANSION_TOOLS_CUSTOM) + 1}")
    print(f"Total Coverage: {len(EXPANSION_TOOLS_CUSTOM)} specialized + 500+ via wrapper")

    print("\n" + "=" * 70)
    print("See EXPANSION_STRATEGY.md for full implementation plan")
