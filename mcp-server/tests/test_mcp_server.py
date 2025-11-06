"""Integration tests for MCP server call_tool function."""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import grass_mcp_server
from mcp.types import TextContent


class TestCallTool:
    """Test the call_tool MCP function."""

    @pytest.mark.asyncio
    @patch("grass_mcp_server.run_grass_command")
    async def test_call_grass_raster_info(
        self, mock_run_cmd, mock_gisdbase, sample_raster_info
    ):
        """Test calling grass_raster_info tool."""
        mock_run_cmd.return_value = sample_raster_info

        result = await grass_mcp_server.call_tool(
            "grass_raster_info",
            {
                "map_name": "elevation",
                "gisdbase": mock_gisdbase["gisdbase"],
                "location": mock_gisdbase["location"],
                "mapset": mock_gisdbase["mapset"],
            },
        )

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], TextContent)
        assert "north=228500" in result[0].text
        assert "cells=2025000" in result[0].text

        # Verify command was called correctly
        mock_run_cmd.assert_called_once()
        call_args = mock_run_cmd.call_args[0]
        assert call_args[0] == ["r.info", "-g", "map=elevation"]

    @pytest.mark.asyncio
    @patch("grass_mcp_server.run_grass_command")
    async def test_call_grass_vector_info(
        self, mock_run_cmd, mock_gisdbase, sample_vector_info
    ):
        """Test calling grass_vector_info tool."""
        mock_run_cmd.return_value = sample_vector_info

        result = await grass_mcp_server.call_tool(
            "grass_vector_info",
            {
                "map_name": "roads",
                "gisdbase": mock_gisdbase["gisdbase"],
                "location": mock_gisdbase["location"],
            },
        )

        assert isinstance(result, list)
        assert len(result) == 1
        assert "lines=1631" in result[0].text

        # Verify correct command
        call_args = mock_run_cmd.call_args[0]
        assert call_args[0] == ["v.info", "-g", "map=roads"]

    @pytest.mark.asyncio
    @patch("grass_mcp_server.run_grass_command")
    async def test_call_grass_raster_univar(
        self, mock_run_cmd, mock_gisdbase, sample_univar_output
    ):
        """Test calling grass_raster_univar tool."""
        mock_run_cmd.return_value = sample_univar_output

        result = await grass_mcp_server.call_tool(
            "grass_raster_univar",
            {
                "map_name": "elevation",
                "gisdbase": mock_gisdbase["gisdbase"],
                "location": mock_gisdbase["location"],
                "extended": False,
            },
        )

        assert isinstance(result, list)
        assert "mean=" in result[0].text
        assert "stddev=" in result[0].text

        # Check command flags
        call_args = mock_run_cmd.call_args[0]
        assert call_args[0][0] == "r.univar"
        assert call_args[0][1] == "-g"

    @pytest.mark.asyncio
    @patch("grass_mcp_server.run_grass_command")
    async def test_call_grass_raster_univar_extended(
        self, mock_run_cmd, mock_gisdbase, sample_univar_output
    ):
        """Test calling grass_raster_univar with extended flag."""
        mock_run_cmd.return_value = sample_univar_output

        result = await grass_mcp_server.call_tool(
            "grass_raster_univar",
            {
                "map_name": "elevation",
                "gisdbase": mock_gisdbase["gisdbase"],
                "location": mock_gisdbase["location"],
                "extended": True,
            },
        )

        # Check extended flag is included
        call_args = mock_run_cmd.call_args[0]
        assert "-ge" in call_args[0]

    @pytest.mark.asyncio
    @patch("grass_mcp_server.run_grass_command")
    async def test_call_grass_list_maps_raster(
        self, mock_run_cmd, mock_gisdbase, sample_map_list
    ):
        """Test calling grass_list_maps for raster type."""
        mock_run_cmd.return_value = sample_map_list

        result = await grass_mcp_server.call_tool(
            "grass_list_maps",
            {
                "gisdbase": mock_gisdbase["gisdbase"],
                "location": mock_gisdbase["location"],
                "map_type": "raster",
            },
        )

        assert isinstance(result, list)
        assert "elevation" in result[0].text

        call_args = mock_run_cmd.call_args[0]
        assert call_args[0] == ["g.list", "type=raster", "-m"]

    @pytest.mark.asyncio
    @patch("grass_mcp_server.run_grass_command")
    async def test_call_grass_list_maps_all(self, mock_run_cmd, mock_gisdbase):
        """Test calling grass_list_maps for all types."""
        mock_run_cmd.return_value = "elevation\nroads\n"

        result = await grass_mcp_server.call_tool(
            "grass_list_maps",
            {
                "gisdbase": mock_gisdbase["gisdbase"],
                "location": mock_gisdbase["location"],
                "map_type": "all",
            },
        )

        # Should call g.list multiple times
        assert mock_run_cmd.call_count >= 1

    @pytest.mark.asyncio
    @patch("grass_mcp_server.run_grass_command")
    async def test_call_grass_mapcalc(self, mock_run_cmd, mock_gisdbase):
        """Test calling grass_mapcalc tool."""
        mock_run_cmd.return_value = "Map calculation completed"

        expression = "result = elevation * 2"
        result = await grass_mcp_server.call_tool(
            "grass_mapcalc",
            {
                "expression": expression,
                "gisdbase": mock_gisdbase["gisdbase"],
                "location": mock_gisdbase["location"],
            },
        )

        assert isinstance(result, list)
        assert "completed" in result[0].text.lower()

        call_args = mock_run_cmd.call_args[0]
        assert call_args[0] == ["r.mapcalc", f"expression={expression}"]

    @pytest.mark.asyncio
    @patch("grass_mcp_server.run_grass_command")
    async def test_call_grass_slope_aspect(self, mock_run_cmd, mock_gisdbase):
        """Test calling grass_slope_aspect tool."""
        mock_run_cmd.return_value = "Calculation completed"

        result = await grass_mcp_server.call_tool(
            "grass_slope_aspect",
            {
                "elevation": "dem",
                "slope": "slope_map",
                "aspect": "aspect_map",
                "gisdbase": mock_gisdbase["gisdbase"],
                "location": mock_gisdbase["location"],
            },
        )

        assert isinstance(result, list)
        assert "slope" in result[0].text.lower()

        call_args = mock_run_cmd.call_args[0]
        cmd = call_args[0]
        assert cmd[0] == "r.slope.aspect"
        assert "elevation=dem" in cmd
        assert "slope=slope_map" in cmd
        assert "aspect=aspect_map" in cmd

    @pytest.mark.asyncio
    @patch("grass_mcp_server.run_grass_command")
    async def test_call_grass_slope_without_aspect(self, mock_run_cmd, mock_gisdbase):
        """Test calling grass_slope_aspect without aspect parameter."""
        mock_run_cmd.return_value = "Calculation completed"

        result = await grass_mcp_server.call_tool(
            "grass_slope_aspect",
            {
                "elevation": "dem",
                "slope": "slope_map",
                "gisdbase": mock_gisdbase["gisdbase"],
                "location": mock_gisdbase["location"],
            },
        )

        call_args = mock_run_cmd.call_args[0]
        cmd = call_args[0]
        # aspect should not be in command
        assert not any("aspect=" in arg for arg in cmd)

    @pytest.mark.asyncio
    @patch("grass_mcp_server.run_grass_command")
    async def test_call_grass_buffer(self, mock_run_cmd, mock_gisdbase):
        """Test calling grass_buffer tool."""
        mock_run_cmd.return_value = "Buffer created"

        result = await grass_mcp_server.call_tool(
            "grass_buffer",
            {
                "input_map": "roads",
                "output_map": "roads_buffer",
                "distance": 500,
                "gisdbase": mock_gisdbase["gisdbase"],
                "location": mock_gisdbase["location"],
            },
        )

        assert isinstance(result, list)
        assert "buffer" in result[0].text.lower()

        call_args = mock_run_cmd.call_args[0]
        cmd = call_args[0]
        assert cmd[0] == "v.buffer"
        assert "input=roads" in cmd
        assert "output=roads_buffer" in cmd
        assert "distance=500" in cmd

    @pytest.mark.asyncio
    @patch("grass_mcp_server.run_grass_command")
    async def test_call_grass_region_info(
        self, mock_run_cmd, mock_gisdbase, sample_region_output
    ):
        """Test calling grass_region_info tool."""
        mock_run_cmd.return_value = sample_region_output

        result = await grass_mcp_server.call_tool(
            "grass_region_info",
            {
                "gisdbase": mock_gisdbase["gisdbase"],
                "location": mock_gisdbase["location"],
            },
        )

        assert isinstance(result, list)
        assert "north:" in result[0].text
        assert "projection:" in result[0].text

        call_args = mock_run_cmd.call_args[0]
        assert call_args[0] == ["g.region", "-p"]

    @pytest.mark.asyncio
    async def test_call_unknown_tool(self, mock_gisdbase):
        """Test calling an unknown tool."""
        result = await grass_mcp_server.call_tool(
            "unknown_tool",
            {"gisdbase": mock_gisdbase["gisdbase"]},
        )

        assert isinstance(result, list)
        assert "unknown" in result[0].text.lower()

    @pytest.mark.asyncio
    @patch("grass_mcp_server.run_grass_command")
    async def test_call_tool_error_handling(self, mock_run_cmd, mock_gisdbase):
        """Test error handling in call_tool."""
        mock_run_cmd.side_effect = RuntimeError("GRASS command failed: Map not found")

        result = await grass_mcp_server.call_tool(
            "grass_raster_info",
            {
                "map_name": "nonexistent",
                "gisdbase": mock_gisdbase["gisdbase"],
                "location": mock_gisdbase["location"],
            },
        )

        assert isinstance(result, list)
        assert "error" in result[0].text.lower()
        assert "map not found" in result[0].text.lower()

    @pytest.mark.asyncio
    @patch("grass_mcp_server.run_grass_command")
    async def test_call_tool_uses_default_mapset(self, mock_run_cmd, mock_gisdbase):
        """Test that default mapset is used when not specified."""
        mock_run_cmd.return_value = "output"

        await grass_mcp_server.call_tool(
            "grass_raster_info",
            {
                "map_name": "elevation",
                "gisdbase": mock_gisdbase["gisdbase"],
                "location": mock_gisdbase["location"],
                # mapset not specified
            },
        )

        # Check that PERMANENT was used as default
        call_args = mock_run_cmd.call_args[0]
        assert len(call_args) >= 4
        assert call_args[3] == "PERMANENT"


class TestMCPServerIntegration:
    """Integration tests for the MCP server."""

    @pytest.mark.asyncio
    async def test_server_initialization(self):
        """Test that the MCP server can be initialized."""
        assert grass_mcp_server.app is not None
        assert grass_mcp_server.app.name == "grass-gis"

    @pytest.mark.asyncio
    async def test_list_and_call_tool_integration(self):
        """Test that listed tools can be called."""
        tools = await grass_mcp_server.list_tools()
        tool_names = [t.name for t in tools]

        # These tool names should be callable
        expected_tools = [
            "grass_raster_info",
            "grass_vector_info",
            "grass_raster_univar",
            "grass_list_maps",
            "grass_mapcalc",
            "grass_slope_aspect",
            "grass_buffer",
            "grass_region_info",
        ]

        for tool_name in expected_tools:
            assert tool_name in tool_names
