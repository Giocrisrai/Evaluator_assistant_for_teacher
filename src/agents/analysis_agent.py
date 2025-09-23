#!/usr/bin/env python3
"""
Agente de Análisis Inteligente para Evaluaciones
Basado en la configuración de GitHub Models del proyecto de curso
"""

import os
import json
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import openai
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

@dataclass
class EvaluationInsight:
    """Insight generado por el agente de análisis."""
    tipo: str  # "tendencia", "problema_comun", "recomendacion"
    titulo: str
    descripcion: str
    criterios_afectados: List[str]
    gravedad: str  # "baja", "media", "alta"
    evidencias: List[str]

class AnalysisAgent:
    """Agente inteligente para análisis de evaluaciones."""
    
    def __init__(self):
        """Inicializa el agente con configuración de GitHub Models."""
        self.client = openai.OpenAI(
            base_url=os.getenv("OPENAI_BASE_URL", "https://models.inference.ai.azure.com"),
            api_key=os.getenv("GITHUB_TOKEN")
        )
        self.model = "gpt-4o-mini"
        
    def analyze_evaluation_trends(self, evaluations: List[Dict]) -> List[EvaluationInsight]:
        """Analiza tendencias en múltiples evaluaciones."""
        
        prompt = self._build_trend_analysis_prompt(evaluations)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "Eres un experto analista educativo especializado en identificar patrones y tendencias en evaluaciones de proyectos de Machine Learning. Tu trabajo es encontrar insights valiosos que ayuden a mejorar la enseñanza."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            insights_text = response.choices[0].message.content
            return self._parse_insights(insights_text)
            
        except Exception as e:
            print(f"Error en análisis de tendencias: {e}")
            return []
    
    def identify_common_issues(self, evaluations: List[Dict]) -> List[EvaluationInsight]:
        """Identifica problemas comunes en las evaluaciones."""
        
        prompt = self._build_issues_analysis_prompt(evaluations)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un mentor experto que identifica problemas recurrentes en proyectos de estudiantes. Ayudas a los profesores a entender qué aspectos necesitan más atención pedagógica."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            
            issues_text = response.choices[0].message.content
            return self._parse_insights(issues_text)
            
        except Exception as e:
            print(f"Error identificando problemas comunes: {e}")
            return []
    
    def generate_improvement_recommendations(self, evaluation: Dict) -> List[EvaluationInsight]:
        """Genera recomendaciones específicas para una evaluación."""
        
        prompt = self._build_recommendation_prompt(evaluation)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un coach personalizado que da recomendaciones específicas y accionables para mejorar proyectos de Machine Learning. Tus sugerencias son prácticas y detalladas."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )
            
            recommendations_text = response.choices[0].message.content
            return self._parse_insights(recommendations_text)
            
        except Exception as e:
            print(f"Error generando recomendaciones: {e}")
            return []
    
    def _build_trend_analysis_prompt(self, evaluations: List[Dict]) -> str:
        """Construye prompt para análisis de tendencias."""
        
        # Preparar datos para análisis
        criterios_stats = {}
        notas_totales = []
        
        for eval_data in evaluations:
            notas_totales.append(eval_data.get('nota_final', 0))
            
            for criterio in eval_data.get('criterios', []):
                nombre = criterio.get('criterio', '')
                puntuacion = criterio.get('puntuacion', 0)
                
                if nombre not in criterios_stats:
                    criterios_stats[nombre] = []
                criterios_stats[nombre].append(puntuacion)
        
        # Calcular estadísticas
        stats_text = f"""
DATOS DE ANÁLISIS:
- Total evaluaciones: {len(evaluations)}
- Nota promedio: {sum(notas_totales)/len(notas_totales):.2f}/7.0
- Nota máxima: {max(notas_totales):.2f}/7.0
- Nota mínima: {min(notas_totales):.2f}/7.0

ESTADÍSTICAS POR CRITERIO:
"""
        
        for criterio, puntuaciones in criterios_stats.items():
            promedio = sum(puntuaciones) / len(puntuaciones)
            stats_text += f"- {criterio}: {promedio:.1f}% promedio\n"
        
        prompt = f"""
Analiza las siguientes tendencias en las evaluaciones de proyectos de Machine Learning:

{stats_text}

EVALUACIONES DETALLADAS:
{json.dumps(evaluations, indent=2, ensure_ascii=False)}

INSTRUCCIONES:
1. Identifica 3-5 tendencias principales
2. Encuentra patrones en criterios con bajo rendimiento
3. Analiza correlaciones entre diferentes aspectos
4. Sugiere áreas de mejora pedagógica

FORMATO DE RESPUESTA (JSON):
[
    {{
        "tipo": "tendencia",
        "titulo": "Título de la tendencia",
        "descripcion": "Descripción detallada...",
        "criterios_afectados": ["criterio1", "criterio2"],
        "gravedad": "media",
        "evidencias": ["evidencia1", "evidencia2"]
    }}
]
"""
        return prompt
    
    def _build_issues_analysis_prompt(self, evaluations: List[Dict]) -> str:
        """Construye prompt para análisis de problemas comunes."""
        
        prompt = f"""
Analiza los problemas más comunes en estas evaluaciones de proyectos de Machine Learning:

{json.dumps(evaluations, indent=2, ensure_ascii=False)}

INSTRUCCIONES:
1. Identifica los 5 problemas más recurrentes
2. Clasifica por gravedad (alta/media/baja)
3. Sugiere soluciones específicas
4. Enfócate en aspectos pedagógicos

FORMATO DE RESPUESTA (JSON):
[
    {{
        "tipo": "problema_comun",
        "titulo": "Problema identificado",
        "descripcion": "Descripción del problema...",
        "criterios_afectados": ["criterio1"],
        "gravedad": "alta",
        "evidencias": ["% de estudiantes afectados", "ejemplos específicos"]
    }}
]
"""
        return prompt
    
    def _build_recommendation_prompt(self, evaluation: Dict) -> str:
        """Construye prompt para recomendaciones específicas."""
        
        prompt = f"""
Genera recomendaciones específicas para mejorar este proyecto de Machine Learning:

{json.dumps(evaluation, indent=2, ensure_ascii=False)}

INSTRUCCIONES:
1. Enfócate en los criterios con menor puntuación
2. Da recomendaciones accionables y específicas
3. Prioriza las mejoras por impacto
4. Incluye recursos de aprendizaje

FORMATO DE RESPUESTA (JSON):
[
    {{
        "tipo": "recomendacion",
        "titulo": "Recomendación específica",
        "descripcion": "Descripción detallada...",
        "criterios_afectados": ["criterio1"],
        "gravedad": "alta",
        "evidencias": ["puntuación actual", "área de mejora"]
    }}
]
"""
        return prompt
    
    def _parse_insights(self, insights_text: str) -> List[EvaluationInsight]:
        """Parsea la respuesta del LLM en objetos EvaluationInsight."""
        try:
            # Buscar JSON en la respuesta
            start = insights_text.find('[')
            end = insights_text.rfind(']') + 1
            json_str = insights_text[start:end]
            
            insights_data = json.loads(json_str)
            insights = []
            
            for insight_data in insights_data:
                insight = EvaluationInsight(
                    tipo=insight_data.get('tipo', ''),
                    titulo=insight_data.get('titulo', ''),
                    descripcion=insight_data.get('descripcion', ''),
                    criterios_afectados=insight_data.get('criterios_afectados', []),
                    gravedad=insight_data.get('gravedad', 'media'),
                    evidencias=insight_data.get('evidencias', [])
                )
                insights.append(insight)
            
            return insights
            
        except Exception as e:
            print(f"Error parseando insights: {e}")
            return []
    
    def generate_summary_report(self, insights: List[EvaluationInsight]) -> str:
        """Genera un reporte resumen de los insights."""
        
        if not insights:
            return "No se generaron insights en el análisis."
        
        report = f"# 📊 Reporte de Análisis Inteligente\n\n"
        report += f"**Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
        report += f"**Total Insights:** {len(insights)}\n\n"
        
        # Agrupar por tipo
        by_type = {}
        for insight in insights:
            if insight.tipo not in by_type:
                by_type[insight.tipo] = []
            by_type[insight.tipo].append(insight)
        
        for tipo, insights_list in by_type.items():
            tipo_title = {
                'tendencia': '🔍 Tendencias Identificadas',
                'problema_comun': '⚠️ Problemas Comunes',
                'recomendacion': '💡 Recomendaciones'
            }.get(tipo, f'📋 {tipo.title()}')
            
            report += f"## {tipo_title}\n\n"
            
            for insight in insights_list:
                gravedad_emoji = {
                    'alta': '🔴',
                    'media': '🟡',
                    'baja': '🟢'
                }.get(insight.gravedad, '⚪')
                
                report += f"### {gravedad_emoji} {insight.titulo}\n\n"
                report += f"{insight.descripcion}\n\n"
                
                if insight.criterios_afectados:
                    report += f"**Criterios afectados:** {', '.join(insight.criterios_afectados)}\n\n"
                
                if insight.evidencias:
                    report += f"**Evidencias:**\n"
                    for evidencia in insight.evidencias:
                        report += f"- {evidencia}\n"
                    report += "\n"
                
                report += "---\n\n"
        
        return report


