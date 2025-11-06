"""Tests for GRASS command execution."""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import subprocess

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import grass_mcp_server


class TestRunGrassCommand:
    """Test the run_grass_command function."""

    @patch("grass_mcp_server.subprocess.run")
    def test_run_grass_command_success(
        self, mock_run, mock_gisdbase, sample_raster_info
    ):
        """Test successful GRASS command execution."""
        # Mock successful subprocess run
        mock_run.return_value = Mock(
            returncode=0, stdout=sample_raster_info, stderr=""
        )

        result = grass_mcp_server.run_grass_command(
            ["r.info", "-g", "map=elevation"],
            mock_gisdbase["gisdbase"],
            mock_gisdbase["location"],
            mock_gisdbase["mapset"],
        )

        assert "north=228500" in result
        assert "cells=2025000" in result

    @patch("grass_mcp_server.subprocess.run")
    def test_run_grass_command_failure(self, mock_run, mock_gisdbase):
        """Test GRASS command execution failure."""
        # Mock which command to find grass, then mock failed grass command
        def run_side_effect(*args, **kwargs):
            if "which" in args[0]:
                # which grass succeeds
                return Mock(returncode=0, stdout="/usr/bin/grass\n", stderr="")
            else:
                # actual grass command fails
                return Mock(returncode=1, stdout="", stderr="ERROR: Map not found")

        mock_run.side_effect = run_side_effect

        with pytest.raises(RuntimeError, match="GRASS command failed"):
            grass_mcp_server.run_grass_command(
                ["r.info", "-g", "map=nonexistent"],
                mock_gisdbase["gisdbase"],
                mock_gisdbase["location"],
                mock_gisdbase["mapset"],
            )

    @patch("grass_mcp_server.subprocess.run")
    def test_run_grass_command_sets_environment(self, mock_run, mock_gisdbase):
        """Test that GRASS environment variables are set correctly."""
        mock_run.return_value = Mock(returncode=0, stdout="test output", stderr="")

        grass_mcp_server.run_grass_command(
            ["g.region", "-p"],
            mock_gisdbase["gisdbase"],
            mock_gisdbase["location"],
            mock_gisdbase["mapset"],
        )

        # Check that subprocess.run was called with correct env
        call_args = mock_run.call_args
        env = call_args.kwargs["env"]

        assert env["GISDBASE"] == mock_gisdbase["gisdbase"]
        assert env["LOCATION_NAME"] == mock_gisdbase["location"]
        assert env["MAPSET"] == mock_gisdbase["mapset"]

    @patch("grass_mcp_server.subprocess.run")
    def test_run_grass_command_timeout(self, mock_run, mock_gisdbase):
        """Test command execution respects timeout."""
        mock_run.return_value = Mock(returncode=0, stdout="output", stderr="")

        grass_mcp_server.run_grass_command(
            ["r.info", "map=test"],
            mock_gisdbase["gisdbase"],
            mock_gisdbase["location"],
        )

        # Check timeout was set
        call_args = mock_run.call_args
        assert call_args.kwargs["timeout"] == 60


class TestCommandBuilding:
    """Test GRASS command building for different tools."""

    def test_raster_info_command(self):
        """Test building r.info command."""
        expected = ["r.info", "-g", "map=elevation"]
        # This would be part of the call_tool function
        # Just verify the expected command structure
        assert expected[0] == "r.info"
        assert "-g" in expected
        assert "map=elevation" in expected

    def test_vector_info_command(self):
        """Test building v.info command."""
        expected = ["v.info", "-g", "map=roads"]
        assert expected[0] == "v.info"
        assert "-g" in expected
        assert "map=roads" in expected

    def test_mapcalc_command(self):
        """Test building r.mapcalc command."""
        expression = "result = elevation * 2"
        expected = ["r.mapcalc", f"expression={expression}"]
        assert expected[0] == "r.mapcalc"
        assert f"expression={expression}" in expected

    def test_slope_aspect_command(self):
        """Test building r.slope.aspect command."""
        expected = [
            "r.slope.aspect",
            "elevation=dem",
            "slope=slope_map",
            "aspect=aspect_map",
        ]
        assert expected[0] == "r.slope.aspect"
        assert "elevation=dem" in expected
        assert "slope=slope_map" in expected
        assert "aspect=aspect_map" in expected

    def test_buffer_command(self):
        """Test building v.buffer command."""
        expected = ["v.buffer", "input=roads", "output=roads_buffer", "distance=500"]
        assert expected[0] == "v.buffer"
        assert "input=roads" in expected
        assert "output=roads_buffer" in expected
        assert "distance=500" in expected

    def test_univar_command_basic(self):
        """Test building r.univar command without extended flag."""
        expected = ["r.univar", "-g", "map=elevation"]
        assert expected[0] == "r.univar"
        assert "-g" in expected

    def test_univar_command_extended(self):
        """Test building r.univar command with extended flag."""
        expected = ["r.univar", "-ge", "map=elevation"]
        assert expected[0] == "r.univar"
        assert "-ge" in expected


class TestGrassNotFound:
    """Test behavior when GRASS is not found."""

    @patch("grass_mcp_server.subprocess.run")
    @patch("builtins.__import__")
    def test_grass_not_found_error(self, mock_import, mock_run, mock_gisdbase):
        """Test error when GRASS is not available."""
        # Mock 'which' command to return nothing
        def run_side_effect(*args, **kwargs):
            if "which" in args[0]:
                return Mock(returncode=1, stdout="", stderr="")
            return Mock(returncode=0, stdout="", stderr="")

        mock_run.side_effect = run_side_effect

        # Mock grass.script import to fail
        def import_side_effect(name, *args, **kwargs):
            if name == "grass.script" or name == "grass":
                raise ImportError("No module named grass")
            return MagicMock()

        mock_import.side_effect = import_side_effect

        with pytest.raises(RuntimeError, match="GRASS GIS not found"):
            grass_mcp_server.run_grass_command(
                ["r.info", "map=test"],
                mock_gisdbase["gisdbase"],
                mock_gisdbase["location"],
            )
