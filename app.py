import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import time
import random
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, MetaData, Table, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Set page configuration
st.set_page_config(
    page_title="OmniStream: Data Engineering Pipeline",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define CSS for custom styling
st.markdown("""
<style>
/* Base text and background colors to ensure visibility */
.stApp {
    color: #1A202C !important;
    background-color: #F7FAFC !important;
}

/* Make all standard text visible */
p, div, span, li, td, th, caption, h1, h2, h3, h4, h5, h6 {
    color: #2D3748 !important;
}

/* Override Streamlit defaults for specific components */
.st-bw {
    color: #2D3748 !important;
}

.st-cn {
    background-color: white !important;
}

.main-header {
    font-size: 2.8rem;
    color: #1E3A8A !important;
    margin-bottom: 20px;
    text-align: center;
    font-weight: 700;
    background: linear-gradient(90deg, #1E40AF, #3B82F6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding: 15px 0;
}

.sub-header {
    font-size: 1.8rem;
    color: #2563EB !important;
    margin-top: 30px;
    margin-bottom: 15px;
    font-weight: 600;
    border-bottom: 2px solid #E5E7EB;
    padding-bottom: 10px;
}

.section-title {
    font-size: 1.5rem;
    color: #3B82F6 !important;
    margin-top: 20px;
    margin-bottom: 15px;
    font-weight: 500;
    display: flex;
    align-items: center;
}

.section-title:before {
    content: "";
    display: inline-block;
    width: 12px;
    height: 24px;
    background-color: #3B82F6;
    margin-right: 10px;
    border-radius: 3px;
}

.metric-card {
    background-color: white;
    border-radius: 12px;
    padding: 25px;
    box-shadow: 0 10px 15px rgba(0, 0, 0, 0.05);
    text-align: center;
    transition: all 0.3s;
    border: 1px solid #E5E7EB;
    height: 100%;
}

.metric-card:hover {
    transform: translateY(-7px);
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
    border-color: #BFDBFE;
}

.metric-value {
    font-size: 2.4rem;
    font-weight: bold;
    color: #1D4ED8 !important;
    margin: 10px 0;
}

.metric-label {
    font-size: 1.1rem;
    color: #4B5563 !important;
    font-weight: 500;
}

.insight-card {
    background-color: white;
    border-left: 4px solid #3B82F6;
    padding: 16px;
    margin-bottom: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    border-top: 1px solid #E5E7EB;
    border-right: 1px solid #E5E7EB;
    border-bottom: 1px solid #E5E7EB;
}

.alert-card {
    background-color: white;
    border-left: 4px solid #EF4444;
    padding: 16px;
    margin-bottom: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    border-top: 1px solid #FCA5A5;
    border-right: 1px solid #FCA5A5;
    border-bottom: 1px solid #FCA5A5;
}

.success-card {
    background-color: white;
    border-left: 4px solid #10B981;
    padding: 16px;
    margin-bottom: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    border-top: 1px solid #A7F3D0;
    border-right: 1px solid #A7F3D0;
    border-bottom: 1px solid #A7F3D0;
}

.warning-card {
    background-color: white;
    border-left: 4px solid #F59E0B;
    padding: 16px;
    margin-bottom: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    border-top: 1px solid #FCD34D;
    border-right: 1px solid #FCD34D;
    border-bottom: 1px solid #FCD34D;
}

.code-block {
    background-color: #1F2937;
    color: #F9FAFB !important;
    padding: 18px;
    border-radius: 8px;
    font-family: "JetBrains Mono", monospace;
    overflow-x: auto;
    margin: 15px 0;
    border: 1px solid #374151;
}

.code-block code, .code-block pre {
    color: #F9FAFB !important;
}

.badge {
    background-color: #DBEAFE;
    color: #1E40AF !important;
    padding: 6px 12px;
    border-radius: 9999px;
    font-size: 0.8rem;
    font-weight: 500;
    display: inline-block;
    margin-right: 8px;
    margin-bottom: 8px;
}

.badge-alert {
    background-color: #FEE2E2;
    color: #B91C1C !important;
}

.badge-success {
    background-color: #D1FAE5;
    color: #065F46 !important;
}

.badge-warning {
    background-color: #FEF3C7;
    color: #92400E !important;
}

.dashboard-tab {
    border-radius: 8px;
    padding: 25px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    margin-bottom: 25px;
    background-color: white;
    border: 1px solid #E5E7EB;
}

.technical-details {
    font-size: 0.9rem;
    color: #4B5563 !important;
    font-style: italic;
    line-height: 1.5;
}

.highlight {
    color: #2563EB !important;
    font-weight: 600;
    background-color: #EFF6FF;
    padding: 0 5px;
    border-radius: 4px;
}

/* Style for DataFrames */
.dataframe {
    border-collapse: collapse !important;
    border: none !important;
    font-size: 0.9rem !important;
}

.dataframe th {
    background-color: #F3F4F6 !important;
    color: #1F2937 !important;
    font-weight: 600 !important;
    border: 1px solid #E5E7EB !important;
    padding: 8px 15px !important;
}

.dataframe td {
    border: 1px solid #E5E7EB !important;
    padding: 8px 15px !important;
    background-color: white !important;
    color: #1F2937 !important;
}

/* Style for tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    padding: 10px 20px;
    border-radius: 8px 8px 0 0;
    font-weight: 500;
}

.stTabs [aria-selected="true"] {
    background-color: #BFDBFE !important;
    color: #1E40AF !important;
}

/* Style for markdown text */
.stMarkdown p {
    margin-bottom: 12px;
    line-height: 1.6;
}

/* Custom styles for buttons */
.stButton button {
    background-color: #3B82F6 !important;
    color: white !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    padding: 5px 25px !important;
    border: none !important;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1) !important;
    transition: all 0.2s !important;
}

.stButton button:hover {
    background-color: #2563EB !important;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15) !important;
}

/* Sidebar styles */
.stSidebar {
    background-color: #F8FAFC !important;
    padding-top: 1rem !important;
}

.stSidebar [data-testid="stMarkdownContainer"] > p {
    color: #4B5563 !important;  
    font-size: 0.9rem !important;
}

.stSidebar [data-testid="stSidebarNav"] {
    background-color: #F1F5F9 !important;
    border-radius: 8px !important;
}

/* Progress bar */
.stProgress > div > div {
    background-color: #3B82F6 !important;
}

/* Chart borders */
[data-testid="stPlotlyChart"] > div {
    border: 1px solid #E5E7EB !important;
    border-radius: 8px !important;
    padding: 10px !important;
    background-color: white !important;
}

/* Override for info box text */
.stAlert p {
    color: #1F2937 !important;
}
</style>
""", unsafe_allow_html=True)

# Add sidebar with additional information
with st.sidebar:
    st.image("/Users/susmithreddy/realestate/real-estate-app/src/components/logo.svg", width=150)
    st.markdown("## OmniStream Controls")
    st.markdown("---")
    st.markdown("### Data Sources")
    
    # Source toggles
    all_sources = ["Stock Market API", "Weather API", "Social Media", "Retail", "IoT Sensors"]
    active_sources = st.multiselect("Active Sources", all_sources, default=all_sources)
    
    # Fake refresh rate slider
    refresh_rate = st.slider("Update Frequency (sec)", 1, 60, 5)
    
    # Fake time range selector
    time_range = st.selectbox("Time Range", ["Last Hour", "Last Day", "Last Week", "Last Month"])
    
    # Fake environment selector
    environment = st.radio("Environment", ["Production", "Staging", "Development"])
    
    st.markdown("---")
    st.markdown("### Documentation")
    
    # Faux documentation links
    doc_links = {
        "User Guide": "https://example.com/user-guide",
        "API Reference": "https://example.com/api",
        "Admin Manual": "https://example.com/admin",
        "Troubleshooting": "https://example.com/troubleshoot"
    }
    
    for name, link in doc_links.items():
        st.markdown(f"[{name}]({link})")
        
    st.markdown("---")
    st.markdown("### System Status")
    st.success("All Systems Operational")
    st.markdown("Last Updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Initialize state for demonstration
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.start_time = datetime.now()
    st.session_state.last_update = datetime.now()
    
    # Initialize metrics and counters
    st.session_state.data_sources = {
        "stock_market": {
            "name": "Stock Market API",
            "status": "active",
            "records_processed": 0,
            "failures": 0,
            "last_update": datetime.now() - timedelta(minutes=2),
            "latency_ms": random.randint(50, 150),
        },
        "weather_data": {
            "name": "Weather API",
            "status": "active",
            "records_processed": 0,
            "failures": 0,
            "last_update": datetime.now() - timedelta(minutes=3),
            "latency_ms": random.randint(100, 250),
        },
        "social_media": {
            "name": "Social Media Analytics",
            "status": "active",
            "records_processed": 0,
            "failures": 0,
            "last_update": datetime.now() - timedelta(minutes=1),
            "latency_ms": random.randint(150, 300),
        },
        "retail_transactions": {
            "name": "Retail Transactions",
            "status": "active",
            "records_processed": 0,
            "failures": 0,
            "last_update": datetime.now() - timedelta(minutes=4),
            "latency_ms": random.randint(75, 200),
        },
        "iot_sensors": {
            "name": "IoT Sensor Network",
            "status": "active",
            "records_processed": 0,
            "failures": 0,
            "last_update": datetime.now() - timedelta(minutes=2),
            "latency_ms": random.randint(20, 80),
        }
    }
    
    st.session_state.processing_steps = [
        "data_ingestion",
        "data_validation",
        "data_transformation",
        "data_enrichment",
        "data_loading",
        "anomaly_detection"
    ]
    
    st.session_state.pipeline_metrics = {
        "total_records_processed": 0,
        "total_errors": 0,
        "overall_latency_ms": 0,
        "data_quality_score": 98.5,
        "pipeline_uptime": 99.98,
        "active_sources": 5,
        "active_destinations": 3,
        "schema_violations": 0,
        "data_drift_incidents": 0
    }
    
    # Create some historical processing data
    hours_back = 48
    st.session_state.timeseries_data = {
        "timestamps": [(datetime.now() - timedelta(hours=i)).strftime("%Y-%m-%d %H:%M:%S") for i in range(hours_back, 0, -1)],
        "throughput": [random.randint(5000, 15000) for _ in range(hours_back)],
        "latency": [random.randint(50, 500) for _ in range(hours_back)],
        "error_rate": [random.uniform(0, 2) for _ in range(hours_back)],
        "quality_score": [random.uniform(95, 100) for _ in range(hours_back)]
    }
    
    # Recent alerts and events
    st.session_state.alerts = []
    st.session_state.events = []

# Function to simulate real-time data updates
def update_pipeline_metrics():
    """Update pipeline metrics to simulate real-time processing"""
    now = datetime.now()
    
    # Only update every 1-2 seconds to avoid excessive recomputation
    if (now - st.session_state.last_update).total_seconds() < 1.5:
        return
    
    # Update source metrics
    for source_id, source in st.session_state.data_sources.items():
        # Calculate records to process this cycle
        time_diff = (now - source["last_update"]).total_seconds()
        records_this_cycle = int(time_diff * random.randint(10, 50))
        
        # Determine if we should simulate a failure
        failure_chance = 0.05  # 5% chance of failure
        will_fail = random.random() < failure_chance
        
        if will_fail:
            source["failures"] += 1
            failure_type = random.choice([
                "API Timeout", 
                "Connection Error", 
                "Authentication Failure",
                "Rate Limit Exceeded",
                "Malformed Response"
            ])
            
            # Add an alert for the failure
            st.session_state.alerts.append({
                "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                "source": source["name"],
                "message": f"{failure_type} encountered when processing {source_id}",
                "severity": "high" if failure_type in ["Authentication Failure", "Connection Error"] else "medium",
                "status": "active"
            })
        
        # Update metrics
        source["records_processed"] += records_this_cycle
        source["last_update"] = now
        source["latency_ms"] = random.randint(
            max(10, source["latency_ms"] - 20),
            min(500, source["latency_ms"] + 20)
        )
        
        # Log an event for large batches
        if records_this_cycle > 30:
            st.session_state.events.append({
                "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                "component": source["name"],
                "message": f"Processed large batch: {records_this_cycle} records",
                "type": "info"
            })
    
    # Update overall pipeline metrics
    total_records = sum(s["records_processed"] for s in st.session_state.data_sources.values())
    new_records = total_records - st.session_state.pipeline_metrics["total_records_processed"]
    
    st.session_state.pipeline_metrics["total_records_processed"] = total_records
    
    # Calculate a weighted average latency
    latencies = [s["latency_ms"] for s in st.session_state.data_sources.values()]
    st.session_state.pipeline_metrics["overall_latency_ms"] = sum(latencies) / len(latencies)
    
    # Count total errors
    total_errors = sum(s["failures"] for s in st.session_state.data_sources.values())
    st.session_state.pipeline_metrics["total_errors"] = total_errors
    
    # Simulate occasional data quality issues
    if random.random() < 0.1:  # 10% chance each update
        quality_shift = random.uniform(-0.5, 0.2)
        st.session_state.pipeline_metrics["data_quality_score"] = min(100, max(90, 
            st.session_state.pipeline_metrics["data_quality_score"] + quality_shift
        ))
        
        # If quality decreased significantly, add an alert
        if quality_shift < -0.3:
            st.session_state.alerts.append({
                "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                "source": "Data Quality Monitor",
                "message": f"Data quality score decreased to {st.session_state.pipeline_metrics['data_quality_score']:.2f}%",
                "severity": "medium",
                "status": "active"
            })
            
            # Also track as a schema violation or data drift
            if random.random() < 0.5:
                st.session_state.pipeline_metrics["schema_violations"] += 1
            else:
                st.session_state.pipeline_metrics["data_drift_incidents"] += 1
    
    # Update time series data
    hour_key = now.strftime("%Y-%m-%d %H:00:00")
    if hour_key not in st.session_state.timeseries_data["timestamps"]:
        st.session_state.timeseries_data["timestamps"].append(hour_key)
        st.session_state.timeseries_data["throughput"].append(new_records)
        st.session_state.timeseries_data["latency"].append(st.session_state.pipeline_metrics["overall_latency_ms"])
        
        error_rate = 100 * total_errors / max(1, total_records)
        st.session_state.timeseries_data["error_rate"].append(error_rate)
        st.session_state.timeseries_data["quality_score"].append(st.session_state.pipeline_metrics["data_quality_score"])
        
        # Keep only the most recent data points
        max_points = 48  # Two days worth of hourly data
        if len(st.session_state.timeseries_data["timestamps"]) > max_points:
            for key in st.session_state.timeseries_data:
                st.session_state.timeseries_data[key] = st.session_state.timeseries_data[key][-max_points:]
    
    # Limit alerts and events to the most recent 20
    st.session_state.alerts = st.session_state.alerts[-20:]
    st.session_state.events = st.session_state.events[-20:]
    
    # Update the last update timestamp
    st.session_state.last_update = now

# Simulate occasional full pipeline execution for demo
def demo_full_pipeline_execution():
    """Simulate running a full pipeline execution with detailed steps"""
    pipeline_steps = [
        {
            "name": "Data Ingestion", 
            "description": "Extracting data from source systems",
            "substeps": [
                "Establishing secure connections to data sources",
                "Authenticating with API credentials",
                "Reading raw data from endpoints",
                "Applying source-specific parsers",
                "Tracking source record counts"
            ],
            "time_range": (0.5, 2.0)
        },
        {
            "name": "Data Validation", 
            "description": "Ensuring data meets quality standards",
            "substeps": [
                "Checking for data completeness",
                "Validating data against schema definitions",
                "Identifying anomalous values",
                "Logging validation issues",
                "Applying validation rules by data source"
            ],
            "time_range": (0.3, 1.0)
        },
        {
            "name": "Data Transformation", 
            "description": "Converting data to standardized formats",
            "substeps": [
                "Normalizing numerical values",
                "Standardizing date/time formats",
                "Converting units of measurement",
                "Flattening nested structures",
                "Applying business transformation rules"
            ],
            "time_range": (0.8, 1.5)
        },
        {
            "name": "Data Enrichment", 
            "description": "Enhancing data with additional context",
            "substeps": [
                "Joining with reference datasets",
                "Adding geographical information",
                "Calculating derived metrics",
                "Applying machine learning predictions",
                "Tagging with metadata"
            ],
            "time_range": (0.5, 1.2)
        },
        {
            "name": "Data Loading", 
            "description": "Writing processed data to destination systems",
            "substeps": [
                "Preparing data for target systems",
                "Optimizing batch sizes",
                "Performing upsert operations",
                "Updating data lineage records",
                "Verifying destination record counts"
            ],
            "time_range": (0.7, 2.0)
        },
        {
            "name": "Post-Processing", 
            "description": "Finalizing the pipeline execution",
            "substeps": [
                "Updating data catalogs",
                "Generating data quality reports",
                "Sending notifications to stakeholders",
                "Archiving processing logs",
                "Updating pipeline metadata"
            ],
            "time_range": (0.2, 0.8)
        }
    ]
    
    # Create a placeholder for the pipeline execution
    pipeline_container = st.empty()
    
    # Display initial state
    with pipeline_container.container():
        st.markdown('<p class="section-title">Pipeline Execution Demo</p>', unsafe_allow_html=True)
        st.info("Initializing pipeline execution...")
        
        # Show overall progress bar
        overall_progress = st.progress(0)
        step_status = st.empty()
        substep_status = st.empty()
        
        # Metrics to track during execution
        col1, col2, col3, col4 = st.columns(4)
        records_metric = col1.empty()
        time_metric = col2.empty()
        errors_metric = col3.empty()
        quality_metric = col4.empty()
        
        # Initial values
        records_processed = 0
        errors_found = 0
        quality_score = 100.0
        
        records_metric.metric("Records Processed", f"{records_processed:,}")
        time_metric.metric("Elapsed Time", "0.0s")
        errors_metric.metric("Errors Found", f"{errors_found}")
        quality_metric.metric("Quality Score", f"{quality_score:.1f}%")
    
    # Simulate pipeline execution
    start_time = time.time()
    for step_idx, step in enumerate(pipeline_steps):
        step_start = time.time()
        
        # Update step status
        step_status.markdown(f"**Current Step:** {step['name']} - {step['description']}")
        
        # Process each substep
        for substep_idx, substep in enumerate(step["substeps"]):
            # Simulate processing time
            substep_time = random.uniform(step["time_range"][0], step["time_range"][1])
            substep_status.markdown(f"Executing: {substep}...")
            
            # Simulate records being processed
            new_records = random.randint(100, 500)
            records_processed += new_records
            
            # Simulate occasional errors
            if random.random() < 0.15:  # 15% chance of error
                new_errors = random.randint(1, 5)
                errors_found += new_errors
                
                # Adjust quality score
                quality_delta = -random.uniform(0.1, 0.5)
                quality_score = max(90, quality_score + quality_delta)
            
            # Update metrics
            elapsed = time.time() - start_time
            records_metric.metric("Records Processed", f"{records_processed:,}")
            time_metric.metric("Elapsed Time", f"{elapsed:.1f}s")
            errors_metric.metric("Errors Found", f"{errors_found}")
            quality_metric.metric("Quality Score", f"{quality_score:.1f}%")
            
            # Update progress
            progress_pct = (step_idx / len(pipeline_steps)) + ((substep_idx + 1) / len(step["substeps"])) / len(pipeline_steps)
            overall_progress.progress(progress_pct)
            
            # Pause for visual effect
            time.sleep(substep_time / 5)  # Divide by 5 to make the demo faster but still visible
        
        # Add completion message
        step_time = time.time() - step_start
        # Calculate total records for this step (20-100 records per substep)
        step_records = random.randint(100, 500) * len(step["substeps"])
        st.session_state.events.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "component": step["name"],
            "message": f"{step['name']} completed in {step_time:.2f}s - processed {step_records} records",
            "type": "success"
        })
    
    # Final update
    total_time = time.time() - start_time
    
    # Complete the progress bar
    overall_progress.progress(100)
    step_status.markdown(f"**Pipeline Execution Completed!**")
    substep_status.markdown(f"Total records processed: {records_processed:,} in {total_time:.2f} seconds")
    
    # Add summary to events
    st.session_state.events.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "component": "Pipeline Manager",
        "message": f"Full pipeline execution completed - {records_processed:,} records, {errors_found} errors, {quality_score:.1f}% quality score",
        "type": "info"
    })
    
    # Pause briefly to show completion
    time.sleep(1)
    
    # Clear the container to return to main dashboard
    pipeline_container.empty()

