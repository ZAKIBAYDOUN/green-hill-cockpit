import re

with open('streamlit_app.py', 'r') as f:
    content = f.read()

# Define the correctly indented function
correct_function = '''def setup_environment():
    """Bridge Streamlit secrets to environment variables"""
    secret_keys = ["LANGGRAPH_API_URL", "LANGGRAPH_API_KEY", "OPENAI_API_KEY", 
                   "DEMO_MODE", "GHC_DT_MODEL", "GHC_DT_TEMPERATURE", "GHC_DT_EVIDENCE_LOG"]
    
    for key in secret_keys:
        try:
            if key in st.secrets:
                os.environ[key] = st.secrets[key]
        except:
            pass  # Use existing env var or default'''

# Find the setup_environment function and replace it
pattern = r'def setup_environment\(\):.*?(?=\n(?:def|class|\Z))'
content = re.sub(pattern, correct_function, content, flags=re.DOTALL)

# Write back
with open('streamlit_app.py', 'w') as f:
    f.write(content)

print("✅ Replaced setup_environment function with correct indentation")
