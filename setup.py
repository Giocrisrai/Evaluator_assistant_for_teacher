#!/usr/bin/env python
"""
Script de Configuración Inicial del Sistema de Evaluación Kedro ML
Configura automáticamente el entorno para el profesor
"""

import os
import sys
import subprocess
import json
from pathlib import Path
import getpass

# Colores para output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    """Imprime un encabezado formateado."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_success(text):
    """Imprime un mensaje de éxito."""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_warning(text):
    """Imprime una advertencia."""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_error(text):
    """Imprime un error."""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_info(text):
    """Imprime información."""
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")

def check_python_version():
    """Verifica la versión de Python."""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor} - Se requiere 3.8+")
        return False

def install_requirements():
    """Instala las dependencias requeridas."""
    print_info("Instalando dependencias...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print_success("Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Error instalando dependencias: {e}")
        return False

def setup_github_token():
    """Configura el token de GitHub."""
    print_info("Configuración de GitHub Token")
    print("Necesitas un token de GitHub para acceder a los repositorios.")
    print("Puedes obtener uno en: https://github.com/settings/tokens")
    print("Permisos necesarios: repo, read:user\n")
    
    token = getpass.getpass("Ingresa tu GitHub Token: ")
    
    if token:
        # Verificar el token
        try:
            import requests
            headers = {'Authorization': f'token {token}'}
            response = requests.get('https://api.github.com/user', headers=headers)
            
            if response.status_code == 200:
                user_data = response.json()
                print_success(f"Token válido - Usuario: {user_data.get('login', 'Unknown')}")
                
                # Guardar en archivo .env
                with open('.env', 'a') as f:
                    f.write(f"\nGITHUB_TOKEN={token}\n")
                
                # También exportar para la sesión actual
                os.environ['GITHUB_TOKEN'] = token
                
                return True
            else:
                print_error("Token inválido o sin permisos suficientes")
                return False
        except Exception as e:
            print_error(f"Error verificando token: {e}")
            return False
    else:
        print_warning("No se configuró ningún token")
        return False

def setup_ollama():
    """Configura Ollama para LLM local."""
    print_info("Configuración de Ollama (opcional)")
    
    response = input("¿Deseas instalar Ollama para análisis con IA local? [s/N]: ")
    
    if response.lower() == 's':
        try:
            # Verificar si ya está instalado
            result = subprocess.run(['which', 'ollama'], capture_output=True)
            
            if result.returncode == 0:
                print_success("Ollama ya está instalado")
            else:
                print_info("Instalando Ollama...")
                subprocess.run(['curl', '-fsSL', 'https://ollama.ai/install.sh', '|', 'sh'], 
                             shell=True, check=True)
                print_success("Ollama instalado correctamente")
            
            # Descargar modelo
            print_info("Descargando modelo llama2 (puede tomar varios minutos)...")
            subprocess.run(['ollama', 'pull', 'llama2'], check=True)
            print_success("Modelo llama2 descargado")
            
            return True
        except Exception as e:
            print_warning(f"No se pudo instalar Ollama: {e}")
            print_info("Puedes instalarlo manualmente desde https://ollama.ai")
            return False
    else:
        print_info("Omitiendo instalación de Ollama")
        return False

def create_directories():
    """Crea la estructura de directorios necesaria."""
    print_info("Creando estructura de directorios...")
    
    directories = [
        'evaluaciones',
        'data/input',
        'data/output',
        'data/cache',
        'logs',
        'backups'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print_success("Estructura de directorios creada")
    return True

def setup_sample_data():
    """Crea archivo de ejemplo con estudiantes."""
    print_info("Configurando datos de ejemplo...")
    
    sample_csv = """nombre,pareja,repositorio
Juan Pérez,María González,https://github.com/ejemplo/proyecto-kedro-1
Ana Rodríguez,Carlos López,https://github.com/ejemplo/proyecto-kedro-2
Pedro Martínez,,https://github.com/ejemplo/proyecto-kedro-3
"""
    
    csv_path = Path('data/estudiantes_ejemplo.csv')
    
    if not csv_path.exists():
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write(sample_csv)
        print_success("Archivo de ejemplo creado: data/estudiantes_ejemplo.csv")
    else:
        print_info("Archivo de ejemplo ya existe")
    
    return True

def create_config_file():
    """Crea archivo de configuración del sistema."""
    config = {
        "system": {
            "version": "1.0.0",
            "course": "MLY0100 - Machine Learning",
            "evaluation": "Parcial 1 - Proyecto Kedro"
        },
        "evaluation": {
            "criteria_count": 10,
            "weight_per_criterion": 0.10,
            "grading_scale": {
                "min": 1.0,
                "max": 7.0,
                "passing": 4.0
            }
        },
        "bonuses": {
            "kedro_viz": 0.3,
            "unit_tests": 0.5,
            "ci_cd": 0.3,
            "docker": 0.2,
            "dashboard": 0.5
        },
        "penalties": {
            "late_delivery_per_day": 0.5,
            "missing_dataset": 1.0,
            "project_not_running": 2.0,
            "no_documentation": 1.0
        },
        "settings": {
            "parallel_evaluations": 3,
            "timeout_seconds": 300,
            "use_cache": True,
            "output_formats": ["json", "html", "markdown"]
        }
    }
    
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print_success("Archivo de configuración creado: config.json")
    return True

def test_evaluation():
    """Prueba el sistema con una evaluación de ejemplo."""
    print_info("Probando el sistema de evaluación...")
    
    try:
        # Intentar importar el evaluador
        sys.path.insert(0, str(Path.cwd() / 'src'))
        from kedro_evaluator import KedroEvaluator
        
        token = os.getenv('GITHUB_TOKEN', 'dummy_token')
        evaluator = KedroEvaluator(token)
        
        print_success("Sistema de evaluación funciona correctamente")
        return True
    except Exception as e:
        print_error(f"Error en sistema de evaluación: {e}")
        return False

def generate_quick_guide():
    """Genera una guía rápida de uso."""
    guide = """
# 📚 GUÍA RÁPIDA DE USO - SISTEMA DE EVALUACIÓN KEDRO ML

## 🚀 Inicio Rápido

### 1. Preparar lista de estudiantes
Edita el archivo `data/estudiantes_kedro.csv` con la información de tus estudiantes:
```csv
nombre,pareja,repositorio
Juan Pérez,María González,https://github.com/juanperez/proyecto-kedro
```

### 2. Ejecutar evaluación masiva
```bash
make evaluate-all
```

### 3. Ver resultados
Los resultados se guardan en `evaluaciones/` con:
- Reporte individual por estudiante
- Estadísticas del curso
- Archivo Excel con todas las notas

## 📋 Comandos Principales

| Comando | Descripción |
|---------|-------------|
| `make evaluate-all` | Evalúa todos los estudiantes |
| `make stats` | Ver estadísticas rápidas |
| `make report` | Generar reportes consolidados |
| `make clean` | Limpiar archivos temporales |

## 🔍 Evaluar un solo estudiante
```bash
make evaluate-single REPO=https://github.com/usuario/repo STUDENT="Nombre Estudiante"
```

## 📊 Criterios Evaluados (10% cada uno)
1. Estructura y Configuración Kedro
2. Catálogo de Datos (mínimo 3)
3. Nodos y Funciones
4. Pipelines
5. Análisis Exploratorio (EDA)
6. Limpieza de Datos
7. Feature Engineering
8. Identificación de Targets
9. Documentación y Notebooks
10. Reproducibilidad

## 🎯 Escala de Notas
- 100% = 7.0
- 80% = 6.0
- 60% = 5.0
- 40% = 4.0 (Aprobación)
- 20% = 3.0
- 0% = 1.0

## ⚡ Tips
- Usa `--parallel 5` para evaluar más rápido
- Revisa `evaluaciones/estadisticas_*.json` para análisis detallado
- Los logs se guardan en `evaluaciones_kedro.log`

## 🆘 Ayuda
- Ver todos los comandos: `make help`
- Validar instalación: `make validate`
- Documentación completa: README_KEDRO.md

---
Sistema de Evaluación Kedro ML v1.0
"""
    
    with open('GUIA_RAPIDA.md', 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print_success("Guía rápida creada: GUIA_RAPIDA.md")
    return True

def main():
    """Función principal del configurador."""
    print_header("CONFIGURACIÓN INICIAL")
    print_header("Sistema de Evaluación Kedro ML")
    
    print("Este script configurará automáticamente tu entorno")
    print("para evaluar proyectos de Machine Learning con Kedro.\n")
    
    steps = [
        ("Verificando Python", check_python_version),
        ("Creando directorios", create_directories),
        ("Instalando dependencias", install_requirements),
        ("Configurando GitHub Token", setup_github_token),
        ("Configurando Ollama (opcional)", setup_ollama),
        ("Creando datos de ejemplo", setup_sample_data),
        ("Generando configuración", create_config_file),
        ("Probando sistema", test_evaluation),
        ("Creando guía rápida", generate_quick_guide)
    ]
    
    results = []
    
    for step_name, step_function in steps:
        print(f"\n{Colors.BOLD}{step_name}...{Colors.ENDC}")
        result = step_function()
        results.append((step_name, result))
        
        if not result and step_name in ["Verificando Python", "Configurando GitHub Token"]:
            print_error("Paso crítico falló. Abortando configuración.")
            sys.exit(1)
    
    # Resumen
    print_header("RESUMEN DE CONFIGURACIÓN")
    
    for step_name, result in results:
        if result:
            print_success(step_name)
        else:
            print_warning(f"{step_name} - Requiere atención")
    
    # Instrucciones finales
    if all(result for _, result in results):
        print_header("✅ SISTEMA LISTO PARA USAR")
        print("\n📋 Próximos pasos:")
        print("1. Edita data/estudiantes_kedro.csv con los datos reales")
        print("2. Ejecuta: make evaluate-all")
        print("3. Revisa los resultados en evaluaciones/")
        print("\n📚 Para más ayuda: cat GUIA_RAPIDA.md")
    else:
        print_header("⚠️ CONFIGURACIÓN PARCIAL")
        print("\nAlgunos componentes necesitan configuración manual.")
        print("Revisa los mensajes anteriores para más detalles.")
        print("\n🔧 Para validar la instalación: make validate")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nConfiguración cancelada por el usuario.")
        sys.exit(0)
    except Exception as e:
        print_error(f"Error inesperado: {e}")
        sys.exit(1)
