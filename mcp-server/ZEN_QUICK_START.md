# Zen MCP Quick Start Guide
## Using AI Model Orchestration for GIS Analysis

**Prerequisites**: Zen MCP must be connected (restart Claude Code if needed)

---

## Quick Verification

**Check if Zen is available**:
```
List available models using zen
```

If this works, you're ready to go!

---

## Essential Commands

### 1. Chat with Specific Models

**Basic usage**:
```
Use zen chat with gemini-2.5-pro to analyze the GRASS MCP server architecture
```

**With specific thinking mode**:
```
Use zen chat with gemini-2.5-pro in max thinking mode to explore
optimization opportunities for the session persistence implementation
```

**Continue conversation**:
```
Continue the zen chat to discuss implementation challenges
```

### 2. Deep Thinking

**Extended reasoning**:
```
Use zen thinkdeep with gemini-2.5-pro to analyze edge cases in
the grass_buffer operation for geographic coordinates
```

**Thinking modes**:
- `low` - Quick, less thorough
- `medium` - Balanced (default)
- `high` - Thorough analysis
- `max` - Maximum depth

### 3. Multi-Model Consensus

**Get opinions from multiple AIs**:
```
Use zen consensus with gemini-2.5-pro, gpt-5-pro, and o3 to decide:
Should we prioritize interactive visualization or temporal data support?
```

**Structured debate**:
```
Use zen consensus with stance="for,against,neutral" using gemini-2.5-pro,
gpt-5-pro, and o3 on whether to create a separate QGIS MCP server
```

### 4. Project Planning

**Create implementation plans**:
```
Use zen planner with gemini-2.5-pro to create a detailed implementation
plan for adding interactive web map visualization to the GRASS MCP server
```

**Break down complex tasks**:
```
Use zen planner to break down the "Natural Language Geospatial Queries"
feature into a 4-week development plan
```

### 5. Code Review

**Review code changes**:
```
Use zen codereview with gemini-2.5-pro to review the grass_mcp_server.py
implementation focusing on error handling and edge cases
```

**Pre-commit validation**:
```
Use zen precommit with gemini-2.5-pro to validate changes before
committing the new visualization tools
```

### 6. Debugging

**Systematic problem analysis**:
```
Use zen debug with gemini-2.5-pro to investigate why the buffer
operation fails with lat/lon coordinates
```

### 7. API Lookup

**Get current documentation**:
```
Use zen apilookup for "Python Folium ImageOverlay 2025"
```

**Avoid outdated responses**:
```
Use zen apilookup to find the latest GRASS Python API documentation
for the temporal framework
```

---

## GIS-Specific Use Cases

### Analyzing Design Decisions

```
Use zen consensus with gemini-2.5-pro and gpt-5-pro to evaluate:

Option A: Integrate visualization into existing GRASS MCP server
Option B: Create separate visualization MCP server
Option C: Hybrid approach with multiple rendering backends

Consider factors:
- Maintenance complexity
- User experience
- Performance
- Extensibility
```

### Planning Feature Implementation

```
Use zen planner with gemini-2.5-pro to create an 8-week implementation
plan for adding the complete vector analysis toolkit (15+ operations)
to the GRASS MCP server. Include:
- Week-by-week milestones
- Testing strategy
- Documentation requirements
- Risk mitigation
```

### Deep Technical Analysis

```
Use zen thinkdeep with max thinking mode to analyze:

How should we implement persistent GRASS sessions in the MCP server?
Consider:
- Thread safety
- Resource management
- Session lifecycle
- Error recovery
- Multi-user scenarios
```

### Strategic Decision Making

```
Use zen consensus with gemini-2.5-pro, gpt-5-pro, and o3 to prioritize
these opportunities:

1. Interactive web map visualization
2. Temporal data support
3. Natural language query interface
4. Cloud data integration
5. Hydrological analysis tools

Evaluate based on:
- User value
- Implementation effort
- Strategic positioning
- Technical risk
```

### Exploring Implementation Options

```
Use zen chat with gemini-2.5-pro to explore different approaches
for implementing natural language geospatial queries:

1. Prompt engineering approach
2. Fine-tuned model for GIS
3. Retrieval-augmented generation
4. Tool chain orchestration

Discuss pros, cons, and feasibility of each
```

### Code Quality Assurance

```
Use zen codereview with gemini-2.5-pro to review the new
create_interactive_map_with_elevation.py script focusing on:
- Error handling
- Resource cleanup
- Edge cases (empty data, coordinate system issues)
- Performance with large datasets
- Code organization and readability
```

### Documentation Review

```
Use zen chat with gemini-2.5-pro to review GIS_OPPORTUNITIES_ANALYSIS.md
and suggest:
- Missing opportunity areas
- Additional use cases
- Market insights
- Implementation considerations
```

---

## Advanced Workflows

### Multi-Stage Analysis

**Stage 1: Explore**
```
Use zen thinkdeep with gemini-2.5-pro to explore challenges in
implementing time series analysis for satellite imagery
```

**Stage 2: Plan**
```
Continue with zen planner to create a detailed implementation roadmap
based on the challenges identified
```

**Stage 3: Validate**
```
Use zen consensus with gpt-5-pro and o3 to validate the proposed
approach and identify potential improvements
```

### Collaborative Problem Solving

**Problem**: How to handle large raster datasets (>10GB) efficiently?

**Step 1**: Get multiple perspectives
```
Use zen consensus with gemini-2.5-pro, gpt-5-pro, and o3 on strategies
for handling large raster datasets in the GRASS MCP server
```

