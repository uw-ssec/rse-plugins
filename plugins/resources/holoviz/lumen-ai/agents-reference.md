# Built-in Agents Reference

Complete reference for Lumen AI's built-in agents and their capabilities.

## Table of Contents
- [Agent Architecture](#agent-architecture)
- [TableListAgent](#tablelistagent)
- [ChatAgent](#chatagent)
- [SQLAgent](#sqlagent)
- [hvPlotAgent](#hvplotagent)
- [VegaLiteAgent](#vegaliteagent)
- [AnalysisAgent](#analysisagent)
- [SourceAgent](#sourceagent)
- [Agent Selection Logic](#agent-selection-logic)

## Agent Architecture

Lumen AI uses a multi-agent architecture where specialized agents handle different task types. Each agent has:

- **Purpose**: Description of when the agent should be used
- **Requires**: Memory keys that must be present
- **Provides**: Memory keys the agent will populate
- **Prompts**: System prompts guiding the agent's behavior

### How Agents Work

1. User submits a query
2. Coordinator analyzes query and available agents
3. Agent selected based on purpose matching
4. Agent checks if requirements are met
5. Agent executes and streams response
6. Agent updates shared memory
7. Other agents can access results

## TableListAgent

### Purpose

Provides overview of available tables and their schemas.

### When to Use

- User asks "What tables are available?"
- User requests schema information
- User wants to know column names/types
- Starting exploration of unknown dataset

### Example Queries

```
"What tables are available?"
"Show me the schema of the sales table"
"What columns does the customer table have?"
"Describe the structure of my data"
"List all tables and their columns"
```

### Memory

**Requires**:
- `current_source`

**Provides**:
- `available_tables`: List of table metadata
- `table_schemas`: Column information for each table

### Output Format

Returns formatted table listing with:
- Table names
- Column names and types
- Row counts (if available)
- Primary keys (if defined)

### Example Output

```
Available Tables:

1. sales (15,234 rows)
   - order_id (INTEGER, PRIMARY KEY)
   - customer_id (INTEGER)
   - product_id (INTEGER)
   - order_date (DATE)
   - revenue (DECIMAL)
   - region (VARCHAR)

2. customers (5,421 rows)
   - customer_id (INTEGER, PRIMARY KEY)
   - name (VARCHAR)
   - email (VARCHAR)
   - signup_date (DATE)
```

## ChatAgent

### Purpose

General conversation, dataset summaries, explanations, and suggestions.

### When to Use

- User asks open-ended questions
- User wants dataset overview
- User requests suggestions for analyses
- User needs concept explanations

### Example Queries

```
"Give me a summary of this dataset"
"What interesting questions can I ask?"
"Explain what this data represents"
"What trends should I look for?"
"Help me understand this data"
```

### Memory

**Requires**:
- `current_source`
- `available_tables` (optional, enhances responses)

**Provides**:
- `chat_context`: Conversation history
- `suggestions`: Query suggestions

### Capabilities

- Summarizes dataset characteristics
- Suggests relevant analyses
- Explains domain concepts
- Provides context about data
- Answers general questions

## SQLAgent

### Purpose

Generates and executes SQL queries from natural language.

### When to Use

- User asks for data aggregations
- User requests filtering or sorting
- User wants to see specific records
- User asks calculation questions

### Example Queries

```
"Show me total sales by region"
"What were the top 10 products last month?"
"Calculate average order value per customer"
"Find customers who haven't purchased in 90 days"
"Show me monthly revenue for 2024"
```

### Memory

**Requires**:
- `current_source`
- `available_tables`

**Provides**:
- `sql_query`: Generated SQL
- `sql_result`: Query results as DataFrame
- `current_table`: Active table name

### Output Format

1. **Generated SQL** (code block)
2. **Result table** (formatted DataFrame)
3. **Summary** (row count, insights)

### Example Output

```
📊 Generated SQL:
```sql
SELECT region, SUM(revenue) as total_sales
FROM sales
WHERE order_date >= '2024-01-01'
GROUP BY region
ORDER BY total_sales DESC
```

Results (4 rows):

| region    | total_sales |
|-----------|-------------|
| West      | $1,245,320  |
| East      | $987,450    |
| South     | $876,230    |
| North     | $654,100    |
```

### SQL Generation Best Practices

The agent follows these practices:
- Uses appropriate date formats (YYYY-MM-DD)
- Rounds monetary values to 2 decimals
- Adds meaningful column aliases
- Includes appropriate WHERE clauses
- Orders results logically
- Limits results when appropriate

## hvPlotAgent

### Purpose

Creates interactive visualizations using hvPlot.

### When to Use

- User requests a chart or plot
- User wants to visualize relationships
- User asks for trends or patterns
- Interactive exploration needed

### Example Queries

```
"Create a scatter plot of price vs quantity"
"Show me revenue trend over time by category"
"Plot a histogram of customer ages"
"Make a bar chart of products by sales"
"Visualize the relationship between X and Y"
```

### Memory

**Requires**:
- `current_source` or `sql_result`
- Data to visualize

**Provides**:
- `current_plot`: hvPlot object
- `plot_config`: Chart configuration

### Chart Types

Automatically selects appropriate chart type:

- **Line**: Time series, trends
- **Scatter**: Relationships, correlations
- **Bar**: Categories, comparisons
- **Histogram**: Distributions
- **Box**: Statistical summaries
- **Heatmap**: Matrices, correlations

### Output Format

Returns interactive hvPlot visualization with:
- Appropriate chart type
- Clear title
- Labeled axes
- Hover tools
- Responsive sizing

### Example Output

```
📈 Created interactive scatter plot

[Interactive hvPlot visualization]

- X-axis: purchase_count
- Y-axis: total_revenue
- Color by: customer_segment
- Hover: Shows customer details
```

## VegaLiteAgent

### Purpose

Generates publication-quality Vega-Lite specifications.

### When to Use

- User needs exportable visualizations
- User wants polished, professional charts
- User needs static images
- User requires Vega-Lite format

### Example Queries

```
"Create a polished bar chart of sales by region"
"Make an exportable visualization of trends"
"Generate a Vega-Lite chart for my presentation"
"Create a publication-quality plot"
```

### Memory

**Requires**:
- `current_source` or `sql_result`
- Data to visualize

**Provides**:
- `vegalite_spec`: Vega-Lite JSON
- `rendered_chart`: Rendered output

### Output Format

1. **Vega-Lite JSON specification**
2. **Rendered visualization**
3. **Export instructions**

### Advantages Over hvPlot

- Better for static exports
- Consistent cross-platform rendering
- Professional styling by default
- Easier to embed in reports
- JSON spec for programmatic use

## AnalysisAgent

### Purpose

Executes custom domain-specific analyses.

### When to Use

Automatically invoked when:
- Custom Analysis registered
- Analysis columns match available data
- Query keywords match analysis purpose

### Custom Analyses

See [Custom Analyses Guide](custom-analyses.md) for creating domain-specific analyses like:
- Customer segmentation
- Cohort analysis
- Churn prediction
- Anomaly detection

### Memory

**Requires**:
- Data matching analysis columns
- `current_source`

**Provides**:
- Analysis results (varies by analysis)
- Generated visualizations
- Summary statistics

## SourceAgent

### Purpose

Handles file uploads and data imports.

### When to Use

Automatically triggered when:
- User uploads file via UI
- User drags-and-drops data
- User requests to import data

### Supported Formats

- CSV
- Excel (XLSX, XLS)
- Parquet
- JSON
- Feather

### Memory

**Provides**:
- `current_source`: New data source
- `available_tables`: Updated table list
- `upload_summary`: Import details

## Agent Selection Logic

### Coordinator Types

#### DependencyResolver (Default)

Selects agent by matching query to agent purposes:

```python
ui = lmai.ExplorerUI(
    source=source,
    coordinator="dependency"  # Default
)
```

**Process**:
1. Analyze query keywords
2. Match to agent purposes
3. Check if requirements met
4. Select best matching agent
5. Recursively satisfy dependencies

#### Planner

Creates execution plan upfront:

```python
ui = lmai.ExplorerUI(
    source=source,
    coordinator="planner"
)
```

**Process**:
1. Analyze overall task
2. Break into steps
3. Assign agents to steps
4. Execute sequentially
5. Pass results between steps

### Agent Priority

When multiple agents could handle a query:

1. **Most specific purpose** wins
2. **Fewest unmet requirements** preferred
3. **Most recently successful** given slight boost

### Debugging Agent Selection

```python
# See which agent was selected
print(ui.agent_manager.last_selected_agent)

# View agent purposes
for agent in ui.agents:
    print(f"{agent.__class__.__name__}: {agent.purpose}")

# Check memory state
print(ui.agent_manager.memory.keys())
```

## Customizing Built-in Agents

### Override System Prompts

```python
from lumen.ai.agents import SQLAgent

class CustomSQLAgent(SQLAgent):
    _prompts = {
        "system": """
        You are a SQL expert for financial data.

        Always:
        - Use fiscal calendar dates
        - Round currency to 2 decimals
        - Include year-over-year comparisons
        - Apply data quality filters
        """
    }

# Use custom agent
ui = lmai.ExplorerUI(
    source=source,
    agents=[CustomSQLAgent]
)
```

### Extend Agent Behavior

```python
from lumen.ai.agents import ChatAgent

class DomainChatAgent(ChatAgent):
    async def respond(self, query: str):
        # Add domain-specific preprocessing
        if "revenue" in query.lower():
            yield "Note: Revenue data is in USD\n\n"

        # Call parent implementation
        async for chunk in super().respond(query):
            yield chunk
```

### Agent Configuration

```python
# Select specific agents
agents = [
    lmai.agents.TableListAgent,
    lmai.agents.ChatAgent,
    lmai.agents.SQLAgent,
    lmai.agents.hvPlotAgent,
    # lmai.agents.VegaLiteAgent,  # Exclude if not needed
]

ui = lmai.ExplorerUI(
    source=source,
    agents=agents
)
```

## Best Practices

### Clear Agent Purposes

```python
purpose = """
Use this agent when the user asks about customer segmentation,
RFM analysis, or lifetime value calculations.

Keywords: segment, cohort, RFM, LTV, customer value

DO NOT use for general statistics or simple aggregations.
"""
```

### Memory Management

```python
# Access memory in custom code
memory = ui.agent_manager.memory

# Check what's available
print(memory.keys())

# Access specific values
current_source = memory.get("current_source")
last_sql = memory.get("sql_query")
```

### Error Handling

```python
class RobustAgent(Agent):
    async def respond(self, query: str):
        try:
            result = await self.process(query)
            yield result
        except KeyError as e:
            yield f"❌ Column not found: {e}"
        except Exception as e:
            yield f"❌ Error: {str(e)}. Please rephrase."
```

## Related Resources

- [Custom Agents Guide](custom-agents.md) - Build your own agents
- [Custom Tools Guide](custom-tools.md) - Extend agent capabilities
- [Memory and Context](memory-context.md) - Understanding the memory system