# Ejemplo de uso
if __name__ == "__main__":
    # Crear agente
    agent = AnalysisAgent()
    
    # Datos de ejemplo (en la práctica vendrían de evaluaciones reales)
    sample_evaluations = [
        {
            "repositorio": "https://github.com/estudiante1/proyecto-ml",
            "nota_final": 5.2,
            "criterios": [
                {"criterio": "Estructura del Proyecto", "puntuacion": 60},
                {"criterio": "Análisis de Datos", "puntuacion": 80},
                {"criterio": "Modelado", "puntuacion": 40}
            ]
        },
        {
            "repositorio": "https://github.com/estudiante2/proyecto-ml",
            "nota_final": 4.8,
            "criterios": [
                {"criterio": "Estructura del Proyecto", "puntuacion": 70},
                {"criterio": "Análisis de Datos", "puntuacion": 50},
                {"criterio": "Modelado", "puntuacion": 45}
            ]
        }
    ]
    
    print("🤖 Agente de Análisis Inteligente")
    print("=" * 50)
    
    # Análisis de tendencias
    print("📈 Analizando tendencias...")
    trends = agent.analyze_evaluation_trends(sample_evaluations)
    print(f"✅ Encontradas {len(trends)} tendencias")
    
    # Problemas comunes
    print("\n⚠️ Identificando problemas comunes...")
    issues = agent.identify_common_issues(sample_evaluations)
    print(f"✅ Identificados {len(issues)} problemas")
    
    # Generar reporte
    all_insights = trends + issues
    report = agent.generate_summary_report(all_insights)
    
    print("\n📊 Reporte generado:")
    print(report)
