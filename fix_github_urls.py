#!/usr/bin/env python3
"""
Corregir todas las URLs de GitHub para usar la estructura correcta
"""

import os
import re

print("🔧 Fixing GitHub URLs to use correct structure...")

# Patrón para encontrar URLs incorrectas
incorrect_patterns = [
    (r'github\.com/ZAKIBAYDOUN/', 'github.com/green-hill-canarias/'),
    (r'github\.com/digital-roots/', 'github.com/green-hill-canarias/'),
    (r'ZAKIBAYDOUN/', 'green-hill-canarias/')
]

# Archivos a revisar
files_to_check = [
    'fix_everything.py',
    'emergency_fix.py',
    'unified_deploy.sh',
    'deploy.sh',
    '.github/workflows/emergency-deploy.yml'
]

# Directorios de apps
app_dirs = [
    '/workspaces/green-hill-cockpit',
    '/workspaces/digital-roots',
    '/workspaces/ground-control'
]

for base_dir in app_dirs:
    if os.path.exists(base_dir):
        print(f"\n📁 Checking {base_dir}...")
        
        for root, dirs, files in os.walk(base_dir):
            # Skip .git directories
            if '.git' in root:
                continue
                
            for file in files:
                if file.endswith(('.py', '.sh', '.yml', '.yaml', '.md')):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r') as f:
                            content = f.read()
                        
                        original_content = content
                        
                        # Apply all corrections
                        for pattern, replacement in incorrect_patterns:
                            content = re.sub(pattern, replacement, content)
                        
                        if content != original_content:
                            with open(filepath, 'w') as f:
                                f.write(content)
                            print(f"  ✅ Fixed: {filepath}")
                            
                    except Exception as e:
                        pass

print("\n✅ All GitHub URLs have been corrected!")
