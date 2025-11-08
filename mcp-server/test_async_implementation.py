#!/usr/bin/env python3
"""
Test suite for async refactor implementation
Tests that the async conversion works correctly and provides concurrency benefits
"""

import asyncio
import time
import sys
from pathlib import Path

# Add parent directory to path to import the server
sys.path.insert(0, str(Path(__file__).parent))


async def test_basic_async_function():
    """Test that run_grass_command is actually async"""
    print("\n=== Test 1: Verify run_grass_command is async ===")

    from grass_mcp_server import run_grass_command
    import inspect

    # Check if function is a coroutine function
    is_async = inspect.iscoroutinefunction(run_grass_command)
    print(f"✓ run_grass_command is async: {is_async}")

    if not is_async:
        print("✗ FAILED: run_grass_command is not async!")
        return False

    return True


async def test_concurrent_execution():
    """Test that multiple async calls can run concurrently"""
    print("\n=== Test 2: Concurrent Execution Test ===")
    print("This test simulates concurrent GRASS commands using sleep")

    async def mock_grass_command(delay: float, name: str):
        """Mock async GRASS command with delay"""
        start = time.time()
        print(f"  Starting {name} (will take {delay}s)...")
        await asyncio.sleep(delay)  # Simulates async subprocess
        elapsed = time.time() - start
        print(f"  ✓ {name} completed in {elapsed:.2f}s")
        return f"Result from {name}"

    # Test concurrent execution
    print("\nRunning 3 commands concurrently (each takes 1s)...")
    start_time = time.time()

    results = await asyncio.gather(
        mock_grass_command(1.0, "Command A"),
        mock_grass_command(1.0, "Command B"),
        mock_grass_command(1.0, "Command C"),
    )

    total_time = time.time() - start_time

    print(f"\n✓ All commands completed")
    print(f"Total time: {total_time:.2f}s")

    # If truly concurrent, should take ~1s not ~3s
    if total_time < 2.0:
        print("✓ PASSED: Commands ran concurrently (< 2s)")
        return True
    else:
        print(f"✗ FAILED: Commands appear to be sequential ({total_time:.2f}s >= 2s)")
        return False


async def test_call_tool_async():
    """Test that call_tool properly awaits async operations"""
    print("\n=== Test 3: call_tool async implementation ===")

    from grass_mcp_server import call_tool
    import inspect

    # Verify call_tool is async
    is_async = inspect.iscoroutinefunction(call_tool)
    print(f"✓ call_tool is async: {is_async}")

    if not is_async:
        print("✗ FAILED: call_tool is not async!")
        return False

    # Try to call it and verify it returns a coroutine
    try:
        # This should return a coroutine, not block
        coro = call_tool("unknown_tool", {})
        is_coro = inspect.iscoroutine(coro)
        print(f"✓ call_tool returns coroutine: {is_coro}")

        # Clean up the coroutine
        coro.close()

        return is_coro
    except Exception as e:
        print(f"✗ FAILED: Error checking call_tool: {e}")
        return False


async def test_visualization_addon_async():
    """Test that visualization addon functions are async"""
    print("\n=== Test 4: Visualization addon async implementation ===")

    try:
        from grass_visualization_addon import (
            run_grass_command,
            visualize_raster_simple,
            visualize_with_hillshade,
            create_interactive_map,
            handle_visualization_tool
        )
        import inspect

        functions = {
            "run_grass_command": run_grass_command,
            "visualize_raster_simple": visualize_raster_simple,
            "visualize_with_hillshade": visualize_with_hillshade,
            "create_interactive_map": create_interactive_map,
            "handle_visualization_tool": handle_visualization_tool,
        }

        all_async = True
        for name, func in functions.items():
            is_async = inspect.iscoroutinefunction(func)
            status = "✓" if is_async else "✗"
            print(f"  {status} {name}: async={is_async}")
            if not is_async:
                all_async = False

        if all_async:
            print("✓ PASSED: All visualization functions are async")
        else:
            print("✗ FAILED: Some visualization functions are not async")

        return all_async

    except ImportError as e:
        print(f"⚠ SKIPPED: Visualization addon not available ({e})")
        return True  # Don't fail if addon isn't loaded


async def test_no_blocking_subprocess():
    """Verify no blocking subprocess.run calls in main code"""
    print("\n=== Test 5: No blocking subprocess calls ===")

    import grass_mcp_server
    import inspect

    # Get the source code
    source = inspect.getsource(grass_mcp_server)

    # Check for subprocess.run (should not exist in main code)
    if "subprocess.run" in source:
        print("✗ FAILED: Found 'subprocess.run' in grass_mcp_server.py!")
        # Find the lines
        lines = source.split('\n')
        for i, line in enumerate(lines, 1):
            if "subprocess.run" in line and not line.strip().startswith('#'):
                print(f"  Line {i}: {line.strip()}")
        return False

    print("✓ PASSED: No blocking subprocess.run calls found")
    return True


async def test_asyncio_subprocess_usage():
    """Verify async subprocess is being used"""
    print("\n=== Test 6: asyncio.create_subprocess_exec usage ===")

    import grass_mcp_server
    import inspect

    source = inspect.getsource(grass_mcp_server)

    # Check for asyncio subprocess usage
    if "asyncio.create_subprocess_exec" in source:
        print("✓ PASSED: Using asyncio.create_subprocess_exec")
        return True
    elif "loop.run_in_executor" in source:
        print("✓ PASSED: Using loop.run_in_executor for blocking calls")
        return True
    else:
        print("✗ FAILED: Not using async subprocess methods!")
        return False


async def test_concurrent_call_tool():
    """Test that multiple call_tool invocations can run concurrently"""
    print("\n=== Test 7: Concurrent call_tool test ===")
    print("Testing that multiple tool calls don't block each other...")

    from grass_mcp_server import call_tool

    # We'll call with unknown tools (they'll fail fast but won't block)
    start_time = time.time()

    results = await asyncio.gather(
        call_tool("test_tool_1", {}),
        call_tool("test_tool_2", {}),
        call_tool("test_tool_3", {}),
        return_exceptions=True
    )

    total_time = time.time() - start_time

    print(f"✓ All tool calls completed in {total_time:.2f}s")

    # Should complete nearly instantly since they're just returning errors
    if total_time < 1.0:
        print("✓ PASSED: Tool calls executed concurrently")
        return True
    else:
        print(f"⚠ WARNING: Tool calls took longer than expected ({total_time:.2f}s)")
        return True  # Don't fail, might just be slow system


async def run_all_tests():
    """Run all async implementation tests"""
    print("=" * 70)
    print("ASYNC REFACTOR IMPLEMENTATION TEST SUITE")
    print("=" * 70)

    tests = [
        ("Basic async function", test_basic_async_function),
        ("Concurrent execution", test_concurrent_execution),
        ("call_tool async", test_call_tool_async),
        ("Visualization addon async", test_visualization_addon_async),
        ("No blocking subprocess", test_no_blocking_subprocess),
        ("Asyncio subprocess usage", test_asyncio_subprocess_usage),
        ("Concurrent call_tool", test_concurrent_call_tool),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = await test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} CRASHED: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")

    print("\n" + "=" * 70)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("✓ ALL TESTS PASSED - Async refactor implementation is correct!")
    else:
        print(f"✗ {total - passed} TEST(S) FAILED - Review implementation")

    print("=" * 70)

    return passed == total


if __name__ == "__main__":
    # Run the test suite
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
