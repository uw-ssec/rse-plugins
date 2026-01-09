# HoloViz Expert - Claude Code Plugin

**Expert-level guidance for interactive data visualization and dashboards with HoloViz**

The definitive Claude Code plugin for mastering the HoloViz ecosystem. Get strategic guidance, production-ready code patterns, and deep expertise in Panel, HoloViews, hvPlot, GeoViews, Datashader, Lumen, Param, and Colorcet.

**Version**: 0.1.0 | **Status**: Production Ready | **License**: BSD-3-Clause

---

## Overview

This production-ready, expert-quality Claude Code plugin provides comprehensive coverage of the entire HoloViz ecosystem through specialized AI agents, detailed skills, and curated resources. Whether you're building interactive dashboards, visualizing massive datasets, creating geographic applications, or exploring data with AI, this plugin offers strategic guidance and production-ready patterns.

### What Makes This Plugin Different

- **Token-Optimized Architecture**: Lean agents focused on orchestration, comprehensive skills for technical depth
- **Strategic Guidance**: Not just documentation, but expert decision-making support
- **Production-Ready**: Real-world code patterns you can use immediately
- **Comprehensive**: All 8 HoloViz libraries covered in depth
- **Workflow-Based**: Organized around how you actually work, not just library APIs
- **Accessibility-First**: Colorblind-friendly designs and multiple visual encodings
- **Performance-Aware**: Optimization guidance integrated throughout
- **Multi-Plugin Ready**: Self-contained structure supporting future plugin expansion

---

## Features

### 4 Specialized Agents

Each agent provides complementary expertise for different workflows with a lean, token-efficient design:

**Architecture Philosophy**: Agents orchestrate skills and provide workflow guidance, while skills contain authoritative technical documentation. This eliminates duplication and improves token efficiency.

1. **Panel Specialist** (117 lines) - Interactive Dashboard Expert
   - Component-based application development
   - Reactive programming patterns
   - Template systems and theming
   - Real-time data streaming
   - Focus: "Build interactive dashboards"

2. **Visualization Designer** (135 lines) - Strategic Visualization Guide
   - Multi-library visualization strategy
   - Ecosystem navigation and tool selection
   - Visualization design principles
   - Accessibility and performance
   - Focus: "What's the best way to visualize this?"

3. **Data Engineer** (156 lines) - Performance Optimization Expert
   - Large-scale data handling (100M+ points)
   - Datashader and aggregation strategies
   - Memory optimization
   - Chunked processing for massive datasets
   - Focus: "Optimize rendering for large data"

4. **Geo-Spatial Expert** (176 lines) - Geographic Visualization Specialist
   - Maps and geographic data with GeoViews
   - Coordinate reference systems (CRS)
   - Spatial analysis and joins
   - Multi-layer map composition
   - Focus: "Create interactive maps"

### 9 Comprehensive Skills

Over 4,000 lines of expert content with production-ready code examples:

| Skill | Lines | Focus |
|-------|-------|-------|
| **Lumen Dashboards** | 720 | No-code dashboards with YAML specifications |
| **Lumen AI** | 555 | AI-powered natural language data exploration |
| **Colormaps & Styling** | 469 | Color management and visual design |
| **Parameterization** | 439 | Declarative parameter systems |
| **Advanced Rendering** | 415 | Datashader for massive datasets |
| **Data Visualization** | 385 | Advanced HoloViews composition |
| **Geospatial Visualization** | 374 | Maps and geographic data |
| **Plotting Fundamentals** | 355 | Quick visualization with hvPlot |
| **Panel Dashboards** | 343 | Interactive apps with Panel and Param |

### Rich Resource Library

Comprehensive reference guides organized by topic (11,200+ lines):

**Core References:**
- **HoloViz Ecosystem Overview** (326 lines): Understanding all the libraries and how they work together
- **Library Selection Matrix** (276 lines): Choosing the right tools for your use case
- **Best Practices** (400 lines): Proven patterns and techniques
- **Code Patterns** (335 lines): Production-ready snippets and design patterns
- **Troubleshooting** (453 lines): Solutions to common issues

