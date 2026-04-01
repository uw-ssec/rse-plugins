# Visualization Patterns — Deep Reference

## Contents

| Section | Lines | Description |
|---------|-------|-------------|
| Bar Charts for Configuration Comparison | 16–67 | Time per config grouped by pattern with formatting guidelines |
| Heatmaps for Multi-Dimensional Results | 70–111 | Config x pattern to metric mapping with color scale guidance |
| Radar/Spider Charts for Balance Assessment | 114–163 | Multi-metric per config for visual PB assessment |
| Memory vs Time Scatter Plots | 166–219 | Pareto frontier identification for trade-off analysis |
| Performance Bias Visualization | 222–267 | Bar chart of bias values with classification bands |
| Generating Plots with matplotlib/hvPlot | 270–463 | Complete code examples for all chart types |

---

## Bar Charts for Configuration Comparison

Grouped bar charts are the most effective visualization for comparing wall-clock times across configurations and access patterns.

### Structure

- **X-axis**: Chunk configurations (labeled by shape or letter identifier)
- **Y-axis**: Wall-clock time in seconds
- **Groups**: One bar per access pattern, grouped by configuration
- **Error bars**: Standard deviation from benchmark runs

### When to Use

- Comparing 2–8 configurations across 2–4 access patterns
- Presenting results to stakeholders who need a quick visual comparison
- Identifying which configuration wins for each pattern

### Formatting Guidelines

- Use distinct colors for each access pattern (e.g., blue = spatial, orange = temporal, green = spectral)
- Include error bars showing +/- 1 standard deviation
- Add a horizontal dashed line at the memory budget threshold if plotting memory alongside time
- Label the y-axis with units: "Wall-Clock Time (s)"
- Sort configurations by the primary pattern time (ascending, left to right)
- Add value labels on top of each bar for exact numbers

### Example Layout

```
Wall-Clock Time by Configuration and Access Pattern

    18 |                              ___
    16 |                             | T |
    14 |                    ___      |   |
    12 |         ___       | S |     |   |
    10 |   ___  | T |      |   |     |   |
     8 |  | S | |   | ___  |   | ___ |   |
     6 |  |   | |   || Sp| |   || Sp||   |
     4 |  |   | |   ||   | |   ||   ||   |
     2 |  |   | |   ||   | |   ||   ||   |
     0 +--+---+-+---++---+-+---++---++---+--
          Config B      Config C     Config A

    [S] Spatial  [T] Temporal  [Sp] Spectral
```

### Pitfalls

- Do not use stacked bars — they obscure individual pattern comparisons
- Do not omit error bars — without them, small differences may appear significant
- Do not use 3D effects — they distort perception of bar heights

---

## Heatmaps for Multi-Dimensional Results

Heatmaps display the relationship between two categorical variables (configuration and access pattern) mapped to a continuous metric (time, memory, or throughput).

### Structure

- **Rows**: Chunk configurations
- **Columns**: Access patterns (spatial, temporal, spectral)
- **Cell values**: Metric value (e.g., mean wall-clock time)
- **Color scale**: Sequential colormap (e.g., `viridis`, `YlOrRd`) mapping low-to-high

### When to Use

- Displaying results for many configurations (8+) where grouped bars become cluttered
- Showing relative performance patterns across the full config x pattern matrix
- Identifying clusters of similarly-performing configurations

### Color Scale Selection

| Metric | Recommended Colormap | Direction |
|--------|---------------------|-----------|
| Wall-clock time | `YlOrRd` (yellow to red) | Lower = lighter = better |
| Throughput | `YlGn` (yellow to green) | Higher = darker = better |
| Memory | `YlOrRd` (yellow to red) | Lower = lighter = better |
| PB | `RdYlGn_r` (green to red) | Lower = green = better |

### Formatting Guidelines

- Annotate each cell with the numeric value
- Use consistent decimal places across all cells
- Add a colorbar with units
- Sort rows by composite score or PB to group similar configurations
- Highlight the best value per column with a border or bold text

### Normalization

For heatmaps comparing across patterns with very different absolute scales, normalize by column (min-max scaling per pattern) so color intensity reflects relative rank rather than absolute value:

