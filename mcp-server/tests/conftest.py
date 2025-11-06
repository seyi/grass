"""Pytest configuration and fixtures for GRASS MCP Server tests."""

import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, MagicMock
import pytest


@pytest.fixture
def mock_gisdbase(tmp_path):
    """Create a mock GRASS database structure."""
    gisdbase = tmp_path / "grassdata"
    location = gisdbase / "test_location"
    mapset = location / "PERMANENT"

    # Create directory structure
    mapset.mkdir(parents=True)
    (mapset / "WIND").touch()
    (mapset / "cellhd").mkdir()
    (mapset / "cell").mkdir()
    (mapset / "vector").mkdir()

    return {
        "gisdbase": str(gisdbase),
        "location": "test_location",
        "mapset": "PERMANENT",
    }


@pytest.fixture
def sample_raster_info():
    """Sample raster info output."""
    return """north=228500
south=215000
east=645000
west=630000
nsres=10
ewres=10
rows=1350
cols=1500
cells=2025000
datatype=FCELL
ncats=255
min=55.5787925720215
max=156.3299102783203
"""


@pytest.fixture
def sample_vector_info():
    """Sample vector info output."""
    return """name=roads
mapset=PERMANENT
location=nc_spm_08
database=/home/user/grassdata
title=Roads (test data)
scale=1:24000
creator=GRASS Development Team
organization=
source1=
source2=
comments=
level=2
num_dblinks=1
projection=Lambert Conformal Conic
zone=0
north=228513.08
south=215018.38
east=644781.63
west=629980.45
top=0.00
bottom=0.00
nodes=0
points=0
lines=1631
boundaries=0
centroids=0
areas=0
islands=0
primitives=1631
map3d=0
"""


@pytest.fixture
def sample_univar_output():
    """Sample r.univar output."""
    return """n=2025000
null_cells=0
cells=2025000
min=55.5787925720215
max=156.3299102783203
range=100.751117706299
mean=110.375440275933
mean_of_abs=110.375440275933
stddev=20.3153233205981
variance=412.712269134689
coeff_var=18.4053338303028
sum=223510516.558518
"""


@pytest.fixture
def sample_region_output():
    """Sample g.region output."""
    return """projection: 99 (Lambert Conformal Conic)
zone:       0
datum:      nad83
ellipsoid:  a=6378137 es=0.006694380022900787
north:      228500
south:      215000
west:       630000
east:       645000
nsres:      10
ewres:      10
rows:       1350
cols:       1500
cells:      2025000
"""


@pytest.fixture
def sample_map_list():
    """Sample g.list output."""
    return """elevation
slope
aspect
landuse
"""


@pytest.fixture
def mock_subprocess_success():
    """Mock subprocess with successful execution."""
    mock_result = Mock()
    mock_result.returncode = 0
    mock_result.stdout = "Command executed successfully"
    mock_result.stderr = ""
    return mock_result


@pytest.fixture
def mock_subprocess_failure():
    """Mock subprocess with failed execution."""
    mock_result = Mock()
    mock_result.returncode = 1
    mock_result.stdout = ""
    mock_result.stderr = "ERROR: Command failed"
    return mock_result


@pytest.fixture
def mock_grass_env(mock_gisdbase):
    """Mock GRASS environment variables."""
    return {
        "GISDBASE": mock_gisdbase["gisdbase"],
        "LOCATION_NAME": mock_gisdbase["location"],
        "MAPSET": mock_gisdbase["mapset"],
        "GRASS_VERBOSE": "0",
    }


@pytest.fixture
def mcp_tool_arguments(mock_gisdbase):
    """Common MCP tool arguments."""
    return {
        "map_name": "elevation",
        "gisdbase": mock_gisdbase["gisdbase"],
        "location": mock_gisdbase["location"],
        "mapset": mock_gisdbase["mapset"],
    }