**Specialized References:**
- **Colormaps** (2,352 lines): Accessibility, colormap reference, HoloViews styling, Panel themes
- **Lumen Dashboards** (5,267 lines): Sources, transforms, views, layouts, Python API, deployment, examples, troubleshooting
- **Lumen AI** (2,115 lines): Agent reference, custom agents, LLM providers, deployment

---

## Content Metrics

| Metric | Count |
|--------|-------|
| **Total Lines of Content** | 16,600+ |
| **Agents** | 4 (584 lines) |
| **Skills** | 9 (4,055 lines) |
| **Reference Materials** | 21 files (11,224 lines) |
| **HoloViz Libraries Covered** | 8 (all) |
| **Total Markdown Files** | 35 |

---

## Quick Start

### For Exploratory Visualization
Ask the **Visualization Designer**:
> "What's the best way to visualize this dataset?"

### For Building Dashboards
Ask the **Panel Specialist**:
> "Build an interactive dashboard for monitoring real-time metrics"

### For Large Datasets
Ask the **Data Engineer**:
> "How do I visualize 100 million data points efficiently?"

### For Geographic Data
Ask the **Geo-Spatial Expert**:
> "Create an interactive map of my geospatial data"

---

## Use Cases

### Interactive Dashboards
- Real-time monitoring applications
- Business intelligence dashboards
- Data exploration tools
- Scientific analysis interfaces

### Data Visualization
- Publication-quality figures
- Multi-dimensional data exploration
- Comparative analysis visualizations
- Report generation

### Large-Scale Data
- 100M+ point cloud visualization
- Geospatial analysis of massive datasets
- Time-series data exploration
- High-frequency trading analytics

### Geographic Applications
- Maps and spatial analysis
- Weather data visualization
- Real estate and market analysis
- Infrastructure planning tools

### AI-Powered Analytics
- Natural language data queries
- Conversational data exploration
- Automated visualization generation
- Self-service analytics

---

## Library Guide

### Param
Declarative, type-safe parameter system with automatic validation
```python
class Config(param.Parameterized):
    count = param.Integer(default=10, bounds=(1, 100))
    name = param.String(default='Data')
```

### HoloViews
Declarative data visualization with advanced composition
```python
scatter = hv.Scatter(data, 'x', 'y')
curve = hv.Curve(data, 'x', 'y')
overlay = scatter * curve
```

### hvPlot
Pandas-like plotting interface for quick visualization
```python
df.hvplot.scatter(x='x', y='y', by='category')
```

### GeoViews
Geographic data visualization with tile providers
```python
gv.Polygons(geodataframe).opts(cmap='viridis')
```

### Datashader
Efficient rendering of 100M+ point datasets
```python
from holoviews.operation.datashader import datashade
datashade(scatter, cmap='viridis')
```

### Panel
Interactive web applications in pure Python
```python
pn.Column(
    pn.pane.Markdown('# Dashboard'),
    plot,
    controls
).servable()
```

### Colorcet
Perceptually uniform colormaps for scientific visualization
```python
from colorcet import cm
plot.opts(cmap=cm['cet_fire'])
```

### Lumen
No-code dashboards with YAML specs or AI-powered data exploration
```python
# Lumen Dashboards: YAML configuration
lumen serve dashboard.yaml

# Lumen AI: Natural language queries
lumen-ai serve data.csv
# Ask: "Show me total sales by region"
```

---

## Expert Guidance Examples

### Example 1: Performance Optimization
**User**: "My dashboard with 10M points is too slow"

**Data Engineer recommends**:
1. Use Datashader for rasterization
2. Aggregate data by region
3. Implement progressive disclosure with zooming
4. Profile with memory_profiler to find bottlenecks
5. Caching strategy with reduced update frequency

### Example 2: Visualization Selection
**User**: "50M GPS points, value gradient, need to find patterns"

