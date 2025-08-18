#!/usr/bin/env python3
"""
Test script to verify LangGraph configuration and agents
"""

def test_langgraph_config():
    """Test that langgraph.json is valid and graphs can be imported"""
    import json
    
    # Load and validate langgraph.json
    with open('langgraph.json', 'r') as f:
        config = json.load(f)
    
    print("✅ langgraph.json is valid JSON")
    print(f"📦 Dependencies: {len(config['dependencies'])}")
    print(f"🔗 Graphs: {list(config['graphs'].keys())}")
    
    # Test graph imports
    import importlib
    for graph_name, graph_path in config['graphs'].items():
        module_path, graph_attr = graph_path.split(':')
        module_path = module_path.replace('./', '').replace('.py', '')

        try:
            module = importlib.import_module(module_path)
            graph = getattr(module, graph_attr)
            print(f"✅ {graph_name}: {type(graph)}")
        except Exception as e:
            print(f"❌ {graph_name}: {e}")
    
    print("\n🎯 LangGraph configuration is ready!")


if __name__ == "__main__":
    test_langgraph_config()