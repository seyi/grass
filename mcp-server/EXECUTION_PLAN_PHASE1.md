# GRASS GIS MCP Server - Phase 1 Execution Plan
**Planning Date**: November 7, 2025
**Planned By**: Zen Planner (Gemini 2.5 Pro)
**Duration**: 4 Weeks
**Team Size**: 2-3 Developers

---

## Executive Summary

This execution plan implements the strategic recommendations from multi-model analysis (Gemini Flash, Grok-4, Gemini Pro) that rejected shared sessions in favor of **per-user ephemeral sessions** due to GRASS GIS's inherent statefulness.

**Phase 1 Goal**: Transform blocking, single-threaded GRASS MCP server into production-ready, concurrent, session-managed system.

**Approach**: Incremental migration (lowest risk, continuous delivery)

---

## Timeline Overview

```
Week 1: Async Foundation
  |
  +-- Day 1-2: Refactor run_grass_command to async
  +-- Day 3-4: Migrate 2 tools + create test suite
  +-- Day 5: GO/NO-GO CHECKPOINT #1
  |
Week 2: Session Lifecycle
  |
  +-- Day 1-2: GrassSession class implementation
  +-- Day 3: SessionManager + MCP tools
  +-- Day 4: Integration testing
  +-- Day 5: GO/NO-GO CHECKPOINT #2
  |
Week 3: Tool Migration
  |
  +-- Day 1-2: State management tools + isolation tests
  +-- Day 3-4: Migrate read-only tools to sessions
  +-- Day 5: GO/NO-GO CHECKPOINT #3
  |
Week 4: Production Hardening
  |
  +-- Day 1-2: Migrate write operations
  +-- Day 3: Session timeout + cleanup
  +-- Day 4: Load testing (50 sessions, 100 req/s)
  +-- Day 5: PHASE 1 COMPLETE CHECKPOINT
```

---

## Week 1: Asynchronous Foundation

### Team Allocation
- **Dev 1 (Senior Python)**: Async refactor lead - 80% time
- **Dev 2 (GRASS Expert)**: Testing & validation - 60% time
- **Dev 3 (DevOps)**: Docker setup & documentation - 40% time

### Monday-Tuesday Goals

**Async Refactor** (Dev 1):
```python
# Current problem: LINE 302-378 in grass_mcp_server.py
# subprocess.run() blocks entire server

# Solution: Convert to async
async def run_grass_command_async(
    command: list[str],
    gisdbase: str,
    location: str,
    mapset: str = "PERMANENT",
) -> str:
    loop = asyncio.get_running_loop()
    env = os.environ.copy()
    env["GISDBASE"] = gisdbase
    env["LOCATION_NAME"] = location
    env["MAPSET"] = mapset

    # Run in executor to avoid blocking
    result = await loop.run_in_executor(
        None,
        functools.partial(
            subprocess.run,
            full_command,
            env=env,
            capture_output=True,
            text=True,
            timeout=60,
        )
    )

    if result.returncode != 0:
        raise RuntimeError(f"GRASS command failed: {result.stderr}")
    return result.stdout
```

**Update call_tool** (Dev 1):
- Change function signature to `async def`
- Update all tool handlers to await async command execution

**Deliverable**: Async-capable server with 2 migrated tools

### Wednesday-Thursday Goals

**Testing Infrastructure** (Dev 2):
```python
# tests/test_async.py
@pytest.mark.asyncio
async def test_concurrent_execution():
    """Test 10 concurrent requests"""
    tasks = [
        grass_region_info(gisdbase, location)
        for _ in range(10)
    ]

    start = time.time()
    results = await asyncio.gather(*tasks)
    duration = time.time() - start

    # Should complete in <5s (not 10x sequential time)
    assert duration < 5
    assert len(results) == 10
```

**Tool Migration** (Dev 1):
- Migrate `grass_region_info` to async
- Migrate `grass_list_maps` to async
- Add JSON output for `grass_list_maps`

**Deliverable**: 2 fully async tools with test coverage

### Friday - GO/NO-GO Checkpoint #1

**Success Criteria**:
- [ ] Async execution working without blocking
- [ ] Logs show concurrent request handling
- [ ] Response time <2s per request under load
- [ ] All async tests passing
- [ ] Docker environment configured

**Decision**:
- **GO**: Async working, no blocking → Proceed to Week 2
- **NO-GO**: Async issues persist → Extend Week 1, escalate

---

## Week 2: Session Lifecycle Management

### Monday-Tuesday Goals

