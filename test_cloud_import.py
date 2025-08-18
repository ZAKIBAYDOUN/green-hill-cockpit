#!/usr/bin/env python3
"""
Simula exactamente lo que hace LangGraph Cloud para importar los graphs
"""

def test_langgraph_cloud_import():
    """Simula el proceso de importación de LangGraph Cloud"""
    import json
    import importlib.util
    import sys
    from pathlib import Path
    
    # Cargar configuración
    with open('langgraph.json', 'r') as f:
        config = json.load(f)
    
    print("🔍 Simulando proceso de importación de LangGraph Cloud...")
    print(f"📋 Configuración: {config}")
    
    # Probar cada graph según el formato esperado por LangGraph Cloud
    for graph_name, graph_path in config['graphs'].items():
        print(f"\n🧪 Probando graph '{graph_name}': {graph_path}")
        
        # Parsear el path del graph (formato: ./file.py:attribute)
        if ':' not in graph_path:
            print(f"❌ Error: Path '{graph_path}' no tiene formato './file.py:attribute'")
            continue
            
        module_path, attr_name = graph_path.split(':')
        print(f"  📄 Módulo: {module_path}")
        print(f"  🔗 Atributo: {attr_name}")
        
        # Verificar que el archivo existe
        file_path = Path(module_path)
        if not file_path.exists():
            print(f"❌ Error: Archivo '{module_path}' no existe")
            continue
        print(f"  ✅ Archivo existe: {file_path.absolute()}")
        
        try:
            # Importar el módulo dinámicamente (como hace LangGraph Cloud)
            spec = importlib.util.spec_from_file_location("temp_module", file_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules["temp_module"] = module
            spec.loader.exec_module(module)
            print(f"  ✅ Módulo cargado exitosamente")
            
            # Verificar que el atributo existe
            if not hasattr(module, attr_name):
                print(f"❌ Error: Atributo '{attr_name}' no encontrado en módulo")
                continue
            
            graph_obj = getattr(module, attr_name)
            print(f"  ✅ Graph encontrado: {type(graph_obj)}")
            
            # Verificar que es un graph compilado de LangGraph
            if 'CompiledStateGraph' not in str(type(graph_obj)):
                print(f"❌ Warning: Graph no es CompiledStateGraph: {type(graph_obj)}")
            else:
                print(f"  ✅ Graph es válido: CompiledStateGraph")
                
        except Exception as e:
            print(f"❌ Error al importar: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n🎯 Simulación de importación completada!")

if __name__ == "__main__":
    test_langgraph_cloud_import()