#!/usr/bin/env python3
"""
Agente de Recomendaciones Personalizadas
Genera planes de mejora específicos para cada estudiante
"""

import os
import json
import sys
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import openai
import requests
from dotenv import load_dotenv

# Agregar src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config import Config

# Cargar variables de entorno
load_dotenv()

@dataclass
class PersonalizedRecommendation:
    """Recomendación personalizada para un estudiante."""
    titulo: str
    descripcion: str
    prioridad: str  # "alta", "media", "baja"
    tiempo_estimado: str
    recursos: List[str]
    pasos: List[str]
    criterio_relacionado: str
    nivel_dificultad: str  # "principiante", "intermedio", "avanzado"

@dataclass
class LearningPath:
    """Plan de aprendizaje personalizado."""
    estudiante: str
    nivel_actual: str
    objetivos: List[str]
    recomendaciones: List[PersonalizedRecommendation]
    cronograma: Dict[str, str]
    recursos_generales: List[str]

class RecommendationAgent:
    """Agente que genera recomendaciones personalizadas."""
    
    def __init__(self):
        """Inicializa el agente con configuración centralizada."""
        self.provider = Config.LLM_PROVIDER
        
        # Inicializar atributos por defecto
        self.client = None
        self.ollama_url = None
        
        if self.provider == "github":
            self.client = openai.OpenAI(
                base_url=Config.LLM_PROVIDERS["github"]["base_url"],
                api_key=Config.GITHUB_TOKEN
            )
            self.model = "gpt-4o-mini"
        elif self.provider == "ollama":
            self.ollama_url = Config.LLM_PROVIDERS["ollama"]["base_url"]
            self.model = "llama3:latest"
        else:
            # Fallback a GitHub Models
            self.client = openai.OpenAI(
                base_url=Config.LLM_PROVIDERS["github"]["base_url"],
                api_key=Config.GITHUB_TOKEN
            )
            self.model = "gpt-4o-mini"
        
        # Recursos de aprendizaje por criterio
        self.learning_resources = {
            "Estructura y Configuración del Proyecto Kedro": [
                "Documentación oficial de Kedro: https://docs.kedro.org/",
                "Tutorial de configuración: https://docs.kedro.org/en/stable/get_started/",
                "Ejemplos de proyectos: https://github.com/kedro-org/kedro-starters"
            ],
            "Implementación del Catálogo de Datos": [
                "Catálogo de datos Kedro: https://docs.kedro.org/en/stable/data/data_catalog.html",
                "Tipos de datasets: https://docs.kedro.org/en/stable/data/data_catalog.html#dataset-types",
                "Configuración avanzada: https://docs.kedro.org/en/stable/data/data_catalog.html#advanced-configuration"
            ],
            "Desarrollo de Nodos y Funciones": [
                "Creación de nodos: https://docs.kedro.org/en/stable/nodes_and_pipelines/nodes.html",
                "Mejores prácticas: https://docs.kedro.org/en/stable/nodes_and_pipelines/nodes.html#best-practices",
                "Testing de nodos: https://docs.kedro.org/en/stable/development/testing.html"
            ],
            "Construcción de Pipelines": [
                "Pipelines en Kedro: https://docs.kedro.org/en/stable/nodes_and_pipelines/pipelines.html",
                "Diseño de pipelines: https://docs.kedro.org/en/stable/nodes_and_pipelines/pipelines.html#designing-pipelines",
                "Pipeline modular: https://docs.kedro.org/en/stable/nodes_and_pipelines/pipelines.html#modular-pipelines"
            ],
            "Análisis Exploratorio de Datos (EDA)": [
                "EDA con pandas: https://pandas.pydata.org/docs/user_guide/index.html",
                "Visualización con matplotlib: https://matplotlib.org/stable/tutorials/introductory/usage.html",
                "EDA con seaborn: https://seaborn.pydata.org/tutorial.html"
            ],
            "Limpieza y Tratamiento de Datos": [
                "Data cleaning con pandas: https://pandas.pydata.org/docs/user_guide/missing_data.html",
                "Manejo de outliers: https://pandas.pydata.org/docs/user_guide/groupby.html",
                "Preprocessing: https://scikit-learn.org/stable/modules/preprocessing.html"
            ],
            "Transformación y Feature Engineering": [
                "Feature engineering: https://scikit-learn.org/stable/modules/feature_extraction.html",
                "Transformaciones: https://scikit-learn.org/stable/modules/preprocessing.html",
                "Selección de features: https://scikit-learn.org/stable/modules/feature_selection.html"
            ],
            "Identificación de Targets para ML": [
                "Target selection: https://scikit-learn.org/stable/supervised_learning.html",
                "Problemas de clasificación: https://scikit-learn.org/stable/modules/classes.html#classification",
                "Problemas de regresión: https://scikit-learn.org/stable/modules/classes.html#regression"
            ],
            "Documentación y Notebooks": [
                "Jupyter notebooks: https://jupyter-notebook.readthedocs.io/en/stable/",
                "Markdown guide: https://www.markdownguide.org/",
                "Documentación de código: https://docs.python.org/3/tutorial/controlflow.html#documentation-strings"
            ],
            "Reproducibilidad y Mejores Prácticas": [
                "Version control: https://git-scm.com/doc",
                "Entornos virtuales: https://docs.python.org/3/tutorial/venv.html",
                "Requirements: https://pip.pypa.io/en/stable/user_guide/#requirements-files"
            ]
        }
    
    def generate_personalized_recommendations(self, evaluation: Dict, student_info: Optional[Dict] = None) -> List[PersonalizedRecommendation]:
        """Genera recomendaciones personalizadas para un estudiante."""
        
        prompt = self._build_recommendation_prompt(evaluation, student_info)
        
        try:
            if self.provider == "github":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "Eres un mentor personalizado de Machine Learning que crea planes de mejora específicos y accionables. Tus recomendaciones son prácticas, detalladas y adaptadas al nivel del estudiante."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3
                )
                recommendations_text = response.choices[0].message.content
                
            elif self.provider == "ollama":
                # Ollama API call
                ollama_payload = {
                    "model": self.model,
                    "prompt": f"Eres un mentor personalizado de Machine Learning que crea planes de mejora específicos y accionables. SIEMPRE responde en ESPAÑOL. Tus recomendaciones son prácticas, detalladas y adaptadas al nivel del estudiante.\n\n{prompt}",
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "num_predict": 4000
                    }
                }
                
                response = requests.post(
                    f"{self.ollama_url}/api/generate",
                    json=ollama_payload,
                    timeout=120
                )
                
                if response.status_code == 200:
                    recommendations_text = response.json()["response"]
                else:
                    raise Exception(f"Error de Ollama: {response.status_code} - {response.text}")
            
            return self._parse_recommendations(recommendations_text)
            
        except Exception as e:
            print(f"Error generando recomendaciones: {e}")
            return []
    
    def create_learning_path(self, evaluations: List[Dict], student_info: Dict) -> LearningPath:
        """Crea un plan de aprendizaje completo para un estudiante."""
        
        # Analizar evaluaciones del estudiante
        promedio_nota = sum(e.get('nota_final', 0) for e in evaluations) / len(evaluations)
        
        # Determinar nivel actual
        if promedio_nota >= 6.0:
            nivel_actual = "avanzado"
        elif promedio_nota >= 4.0:
            nivel_actual = "intermedio"
        else:
            nivel_actual = "principiante"
        
        # Generar recomendaciones para la evaluación más reciente
        latest_evaluation = max(evaluations, key=lambda x: x.get('fecha_evaluacion', ''))
        recommendations = self.generate_personalized_recommendations(latest_evaluation, student_info)
        
        # Crear objetivos basados en el nivel
        objetivos = self._generate_learning_objectives(nivel_actual, latest_evaluation)
        
        # Crear cronograma
        cronograma = self._create_timeline(recommendations)
        
        # Recursos generales
        recursos_generales = self._get_general_resources(nivel_actual)
        
        return LearningPath(
            estudiante=student_info.get('nombre', 'Estudiante'),
            nivel_actual=nivel_actual,
            objetivos=objetivos,
            recomendaciones=recommendations,
            cronograma=cronograma,
            recursos_generales=recursos_generales
        )
    
    def _build_recommendation_prompt(self, evaluation: Dict, student_info: Optional[Dict] = None) -> str:
        """Construye prompt para recomendaciones personalizadas."""
        
        student_context = ""
        if student_info:
            student_context = f"""
INFORMACIÓN DEL ESTUDIANTE:
- Nombre: {student_info.get('nombre', 'N/A')}
- Nivel: {student_info.get('nivel', 'intermedio')}
- Experiencia previa: {student_info.get('experiencia', 'N/A')}
"""
        
        prompt = f"""
Genera recomendaciones personalizadas de mejora para este proyecto de Machine Learning:

{student_context}

EVALUACIÓN ACTUAL:
{json.dumps(evaluation, indent=2, ensure_ascii=False)}

RECURSOS DISPONIBLES POR CRITERIO:
{json.dumps(self.learning_resources, indent=2, ensure_ascii=False)}

INSTRUCCIONES:
1. Enfócate en los criterios con menor puntuación
2. Crea recomendaciones específicas y accionables
3. Incluye pasos detallados para cada recomendación
4. Estima tiempo de implementación
5. Sugiere recursos específicos de aprendizaje
6. Adapta el nivel de dificultad al estudiante

FORMATO DE RESPUESTA (JSON):
[
    {{
        "titulo": "Título de la recomendación",
        "descripcion": "Descripción detallada...",
        "prioridad": "alta",
        "tiempo_estimado": "2-3 horas",
        "recursos": ["recurso1", "recurso2"],
        "pasos": ["Paso 1", "Paso 2", "Paso 3"],
        "criterio_relacionado": "Nombre del criterio",
        "nivel_dificultad": "intermedio"
    }}
]
"""
        return prompt
    
    def _parse_recommendations(self, recommendations_text: str) -> List[PersonalizedRecommendation]:
        """Parsea la respuesta del LLM en objetos PersonalizedRecommendation."""
        try:
            # Buscar JSON en la respuesta
            start = recommendations_text.find('[')
            end = recommendations_text.rfind(']') + 1
            json_str = recommendations_text[start:end]
            
            recommendations_data = json.loads(json_str)
            recommendations = []
            
            for rec_data in recommendations_data:
                recommendation = PersonalizedRecommendation(
                    titulo=rec_data.get('titulo', ''),
                    descripcion=rec_data.get('descripcion', ''),
                    prioridad=rec_data.get('prioridad', 'media'),
                    tiempo_estimado=rec_data.get('tiempo_estimado', ''),
                    recursos=rec_data.get('recursos', []),
                    pasos=rec_data.get('pasos', []),
                    criterio_relacionado=rec_data.get('criterio_relacionado', ''),
                    nivel_dificultad=rec_data.get('nivel_dificultad', 'intermedio')
                )
                recommendations.append(recommendation)
            
            return recommendations
            
        except Exception as e:
            print(f"Error parseando recomendaciones: {e}")
            return []
    
    def _generate_learning_objectives(self, nivel: str, evaluation: Dict) -> List[str]:
        """Genera objetivos de aprendizaje basados en el nivel."""
        
        base_objectives = {
            "principiante": [
                "Completar configuración básica del proyecto",
                "Implementar análisis exploratorio de datos",
                "Crear documentación básica"
            ],
            "intermedio": [
                "Optimizar arquitectura del proyecto",
                "Implementar pipelines robustos",
                "Mejorar calidad del código"
            ],
            "avanzado": [
                "Implementar mejores prácticas avanzadas",
                "Optimizar rendimiento del sistema",
                "Crear documentación técnica completa"
            ]
        }
        
        # Agregar objetivos específicos basados en criterios débiles
        criterios_debiles = [
            c['criterio'] for c in evaluation.get('criterios', []) 
            if c.get('puntuacion', 0) < 60
        ]
        
        objectives = base_objectives.get(nivel, base_objectives["intermedio"])
        
        if criterios_debiles:
            objectives.append(f"Mejorar: {', '.join(criterios_debiles[:3])}")
        
        return objectives
    
    def _create_timeline(self, recommendations: List[PersonalizedRecommendation]) -> Dict[str, str]:
        """Crea un cronograma basado en las recomendaciones."""
        
        timeline = {}
        current_week = 1
        
        # Agrupar por prioridad
        high_priority = [r for r in recommendations if r.prioridad == "alta"]
        medium_priority = [r for r in recommendations if r.prioridad == "media"]
        low_priority = [r for r in recommendations if r.prioridad == "baja"]
        
        # Asignar semanas
        for rec in high_priority[:2]:  # Máximo 2 por semana
            timeline[f"Semana {current_week}"] = rec.titulo
            current_week += 1
        
        for rec in medium_priority[:2]:
            timeline[f"Semana {current_week}"] = rec.titulo
            current_week += 1
        
        for rec in low_priority[:1]:
            timeline[f"Semana {current_week}"] = rec.titulo
            current_week += 1
        
        return timeline
    
    def _get_general_resources(self, nivel: str) -> List[str]:
        """Obtiene recursos generales según el nivel."""
        
        resources = {
            "principiante": [
                "Python básico: https://docs.python.org/3/tutorial/",
                "Pandas tutorial: https://pandas.pydata.org/docs/getting_started/intro_tutorials/",
                "Kedro getting started: https://docs.kedro.org/en/stable/get_started/"
            ],
            "intermedio": [
                "Scikit-learn user guide: https://scikit-learn.org/stable/user_guide.html",
                "Kedro advanced: https://docs.kedro.org/en/stable/advanced_topics/",
                "Machine Learning patterns: https://scikit-learn.org/stable/modules/classes.html"
            ],
            "avanzado": [
                "MLOps best practices: https://ml-ops.org/",
                "Kedro deployment: https://docs.kedro.org/en/stable/deployment/",
                "Advanced ML techniques: https://scikit-learn.org/stable/modules/ensemble.html"
            ]
        }
        
        return resources.get(nivel, resources["intermedio"])
    
    def generate_learning_path_report(self, learning_path: LearningPath) -> str:
        """Genera un reporte del plan de aprendizaje."""
        
        report = f"""# 🎯 Plan de Aprendizaje Personalizado

**Estudiante:** {learning_path.estudiante}  
**Nivel Actual:** {learning_path.nivel_actual.title()}  
**Fecha:** {datetime.now().strftime('%d/%m/%Y')}

## 📋 Objetivos de Aprendizaje

"""
        
        for i, objetivo in enumerate(learning_path.objetivos, 1):
            report += f"{i}. {objetivo}\n"
        
        report += "\n## 🗓️ Cronograma Recomendado\n\n"
        
        for semana, tarea in learning_path.cronograma.items():
            report += f"- **{semana}:** {tarea}\n"
        
        report += "\n## 💡 Recomendaciones Específicas\n\n"
        
        # Agrupar por prioridad
        by_priority = {"alta": [], "media": [], "baja": []}
        for rec in learning_path.recomendaciones:
            by_priority[rec.prioridad].append(rec)
        
        for prioridad in ["alta", "media", "baja"]:
            if by_priority[prioridad]:
                emoji = {"alta": "🔴", "media": "🟡", "baja": "🟢"}[prioridad]
                report += f"### {emoji} Prioridad {prioridad.title()}\n\n"
                
                for rec in by_priority[prioridad]:
                    report += f"#### {rec.titulo}\n\n"
                    report += f"**Criterio:** {rec.criterio_relacionado}\n"
                    report += f"**Tiempo estimado:** {rec.tiempo_estimado}\n"
                    report += f"**Nivel:** {rec.nivel_dificultad}\n\n"
                    report += f"{rec.descripcion}\n\n"
                    
                    if rec.pasos:
                        report += "**Pasos a seguir:**\n"
                        for paso in rec.pasos:
                            report += f"- {paso}\n"
                        report += "\n"
                    
                    if rec.recursos:
                        report += "**Recursos:**\n"
                        for recurso in rec.recursos:
                            report += f"- {recurso}\n"
                        report += "\n"
                    
                    report += "---\n\n"
        
        report += "\n## 📚 Recursos Generales\n\n"
        
        for recurso in learning_path.recursos_generales:
            report += f"- {recurso}\n"
        
        report += f"\n---\n\n*Plan generado automáticamente el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}*"
        
        return report