**GrassSession Class** (Dev 2):
```python
class GrassSession:
    """Manages isolated GRASS session with temporary mapset"""

    def __init__(self, gisdbase: str, location: str):
        self.session_id = str(uuid.uuid4())
        self.mapset = f"session_{self.session_id[:8]}"
        self.gisdbase = gisdbase
        self.location = location
        self.last_access = time.time()

        # Create temporary mapset for isolation
        self._create_mapset()

    def _create_mapset(self):
        """Use g.mapset -c to create isolated workspace"""
        cmd = ["g.mapset", "-c", self.mapset]
        # Execute in GRASS context
        pass

    async def execute(self, command: list[str]) -> str:
        """Execute command in this session's mapset"""
        self.last_access = time.time()
        return await run_grass_command_async(
            command, self.gisdbase, self.location, self.mapset
        )

    def close(self):
        """Remove temporary mapset completely"""
        # g.mapset -r {self.mapset}
        pass
```

**Deliverable**: Working GrassSession class with tests

### Wednesday Goals

**SessionManager Class** (Dev 1):
```python
class SessionManager:
    """Manages lifecycle of all GRASS sessions"""

    def __init__(self):
        self.sessions = {}  # session_id -> GrassSession
        self.ttl = 1800  # 30 minutes
        self.max_sessions = 50

        # Start background cleanup task
        asyncio.create_task(self._cleanup_loop())

    def create_session(self, gisdbase: str, location: str) -> str:
        """Create new isolated session"""
        if len(self.sessions) >= self.max_sessions:
            raise RuntimeError("Max concurrent sessions reached")

        session = GrassSession(gisdbase, location)
        self.sessions[session.session_id] = session
        return session.session_id

    def get_session(self, session_id: str) -> GrassSession:
        """Get existing session or raise error"""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        return self.sessions[session_id]

    async def _cleanup_loop(self):
        """Background task: cleanup expired sessions"""
        while True:
            await asyncio.sleep(300)  # Every 5 minutes
            expired = [
                sid for sid, session in self.sessions.items()
                if time.time() - session.last_access > self.ttl
            ]
            for sid in expired:
                self.sessions[sid].close()
                del self.sessions[sid]
```

**New MCP Tools**:
- `create_session(gisdbase, location) -> session_id`
- `close_session(session_id) -> success`

**Deliverable**: Session management infrastructure

### Thursday Goals

**Session-Aware Execution** (Dev 1):
```python
# Update call_tool to accept optional session_id
async def call_tool(name: str, arguments: dict) -> dict:
    session_id = arguments.get("session_id")

    if session_id:
        # Use existing session
        session = session_manager.get_session(session_id)
        result = await session.execute(command)
    else:
        # Create temporary one-shot session
        temp_session = GrassSession(gisdbase, location)
        try:
            result = await temp_session.execute(command)
        finally:
            temp_session.close()

    return {"result": result}
```

**Deliverable**: Session-aware tool execution

### Friday - GO/NO-GO Checkpoint #2

**Success Criteria**:
- [ ] Sessions can be created and reused
- [ ] Session isolation verified (separate mapsets)
- [ ] Automatic cleanup working
- [ ] Session limit enforced

**Decision**:
- **GO**: Sessions working, isolation verified → Proceed to Week 3
- **NO-GO**: Session leaks detected → CRITICAL BLOCKER

---

## Week 3: State-Aware Tools & Migration

### Monday-Tuesday Goals

**State Management Tools** (Dev 1):
```python
# grass_set_region
async def grass_set_region(
    session_id: str,
    north: float,
    south: float,
    east: float,
    west: float,
    nsres: float,
    ewres: float
) -> dict:
    """Set computational region for session"""
    session = session_manager.get_session(session_id)
    cmd = [
        "g.region",
        f"n={north}", f"s={south}",
        f"e={east}", f"w={west}",
        f"nsres={nsres}", f"ewres={ewres}"
    ]
    await session.execute(cmd)
    return {"status": "success"}

# grass_get_region
async def grass_get_region(session_id: str) -> dict:
    """Get current region for session"""
    session = session_manager.get_session(session_id)
    result = await session.execute(["g.region", "-p"])
    # Parse result into JSON
    return parse_region_output(result)
```

**Isolation Testing** (Dev 2):
```python
@pytest.mark.asyncio
async def test_session_isolation():
    """Verify sessions don't interfere"""
    session_a = session_manager.create_session(gisdbase, location)
    session_b = session_manager.create_session(gisdbase, location)

    # Set different regions
    bounds_a = {"north": 100, "south": 0, "east": 100, "west": 0}
    bounds_b = {"north": 200, "south": 100, "east": 200, "west": 100}

    await grass_set_region(session_a, **bounds_a)
    await grass_set_region(session_b, **bounds_b)

    # Verify isolation
    region_a = await grass_get_region(session_a)
    region_b = await grass_get_region(session_b)

    assert region_a["north"] == 100
    assert region_b["north"] == 200
```

