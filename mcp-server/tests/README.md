# Test Suite for GRASS GIS MCP Server

This directory contains the comprehensive test suite for the GRASS GIS MCP Server.

## Overview

The test suite includes:
- **Unit tests**: Test individual components without requiring GRASS installation
- **Integration tests**: Test the complete MCP server workflow
- **Mock tests**: Test behavior with mocked GRASS commands
- **Fixtures**: Reusable test data and configurations

## Test Structure

```
tests/
├── __init__.py          # Test package initialization
├── conftest.py          # Pytest fixtures and configuration
├── test_tools.py        # Tests for MCP tool definitions
├── test_commands.py     # Tests for GRASS command execution
├── test_mcp_server.py   # Integration tests for call_tool
└── README.md            # This file
```

## Running Tests

### Install Test Dependencies

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Or install from requirements-dev.txt
pip install -r requirements-dev.txt
```

### Run All Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=grass_mcp_server --cov-report=html
```

### Run Specific Test Files

```bash
# Test tool definitions only
pytest tests/test_tools.py

# Test command execution only
pytest tests/test_commands.py

# Test MCP server integration
pytest tests/test_mcp_server.py
```

### Run Specific Test Classes or Functions

```bash
# Run a specific test class
pytest tests/test_tools.py::TestToolDefinitions

# Run a specific test function
pytest tests/test_tools.py::TestToolDefinitions::test_list_tools_returns_list
```

### Run Tests by Markers

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"
```

## Test Categories

### 1. Tool Definition Tests (`test_tools.py`)

Tests the MCP tool definitions and schemas:
- ✅ All tools have required fields (name, description, inputSchema)
- ✅ Tool names are unique
- ✅ Input schemas are valid JSON Schema
- ✅ Required fields are properly specified
- ✅ Tool-specific schema validation

**Example:**
```python
async def test_grass_raster_info_tool_definition():
    """Test grass_raster_info tool definition."""
    tools = await grass_mcp_server.list_tools()
    raster_info_tool = next(
        (t for t in tools if t.name == "grass_raster_info"), None
    )
    assert raster_info_tool is not None
    # ... more assertions
```

### 2. Command Execution Tests (`test_commands.py`)

Tests GRASS command building and execution:
- ✅ Successful command execution
- ✅ Command failure handling
- ✅ Environment variable setup
- ✅ Timeout handling
- ✅ Command structure validation
- ✅ Error handling when GRASS not found

**Example:**
```python
def test_run_grass_command_success(mock_run, mock_gisdbase, sample_raster_info):
    """Test successful GRASS command execution."""
    mock_run.return_value = Mock(
        returncode=0, stdout=sample_raster_info, stderr=""
    )
    result = grass_mcp_server.run_grass_command(...)
    assert "north=228500" in result
```

### 3. MCP Server Integration Tests (`test_mcp_server.py`)

Tests the complete MCP server workflow:
- ✅ Tool calling via call_tool function
- ✅ Argument parsing and validation
- ✅ Response format (TextContent)
- ✅ Error handling and error messages
- ✅ Default parameter handling
- ✅ Server initialization

**Example:**
```python
async def test_call_grass_raster_info(mock_run_cmd, mock_gisdbase):
    """Test calling grass_raster_info tool."""
    result = await grass_mcp_server.call_tool(
        "grass_raster_info",
        {"map_name": "elevation", ...}
    )
    assert isinstance(result, list)
    assert isinstance(result[0], TextContent)