**Visualization Designer suggests**:
1. Datashader for density heatmap
2. Perceptually uniform colormap (Colorcet)
3. Multi-resolution exploration (zoom-based)
4. Panel application for interactive exploration
5. Alternative: Hexbin aggregation

### Example 3: Application Architecture
**User**: "Build a multi-page app for data analysis"

**Panel Specialist designs**:
1. Param class for application state
2. Panel tabs for different views
3. Reactive dependencies for auto-updates
4. Template for consistent styling
5. File upload for data ingestion

### Example 4: Geographic Application
**User**: "Create a map showing store locations colored by revenue"

**Geo-Spatial Expert implements**:
1. GeoDataFrame from lat/lon coordinates
2. GeoViews Points layer with color encoding
3. Tile provider background (OpenStreetMap)
4. Interactive hover with store details
5. Panel integration for controls

---

## Installation

This plugin requires HoloViz libraries:

```bash
pip install panel holoviews hvplot geoviews datashader lumen param colorcet
```

Optional: For Lumen AI features
```bash
pip install lumen[ai]
# Plus LLM provider (choose one):
pip install openai        # OpenAI
pip install anthropic     # Anthropic Claude
```

Optional: For MCP server integration
```bash
pip install holoviz-mcp
```

---

## Architecture

**Self-Contained Plugin Structure** - Designed for the rse-agents marketplace:

```
plugins/holoviz-expert/                       # Self-contained plugin
├── .claude-plugin/
│   └── plugin.json                          # Plugin metadata and configuration
├── agents/                                   # 4 specialized agents (584 lines)
│   ├── panel-specialist.md                  # 117 lines
│   ├── visualization-designer.md            # 135 lines
│   ├── data-engineer.md                     # 156 lines
│   └── geo-spatial-expert.md                # 176 lines
├── skills/                                   # 9 comprehensive skills (4,055 lines)
│   ├── advanced-rendering/SKILL.md          # 415 lines
│   ├── colormaps-styling/SKILL.md           # 469 lines
│   ├── data-visualization/SKILL.md          # 385 lines
│   ├── geospatial-visualization/SKILL.md    # 374 lines
│   ├── lumen-ai/SKILL.md                    # 555 lines
│   ├── lumen-dashboards/SKILL.md            # 720 lines
│   ├── panel-dashboards/SKILL.md            # 343 lines
│   ├── parameterization/SKILL.md            # 439 lines
│   └── plotting-fundamentals/SKILL.md       # 355 lines
├── references/                               # Reference materials (11,224 lines)
│   ├── best-practices/
│   │   └── README.md                        # 400 lines
│   ├── colormaps/
│   │   ├── accessibility.md                 # 561 lines
│   │   ├── colormap-reference.md            # 388 lines
│   │   ├── holoviews-styling.md             # 700 lines
│   │   └── panel-themes.md                  # 703 lines
│   ├── lumen-ai/
│   │   ├── agents-reference.md              # 550 lines
│   │   ├── custom-agents.md                 # 649 lines
│   │   ├── deployment.md                    # 594 lines
│   │   └── llm-providers.md                 # 322 lines
│   ├── lumen-dashboards/
│   │   ├── deployment.md                    # 398 lines
│   │   ├── examples.md                      # 682 lines
│   │   ├── layouts.md                       # 415 lines
│   │   ├── python-api.md                    # 602 lines
│   │   ├── sources.md                       # 771 lines
│   │   ├── transforms.md                    # 696 lines
│   │   ├── troubleshooting.md               # 614 lines
│   │   └── views.md                         # 789 lines
│   ├── patterns/
│   │   └── README.md                        # 335 lines
│   ├── troubleshooting/
│   │   └── README.md                        # 453 lines
│   ├── holoviz-ecosystem.md                 # 326 lines
│   └── library-matrix.md                    # 276 lines
├── .mcp.json                                 # MCP server configuration
├── LICENSE                                   # BSD-3-Clause
└── README.md                                 # This file
```

### Design Principles

