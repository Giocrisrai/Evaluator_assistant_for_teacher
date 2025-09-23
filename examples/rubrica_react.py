# Ejemplo de rúbrica personalizada para aplicaciones React

def create_react_rubrica():
    """Crea rúbrica específica para proyectos React."""
    
    niveles_estandar = {
        100: "Implementación ejemplar que excede expectativas",
        80: "Buena implementación con características sólidas", 
        60: "Implementación básica que cumple requisitos",
        40: "Implementación limitada con problemas",
        20: "Implementación deficiente con errores importantes",
        0: "No implementado o completamente incorrecto"
    }
    
    return {
        "nombre": "Evaluación Aplicación React",
        "descripcion": "Rúbrica para evaluar aplicaciones web con React.js",
        "criterios": [
            {
                "nombre": "Estructura de Componentes",
                "descripcion": "Organización y reutilización de componentes React",
                "ponderacion": 0.20,
                "niveles": niveles_estandar,
                "archivos_revisar": [
                    "src/components/",
                    "src/pages/",
                    "src/hooks/",
                    "src/utils/"
                ]
            },
            {
                "nombre": "Manejo de Estado",
                "descripcion": "Gestión correcta del estado con useState, useContext, Redux, etc.",
                "ponderacion": 0.15,
                "niveles": niveles_estandar,
                "archivos_revisar": [
                    "src/store/",
                    "src/context/",
                    "src/reducers/",
                    "src/hooks/"
                ]
            },
            {
                "nombre": "Routing y Navegación",
                "descripcion": "Implementación de rutas y navegación entre páginas",
                "ponderacion": 0.10,
                "niveles": niveles_estandar,
                "archivos_revisar": [
                    "src/App.js",
                    "src/routes/",
                    "src/router/"
                ]
            },
            {
                "nombre": "Styling y CSS",
                "descripcion": "Diseño responsivo y buenas prácticas de CSS",
                "ponderacion": 0.15,
                "niveles": niveles_estandar,
                "archivos_revisar": [
                    "src/styles/",
                    "src/css/",
                    "*.css",
                    "*.scss",
                    "*.module.css"
                ]
            },
            {
                "nombre": "API Integration",
                "descripcion": "Consumo de APIs y manejo de datos asincrónicos",
                "ponderacion": 0.15,
                "niveles": niveles_estandar,
                "archivos_revisar": [
                    "src/api/",
                    "src/services/",
                    "src/utils/api.js"
                ]
            },
            {
                "nombre": "Testing",
                "descripcion": "Tests unitarios y de integración",
                "ponderacion": 0.10,
                "niveles": niveles_estandar,
                "archivos_revisar": [
                    "src/__tests__/",
                    "*.test.js",
                    "*.spec.js"
                ]
            },
            {
                "nombre": "Performance y Optimización",
                "descripcion": "Optimización de rendimiento y mejores prácticas",
                "ponderacion": 0.10,
                "niveles": niveles_estandar,
                "archivos_revisar": [
                    "src/",
                    "package.json",
                    "webpack.config.js"
                ]
            },
            {
                "nombre": "Documentación y README",
                "descripcion": "Documentación clara del proyecto y cómo ejecutarlo",
                "ponderacion": 0.05,
                "niveles": niveles_estandar,
                "archivos_revisar": [
                    "README.md",
                    "docs/",
                    "CONTRIBUTING.md"
                ]
            }
        ]
    }

# Ejemplo de uso
if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
    
    from rubrica_evaluator import RubricaEvaluator
    
    # Configuración
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    LLM_PROVIDER = "github"
    LLM_API_KEY = os.getenv("LLM_API_KEY")
    
    if not GITHUB_TOKEN or not LLM_API_KEY:
        print("❌ Configurar GITHUB_TOKEN y LLM_API_KEY en .env")
        exit(1)
    
    # Crear evaluador
    evaluador = RubricaEvaluator(GITHUB_TOKEN, LLM_PROVIDER, LLM_API_KEY)
    
    # Cargar rúbrica React
    rubrica_dict = create_react_rubrica()
    rubrica = evaluador.load_rubrica_from_dict(rubrica_dict)
    
    # Evaluar proyecto React de ejemplo
    repo_url = "https://github.com/facebook/create-react-app"
    print(f"🚀 Evaluando proyecto React: {repo_url}")
    
    evaluacion = evaluador.evaluate_repository(repo_url, rubrica)
    evaluador.export_evaluation(evaluacion, "evaluacion_react_example")
    
    print(f"✅ Evaluación completada - Nota: {evaluacion.nota_final}/7.0")
