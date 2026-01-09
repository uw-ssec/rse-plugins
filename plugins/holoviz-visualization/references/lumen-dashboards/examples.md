# Lumen Dashboard Examples

## Overview

Complete, ready-to-use Lumen dashboard examples for common use cases.

**When to use this reference**:
- Starting a new dashboard
- Looking for best practice patterns
- Understanding complete implementations

## Table of Contents

1. [Simple Data Explorer](#simple-data-explorer)
2. [KPI Dashboard](#kpi-dashboard)
3. [Sales Analytics](#sales-analytics)
4. [Multi-Source Dashboard](#multi-source-dashboard)
5. [Real-Time Monitoring](#real-time-monitoring)

## Simple Data Explorer

### Basic CSV Dashboard

```yaml
# dashboard.yaml
config:
  title: Data Explorer
  theme: default

sources:
  data:
    type: file
    tables:
      penguins: https://datasets.holoviz.org/penguins/v1/penguins.csv

pipelines:
  main:
    source: data
    table: penguins

    filters:
      - type: widget
        field: species

      - type: widget
        field: island

layouts:
  - title: Explorer
    views:
      - type: hvplot
        pipeline: main
        kind: scatter
        x: bill_length_mm
        y: bill_depth_mm
        by: species
        title: Bill Dimensions
        width: 600
        height: 400

      - type: table
        pipeline: main
        page_size: 20
```

## KPI Dashboard

### Executive Dashboard

```yaml
# kpi_dashboard.yaml
config:
  title: Executive Dashboard
  theme: material

sources:
  sales_db:
    type: postgres
    connection_string: ${DATABASE_URL}
    tables:
      sales: |
        SELECT * FROM sales
        WHERE date >= CURRENT_DATE - INTERVAL '90 days'

pipelines:
  # KPI metrics
  metrics:
    source: sales_db
    table: sales

    transforms:
      - type: aggregate
        aggregate:
          total_revenue: {revenue: sum}
          total_orders: {order_id: count}
          avg_order_value: {revenue: mean}

  # Trend data
  trend:
    source: sales_db
    table: sales

    filters:
      - type: widget
        field: region

    transforms:
      - type: sql
        query: |
          SELECT
            DATE_TRUNC('day', date) as date,
            SUM(revenue) as daily_revenue
          FROM table
          GROUP BY date
          ORDER BY date

  # Regional breakdown
  regional:
    source: sales_db
    table: sales

    transforms:
      - type: aggregate
        by: ['region']
        aggregate:
          revenue: {revenue: sum}
          orders: {order_id: count}

layouts:
  - title: Overview
    layout: [[0, 1, 2], [3], [4]]
    views:
      # KPI cards
      - type: indicator
        pipeline: metrics
        field: total_revenue
        title: Total Revenue
        format: '${value:,.0f}'

      - type: indicator
        pipeline: metrics
        field: total_orders
        title: Total Orders
        format: '{value:,d}'

      - type: indicator
        pipeline: metrics
        field: avg_order_value
        title: Avg Order Value
        format: '${value:.2f}'

      # Trend chart
      - type: hvplot
        pipeline: trend
        kind: line
        x: date
        y: daily_revenue
        title: Daily Revenue Trend
        responsive: true

      # Regional breakdown
      - type: hvplot
        pipeline: regional
        kind: bar
        x: region
        y: revenue
        title: Revenue by Region
        responsive: true
```

## Sales Analytics

### Multi-Tab Sales Dashboard

```yaml
# sales_dashboard.yaml
config:
  title: Sales Analytics
  theme: dark

sources:
  data:
    type: file
    tables:
      sales: ./data/sales.csv
      products: ./data/products.csv
      customers: ./data/customers.csv

pipelines:
  # Main sales pipeline
  sales:
    source: data
    table: sales

    filters:
      - type: widget
        field: region
        label: Region

      - type: widget
        field: category
        label: Category
        multiple: true

      - type: widget
        field: date
        widget: date_range_slider
        label: Date Range

    transforms:
      - type: astype
        dtypes:
          date: datetime64

  # Product analysis
  products:
    source: data
    table: sales

    transforms:
      - type: aggregate
        by: ['product_name']
        aggregate:
          revenue: {revenue: sum}
          quantity: {quantity: sum}

      - type: sort
        by: revenue
        ascending: false

      - type: head
        n: 10

  # Customer segments
  customers:
    source: data
    table: sales

    transforms:
      - type: aggregate
        by: ['customer_id']
        aggregate:
          total_spent: {revenue: sum}
          order_count: {order_id: count}

      - type: sql
        query: |
          SELECT
            CASE
              WHEN total_spent < 1000 THEN 'Bronze'
              WHEN total_spent < 5000 THEN 'Silver'
              ELSE 'Gold'
            END as segment,
            COUNT(*) as customer_count,
            SUM(total_spent) as segment_revenue
          FROM table
          GROUP BY segment

layouts:
  # Tab 1: Overview
  - title: Overview
    layout: [[0, 1], [2, 3]]
    views:
      - type: hvplot
        pipeline: sales
        kind: line
        x: date
        y: revenue
        title: Revenue Over Time
        responsive: true

      - type: hvplot
        pipeline: sales
        kind: bar
        x: region
        y: revenue
        title: Revenue by Region

      - type: hvplot
        pipeline: sales
        kind: box
        y: revenue
        by: category
        title: Revenue Distribution

      - type: indicator
        pipeline: sales
        field: revenue
        title: Total Revenue
        format: '${value:,.0f}'

  # Tab 2: Products
  - title: Products
    views:
      - type: hvplot
        pipeline: products
        kind: bar
        x: product_name
        y: revenue
        title: Top 10 Products by Revenue
        rot: 45
        responsive: true

      - type: table
        pipeline: products
        page_size: 10
        formatters:
          revenue: '${value:,.2f}'
          quantity: '{value:,d}'

  # Tab 3: Customers
  - title: Customers
    views:
      - type: hvplot
        pipeline: customers
        kind: bar
        x: segment
        y: customer_count
        title: Customer Segmentation

      - type: hvplot
        pipeline: customers
        kind: bar
        x: segment
        y: segment_revenue
        title: Revenue by Segment
```

## Multi-Source Dashboard

### Combined File + Database Dashboard

```yaml
# multi_source.yaml
config:
  title: Analytics Dashboard

sources:
  # Reference data from files
  reference:
    type: file
    tables:
      categories: ./data/categories.csv
      regions: ./data/regions.csv

  # Transactional data from database
  transactions:
    type: postgres
    connection_string: ${DATABASE_URL}
    cache: true
    cache_timeout: 300
    tables:
      orders: |
        SELECT * FROM orders
        WHERE date >= CURRENT_DATE - INTERVAL '30 days'

  # External API data
  external:
    type: rest
    url: https://api.example.com/metrics
    headers:
      Authorization: Bearer ${API_TOKEN}
    tables:
      metrics: $.data

pipelines:
  orders:
    source: transactions
    table: orders

    filters:
      - type: widget
        field: status

    transforms:
      - type: sql
        query: |
          SELECT
            *,
            revenue - cost as profit,
            revenue / NULLIF(quantity, 0) as unit_price
          FROM table

  summary:
    source: transactions
    table: orders

    transforms:
      - type: aggregate
        by: ['category']
        aggregate:
          total_revenue: {revenue: sum}
          total_profit: {profit: sum}
          order_count: {order_id: count}

layouts:
  - title: Dashboard
    views:
      - type: hvplot
        pipeline: summary
        kind: bar
        x: category
        y: total_revenue
        title: Revenue by Category

      - type: table
        pipeline: orders
        page_size: 20
```

## Real-Time Monitoring

### Live Metrics Dashboard

```yaml
# monitoring.yaml
config:
  title: System Monitoring
  theme: dark

sources:
  metrics:
    type: postgres
    connection_string: ${DATABASE_URL}
    refresh_rate: 30  # Refresh every 30 seconds
    tables:
      live_metrics: |
        SELECT *
        FROM system_metrics
        WHERE timestamp >= NOW() - INTERVAL '1 hour'
        ORDER BY timestamp DESC

pipelines:
  latest:
    source: metrics
    table: live_metrics

    transforms:
      - type: head
        n: 1  # Latest value

  historical:
    source: metrics
    table: live_metrics

    transforms:
      - type: sql
        query: |
          SELECT
            DATE_TRUNC('minute', timestamp) as minute,
            AVG(cpu_usage) as avg_cpu,
            AVG(memory_usage) as avg_memory,
            AVG(requests_per_sec) as avg_requests
          FROM table
          GROUP BY minute
          ORDER BY minute

layouts:
  - title: Live Metrics
    layout: [[0, 1, 2], [3]]
    views:
      # Current values
      - type: indicator
        pipeline: latest
        field: cpu_usage
        title: CPU Usage
        format: '{value:.1f}%'
        colors: [[50, 'green'], [75, 'orange'], [100, 'red']]

      - type: indicator
        pipeline: latest
        field: memory_usage
        title: Memory Usage
        format: '{value:.1f}%'
        colors: [[50, 'green'], [75, 'orange'], [100, 'red']]

      - type: indicator
        pipeline: latest
        field: requests_per_sec
        title: Requests/sec
        format: '{value:,.0f}'

      # Historical trends
      - type: hvplot
        pipeline: historical
        kind: line
        x: minute
        y: ['avg_cpu', 'avg_memory']
        title: System Usage Over Time
        legend: top_right
        responsive: true
```

## Complete Example with All Features

```yaml
# complete_dashboard.yaml
config:
  title: Complete Dashboard
  theme: material
  logo: ./assets/logo.png
  favicon: ./assets/favicon.ico

sources:
  database:
    type: postgres
    connection_string: ${DATABASE_URL}
    cache: true
    cache_dir: ./cache
    cache_timeout: 600
    pool_size: 10
    tables:
      sales: |
        SELECT
          s.*,
          c.customer_name,
          c.segment,
          p.product_name,
          p.category
        FROM sales s
        LEFT JOIN customers c ON s.customer_id = c.id
        LEFT JOIN products p ON s.product_id = p.id
        WHERE s.date >= CURRENT_DATE - INTERVAL '1 year'

pipelines:
  main:
    source: database
    table: sales

    filters:
      - type: widget
        field: segment
        label: Customer Segment

      - type: widget
        field: category
        label: Product Category
        multiple: true

      - type: widget
        field: date
        widget: date_range_slider
        label: Date Range

    transforms:
      - type: query
        query: "status == 'completed'"

  metrics:
    pipeline: main

    transforms:
      - type: aggregate
        aggregate:
          total_revenue: {revenue: sum}
          total_orders: {order_id: count}
          avg_order_value: {revenue: mean}
          total_customers: {customer_id: nunique}

  trend:
    pipeline: main

    transforms:
      - type: sql
        query: |
          SELECT
            DATE_TRUNC('month', date) as month,
            SUM(revenue) as revenue,
            COUNT(DISTINCT customer_id) as customers
          FROM table
          GROUP BY month
          ORDER BY month

  top_products:
    pipeline: main

    transforms:
      - type: aggregate
        by: ['product_name', 'category']
        aggregate:
          revenue: {revenue: sum}
          quantity: {quantity: sum}

      - type: sort
        by: revenue
        ascending: false

      - type: head
        n: 10

layouts:
  # Tab 1: Executive Summary
  - title: Summary
    layout: [[0, 1, 2, 3], [4], [5, 6]]
    views:
      # KPIs
      - type: indicator
        pipeline: metrics
        field: total_revenue
        title: Total Revenue
        format: '${value:,.0f}'

      - type: indicator
        pipeline: metrics
        field: total_orders
        title: Total Orders
        format: '{value:,d}'

      - type: indicator
        pipeline: metrics
        field: avg_order_value
        title: Avg Order Value
        format: '${value:.2f}'

      - type: indicator
        pipeline: metrics
        field: total_customers
        title: Unique Customers
        format: '{value:,d}'

      # Trend
      - type: hvplot
        pipeline: trend
        kind: line
        x: month
        y: revenue
        title: Monthly Revenue Trend
        responsive: true

      # Top products
      - type: hvplot
        pipeline: top_products
        kind: bar
        x: product_name
        y: revenue
        by: category
        title: Top 10 Products
        rot: 45
        width: 600

      # Regional breakdown
      - type: hvplot
        pipeline: main
        kind: bar
        x: region
        y: revenue
        title: Revenue by Region
        width: 600

  # Tab 2: Details
  - title: Details
    views:
      - type: table
        pipeline: main
        page_size: 50
        pagination: remote
        selectable: true
        formatters:
          revenue: '${value:,.2f}'
          date: '{value:%Y-%m-%d}'
```

## Summary

**Example dashboards**:
- Simple Data Explorer: Basic CSV exploration
- KPI Dashboard: Executive metrics
- Sales Analytics: Multi-tab analysis
- Multi-Source Dashboard: Combined data sources
- Real-Time Monitoring: Live metrics

**Common patterns**:
- Filters for interactivity
- KPI indicators for metrics
- Charts for trends and comparisons
- Tables for detailed data
- Tabs for organization

## References

- [Lumen Gallery](https://lumen.holoviz.org/gallery/)
- [Panel Examples](https://panel.holoviz.org/gallery/index.html)