# Ejemplo de uso
if __name__ == "__main__":
    # Crear agente
    agent = RecommendationAgent()
    
    # Evaluación de ejemplo
    sample_evaluation = {
        "repositorio": "https://github.com/estudiante/proyecto-ml",
        "nota_final": 4.2,
        "fecha_evaluacion": "2024-01-15",
        "criterios": [
            {"criterio": "Estructura y Configuración del Proyecto Kedro", "puntuacion": 60},
            {"criterio": "Análisis Exploratorio de Datos (EDA)", "puntuacion": 80},
            {"criterio": "Modelado y Machine Learning", "puntuacion": 30},
            {"criterio": "Documentación y Notebooks", "puntuacion": 40}
        ]
    }
    
    student_info = {
        "nombre": "Juan Pérez",
        "nivel": "intermedio",
        "experiencia": "6 meses con Python, 3 meses con ML"
    }
    
    print("🎯 Agente de Recomendaciones Personalizadas")
    print("=" * 50)
    
    # Generar recomendaciones
    print("💡 Generando recomendaciones personalizadas...")
    recommendations = agent.generate_personalized_recommendations(sample_evaluation, student_info)
    print(f"✅ Generadas {len(recommendations)} recomendaciones")
    
    # Crear plan de aprendizaje
    print("\n📚 Creando plan de aprendizaje...")
    learning_path = agent.create_learning_path([sample_evaluation], student_info)
    
    # Generar reporte
    report = agent.generate_learning_path_report(learning_path)
    
    print("\n📊 Plan de aprendizaje generado:")
    print(report)
