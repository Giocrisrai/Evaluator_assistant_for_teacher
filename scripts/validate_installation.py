#!/usr/bin/env python
"""
Script de Validación de Instalación del Sistema de Evaluación Kedro ML
Verifica que todos los componentes estén correctamente instalados
"""

import os
import sys
import subprocess
import importlib
from pathlib import Path

# Colores para output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def check(condition, message, error_msg=""):
    """Verifica una condición y muestra el resultado."""
    if condition:
        print(f"{Colors.GREEN}✓{Colors.END} {message}")
        return True
    else:
        print(f"{Colors.RED}✗{Colors.END} {message}")
        if error_msg:
            print(f"  {Colors.YELLOW}→ {error_msg}{Colors.END}")
        return False

def check_python_version():
    """Verifica la versión de Python."""
    version = sys.version_info
    valid = version.major == 3 and version.minor >= 8
    return check(
        valid,
        f"Python {version.major}.{version.minor}.{version.micro}",
        "Se requiere Python 3.8 o superior" if not valid else ""
    )

def check_required_packages():
    """Verifica que los paquetes requeridos estén instalados."""
    packages = {
        'github': 'PyGithub',
        'yaml': 'PyYAML',
        'pandas': 'pandas',
        'requests': 'requests',
        'openpyxl': 'openpyxl'
    }
    
    all_installed = True
    print(f"\n{Colors.BOLD}Verificando paquetes Python:{Colors.END}")
    
    for module, package in packages.items():
        try:
            importlib.import_module(module)
            check(True, f"{package} instalado")
        except ImportError:
            check(False, f"{package} no encontrado", f"Instalar con: pip install {package}")
            all_installed = False
    
    return all_installed

def check_github_token():
    """Verifica que el GitHub token esté configurado."""
    token = os.getenv('GITHUB_TOKEN')
    if token:
        masked_token = token[:7] + '...' + token[-4:] if len(token) > 11 else 'TOKEN'
        return check(True, f"GitHub Token configurado ({masked_token})")
    else:
        return check(
            False,
            "GitHub Token no configurado",
            "Exportar variable: export GITHUB_TOKEN='tu_token_aqui'"
        )

def check_ollama():
    """Verifica que Ollama esté instalado y funcionando."""
    print(f"\n{Colors.BOLD}Verificando Ollama:{Colors.END}")
    
    # Verificar instalación
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        ollama_installed = result.returncode == 0
    except FileNotFoundError:
        ollama_installed = False
    
    if not check(ollama_installed, "Ollama instalado", "Instalar desde https://ollama.ai"):
        return False
    
    # Verificar servicio
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=2)
        service_running = response.status_code == 200
    except:
        service_running = False
    
    if not check(service_running, "Servicio Ollama activo", "Iniciar con: ollama serve"):
        return False
    
    # Verificar modelos
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            models = result.stdout.strip().split('\n')[1:]  # Skip header
            if models:
                print(f"{Colors.GREEN}✓{Colors.END} Modelos disponibles:")
                for model in models[:3]:  # Mostrar máximo 3
                    print(f"  • {model.split()[0]}")
                return True
            else:
                return check(False, "No hay modelos", "Descargar con: ollama pull llama2")
    except:
        pass
    
    return False

def check_project_structure():
    """Verifica la estructura del proyecto."""
    print(f"\n{Colors.BOLD}Verificando estructura del proyecto:{Colors.END}")
    
    base_path = Path(__file__).parent.parent
    required_files = [
        'src/kedro_evaluator.py',
        'examples/rubrica_kedro.py',
        'scripts/evaluate_batch.py',
        'data/estudiantes_kedro.csv'
    ]
    
    all_present = True
    for file in required_files:
        path = base_path / file
        exists = path.exists()
        check(exists, f"{file}")
        all_present = all_present and exists
    
    return all_present

def check_sample_evaluation():
    """Intenta hacer una evaluación de prueba."""
    print(f"\n{Colors.BOLD}Prueba de evaluación:{Colors.END}")
    
    try:
        # Intentar importar el evaluador
        sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
        from kedro_evaluator import KedroEvaluator
        
        check(True, "Módulo de evaluación importado correctamente")
        
        # Verificar que se puede crear una instancia
        token = os.getenv('GITHUB_TOKEN', 'dummy_token')
        evaluator = KedroEvaluator(token)
        check(True, "Evaluador inicializado correctamente")
        
        return True
    except Exception as e:
        check(False, "Error en módulo de evaluación", str(e))
        return False

def generate_test_command():
    """Genera un comando de prueba."""
    print(f"\n{Colors.BOLD}Comando de prueba sugerido:{Colors.END}")
    print(f"{Colors.YELLOW}python scripts/evaluate_batch.py \\")
    print(f"  --csv data/estudiantes_kedro.csv \\")
    print(f"  --output evaluaciones_test \\")
    print(f"  --parallel 2{Colors.END}")

def main():
    """Función principal de validación."""
    print(f"{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}Sistema de Evaluación Automática para Proyectos Kedro ML{Colors.END}")
    print(f"{Colors.BOLD}Validación de Instalación{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}")
    
    all_checks_passed = True
    
    # Verificaciones básicas
    print(f"\n{Colors.BOLD}Verificando requisitos básicos:{Colors.END}")
    all_checks_passed &= check_python_version()
    all_checks_passed &= check_required_packages()
    all_checks_passed &= check_github_token()
    
    # Verificaciones de Ollama
    ollama_ok = check_ollama()
    if not ollama_ok:
        print(f"{Colors.YELLOW}⚠ Ollama no está configurado pero el sistema puede funcionar con GitHub Models{Colors.END}")
    
    # Verificación de estructura
    all_checks_passed &= check_project_structure()
    
    # Prueba de evaluación
    all_checks_passed &= check_sample_evaluation()
    
    # Resumen
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    if all_checks_passed:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ Sistema listo para usar!{Colors.END}")
        generate_test_command()
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ Hay problemas que resolver{Colors.END}")
        print(f"{Colors.YELLOW}Revisa los mensajes anteriores para más detalles{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()
