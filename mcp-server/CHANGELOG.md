# Changelog

All notable changes to the GRASS GIS MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-11-06

### Added
- Initial release of GRASS GIS MCP Server
- Core MCP server implementation using Python
- Support for raster operations:
  - `grass_raster_info` - Get raster map information
  - `grass_raster_univar` - Calculate univariate statistics
  - `grass_mapcalc` - Raster map algebra
  - `grass_slope_aspect` - Calculate terrain slope and aspect
- Support for vector operations:
  - `grass_vector_info` - Get vector map information
  - `grass_buffer` - Create buffers around features
- General utilities:
  - `grass_list_maps` - List maps in location/mapset
  - `grass_region_info` - Get computational region info
- Comprehensive documentation:
  - README with installation and configuration
  - USAGE guide with workflows and examples
  - Example configuration files
- Python package setup with pyproject.toml
- Requirements specification

### Technical Details
- Uses MCP Python SDK (mcp>=0.9.0)
- Supports both direct GRASS binary execution and Python API
- Stdio-based communication following MCP protocol
- Comprehensive error handling
- Support for multiple GRASS versions (8.0+)

### Documentation
- Installation instructions for multiple platforms
- Claude Desktop configuration examples
- 8 implemented tools with detailed schemas
- Usage workflows for common GIS tasks
- Troubleshooting guide

## [Unreleased]

### Planned Features
- Additional raster tools (r.neighbors, r.resample, r.contour)
- Additional vector tools (v.overlay, v.select, v.clean)
- Database query tools (db.select, db.execute)
- Imagery tools (i.cluster, i.maxlik)
- Temporal tools for time series analysis
- Support for 3D raster (voxel) operations
- Import/export tools for external data formats
- Visualization and map rendering tools
- Batch processing capabilities
- WebSocket transport option
- Configuration file support for default locations
