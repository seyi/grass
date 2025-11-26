# GRASS GIS MCP Server Expansion Strategy
## From 11 Tools to 100+ Tools

---

## Current Status

**Implemented:** 11 tools (8 base + 3 visualization)
**Available in GRASS:** 500+ core commands (509 by category breakdown)
**Total modules:** 2,474 (including add-ons and variations)

### Command Categories

| Prefix | Count | Category | Current Coverage |
|--------|-------|----------|------------------|
| `r.*` | 167 | Raster operations | 4 tools (2.4%) |
| `v.*` | 126 | Vector operations | 2 tools (1.6%) |
| `i.*` | 50 | Image processing | 0 tools (0%) |
| `t.*` | 51 | Temporal analysis | 0 tools (0%) |
| `d.*` | 43 | Display/rendering | 0 tools (0%) |
| `g.*` | 27 | General utilities | 2 tools (7.4%) |
| `r3.*` | 27 | 3D raster | 0 tools (0%) |
| `db.*` | 18 | Database | 0 tools (0%) |

---

## Expansion Approaches

### **Approach 1: High-Priority Tools (Recommended for Phase 2)**
Add 30-50 most commonly used tools with custom schemas

**Pros:**
- ✅ Best user experience (tailored schemas)
- ✅ Clear documentation
- ✅ Type-safe parameters
- ✅ Custom validation

**Cons:**
- ⚠️ Time-intensive (need to define each tool)
- ⚠️ Maintenance burden

**Use for:** Top 50 most common workflows

---

### **Approach 2: Generic Command Wrapper**
Create a single `grass_execute` tool that can run any GRASS command

**Pros:**
- ✅ Immediate access to all 500+ commands
- ✅ Minimal code to maintain
- ✅ Flexible for advanced users

**Cons:**
- ⚠️ No parameter validation
- ⚠️ Users need GRASS knowledge
- ⚠️ Less beginner-friendly

**Use for:** Advanced/uncommon commands

---

### **Approach 3: Hybrid (RECOMMENDED)**
Combine both approaches:
- 50-100 high-priority tools with custom schemas
- 1 generic wrapper for everything else

**Pros:**
- ✅ Best of both worlds
- ✅ Covers 80% use cases perfectly
- ✅ Flexible for edge cases
- ✅ Scalable architecture

**Example:**
```
# Common operations - custom tools
grass_raster_reclass()  # Tailored schema
grass_watershed()       # Tailored schema
grass_viewshed()        # Tailored schema

# Advanced/rare operations - generic wrapper
grass_execute("r.sim.water", params={...})
grass_execute("i.atcorr", params={...})
```

---

## Recommended Phase 2 Expansion: Top 50 Tools

### Priority 1: Essential Raster Operations (15 tools)

**Analysis:**
- `r.watershed` - Watershed and stream extraction
- `r.viewshed` - Viewshed analysis
- `r.cost` - Cost surface analysis
- `r.drain` - Flow path calculation
- `r.neighbors` - Neighborhood analysis
- `r.resample` - Resample to different resolution
- `r.patch` - Patch multiple rasters together

**Classification & Statistics:**
- `r.reclass` - Reclassify raster values
- `r.recode` - Recode raster categories
- `r.quantile` - Calculate quantiles
- `r.category` - Manage category labels
- `r.describe` - Describe raster categories

**Processing:**
- `r.fill.stats` - Fill nulls with statistics
- `r.grow` - Grow/shrink areas
- `r.null` - Null data management

### Priority 2: Essential Vector Operations (12 tools)

**Analysis:**
- `v.overlay` - Overlay vector layers (intersect, union, etc.)
- `v.select` - Select features by location
- `v.distance` - Calculate distances between features
- `v.voronoi` - Voronoi diagrams
- `v.net.*` - Network analysis (shortest path, allocation, etc.)
- `v.hull` - Convex hull

**Processing:**
- `v.generalize` - Line generalization
- `v.clean` - Topology cleaning
- `v.dissolve` - Dissolve features
- `v.extract` - Extract features by attributes
- `v.clip` - Clip vector by area
- `v.patch` - Merge vector maps

### Priority 3: Image Processing (8 tools)

**Classification:**
- `i.cluster` - Unsupervised classification
- `i.maxlik` - Maximum likelihood classification
- `i.smap` - Sequential maximum a posteriori

**Enhancement:**
- `i.colors.enhance` - Color enhancement
- `i.pca` - Principal component analysis
- `i.fft` - Fast Fourier Transform

