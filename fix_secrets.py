# Find the line with setup_environment() call and ensure it's executed

import fileinput
import sys

found_setup = False
for line in fileinput.input('streamlit_app.py', inplace=True):
    print(line, end='')
    if 'def setup_environment():' in line:
        found_setup = True
    if found_setup and 'setup_environment()' in line and not line.strip().startswith('#'):
        print("# Ensure setup_environment is called", file=sys.stderr)

# Check if setup_environment() is called after the function definition
with open('streamlit_app.py', 'r') as f:
    content = f.read()
    if 'setup_environment()' not in content.split('def setup_environment():')[1].split('def')[0]:
        print("WARNING: setup_environment() is not being called!", file=sys.stderr)