```python
normalized = (value - col_min) / (col_max - col_min)
```

---

## Radar/Spider Charts for Balance Assessment

Radar charts display multiple metrics for a single configuration on radial axes, making it easy to visually assess balance.

### Structure

- **Axes**: One per metric or access pattern (3–6 axes)
- **Lines**: One polygon per configuration
- **Scale**: Normalized 0–1 where 1 = best observed value

### When to Use

- Comparing 2–4 configurations on 3–6 metrics simultaneously
- Visually assessing whether a configuration is balanced (round polygon) or specialized (spiky polygon)
- Complementing the PB metric with a visual representation

### Axis Design

For access pattern comparison:
- Each axis represents one access pattern
- Scale is inverted (lower time = further from center = better)
- A perfectly balanced configuration forms a regular polygon

For multi-metric comparison:
- Axes: wall-clock time (inverted), throughput, memory (inverted), utilization, PB (inverted)
- Normalize each axis 0–1 based on best/worst observed values

### Formatting Guidelines

- Use distinct line colors and styles for each configuration
- Fill polygons with low-opacity color (alpha = 0.1–0.2) to see overlap
- Label each axis clearly
- Include a legend identifying configurations
- Limit to 4 configurations per chart — more becomes unreadable

### Interpretation

- **Round polygon**: Balanced configuration (low PB)
- **Spiky polygon**: Specialized configuration (high PB)
- **Large polygon**: Good overall performance
- **Small polygon**: Poor overall performance
- **Overlapping polygons**: Configurations with similar trade-offs

### Limitations

- Radar charts can mislead when axes have very different scales
- The visual area of the polygon depends on axis ordering
- Not suitable for more than 4–5 configurations (too cluttered)
- Always present alongside numeric tables, never as the sole representation

---

## Memory vs Time Scatter Plots

Scatter plots with memory on one axis and time on the other reveal the Pareto frontier — configurations where improving one metric requires sacrificing the other.

### Structure

- **X-axis**: Wall-clock time for the primary access pattern (seconds)
- **Y-axis**: Peak memory (GB)
- **Points**: One per configuration, labeled with chunk shape or config letter
- **Pareto frontier**: Line connecting non-dominated points

### When to Use

- Identifying trade-offs between speed and memory
- Finding the Pareto-optimal set of configurations
- Communicating that "faster" and "less memory" often conflict

### Pareto Frontier Identification

A configuration is Pareto-optimal if no other configuration is both faster and uses less memory:

```python
def pareto_frontier(configs):
    """Return Pareto-optimal configs (minimizing both time and memory)."""
    sorted_configs = sorted(configs, key=lambda c: c['time'])
    frontier = [sorted_configs[0]]
    min_mem = frontier[0]['memory']
    for config in sorted_configs[1:]:
        if config['memory'] < min_mem:
            frontier.append(config)
            min_mem = config['memory']
    return frontier
```

### Formatting Guidelines

- Draw the memory budget as a horizontal dashed line — configs above it are infeasible
- Color Pareto-optimal points differently (e.g., green) from dominated points (e.g., gray)
- Add error bars for time (horizontal) and memory (vertical) if variance data is available
- Annotate each point with its chunk shape
- Shade the infeasible region (above memory budget) in light red

### Multi-Pattern Variant

Create one scatter plot per access pattern, or use a faceted layout with shared axes for direct comparison:

```
Spatial                  Temporal                 Spectral
Mem |  x                Mem |     x              Mem |    x
    |    x   (budget)       |  x     (budget)        |  x    (budget)
    | x                     |x                       |   x
    +-------Time            +-------Time              +-------Time
```

---

## Performance Bias Visualization

A horizontal bar chart of PB values provides an immediate visual ranking of configuration balance.

### Structure

- **Y-axis**: Configurations (sorted by PB ascending)
- **X-axis**: Performance bias value
- **Bars**: One per configuration, colored by classification band
- **Reference lines**: Vertical lines at PB = 1.5, 3.0, 10.0 marking classification boundaries

### When to Use

- Highlighting how balanced each configuration is
- Communicating PB classification visually
- Identifying configurations suitable for mixed workloads (PB < 1.5)

