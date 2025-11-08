#!/usr/bin/env python3
"""
Test Visualization Integration with MCP Server

This tests that the visualization tools are properly integrated into the main
GRASS GIS MCP server and can be called successfully.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add mcp-server to path
sys.path.insert(0, str(Path(__file__).parent))

import grass_mcp_server


async def test_tool_listing():
    """Test that visualization tools appear in tool list."""
    print("=" * 70)
    print("TEST 1: Tool Listing")
    print("=" * 70)

    tools = await grass_mcp_server.list_tools()
    print(f"✓ Total tools available: {len(tools)}")

    # Check for visualization tools
    viz_tools = [t for t in tools if 'visualize' in t.name or 'composite' in t.name or 'interactive' in t.name]

    if len(viz_tools) == 3:
        print(f"✓ All 3 visualization tools found:")
        for tool in viz_tools:
            print(f"    - {tool.name}")
        return True
    else:
        print(f"✗ Expected 3 visualization tools, found {len(viz_tools)}")
        return False


async def test_grass_native_visualization():
    """Test GRASS native visualization using Cairo driver (no matplotlib needed)."""
    print("\n" + "=" * 70)
    print("TEST 2: GRASS Native Visualization (Cairo Driver)")
    print("=" * 70)

    gisdbase = "/home/user/grassdata"
    location = "nc_spm_08_grass7"
    output_path = "/tmp/test_viz_integration.png"

    # Check if NC dataset exists
    if not os.path.exists(f"{gisdbase}/{location}"):
        print(f"⚠ Skipping: NC dataset not found at {gisdbase}/{location}")
        return None

    print(f"Using dataset: {gisdbase}/{location}")
    print(f"Output: {output_path}")

    # Call grass_visualize_raster with simple style (uses GRASS native rendering as fallback)
    try:
        result = await grass_mcp_server.call_tool(
            "grass_visualize_raster",
            {
                "map_name": "elevation",
                "output_path": output_path,
                "gisdbase": gisdbase,
                "location": location,
                "width": 800,
                "height": 600,
                "style": "simple",
                "add_legend": True,
                "add_scalebar": True,
                "add_north_arrow": True
            }
        )

        print(f"✓ Tool executed")
        print(f"  Result: {result[0].text[:100]}...")

        # Check if output file was created
        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"✓ Output file created: {output_path}")
            print(f"  Size: {size:,} bytes")
            return True
        else:
            print(f"✗ Output file not created: {output_path}")
            print(f"  Full result: {result[0].text}")
            return False

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_tool_error_handling():
    """Test that visualization tools handle errors gracefully."""
    print("\n" + "=" * 70)
    print("TEST 3: Error Handling")
    print("=" * 70)

    # Try to visualize a non-existent map
    try:
        result = await grass_mcp_server.call_tool(
            "grass_visualize_raster",
            {
                "map_name": "nonexistent_map_12345",
                "output_path": "/tmp/test_error.png",
                "gisdbase": "/home/user/grassdata",
                "location": "nc_spm_08_grass7"
            }
        )

        # Should not crash, should return error message
        if "Error" in result[0].text or "not found" in result[0].text.lower():
            print(f"✓ Error handled gracefully")
            print(f"  Message: {result[0].text[:100]}...")
            return True
        else:
            print(f"✗ Unexpected success with non-existent map")
            return False

    except Exception as e:
        print(f"✓ Exception caught and handled: {type(e).__name__}")
        return True


async def test_visualization_addon_directly():
    """Test the visualization addon module directly."""
    print("\n" + "=" * 70)
    print("TEST 4: Direct Addon Test")
    print("=" * 70)

    try:
        from grass_visualization_addon import VISUALIZATION_TOOLS
        print(f"✓ Visualization addon imported successfully")
        print(f"  Tools provided: {len(VISUALIZATION_TOOLS)}")

        for tool in VISUALIZATION_TOOLS:
            print(f"    - {tool.name}")
            # Check tool has required fields
            assert hasattr(tool, 'name')
            assert hasattr(tool, 'description')
            assert hasattr(tool, 'inputSchema')

        print(f"✓ All tools have required attributes")
        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def print_summary(results):
    """Print test summary."""
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    total = len([r for r in results if r is not None])
    passed = len([r for r in results if r is True])
    skipped = len([r for r in results if r is None])
    failed = total - passed

    print(f"Total tests: {len(results)}")
    print(f"  Passed: {passed}")
    print(f"  Failed: {failed}")
    print(f"  Skipped: {skipped}")

    if failed == 0 and passed > 0:
        print("\n✅ ALL TESTS PASSED!")
        return True
    elif skipped == len(results):
        print("\n⚠ ALL TESTS SKIPPED (likely missing dataset)")
        return True
    else:
        print(f"\n❌ {failed} TEST(S) FAILED")
        return False


async def main():
    """Run all tests."""
    print("GRASS GIS MCP Server - Visualization Integration Tests")
    print("=" * 70)
    print(f"Visualization available: {grass_mcp_server.VISUALIZATION_AVAILABLE}")

    if not grass_mcp_server.VISUALIZATION_AVAILABLE:
        print(f"⚠ Warning: Visualization not available")
        print(f"  Reason: {grass_mcp_server.VISUALIZATION_IMPORT_ERROR}")
        print("  Tests will check integration but may skip visualization functionality")

    print()

    # Run tests
    results = []
    results.append(await test_tool_listing())
    results.append(await test_visualization_addon_directly())
    results.append(await test_grass_native_visualization())
    results.append(await test_tool_error_handling())

    # Print summary
    success = print_summary(results)

    return 0 if success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
