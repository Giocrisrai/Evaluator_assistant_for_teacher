# rubrica_kedro.py
# Rúbrica específica para evaluar proyectos de Machine Learning con Kedro
# Basada en la metodología CRISP-DM y los 10 criterios de evaluación

from datetime import datetime

def create_kedro_ml_rubrica():
    """
    Crea rúbrica específica para proyectos de Machine Learning con Kedro.
    Implementa los 10 criterios de evaluación con sus ponderaciones.
    """
    
    # Niveles de desempeño según el documento
    niveles_evaluacion = {
        100: "Muy buen desempeño - Logro completo de todos los aspectos",
        80: "Buen desempeño - Alto desempeño con mínimas omisiones",
        60: "Desempeño aceptable - Logro de elementos básicos",
        40: "Desempeño incipiente - Importantes omisiones o errores",
        20: "Desempeño insuficiente - Desempeño incorrecto",
        0: "No logrado - No cumple requisitos mínimos"
    }
    
    return {
        "nombre": "Evaluación Proyecto Machine Learning con Framework Kedro",
        "descripcion": "Rúbrica para evaluar proyectos ML implementados con Kedro siguiendo CRISP-DM (3 primeras fases)",
        "asignatura": "MLY0100 - Machine Learning",
        "ponderacion_total": 0.7,  # 70% de la nota parcial 1
        "tiempo_asignado": "4 semanas",
        "modalidad": "Parejas",
        
        "criterios": [
            # CRITERIO 1: Estructura y Configuración del Proyecto Kedro (10%)
            {
                "nombre": "Estructura y Configuración del Proyecto Kedro",
                "descripcion": "Proyecto Kedro correctamente estructurado con configuración completa",
                "ponderacion": 0.10,
                "niveles": niveles_evaluacion,
                "archivos_revisar": [
                    "conf/base/catalog.yml",
                    "conf/base/parameters.yml",
                    "conf/base/logging.yml",
                    "conf/local/credentials.yml",
                    "src/*/pipeline_registry.py",
                    "pyproject.toml",
                    "README.md",
                    ".gitignore"
                ],
                "comandos_verificacion": [
                    "kedro info",
                    "kedro run --dry-run",
                    "kedro catalog list"
                ]
            },
            
            # CRITERIO 2: Implementación del Catálogo de Datos (10%)
            {
                "nombre": "Implementación del Catálogo de Datos",
                "descripcion": "Configuración correcta de múltiples datasets en el catálogo de Kedro",
                "ponderacion": 0.10,
                "niveles": niveles_evaluacion,
                "archivos_revisar": [
                    "conf/base/catalog.yml",
                    "data/01_raw/*",
                    "data/02_intermediate/*",
                    "data/03_primary/*",
                    "data/04_feature/*",
                    "data/05_model_input/*"
                ],
                "comandos_verificacion": [
                    "kedro catalog list",
                    "kedro catalog resolve"
                ]
            },
            
            # CRITERIO 3: Desarrollo de Nodos y Funciones (10%)
            {
                "nombre": "Desarrollo de Nodos y Funciones",
                "descripcion": "Nodos modulares con funciones puras y bien documentadas",
                "ponderacion": 0.10,
                "niveles": niveles_evaluacion,
                "archivos_revisar": [
                    "src/*/pipelines/data_engineering/nodes.py",
                    "src/*/pipelines/data_science/nodes.py",
                    "src/*/pipelines/*/nodes.py",
                    "src/*/nodes.py"
                ]
            },
            
            # CRITERIO 4: Construcción de Pipelines (10%)
            {
                "nombre": "Construcción de Pipelines",
                "descripcion": "Pipelines organizados por fase CRISP-DM con dependencias claras",
                "ponderacion": 0.10,
                "niveles": niveles_evaluacion,
                "archivos_revisar": [
                    "src/*/pipelines/data_engineering/pipeline.py",
                    "src/*/pipelines/data_science/pipeline.py",
                    "src/*/pipelines/*/pipeline.py",
                    "src/*/pipeline_registry.py"
                ],
                "comandos_verificacion": [
                    "kedro pipeline list",
                    "kedro viz",
                    "kedro run --pipeline=data_engineering"
                ]
            },
            
            # CRITERIO 5: Análisis Exploratorio de Datos - EDA (10%)
            {
                "nombre": "Análisis Exploratorio de Datos - EDA",
                "descripcion": "EDA exhaustivo con análisis univariado, bivariado y multivariado",
                "ponderacion": 0.10,
                "niveles": niveles_evaluacion,
                "archivos_revisar": [
                    "notebooks/02_data_understanding.ipynb",
                    "notebooks/*_eda.ipynb",
                    "src/*/pipelines/data_science/nodes.py",
                    "docs/eda/*"
                ]
            },
            
            # CRITERIO 6: Limpieza y Tratamiento de Datos (10%)
            {
                "nombre": "Limpieza y Tratamiento de Datos",
                "descripcion": "Estrategias diferenciadas para limpieza de datos",
                "ponderacion": 0.10,
                "niveles": niveles_evaluacion,
                "archivos_revisar": [
                    "notebooks/03_data_preparation.ipynb",
                    "src/*/pipelines/data_engineering/nodes.py",
                    "data/03_primary/*"
                ]
            },
            
            # CRITERIO 7: Transformación y Feature Engineering (10%)
            {
                "nombre": "Transformación y Feature Engineering",
                "descripcion": "Transformaciones avanzadas y creación de features derivadas",
                "ponderacion": 0.10,
                "niveles": niveles_evaluacion,
                "archivos_revisar": [
                    "notebooks/03_data_preparation.ipynb",
                    "src/*/pipelines/data_engineering/nodes.py",
                    "data/04_feature/*",
                    "conf/base/parameters.yml"
                ]
            },
            
            # CRITERIO 8: Identificación de Targets para ML (10%)
            {
                "nombre": "Identificación de Targets para ML",
                "descripcion": "Identificación correcta de variables objetivo para ML",
                "ponderacion": 0.10,
                "niveles": niveles_evaluacion,
                "archivos_revisar": [
                    "notebooks/01_business_understanding.ipynb",
                    "notebooks/02_data_understanding.ipynb",
                    "README.md",
                    "docs/*"
                ]
            },
            
            # CRITERIO 9: Documentación y Notebooks (10%)
            {
                "nombre": "Documentación y Notebooks",
                "descripcion": "Documentación excepcional con notebooks estructurados por CRISP-DM",
                "ponderacion": 0.10,
                "niveles": niveles_evaluacion,
                "archivos_revisar": [
                    "README.md",
                    "notebooks/01_business_understanding.ipynb",
                    "notebooks/02_data_understanding.ipynb",
                    "notebooks/03_data_preparation.ipynb",
                    "docs/*",
                    "src/**/*.py"
                ]
            },
            
            # CRITERIO 10: Reproducibilidad y Mejores Prácticas (10%)
            {
                "nombre": "Reproducibilidad y Mejores Prácticas",
                "descripcion": "Proyecto completamente reproducible siguiendo mejores prácticas",
                "ponderacion": 0.10,
                "niveles": niveles_evaluacion,
                "archivos_revisar": [
                    "requirements.txt",
                    "pyproject.toml",
                    ".gitignore",
                    "conf/base/parameters.yml",
                    "conf/local/.gitkeep",
                    ".env.example",
                    "tests/*",
                    ".pre-commit-config.yaml"
                ],
                "comandos_verificacion": [
                    "pip install -r requirements.txt",
                    "kedro test",
                    "kedro run"
                ]
            }
        ],
        
        # Configuración adicional para la evaluación
        "configuracion_evaluacion": {
            "nota_minima": 1.0,
            "nota_maxima": 7.0,
            "nota_aprobacion": 4.0,
            "escala_conversion": {
                "100": 7.0,
                "90": 6.5,
                "80": 6.0,
                "70": 5.5,
                "60": 5.0,
                "50": 4.5,
                "40": 4.0,
                "30": 3.5,
                "20": 3.0,
                "10": 2.0,
                "0": 1.0
            }
        },
        
        # Entregables requeridos
        "entregables_obligatorios": [
            "Repositorio Git con el proyecto Kedro completo",
            "Mínimo 3 datasets diferentes en data/01_raw/",
            "Catálogo de datos configurado (conf/base/catalog.yml)",
            "Pipelines implementados para las 3 fases CRISP-DM",
            "3 Notebooks de análisis (uno por fase)",
            "README.md con instrucciones de instalación y ejecución",
            "requirements.txt actualizado",
            "Documentación en código (docstrings)"
        ],
        
        # Penalizaciones y bonificaciones
        "modificadores": {
            "penalizaciones": {
                "entrega_tardia": -0.5,  # por día
                "falta_dataset": -1.0,   # por cada dataset faltante bajo 3
                "no_ejecuta": -2.0,       # si kedro run falla
                "sin_documentacion": -1.0
            },
            "bonificaciones": {
                "kedro_viz": 0.3,         # Visualización interactiva
                "tests_unitarios": 0.5,   # Tests implementados
                "ci_cd": 0.3,            # GitHub Actions
                "docker": 0.2,           # Containerización
                "dashboard": 0.5         # Dashboard interactivo
            }
        }
    }


