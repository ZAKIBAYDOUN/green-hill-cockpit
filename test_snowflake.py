import streamlit as st
import pandas as pd

st.title("Snowflake Connection Test")

try:
    # Get connection
    conn = st.connection("snowflake")
    
    # Test query
    df = conn.query("SELECT CURRENT_VERSION() as VERSION, CURRENT_USER() as USER, CURRENT_ROLE() as ROLE")
    
    st.success("✅ Connected to Snowflake!")
    st.dataframe(df)
    
    # Show account info
    account_info = conn.query("SELECT CURRENT_ACCOUNT() as ACCOUNT, CURRENT_WAREHOUSE() as WAREHOUSE, CURRENT_DATABASE() as DATABASE")
    st.write("Account Info:")
    st.dataframe(account_info)
    
except Exception as e:
    st.error(f"❌ Connection failed: {str(e)}")
    st.info("Make sure Snowflake credentials are configured in secrets.toml")
