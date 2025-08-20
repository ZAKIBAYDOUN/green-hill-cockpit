import re

with open('streamlit_app.py', 'r') as f:
    content = f.read()

# Replace the setup_environment function with a properly indented version
new_function = '''def setup_environment():
    """Bridge Streamlit secrets to environment variables"""
    secret_keys = ["LANGGRAPH_API_URL", "LANGGRAPH_API_KEY", "OPENAI_API_KEY", 
                   "DEMO_MODE", "GHC_DT_MODEL", "GHC_DT_TEMPERATURE", "GHC_DT_EVIDENCE_LOG"]
    
    for key in secret_keys:
        try:
            if key in st.secrets:
                os.environ[key] = st.secrets[key]
        except:
            pass  # Use existing env var or default

setup_environment()'''

# Find and replace the function
pattern = r'def setup_environment\(\):.*?setup_environment\(\)'
content_fixed = re.sub(pattern, new_function, content, flags=re.DOTALL)

with open('streamlit_app.py', 'w') as f:
    f.write(content_fixed)

print("✅ Fixed setup_environment function")