### Color Coding

| PB Range | Color | Classification |
|----------|-------|---------------|
| < 1.5 | Green | Balanced |
| 1.5–3.0 | Yellow/Orange | Moderate |
| 3.0–10.0 | Orange/Red | Biased |
| > 10.0 | Dark Red | Extreme |

### Formatting Guidelines

- Sort bars from lowest PB (top) to highest PB (bottom)
- Add vertical dashed lines at classification boundaries (1.5, 3.0, 10.0)
- Label each bar with the exact PB value
- Include the chunk shape as part of the y-axis label
- Add a shaded background for each classification zone

### Annotation

Add the best and worst pattern names next to each bar to explain what drives the bias:

```
(50, 512, 512)   |======| 1.35  [best: Spatial, worst: Temporal]
(100, 256, 256)  |======| 1.42  [best: Temporal, worst: Spectral]
(200, 128, 128)  |============| 2.64  [best: Temporal, worst: Spatial]
(10, 1024, 1024) |===============| 3.02  [best: Spatial, worst: Temporal]
                  0    1.5   3.0
```

---

## Generating Plots with matplotlib/hvPlot

### Grouped Bar Chart with matplotlib

```python
import matplotlib.pyplot as plt
import numpy as np

configs = ["(50,512,512)", "(100,256,256)", "(10,1024,1024)", "(200,128,128)"]
spatial = [8.3, 9.1, 6.1, 15.3]
temporal = [11.2, 9.8, 18.4, 5.8]
spectral = [10.1, 11.5, 12.7, 14.2]
spatial_err = [0.7, 0.8, 0.5, 1.1]
temporal_err = [0.9, 0.7, 1.2, 0.4]
spectral_err = [0.6, 0.9, 0.8, 1.0]

x = np.arange(len(configs))
width = 0.25

fig, ax = plt.subplots(figsize=(10, 6))
bars1 = ax.bar(x - width, spatial, width, yerr=spatial_err,
               label="Spatial", color="#4C72B0", capsize=3)
bars2 = ax.bar(x, temporal, width, yerr=temporal_err,
               label="Temporal", color="#DD8452", capsize=3)
bars3 = ax.bar(x + width, spectral, width, yerr=spectral_err,
               label="Spectral", color="#55A868", capsize=3)

ax.set_xlabel("Chunk Configuration")
ax.set_ylabel("Wall-Clock Time (s)")
ax.set_title("Benchmark Results by Configuration and Access Pattern")
ax.set_xticks(x)
ax.set_xticklabels(configs, rotation=15)
ax.legend()
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("benchmark_comparison.png", dpi=150)
```

### Heatmap with matplotlib

```python
import matplotlib.pyplot as plt
import numpy as np

configs = ["(50,512,512)", "(100,256,256)", "(10,1024,1024)", "(200,128,128)"]
patterns = ["Spatial", "Temporal", "Spectral"]
data = np.array([
    [8.3, 11.2, 10.1],
    [9.1, 9.8, 11.5],
    [6.1, 18.4, 12.7],
    [15.3, 5.8, 14.2],
])

fig, ax = plt.subplots(figsize=(8, 5))
im = ax.imshow(data, cmap="YlOrRd", aspect="auto")

ax.set_xticks(range(len(patterns)))
ax.set_xticklabels(patterns)
ax.set_yticks(range(len(configs)))
ax.set_yticklabels(configs)

for i in range(len(configs)):
    for j in range(len(patterns)):
        ax.text(j, i, f"{data[i, j]:.1f}", ha="center", va="center",
                color="black" if data[i, j] < 12 else "white")

ax.set_title("Wall-Clock Time (s) by Configuration and Pattern")
fig.colorbar(im, ax=ax, label="Time (s)")
plt.tight_layout()
plt.savefig("benchmark_heatmap.png", dpi=150)
```

### Radar Chart with matplotlib

