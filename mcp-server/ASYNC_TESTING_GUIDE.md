# Async Refactor Testing Guide

**Purpose**: Verify the async refactor implementation works correctly and provides expected performance improvements.

---

## Quick Start

```bash
cd /root/aiyifyproject/repos/grass/mcp-server

# 1. Run automated async implementation tests
python3 test_async_implementation.py

# 2. Run performance/load tests
python3 test_async_performance.py

# 3. Manual testing with MCP server (optional, requires GRASS GIS)
python3 grass_mcp_server.py
```

---

## Test Suite 1: Implementation Verification

**File**: `test_async_implementation.py`

**Purpose**: Verify that the async refactor was implemented correctly.

### Tests Included:

1. **Basic async function** - Verifies `run_grass_command` is an async function
2. **Concurrent execution** - Proves async allows concurrent operations
3. **call_tool async** - Verifies main handler is async
4. **Visualization addon async** - Checks all visualization functions are async
5. **No blocking subprocess** - Confirms no `subprocess.run()` in code
6. **Asyncio subprocess usage** - Verifies using `asyncio.create_subprocess_exec`
7. **Concurrent call_tool** - Tests multiple tool calls don't block each other

### Expected Output:

```
======================================================================
ASYNC REFACTOR IMPLEMENTATION TEST SUITE
======================================================================

=== Test 1: Verify run_grass_command is async ===
✓ run_grass_command is async: True

=== Test 2: Concurrent Execution Test ===
  Starting Command A (will take 1s)...
  Starting Command B (will take 1s)...
  Starting Command C (will take 1s)...
  ✓ Command A completed in 1.00s
  ✓ Command B completed in 1.00s
  ✓ Command C completed in 1.00s

✓ All commands completed
Total time: 1.01s
✓ PASSED: Commands ran concurrently (< 2s)

... [additional tests] ...

======================================================================
TEST SUMMARY
======================================================================
✓ PASS: Basic async function
✓ PASS: Concurrent execution
✓ PASS: call_tool async
✓ PASS: Visualization addon async
✓ PASS: No blocking subprocess
✓ PASS: Asyncio subprocess usage
✓ PASS: Concurrent call_tool

======================================================================
Results: 7/7 tests passed
✓ ALL TESTS PASSED - Async refactor implementation is correct!
======================================================================
```

---

## Test Suite 2: Performance Testing

**File**: `test_async_performance.py`

**Purpose**: Demonstrate the performance benefits of async refactor.

### Tests Included:

1. **Sequential vs Concurrent** - Compares old blocking vs new async approach
2. **Multi-user Load Test** - Simulates 5 concurrent users with 3 commands each
3. **Request Latency** - Ensures async doesn't add overhead
4. **Burst Load Handling** - Tests 20 simultaneous requests

### Expected Output:

```
======================================================================
PERFORMANCE TEST: Sequential vs Concurrent Execution
======================================================================

1. Sequential execution (6 commands, 0.5s each):
   Simulating old blocking subprocess.run() behavior...
   ✓ Completed in 3.01s
   Expected: ~3.0s (sequential)

2. Concurrent execution (6 commands, 0.5s each):
   Using new asyncio.create_subprocess_exec() behavior...
   ✓ Completed in 0.51s
   Expected: ~0.5s (concurrent)

======================================================================
PERFORMANCE ANALYSIS
======================================================================
Sequential time:  3.01s
Concurrent time:  0.51s
Speedup:          5.90x
Time saved:       2.50s (83.1%)

✓ EXCELLENT: Significant performance improvement from async!

======================================================================
LOAD TEST: 5 concurrent users, 3 commands each
======================================================================

✓ All 5 users completed
✓ Total commands executed: 15
✓ Total time: 0.91s

Throughput: 16.48 commands/second

If sequential: ~4.5s
Actual time:    0.91s
Speedup:        4.95x
```

---

## Test Suite 3: Manual Testing with GRASS GIS

**Prerequisites**: GRASS GIS must be installed and a test location available.

### Setup Test Environment

```bash
# Create test GRASS location (if you don't have one)
grass -c EPSG:4326 ~/grassdata/test_location -e

# Create some test data
grass ~/grassdata/test_location/PERMANENT

# Inside GRASS session:
g.region n=40 s=0 e=40 w=0 res=1
r.mapcalc "elevation = row() + col()"
r.mapcalc "test_raster = sin(row()) * cos(col())"
v.random output=test_points n=100
exit
```

### Test 1: Single Tool Call

```bash
# Start the MCP server
python3 grass_mcp_server.py
```

In Claude Desktop or another MCP client, run:

```
Get information about the raster map "elevation" in
gisdbase: ~/grassdata
location: test_location
```

**Expected**: Fast response with raster info (no blocking).

### Test 2: Concurrent Tool Calls

In Claude Desktop, send multiple requests quickly:

```
1. Get raster info for "elevation"
2. Get raster info for "test_raster"
3. List all maps in the location
```

**Expected**: All three requests process concurrently, not sequentially.

**Before Async** (blocking):
- Request 1: 0-2s
- Request 2: 2-4s (waits for 1)
- Request 3: 4-6s (waits for 2)
- Total: ~6s

**After Async** (concurrent):
- Request 1: 0-2s
- Request 2: 0-2s (parallel with 1)
- Request 3: 0-2s (parallel with 1 & 2)
- Total: ~2s

### Test 3: Visualization Concurrency

```
1. Create a visualization of "elevation" map
2. Create a visualization of "test_raster" map
```

**Expected**: Both visualizations generate concurrently.

