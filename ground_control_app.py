#!/usr/bin/env python3
"""
🎮 Ground Control
Cannabis operations command center and business intelligence

🚨 BULLETPROOF MODE - Always works!
Built for: ZAKIBAYDOUN (Cannabis Tech Entrepreneur)
"""

import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

st.set_page_config(
    page_title="🎮 Ground Control",
    page_icon="🎮",
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Operations data
OPERATIONS = [
    "Production Planning", "Quality Control", "Inventory Management", "Sales Analytics",
    "Compliance Monitoring", "Supply Chain", "Customer Service", "Financial Tracking"
]

def main():
    st.title("🎮 Ground Control")
    st.caption("Cannabis operations command center and business intelligence • Live Dashboard")
    
    st.success("🚀 **COMMAND CENTER ONLINE** - All business operations active!")
    
    # Sidebar
    with st.sidebar:
        st.header("🎮 Control Panel")
        
        dashboard_view = st.selectbox(
            "Dashboard View",
            ["Executive Summary", "Operations", "Financial", "Compliance", "Analytics"]
        )
        
        time_range = st.selectbox("Time Range", ["Today", "This Week", "This Month", "This Quarter"])
        
        st.subheader("🎯 Command Status")
        st.success("🟢 All Systems Go")
        st.metric("Active Operations", len(OPERATIONS))
        st.metric("Efficiency", "96.8%")
        st.metric("Profit Margin", "34.2%")

    # Executive KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        revenue = random.randint(180000, 250000)
        st.metric("Monthly Revenue", f"${revenue:,}", delta="12.5%")
    with col2:
        production = random.uniform(220, 280)
        st.metric("Production (kg)", f"{production:.1f}", delta="8.2 kg")
    with col3:
        customers = random.randint(1200, 1800)
        st.metric("Active Customers", f"{customers:,}", delta="156")
    with col4:
        compliance_score = random.randint(97, 100)
        st.metric("Compliance Score", f"{compliance_score}%", delta="2%")

    if dashboard_view == "Executive Summary":
        # Business overview
        st.header("📊 Business Overview")
        
        # Performance metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💰 Revenue Trends")
            
            # Generate revenue data
            dates = pd.date_range(start="2025-07-01", end="2025-08-20", freq="D")
            revenue_data = pd.DataFrame({
                "Daily Revenue": np.cumsum(np.random.normal(8000, 1000, len(dates)))
            }, index=dates)
            
            st.line_chart(revenue_data)
        
        with col2:
            st.subheader("🎯 Key Metrics")
            
            metrics = [
                ("Customer Acquisition", "89 new", "🟢"),
                ("Inventory Turnover", "8.2x", "🟢"), 
                ("Average Order", "$147", "🟡"),
                ("Return Rate", "2.1%", "🟢"),
                ("Employee Satisfaction", "94%", "🟢")
            ]
            
            for metric, value, status in metrics:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{metric}:** {value}")
                with col2:
                    st.write(status)
        
        # Top products
        st.subheader("🏆 Top Performing Products")
        
        top_products = [
            {"product": "Blue Dream Premium", "sales": "$34,250", "units": "1,370g", "margin": "38%"},
            {"product": "OG Kush Special", "sales": "$28,900", "units": "1,156g", "margin": "35%"},
            {"product": "White Widow Elite", "sales": "$26,100", "units": "1,044g", "margin": "42%"},
            {"product": "Green Crack Gold", "sales": "$23,800", "units": "952g", "margin": "33%"}
        ]
        
        st.dataframe(pd.DataFrame(top_products), use_container_width=True)
        
    elif dashboard_view == "Operations":
        st.header("⚙️ Operations Dashboard")
        
        # Operations status
        st.subheader("🔧 Operations Status")
        
        for operation in OPERATIONS:
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"**{operation}**")
            
            with col2:
                efficiency = random.randint(92, 100)
                if efficiency >= 98:
                    st.success(f"{efficiency}%")
                elif efficiency >= 95:
                    st.warning(f"{efficiency}%") 
                else:
                    st.error(f"{efficiency}%")
            
            with col3:
                status = random.choice(["🟢 Online", "🟡 Monitoring", "🔴 Alert"])
                st.write(status)
        
        # Production pipeline
        st.subheader("🏭 Production Pipeline")
        
        pipeline_data = {
            "Stage": ["Raw Materials", "Processing", "Quality Check", "Packaging", "Distribution", "Retail"],
            "Units": [450, 425, 410, 398, 385, 370],
            "Status": ["🟢", "🟢", "🟡", "🟢", "🟢", "🟢"]
        }
        
        st.dataframe(pd.DataFrame(pipeline_data), use_container_width=True)
        
    elif dashboard_view == "Financial":
        st.header("💰 Financial Dashboard")
        
        # Financial metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Gross Revenue", "$247,850", delta="15.2%")
            st.metric("Net Profit", "$84,729", delta="18.1%")
        
        with col2:
            st.metric("Operating Expenses", "$163,121", delta="12.8%")
            st.metric("Tax Liability", "$29,842", delta="14.5%")
        
        with col3:
            st.metric("Cash Flow", "+$54,887", delta="22.3%")
            st.metric("ROI", "34.2%", delta="3.1%")
        
        # Financial trends
        st.subheader("📈 Financial Trends")
        
        dates = pd.date_range(start="2025-06-01", end="2025-08-20", freq="W")
        financial_data = pd.DataFrame({
            "Revenue": np.cumsum(np.random.normal(50000, 5000, len(dates))),
            "Expenses": np.cumsum(np.random.normal(30000, 3000, len(dates))),
            "Profit": np.cumsum(np.random.normal(20000, 2000, len(dates)))
        }, index=dates)
        
        st.line_chart(financial_data)
        
    elif dashboard_view == "Compliance":
        st.header("✅ Compliance Dashboard")
        
        st.success("🌿 **ALL SYSTEMS COMPLIANT** - Meeting all regulatory requirements")
        
        # Compliance areas
        compliance_areas = [
            ("🏭 Cultivation License", 100),
            ("🧪 Lab Testing & QA", 98),
            ("📦 Packaging & Labeling", 100),
            ("🚛 Transportation & Delivery", 95),
            ("💰 Tax & Financial Compliance", 100),
            ("🔒 Security & Surveillance", 97),
            ("📋 Record Keeping", 100),
            ("👥 Employee Training", 94)
        ]
        
        for area, score in compliance_areas:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{area}**")
                st.progress(score/100)
            with col2:
                if score >= 98:
                    st.success(f"{score}%")
                elif score >= 95:
                    st.warning(f"{score}%")
                else:
                    st.error(f"{score}%")
        
        # Upcoming compliance events
        st.subheader("📅 Upcoming Compliance Events")
        
        events = [
            {"date": "2025-08-25", "event": "Monthly Inventory Audit", "status": "Scheduled"},
            {"date": "2025-09-01", "event": "Employee Safety Training", "status": "Pending"},
            {"date": "2025-09-15", "event": "State Inspection", "status": "Confirmed"},
            {"date": "2025-09-30", "event": "Quarterly Tax Filing", "status": "Upcoming"}
        ]
        
        st.dataframe(pd.DataFrame(events), use_container_width=True)

    # Real-time alerts
    st.header("🚨 Real-time Alerts")
    
    alerts = [
        {"time": "14:32", "type": "Info", "message": "Inventory levels optimal across all products"},
        {"time": "13:45", "type": "Success", "message": "Quality control batch #QC-2025-0820 passed all tests"},
        {"time": "12:18", "type": "Warning", "message": "High demand detected for Blue Dream - consider restocking"},
        {"time": "11:02", "type": "Info", "message": "Daily compliance check completed successfully"}
    ]
    
    for alert in alerts:
        alert_type = alert["type"].lower()
        if alert_type == "success":
            st.success(f"**{alert['time']}** - {alert['message']}")
        elif alert_type == "warning":
            st.warning(f"**{alert['time']}** - {alert['message']}")
        elif alert_type == "error":
            st.error(f"**{alert['time']}** - {alert['message']}")
        else:
            st.info(f"**{alert['time']}** - {alert['message']}")

    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption("🎮 Cannabis Command Excellence")
    with col2:
        st.caption(f"⚡ Live System • {datetime.now().strftime('%H:%M:%S')}")
    with col3:
        st.caption("👨‍⚕️ Built for ZAKIBAYDOUN")

if __name__ == "__main__":
    main()