**Agent Optimization**: Agents are lean orchestrators (~146 lines avg) that focus on workflow coordination and delegate technical details to skills. This separation of concerns ensures efficiency and maintainability.

**Single Source of Truth**: Skills contain authoritative technical documentation. Agents reference skills but don't duplicate their content.

**Comprehensive References**: Detailed reference materials are organized by topic in the `references/` directory, providing deep technical documentation that complements the skills.

---

## Key Design Decisions

### Token-Optimized Architecture

**Philosophy**: Clear separation between orchestration and technical depth.

**Agent Structure**: Agents are lean orchestrators that include:
- Frontmatter metadata and skill references
- Domain context and expertise areas
- Workflow frameworks (e.g., Spatial Workflow, Performance Optimization)
- Communication style and agent personality
- Integration patterns with other agents
- Example interactions demonstrating orchestration

**Skills Structure**: Skills provide comprehensive technical documentation with:
- Detailed library usage and API references
- Production-ready code examples
- Best practices and patterns
- Performance considerations
- Integration guidance

**References Structure**: Deep-dive reference materials organized by topic:
- Library ecosystem overviews
- Specialized guides (colormaps, Lumen, etc.)
- Best practices and troubleshooting
- Design patterns and examples

### Workflow-Based Organization
Skills are organized by user workflows, not 1-to-1 library mapping. This reduces cognitive load and shows how libraries integrate in practice.

**Skills Map to Problems**:
- "I'm building a dashboard" → Panel Dashboards skill
- "I need to visualize data quickly" → Plotting Fundamentals skill
- "I need advanced visualizations" → Data Visualization skill
- "I'm working with maps" → Geospatial Visualization skill
- "I have massive data" → Advanced Rendering skill
- "I need AI-powered analytics" → Lumen AI skill

### Complementary Agents
Four specialized agents with distinct expertise areas that work together:
- Panel + Param integration → Panel Specialist
- HoloViews + hvPlot + Colorcet → Visualization Designer
- Datashader + optimization → Data Engineer
- GeoViews + spatial → Geo-Spatial Expert

### Expert-Level Positioning
Focus on strategic decision-making, not just documentation:
- Teaches "why" not just "how"
- Addresses real-world problems
- Provides ecosystem navigation
- Production-focused guidance

---

## Skill Deep Dives

### Panel Dashboards Skill (343 lines)
Complete guide to building interactive applications:
- Component-based architecture with Panel and Param
- Reactive programming patterns
- Template systems (Material, Bootstrap, Vanilla, Dark)
- Real-time data streaming
- File handling and validation
- Production-ready code examples

### Plotting Fundamentals Skill (355 lines)
Quick visualization with hvPlot and HoloViews basics:
- Common plot types (scatter, line, bar, histogram, etc.)
- Customization options
- Interactive features
- Geographic plotting
- Performance considerations
- Integration with pandas DataFrames

### Data Visualization Skill (385 lines)
Advanced HoloViews composition and interactivity:
- Element composition (overlays, layouts, facets)
- Interactive streams and selection
- Dynamic maps for responsive visualization
- Network and hierarchical data
- Statistical visualizations
- Multi-dimensional data exploration

### Geospatial Visualization Skill (374 lines)
Professional mapping with GeoViews:
- Basic geographic visualization
- Point, polygon, and line features
- Choropleth maps
- Spatial analysis workflows
- Multi-layer compositions
- Coordinate reference systems (CRS)
- Optimization for large geographic datasets

### Advanced Rendering Skill (415 lines)
Efficient handling of massive datasets with Datashader:
- Datashader fundamentals
- Aggregation strategies (count, mean, sum, max/min)
- Memory optimization techniques
- Transfer functions and color mapping
- Chunked processing for files larger than RAM
- Integration with Panel and HoloViews

### Parameterization Skill (439 lines)
Declarative parameter systems with Param:
- Parameter basics and type validation
- Advanced parameter types (Date, Path, Range, Color, Dict)
- Dynamic dependencies with @param.depends
- Watchers for side effects
- Custom validation patterns
- Hierarchical parameterization
- Automatic Panel UI generation

