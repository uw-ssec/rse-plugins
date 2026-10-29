# Lumen Data Sources Reference

## Overview

Complete reference for configuring data sources in Lumen dashboards. Covers files, databases, APIs, and custom sources.

**When to use this reference**:
- Connecting to data sources
- Configuring database connections
- Setting up API data sources
- Understanding source options

## Table of Contents

1. [File Sources](#file-sources)
2. [Database Sources](#database-sources)
3. [API Sources](#api-sources)
4. [Intake Catalogs](#intake-catalogs)
5. [Custom Sources](#custom-sources)
6. [Source Configuration](#source-configuration)

## File Sources

### CSV Files

```yaml
sources:
  csv_data:
    type: file
    tables:
      sales: ./data/sales.csv
      customers: ./data/customers.csv

    # Optional: CSV reading options
    kwargs:
      parse_dates: ['date']
      dtype:
        customer_id: str
      encoding: 'utf-8'
```

### Parquet Files

**Recommended for large datasets** - faster loading and smaller size:

```yaml
sources:
  parquet_data:
    type: file
    tables:
      large_dataset: ./data/large_dataset.parquet

    # Optional: Parquet options
    kwargs:
      engine: 'pyarrow'  # or 'fastparquet'
      columns: ['col1', 'col2', 'col3']  # Load specific columns
```

### Excel Files

```yaml
sources:
  excel_data:
    type: file
    tables:
      sales: ./data/sales.xlsx

    # Optional: Excel options
    kwargs:
      sheet_name: 'Sales Data'  # Specific sheet
      header: 0
      skiprows: 2
```

### JSON Files

```yaml
sources:
  json_data:
    type: file
    tables:
      config: ./data/config.json

    # Optional: JSON options
    kwargs:
      orient: 'records'  # or 'split', 'index', 'columns'
```

### Remote Files

```yaml
sources:
  remote_data:
    type: file
    tables:
      penguins: https://datasets.holoviz.org/penguins/v1/penguins.csv
      iris: https://datasets.holoviz.org/iris/v1/iris.csv
```

### File Source Options

```yaml
sources:
  files:
    type: file
    tables:
      data: ./data/file.csv

    # Common options
    kwargs:
      # CSV options
      sep: ','              # Delimiter
      header: 0             # Header row
      names: ['a', 'b']     # Column names
      parse_dates: ['date'] # Parse dates
      dtype: {...}          # Data types
      encoding: 'utf-8'     # File encoding
      nrows: 1000           # Limit rows

      # Parquet options
      engine: 'pyarrow'
      columns: [...]        # Specific columns

      # Excel options
      sheet_name: 'Sheet1'
      skiprows: 0
```

## Database Sources

### PostgreSQL

```yaml
sources:
  postgres:
    type: postgres
    connection_string: postgresql://user:password@localhost:5432/dbname

    # Option 1: List tables
    tables: [sales, customers, products]

    # Option 2: Custom queries
    tables:
      sales: SELECT * FROM sales WHERE date >= '2024-01-01'
      summary: |
        SELECT
          region,
          SUM(revenue) as total_revenue
        FROM sales
        GROUP BY region

    # Optional: Connection pool settings
    pool_size: 5
    max_overflow: 10
```

### DuckDB

**Recommended for analytics** - fast SQL on files:

```yaml
sources:
  duckdb:
    type: duckdb
    uri: ./data/analytics.duckdb

    # Or connect to files directly
    tables:
      sales: SELECT * FROM read_csv_auto('./data/sales.csv')
      parquet_data: SELECT * FROM read_parquet('./data/*.parquet')

    # Advanced: Run initialization SQL
    init_sql: |
      CREATE TABLE IF NOT EXISTS summary AS
      SELECT region, COUNT(*) as count
      FROM sales
      GROUP BY region;
```

### SQLite

```yaml
sources:
  sqlite:
    type: sqlite
    uri: ./data/app.db

    tables:
      users: SELECT * FROM users
      logs: SELECT * FROM logs WHERE date >= date('now', '-7 days')
```

### MySQL/MariaDB

```yaml
sources:
  mysql:
    type: mysql
    connection_string: mysql+pymysql://user:password@localhost:3306/dbname

    tables: [orders, customers]
```

### Microsoft SQL Server

```yaml
sources:
  mssql:
    type: mssql
    connection_string: mssql+pyodbc://user:password@localhost:1433/dbname?driver=ODBC+Driver+17+for+SQL+Server

    tables: [sales, inventory]
```

### Environment Variables

**Best practice for credentials**:

```yaml
sources:
  postgres:
    type: postgres
    connection_string: ${DATABASE_URL}  # From environment variable

    tables: [sales, customers]
```

```bash
# Set environment variable
export DATABASE_URL="postgresql://user:password@localhost:5432/dbname"
```

### Database Configuration Options

```yaml
sources:
  db:
    type: postgres
    connection_string: postgresql://...

    # Connection pool
    pool_size: 5
    max_overflow: 10
    pool_recycle: 3600

    # Query options
    chunksize: 10000      # Fetch in chunks
    cache_dir: ./cache    # Cache query results

    # Tables
    tables:
      # Simple table
      simple: table_name

      # Custom query
      custom: SELECT * FROM table WHERE condition

      # Parameterized query (use with filters)
      filtered: |
        SELECT * FROM sales
        WHERE region = :region
        AND date >= :start_date
```

## API Sources

### REST API (JSON)

```yaml
sources:
  api:
    type: rest
    url: https://api.example.com/data

    # Optional: Authentication
    headers:
      Authorization: Bearer ${API_TOKEN}
      Content-Type: application/json

    # Query parameters
    params:
      format: json
      limit: 1000

    # Response parsing
    tables:
      data: $.results[*]  # JSONPath expression
```

### GraphQL API

```yaml
sources:
  graphql:
    type: graphql
    url: https://api.example.com/graphql

    headers:
      Authorization: Bearer ${API_TOKEN}

    tables:
      users: |
        query {
          users {
            id
            name
            email
          }
        }
```

### Custom HTTP Source

```yaml
sources:
  custom_api:
    type: rest
    url: https://api.example.com/endpoint

    # HTTP method
    method: POST

    # Request body
    body:
      query: "SELECT * FROM data"
      format: "json"

    # Response parsing
    tables:
      data: $.data.results
```

## Intake Catalogs

### Intake Source

**Best for managing multiple data sources**:

```yaml
sources:
  catalog:
    type: intake
    uri: ./data/catalog.yaml

    # Use sources from catalog
    tables: [dataset1, dataset2]
```

**catalog.yaml**:
```yaml
sources:
  dataset1:
    driver: csv
    args:
      urlpath: ./data/dataset1.csv

  dataset2:
    driver: parquet
    args:
      urlpath: ./data/dataset2.parquet
```

## Custom Sources

### Python Class Source

```python
# custom_source.py
from lumen.sources import Source
import pandas as pd

class CustomSource(Source):
    """Custom data source."""

    source_type = 'custom'

    def get_table(self, table_name):
        """Load table data."""
        if table_name == 'data':
            return pd.read_csv(f'./data/{table_name}.csv')
        raise ValueError(f"Unknown table: {table_name}")

    def get_tables(self):
        """Return available tables."""
        return ['data', 'other']
```

**dashboard.yaml**:
```yaml
sources:
  custom:
    type: custom
    module: custom_source  # Python module name
    tables: [data, other]
```

## Source Configuration

### Shared Configuration

```yaml
sources:
  # Multiple file sources
  files:
    type: file
    tables:
      sales: ./data/sales.csv
      customers: ./data/customers.csv

  # Database source
  database:
    type: postgres
    connection_string: ${DATABASE_URL}
    tables: [orders, products]

  # API source
  api:
    type: rest
    url: https://api.example.com/data
    tables:
      live_data: $.results
```

### Source Reuse

```yaml
sources:
  base_db:
    type: postgres
    connection_string: ${DATABASE_URL}

pipelines:
  pipeline1:
    source: base_db
    table: sales

  pipeline2:
    source: base_db
    table: customers
```

### Caching

```yaml
sources:
  cached_data:
    type: file
    tables:
      large_data: ./data/large.parquet

    # Enable caching
    cache: true
    cache_dir: ./cache
    cache_timeout: 3600  # Seconds
```

### Auto-refresh

```yaml
sources:
  live_data:
    type: postgres
    connection_string: ${DATABASE_URL}
    tables: [live_metrics]

    # Auto-refresh every 60 seconds
    refresh_rate: 60
```

## Common Patterns

### Pattern 1: Multi-File Source

```yaml
sources:
  data_files:
    type: file
    tables:
      sales_2023: ./data/sales_2023.csv
      sales_2024: ./data/sales_2024.csv
      customers: ./data/customers.csv
      products: ./data/products.csv

pipelines:
  sales:
    source: data_files
    table: sales_2024
```

### Pattern 2: Database with SQL

```yaml
sources:
  analytics_db:
    type: postgres
    connection_string: ${DATABASE_URL}

    tables:
      # Direct table
      raw_sales: sales

      # Aggregated query
      daily_summary: |
        SELECT
          date,
          region,
          SUM(revenue) as total_revenue,
          COUNT(*) as order_count
        FROM sales
        GROUP BY date, region
        ORDER BY date DESC

      # Filtered query
      recent_sales: |
        SELECT *
        FROM sales
        WHERE date >= CURRENT_DATE - INTERVAL '30 days'
```

### Pattern 3: Mixed Sources

```yaml
sources:
  # CSV files for reference data
  reference:
    type: file
    tables:
      categories: ./data/categories.csv
      regions: ./data/regions.csv

  # Database for transactional data
  transactions:
    type: postgres
    connection_string: ${DATABASE_URL}
    tables: [orders, payments]

  # API for external data
  external:
    type: rest
    url: https://api.example.com/rates
    tables:
      exchange_rates: $.rates

pipelines:
  # Use reference data
  categories_pipeline:
    source: reference
    table: categories

  # Use transactional data
  orders_pipeline:
    source: transactions
    table: orders

  # Use external data
  rates_pipeline:
    source: external
    table: exchange_rates
```

### Pattern 4: DuckDB Analytics

```yaml
sources:
  duckdb_analytics:
    type: duckdb
    uri: ':memory:'  # In-memory database

    tables:
      # Read CSV files
      sales: SELECT * FROM read_csv_auto('./data/sales_*.csv')

      # Read Parquet with glob
      logs: SELECT * FROM read_parquet('./data/logs/**/*.parquet')

      # Aggregate on the fly
      summary: |
        SELECT
          strftime(date, '%Y-%m') as month,
          region,
          SUM(revenue) as revenue
        FROM read_csv_auto('./data/sales.csv')
        GROUP BY month, region
```

## Troubleshooting

### Connection Errors

```yaml
# Problem: Can't connect to database
# Solution: Check connection string format

sources:
  postgres:
    type: postgres
    # Correct format
    connection_string: postgresql://user:password@host:5432/database

    # Test connection
    tables: [test_table]
```

### File Not Found

```yaml
# Problem: File path not found
# Solution: Use absolute paths or check working directory

sources:
  files:
    type: file
    tables:
      # Relative path (from dashboard.yaml location)
      data: ./data/file.csv

      # Absolute path
      data2: /full/path/to/file.csv

      # URL
      data3: https://example.com/data.csv
```

### Memory Issues

```yaml
# Problem: Large file causes memory issues
# Solution: Use Parquet or chunked loading

sources:
  large_data:
    type: file
    tables:
      # Convert to Parquet first (more efficient)
      data: ./data/large.parquet

    # Or use database with chunked queries
  db:
    type: postgres
    connection_string: ${DATABASE_URL}
    chunksize: 10000  # Load in chunks
```

### Authentication

```yaml
# Problem: API authentication required
# Solution: Use headers and environment variables

sources:
  api:
    type: rest
    url: https://api.example.com/data

    headers:
      Authorization: Bearer ${API_TOKEN}

    tables:
      data: $.results
```

```bash
# Set token
export API_TOKEN="your_token_here"
```

## Best Practices

### 1. Use Environment Variables

```yaml
# ✅ Good: Credentials in environment
sources:
  db:
    type: postgres
    connection_string: ${DATABASE_URL}

# ❌ Bad: Credentials in YAML
sources:
  db:
    type: postgres
    connection_string: postgresql://user:password123@host/db
```

### 2. Optimize Data Format

```yaml
# ✅ Good: Use Parquet for large data
sources:
  data:
    type: file
    tables:
      large: ./data/large.parquet  # Fast, compressed

# ❌ Bad: CSV for large data
sources:
  data:
    type: file
    tables:
      large: ./data/large.csv  # Slow, large file
```

### 3. Use SQL for Filtering

```yaml
# ✅ Good: Filter in database
sources:
  db:
    type: postgres
    connection_string: ${DATABASE_URL}
    tables:
      recent: |
        SELECT * FROM sales
        WHERE date >= CURRENT_DATE - INTERVAL '30 days'

# ❌ Bad: Load all data then filter
sources:
  db:
    type: postgres
    connection_string: ${DATABASE_URL}
    tables: [sales]  # Loads entire table

pipelines:
  recent:
    source: db
    table: sales
    transforms:
      - type: query
        query: "date >= @start_date"  # Filters after loading
```

### 4. Enable Caching

```yaml
# ✅ Good: Cache expensive queries
sources:
  db:
    type: postgres
    connection_string: ${DATABASE_URL}
    cache: true
    cache_dir: ./cache
    cache_timeout: 3600
```

## Summary

**Key concepts**:
- Multiple source types: files, databases, APIs
- Use environment variables for credentials
- Optimize with Parquet format
- Filter data at source when possible
- Enable caching for expensive queries

**Most common sources**:
- **File**: CSV, Parquet, Excel
- **Database**: PostgreSQL, DuckDB, SQLite
- **API**: REST JSON endpoints

**Best practices**:
- Secure credentials with environment variables
- Use Parquet for large datasets
- Filter at database level
- Enable caching for slow sources
- Test connection strings

## References

- [Lumen Sources Documentation](https://lumen.holoviz.org/user_guide/Sources.html)
- [Pandas I/O](https://pandas.pydata.org/docs/user_guide/io.html)
- [SQLAlchemy Connection Strings](https://docs.sqlalchemy.org/en/14/core/engines.html)
- [Intake Catalogs](https://intake.readthedocs.io/)