**Correction:**
- `i.atcorr` - Atmospheric correction
- `i.topo.corr` - Topographic correction

### Priority 4: Import/Export (8 tools)

**Import:**
- `r.import` - Import raster with reprojection
- `v.import` - Import vector with reprojection
- `r.in.gdal` - Import raster via GDAL
- `v.in.ogr` - Import vector via OGR

**Export:**
- `r.out.gdal` - Export raster (already have for viz)
- `v.out.ogr` - Export vector
- `r.out.xyz` - Export to XYZ format
- `v.out.ascii` - Export to ASCII

### Priority 5: General Utilities (7 tools)

- `g.copy` - Copy maps
- `g.rename` - Rename maps
- `g.remove` - Remove maps (already have basic)
- `g.proj` - Projection information
- `g.findfile` - Find files in GRASS database
- `g.mapsets` - Mapset management
- `g.extension` - Extension management

---

## Implementation Strategy

### Phase 2A: Add 15 High-Priority Tools (Week 2-3)
Focus on most requested operations:
1. `r.watershed` - Critical for hydrology
2. `r.viewshed` - Common in visibility analysis
3. `r.reclass` - Essential for categorization
4. `v.overlay` - Core vector analysis
5. `v.select` - Spatial queries
6. `r.import` / `v.import` - Data import
7. `r.neighbors` - Common analysis
8. `v.distance` - Spatial relationships
9. `r.cost` - Path analysis
10. `v.dissolve` - Vector processing
11. `i.cluster` - Image classification
12. `r.patch` - Raster mosaicking
13. `v.clip` - Vector clipping
14. `r.null` - Data cleanup
15. `g.copy` - Data management

### Phase 2B: Add Generic Wrapper (Week 3)
Create `grass_execute()` tool for all other commands

### Phase 2C: Add 20 More Common Tools (Week 4-5)
Based on usage patterns and user feedback

### Phase 2D: Add 15 Advanced Tools (Week 6)
Specialized operations for power users

---

## Generic Wrapper Implementation

```python
Tool(
    name="grass_execute",
    description=(
        "Execute any GRASS GIS command directly. Use this for advanced "
        "operations not covered by specialized tools. Requires knowledge "
        "of GRASS command syntax."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "GRASS command name (e.g., 'r.watershed', 'v.overlay')",
            },
            "parameters": {
                "type": "object",
                "description": "Command parameters as key-value pairs",
                "additionalProperties": True,
            },
            "flags": {
                "type": "string",
                "description": "Command flags (e.g., 'a' for -a flag)",
                "default": "",
            },
            "gisdbase": {"type": "string"},
            "location": {"type": "string"},
            "mapset": {"type": "string", "default": "PERMANENT"},
        },
        "required": ["command", "parameters", "gisdbase", "location"],
    },
)
```

**Usage:**
```
User: "Create a watershed analysis of the elevation map"

Claude calls grass_execute with:
{
  "command": "r.watershed",
  "parameters": {
    "elevation": "dem",
    "accumulation": "flow_accum",
    "drainage": "flow_dir",
    "basin": "watersheds"
  },
  "flags": "a",
  "gisdbase": "/home/user/grassdata",
  "location": "nc_spm_08_grass7"
}
```

---

## Tool Priority Matrix

### By Use Case Frequency

| Priority | Tools | Justification |
|----------|-------|---------------|
| Critical (Top 10) | watershed, viewshed, reclass, overlay, select, import, neighbors, cost, clip, dissolve | Used in 80% of workflows |
| High (11-30) | distance, voronoi, patch, clean, recode, grow, net, quantile, pca, cluster | Common in specific domains |
| Medium (31-50) | hull, generalize, fill.stats, category, topo.corr, maxlik, extract, drain | Specialized but frequent |
| Low (51+) | Advanced operations | Use generic wrapper |

### By Domain

**Environmental Analysis:**
- r.watershed, r.cost, r.drain, r.viewshed, r.neighbors

**Urban Planning:**
- v.overlay, v.select, v.buffer, v.distance, v.net.*

**Remote Sensing:**
- i.cluster, i.pca, i.atcorr, i.maxlik, i.topo.corr

**Data Management:**
- r.import, v.import, g.copy, g.rename, r.patch

---

## Development Approach

### Step 1: Create Tool Generator Script

```python
def generate_grass_tool(command_name, description, params):
    """Generate MCP tool definition from GRASS command metadata"""
    # Auto-generate from g.parser output
    pass
```

### Step 2: Use GRASS Metadata

