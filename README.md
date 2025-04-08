# OmniStream: Multi-source Data Engineering Pipeline

![OmniStream Logo](logo.svg)

## Project Overview

OmniStream is a sophisticated data engineering platform designed to process, monitor, and analyze real-time data from multiple sources. The platform features automated data quality controls, anomaly detection, and comprehensive dashboards for monitoring pipeline performance.

### Key Features

- **Real-time Data Processing**: Ingest and process data from multiple sources with low latency
- **Automated Quality Controls**: Continuously monitor data quality and detect anomalies
- **Interactive Dashboards**: Visualize pipeline performance and data insights
- **Multi-stage Processing**: Implement a complete data engineering workflow from ingestion to analysis
- **Scalable Architecture**: Designed to handle growing data volumes across diverse sources

## Dashboard Components

The application features four main dashboard tabs:

### 1. Pipeline Dashboard

The main monitoring interface that provides a real-time overview of the entire data pipeline, including:

- **System Status Cards**: Visual indicators of active data sources, records processed, processing latency, and data quality
- **Data Source Status Table**: Detailed status of each connected data source including processing metrics
- **Recent Alerts & Events**: Timeline of system activities and issues requiring attention
- **Throughput Chart**: Time-series visualization of data volume processed over time

![Pipeline Dashboard](docs/images/pipeline_dashboard.png)

### 2. Data Quality Metrics

Comprehensive visualization of data quality across the system:

- **Quality Score Metrics**: Overall quality metrics with breakdown of violations and incidents
- **Quality Trend Chart**: Dual-axis visualization showing quality score and error rate over time
- **Automated Data Quality Rules**: Table of configured quality validation rules with severity and status
- **Data Enrichment Processes**: Details of the enrichment processes applied to incoming data

![Data Quality](docs/images/data_quality.png)

### 3. Pipeline Demo

Interactive demonstration of the complete pipeline process:

- **Pipeline Architecture Diagram**: Visual representation of the data flow through the system
- **Step-by-step Execution**: Interactive walkthrough of each pipeline stage with real-time metrics
- **Technical Implementation Examples**: Code snippets showing how key components are implemented
- **Progress Visualization**: Real-time tracking of pipeline execution

![Pipeline Demo](docs/images/pipeline_demo.png)

### 4. Performance Analytics

Detailed performance metrics with sophisticated visualizations:

- **Enhanced Performance Dashboard**: Multi-tab interface for in-depth analysis
- **Latency Metrics**: Processing time analysis across different pipeline stages
- **Throughput Analysis**: Visualizations of data volume patterns and distribution
- **Resource Utilization**: System resource consumption monitoring
- **Error Tracking**: Detailed error rate analysis with breakdowns by type and source
- **Optimization Recommendations**: Actionable insights for improving pipeline performance

![Performance Analytics](docs/images/performance_analytics.png)

## Visualization Types

The platform includes a variety of advanced data visualizations:

1. **Time-series Line Charts**: Track metrics like latency, throughput, and error rates over time
2. **Area Charts**: Visualize cumulative metrics like total records processed
3. **Bar Charts**: Compare metrics across different data sources or processing stages
4. **Donut Charts**: Show distribution of data volume or errors by category
5. **Stacked Bar Charts**: Display composite metrics with component breakdowns
6. **Heat Maps**: Visualize patterns in hourly or daily processing volumes
7. **Grouped Bar Charts**: Compare multiple metrics across different dimensions
8. **Scatter Plots**: Analyze relationships between different performance metrics
9. **Horizontal Bar Charts**: Compare metrics across different system components
10. **Multi-axis Charts**: Display related metrics with different scales on a single chart

## Technical Implementation

OmniStream is built using a modern data engineering tech stack:

- **Front-end**: Streamlit for interactive dashboards and visualizations
- **Data Processing**: Simulated pipeline based on Apache Kafka, Spark, and Airflow patterns
- **Data Quality**: Implementation of Great Expectations patterns for quality monitoring
- **Monitoring**: Prometheus-style metrics collection and visualization
- **Database**: Connectivity with PostgreSQL for data persistence

## Use Cases

This platform demonstrates advanced data engineering capabilities useful for:

1. **Enterprise Data Integration**: Combining data from multiple business systems
2. **IoT Data Processing**: Handling high-volume sensor data with quality controls
3. **Financial Data Analysis**: Processing market data feeds with strict quality requirements
4. **E-commerce Data Pipelines**: Managing customer, product, and transaction data flows
5. **Social Media Analytics**: Processing and analyzing engagement metrics in real-time

## Getting Started

To run the application locally:

```bash
# Install dependencies
pip install streamlit pandas numpy plotly psycopg2-binary sqlalchemy

# Run the application
streamlit run app.py
```

## Showcase for Recruiters

This project demonstrates advanced data engineering skills including:

- Data pipeline architecture design
- Real-time data processing
- Data quality monitoring and enforcement
- Performance optimization
- Advanced data visualization
- System observability implementation

The project is specifically designed to showcase technical capabilities that are highly relevant for senior data engineering roles.
