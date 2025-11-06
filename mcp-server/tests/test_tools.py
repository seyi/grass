"""Tests for MCP tool definitions and schemas."""

import pytest
import sys
from pathlib import Path

# Add parent directory to path to import grass_mcp_server
sys.path.insert(0, str(Path(__file__).parent.parent))

import grass_mcp_server


class TestToolDefinitions:
    """Test MCP tool definitions."""

    @pytest.mark.asyncio
    async def test_list_tools_returns_list(self):
        """Test that list_tools returns a list."""
        tools = await grass_mcp_server.list_tools()
        assert isinstance(tools, list)
        assert len(tools) > 0

    @pytest.mark.asyncio
    async def test_all_tools_have_required_fields(self):
        """Test that all tools have required fields."""
        tools = await grass_mcp_server.list_tools()

        for tool in tools:
            assert hasattr(tool, "name")
            assert hasattr(tool, "description")
            assert hasattr(tool, "inputSchema")
            assert tool.name
            assert tool.description
            assert isinstance(tool.inputSchema, dict)

    @pytest.mark.asyncio
    async def test_tool_names_are_unique(self):
        """Test that tool names are unique."""
        tools = await grass_mcp_server.list_tools()
        tool_names = [tool.name for tool in tools]
        assert len(tool_names) == len(set(tool_names))

    @pytest.mark.asyncio
    async def test_grass_raster_info_tool_definition(self):
        """Test grass_raster_info tool definition."""
        tools = await grass_mcp_server.list_tools()
        raster_info_tool = next(
            (t for t in tools if t.name == "grass_raster_info"), None
        )

        assert raster_info_tool is not None
        assert "raster map" in raster_info_tool.description.lower()

        schema = raster_info_tool.inputSchema
        assert "properties" in schema
        assert "required" in schema

        # Check required fields
        required_fields = schema["required"]
        assert "map_name" in required_fields
        assert "gisdbase" in required_fields
        assert "location" in required_fields

        # Check properties
        props = schema["properties"]
        assert "map_name" in props
        assert "gisdbase" in props
        assert "location" in props
        assert "mapset" in props

    @pytest.mark.asyncio
    async def test_grass_vector_info_tool_definition(self):
        """Test grass_vector_info tool definition."""
        tools = await grass_mcp_server.list_tools()
        vector_info_tool = next(
            (t for t in tools if t.name == "grass_vector_info"), None
        )

        assert vector_info_tool is not None
        assert "vector" in vector_info_tool.description.lower()

        schema = vector_info_tool.inputSchema
        required_fields = schema["required"]
        assert "map_name" in required_fields
        assert "gisdbase" in required_fields
        assert "location" in required_fields

    @pytest.mark.asyncio
    async def test_grass_mapcalc_tool_definition(self):
        """Test grass_mapcalc tool definition."""
        tools = await grass_mcp_server.list_tools()
        mapcalc_tool = next((t for t in tools if t.name == "grass_mapcalc"), None)

        assert mapcalc_tool is not None
        assert "algebra" in mapcalc_tool.description.lower()

        schema = mapcalc_tool.inputSchema
        props = schema["properties"]
        assert "expression" in props
        assert "expression" in schema["required"]

    @pytest.mark.asyncio
    async def test_grass_slope_aspect_tool_definition(self):
        """Test grass_slope_aspect tool definition."""
        tools = await grass_mcp_server.list_tools()
        slope_tool = next((t for t in tools if t.name == "grass_slope_aspect"), None)

        assert slope_tool is not None
        assert "slope" in slope_tool.description.lower()

        schema = slope_tool.inputSchema
        props = schema["properties"]
        assert "elevation" in props
        assert "slope" in props
        assert "aspect" in props

        required = schema["required"]
        assert "elevation" in required
        assert "slope" in required
        assert "aspect" not in required  # aspect is optional

    @pytest.mark.asyncio
    async def test_grass_buffer_tool_definition(self):
        """Test grass_buffer tool definition."""
        tools = await grass_mcp_server.list_tools()
        buffer_tool = next((t for t in tools if t.name == "grass_buffer"), None)

        assert buffer_tool is not None
        assert "buffer" in buffer_tool.description.lower()

        schema = buffer_tool.inputSchema
        props = schema["properties"]
        assert "input_map" in props
        assert "output_map" in props
        assert "distance" in props

        # Check distance is a number type
        assert props["distance"]["type"] == "number"

    @pytest.mark.asyncio
    async def test_grass_list_maps_tool_definition(self):
        """Test grass_list_maps tool definition."""
        tools = await grass_mcp_server.list_tools()
        list_tool = next((t for t in tools if t.name == "grass_list_maps"), None)

        assert list_tool is not None

        schema = list_tool.inputSchema
        props = schema["properties"]
        assert "map_type" in props

        # Check enum values
        map_type_prop = props["map_type"]
        assert "enum" in map_type_prop
        enum_values = map_type_prop["enum"]
        assert "raster" in enum_values
        assert "vector" in enum_values
        assert "all" in enum_values

    @pytest.mark.asyncio
    async def test_grass_univar_tool_definition(self):
        """Test grass_raster_univar tool definition."""
        tools = await grass_mcp_server.list_tools()
        univar_tool = next((t for t in tools if t.name == "grass_raster_univar"), None)

        assert univar_tool is not None
        assert "statistics" in univar_tool.description.lower()

        schema = univar_tool.inputSchema
        props = schema["properties"]
        assert "extended" in props
        assert props["extended"]["type"] == "boolean"

    @pytest.mark.asyncio
    async def test_grass_region_info_tool_definition(self):
        """Test grass_region_info tool definition."""
        tools = await grass_mcp_server.list_tools()
        region_tool = next((t for t in tools if t.name == "grass_region_info"), None)

        assert region_tool is not None
        assert "region" in region_tool.description.lower()

        schema = region_tool.inputSchema
        required = schema["required"]
        assert "gisdbase" in required
        assert "location" in required

    @pytest.mark.asyncio
    async def test_all_schemas_are_valid_json_schema(self):
        """Test that all tool schemas are valid JSON schema format."""
        tools = await grass_mcp_server.list_tools()

        for tool in tools:
            schema = tool.inputSchema
            assert "type" in schema
            assert schema["type"] == "object"
            assert "properties" in schema

            # Check all properties have type
            for prop_name, prop_def in schema["properties"].items():
                assert "type" in prop_def or "enum" in prop_def, (
                    f"Property {prop_name} in {tool.name} missing type or enum"
                )
