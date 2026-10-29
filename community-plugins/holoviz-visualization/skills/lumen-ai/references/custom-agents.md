# Custom Agents Development Guide

Learn to build specialized AI agents for domain-specific tasks in Lumen AI.

## Table of Contents
- [Agent Basics](#agent-basics)
- [Agent Structure](#agent-structure)
- [Building Your First Agent](#building-your-first-agent)
- [Advanced Agent Patterns](#advanced-agent-patterns)
- [Agent Communication](#agent-communication)
- [Best Practices](#best-practices)

## Agent Basics

### What is an Agent?

An agent is a specialized component that:
- Handles a specific type of query or task
- Has a clear purpose and scope
- Can access shared memory
- Streams responses to users
- Updates context for other agents

### When to Create a Custom Agent

Create a custom agent when you need:
- Domain-specific analysis logic
- Integration with external systems
- Specialized data transformations
- Custom visualization types
- Industry-specific calculations

**Don't create an agent when**:
- Built-in agents already handle it
- A custom tool would suffice
- A custom analysis is more appropriate

## Agent Structure

### Basic Agent Class

```python
from lumen.ai.agents import Agent
import param

class MyAgent(Agent):
    """Agent description."""

    # What memory keys this agent needs
    requires = param.List(default=["current_source"])

    # What memory keys this agent will provide
    provides = param.List(default=["my_result"])

    # When to use this agent
    purpose = """
    Use this agent when the user asks about X, Y, or Z.
    Keywords: keyword1, keyword2, keyword3
    """

    # System prompts for LLM
    _prompts = {
        "system": """
        You are an expert in...
        Your role is to...
        """
    }

    async def respond(self, query: str):
        """
        Execute agent logic and yield responses.

        Args:
            query: User's natural language query
        """
        # Access memory
        source = self.memory["current_source"]

        # Process query
        result = self.process(query, source)

        # Stream response
        yield result

        # Update memory
        self.memory["my_result"] = result
```

### Key Components

**requires**: Memory keys that must exist before agent runs
**provides**: Memory keys agent will create/update
**purpose**: Description for agent selection
**_prompts**: System prompts for LLM calls
**respond()**: Main execution method (must be async generator)

## Building Your First Agent

### Example: Sentiment Analysis Agent

```python
from lumen.ai.agents import Agent
import param
import pandas as pd

class SentimentAgent(Agent):
    """Analyze sentiment in text data."""

    requires = param.List(default=["current_source"])
    provides = param.List(default=["sentiment_analysis"])

    purpose = """
    Analyzes sentiment in text columns of the dataset.
    Use when user asks about sentiment, emotions, or tone in text data.
    Keywords: sentiment, emotion, positive, negative, tone, feeling
    """

    _prompts = {
        "system": """
        You are a sentiment analysis expert.
        Analyze text data to determine positive, negative, or neutral sentiment.
        Provide confidence scores and key phrases driving the sentiment.
        """
    }

    async def respond(self, query: str):
        """Execute sentiment analysis."""
        # Get data source
        source = self.memory["current_source"]

        # Find text columns
        df = source.get(source.tables[0])
        text_columns = df.select_dtypes(include=['object']).columns.tolist()

        if not text_columns:
            yield "❌ No text columns found for sentiment analysis."
            return

        yield f"🔍 Found text columns: {', '.join(text_columns)}\n\n"
        yield f"📊 Analyzing sentiment in '{text_columns[0]}'...\n\n"

        # Prepare analysis prompt
        sample_text = df[text_columns[0]].dropna().head(10).tolist()
        analysis_prompt = f"""
        Analyze sentiment in these text samples:
        {sample_text}

        User query: {query}

        Provide:
        1. Overall sentiment distribution (positive/negative/neutral %)
        2. Key themes and topics
        3. Notable patterns
        4. Recommendations for further analysis
        """

        # Stream LLM response
        response = ""
        async for chunk in self._stream(analysis_prompt):
            response += chunk
            yield chunk

        # Store in memory for other agents
        self.memory["sentiment_analysis"] = response
        self.memory["analyzed_column"] = text_columns[0]
```

### Register and Use

```python
import lumen.ai as lmai
from lumen.sources.duckdb import DuckDBSource

source = DuckDBSource(tables=["customer_reviews.csv"])

ui = lmai.ExplorerUI(
    source=source,
    agents=[
        SentimentAgent,          # Your custom agent
        lmai.agents.ChatAgent,   # Still include built-ins
        lmai.agents.SQLAgent,
    ]
)

ui.servable()
```

### Test Queries

```
"Analyze sentiment in the reviews"
"What's the overall tone of customer feedback?"
"Show me positive vs negative sentiment distribution"
```

## Advanced Agent Patterns

### Pattern 1: External API Integration

```python
from lumen.ai.agents import Agent
import param
import requests

class WeatherEnrichmentAgent(Agent):
    """Enrich data with weather information."""

    api_key = param.String(default=None)
    requires = param.List(default=["current_source"])
    provides = param.List(default=["weather_enriched_data"])

    purpose = """
    Enriches data with weather information from external API.
    Use when user asks about weather impact, climate correlation,
    or seasonal patterns.
    Keywords: weather, temperature, climate, seasonal
    """

    async def respond(self, query: str):
        """Fetch weather data and enrich dataset."""
        source = self.memory["current_source"]
        df = source.get(source.tables[0])

        # Check for date and location columns
        if "date" not in df.columns or "city" not in df.columns:
            yield "❌ Need 'date' and 'city' columns for weather enrichment."
            return

        yield "🌤️ Fetching weather data...\n\n"

        # Fetch weather for each date/city
        weather_data = []
        for _, row in df.iterrows():
            weather = self._fetch_weather(row["date"], row["city"])
            weather_data.append(weather)

        df["temperature"] = [w["temp"] for w in weather_data]
        df["conditions"] = [w["conditions"] for w in weather_data]

        # Update source with enriched data
        self.memory["weather_enriched_data"] = df

        yield f"✅ Enriched {len(df)} rows with weather data\n"
        yield df.head()

    def _fetch_weather(self, date: str, city: str) -> dict:
        """Fetch weather from API."""
        url = f"https://api.weather.com/historical"
        params = {"date": date, "city": city, "key": self.api_key}
        response = requests.get(url, params=params)
        return response.json()
```

### Pattern 2: Multi-Step Analysis

```python
class MultiStepAnalysisAgent(Agent):
    """Execute complex multi-step analysis."""

    requires = param.List(default=["current_source"])
    provides = param.List(default=["analysis_result", "recommendations"])

    purpose = """
    Performs complex multi-step data analysis.
    Use for comprehensive data investigations.
    Keywords: analyze, investigate, deep dive, comprehensive
    """

    async def respond(self, query: str):
        """Execute multi-step analysis."""
        # Step 1: Data quality check
        yield "### Step 1: Data Quality Assessment\n\n"
        quality_report = await self._assess_quality()
        yield quality_report
        yield "\n\n"

        # Step 2: Descriptive statistics
        yield "### Step 2: Descriptive Statistics\n\n"
        stats = await self._compute_statistics()
        yield stats
        yield "\n\n"

        # Step 3: Pattern detection
        yield "### Step 3: Pattern Detection\n\n"
        patterns = await self._detect_patterns()
        yield patterns
        yield "\n\n"

        # Step 4: Recommendations
        yield "### Step 4: Recommendations\n\n"
        recommendations = await self._generate_recommendations(
            quality_report, stats, patterns
        )
        yield recommendations

        # Store final results
        self.memory["analysis_result"] = {
            "quality": quality_report,
            "statistics": stats,
            "patterns": patterns,
            "recommendations": recommendations
        }

    async def _assess_quality(self):
        """Assess data quality."""
        source = self.memory["current_source"]
        df = source.get(source.tables[0])

        missing = df.isnull().sum()
        duplicates = df.duplicated().sum()

        return f"""
        - Total rows: {len(df):,}
        - Missing values: {missing.sum():,}
        - Duplicate rows: {duplicates:,}
        - Completeness: {(1 - missing.sum() / df.size) * 100:.1f}%
        """

    async def _compute_statistics(self):
        """Compute descriptive statistics."""
        # Implementation here
        pass

    async def _detect_patterns(self):
        """Detect patterns in data."""
        # Implementation here
        pass

    async def _generate_recommendations(self, quality, stats, patterns):
        """Generate analysis recommendations."""
        prompt = f"""
        Based on this analysis:

        Quality: {quality}
        Statistics: {stats}
        Patterns: {patterns}

        Provide actionable recommendations for:
        1. Data quality improvements
        2. Further analyses to conduct
        3. Business insights to explore
        """

        response = ""
        async for chunk in self._stream(prompt):
            response += chunk

        return response
```

### Pattern 3: Conditional Logic

```python
class SmartQueryAgent(Agent):
    """Intelligently routes queries to sub-analyses."""

    requires = param.List(default=["current_source"])
    provides = param.List(default=["smart_result"])

    purpose = """
    Intelligently analyzes queries and routes to appropriate sub-analysis.
    Use for complex or ambiguous questions.
    """

    async def respond(self, query: str):
        """Route query to appropriate handler."""
        # Classify query type
        query_type = await self._classify_query(query)

        if query_type == "aggregation":
            yield "🔢 Detected aggregation query\n\n"
            async for chunk in self._handle_aggregation(query):
                yield chunk

        elif query_type == "comparison":
            yield "⚖️ Detected comparison query\n\n"
            async for chunk in self._handle_comparison(query):
                yield chunk

        elif query_type == "trend":
            yield "📈 Detected trend analysis query\n\n"
            async for chunk in self._handle_trend(query):
                yield chunk

        else:
            yield "🤔 General analysis query\n\n"
            async for chunk in self._handle_general(query):
                yield chunk

    async def _classify_query(self, query: str) -> str:
        """Classify query type using LLM."""
        prompt = f"""
        Classify this query into one category:
        - aggregation (sum, count, average)
        - comparison (compare A vs B)
        - trend (over time, pattern)
        - general (other)

        Query: {query}

        Respond with just the category name.
        """

        classification = ""
        async for chunk in self._stream(prompt):
            classification += chunk

        return classification.strip().lower()

    async def _handle_aggregation(self, query: str):
        """Handle aggregation queries."""
        # Implementation
        yield "Aggregation result..."

    async def _handle_comparison(self, query: str):
        """Handle comparison queries."""
        # Implementation
        yield "Comparison result..."

    async def _handle_trend(self, query: str):
        """Handle trend queries."""
        # Implementation
        yield "Trend analysis..."

    async def _handle_general(self, query: str):
        """Handle general queries."""
        # Implementation
        yield "General analysis..."
```

## Agent Communication

### Reading from Memory

```python
async def respond(self, query: str):
    # Access previous results
    sql_result = self.memory.get("sql_result")
    current_table = self.memory.get("current_table")
    previous_analysis = self.memory.get("sentiment_analysis")

    if sql_result is not None:
        # Use previous SQL results
        yield f"Building on previous query with {len(sql_result)} rows...\n"
    else:
        # No previous results
        yield "No previous query results found.\n"
```

### Writing to Memory

```python
async def respond(self, query: str):
    # Process data
    result = self.process_data()

    # Store for other agents
    self.memory["my_analysis"] = result
    self.memory["analysis_timestamp"] = datetime.now()
    self.memory["analysis_type"] = "sentiment"

    yield result
```

### Agent Chaining

```python
class PreprocessAgent(Agent):
    """Preprocess data for other agents."""

    provides = param.List(default=["cleaned_data"])

    async def respond(self, query: str):
        # Clean data
        cleaned = self.clean_data()

        # Store for next agent
        self.memory["cleaned_data"] = cleaned

        yield "✅ Data preprocessed\n"


class AnalysisAgent(Agent):
    """Analyze preprocessed data."""

    requires = param.List(default=["cleaned_data"])

    async def respond(self, query: str):
        # Use cleaned data from PreprocessAgent
        data = self.memory["cleaned_data"]

        # Analyze
        result = self.analyze(data)

        yield result
```

## Best Practices

### 1. Clear Agent Purpose

```python
# ❌ Too vague
purpose = "Handles data analysis"

# ✅ Specific and clear
purpose = """
Performs customer segmentation analysis using RFM methodology.
Use when user asks about:
- Customer segments or cohorts
- RFM (Recency, Frequency, Monetary) analysis
- Customer lifetime value grouping

Keywords: segment, cohort, RFM, customer value, grouping

Do NOT use for:
- Simple aggregations (use SQLAgent)
- Visualization only (use hvPlotAgent)
"""
```

### 2. Streaming Responses

```python
# ✅ Good: Stream for real-time feedback
async def respond(self, query: str):
    yield "🔍 Step 1: Loading data...\n"
    data = self.load_data()

    yield "🔍 Step 2: Processing...\n"
    result = self.process(data)

    yield "✅ Complete!\n\n"
    yield result

# ❌ Bad: User sees nothing until complete
async def respond(self, query: str):
    data = self.load_data()
    result = self.process(data)
    yield result  # Long wait with no feedback
```

### 3. Error Handling

```python
async def respond(self, query: str):
    try:
        result = await self.process(query)
        yield result

    except KeyError as e:
        yield f"❌ Column not found: {e}\n"
        yield f"Available columns: {self.get_columns()}\n"

    except ValueError as e:
        yield f"❌ Invalid value: {e}\n"
        yield "Please check your query and try again.\n"

    except Exception as e:
        yield f"❌ Unexpected error: {str(e)}\n"
        yield "Please rephrase your question or contact support.\n"
```

### 4. Memory Management

```python
# ✅ Good: Check before access
async def respond(self, query: str):
    if "previous_result" in self.memory:
        prev = self.memory["previous_result"]
        yield "Building on previous analysis...\n"
    else:
        yield "Starting fresh analysis...\n"

# ❌ Bad: Assume memory exists
async def respond(self, query: str):
    prev = self.memory["previous_result"]  # KeyError if not present
```

### 5. Testing Agents

```python
import pytest
from lumen.sources.duckdb import DuckDBSource

@pytest.mark.asyncio
async def test_sentiment_agent():
    # Setup
    source = DuckDBSource(tables=["test_data.csv"])
    agent = SentimentAgent()
    agent.memory["current_source"] = source

    # Execute
    results = []
    async for chunk in agent.respond("analyze sentiment"):
        results.append(chunk)

    # Assert
    result = "".join(results)
    assert "sentiment" in result.lower()
    assert "sentiment_analysis" in agent.memory
```

### 6. Documentation

```python
class MyAgent(Agent):
    """
    Short one-line description.

    Longer description explaining:
    - What this agent does
    - When to use it
    - What it requires
    - What it provides

    Examples:
        >>> agent = MyAgent()
        >>> async for chunk in agent.respond("example query"):
        ...     print(chunk)
    """

    async def respond(self, query: str):
        """
        Execute agent logic.

        Args:
            query: User's natural language question

        Yields:
            Response chunks for streaming to user

        Raises:
            ValueError: If query cannot be processed
            KeyError: If required memory keys missing
        """
        pass
```

## Complete Example

See [Examples Guide](examples.md) for a complete end-to-end example of a custom agent in a production application.

## Related Resources

- [Built-in Agents Reference](agents-reference.md)
- [Custom Tools Guide](custom-tools.md)
- [Custom Analyses Guide](custom-analyses.md)
- [Memory System](memory-context.md)
