# Panel Themes and Branding Guide

## Overview

Complete guide to Panel themes, templates, and custom branding for creating professional, consistent applications.

**When to use this guide**:
- Customizing application appearance
- Corporate branding
- Dark mode support
- Template selection and customization

## Table of Contents

1. [Built-in Designs](#built-in-designs)
2. [Templates](#templates)
3. [Dark Mode](#dark-mode)
4. [Custom Themes](#custom-themes)
5. [CSS Customization](#css-customization)
6. [Branding](#branding)

## Built-in Designs

### Design Systems

Panel supports multiple design systems:

```python
import panel as pn

# Material Design
pn.extension(design='material')

# Bootstrap
pn.extension(design='bootstrap')

# Fast (Microsoft Fluent)
pn.extension(design='fast')

# Native (default)
pn.extension(design='native')
```

### Design Comparison

| Design | Style | Best For |
|--------|-------|----------|
| `material` | Google Material Design | Modern apps, dashboards |
| `bootstrap` | Bootstrap framework | Traditional web apps |
| `fast` | Microsoft Fluent | Enterprise apps |
| `native` | Minimal styling | Maximum customization |

**Example**:
```python
# Material design with dark theme
pn.extension(design='material')
pn.config.theme = 'dark'

# Create app
app = pn.Column(
    pn.widgets.Select(name='Category', options=['A', 'B', 'C']),
    pn.widgets.FloatSlider(name='Value', start=0, end=100),
    pn.pane.Markdown('## Results')
)

app.servable()
```

## Templates

### Available Templates

```python
import panel as pn

# Fast templates
from panel.template import FastListTemplate, FastGridTemplate

# Bootstrap templates
from panel.template import BootstrapTemplate

# Material templates
from panel.template import MaterialTemplate

# Vanilla (minimal)
from panel.template import VanillaTemplate

# Golden layout
from panel.template import GoldenTemplate
```

### FastListTemplate

**Best for**: Vertical list layouts, dashboards

```python
from panel.template import FastListTemplate

template = FastListTemplate(
    title='My Dashboard',
    sidebar=[
        pn.pane.Markdown('## Filters'),
        pn.widgets.Select(name='Region', options=['North', 'South']),
        pn.widgets.DateRangePicker(name='Date Range'),
    ],
    main=[
        pn.pane.Markdown('## Analysis'),
        plot1,
        plot2,
        table,
    ],
    accent='#00aa41',  # Brand color
    header_background='#2c3e50',
)

template.servable()
```

### FastGridTemplate

**Best for**: Grid layouts, complex dashboards

```python
from panel.template import FastGridTemplate

template = FastGridTemplate(
    title='Analytics Dashboard',
    sidebar=[filters],
    accent='#de8f05'
)

# Add to grid (row, column, row_span, column_span)
template.main[0:3, 0:6] = kpi_cards      # Top row
template.main[3:9, 0:6] = main_plot      # Middle
template.main[9:12, 0:3] = table1        # Bottom left
template.main[9:12, 3:6] = table2        # Bottom right

template.servable()
```

### MaterialTemplate

**Best for**: Google Material Design aesthetic

```python
from panel.template import MaterialTemplate

template = MaterialTemplate(
    title='Data Explorer',
    sidebar=[widgets],
    main=[plots],
    accent='#00aa41',
    favicon='./favicon.ico',
    logo='./logo.png'
)

template.servable()
```

### Template Comparison

| Template | Layout | Complexity | Best For |
|----------|--------|------------|----------|
| `FastListTemplate` | Vertical list | Simple | Reports, dashboards |
| `FastGridTemplate` | Grid | Medium | Complex dashboards |
| `MaterialTemplate` | Flexible | Simple | Material Design apps |
| `BootstrapTemplate` | Bootstrap | Medium | Traditional web apps |
| `VanillaTemplate` | Minimal | Simple | Maximum control |
| `GoldenTemplate` | Drag-drop | Complex | Customizable layouts |

## Dark Mode

### Enable Dark Mode

```python
import panel as pn

# Enable dark theme
pn.extension(design='material')
pn.config.theme = 'dark'

# Or with template
template = FastListTemplate(
    title='My App',
    theme='dark',  # Or 'default'
    accent='#00aa41'
)
```

### Theme Toggle

```python
# Add theme toggle button
theme_toggle = pn.widgets.Toggle(
    name='Dark Mode',
    value=False,
    button_type='primary'
)

def update_theme(event):
    if event.new:
        pn.config.theme = 'dark'
    else:
        pn.config.theme = 'default'

theme_toggle.param.watch(update_theme, 'value')

# Add to app
app = pn.Column(
    theme_toggle,
    # ... rest of app
)
```

### Dark Mode Color Considerations

```python
from colorcet import cm

# Choose colormap based on theme
def get_colormap():
    if pn.config.theme == 'dark':
        return cm['cet_fire']  # Shows well on dark
    else:
        return cm['cet_blues']  # Shows well on light

# Use in plot
plot = data.hvplot.scatter('x', 'y', c='value', cmap=get_colormap())
```

## Custom Themes

### Theme JSON

```python
import panel as pn

# Define custom theme
custom_theme = {
    'palette': {
        'primary': '#0173b2',      # Primary brand color
        'secondary': '#616161',    # Secondary color
        'accent': '#de8f05',       # Accent color
        'background': '#f8f9fa',   # Background
        'text': '#212529',         # Text color
    },
    'font': {
        'family': 'Helvetica, Arial, sans-serif',
        'size': '14px',
    }
}

pn.extension(design='material')
pn.config.theme_json = custom_theme
```

### Per-Template Theming

```python
from panel.template import FastListTemplate

template = FastListTemplate(
    title='Branded App',

    # Color customization
    accent='#0173b2',               # Accent color
    header_background='#2c3e50',    # Header background
    header_color='#ffffff',         # Header text

    # Logo and branding
    logo='./logo.png',
    favicon='./favicon.ico',

    # Sidebar
    sidebar_width=300,

    # Main area
    main_max_width='1200px',
)
```

## CSS Customization

### Raw CSS

```python
import panel as pn

# Add custom CSS
pn.config.raw_css.append("""
.card {
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    padding: 15px;
    margin: 10px;
}

.card:hover {
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.custom-title {
    font-size: 24px;
    font-weight: bold;
    color: #0173b2;
    margin-bottom: 20px;
}
""")

# Apply CSS classes
card = pn.Card(
    pn.pane.Markdown('## Card Content'),
    plot,
    css_classes=['card']
)

title = pn.pane.Markdown('Dashboard', css_classes=['custom-title'])
```

### Styled Components

```python
# Style individual components
button = pn.widgets.Button(
    name='Submit',
    button_type='primary',
    styles={
        'background': '#0173b2',
        'color': 'white',
        'border-radius': '5px',
        'font-weight': 'bold',
        'padding': '10px 20px',
    }
)

# Style containers
column = pn.Column(
    widget1,
    widget2,
    styles={
        'background': '#f8f9fa',
        'border-radius': '10px',
        'padding': '20px',
        'box-shadow': '0 2px 4px rgba(0,0,0,0.1)',
    }
)
```

### CSS Variables

```python
# Use CSS variables for consistency
pn.config.raw_css.append("""
:root {
    --primary-color: #0173b2;
    --secondary-color: #de8f05;
    --accent-color: #029e73;
    --border-radius: 10px;
    --spacing: 15px;
}

.card {
    background: var(--primary-color);
    border-radius: var(--border-radius);
    padding: var(--spacing);
}
""")
```

## Branding

### Complete Branding Pattern

```python
import panel as pn
from panel.template import FastListTemplate

# Brand configuration
BRAND = {
    'name': 'Company Name',
    'colors': {
        'primary': '#0173b2',
        'secondary': '#de8f05',
        'accent': '#029e73',
        'background': '#f8f9fa',
        'text': '#212529',
    },
    'fonts': {
        'heading': 'Helvetica, Arial, sans-serif',
        'body': 'Helvetica, Arial, sans-serif',
    },
    'logo': './assets/logo.png',
    'favicon': './assets/favicon.ico',
}

# Apply branding
pn.extension(design='material')

template = FastListTemplate(
    title=BRAND['name'],
    logo=BRAND['logo'],
    favicon=BRAND['favicon'],
    accent=BRAND['colors']['primary'],
    header_background=BRAND['colors']['primary'],
    header_color='#ffffff',
)

# Custom CSS for brand
pn.config.raw_css.append(f"""
body {{
    font-family: {BRAND['fonts']['body']};
    color: {BRAND['colors']['text']};
    background: {BRAND['colors']['background']};
}}

h1, h2, h3, h4, h5, h6 {{
    font-family: {BRAND['fonts']['heading']};
    color: {BRAND['colors']['primary']};
}}

.card {{
    border-left: 4px solid {BRAND['colors']['accent']};
}}
""")
```

### Logo and Favicon

```python
from panel.template import FastListTemplate

template = FastListTemplate(
    title='My App',

    # Logo in header
    logo='./logo.png',          # Path or URL
    logo_height='40px',

    # Browser favicon
    favicon='./favicon.ico',

    # Title next to logo
    site='Company Name',
    site_url='https://company.com',
)
```

### Consistent Color Scheme

```python
# Define color palette
COLORS = {
    'primary': '#0173b2',
    'secondary': '#de8f05',
    'success': '#029e73',
    'warning': '#d55e00',
    'danger': '#cc3311',
    'info': '#56b4e9',
}

# Use throughout app
button_submit = pn.widgets.Button(
    name='Submit',
    button_type='primary',
    styles={'background': COLORS['primary']}
)

button_cancel = pn.widgets.Button(
    name='Cancel',
    button_type='danger',
    styles={'background': COLORS['danger']}
)

# In plots
from colorcet import cm
plot = data.hvplot.scatter('x', 'y', color=COLORS['primary'])
```

## Component Styling

### Widgets

```python
# Style individual widgets
slider = pn.widgets.FloatSlider(
    name='Value',
    start=0,
    end=100,
    styles={
        'color': '#0173b2',
        'font-weight': 'bold',
    }
)

# Button styling
button = pn.widgets.Button(
    name='Submit',
    button_type='primary',  # 'default', 'primary', 'success', 'warning', 'danger'
    styles={
        'background': '#0173b2',
        'border-radius': '5px',
    }
)
```

### Cards and Containers

```python
# Styled card
card = pn.Card(
    pn.pane.Markdown('## Title'),
    plot,
    title='Analysis',
    collapsed=False,
    styles={
        'background': 'white',
        'border-radius': '10px',
        'box-shadow': '0 2px 8px rgba(0,0,0,0.1)',
        'padding': '20px',
    }
)

# Styled column
column = pn.Column(
    widget1,
    widget2,
    styles={
        'background': '#f8f9fa',
        'padding': '15px',
        'border-radius': '8px',
    }
)
```

### Responsive Styling

```python
# Responsive sizing
app = pn.Column(
    title,
    plot,
    table,
    sizing_mode='stretch_width',  # 'fixed', 'stretch_width', 'stretch_both', 'scale_width', 'scale_both'
    max_width=1200,               # Maximum width
    min_width=400,                # Minimum width
)
```

## Advanced Patterns

### Multi-Theme Support

```python
# Support both light and dark themes
class ThemedApp:
    def __init__(self):
        self.theme = pn.state.session_args.get('theme', [b'light'])[0].decode()
        pn.config.theme = 'dark' if self.theme == 'dark' else 'default'

    def get_colors(self):
        if pn.config.theme == 'dark':
            return {
                'background': '#1e1e1e',
                'text': '#ffffff',
                'primary': '#00aa41',
            }
        else:
            return {
                'background': '#ffffff',
                'text': '#212529',
                'primary': '#0173b2',
            }

app = ThemedApp()
colors = app.get_colors()
```

### Dynamic Styling

```python
# Change styling based on state
def get_status_color(status):
    colors = {
        'success': '#029e73',
        'warning': '#de8f05',
        'error': '#cc3311',
    }
    return colors.get(status, '#616161')

indicator = pn.indicators.Number(
    name='Status',
    value=100,
    format='{value}%',
    colors=[(33, 'red'), (66, 'orange'), (100, 'green')],
)
```

### Template Inheritance

```python
# Create custom template base
from panel.template import FastListTemplate

class BrandedTemplate(FastListTemplate):
    def __init__(self, **params):
        params.setdefault('accent', '#0173b2')
        params.setdefault('logo', './logo.png')
        params.setdefault('favicon', './favicon.ico')
        params.setdefault('header_background', '#2c3e50')
        super().__init__(**params)

# Use branded template
app = BrandedTemplate(title='My App')
app.main.append(plot)
app.servable()
```

## Best Practices

### 1. Consistent Theming

```python
# ✅ Good: Centralized theme config
THEME = {
    'colors': {...},
    'fonts': {...},
    'spacing': {...},
}

# Apply consistently
template = FastListTemplate(**THEME)
```

### 2. Responsive Design

```python
# ✅ Good: Responsive components
app = pn.Column(
    plot,
    table,
    sizing_mode='stretch_width',
    max_width=1200
)
```

### 3. Accessible Colors

```python
# ✅ Good: High contrast colors
from colorcet import cm
colors = {
    'primary': '#0173b2',    # High contrast
    'background': '#ffffff',
}

# ❌ Bad: Low contrast
colors = {
    'primary': '#cccccc',    # Low contrast on white
    'background': '#ffffff',
}
```

### 4. Mobile-Friendly

```python
# ✅ Good: Mobile-responsive
template = FastListTemplate(
    title='App',
    main_max_width='100%',  # Full width on mobile
    sidebar_width=250,
)
```

## Summary

**Key concepts**:
- Choose appropriate design system (Material, Bootstrap, Fast)
- Use templates for consistent layouts
- Support dark mode for accessibility
- Define brand colors and apply consistently
- Test responsive behavior

**Most common patterns**:
- FastListTemplate for dashboards
- Material design for modern apps
- Dark mode support
- Custom CSS for branding
- Consistent color schemes

**Best practices**:
- Centralize theme configuration
- Use CSS variables for consistency
- Test in light and dark modes
- Ensure mobile responsiveness
- Maintain high contrast for accessibility

## References

- [Panel Templates](https://panel.holoviz.org/user_guide/Templates.html)
- [Panel Styling](https://panel.holoviz.org/user_guide/Styling.html)
- [Material Design](https://material.io/design)
- [Bootstrap](https://getbootstrap.com/)
- [Fast Design System](https://www.fast.design/)
