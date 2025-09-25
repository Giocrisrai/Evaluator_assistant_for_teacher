#!/usr/bin/env python
"""
Script de Limpieza y Reorganización del Sistema
Mantiene solo lo esencial para evaluar proyectos Kedro ML
"""

import os
import shutil
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_action(action, item):
    """Imprime la acción realizada."""
    if action == "delete":
        print(f"{Colors.RED}✗ Eliminando:{Colors.END} {item}")
    elif action == "keep":
        print(f"{Colors.GREEN}✓ Manteniendo:{Colors.END} {item}")
    elif action == "create":
        print(f"{Colors.GREEN}+ Creando:{Colors.END} {item}")

def clean_system():
    """Limpia el sistema dejando solo lo esencial para Kedro."""
    
    print(f"{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}LIMPIEZA DEL SISTEMA - EVALUADOR KEDRO ML{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")
    
    base_path = Path.cwd()
    
    # Lista de archivos a ELIMINAR (genéricos o no relacionados con Kedro)
    files_to_delete = [
        'app.py',
        'main.py',
        'simple_evaluator.py',
        'config_simple.py',
        'start.py',
        'switch_provider.py',
        'test_app.py',
        'test_providers.py',
        'validate.py',
        'COMO_USAR.md',
        'INSTRUCCIONES.md',
        'PROVEEDORES_LLM.md',
        'README.md',  # Mantendremos solo README_KEDRO.md
        'examples/rubrica_python.py',
        'examples/rubrica_react.py',
        'examples/estudiantes_ejemplo.csv',
        'examples/repos_example.txt',
    ]
    
    # Lista de archivos a MANTENER (esenciales para Kedro)
    files_to_keep = [
        'src/kedro_evaluator.py',
        'src/rubrica_evaluator.py',  # Base necesaria
        'examples/rubrica_kedro.py',
        'scripts/evaluate_batch.py',
        'scripts/validate_installation.py',
        'data/estudiantes_kedro.csv',
        'setup.py',
        'Makefile',
        'requirements.txt',
        'README_KEDRO.md',
        '.gitignore',
        'LICENSE',
        '.env.example',
    ]
    
    # Directorios a limpiar
    dirs_to_clean = [
        '__pycache__',
        'evaluaciones_agentes',
        'tests',  # Lo recrearemos con tests específicos
    ]
    
    print(f"{Colors.YELLOW}1. Eliminando archivos genéricos...{Colors.END}")
    for file_path in files_to_delete:
        full_path = base_path / file_path
        if full_path.exists():
            try:
                full_path.unlink()
                print_action("delete", file_path)
            except:
                pass
    
    print(f"\n{Colors.YELLOW}2. Limpiando directorios...{Colors.END}")
    for dir_path in dirs_to_clean:
        full_path = base_path / dir_path
        if full_path.exists():
            try:
                shutil.rmtree(full_path)
                print_action("delete", dir_path)
            except:
                pass
    
    print(f"\n{Colors.YELLOW}3. Verificando archivos esenciales...{Colors.END}")
    for file_path in files_to_keep:
        full_path = base_path / file_path
        if full_path.exists():
            print_action("keep", file_path)
    
    print(f"\n{Colors.YELLOW}4. Renombrando README...{Colors.END}")
    if (base_path / 'README_KEDRO.md').exists():
        shutil.copy(base_path / 'README_KEDRO.md', base_path / 'README.md')
        (base_path / 'README_KEDRO.md').unlink()
        print_action("create", "README.md (desde README_KEDRO.md)")
    
    print(f"\n{Colors.GREEN}✅ Sistema limpio y listo para evaluar proyectos Kedro ML{Colors.END}")
    print(f"\n{Colors.BOLD}Estructura final:{Colors.END}")
    print("""
kedro-ml-evaluator/
├── src/
│   ├── kedro_evaluator.py      # Evaluador principal
│   └── rubrica_evaluator.py    # Sistema base
├── examples/
│   └── rubrica_kedro.py         # Rúbrica de 10 criterios
├── scripts/
│   ├── evaluate_batch.py        # Evaluación masiva
│   └── validate_installation.py # Validador
├── data/
│   └── estudiantes_kedro.csv   # Lista de estudiantes
├── setup.py                     # Configuración inicial
├── Makefile                     # Comandos útiles
├── requirements.txt             # Dependencias
├── README.md                    # Documentación principal
└── .gitignore                   # Ignorar archivos
    """)

if __name__ == "__main__":
    clean_system()
