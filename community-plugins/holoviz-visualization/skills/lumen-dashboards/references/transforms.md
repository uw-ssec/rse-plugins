# Lumen Data Transforms Reference

## Overview

Complete reference for data transformations in Lumen pipelines. Covers filtering, aggregation, SQL queries, and custom transforms.

**When to use this reference**:
- Processing data in pipelines
- Filtering and aggregating data
- Writing SQL transforms
- Creating custom transforms

## Table of Contents

1. [Transform Types](#transform-types)
2. [Filter Transforms](#filter-transforms)
3. [Aggregation](#aggregation)
4. [SQL Transforms](#sql-transforms)
5. [Data Manipulation](#data-manipulation)
6. [Custom Transforms](#custom-transforms)

## Transform Types

### Available Transforms

| Transform | Purpose | Example |
|-----------|---------|---------|
| `columns` | Select specific columns | Keep only needed columns |
| `query` | Filter rows with pandas query | `revenue > 1000` |
| `aggregate` | Group and aggregate | Sum revenue by region |
| `sort` | Sort data | Order by date desc |
| `sql` | Custom SQL | Complex aggregations |
| `astype` | Change data types | Convert to datetime |
| `dropna` | Remove null values | Clean missing data |
| `fillna` | Fill null values | Replace with defaults |
| `rename` | Rename columns | Standardize names |
| `iloc` | Select by position | Get first N rows |
| `head` | Get first N rows | Preview data |
| `tail` | Get last N rows | Recent data |

## Filter Transforms

### Query Transform

**Filter rows using pandas query syntax**:

```yaml
transforms:
  # Simple filter
  - type: query
    query: "revenue > 1000"

  # Multiple conditions
  - type: query
    query: "revenue > 1000 and region == 'North'"

  # Using operators
  - type: query
    query: "category in ['A', 'B', 'C']"

  # Date filtering
  - type: query
    query: "date >= '2024-01-01'"

  # String operations
  - type: query
    query: "name.str.contains('test')"
```

### Query Examples

```yaml
transforms:
  # Numeric comparison
  - type: query
    query: "price >= 10 and price <= 100"

  # String matching
  - type: query
    query: "status == 'active'"

  # List membership
  - type: query
    query: "region in @allowed_regions"  # Uses variable

  # Not equal
  - type: query
    query: "category != 'excluded'"

  # Null checking
  - type: query
    query: "value.notna()"  # Not null

  # Combined conditions
  - type: query
    query: "(revenue > 5000) and (region in ['North', 'South'])"
```

### Columns Transform

**Select specific columns**:

```yaml
transforms:
  # Select columns
  - type: columns
    columns: ['date', 'region', 'revenue', 'quantity']

  # Exclude columns (use query with drop)
  - type: query
    query: "columns.difference(['col_to_drop'])"
```

## Aggregation

### Basic Aggregation

```yaml
transforms:
  - type: aggregate
    by: ['region']  # Group by columns
    aggregate:
      # Column: {source_column: aggregation_function}
      total_revenue: {revenue: sum}
      avg_revenue: {revenue: mean}
      order_count: {order_id: count}
      max_price: {price: max}
      min_price: {price: min}
```

### Aggregation Functions

```yaml
transforms:
  - type: aggregate
    by: ['date', 'category']
    aggregate:
      # Numeric aggregations
      sum_col: {value: sum}
      mean_col: {value: mean}
      median_col: {value: median}
      std_col: {value: std}
      var_col: {value: var}
      min_col: {value: min}
      max_col: {value: max}

      # Count aggregations
      count_col: {id: count}
      nunique_col: {customer_id: nunique}  # Count unique

      # String aggregations
      first_col: {name: first}
      last_col: {name: last}
```

### Multi-Column Aggregation

```yaml
transforms:
  - type: aggregate
    by: ['region', 'category']
    aggregate:
      # Multiple metrics per column
      revenue_sum: {revenue: sum}
      revenue_mean: {revenue: mean}
      revenue_max: {revenue: max}

      # Different columns
      order_count: {order_id: count}
      customer_count: {customer_id: nunique}
      avg_quantity: {quantity: mean}
```

### Time-Based Aggregation

```yaml
transforms:
  # First, create time grouping
  - type: sql
    query: |
      SELECT
        DATE_TRUNC('month', date) as month,
        region,
        SUM(revenue) as monthly_revenue,
        COUNT(*) as order_count
      FROM table
      GROUP BY month, region
      ORDER BY month DESC
```

## SQL Transforms

### Basic SQL

```yaml
transforms:
  - type: sql
    query: |
      SELECT
        region,
        SUM(revenue) as total_revenue,
        AVG(revenue) as avg_revenue,
        COUNT(*) as order_count
      FROM table
      GROUP BY region
      ORDER BY total_revenue DESC
```

### Complex SQL Queries

```yaml
transforms:
  # Window functions
  - type: sql
    query: |
      SELECT
        date,
        revenue,
        SUM(revenue) OVER (
          ORDER BY date
          ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) as rolling_7day
      FROM table

  # Common Table Expressions (CTE)
  - type: sql
    query: |
      WITH monthly_summary AS (
        SELECT
          DATE_TRUNC('month', date) as month,
          region,
          SUM(revenue) as revenue
        FROM table
        GROUP BY month, region
      )
      SELECT
        month,
        region,
        revenue,
        revenue - LAG(revenue) OVER (
          PARTITION BY region
          ORDER BY month
        ) as growth
      FROM monthly_summary

  # Subqueries
  - type: sql
    query: |
      SELECT *
      FROM table
      WHERE revenue > (
        SELECT AVG(revenue) FROM table
      )
```

### SQL with Parameters

```yaml
transforms:
  # Use filter values in SQL
  - type: sql
    query: |
      SELECT *
      FROM table
      WHERE region = :region
      AND date >= :start_date
      AND date <= :end_date
```

## Data Manipulation

### Sort Transform

```yaml
transforms:
  # Sort by single column
  - type: sort
    by: date
    ascending: false  # Descending

  # Sort by multiple columns
  - type: sort
    by: ['region', 'revenue']
    ascending: [true, false]  # Region asc, revenue desc
```

### Type Conversion

```yaml
transforms:
  # Convert data types
  - type: astype
    dtypes:
      date: datetime64
      customer_id: str
      revenue: float
      quantity: int
```

### Missing Data

```yaml
transforms:
  # Drop null values
  - type: dropna
    subset: ['revenue', 'customer_id']  # Columns to check

  # Fill null values
  - type: fillna
    values:
      revenue: 0
      category: 'Unknown'
      quantity: 1

  # Forward fill
  - type: fillna
    method: 'ffill'  # Forward fill

  # Backward fill
  - type: fillna
    method: 'bfill'  # Backward fill
```

### Rename Columns

```yaml
transforms:
  - type: rename
    columns:
      old_name: new_name
      rev: revenue
      qty: quantity
      cust_id: customer_id
```

### Row Selection

```yaml
transforms:
  # Get first N rows
  - type: head
    n: 100

  # Get last N rows
  - type: tail
    n: 50

  # Get rows by position
  - type: iloc
    start: 0
    end: 1000
```

## Custom Transforms

### Python Function Transform

```python
# custom_transforms.py
from lumen.transforms import Transform
import pandas as pd

class CustomTransform(Transform):
    """Custom data transformation."""

    transform_type = 'custom'

    parameter1 = param.String(default='value')

    def apply(self, table):
        """Apply transformation to table."""
        # Your custom logic here
        table['new_column'] = table['existing'].apply(lambda x: x * 2)
        return table
```

**dashboard.yaml**:
```yaml
transforms:
  - type: custom
    module: custom_transforms
    parameter1: 'custom_value'
```

## Transform Patterns

### Pattern 1: Data Cleaning Pipeline

```yaml
transforms:
  # Step 1: Select relevant columns
  - type: columns
    columns: ['date', 'region', 'category', 'revenue', 'quantity']

  # Step 2: Remove nulls
  - type: dropna
    subset: ['revenue', 'date']

  # Step 3: Filter outliers
  - type: query
    query: "revenue > 0 and revenue < 1000000"

  # Step 4: Convert types
  - type: astype
    dtypes:
      date: datetime64
      revenue: float

  # Step 5: Sort
  - type: sort
    by: date
    ascending: true
```

### Pattern 2: Aggregation Pipeline

```yaml
transforms:
  # Step 1: Filter data
  - type: query
    query: "status == 'completed'"

  # Step 2: Aggregate
  - type: aggregate
    by: ['region', 'category']
    aggregate:
      total_revenue: {revenue: sum}
      order_count: {order_id: count}
      avg_order_value: {revenue: mean}

  # Step 3: Calculate metrics
  - type: sql
    query: |
      SELECT
        *,
        total_revenue / order_count as avg_per_order,
        total_revenue / SUM(total_revenue) OVER () as pct_of_total
      FROM table
```

### Pattern 3: Time Series Processing

```yaml
transforms:
  # Step 1: Ensure date sorted
  - type: sort
    by: date

  # Step 2: Create time features
  - type: sql
    query: |
      SELECT
        *,
        DATE_TRUNC('month', date) as month,
        DATE_TRUNC('week', date) as week,
        EXTRACT(YEAR FROM date) as year,
        EXTRACT(QUARTER FROM date) as quarter
      FROM table

  # Step 3: Calculate rolling metrics
  - type: sql
    query: |
      SELECT
        *,
        AVG(revenue) OVER (
          ORDER BY date
          ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) as rolling_7day_avg
      FROM table
```

### Pattern 4: Join Pattern (via SQL)

```yaml
pipelines:
  # Main pipeline with transform
  sales_with_categories:
    source: sales_db
    table: sales

    transforms:
      - type: sql
        query: |
          SELECT
            s.*,
            c.category_name,
            c.category_group
          FROM sales s
          LEFT JOIN categories c
            ON s.category_id = c.id
```

## Advanced Patterns

### Conditional Logic

```yaml
transforms:
  # Add calculated columns
  - type: sql
    query: |
      SELECT
        *,
        CASE
          WHEN revenue < 1000 THEN 'Small'
          WHEN revenue < 10000 THEN 'Medium'
          ELSE 'Large'
        END as revenue_category,

        CASE
          WHEN quantity > 0 THEN revenue / quantity
          ELSE 0
        END as unit_price
      FROM table
```

### Percentile Calculations

```yaml
transforms:
  - type: sql
    query: |
      SELECT
        *,
        PERCENT_RANK() OVER (ORDER BY revenue) as revenue_percentile,
        NTILE(10) OVER (ORDER BY revenue) as revenue_decile
      FROM table
```

### Pivot Operations

```yaml
transforms:
  - type: sql
    query: |
      SELECT
        date,
        SUM(CASE WHEN region = 'North' THEN revenue ELSE 0 END) as north_revenue,
        SUM(CASE WHEN region = 'South' THEN revenue ELSE 0 END) as south_revenue,
        SUM(CASE WHEN region = 'East' THEN revenue ELSE 0 END) as east_revenue,
        SUM(CASE WHEN region = 'West' THEN revenue ELSE 0 END) as west_revenue
      FROM table
      GROUP BY date
```

## Troubleshooting

### Query Syntax Errors

```yaml
# Problem: Query fails
# Solution: Check pandas query syntax

transforms:
  # ✅ Good: Correct syntax
  - type: query
    query: "revenue > 1000 and category == 'A'"

  # ❌ Bad: Wrong operators
  - type: query
    query: "revenue > 1000 AND category = 'A'"  # Use 'and' and '=='
```

### SQL Errors

```yaml
# Problem: SQL query fails
# Solution: Verify SQL syntax for your database

transforms:
  # Check table name is 'table'
  - type: sql
    query: |
      SELECT * FROM table  -- 'table' is the keyword for current data

  # Use correct SQL dialect (PostgreSQL, DuckDB, etc.)
```

### Null Handling

```yaml
# Problem: Nulls causing issues
# Solution: Handle explicitly

transforms:
  # Option 1: Drop nulls
  - type: dropna
    subset: ['critical_column']

  # Option 2: Fill nulls
  - type: fillna
    values:
      column: 0

  # Option 3: Filter in query
  - type: query
    query: "column.notna()"
```

## Best Practices

### 1. Transform Order Matters

```yaml
# ✅ Good: Filter before aggregate
transforms:
  - type: query
    query: "status == 'active'"  # Filter first (fewer rows)

  - type: aggregate
    by: ['region']
    aggregate:
      total: {revenue: sum}

# ❌ Bad: Aggregate before filter
transforms:
  - type: aggregate
    by: ['region', 'status']
    aggregate:
      total: {revenue: sum}

  - type: query
    query: "status == 'active'"  # Filter after (wasted computation)
```

### 2. Use SQL for Complex Logic

```yaml
# ✅ Good: Single SQL transform
transforms:
  - type: sql
    query: |
      SELECT
        region,
        SUM(revenue) as total,
        COUNT(*) as count,
        AVG(revenue) as avg
      FROM table
      WHERE status = 'active'
      GROUP BY region

# ❌ Bad: Multiple transforms
transforms:
  - type: query
    query: "status == 'active'"
  - type: aggregate
    by: ['region']
    aggregate:
      total: {revenue: sum}
      count: {id: count}
      avg: {revenue: mean}
```

### 3. Minimize Data Early

```yaml
# ✅ Good: Filter and select columns early
transforms:
  - type: query
    query: "date >= '2024-01-01'"

  - type: columns
    columns: ['date', 'region', 'revenue']

  # ... further processing
```

## Summary

**Key concepts**:
- Chain transforms in pipelines
- Use `query` for filtering
- Use `aggregate` for grouping
- Use `sql` for complex operations
- Transform order affects performance

**Most common transforms**:
- `query`: Filter rows
- `aggregate`: Group and aggregate
- `sql`: Complex SQL queries
- `columns`: Select columns
- `sort`: Order data

**Best practices**:
- Filter early to reduce data size
- Use SQL for complex logic
- Handle nulls explicitly
- Test transforms incrementally
- Minimize data before aggregation

## References

- [Lumen Transforms Documentation](https://lumen.holoviz.org/user_guide/Transforms.html)
- [Pandas Query Syntax](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.query.html)
- [SQL Tutorial](https://www.w3schools.com/sql/)
- [DuckDB SQL Reference](https://duckdb.org/docs/sql/introduction)