---

## Test Suite 4: Integration Testing

### Test with Real MCP Client

**Using Claude Desktop**:

1. Configure MCP server in Claude Desktop settings
2. Start a conversation
3. Request multiple GRASS operations in quick succession
4. Observe response times

**Example conversation**:
```
User: "I need info on three raster maps: elevation, test_raster, and slope.
       Can you get all three for me?"

Expected: Claude makes 3 concurrent tool calls, gets results in ~2-3s
         instead of 6-9s (sequential)
```

### Test with Python MCP Client

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_concurrent_requests():
    server_params = StdioServerParameters(
        command="python3",
        args=["grass_mcp_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Make 3 concurrent requests
            results = await asyncio.gather(
                session.call_tool("grass_raster_info", {
                    "map_name": "elevation",
                    "gisdbase": "~/grassdata",
                    "location": "test_location"
                }),
                session.call_tool("grass_raster_info", {
                    "map_name": "test_raster",
                    "gisdbase": "~/grassdata",
                    "location": "test_location"
                }),
                session.call_tool("grass_list_maps", {
                    "gisdbase": "~/grassdata",
                    "location": "test_location"
                }),
            )

            print(f"Got {len(results)} results concurrently!")

asyncio.run(test_concurrent_requests())
```

---

## Debugging Tips

### Check if Async is Working

```python
import asyncio
import inspect
from grass_mcp_server import run_grass_command

# Should print True
print(inspect.iscoroutinefunction(run_grass_command))
```

### Monitor Concurrent Execution

Add timing logs to `grass_mcp_server.py`:

```python
import time

async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    start = time.time()
    print(f"[{start:.2f}] Tool {name} started")

    # ... existing code ...

    elapsed = time.time() - start
    print(f"[{time.time():.2f}] Tool {name} completed in {elapsed:.2f}s")
```

### Check for Blocking Calls

```bash
# Should return nothing (no matches in main files)
grep -n "subprocess.run" grass_mcp_server.py grass_visualization_addon.py
```

### Verify Async Subprocess Usage

```bash
# Should find multiple matches
grep -n "asyncio.create_subprocess_exec" grass_mcp_server.py grass_visualization_addon.py

# Or check for executor usage
grep -n "run_in_executor" grass_mcp_server.py
```

---

## Performance Benchmarking

### Method 1: Time Tool Execution

```python
import asyncio
import time
from grass_mcp_server import call_tool

async def benchmark():
    # Single call
    start = time.time()
    await call_tool("grass_list_maps", {
        "gisdbase": "~/grassdata",
        "location": "test_location"
    })
    single_time = time.time() - start
    print(f"Single call: {single_time:.2f}s")

    # Concurrent calls
    start = time.time()
    await asyncio.gather(*[
        call_tool("grass_list_maps", {
            "gisdbase": "~/grassdata",
            "location": "test_location"
        })
        for _ in range(5)
    ])
    concurrent_time = time.time() - start
    print(f"5 concurrent calls: {concurrent_time:.2f}s")
    print(f"Speedup: {(single_time * 5) / concurrent_time:.2f}x")

asyncio.run(benchmark())
```

### Method 2: Load Testing with Locust

```python
# locustfile.py
from locust import User, task, between
import asyncio
from mcp import ClientSession
# ... setup MCP client ...

class MCPUser(User):
    wait_time = between(1, 3)

    @task
    def get_raster_info(self):
        # Make MCP tool call
        pass
```

---

## Expected Results Summary

| Test Type | Metric | Before (Blocking) | After (Async) | Improvement |
|-----------|--------|-------------------|---------------|-------------|
| Implementation | All tests pass | N/A | 7/7 | ✓ |
| Concurrent (6 cmds) | Time | ~3.0s | ~0.5s | 6x faster |
| Load (5 users, 3 cmds) | Time | ~4.5s | ~0.9s | 5x faster |
| Burst (20 requests) | Time | ~10.0s | ~0.5s | 20x faster |
| Latency | Per request | Same | Same | No overhead |

---

## Troubleshooting

### Test Fails: "run_grass_command is not async"

**Problem**: Function wasn't converted to async
**Solution**: Check line 317 in grass_mcp_server.py, should be `async def`

### Test Fails: "Commands appear to be sequential"

**Problem**: Missing `await` keyword somewhere
**Solution**: Check all `run_grass_command()` calls have `await`

### ImportError: No module named 'grass'

**Problem**: GRASS GIS Python bindings not installed
**Solution**: Install GRASS GIS or skip real GRASS tests

### Test Passes but Manual Testing Shows Blocking

**Problem**: MCP framework might be serializing requests
**Solution**: Check MCP client configuration, ensure it supports concurrent requests

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Test Async Implementation

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Run async tests
        run: |
          cd mcp-server
          python3 test_async_implementation.py
      - name: Run performance tests
        run: |
          cd mcp-server
          python3 test_async_performance.py
```

---

## Next Steps After Testing

1. ✓ Verify all tests pass
2. ✓ Benchmark performance improvements
3. ✓ Document results
4. → Move to Week 1 Day 3-5: Implement per-user ephemeral sessions
5. → Week 2: Session-aware tool migration
6. → Week 3: Load testing with real concurrent users

---

## Questions?

- Review `ASYNC_REFACTOR_SUMMARY.md` for implementation details
- Check `EXECUTION_PLAN_PHASE1.md` for overall plan context
- See `FINAL_STRATEGIC_RECOMMENDATION.md` for architectural decisions

---

**Last Updated**: November 8, 2025
**Status**: Ready for testing
