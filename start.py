#!/usr/bin/env python3
"""
Script de Inicio Rápido
Guía interactiva para comenzar a usar el sistema
"""

import os
import sys
from pathlib import Path

def print_welcome():
    """Muestra mensaje de bienvenida."""
    print("🤖" + "="*60 + "🤖")
    print("   SISTEMA DE EVALUACIÓN CON AGENTES INTELIGENTES")
    print("   Guía de Inicio Rápido")
    print("🤖" + "="*60 + "🤖")

def check_installation():
    """Verifica la instalación básica."""
    print("\n🔍 VERIFICANDO INSTALACIÓN...")
    
    # Verificar archivos principales
    required_files = [
        "src/config.py",
        "src/rubrica_evaluator.py", 
        "src/agents_manager.py",
        "src/agents/analysis_agent.py",
        "src/agents/recommendation_agent.py",
        "src/agents/monitoring_agent.py",
        "requirements.txt"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Archivos faltantes:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ Todos los archivos principales están presentes")
    return True

def check_dependencies():
    """Verifica las dependencias."""
    print("\n📦 VERIFICANDO DEPENDENCIAS...")
    
    try:
        import openai
        import github
        import pandas
        import plotly
        print("✅ Dependencias principales instaladas")
        return True
    except ImportError as e:
        print(f"❌ Dependencias faltantes: {e}")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return False

def check_configuration():
    """Verifica la configuración."""
    print("\n🔧 VERIFICANDO CONFIGURACIÓN...")
    
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ Archivo .env no encontrado")
        print("💡 Ejecuta: python config_simple.py")
        return False
    
    try:
        sys.path.append("src")
        from src.config import Config
        
        if Config.validate_config():
            print("✅ Configuración válida")
            return True
        else:
            print("❌ Configuración incompleta")
            print("💡 Ejecuta: python config_simple.py")
            return False
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

def show_quick_start():
    """Muestra guía de inicio rápido."""
    print("\n🚀 GUÍA DE INICIO RÁPIDO")
    print("="*50)
    
    steps = [
        "1. Configurar el sistema:",
        "   python config_simple.py",
        "",
        "2. Probar el sistema:",
        "   python main.py test",
        "",
        "3. Ver demo de capacidades:",
        "   python main.py demo",
        "",
        "4. Evaluar un repositorio:",
        "   python main.py app --repo https://github.com/kedro-org/kedro-starters",
        "",
        "5. Evaluar una clase completa:",
        "   python main.py app --class examples/estudiantes_ejemplo.csv"
    ]
    
    for step in steps:
        print(step)

def show_examples():
    """Muestra ejemplos de uso."""
    print("\n📚 EJEMPLOS DE USO")
    print("="*50)
    
    examples = [
        "# Evaluación individual",
        "python main.py app --repo https://github.com/usuario/proyecto",
        "",
        "# Con información del estudiante", 
        "python main.py app --repo https://github.com/usuario/proyecto --student 'Juan Pérez'",
        "",
        "# Evaluación masiva",
        "python main.py app --class examples/estudiantes_ejemplo.csv",
        "",
        "# Modo interactivo",
        "python main.py app",
        "",
        "# Demo completo",
        "python main.py demo"
    ]
    
    for example in examples:
        print(example)

def main():
    """Función principal."""
    
    print_welcome()
    
    # Verificaciones
    checks = [
        ("Instalación", check_installation),
        ("Dependencias", check_dependencies), 
        ("Configuración", check_configuration)
    ]
    
    all_good = True
    for check_name, check_func in checks:
        if not check_func():
            all_good = False
    
    if all_good:
        print("\n🎉 ¡SISTEMA LISTO PARA USAR!")
        print("="*50)
        show_quick_start()
        
        print("\n" + "="*50)
        print("📚 EJEMPLOS DE USO DISPONIBLES:")
        show_examples()
        
        print("\n" + "="*50)
        print("🚀 PARA EJECUTAR EL DEMO:")
        print("python main.py demo")
        print("\n🚀 PARA EVALUAR UN REPOSITORIO:")
        print("python main.py app --repo https://github.com/kedro-org/kedro-starters")
    
    else:
        print("\n⚠️  CONFIGURACIÓN REQUERIDA")
        print("="*50)
        print("Sigue estos pasos para configurar el sistema:")
        print("1. Instalar dependencias: pip install -r requirements.txt")
        print("2. Configurar tokens: python config_simple.py")
        print("3. Verificar configuración: python validate.py")
        print("4. Ejecutar este script nuevamente: python start.py")

if __name__ == "__main__":
    main()
