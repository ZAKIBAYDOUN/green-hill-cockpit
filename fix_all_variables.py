#!/usr/bin/env python3
import re

# Leer el archivo actual
with open('streamlit_app.py', 'r') as f:
    content = f.read()

# Asegurarnos que os está importado
if 'import os' not in content:
    content = 'import os\n' + content

# Eliminar definiciones parciales o corruptas
content = re.sub(r'LANGGRAPH_API_URL = os\.getenv.*?EOFnt.*?langgraph\.app"\)', 
                'LANGGRAPH_API_URL = os.getenv("LANGGRAPH_API_URL", "https://cockpit-c5fbf013b8495301890e442307c38955.us.langgraph.app")', 
                content)

# Bloque completo de configuración API
api_config_block = '''
# API Configuration
LANGGRAPH_API_URL = os.getenv("LANGGRAPH_API_URL", "https://cockpit-c5fbf013b8495301890e442307c38955.us.langgraph.app")
LANGGRAPH_API_KEY = os.getenv("LANGGRAPH_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEMO_MODE = os.getenv("DEMO_MODE", "false")
GHC_DT_MODEL = os.getenv("GHC_DT_MODEL", "gpt-4o-mini")
GHC_DT_TEMPERATURE = os.getenv("GHC_DT_TEMPERATURE", "0.2")
GHC_DT_EVIDENCE_LOG = os.getenv("GHC_DT_EVIDENCE_LOG", "evidence.jsonl")
'''

# Buscar dónde insertar el bloque de configuración
if 'setup_environment()' in content:
    # Añadir después de setup_environment()
    content = re.sub(r'(setup_environment\(\))', r'\1\n' + api_config_block, content)
else:
    # Añadir después de las importaciones
    import_section_end = 0
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.strip() and not (line.startswith('import') or line.startswith('from')):
            if i > 10:  # Asegurarnos que no estamos al principio del archivo
                import_section_end = i
                break
    
    if import_section_end > 0:
        lines.insert(import_section_end, api_config_block)
        content = '\n'.join(lines)

# Eliminar definiciones duplicadas de las mismas variables
# Hacemos esto encontrando todas las ocurrencias y conservando solo la primera
variables = ['LANGGRAPH_API_URL', 'LANGGRAPH_API_KEY', 'OPENAI_API_KEY', 
             'DEMO_MODE', 'GHC_DT_MODEL', 'GHC_DT_TEMPERATURE', 'GHC_DT_EVIDENCE_LOG']

lines = content.split('\n')
seen_vars = set()
filtered_lines = []

for line in lines:
    skip = False
    for var in variables:
        if line.strip().startswith(f"{var} = "):
            if var in seen_vars:
                skip = True
                break
            seen_vars.add(var)
    
    if not skip:
        filtered_lines.append(line)

content = '\n'.join(filtered_lines)

# Escribir archivo actualizado
with open('streamlit_app.py', 'w') as f:
    f.write(content)

print("✅ Configuración API completamente reparada")
