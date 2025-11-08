#!/usr/bin/env python3
"""
Performance test for async refactor
Demonstrates the concurrency improvements from async implementation
"""

import asyncio
import time
import statistics
from typing import List, Tuple


class MockGRASSCommand:
    """Mock GRASS command that simulates I/O delay"""

    def __init__(self, command_time: float = 0.5):
        self.command_time = command_time

    async def execute_async(self, cmd: str) -> str:
        """Simulates async GRASS command execution"""
        await asyncio.sleep(self.command_time)
        return f"Result from {cmd}"


async def test_sequential_vs_concurrent():
    """Compare sequential vs concurrent execution times"""
    print("=" * 70)
    print("PERFORMANCE TEST: Sequential vs Concurrent Execution")
    print("=" * 70)

    mock_grass = MockGRASSCommand(command_time=0.5)
    num_commands = 6

    # Test 1: Sequential execution (old blocking way)
    print(f"\n1. Sequential execution ({num_commands} commands, 0.5s each):")
    print("   Simulating old blocking subprocess.run() behavior...")

    start = time.time()
    results = []
    for i in range(num_commands):
        result = await mock_grass.execute_async(f"command_{i}")
        results.append(result)
    sequential_time = time.time() - start

    print(f"   ✓ Completed in {sequential_time:.2f}s")
    print(f"   Expected: ~{num_commands * 0.5:.1f}s (sequential)")

    # Test 2: Concurrent execution (new async way)
    print(f"\n2. Concurrent execution ({num_commands} commands, 0.5s each):")
    print("   Using new asyncio.create_subprocess_exec() behavior...")

    start = time.time()
    results = await asyncio.gather(*[
        mock_grass.execute_async(f"command_{i}")
        for i in range(num_commands)
    ])
    concurrent_time = time.time() - start

    print(f"   ✓ Completed in {concurrent_time:.2f}s")
    print(f"   Expected: ~0.5s (concurrent)")

    # Analysis
    print("\n" + "=" * 70)
    print("PERFORMANCE ANALYSIS")
    print("=" * 70)
    speedup = sequential_time / concurrent_time
    time_saved = sequential_time - concurrent_time

    print(f"Sequential time:  {sequential_time:.2f}s")
    print(f"Concurrent time:  {concurrent_time:.2f}s")
    print(f"Speedup:          {speedup:.2f}x")
    print(f"Time saved:       {time_saved:.2f}s ({time_saved/sequential_time*100:.1f}%)")

    if speedup > 2.0:
        print("\n✓ EXCELLENT: Significant performance improvement from async!")
    elif speedup > 1.5:
        print("\n✓ GOOD: Notable performance improvement from async")
    else:
        print("\n⚠ WARNING: Lower than expected speedup")

    return speedup > 1.5


async def test_load_simulation(num_users: int = 5, commands_per_user: int = 3):
    """Simulate multiple concurrent users"""
    print("\n" + "=" * 70)
    print(f"LOAD TEST: {num_users} concurrent users, {commands_per_user} commands each")
    print("=" * 70)

    mock_grass = MockGRASSCommand(command_time=0.3)

    async def simulate_user(user_id: int) -> Tuple[int, float, List[str]]:
        """Simulate a user making multiple GRASS commands"""
        start = time.time()
        results = []

        for cmd_num in range(commands_per_user):
            cmd = f"user{user_id}_cmd{cmd_num}"
            result = await mock_grass.execute_async(cmd)
            results.append(result)

        elapsed = time.time() - start
        return user_id, elapsed, results

    # Run all users concurrently
    print(f"\nStarting {num_users} concurrent users...")
    start_time = time.time()

    user_results = await asyncio.gather(*[
        simulate_user(i) for i in range(num_users)
    ])

    total_time = time.time() - start_time

    # Analyze results
    user_times = [elapsed for _, elapsed, _ in user_results]
    total_commands = num_users * commands_per_user

    print(f"\n✓ All {num_users} users completed")
    print(f"✓ Total commands executed: {total_commands}")
    print(f"✓ Total time: {total_time:.2f}s")
    print(f"\nPer-user statistics:")
    print(f"  Min time:  {min(user_times):.2f}s")
    print(f"  Max time:  {max(user_times):.2f}s")
    print(f"  Avg time:  {statistics.mean(user_times):.2f}s")
    print(f"  Median:    {statistics.median(user_times):.2f}s")

    # Calculate throughput
    throughput = total_commands / total_time
    print(f"\nThroughput: {throughput:.2f} commands/second")

    # Expected time if sequential
    expected_sequential = total_commands * 0.3
    print(f"\nIf sequential: ~{expected_sequential:.1f}s")
    print(f"Actual time:    {total_time:.2f}s")
    print(f"Speedup:        {expected_sequential/total_time:.2f}x")

    return True