# Main application
st.markdown('<h1 class="main-header">OmniStream: Multi-source Data Processing Pipeline</h1>', unsafe_allow_html=True)

# App description
st.markdown("""
<div class="insight-card">
<p><strong>About this Data Engineering Platform:</strong></p>
<p>OmniStream is an advanced data engineering solution designed to seamlessly integrate, process, and monitor data from multiple sources in real-time. 
The platform implements sophisticated data quality controls, anomaly detection algorithms, and end-to-end observability to ensure reliable 
data pipelines for critical business operations.</p>
</div>
""", unsafe_allow_html=True)

# Dashboard navigation
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Pipeline Dashboard", 
    "🔍 Data Quality Metrics", 
    "🧪 Pipeline Demo", 
    "📈 Performance Analytics"
])

# Update metrics for real-time simulation
update_pipeline_metrics()

# Tab 1: Pipeline Dashboard
with tab1:
    st.markdown('<p class="sub-header">Real-time Pipeline Monitoring</p>', unsafe_allow_html=True)
    
    # System status overview
    st.markdown('<p class="section-title">System Status</p>', unsafe_allow_html=True)
    
    # Status metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{st.session_state.pipeline_metrics["active_sources"]}/{len(st.session_state.data_sources)}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Active Data Sources</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{st.session_state.pipeline_metrics["total_records_processed"]:,}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Total Records Processed</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{st.session_state.pipeline_metrics["overall_latency_ms"]:.0f}ms</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Avg Processing Latency</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{st.session_state.pipeline_metrics["data_quality_score"]:.1f}%</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Overall Data Quality</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Data Source Status
    st.markdown('<p class="section-title">Data Source Status</p>', unsafe_allow_html=True)
    
    # Create a dataframe for display
    source_data = []
    for source_id, source in st.session_state.data_sources.items():
        source_data.append({
            "Source Name": source["name"],
            "Status": source["status"],
            "Records Processed": f"{source['records_processed']:,}",
            "Failures": source["failures"],
            "Last Update": source["last_update"].strftime("%H:%M:%S"),
            "Latency (ms)": source["latency_ms"]
        })
    
    source_df = pd.DataFrame(source_data)
    
    # Use Streamlit's dataframe with styling
    st.dataframe(
        source_df,
        use_container_width=True,
        hide_index=True
    )
    
    # Recent alerts and events
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p class="section-title">Recent Alerts</p>', unsafe_allow_html=True)
        
        if not st.session_state.alerts:
            st.info("No alerts to display.")
        else:
            for alert in st.session_state.alerts[:5]:  # Show only the 5 most recent
                severity_class = "alert-card" if alert["severity"] == "high" else "warning-card"
                st.markdown(f"""
                <div class="{severity_class}">
                    <small>{alert["timestamp"]}</small><br>
                    <strong>{alert["source"]}</strong>: {alert["message"]}
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<p class="section-title">Recent Events</p>', unsafe_allow_html=True)
        
        if not st.session_state.events:
            st.info("No events to display.")
        else:
            for event in st.session_state.events[:5]:  # Show only the 5 most recent
                event_class = "success-card" if event["type"] == "success" else "insight-card"
                st.markdown(f"""
                <div class="{event_class}">
                    <small>{event["timestamp"]}</small><br>
                    <strong>{event["component"]}</strong>: {event["message"]}
                </div>
                """, unsafe_allow_html=True)
    
    # Processing statistics
    st.markdown('<p class="section-title">Pipeline Processing Statistics</p>', unsafe_allow_html=True)
    
    # Throughput chart
    if st.session_state.timeseries_data["timestamps"]:
        throughput_df = pd.DataFrame({
            "Timestamp": st.session_state.timeseries_data["timestamps"],
            "Records Processed": st.session_state.timeseries_data["throughput"]
        })
        throughput_df["Timestamp"] = pd.to_datetime(throughput_df["Timestamp"])
        
        fig = px.line(
            throughput_df, 
            x="Timestamp", 
            y="Records Processed",
            title="Pipeline Throughput Over Time"
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

# Tab 2: Data Quality Metrics
with tab2:
    st.markdown('<p class="sub-header">Data Quality Monitoring</p>', unsafe_allow_html=True)
    
    # Quality Metrics Summary
    st.markdown('<p class="section-title">Quality Metrics Summary</p>', unsafe_allow_html=True)
    
    quality_col1, quality_col2, quality_col3, quality_col4 = st.columns(4)
    
    with quality_col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{st.session_state.pipeline_metrics["data_quality_score"]:.1f}%</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Overall Quality Score</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with quality_col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{st.session_state.pipeline_metrics["schema_violations"]}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Schema Violations</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with quality_col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{st.session_state.pipeline_metrics["data_drift_incidents"]}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Data Drift Incidents</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with quality_col4:
        error_rate = 100 * st.session_state.pipeline_metrics["total_errors"] / max(1, st.session_state.pipeline_metrics["total_records_processed"])
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{error_rate:.2f}%</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Error Rate</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Quality trend chart
    st.markdown('<p class="section-title">Data Quality Trends</p>', unsafe_allow_html=True)
    
    if st.session_state.timeseries_data["timestamps"]:
        quality_df = pd.DataFrame({
            "Timestamp": st.session_state.timeseries_data["timestamps"],
            "Quality Score": st.session_state.timeseries_data["quality_score"],
            "Error Rate": st.session_state.timeseries_data["error_rate"]
        })
        quality_df["Timestamp"] = pd.to_datetime(quality_df["Timestamp"])
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=quality_df["Timestamp"], 
            y=quality_df["Quality Score"],
            mode='lines',
            name='Quality Score (%)',
            line=dict(color='#3B82F6', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=quality_df["Timestamp"], 
            y=quality_df["Error Rate"],
            mode='lines',
            name='Error Rate (%)',
            line=dict(color='#EF4444', width=2),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title='Data Quality Metrics Over Time',
            height=400,
            yaxis=dict(
                title='Quality Score (%)',
                range=[90, 100],
                tickfont=dict(color='#3B82F6')
            ),
            yaxis2=dict(
                title='Error Rate (%)',
                range=[0, 5],
                overlaying='y',
                side='right',
                tickfont=dict(color='#EF4444')
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Data Quality Rules
    st.markdown('<p class="section-title">Automated Data Quality Rules</p>', unsafe_allow_html=True)
    
    # Sample quality rules
    quality_rules = [
        {
            "rule_id": "QR-001",
            "name": "Completeness Check",
            "description": "Ensures critical fields are not null",
            "target": "All Sources",
            "severity": "High",
            "status": "Active"
        },
        {
            "rule_id": "QR-002",
            "name": "Range Validation",
            "description": "Validates numerical values fall within expected ranges",
            "target": "Stock Market API, IoT Sensor Network",
            "severity": "Medium",
            "status": "Active"
        },
        {
            "rule_id": "QR-003",
            "name": "Format Validation",
            "description": "Checks string fields match expected formats (email, phone, etc.)",
            "target": "Social Media Analytics, Retail Transactions",
            "severity": "Medium",
            "status": "Active"
        },
        {
            "rule_id": "QR-004",
            "name": "Freshness Check",
            "description": "Ensures data is not older than predefined threshold",
            "target": "All Sources",
            "severity": "High",
            "status": "Active"
        },
        {
            "rule_id": "QR-005",
            "name": "Consistency Check",
            "description": "Verifies related data points are consistent across sources",
            "target": "All Sources",
            "severity": "Medium",
            "status": "Active"
        },
        {
            "rule_id": "QR-006",
            "name": "Statistical Validation",
            "description": "Applies statistical tests to identify outliers",
            "target": "Stock Market API, Weather API, IoT Sensor Network",
            "severity": "Low",
            "status": "Active"
        },
        {
            "rule_id": "QR-007",
            "name": "Referential Integrity",
            "description": "Ensures foreign key references are valid",
            "target": "Retail Transactions",
            "severity": "High",
            "status": "Active"
        }
    ]
    
    # Display rules as a table
    rules_df = pd.DataFrame(quality_rules)
    st.dataframe(rules_df, use_container_width=True, hide_index=True)
    
    # Data Enrichment Processes
    st.markdown('<p class="section-title">Data Enrichment Processes</p>', unsafe_allow_html=True)
    
    enrichment_col1, enrichment_col2 = st.columns(2)
    
    with enrichment_col1:
        st.markdown("""
        <div class="insight-card">
            <strong>Geospatial Enrichment</strong><br>
            Enhances location data with:
            <ul>
                <li>Geocoding for addresses and place names</li>
                <li>Reverse geocoding for coordinates</li>
                <li>Administrative boundary mapping</li>
                <li>Points of interest integration</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-card">
            <strong>Temporal Enrichment</strong><br>
            Enhances time-based data with:
            <ul>
                <li>Holiday and business day flagging</li>
                <li>Seasonal indicators</li>
                <li>Time zone normalization</li>
                <li>Business hour classification</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with enrichment_col2:
        st.markdown("""
        <div class="insight-card">
            <strong>Entity Resolution</strong><br>
            Improves data consistency with:
            <ul>
                <li>Customer identity resolution</li>
                <li>Product catalogue normalization</li>
                <li>Organization entity matching</li>
                <li>Fuzzy matching algorithms</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-card">
            <strong>ML-based Enrichment</strong><br>
            Adds valuable context with:
            <ul>
                <li>Sentiment analysis for text</li>
                <li>Content categorization</li>
                <li>Predictive attributes</li>
                <li>Anomaly score calculation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Tab 3: Pipeline Demo
with tab3:
    st.markdown('<p class="sub-header">Interactive Pipeline Demonstration</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-card">
    <p>This demonstration shows how the OmniStream pipeline processes data from multiple sources, 
    applying validation, transformation, enrichment, and loading steps. The demo simulates a complete 
    pipeline execution with real-time metrics and step-by-step visualization.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pipeline architecture diagram
    st.markdown('<p class="section-title">Pipeline Architecture</p>', unsafe_allow_html=True)
    
    st.markdown("""
    ```
    ┌─────────────────┐     ┌──────────────────────────────────────────────────────────┐     ┌─────────────────┐
    │  DATA SOURCES   │     │               OMNISTREAM PROCESSING                      │     │  DESTINATIONS   │
    │                 │     │                                                          │     │                 │
    │  ┌───────────┐  │     │  ┌───────────┐   ┌───────────┐   ┌───────────┐   ┌───┐  │     │  ┌───────────┐  │
    │  │Stock Market│──┼────┼─▶│   Data    │──▶│   Data    │──▶│   Data    │──▶│ D │  │     │  │Data        │  │
    │  │    API     │  │     │  │ Ingestion │   │Validation │   │Transformat│   │ a │  │     │  │Warehouse   │◀─┼──┐
    │  └───────────┘  │     │  └───────────┘   └───────────┘   └───────────┘   │ t │  │     │  └───────────┘  │  │
    │                 │     │         │               │               │         │ a │  │     │                 │  │
    │  ┌───────────┐  │     │         ▼               ▼               ▼         │   │  │     │  ┌───────────┐  │  │
    │  │Weather Data│──┼────┼─▶┌───────────┐   ┌───────────┐   ┌───────────┐   │ E │  │     │  │Analytics   │  │  │
    │  │    API     │  │     │  │Data Source│   │  Schema   │   │Standardized│   │ n │  │     │  │Dashboards │◀─┼──┤
    │  └───────────┘  │     │  │Connectors │   │Validators │   │Formats    │   │ r │──┼────▶│  └───────────┘  │  │
    │                 │     │  └───────────┘   └───────────┘   └───────────┘   │ i │  │     │                 │  │
    │  ┌───────────┐  │     │         │               │               │         │ c │  │     │  ┌───────────┐  │  │
    │  │Social Media│──┼────┼─▶       │               │               │         │ h │  │     │  │Real-time   │  │  │
    │  │ Analytics  │  │     │         ▼               ▼               ▼         │ m │  │     │  │Applications│◀─┼──┤
    │  └───────────┘  │     │  ┌───────────┐   ┌───────────┐   ┌───────────┐   │ e │  │     │  └───────────┘  │  │
    │                 │     │  │Error      │   │Quality    │   │ML         │   │ n │  │     │                 │  │
    │  ┌───────────┐  │     │  │Handling   │   │Metrics    │   │Enrichment │   │ t │  │     │  ┌───────────┐  │  │
    │  │  Retail    │──┼────┼─▶│& Retry    │   │Dashboard  │   │Layer      │   │   │  │     │  │ML Model    │  │  │
    │  │Transactions│  │     │  └───────────┘   └───────────┘   └───────────┘   │ L │  │     │  │Training    │◀─┼──┘
    │  └───────────┘  │     │                                                   │ o │  │     │  └───────────┘  │
    │                 │     │  ┌─────────────────────────────────────────────┐  │ a │  │     │                 │
    │  ┌───────────┐  │     │  │           Monitoring & Alerting             │  │ d │  │     │                 │
    │  │IoT Sensor  │──┼────┼─▶│                                             │  │ e │  │     │                 │
    │  │Network     │  │     │  └─────────────────────────────────────────────┘  │ r │  │     │                 │
    │  └───────────┘  │     │                                                    └───┘  │     │                 │
    └─────────────────┘     └──────────────────────────────────────────────────────────┘     └─────────────────┘
    ```
    """)
    
    # Run pipeline demo button
    if st.button("▶️ Run Pipeline Demo", type="primary"):
        demo_full_pipeline_execution()
    
    # Technical implementation details
    st.markdown('<p class="section-title">Technical Implementation</p>', unsafe_allow_html=True)
    
    tech_col1, tech_col2 = st.columns(2)
    
    with tech_col1:
        st.markdown("""
        <div class="insight-card">
            <strong>Data Ingestion Layer</strong>
            <p class="technical-details">
            Implements Apache Kafka for stream processing and Apache Airflow for orchestration of batch workflows. 
            Custom connectors handle API integration with rate limiting and automatic retries. Data sources are 
            monitored through a Prometheus-based health check system.
            </p>
            <pre class="code-block">
# Example Kafka Consumer Configuration
consumer_config = {
    'bootstrap.servers': 'kafka-broker:9092',
    'group.id': 'financial-data-processor',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False,
    'max.poll.interval.ms': 300000,
    'session.timeout.ms': 30000
}
            </pre>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-card">
            <strong>Data Transformation Layer</strong>
            <p class="technical-details">
            Uses Apache Spark for large-scale data transformations with custom UDFs (User Defined Functions) 
            for complex business logic. The transformation layer implements a rule engine for dynamic application 
            of business rules without code changes. All transformations are tracked with data lineage metadata.
            </p>
            <pre class="code-block">
# Example Spark Transformation
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType

# Initialize Spark
spark = SparkSession.builder \\
    .appName("OmniStream-Transformation") \\
    .config("spark.sql.adaptive.enabled", "true") \\
    .getOrCreate()

# Register normalization UDF
@udf(returnType=StringType())
def normalize_identifier(id_value):
    # Apply standardization logic
    return standard_format(id_value)

# Apply to dataframe
transformed_df = input_df \\
    .withColumn("normalized_id", normalize_identifier(col("raw_id"))) \\
    .withColumn("process_timestamp", current_timestamp())
            </pre>
        </div>
        """, unsafe_allow_html=True)
    
    with tech_col2:
        st.markdown("""
        <div class="insight-card">
            <strong>Data Quality Framework</strong>
            <p class="technical-details">
            Implements Great Expectations for data validation and quality checks. The framework includes automated 
            profiling of incoming data to establish dynamic baselines and detect anomalies or drift. Quality metrics 
            are stored in a time-series database for historical analysis and trend detection.
            </p>
            <pre class="code-block">
# Example Great Expectations validation
import great_expectations as ge

# Load dataset with validation context
df = ge.read_csv("financial_data.csv")

# Apply expectations
validation_result = df.expect_column_values_to_not_be_null(
    "transaction_id"
).expect_column_values_to_be_between(
    "amount", 
    min_value=0.01, 
    max_value=1000000
).expect_column_values_to_match_regex(
    "account_number", 
    regex="^[A-Z]{2}\\d{18}$"
)

# Check validation results
if not validation_result.success:
    handle_quality_issues(validation_result)
            </pre>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-card">
            <strong>Monitoring & Alerting</strong>
            <p class="technical-details">
            Comprehensive monitoring implemented with Prometheus and Grafana, with custom exporters for 
            application-specific metrics. Alerting system uses a priority-based routing mechanism to ensure 
            critical issues are escalated appropriately, with integration to PagerDuty and Slack.
            </p>
            <pre class="code-block">
# Example Prometheus metric collection
from prometheus_client import Counter, Gauge, Histogram

# Define metrics
RECORDS_PROCESSED = Counter(
    'omnistream_records_processed_total',
    'Total number of records processed',
    ['source', 'status']
)

PROCESSING_LATENCY = Histogram(
    'omnistream_processing_latency_seconds',
    'Time taken to process records',
    ['source', 'processing_stage'],
    buckets=(0.1, 0.5, 1, 2.5, 5, 10, 30, 60, 120)
)

DATA_QUALITY_SCORE = Gauge(
    'omnistream_data_quality_score',
    'Overall quality score of processed data',
    ['source']
)
            </pre>
        </div>
        """, unsafe_allow_html=True)

# Tab 4: Performance Analytics
with tab4:
    st.markdown('<p class="sub-header">Performance Metrics & Analytics</p>', unsafe_allow_html=True)
    
    # Performance metrics
    perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)
    
    with perf_col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{st.session_state.pipeline_metrics["pipeline_uptime"]}%</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Pipeline Uptime</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with perf_col2:
        avg_throughput = sum(st.session_state.timeseries_data["throughput"][-5:]) / 5 if st.session_state.timeseries_data["throughput"] else 0
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{avg_throughput:.0f}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Avg Records/Hour</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with perf_col3:
        avg_latency = sum(st.session_state.timeseries_data["latency"][-5:]) / 5 if st.session_state.timeseries_data["latency"] else 0
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{avg_latency:.0f}ms</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Avg Processing Latency</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with perf_col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{len(st.session_state.processing_steps)}</div>', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Processing Stages</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced Performance Dashboard
    st.markdown('<p class="section-title">Performance Dashboard</p>', unsafe_allow_html=True)
    
    # Create a multi-metric dashboard using tabs within the tab
    perf_subtabs = st.tabs(["Latency Metrics", "Throughput Analysis", "Resource Utilization", "Error Tracking"])
    
    with perf_subtabs[0]:  # Latency Metrics
        st.markdown("### Processing Latency Analysis")
        
        # Dual chart layout
        lat_col1, lat_col2 = st.columns(2)
        
        with lat_col1:
            # Latency over time chart
            if st.session_state.timeseries_data["timestamps"]:
                latency_df = pd.DataFrame({
                    "Timestamp": st.session_state.timeseries_data["timestamps"],
                    "Latency (ms)": st.session_state.timeseries_data["latency"]
                })
                latency_df["Timestamp"] = pd.to_datetime(latency_df["Timestamp"])
                
                fig = px.line(
                    latency_df, 
                    x="Timestamp", 
                    y="Latency (ms)",
                    title="Processing Latency Over Time",
                    labels={"Latency (ms)": "Processing Time (ms)"}
                )
                fig.update_layout(
                    height=350,
                    xaxis_title="Time",
                    yaxis_title="Latency (ms)",
                    hovermode="x unified",
                    margin=dict(l=10, r=10, t=50, b=10),
                    plot_bgcolor="white",
                    xaxis=dict(
                        showgrid=True,
                        gridcolor='#E5E7EB',
                    ),
                    yaxis=dict(
                        showgrid=True,
                        gridcolor='#E5E7EB',
                    ),
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with lat_col2:
            # Latency by data source - bar chart
            source_latencies = pd.DataFrame({
                "Source": [s["name"] for s in st.session_state.data_sources.values()],
                "Latency (ms)": [s["latency_ms"] for s in st.session_state.data_sources.values()]
            })
            
            fig = px.bar(
                source_latencies,
                x="Source",
                y="Latency (ms)",
                title="Latency by Data Source",
                color="Latency (ms)",
                color_continuous_scale="blues",
                labels={"Latency (ms)": "Avg Latency (ms)"}
            )
            fig.update_layout(
                height=350,
                xaxis_title="Data Source",
                yaxis_title="Latency (ms)",
                coloraxis_showscale=False,
                margin=dict(l=10, r=10, t=50, b=10),
                plot_bgcolor="white",
                xaxis=dict(
                    showgrid=True,
                    gridcolor='#E5E7EB',
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='#E5E7EB',
                ),
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Detailed latency breakdown
        st.markdown("### Latency Breakdown by Processing Stage")
        
        # Generate simulated latency breakdown by stage
        stages = ["Data Ingestion", "Data Validation", "Transformation", "Enrichment", "Loading", "Post-Processing"]
        stage_lat_data = pd.DataFrame({
            "Stage": stages,
            "Avg Latency (ms)": [random.randint(20, 120) for _ in range(len(stages))],
            "Min Latency (ms)": [random.randint(10, 40) for _ in range(len(stages))],
            "Max Latency (ms)": [random.randint(150, 350) for _ in range(len(stages))]
        })
        
        # Plot stacked bar chart for min/avg/max latency by stage
        fig = go.Figure()
        
        # Add min latency bars
        fig.add_trace(go.Bar(
            y=stage_lat_data["Stage"],
            x=stage_lat_data["Min Latency (ms)"],
            name="Min Latency",
            orientation='h',
            marker=dict(color="#BFDBFE"),
            hovertemplate="%{y}: %{x} ms (min)<extra></extra>"
        ))
        
        # Add average latency bars (the difference between avg and min)
        fig.add_trace(go.Bar(
            y=stage_lat_data["Stage"],
            x=stage_lat_data["Avg Latency (ms)"] - stage_lat_data["Min Latency (ms)"],
            name="Avg Latency",
            orientation='h',
            marker=dict(color="#3B82F6"),
            hovertemplate="%{y}: %{x} ms (avg portion)<extra></extra>"
        ))
        
        # Add max latency bars (the difference between max and avg)
        fig.add_trace(go.Bar(
            y=stage_lat_data["Stage"],
            x=stage_lat_data["Max Latency (ms)"] - stage_lat_data["Avg Latency (ms)"],
            name="Max Latency",
            orientation='h',
            marker=dict(color="#1E40AF"),
            hovertemplate="%{y}: %{x} ms (max portion)<extra></extra>"
        ))
        
        # Customize layout
        fig.update_layout(
            title="Latency Distribution by Processing Stage",
            barmode='stack',
            height=400,
            margin=dict(l=10, r=10, t=50, b=10),
            plot_bgcolor="white",
            xaxis=dict(
                title="Latency (ms)",
                showgrid=True,
                gridcolor='#E5E7EB',
            ),
            yaxis=dict(
                title="Processing Stage",
                showgrid=False,
                categoryorder='total ascending'
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with perf_subtabs[1]:  # Throughput Analysis
        st.markdown("### Data Throughput Metrics")
        
        # Create throughput visualization
        throughput_col1, throughput_col2 = st.columns(2)
        
        with throughput_col1:
            # Throughput over time
            if st.session_state.timeseries_data["timestamps"]:
                throughput_df = pd.DataFrame({
                    "Timestamp": st.session_state.timeseries_data["timestamps"],
                    "Records Processed": st.session_state.timeseries_data["throughput"]
                })
                throughput_df["Timestamp"] = pd.to_datetime(throughput_df["Timestamp"])
                
                fig = px.area(
                    throughput_df, 
                    x="Timestamp", 
                    y="Records Processed",
                    title="Pipeline Throughput Over Time",
                    labels={"Records Processed": "Records/Hour"}
                )
                fig.update_traces(
                    fill='tozeroy', 
                    line=dict(color="#3B82F6"),
                    fillcolor="rgba(59, 130, 246, 0.2)"
                )
                fig.update_layout(
                    height=350,
                    xaxis_title="Time",
                    yaxis_title="Records Processed",
                    hovermode="x unified",
                    margin=dict(l=10, r=10, t=50, b=10),
                    plot_bgcolor="white",
                    xaxis=dict(
                        showgrid=True,
                        gridcolor='#E5E7EB',
                    ),
                    yaxis=dict(
                        showgrid=True,
                        gridcolor='#E5E7EB',
                    ),
                )
                st.plotly_chart(fig, use_container_width=True)
                
        with throughput_col2:
            # Throughput by source - Donut chart
            source_throughput = pd.DataFrame({
                "Source": [s["name"] for s in st.session_state.data_sources.values()],
                "Records": [s["records_processed"] for s in st.session_state.data_sources.values()]
            })
            
            # Only generate chart if there's data
            if sum(source_throughput["Records"]) > 0:
                fig = px.pie(
                    source_throughput,
                    values="Records",
                    names="Source",
                    title="Data Volume by Source",
                    hole=0.4,
                    color_discrete_sequence=px.colors.sequential.Blues_r
                )
                fig.update_traces(
                    textposition='inside',
                    textinfo='percent+label',
                    hovertemplate="%{label}<br>Records: %{value:,}<br>Percentage: %{percent}<extra></extra>"
                )
                fig.update_layout(
                    height=350,
                    showlegend=False,
                    margin=dict(l=10, r=10, t=50, b=10),
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No throughput data available yet. Please wait for data processing to begin.")
        
        # Hourly throughput patterns - grouped bar chart
        st.markdown("### Throughput by Hour of Day")
        
        # Create simulated hourly pattern data (more realistic pattern)
        hours = list(range(24))
        hourly_patterns = pd.DataFrame({
            "Hour": hours,
            "Weekday": [random.randint(5000, 12000) if 8 <= h <= 18 else random.randint(1000, 4000) for h in hours],
            "Weekend": [random.randint(3000, 7000) if 10 <= h <= 16 else random.randint(500, 2500) for h in hours]
        })
        
        # Plot grouped bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=hourly_patterns["Hour"],
            y=hourly_patterns["Weekday"],
            name="Weekday",
            marker_color="#3B82F6"
        ))
        
        fig.add_trace(go.Bar(
            x=hourly_patterns["Hour"],
            y=hourly_patterns["Weekend"],
            name="Weekend",
            marker_color="#93C5FD"
        ))
        
        fig.update_layout(
            title="Average Hourly Throughput Patterns",
            xaxis=dict(
                title="Hour of Day",
                tickmode="linear",
                tick0=0,
                dtick=2,
                showgrid=True,
                gridcolor='#E5E7EB',
            ),
            yaxis=dict(
                title="Avg Records Processed",
                showgrid=True,
                gridcolor='#E5E7EB',
            ),
            barmode='group',
            bargap=0.15,
            bargroupgap=0.1,
            height=400,
            margin=dict(l=10, r=10, t=50, b=10),
            plot_bgcolor="white",
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.99
            )
        )
        st.plotly_chart(fig, use_container_width=True)

    with perf_subtabs[2]:  # Resource Utilization
        st.markdown("### System Resource Utilization")
        
        # Generate some simulated resource usage for the demo
        resources = pd.DataFrame({
            "Resource": ["Main Processing Cluster", "Data Validation Workers", "Enrichment Nodes", "Edge Collectors"],
            "CPU (%)": [random.uniform(30, 80) for _ in range(4)],
            "Memory (%)": [random.uniform(40, 90) for _ in range(4)],
            "Disk IO (MB/s)": [random.uniform(5, 150) for _ in range(4)],
            "Network (MB/s)": [random.uniform(10, 200) for _ in range(4)]
        })
        
        # Display resource usage
        st.dataframe(resources, use_container_width=True, hide_index=True)
        
        # Add resource utilization charts
        resource_col1, resource_col2 = st.columns(2)
        
        with resource_col1:
            # CPU and Memory utilization - bar chart
            fig = go.Figure()
            
            # Add bars for CPU usage
            fig.add_trace(go.Bar(
                y=resources["Resource"],
                x=resources["CPU (%)"],
                name="CPU Usage",
                orientation='h',
                marker_color="#3B82F6",
                hovertemplate="%{y}<br>CPU Usage: %{x:.1f}%<extra></extra>"
            ))
            
            # Add bars for Memory usage
            fig.add_trace(go.Bar(
                y=resources["Resource"],
                x=resources["Memory (%)"],
                name="Memory Usage",
                orientation='h',
                marker_color="#93C5FD",
                hovertemplate="%{y}<br>Memory Usage: %{x:.1f}%<extra></extra>"
            ))
            
            # Add reference line for warning threshold
            fig.add_shape(
                type="line",
                x0=80, y0=-0.5,
                x1=80, y1=3.5,
                line=dict(
                    color="#F59E0B",
                    width=2,
                    dash="dash",
                )
            )
            
            fig.add_annotation(
                x=80, y=3.7,
                text="Warning Threshold",
                showarrow=False,
                font=dict(
                    size=10,
                    color="#F59E0B"
                )
            )
            
            # Configure layout
            fig.update_layout(
                title="CPU & Memory Utilization",
                barmode='group',
                xaxis=dict(
                    title="Utilization (%)",
                    range=[0, 100],
                    showgrid=True,
                    gridcolor='#E5E7EB',
                ),
                yaxis=dict(
                    title="System Component",
                    showgrid=False,
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                height=350,
                margin=dict(l=10, r=10, t=50, b=10),
                plot_bgcolor="white",
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with resource_col2:
            # IO Metrics - scatter plot
            fig = px.scatter(
                resources,
                x="Disk IO (MB/s)",
                y="Network (MB/s)",
                size="Memory (%)",
                color="CPU (%)",
                hover_name="Resource",
                title="I/O Performance Metrics",
                color_continuous_scale=px.colors.sequential.Blues,
                size_max=25,
            )
            
            fig.update_layout(
                xaxis=dict(
                    title="Disk I/O (MB/s)",
                    showgrid=True,
                    gridcolor='#E5E7EB',
                ),
                yaxis=dict(
                    title="Network I/O (MB/s)",
                    showgrid=True,
                    gridcolor='#E5E7EB',
                ),
                height=350,
                margin=dict(l=10, r=10, t=50, b=10),
                plot_bgcolor="white",
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Resource utilization over time chart
        st.markdown("### Resource Utilization Trends")
        
        # Generate simulated time series data for resources
        hours = 24
        timestamps = [(datetime.now() - timedelta(hours=i)).strftime("%Y-%m-%d %H:%M:%S") for i in range(hours, 0, -1)]
        
        # Create patterns that look realistic (with peaks during business hours)
        cpu_trend = []
        mem_trend = []
        io_trend = []
        
        for i in range(hours):
            hour = (datetime.now() - timedelta(hours=i)).hour
            # Higher usage during business hours
            if 8 <= hour <= 18:
                cpu_trend.append(random.uniform(50, 85))
                mem_trend.append(random.uniform(60, 90))
                io_trend.append(random.uniform(100, 200))
            else:
                cpu_trend.append(random.uniform(20, 50))
                mem_trend.append(random.uniform(40, 70))
                io_trend.append(random.uniform(30, 100))
        
        resource_trends = pd.DataFrame({
            "Timestamp": timestamps,
            "CPU Usage (%)": cpu_trend,
            "Memory Usage (%)": mem_trend,
            "I/O (MB/s)": io_trend
        })
        
        resource_trends["Timestamp"] = pd.to_datetime(resource_trends["Timestamp"])
        
        # Create a multi-line chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=resource_trends["Timestamp"],
            y=resource_trends["CPU Usage (%)"],
            name="CPU Usage",
            line=dict(color="#3B82F6", width=2),
        ))
        
        fig.add_trace(go.Scatter(
            x=resource_trends["Timestamp"],
            y=resource_trends["Memory Usage (%)"],
            name="Memory Usage",
            line=dict(color="#1D4ED8", width=2, dash="dot"),
        ))
        
        fig.add_trace(go.Scatter(
            x=resource_trends["Timestamp"],
            y=resource_trends["I/O (MB/s)"],
            name="I/O Throughput",
            line=dict(color="#93C5FD", width=2),
            yaxis="y2"
        ))
        
        fig.update_layout(
            title="Resource Utilization Over Time",
            xaxis=dict(
                title="Time",
                showgrid=True,
                gridcolor='#E5E7EB',
            ),
            yaxis=dict(
                title="Utilization (%)",
                range=[0, 100],
                showgrid=True,
                gridcolor='#E5E7EB',
                tickfont=dict(color="#3B82F6")
            ),
            yaxis2=dict(
                title="I/O (MB/s)",
                range=[0, 250],
                overlaying="y",
                side="right",
                showgrid=False,
                tickfont=dict(color="#93C5FD")
            ),
            hovermode="x unified",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            height=400,
            margin=dict(l=10, r=10, t=50, b=10),
            plot_bgcolor="white",
        )
        st.plotly_chart(fig, use_container_width=True)

    with perf_subtabs[3]:  # Error Tracking
        st.markdown("### Error Analysis Dashboard")
        
        # Create error tracking visualizations
        error_col1, error_col2 = st.columns(2)
        
        with error_col1:
            # Error rate over time chart
            if st.session_state.timeseries_data["timestamps"]:
                error_df = pd.DataFrame({
                    "Timestamp": st.session_state.timeseries_data["timestamps"],
                    "Error Rate (%)": st.session_state.timeseries_data["error_rate"]
                })
                error_df["Timestamp"] = pd.to_datetime(error_df["Timestamp"])
                
                fig = px.line(
                    error_df, 
                    x="Timestamp", 
                    y="Error Rate (%)",
                    title="Error Rate Trend"
                )
                
                # Add threshold lines
                fig.add_shape(
                    type="line",
                    x0=error_df["Timestamp"].min(),
                    y0=1,
                    x1=error_df["Timestamp"].max(),
                    y1=1,
                    line=dict(
                        color="#F59E0B",
                        width=2,
                        dash="dash",
                    ),
                    name="Warning Threshold"
                )
                
                fig.add_shape(
                    type="line",
                    x0=error_df["Timestamp"].min(),
                    y0=2,
                    x1=error_df["Timestamp"].max(),
                    y1=2,
                    line=dict(
                        color="#EF4444",
                        width=2,
                        dash="dash",
                    ),
                    name="Critical Threshold"
                )
                
                fig.update_traces(line=dict(color="#FB7185", width=2))
                fig.update_layout(
                    height=350,
                    xaxis_title="Time",
                    yaxis_title="Error Rate (%)",
                    hovermode="x unified",
                    margin=dict(l=10, r=10, t=50, b=10),
                    plot_bgcolor="white",
                    xaxis=dict(
                        showgrid=True,
                        gridcolor='#E5E7EB',
                    ),
                    yaxis=dict(
                        showgrid=True,
                        gridcolor='#E5E7EB',
                    ),
                    showlegend=False
                )
                
                # Add annotations for thresholds
                fig.add_annotation(
                    x=error_df["Timestamp"].max(),
                    y=1,
                    text="Warning",
                    showarrow=False,
                    yshift=10,
                    xshift=5,
                    font=dict(
                        size=10,
                        color="#F59E0B"
                    )
                )
                
                fig.add_annotation(
                    x=error_df["Timestamp"].max(),
                    y=2,
                    text="Critical",
                    showarrow=False,
                    yshift=10,
                    xshift=5,
                    font=dict(
                        size=10,
                        color="#EF4444"
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        with error_col2:
            # Error types distribution - pie chart
            error_types = [
                "API Timeout",
                "Connection Error",
                "Authentication Failure",
                "Rate Limit Exceeded",
                "Malformed Response", 
                "Data Validation Failure"
            ]
            
            error_counts = [random.randint(5, 30) for _ in range(len(error_types))]
            
            error_data = pd.DataFrame({
                "Error Type": error_types,
                "Count": error_counts
            })
            
            fig = px.pie(
                error_data,
                values="Count",
                names="Error Type",
                title="Distribution of Error Types",
                color_discrete_sequence=px.colors.sequential.Reds,
                hole=0.4
            )
            
            fig.update_traces(
                textposition='outside',
                textinfo='percent+label',
                hovertemplate="%{label}<br>Count: %{value}<br>Percentage: %{percent}<extra></extra>"
            )
            
            fig.update_layout(
                height=350,
                margin=dict(l=10, r=10, t=50, b=10),
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Error by data source - horizontal bar chart
        st.markdown("### Errors by Data Source")
        
        error_by_source = pd.DataFrame({
            "Source": [s["name"] for s in st.session_state.data_sources.values()],
            "Errors": [s["failures"] for s in st.session_state.data_sources.values()],
            "Error Rate (%)": [100 * s["failures"] / max(1, s["records_processed"]) for s in st.session_state.data_sources.values()]
        })
        
        # Sort by error rate
        error_by_source = error_by_source.sort_values("Error Rate (%)", ascending=False)
        
        fig = px.bar(
            error_by_source,
            x="Error Rate (%)",
            y="Source",
            title="Error Rate by Data Source",
            orientation='h',
            color="Error Rate (%)",
            color_continuous_scale="Reds",
            labels={"Source": "Data Source"}
        )
        
        fig.update_traces(
            hovertemplate="%{y}<br>Error Rate: %{x:.2f}%<br>Total Errors: %{customdata}<extra></extra>"
        )
        
        fig.update_layout(
            height=350,
            margin=dict(l=10, r=10, t=50, b=10),
            plot_bgcolor="white",
            xaxis=dict(
                title="Error Rate (%)",
                showgrid=True,
                gridcolor='#E5E7EB',
            ),
            yaxis=dict(
                title="Data Source",
                showgrid=False,
            ),
            coloraxis_showscale=False
        )
        
        # Add custom data for hover tooltip
        fig.update_traces(customdata=error_by_source["Errors"])
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Performance optimization recommendations
    st.markdown('<p class="section-title">Performance Optimization Recommendations</p>', unsafe_allow_html=True)
    
    # Create expandable sections for detailed recommendations
    with st.expander("Resource Allocation Analysis", expanded=True):
        st.markdown("""
        Based on current usage patterns, the following resource optimizations are recommended:
        
        - **Memory Allocation**: Increase memory allocation for Data Validation Workers by 20% to reduce swapping and improve validation throughput
        - **Horizontal Scaling**: Add 2 additional Enrichment Nodes to handle peak loads during business hours (10 AM - 2 PM)
        - **I/O Management**: Implement I/O throttling for Edge Collectors during batch processing windows to prevent network saturation
        - **CPU Optimization**: Enable CPU affinity settings for the Main Processing Cluster to improve cache utilization
        """)
        
        # Add sample code for implementation
        st.code("""
# Example Kubernetes configuration for scaling Enrichment Nodes
apiVersion: apps/v1
kind: Deployment
metadata:
  name: enrichment-nodes
spec:
  replicas: 5  # Increased from 3
  selector:
    matchLabels:
      app: enrichment
  template:
    metadata:
      labels:
        app: enrichment
    spec:
      containers:
      - name: enrichment-service
        image: omnistream/enrichment:v1.2.3
        resources:
          requests:
            memory: "4Gi"
            cpu: "2"
          limits:
            memory: "6Gi"
            cpu: "3"
        """, language="yaml")
    
    with st.expander("Query Optimization Opportunities"):
        st.markdown("""
        Performance analysis has identified the following query optimization opportunities:
        
        - **Indexed Access**: Add covering indexes for frequently accessed time-series data to improve dashboard rendering
        - **Partitioning Strategy**: Implement partitioning for historical data tables by month to improve query performance on large datasets
        - **Materialized Views**: Convert expensive joins in analytical queries to materialized views, updated hourly
        - **Query Caching**: Implement result caching for repetitive analytical patterns with a TTL of 15 minutes
        - **Execution Plans**: Review and optimize execution plans for the top 10 most resource-intensive queries
        """)
        
        # Add sample SQL for implementation
        st.code("""
-- Example SQL for implementing partitioning on time series data
CREATE TABLE metrics_partitioned (
    timestamp TIMESTAMP NOT NULL,
    source_id VARCHAR(50) NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    metric_value NUMERIC NOT NULL,
    PRIMARY KEY (timestamp, source_id, metric_name)
) PARTITION BY RANGE (timestamp);

-- Create monthly partitions
CREATE TABLE metrics_y2023m01 PARTITION OF metrics_partitioned
    FOR VALUES FROM ('2023-01-01') TO ('2023-02-01');
    
CREATE TABLE metrics_y2023m02 PARTITION OF metrics_partitioned
    FOR VALUES FROM ('2023-02-01') TO ('2023-03-01');

-- Create index on commonly queried fields
CREATE INDEX idx_metrics_source_name ON metrics_partitioned(source_id, metric_name);
        """, language="sql")
        
    with st.expander("Infrastructure Scaling Recommendations"):
        st.markdown("""
        Based on usage patterns and growth projections, the following infrastructure changes are recommended:
        
        - **Auto-scaling**: Implement auto-scaling for processing nodes based on queue depth rather than CPU utilization
        - **Resource Quotas**: Adjust resource quotas for batch processing jobs to balance throughput and resource consumption
        - **Load Balancing**: Implement weighted load balancing based on data source complexity profiles
        - **Caching Tier**: Add a distributed caching tier for frequently accessed reference data
        """)
        
        # Add sample architecture diagram
        st.markdown("""
        ```
        ┌──────────────────┐     ┌─────────────────┐     ┌───────────────────┐
        │ INGESTION LAYER  │     │ PROCESSING TIER │     │  SERVING LAYER    │
        │  Auto-scaling    │     │ (Resource Quotas)│     │ (Load Balanced)   │
        │  Based on Queue  │     │                 │     │                   │
        │     Depth        │     │ ┌─────────────┐ │     │ ┌───────────────┐ │
        │                  │     │ │ Validation  │ │     │ │ API Gateway   │ │
        │ ┌──────────────┐ │     │ │ Workers     │ │     │ │ (Rate Limits) │ │
        │ │ Kafka Streams│ │     │ │ 8 pods      │ │     │ └───────────────┘ │
        │ │ with K-NN    ├─┼─────┼▶│ 6 vCPU each │ │     │         │         │
        │ └──────────────┘ │     │ └─────────────┘ │     │         ▼         │
        │         │        │     │         │       │     │ ┌───────────────┐ │
        │         ▼        │     │         ▼       │     │ │ Query Service │ │
        │ ┌──────────────┐ │     │ ┌─────────────┐ │     │ │ with Result   │ │
        │ │ Message      │ │     │ │ Enrichment  │ │     │ │ Caching       │ │
        │ │ Router       ├─┼─────┼▶│ Service     ├─┼─────┼▶└───────────────┘ │
        │ └──────────────┘ │     │ │ 5 pods      │ │     │                   │
        │                  │     │ └─────────────┘ │     │ ┌───────────────┐ │
        │                  │     │                 │     │ │ Data Export   │ │
        │                  │     │                 │     │ │ Service       │ │
        │                  │     │                 │     │ └───────────────┘ │
        └──────────────────┘     └─────────────────┘     └───────────────────┘
                  │                       │                        │
                  └───────────────────────▼────────────────────────┘
                                          │
                               ┌──────────────────────┐
                               │   DISTRIBUTED CACHE  │
                               │     Redis Cluster    │
                               │     15GB memory      │
                               └──────────────────────┘
        ```
        """)

# Add info about the project for GitHub/LinkedIn
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; background-color: #F3F4F6; border-radius: 10px;">
    <h3 style="color: #1E3A8A;">About OmniStream Data Engineering Pipeline</h3>
    <p style="color: #4B5563;">
        This comprehensive data engineering project demonstrates advanced capabilities in real-time data processing,
        quality control, and system monitoring. The pipeline is designed to handle high-throughput data streams
        with a focus on data quality and system performance.
        It is built to be scalable, maintainable, and efficient, with a strong emphasis on observability and
        performance optimization.
    </p>
    <p style="color: #4B5563;">
        Tech stack: Apache Kafka, Apache Spark, Apache Airflow, Prometheus, Grafana, Great Expectations, PostgreSQL, Python, and Docker
    </p>
    <p style="font-size: 0.8rem; color: #6B7280; margin-top: 15px;">
        © 2025 | Project created by Alex Johnson | <a href="https://github.com/username/omnistream" target="_blank">GitHub</a> | <a href="https://linkedin.com/in/username" target="_blank">LinkedIn</a>
    </p>
</div>
""", unsafe_allow_html=True)

# Add auto-refresh to simulate real-time updates (5 seconds)
st.markdown("""
<script>
    // Auto refresh the page every 5 seconds
    setTimeout(function(){
        window.location.reload();
    }, 5000);
</script>
""", unsafe_allow_html=True)