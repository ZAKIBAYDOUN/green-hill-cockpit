import re

with open('streamlit_app.py', 'r') as f:
    lines = f.readlines()

# Find and fix the setup_environment function
fixed_lines = []
in_function = False
function_start = -1

for i, line in enumerate(lines):
    if 'def setup_environment():' in line:
        in_function = True
        function_start = i
        fixed_lines.append(line)
        # Add the function body if it's missing
        if i + 1 < len(lines) and not lines[i + 1].strip().startswith(('"""', "'''", '#')) and not lines[i + 1].startswith('    '):
            fixed_lines.append('    """Bridge Streamlit secrets to environment variables"""\n')
            fixed_lines.append('    secret_keys = ["LANGGRAPH_API_URL", "LANGGRAPH_API_KEY", "OPENAI_API_KEY",\n')
            fixed_lines.append('                   "DEMO_MODE", "GHC_DT_MODEL", "GHC_DT_TEMPERATURE", "GHC_DT_EVIDENCE_LOG"]\n')
            fixed_lines.append('    \n')
            fixed_lines.append('    for key in secret_keys:\n')
            fixed_lines.append('        try:\n')
            fixed_lines.append('            if key in st.secrets:\n')
            fixed_lines.append('                os.environ[key] = st.secrets[key]\n')
            fixed_lines.append('        except:\n')
            fixed_lines.append('            pass  # Use existing env var or default\n')
    elif in_function and i == function_start + 1 and not line.startswith('    '):
        # Skip this line if it's not indented (we already added the body)
        continue
    else:
        fixed_lines.append(line)
        # Check if we're out of the function
        if in_function and line.strip() and not line.startswith('    '):
            in_function = False

with open('streamlit_app.py', 'w') as f:
    f.writelines(fixed_lines)

print("✅ Fixed indentation in setup_environment function")
