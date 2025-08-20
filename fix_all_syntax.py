import re

with open('streamlit_app.py', 'r') as f:
    content = f.read()

# Fix function definitions with incorrect return type syntax
# Pattern: def function_name(): -> Type:
# Should be: def function_name() -> Type:
content = re.sub(r'def (\w+)\(\): -> ', r'def \1() -> ', content)

# Fix any Dict[str, Any] import issues
if 'from typing import' in content and 'Dict' not in content.split('from typing import')[1].split('\n')[0]:
    content = content.replace('from typing import', 'from typing import Dict, Any,')

# Make sure typing imports are present
if 'from typing import' not in content:
    # Add typing import after other imports
    lines = content.split('\n')
    import_index = 0
    for i, line in enumerate(lines):
        if line.startswith('import ') or line.startswith('from '):
            import_index = i
    lines.insert(import_index + 1, 'from typing import Dict, Any, List, Optional')
    content = '\n'.join(lines)

with open('streamlit_app.py', 'w') as f:
    f.write(content)

print("✅ Fixed all function syntax errors")
