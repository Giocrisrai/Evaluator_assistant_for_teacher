# Ejemplo de rúbrica para proyectos Python generales

def create_python_rubrica():
    """Crea rúbrica específica para proyectos Python."""
    
    niveles_estandar = {
        100: "Implementación excepcional siguiendo todas las mejores prácticas",
        80: "Buena implementación con estándares sólidos", 
        60: "Implementación básica que funciona correctamente",
        40: "Implementación con problemas menores",
        20: "Implementación deficiente con errores",
        0: "No implementado o no funciona"
    }
    
    return {
        "nombre": "Evaluación Proyecto Python",
        "descripcion": "Rúbrica para evaluar proyectos Python siguiendo PEP8 y mejores prácticas",
        "criterios": [
            {
                "nombre": "Estructura del Proyecto",
                "descripcion": "Organización de archivos y carpetas siguiendo estándares Python",
                "ponderacion": 0.15,
                "niveles": niveles_estandar,
                "archivos_revisar": [
                    "setup.py",
                    "pyproject.toml", 
                    "requirements.txt",
                    "src/",
                    "__init__.py"
                ]
            },
            {
                "nombre": "Calidad del Código",
                "descripcion": "Adherencia a PEP8, naming conventions y code style",
                "ponderacion": 0.20,
                "niveles": niveles_estandar,
                "archivos_revisar": [
                    "*.py",
                    ".flake8",
                    ".pylintrc",
                    "pyproject.toml"
                ]
            },
            {
                "nombre": "Documentación y Docstrings",
                "descripcion": "Documentación clara con docstrings en funciones y clases",
                "ponderacion": 0.15,
                "niveles": niveles_estandar,
                "archivos_revisar": [
                    "*.py",
                    "docs/",
                    "README.md",
                    "CHANGELOG.md"
                ]
            },
            {
                "nombre": "Testing",
                "descripcion": "Tests unitarios comprehensivos usando pytest o unittest",
                "ponderacion": 0.20,
                "niveles": niveles_estandar,
                "archivos_revisar": [
                    "tests/",
                    "test_*.py",
                    "*_test.py",
                    "conftest.py",
                    "pytest.ini"
                ]
            },
            {
                "nombre": "Manejo de Errores",
                "descripcion": "Manejo apropiado de excepciones y edge cases",
                "ponderacion": 0.10,
                "niveles": niveles_estandar,
                "archivos_revisar": [
                    "*.py"
                ]
            },
            {
                "nombre": "Dependencias y Entorno",
                "descripcion": "Gestión correcta de dependencias y entornos virtuales",
                "ponderacion": 0.10,
                "niveles": niveles_estandar,
                "archivos_revisar": [
                    "requirements.txt",
                    "environment.yml",
                    "Pipfile",
                    "pyproject.toml",
                    ".python-version"
                ]
            },
            {
                "nombre": "Logging y Debugging",
                "descripcion": "Implementación de logging apropiado para debugging",
                "ponderacion": 0.05,
                "niveles": niveles_estandar,
                "archivos_revisar": [
                    "*.py",
                    "logging.conf",
                    "config/"
                ]
            },
            {
                "nombre": "Seguridad y Buenas Prácticas",
                "descripcion": "Código seguro sin vulnerabilidades obvias",
                "ponderacion": 0.05,
                "niveles": niveles_estandar,
                "archivos_revisar": [
                    "*.py",
                    ".env.example",
                    "config/",
                    ".gitignore"
                ]
            }
        ]
    }

def create_data_science_rubrica():
    """Rúbrica específica para proyectos de Data Science."""
    
    niveles_estandar = {
        100: "Análisis completo y metodología impecable",
        80: "Buen análisis con metodología sólida", 
        60: "Análisis básico que cumple objetivos",
        40: "Análisis limitado con algunas deficiencias",
        20: "Análisis superficial con errores",
        0: "Sin análisis válido o metodología incorrecta"
    }
    
    return {
        "nombre": "Evaluación Proyecto Data Science",
        "descripcion": "Rúbrica para proyectos de ciencia de datos y análisis",
        "criterios": [
            {
                "nombre": "Análisis Exploratorio de Datos (EDA)",
                "descripcion": "EDA comprensivo con visualizaciones informativas",
                "ponderacion": 0.25,
                "niveles": niveles_estandar,
                "archivos_revisar": [
                    "notebooks/eda.ipynb",
                    "notebooks/exploratory_*",
                    "analysis/",
                    "plots/"
                ]
            },
            {
                "nombre": "Limpieza y Preprocessing",
                "descripcion": "Limpieza de datos y preprocessing apropiados",
                "ponderacion": 0.20,
                "niveles": niveles_estandar,
                "archivos_revisar": [
                    "src/preprocessing.py",
                    "src/cleaning.py",
                    "notebooks/cleaning*",
                    "data/processed/"
                ]
            },
            {
                "nombre": "Modelado y Machine Learning",
                "descripcion": "Selección y entrenamiento apropiado de modelos",
                "ponderacion": 0.25,
                "niveles": niveles_estandar,
                "archivos_revisar": [
                    "src/models/",
                    "notebooks/modeling*",
                    "models/",
                    "experiments/"
                ]
            },
            {
                "nombre": "Evaluación y Validación",
                "descripcion": "Evaluación rigurosa con métricas apropiadas",
                "ponderacion": 0.15,
                "niveles": niveles_estandar,
                "archivos_revisar": [
                    "src/evaluation.py",
                    "notebooks/evaluation*",
                    "results/",
                    "metrics/"
                ]
            },
            {
                "nombre": "Reproducibilidad",
                "descripcion": "Código reproducible con seeds y configuraciones",
                "ponderacion": 0.15,
                "niveles": niveles_estandar,
                "archivos_revisar": [
                    "config.py",
                    "requirements.txt",
                    "environment.yml",
                    "Makefile",
                    "setup.py"
                ]
            }
        ]
    }

# Ejemplo de uso
if __name__ == "__main__":
    print("🐍 Rúbricas Python disponibles:")
    print("1. Proyecto Python General")
    print("2. Proyecto Data Science")
    
    # Mostrar criterios de la rúbrica Python general
    rubrica = create_python_rubrica()
    print(f"\n📋 Rúbrica: {rubrica['nombre']}")
    print(f"📝 Descripción: {rubrica['descripcion']}")
    print("\n📊 Criterios de evaluación:")
    
    for i, criterio in enumerate(rubrica['criterios'], 1):
        print(f"   {i}. {criterio['nombre']} ({criterio['ponderacion']*100:.0f}%)")
        print(f"      {criterio['descripcion']}")
        print(f"      Archivos: {', '.join(criterio['archivos_revisar'][:3])}")
        print()