**Deliverable**: Verified session isolation

### Wednesday-Thursday Goals

**Read-Only Tool Migration** (Dev 1):
- `grass_raster_info(map_name, session_id?)`
- `grass_vector_info(map_name, session_id?)`
- `grass_raster_univar(map_name, session_id?)`

**JSON Output** (Dev 1):
```python
# Use GRASS -j flag for structured output
async def grass_raster_info(map_name: str, session_id: str = None) -> dict:
    """Get raster info with JSON output"""
    if session_id:
        session = session_manager.get_session(session_id)
        result = await session.execute(["r.info", "-j", f"map={map_name}"])
    else:
        # One-shot execution
        result = await run_grass_command_async(
            ["r.info", "-j", f"map={map_name}"],
            gisdbase, location
        )

    return json.loads(result)
```

**Deliverable**: 6/8 tools migrated

### Friday - GO/NO-GO Checkpoint #3

**Success Criteria**:
- [ ] `grass_set_region` in session A doesn't affect session B
- [ ] All read-only tools work with sessions
- [ ] JSON output for at least 3 tools
- [ ] 75% of tools migrated

**Decision**:
- **GO**: 75% migrated, isolation holds → Proceed to Week 4
- **NO-GO**: Cross-session interference → Rethink architecture

---

## Week 4: Write Operations & Production Hardening

### Monday-Tuesday Goals

**Write Tool Migration** (Dev 1):
```python
# HIGH RISK - data integrity critical

async def grass_mapcalc(
    expression: str,
    session_id: str = None
) -> dict:
    """Execute map algebra in session"""
    if not session_id:
        raise ValueError("session_id required for write operations")

    session = session_manager.get_session(session_id)
    await session.execute(["r.mapcalc", f"expression={expression}"])
    return {"status": "success"}

# Similarly for grass_buffer, grass_slope_aspect
```

**Write Operation Testing** (Dev 2):
```python
@pytest.mark.asyncio
async def test_write_isolation():
    """Maps created in session A not visible in session B"""
    session_a = session_manager.create_session(gisdbase, location)
    session_b = session_manager.create_session(gisdbase, location)

    # Create map in session A
    await grass_mapcalc("test_map = 1", session_id=session_a)

    # Verify visible in A
    maps_a = await grass_list_maps(session_id=session_a)
    assert "test_map" in maps_a

    # Verify NOT visible in B
    maps_b = await grass_list_maps(session_id=session_b)
    assert "test_map" not in maps_b

    # Close session A
    await close_session(session_a)

    # Verify map deleted
    # (mapset removed from disk)
```

**Deliverable**: All 8 tools migrated

### Wednesday Goals

**Session Timeout** (Dev 1):
```python
# Already implemented in SessionManager._cleanup_loop()
# TTL: 30 minutes of inactivity
```

**Startup Cleanup** (Dev 1):
```python
async def cleanup_orphaned_sessions(gisdbase: str):
    """Delete session_* mapsets older than 24h on startup"""
    pattern = f"{gisdbase}/*/session_*"
    for mapset_path in glob.glob(pattern):
        mtime = os.path.getmtime(mapset_path)
        if time.time() - mtime > 86400:  # 24 hours
            shutil.rmtree(mapset_path)
            logger.info(f"Cleaned up orphaned: {mapset_path}")

# Call on server startup
asyncio.create_task(cleanup_orphaned_sessions(gisdbase))
```

**Deliverable**: Production-ready session lifecycle

### Thursday Goals

**Load Testing** (All team):
```python
@pytest.mark.asyncio
async def test_50_concurrent_sessions():
    """Production load test"""
    sessions = []

    # Create 50 sessions
    for i in range(50):
        sid = session_manager.create_session(gisdbase, location)
        sessions.append(sid)

    # Each session performs unique operation
    tasks = [
        grass_mapcalc(f"map_{i} = {i}", session_id=sessions[i])
        for i in range(50)
    ]

    # Execute concurrently
    start = time.time()
    await asyncio.gather(*tasks)
    duration = time.time() - start

    # Performance assertions
    assert duration < 10  # Should complete in <10s

    # Verify isolation
    for i, sid in enumerate(sessions):
        maps = await grass_list_maps(session_id=sid)
        assert f"map_{i}" in maps
        # Each session sees only its own map
        assert len([m for m in maps if m.startswith("map_")]) == 1
```

**7-Day Endurance Test** (Start overnight):
- Monitor: memory, disk space, CPU
- Alert thresholds: >10GB disk, >100 session mapsets

**Deliverable**: Performance benchmarks

