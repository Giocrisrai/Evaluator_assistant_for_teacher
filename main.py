#!/usr/bin/env python3
"""
Script Principal - Sistema de Evaluación con Agentes Inteligentes
Punto de entrada principal para la aplicación
"""

import os
import sys
import argparse
from pathlib import Path

# Agregar src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Función principal que maneja los diferentes modos de ejecución."""
    
    parser = argparse.ArgumentParser(
        description="Sistema de Evaluación con Agentes Inteligentes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Modos de ejecución:
  python main.py app          # Aplicación principal
  python main.py demo         # Demo de agentes
  python main.py test         # Pruebas del sistema
  python main.py config       # Configuración inicial
        """
    )
    
    parser.add_argument("modo", choices=["app", "demo", "test", "config"], 
                       help="Modo de ejecución")
    parser.add_argument("--repo", type=str, help="URL del repositorio")
    parser.add_argument("--student", type=str, help="Nombre del estudiante")
    parser.add_argument("--class", type=str, dest="class_file", help="Archivo CSV")
    
    args = parser.parse_args()
    
    if args.modo == "app":
        # Ejecutar aplicación principal
        from app import main as app_main
        app_main()
    
    elif args.modo == "demo":
        # Ejecutar demo
        from src.demo import main as demo_main
        demo_main()
    
    elif args.modo == "test":
        # Ejecutar pruebas
        from test_app import main as test_main
        test_main()
    
    elif args.modo == "config":
        # Configuración inicial
        from config_simple import main as config_main
        config_main()

if __name__ == "__main__":
    main()