```

## Test Fixtures

### Available Fixtures (from `conftest.py`)

- **`mock_gisdbase`**: Creates a temporary GRASS database structure
- **`sample_raster_info`**: Sample output from `r.info -g`
- **`sample_vector_info`**: Sample output from `v.info -g`
- **`sample_univar_output`**: Sample output from `r.univar -g`
- **`sample_region_output`**: Sample output from `g.region -p`
- **`sample_map_list`**: Sample output from `g.list`
- **`mock_subprocess_success`**: Mock successful subprocess execution
- **`mock_subprocess_failure`**: Mock failed subprocess execution
- **`mock_grass_env`**: Mock GRASS environment variables
- **`mcp_tool_arguments`**: Common arguments for MCP tools

### Using Fixtures

```python
def test_example(mock_gisdbase, sample_raster_info):
    """Example test using fixtures."""
    # mock_gisdbase provides paths
    gisdbase = mock_gisdbase["gisdbase"]
    location = mock_gisdbase["location"]

    # sample_raster_info provides expected output
    assert "north=" in sample_raster_info
```

## Coverage

The test suite aims for high code coverage:

```bash
# Generate coverage report
pytest --cov=grass_mcp_server --cov-report=html

# View coverage report
open htmlcov/index.html
```

**Coverage goals:**
- Overall: > 85%
- Tool definitions: 100%
- Command execution: > 90%
- Error handling: > 80%

## Writing New Tests

### Test Naming Convention

- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`

### Example Test Template

```python
import pytest
from unittest.mock import Mock, patch

class TestNewFeature:
    """Tests for new feature."""

    @pytest.mark.asyncio
    async def test_feature_success(self, mock_gisdbase):
        """Test successful feature execution."""
        # Arrange
        expected = "expected output"

        # Act
        result = await some_function(mock_gisdbase)

        # Assert
        assert result == expected

    @pytest.mark.asyncio
    async def test_feature_failure(self):
        """Test feature failure handling."""
        with pytest.raises(RuntimeError, match="expected error"):
            await some_function_that_fails()
```

### Async Tests

For async functions, use `@pytest.mark.asyncio`:

```python
@pytest.mark.asyncio
async def test_async_function():
    """Test an async function."""
    result = await async_function()
    assert result is not None
```

### Mocking

Use `unittest.mock` for mocking:

```python
from unittest.mock import Mock, patch, MagicMock

@patch("grass_mcp_server.subprocess.run")
def test_with_mock(mock_run):
    """Test with mocked subprocess."""
    mock_run.return_value = Mock(returncode=0, stdout="output")
    result = function_that_calls_subprocess()
    mock_run.assert_called_once()
```

## Continuous Integration

The test suite is designed to run in CI environments:

```yaml
# Example GitHub Actions workflow
- name: Install dependencies
  run: pip install -e ".[dev]"

- name: Run tests
  run: pytest --cov=grass_mcp_server --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
```

## Troubleshooting

### Tests Fail with "GRASS not found"

These tests mock GRASS commands and should not require GRASS installation. If you see this error:
1. Check that mocking is working correctly
2. Verify `@patch` decorators are applied
3. Ensure mock fixtures are being used

### Async Tests Fail

Make sure you have `pytest-asyncio` installed:
```bash
pip install pytest-asyncio
```

And verify `pytest.ini` has:
```ini
asyncio_mode = auto
```

### Import Errors

Ensure the parent directory is in the Python path:
```python
sys.path.insert(0, str(Path(__file__).parent.parent))
```

## Best Practices

1. **Keep tests isolated**: Each test should be independent
2. **Use fixtures**: Reuse common setup with fixtures
3. **Mock external dependencies**: Don't rely on GRASS being installed
4. **Test edge cases**: Include tests for error conditions
5. **Write descriptive docstrings**: Explain what each test does
6. **Follow AAA pattern**: Arrange, Act, Assert
7. **Keep tests fast**: Use mocks to avoid slow operations

## Contributing

When adding new features to the MCP server:

1. ✅ Write tests first (TDD approach)
2. ✅ Ensure tests pass: `pytest`
3. ✅ Check coverage: `pytest --cov`
4. ✅ Format code: `black .`
5. ✅ Lint code: `ruff check .`

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-asyncio documentation](https://pytest-asyncio.readthedocs.io/)
- [unittest.mock documentation](https://docs.python.org/3/library/unittest.mock.html)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