### Friday - Phase 1 Complete Checkpoint

**Success Criteria**:
- [ ] ALL 8 tools migrated and tested
- [ ] Session isolation verified (no leaks, no cross-talk)
- [ ] 50+ concurrent sessions working
- [ ] 7-day test running (no crashes)
- [ ] Structured JSON output for all tools
- [ ] Docker deployment ready

**Decision**:
- **COMPLETE**: All criteria met → Move to Phase 2
- **EXTEND**: Missing criteria → Add 1-2 weeks

---

## Risk Mitigation

### Risk 1: GRASS Environment Complexity
**Probability**: HIGH | **Impact**: HIGH

**Docker Setup** (Day 1):
```dockerfile
FROM mundialis/grass-py3-pdal:stable-ubuntu

# Set explicit GISBASE and binary path
ENV GISBASE=/usr/lib/grass83
ENV PATH=$PATH:/usr/lib/grass83/bin

# Install Python dependencies
RUN pip install mcp grass-script

# Copy server code
COPY grass_mcp_server.py /app/

WORKDIR /app
CMD ["python", "grass_mcp_server.py"]
```

**Validation**: All devs running in Docker by Day 3

### Risk 2: Resource Leaks
**Probability**: MEDIUM | **Impact**: HIGH

**Mitigations**:
- Session limit: 50 concurrent max
- Startup cleanup: Delete orphaned `session_*` mapsets
- 7-day endurance test monitoring

### Risk 3: AI Scope Creep
**Probability**: VERY HIGH | **Impact**: MEDIUM

**Mitigations**:
- Weekly stakeholder updates: "Foundation First"
- Demo external LLM using tools (Week 4)
- Roadmap lock: No Phase 3 until Phase 1 complete

---

## Deployment Checklist

### Infrastructure
- [ ] Docker image built and tested
- [ ] GRASS 8.x environment verified
- [ ] Python 3.10+ with asyncio
- [ ] Test data (DEM, vector samples)
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Logging infrastructure (JSON logs)
- [ ] Monitoring (Grafana/Prometheus)

### Code
- [ ] All 8 tools migrated to async
- [ ] GrassSession implemented
- [ ] SessionManager with TTL
- [ ] Session isolation verified (100%)
- [ ] JSON output for all tools
- [ ] Structured error handling
- [ ] Startup cleanup routine
- [ ] Session limit enforcement

### Testing
- [ ] Unit tests: 90%+ coverage
- [ ] Integration tests: Multi-step workflows
- [ ] Concurrency: 50+ sessions
- [ ] Load: 100 requests/second
- [ ] Endurance: 7 days no crashes
- [ ] Resource leaks: Zero orphaned mapsets
- [ ] Performance benchmarks

### Documentation
- [ ] API documentation (all tools)
- [ ] Session lifecycle guide
- [ ] Error handling guide
- [ ] Performance tuning guide
- [ ] Troubleshooting runbook
- [ ] Deployment guide (Docker)

---

## Immediate Next Steps (Monday Morning)

### 9:00 AM - Team Kickoff
- Review this execution plan (all 5 steps)
- Assign roles:
  - Dev 1: Async refactor lead
  - Dev 2: GRASS expert, testing
  - Dev 3: Docker, documentation
- Daily standup: 9 AM
- Confirm access: GRASS, GitHub, dev environment

### 10:00 AM - Environment Setup
- Clone repository
- Set up Docker development environment
- Verify GRASS installation and test data
- Create feature branch: `feature/phase1-async-sessions`

### 11:00 AM - Week 1 Day 1 Execution

**Dev 1** (Async Refactor):
1. Create `async_refactor` branch
2. Backup current `run_grass_command`
3. Start async refactor
4. Write unit tests
5. Target: Working async version by EOD

**Dev 2** (Testing):
1. Set up pytest-asyncio
2. Create test fixtures
3. Write first async test
4. Document testing approach
5. Target: Test framework ready by EOD

**Dev 3** (Docker):
1. Create Dockerfile
2. Create docker-compose.yml
3. Test GRASS in container
4. Document Docker setup
5. Target: All devs in Docker by Day 2

---

## Success Metrics

### Technical
- Zero blocking operations
- 50+ concurrent sessions supported
- Session isolation: 100% verified
- Resource leaks: Zero detected
- Performance: <2s response under load

### Quality
- Test coverage: 90%+
- Documentation: Complete for Phase 1
- Code reviews: All PRs approved
- CI/CD: Automated testing passing

### Team
- Knowledge transfer: All devs understand async + sessions
- No burnout: Sustainable pace maintained
- Clear communication: Weekly stakeholder updates

---

**EXECUTION PLAN COMPLETE - READY FOR MONDAY START**