```python
import matplotlib.pyplot as plt
import numpy as np

categories = ["Spatial", "Temporal", "Spectral"]
n_cats = len(categories)

# Normalize: invert so lower time = higher value (better)
config_b = [8.3, 11.2, 10.1]
config_a = [6.1, 18.4, 12.7]
max_val = max(max(config_b), max(config_a))
config_b_norm = [1 - (v / max_val) for v in config_b]
config_a_norm = [1 - (v / max_val) for v in config_a]

angles = np.linspace(0, 2 * np.pi, n_cats, endpoint=False).tolist()
angles += angles[:1]  # Close the polygon

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

for values, label, color in [
    (config_b_norm, "(50,512,512)", "#4C72B0"),
    (config_a_norm, "(10,1024,1024)", "#DD8452"),
]:
    vals = values + values[:1]
    ax.plot(angles, vals, "o-", label=label, color=color)
    ax.fill(angles, vals, alpha=0.15, color=color)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories)
ax.set_title("Configuration Balance (larger = better)")
ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))
plt.tight_layout()
plt.savefig("benchmark_radar.png", dpi=150)
```

### Memory vs Time Scatter Plot with matplotlib

```python
import matplotlib.pyplot as plt

configs = {
    "(50,512,512)": {"time": 8.3, "memory": 3.8},
    "(100,256,256)": {"time": 9.1, "memory": 5.1},
    "(10,1024,1024)": {"time": 6.1, "memory": 10.2},
    "(200,128,128)": {"time": 15.3, "memory": 4.3},
}
memory_budget = 8.0

fig, ax = plt.subplots(figsize=(8, 6))

for label, vals in configs.items():
    color = "green" if vals["memory"] <= memory_budget else "red"
    ax.scatter(vals["time"], vals["memory"], s=100, c=color, zorder=5)
    ax.annotate(label, (vals["time"], vals["memory"]),
                textcoords="offset points", xytext=(5, 5), fontsize=8)

ax.axhline(y=memory_budget, color="gray", linestyle="--",
           label=f"Memory budget ({memory_budget} GB)")
ax.axhspan(memory_budget, ax.get_ylim()[1] if ax.get_ylim()[1] > memory_budget else memory_budget + 5,
           alpha=0.1, color="red")

ax.set_xlabel("Wall-Clock Time — Spatial (s)")
ax.set_ylabel("Peak Memory (GB)")
ax.set_title("Time vs Memory Trade-off (Spatial Access)")
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("benchmark_scatter.png", dpi=150)
```

### Performance Bias Bar Chart with matplotlib

```python
import matplotlib.pyplot as plt

configs = ["(50,512,512)", "(100,256,256)", "(200,128,128)", "(10,1024,1024)"]
pb_values = [1.35, 1.42, 2.64, 3.02]
colors = ["green" if pb < 1.5 else "orange" if pb < 3.0 else "red" for pb in pb_values]

fig, ax = plt.subplots(figsize=(8, 4))
bars = ax.barh(configs, pb_values, color=colors, height=0.5)

ax.axvline(x=1.5, color="gray", linestyle="--", alpha=0.7, label="Balanced threshold")
ax.axvline(x=3.0, color="gray", linestyle=":", alpha=0.7, label="Biased threshold")

for bar, pb in zip(bars, pb_values):
    ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2,
            f"{pb:.2f}", va="center", fontsize=10)

ax.set_xlabel("Performance Bias (PB)")
ax.set_title("Performance Bias by Configuration")
ax.legend()
ax.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.savefig("benchmark_bias.png", dpi=150)
```

### Interactive Plots with hvPlot

For interactive exploration in Jupyter notebooks, use hvPlot with xarray or pandas:

```python
import pandas as pd
import hvplot.pandas

df = pd.DataFrame({
    "Config": ["B", "B", "B", "C", "C", "C", "A", "A", "A"],
    "Pattern": ["Spatial", "Temporal", "Spectral"] * 3,
    "Time (s)": [8.3, 11.2, 10.1, 9.1, 9.8, 11.5, 6.1, 18.4, 12.7],
})

plot = df.hvplot.bar(
    x="Config", y="Time (s)", by="Pattern",
    title="Benchmark Results",
    width=600, height=400,
    ylabel="Wall-Clock Time (s)",
)
hvplot.save(plot, "benchmark_interactive.html")
```