### Colormaps & Styling Skill (469 lines)
Professional color and visual design:
- Colorcet colormap selection
- Accessibility and colorblind-friendly design
- Custom color mapping and normalization
- HoloViews element styling
- Panel theme customization
- Dark mode support
- Multi-element styling consistency

### Lumen Dashboards Skill (720 lines)
Declarative, no-code dashboard development:
- YAML-based specifications for rapid development
- Data sources (files, databases, REST APIs)
- Transforms and filters for data processing
- Views (tables, plots, indicators)
- Pipelines combining sources → transforms → views
- Layout and responsive design patterns
- Complete dashboard examples
- Python API for programmatic creation

### Lumen AI Skill (555 lines)
AI-powered natural language data exploration:
- Natural language interface for querying data
- Multi-LLM support (OpenAI, Anthropic, Google, Mistral, local models)
- Agent architecture (SQL, hvPlot, VegaLite, Analysis, Chat agents)
- Custom agent development patterns
- Custom analyses for domain-specific tasks
- Document context and RAG integration
- Complete business analytics examples
- Security and privacy best practices

---

## Best Practices Highlights

### Performance
- Use hvPlot for < 100k points
- Use Datashader for 100M+ points
- Implement aggregation and sampling
- Cache expensive computations
- Profile with profilers before optimizing
- Use Parquet format for large datasets
- Leverage Dask for multi-core processing

### Accessibility
- Use perceptually uniform colormaps (Colorcet)
- Provide multiple visual encodings (color, size, shape)
- Test with colorblind vision simulators
- Include clear labels and legends
- Support keyboard navigation
- Design for screen readers where applicable

### Code Organization
- Separate UI concerns from business logic
- Use Param classes for configuration
- Create reusable component functions
- Organize related plots into modules
- Document with clear docstrings
- Follow Scientific Python development guides

### Responsive Design
- Always use `responsive=True` for plots
- Test on multiple screen sizes
- Use appropriate layout strategies
- Implement lazy loading for large content
- Monitor performance on slower devices

---

## Integration with MCP Server

The plugin includes MCP server configuration for real-time library access using Docker:

### Docker Setup (Recommended)

**Step 1: Pull and run the Docker container**

```bash
docker pull ghcr.io/marcskovmadsen/holoviz-mcp:latest

docker run -d \
  --name holoviz-mcp \
  -p 8000:8000 \
  -e HOLOVIZ_MCP_TRANSPORT=http \
  -v ~/.holoviz-mcp:/root/.holoviz-mcp \
  ghcr.io/marcskovmadsen/holoviz-mcp:latest
```

**Step 2: Configuration**

The `.mcp.json` file is pre-configured for Docker HTTP transport:

```json
{
  "servers": {
    "holoviz": {
      "type": "http",
      "url": "http://localhost:8000/mcp/"
    }
  }
}
```

### Alternative: Local Installation

For local installation without Docker:

```bash
uv tool install holoviz-mcp[panel-extensions]
uvx --from holoviz-mcp holoviz-mcp-update
```

Update `.mcp.json` to use stdio transport:

```json
{
  "servers": {
    "holoviz": {
      "type": "stdio",
      "command": "uvx",
      "args": ["holoviz-mcp"]
    }
  }
}
```

### Capabilities

The MCP server enables:
- Real-time library documentation
- Latest API reference access
- Example gallery integration
- Version information lookup

---

## Quality Assurance

### Validation Checklist
- ✅ Plugin structure follows rse-agents pattern
- ✅ All required metadata present
- ✅ Naming conventions correct (kebab-case)
- ✅ Documentation comprehensive
- ✅ Code examples production-ready
- ✅ Best practices integrated
- ✅ Accessibility considered
- ✅ Performance optimization guidance
- ✅ License appropriate (BSD-3-Clause)
- ✅ Compatible with Claude Code marketplace

