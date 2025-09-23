#!/usr/bin/env python3
"""
Script de prueba rápida
Verifica que todo esté funcionando correctamente
"""

import os
import sys
from pathlib import Path

def test_imports():
    """Prueba que todos los módulos se importen correctamente."""
    
    print("🧪 Probando imports...")
    
    try:
        # Agregar src al path
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        
        # Importar módulos principales
        from src.config import Config
        from src.rubrica_evaluator import RubricaEvaluator, create_kedro_rubrica
        from src.agents_manager import AgentsManager
        
        print("✅ Todos los módulos se importan correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en imports: {e}")
        return False

def test_configuration():
    """Prueba la configuración."""
    
    print("🔧 Probando configuración...")
    
    try:
        from src.config import Config
        
        if not Config.validate_config():
            print("❌ Configuración incompleta")
            print("💡 Ejecuta: python config_simple.py")
            return False
        
        print("✅ Configuración válida")
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

def test_agents():
    """Prueba los agentes."""
    
    print("🤖 Probando agentes...")
    
    try:
        from src.agents_manager import AgentsManager
        
        manager = AgentsManager()
        print("✅ Agentes inicializados correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en agentes: {e}")
        return False

def test_rubrica():
    """Prueba la creación de rúbrica."""
    
    print("📊 Probando rúbrica...")
    
    try:
        from src.rubrica_evaluator import create_kedro_rubrica
        
        rubrica = create_kedro_rubrica()
        
        if len(rubrica['criterios']) != 10:
            print(f"❌ Rúbrica incompleta: {len(rubrica['criterios'])} criterios")
            return False
        
        print("✅ Rúbrica Kedro creada correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en rúbrica: {e}")
        return False

def run_quick_test():
    """Ejecuta una prueba rápida del sistema."""
    
    print("🚀 Ejecutando prueba rápida...")
    
    try:
        from src.agents_manager import AgentsManager
        
        # Repositorio simple para prueba
        test_repo = "https://github.com/octocat/Hello-World"
        
        print(f"📍 Probando con: {test_repo}")
        
        manager = AgentsManager()
        results = manager.evaluate_with_agents(test_repo)
        
        print("✅ Prueba rápida completada")
        print(f"   Nota: {results['evaluacion_basica']['nota_final']}/7.0")
        print(f"   Insights: {len(results['insights'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en prueba rápida: {e}")
        return False

def main():
    """Función principal."""
    
    print("🧪 PRUEBA DEL SISTEMA DE EVALUACIÓN")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Configuración", test_configuration),
        ("Agentes", test_agents),
        ("Rúbrica", test_rubrica)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} falló")
    
    print(f"\n📊 RESULTADOS: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("✅ El sistema está listo para usar")
        
        # Preguntar si ejecutar prueba rápida
        response = input("\n🚀 ¿Ejecutar prueba rápida con repositorio real? (s/n): ")
        if response.lower() == 's':
            run_quick_test()
        
        print(f"\n🎯 PRÓXIMOS PASOS:")
        print("   python app.py          # Aplicación principal")
        print("   python demo_agentes.py # Demo completo")
        
    else:
        print("⚠️  Algunas pruebas fallaron")
        print("💡 Revisa los errores arriba y ejecuta:")
        print("   python config_simple.py")

if __name__ == "__main__":
    main()
