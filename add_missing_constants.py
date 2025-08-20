with open('streamlit_app.py', 'r') as f:
    content = f.read()

# Add all missing constants after imports
constants_to_add = []

if 'AGENTS = {' not in content:
    constants_to_add.append('''
AGENTS = {
    "ghc_dt": "CEO Digital Twin",
    "strategy": "Strategy Advisor",
    "finance": "Finance Advisor",
    "operations": "Operations Advisor",
    "market": "Market Advisor",
    "risk": "Risk Advisor",
    "compliance": "Compliance Advisor",
    "innovation": "Innovation Advisor",
    "code": "Code Assistant"
}''')

if 'COMMANDS = {' not in content:
    constants_to_add.append('''
COMMANDS = {
    "analyze": "Analyze current situation",
    "recommend": "Get recommendations",
    "forecast": "Generate forecasts",
    "report": "Generate report",
    "simulate": "Run simulation",
    "optimize": "Optimize strategy"
}''')

if constants_to_add:
    # Find where to insert
    lines = content.split('\n')
    insert_pos = 0
    
    # Find after setup_environment() call
    for i, line in enumerate(lines):
        if 'setup_environment()' in line:
            insert_pos = i + 1
            break
    
    # Insert constants
    for const in constants_to_add:
        lines.insert(insert_pos, const)
        insert_pos += 1
    
    content = '\n'.join(lines)
    
    with open('streamlit_app.py', 'w') as f:
        f.write(content)
    
    print("✅ Added missing constants")