# Configuración para integración con Ollama
OLLAMA_CONFIG = {
    "base_url": "http://localhost:11434",
    "model": "llama2",  # o el modelo que tengas instalado
    "temperature": 0.3,  # Baja temperatura para evaluaciones consistentes
    "max_tokens": 2000,
    "timeout": 60,
    "prompts": {
        "system": """Eres un evaluador experto en proyectos de Machine Learning 
                    con Kedro. Evalúas de manera objetiva basándote en criterios 
                    específicos y evidencia encontrada en el código. Siempre 
                    justificas tus puntuaciones con ejemplos concretos del código."""
    }
}


# Ejemplo de uso con tu sistema
if __name__ == "__main__":
    # Esta rúbrica se puede importar en tu sistema principal
    rubrica = create_kedro_ml_rubrica()
    
    # Mostrar resumen de criterios
    print("=== RÚBRICA DE EVALUACIÓN KEDRO ML ===")
    print(f"Nombre: {rubrica['nombre']}")
    print(f"Total de criterios: {len(rubrica['criterios'])}")
    print(f"\nCriterios de evaluación:")
    
    for i, criterio in enumerate(rubrica['criterios'], 1):
        print(f"{i}. {criterio['nombre']} - {criterio['ponderacion']*100}%")
    
    print(f"\nEntregables obligatorios: {len(rubrica['entregables_obligatorios'])}")
    print(f"Configuración de notas: {rubrica['configuracion_evaluacion']['nota_minima']} - {rubrica['configuracion_evaluacion']['nota_maxima']}")