GRASS commands have built-in help:
```bash
r.watershed --help
r.watershed --interface-description  # XML output
```

We can parse this to auto-generate tool schemas!

### Step 3: Template-Based Generation

Create templates for common patterns:
- Raster input/output tools
- Vector input/output tools
- Analysis tools (multi-parameter)
- Import/export tools

---

## Expected Impact

### After Phase 2A (15 tools → 26 total)
- **Coverage:** 5% of GRASS commands
- **Workflow coverage:** ~40% of common GIS tasks
- **User satisfaction:** Moderate improvement

### After Phase 2B (+ generic wrapper → 27 total)
- **Coverage:** 100% of GRASS commands (via wrapper)
- **Workflow coverage:** ~60% common + 100% advanced
- **User satisfaction:** High improvement

### After Phase 2C (+ 20 tools → 47 total)
- **Coverage:** 9% direct + 100% wrapper
- **Workflow coverage:** ~70% of common tasks with optimal UX
- **User satisfaction:** Very high

### After Phase 2D (+ 15 tools → 62 total)
- **Coverage:** 12% direct + 100% wrapper
- **Workflow coverage:** ~85% common + 100% advanced
- **User satisfaction:** Excellent

---

## Recommended Timeline

**Week 1 (Current):** ✅ Phase 1 complete - Visualization integration

**Week 2-3:** Phase 2A - Add 15 high-priority tools
- Day 1-2: Create tool generator from GRASS metadata
- Day 3-5: Implement raster tools (watershed, viewshed, reclass, etc.)
- Day 6-8: Implement vector tools (overlay, select, distance, etc.)
- Day 9-10: Implement import/export tools
- Day 11-12: Testing and documentation

**Week 3:** Phase 2B - Generic wrapper
- Day 1-2: Implement grass_execute tool
- Day 3-4: Test with various commands
- Day 5: Documentation and examples

**Week 4-5:** Phase 2C - Add 20 more tools based on feedback

**Week 6:** Phase 2D - Add 15 advanced tools

---

## Testing Strategy

**For each new tool:**
1. Unit test with valid parameters
2. Error handling test with invalid parameters
3. Real-world workflow test with NC sample data
4. Documentation example

**Integration tests:**
1. Multi-tool workflows (e.g., watershed → reclass → visualization)
2. Performance benchmarks
3. Error recovery scenarios

---

## Documentation Updates

**For each tool add:**
- Tool description in README
- Usage example
- Common workflows
- Parameter explanations
- Error messages guide

**New documents:**
- TOOL_REFERENCE.md - Complete tool catalog
- WORKFLOWS.md - Common multi-step workflows
- MIGRATION_GUIDE.md - For users of GRASS CLI

---

## Success Metrics

**Quantitative:**
- ✅ Number of tools: 11 → 50+
- ✅ Workflow coverage: ~15% → 70%+
- ✅ Commands accessible: 11 → 500+

**Qualitative:**
- ✅ User can complete common GIS tasks without CLI
- ✅ Reduced learning curve for GRASS GIS
- ✅ Positive user feedback on tool discovery

---

## Next Steps

1. **Approve expansion strategy** (this document)
2. **Prioritize which 15 tools for Phase 2A**
3. **Create tool generator script**
4. **Implement Phase 2A tools**
5. **Test and document**
6. **Release Phase 2**

---

## Alternative: Auto-Generated Tool Set

**Option:** Generate ALL 500+ tools programmatically

**How:**
```python
# Parse GRASS metadata
grass_commands = get_all_grass_commands()

for cmd in grass_commands:
    metadata = parse_grass_interface(cmd)
    tool = generate_mcp_tool(metadata)
    register_tool(tool)
```

**Pros:**
- ✅ Complete coverage immediately
- ✅ Automatically stays in sync with GRASS updates

**Cons:**
- ⚠️ Generic schemas (less user-friendly)
- ⚠️ No customization per tool
- ⚠️ Harder to maintain quality

**Verdict:** Use for Phase 2B onwards, but keep custom tools for top 50

---

## Conclusion

**Recommended approach:** Hybrid strategy
- **Phase 2A:** Add 15 high-priority custom tools
- **Phase 2B:** Add generic wrapper for all others
- **Phase 2C-D:** Continue adding custom tools based on usage

This gives:
- ✅ Immediate access to all 500+ commands (via wrapper)
- ✅ Excellent UX for common operations (custom tools)
- ✅ Scalable and maintainable architecture
- ✅ Flexible for future expansion

**Ready to proceed?** Let me know which phase to start implementing!
