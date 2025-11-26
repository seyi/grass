#!/usr/bin/env python3
"""
Test Phase 2A+B Integration - All 17 Tools

Verifies that the expanded MCP server correctly integrates:
- 8 base tools
- 3 visualization tools
- 5 custom expansion tools (Phase 2A)
- 1 generic wrapper (Phase 2B)
"""

import asyncio
import sys
sys.path.insert(0, '/home/user/grass/mcp-server')

import grass_mcp_server


async def test_tool_count():
    """Test that all 17 tools are registered."""
    print("=" * 70)
    print("TEST 1: Tool Count and Registration")
    print("=" * 70)

    tools = await grass_mcp_server.list_tools()
    print(f"\nTotal tools: {len(tools)}")

    # Expected count
    expected = 17  # 8 base + 3 viz + 5 custom + 1 wrapper

    if len(tools) == expected:
        print(f"✓ Correct! Expected {expected} tools, got {len(tools)}")
    else:
        print(f"✗ Error! Expected {expected} tools, got {len(tools)}")
        return False

    # Categorize tools
    base_tools = []
    viz_tools = []
    expansion_tools = []

    for tool in tools:
        if tool.name in ["grass_raster_info", "grass_vector_info", "grass_raster_univar",
                         "grass_list_maps", "grass_mapcalc", "grass_slope_aspect",
                         "grass_buffer", "grass_region_info"]:
            base_tools.append(tool.name)
        elif tool.name in ["grass_visualize_raster", "grass_create_composite",
                           "grass_create_interactive_map"]:
            viz_tools.append(tool.name)
        elif tool.name in ["grass_watershed", "grass_viewshed", "grass_reclass",
                           "grass_overlay", "grass_import_raster", "grass_execute"]:
            expansion_tools.append(tool.name)

    print(f"\n📊 Tool Categories:")
    print(f"  Base tools: {len(base_tools)}")
    print(f"  Visualization tools: {len(viz_tools)}")
    print(f"  Expansion tools: {len(expansion_tools)}")

    print(f"\n✨ Phase 2A+B Tools:")
    for tool_name in expansion_tools:
        print(f"  - {tool_name}")

    return True


async def test_watershed_tool():
    """Test grass_watershed tool."""
    print("\n" + "=" * 70)
    print("TEST 2: Watershed Tool (Phase 2A)")
    print("=" * 70)

    import os
    gisdbase = "/home/user/grassdata"
    location = "nc_spm_08_grass7"

    if not os.path.exists(f"{gisdbase}/{location}"):
        print("⚠ Skipping: NC dataset not found")
        return None

    print("\nCalling: grass_watershed")
    print("  elevation=elevation")
    print("  accumulation=test_flow_accum")
    print("  basin=test_watersheds")

    try:
        result = await grass_mcp_server.call_tool(
            "grass_watershed",
            {
                "elevation": "elevation",
                "accumulation": "test_flow_accum",
                "basin": "test_watersheds",
                "threshold": 10000,
                "gisdbase": gisdbase,
                "location": location
            }
        )

        print(f"\n✓ Result: {result[0].text}")
        return True
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False


async def test_generic_wrapper():
    """Test grass_execute generic wrapper."""
    print("\n" + "=" * 70)
    print("TEST 3: Generic Wrapper (Phase 2B)")
    print("=" * 70)

    import os
    gisdbase = "/home/user/grassdata"
    location = "nc_spm_08_grass7"

    if not os.path.exists(f"{gisdbase}/{location}"):
        print("⚠ Skipping: NC dataset not found")
        return None

    print("\nCalling: grass_execute")
    print("  command=r.neighbors")
    print("  parameters={input: elevation, output: elev_smooth_test, size: 5}")
    print("\nThis demonstrates accessing ANY GRASS command via the wrapper!")

    try:
        result = await grass_mcp_server.call_tool(
            "grass_execute",
            {
                "command": "r.neighbors",
                "parameters": {
                    "input": "elevation",
                    "output": "elev_smooth_test",
                    "size": 5,
                    "method": "average"
                },
                "gisdbase": gisdbase,
                "location": location
            }
        )

        print(f"\n✓ Result: {result[0].text[:150]}...")
        return True
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False


async def test_expansion_availability():
    """Test that expansion tools are properly loaded."""
    print("\n" + "=" * 70)
    print("TEST 4: Expansion Module Status")
    print("=" * 70)

    print(f"\nExpansion available: {grass_mcp_server.EXPANSION_AVAILABLE}")
    print(f"Visualization available: {grass_mcp_server.VISUALIZATION_AVAILABLE}")

    if grass_mcp_server.EXPANSION_AVAILABLE:
        print("\n✓ Expansion tools loaded successfully")
        return True
    else:
        print(f"\n✗ Expansion tools not loaded: {grass_mcp_server.EXPANSION_IMPORT_ERROR}")
        return False


async def test_tool_details():
    """Test tool schemas and descriptions."""
    print("\n" + "=" * 70)
    print("TEST 5: Tool Details")
    print("=" * 70)

    tools = await grass_mcp_server.list_tools()

    # Check a few key expansion tools
    expansion_tool_names = ["grass_watershed", "grass_execute"]

    for tool_name in expansion_tool_names:
        tool = next((t for t in tools if t.name == tool_name), None)
        if tool:
            print(f"\n✓ {tool.name}")
            print(f"  Description: {tool.description[:60]}...")
            print(f"  Parameters: {len(tool.inputSchema['properties'])}")
            print(f"  Required: {len(tool.inputSchema.get('required', []))}")
        else:
            print(f"\n✗ {tool_name} not found!")
            return False

    return True


async def main():
    """Run all tests."""
    print("\nGRASS GIS MCP Server - Phase 2A+B Integration Tests")
    print("Testing expanded server with 17 tools (11 existing + 6 new)")
    print()

    results = []

    # Run tests
    results.append(await test_tool_count())
    results.append(await test_expansion_availability())
    results.append(await test_tool_details())
    results.append(await test_watershed_tool())
    results.append(await test_generic_wrapper())

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for r in results if r is True)
    skipped = sum(1 for r in results if r is None)
    failed = len(results) - passed - skipped

    print(f"\nTotal tests: {len(results)}")
    print(f"  Passed: {passed}")
    print(f"  Skipped: {skipped}")
    print(f"  Failed: {failed}")

    if failed == 0 and passed > 0:
        print("\n✅ PHASE 2A+B INTEGRATION SUCCESSFUL!")
        print("\nServer now provides:")
        print("  • 8 base geospatial tools")
        print("  • 3 visualization tools (Phase 1)")
        print("  • 5 custom expansion tools (Phase 2A)")
        print("  • 1 generic wrapper for ALL 500+ GRASS commands (Phase 2B)")
        print("\nTotal: 17 tools providing access to 500+ GRASS GIS commands!")
        return 0
    else:
        print(f"\n❌ {failed} TEST(S) FAILED")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