### Expert-Level Indicators
- Deep knowledge of all 8 HoloViz libraries
- Real-world problem-solving focus
- Performance optimization throughout
- Accessibility standards integrated
- Strategic guidance beyond documentation
- Production-ready code patterns
- Clear ecosystem navigation

---

## Resources

### Official Documentation
- [HoloViz Homepage](https://holoviz.org)
- [Panel Documentation](https://panel.holoviz.org)
- [HoloViews Documentation](https://holoviews.org)
- [hvPlot Documentation](https://hvplot.holoviz.org)
- [GeoViews Documentation](https://geoviews.org)
- [Datashader Documentation](https://datashader.org)
- [Lumen Documentation](https://lumen.holoviz.org)
- [Param Documentation](https://param.holoviz.org)
- [Colorcet Documentation](https://colorcet.holoviz.org)

### Community
- [HoloViz Discourse](https://discourse.holoviz.org)
- [GitHub Discussions](https://github.com/holoviz/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/holoviz)

### Learning Resources
- [HoloViz Gallery](https://holoviz.org/gallery/index.html)
- [Panel Examples](https://panel.holoviz.org/gallery/index.html)
- [Datashader Examples](https://datashader.org/getting_started/index.html)
- [Tutorial Notebooks](https://holoviz.org/tutorial/index.html)

---

## Troubleshooting

### Common Issues

**Q: My plot won't display**
- Ensure you've imported the plotting library (hvplot.pandas, geoviews, etc.)
- Check that your data isn't empty
- Verify column names match exactly

**Q: Dashboard is running too slow**
- Profile to find the bottleneck
- Use Datashader for > 100k points
- Implement aggregation or sampling
- Enable caching for expensive computations

**Q: Visualization looks unclear**
- Use perceptually uniform colormaps (Colorcet)
- Add legends and labels
- Increase figure size
- Consider faceting for categorical data

**Q: Map isn't displaying**
- Verify coordinate reference system (CRS)
- Check geometry validity with `gdf.is_valid.all()`
- Ensure coordinates are in correct order (lon, lat for WGS84)

See the **Troubleshooting Guide** in resources for detailed solutions.

---

## Contributing

This plugin is part of the HoloViz ecosystem. To contribute:

1. Visit [HoloViz on GitHub](https://github.com/holoviz)
2. Check existing issues and discussions
3. Submit improvements and updates
4. Follow HoloViz community guidelines

---

## License

BSD 3-Clause License - See LICENSE file for details

---

## Citation

If you use this plugin in your research, please cite HoloViz:

```bibtex
@software{holoviz2024,
  author = {HoloViz Contributors},
  title = {HoloViz: Flexible Scientific Visualization in Python},
  url = {https://holoviz.org},
  year = {2024}
}
```

---

## Support

- **Questions**: Ask in [HoloViz Discourse](https://discourse.holoviz.org)
- **Issues**: Report on respective GitHub repositories
- **Plugin Issues**: Report in plugin repository
- **Professional Support**: Visit [holoviz.org](https://holoviz.org)

---

## Changelog

### Version 0.1.0 (Current)
- Complete restructure following rse-agents plugin pattern
- 4 specialized agents (584 lines total)
- 9 comprehensive skills (4,055 lines total)
- Extensive reference materials (11,224 lines):
  - Core references: ecosystem, library matrix, best practices, patterns, troubleshooting
  - Specialized references: colormaps (4 files), Lumen Dashboards (8 files), Lumen AI (4 files)
- MCP server integration with Docker support
- BSD-3-Clause license
- Total: 16,600+ lines of expert content across 35 markdown files

---

## About HoloViz

HoloViz (formerly PyViz) is a comprehensive Python ecosystem for building data visualization applications. Created and maintained by a dedicated community of data scientists and engineers, it powers visualization solutions across academia, government, and industry.

Learn more at [holoviz.org](https://holoviz.org)

---

**Ready to become a HoloViz expert?** Start by choosing an agent that matches your current task!