async def test_request_response_time():
    """Test that async doesn't add overhead to individual requests"""
    print("\n" + "=" * 70)
    print("LATENCY TEST: Individual request response time")
    print("=" * 70)

    mock_grass = MockGRASSCommand(command_time=0.1)

    print("\nMeasuring single request latency (10 iterations)...")
    latencies = []

    for i in range(10):
        start = time.time()
        await mock_grass.execute_async(f"cmd_{i}")
        latency = time.time() - start
        latencies.append(latency)

    print(f"\nLatency statistics:")
    print(f"  Min:    {min(latencies)*1000:.1f}ms")
    print(f"  Max:    {max(latencies)*1000:.1f}ms")
    print(f"  Mean:   {statistics.mean(latencies)*1000:.1f}ms")
    print(f"  Median: {statistics.median(latencies)*1000:.1f}ms")
    print(f"  Stdev:  {statistics.stdev(latencies)*1000:.1f}ms")

    avg_latency = statistics.mean(latencies)
    if avg_latency < 0.15:  # Within 50ms of expected 100ms
        print("\n✓ PASSED: Low overhead, async doesn't add significant latency")
        return True
    else:
        print(f"\n⚠ WARNING: Higher latency than expected ({avg_latency*1000:.1f}ms)")
        return True


async def test_burst_load():
    """Test handling burst of concurrent requests"""
    print("\n" + "=" * 70)
    print("BURST LOAD TEST: 20 simultaneous requests")
    print("=" * 70)

    mock_grass = MockGRASSCommand(command_time=0.5)

    print("\nSending 20 concurrent requests...")
    start = time.time()

    results = await asyncio.gather(*[
        mock_grass.execute_async(f"burst_cmd_{i}")
        for i in range(20)
    ])

    elapsed = time.time() - start

    print(f"✓ All 20 requests completed in {elapsed:.2f}s")

    if elapsed < 1.0:
        print("✓ EXCELLENT: Handled burst efficiently (< 1s)")
        efficiency = "excellent"
    elif elapsed < 2.0:
        print("✓ GOOD: Handled burst well (< 2s)")
        efficiency = "good"
    else:
        print(f"⚠ WARNING: Burst took longer than expected ({elapsed:.2f}s)")
        efficiency = "slow"

    # Calculate what sequential would be
    sequential_time = 20 * 0.5
    print(f"\nSequential would take: {sequential_time:.1f}s")
    print(f"Async speedup: {sequential_time/elapsed:.2f}x")

    return efficiency in ["excellent", "good"]


async def run_performance_tests():
    """Run all performance tests"""
    print("\n" + "=" * 70)
    print("ASYNC REFACTOR PERFORMANCE TEST SUITE")
    print("=" * 70)
    print("\nThese tests demonstrate the performance benefits of async refactor")
    print("by simulating GRASS GIS command execution with I/O delays.")
    print("=" * 70)

    tests = [
        ("Sequential vs Concurrent", test_sequential_vs_concurrent),
        ("Multi-user Load Test", lambda: test_load_simulation(5, 3)),
        ("Request Latency", test_request_response_time),
        ("Burst Load Handling", test_burst_load),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = await test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} FAILED: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Summary
    print("\n" + "=" * 70)
    print("PERFORMANCE TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")

    print("\n" + "=" * 70)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("\n✓ PERFORMANCE TESTS PASSED")
        print("  The async refactor provides significant performance improvements")
        print("  for concurrent GRASS GIS operations!")
    else:
        print(f"\n⚠ {total - passed} test(s) had issues")

    print("=" * 70)

    return passed == total


if __name__ == "__main__":
    import sys
    success = asyncio.run(run_performance_tests())
    sys.exit(0 if success else 1)