**Step 2**: Deep dive on best approach
```
Use zen thinkdeep with max thinking to analyze the recommended
approach (streaming, tiling, or lazy loading) in detail
```

**Step 3**: Implementation plan
```
Use zen planner to create a detailed implementation plan for the
chosen strategy including testing and validation
```

### Quality Assurance Pipeline

**Before committing**:
```
1. Use zen codereview to identify issues
2. Fix identified issues
3. Use zen precommit to validate fixes
4. Use zen chat to generate commit message
5. Commit with confidence
```

---

## Model Selection Guide

### When to use Gemini 2.5 Pro
- ✅ Complex reasoning tasks
- ✅ Long document analysis
- ✅ Strategic planning
- ✅ Multi-step workflows
- ✅ Code architecture discussions

### When to use GPT-5 Pro
- ✅ Code generation
- ✅ Detailed implementation
- ✅ API integration
- ✅ Testing strategies
- ✅ Documentation writing

### When to use O3
- ✅ Advanced reasoning
- ✅ Edge case analysis
- ✅ Algorithm optimization
- ✅ Security analysis
- ✅ Mathematical problems

### When to use Consensus
- ✅ Important decisions
- ✅ Multiple valid approaches
- ✅ Controversial tradeoffs
- ✅ Innovative solutions
- ✅ Strategic direction

---

## Tips and Best Practices

### 1. Be Specific
❌ "Analyze this project"
✅ "Use zen chat with gemini-2.5-pro to analyze the current GRASS MCP
   server architecture and identify scalability bottlenecks"

### 2. Provide Context
```
Use zen thinkdeep with gemini-2.5-pro to analyze session persistence
implementation. Context: GRASS sessions are expensive to create (~2s),
we need to support multiple concurrent users, and sessions must be
isolated from each other.
```

### 3. Specify Thinking Mode
- Quick questions: `low` or `medium`
- Important decisions: `high`
- Critical analysis: `max`

### 4. Use Continuation
```
# First interaction
Use zen chat with gemini-2.5-pro to explore visualization options

# Continue the conversation
Continue zen chat to discuss performance implications

# Ask follow-up
In the same zen chat, how would caching affect this?
```

### 5. Leverage Multiple Models
For important decisions, always get multiple perspectives:
```
Use zen consensus with gemini-2.5-pro, gpt-5-pro, and o3
```

### 6. Save Important Analyses
```
Use zen thinkdeep with gemini-2.5-pro to analyze X, then save
the analysis to docs/ANALYSIS_X.md
```

---

## Troubleshooting

### "Zen tools not found"
**Solution**: Restart Claude Code session. MCP servers connect at startup.

### "Model not available"
**Check available models**:
```
Use zen listmodels
```

### "API key error"
**Verify keys in mcp.json**:
```json
"env": {
    "GEMINI_API_KEY": "AIzaSy...",
    "OPENAI_API_KEY": "sk-proj-..."
}
```

### "Timeout error"
- Reduce thinking mode (max → high → medium)
- Break down into smaller questions
- Use chat instead of thinkdeep for quick questions

### "Context too large"
- Use apilookup for documentation instead of including full docs
- Break analysis into multiple smaller sessions
- Use clink to spawn subagents for isolated investigations

---

## Example Session

**Goal**: Decide how to implement interactive map visualization

```
User: Use zen consensus with gemini-2.5-pro and gpt-5-pro to evaluate
      approaches for adding interactive map visualization to GRASS MCP:

      A) grass.jupyter for static images
      B) Folium for interactive HTML maps
      C) QGIS bridge for professional cartography
      D) Hybrid approach with multiple backends

      Evaluate based on implementation effort, user value, and maintenance.

[Zen provides multi-model analysis]

User: Continue with zen planner using gemini-2.5-pro to create a
      detailed implementation plan for the recommended approach

[Zen creates structured plan]

User: Use zen thinkdeep with high thinking mode to identify potential
      edge cases and technical challenges in the implementation

[Zen analyzes edge cases]

User: Great! Let's implement the quick win first. Use zen chat with
      gemini-2.5-pro to help me write the grass.jupyter integration.

[Zen assists with implementation]

User: Use zen codereview to check the implementation before committing

[Zen reviews code]

User: Use zen precommit to validate everything is ready

[Zen validates]

User: Perfect! Let's commit.
```

---

## Quick Reference

| Task | Command Pattern |
|------|----------------|
| Quick question | `zen chat with <model>` |
| Deep analysis | `zen thinkdeep with <model>` |
| Multiple opinions | `zen consensus with <model1>, <model2>` |
| Planning | `zen planner with <model>` |
| Code review | `zen codereview with <model>` |
| Pre-commit check | `zen precommit with <model>` |
| Debugging | `zen debug with <model>` |
| Current docs | `zen apilookup for "<query>"` |
| List models | `zen listmodels` |

---

## Getting Help

**Zen Documentation**: Check `/root/aiyifyproject/repos/zen-mcp-server/docs/`

**Available Tools**:
```
Use zen version to see tool list
```

**Model Capabilities**:
```
Use zen listmodels to see all available models and their capabilities
```

---

**Remember**: Zen is most powerful when you:
1. Ask specific, well-scoped questions
2. Use appropriate thinking modes
3. Leverage multiple models for important decisions
4. Provide context and constraints
5. Build on previous conversations with continuation

Happy orchestrating! 🎼
