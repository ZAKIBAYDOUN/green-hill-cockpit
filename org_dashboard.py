import streamlit as st
import json
import requests
from datetime import datetime

st.set_page_config(
    page_title="🌿 Cannabis Empire Dashboard",
    page_icon="🌿",
    layout="wide"
)

# Load discovered structure
try:
    with open("emergency_config.json", "r") as f:
        config = json.load(f)
        structure = config.get("discovered_structure", {})
except:
    st.error("❌ Emergency config not found. Run fix_nested_orgs.py first!")
    st.stop()

st.title("🌿 Cannabis Empire: Nested Organizations Dashboard")
st.caption("For: ZAKIBAYDOUN (Pharmacist & Cannabis Tech Entrepreneur)")

# Organization overview
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏢 Parent Org: green-hill-canarias")
    if "parent" in structure.get("organizations", {}):
        parent = structure["organizations"]["parent"]
        st.metric("Public Repos", parent.get("public_repos", 0))
        st.metric("Private Repos", parent.get("private_repos", 0))
        st.metric("Members", parent.get("members_count", 0))
    else:
        st.warning("⚠️  Parent org not accessible")

with col2:
    st.subheader("💻 Child Org: digital-roots")
    if "child" in structure.get("organizations", {}):
        child = structure["organizations"]["child"]
        st.metric("Public Repos", child.get("public_repos", 0))
        st.metric("Private Repos", child.get("private_repos", 0))
        st.metric("Members", child.get("members_count", 0))
    else:
        st.warning("⚠️  Child org not accessible")

# Cannabis apps status
st.subheader("🌿 Cannabis Applications Status")

cannabis_apps = structure.get("cannabis_apps_found", [])
if cannabis_apps:
    for app in cannabis_apps:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.write(f"📱 **{app['name']}**")
        with col2:
            st.write(f"📍 {app['location']}")
        with col3:
            st.write(f"🏢 {app['org_name']}")
        with col4:
            if app['location'] == 'user_repos':
                st.success("✅ Accessible")
            else:
                st.warning("⚠️  Check permissions")
else:
    st.error("❌ No cannabis apps found!")

# Recommendations
st.subheader("💡 Emergency Recommendations")
recommendations = structure.get("recommendations", [])
for i, rec in enumerate(recommendations, 1):
    with st.expander(f"Recommendation {i}: {rec.get('issue', 'Unknown')}"):
        st.write(f"**Solution:** {rec.get('solution', 'No solution provided')}")
        st.code(rec.get('action', 'No action specified'))
        st.info(rec.get('why', 'No explanation provided'))

# Emergency actions
st.subheader("🚨 Emergency Actions")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 Refresh Structure"):
        st.rerun()

with col2:
    if st.button("🚀 Emergency Deploy All"):
        st.code("bash unified_deploy.sh")
        
with col3:
    if st.button("📊 Export Report"):
        st.download_button(
            "Download Structure Report",
            json.dumps(structure, indent=2),
            "cannabis_org_structure.json",
            "application/json"
        )

# Footer
st.markdown("---")
st.caption("🌿 Cannabis Empire Management • Emergency Response System")
st.caption("Pharmacist-friendly org structure visualization")
