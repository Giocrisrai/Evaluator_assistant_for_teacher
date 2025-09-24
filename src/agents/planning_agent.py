#!/usr/bin/env python3
"""
Agente de Planificación Avanzada
Utiliza técnicas de planificación y meta-prompting para evaluaciones más rigurosas
"""

import os
import sys
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import requests
import openai

# Agregar src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config import Config

@dataclass
class EvaluationPlan:
    """Plan de evaluación estructurado."""
    criterio: str
    objetivos: List[str]
    estrategias: List[str]
    criterios_especificos: Dict[str, str]
    evidencias_requeridas: List[str]
    pasos_evaluacion: List[str]
    criterios_puntuacion: Dict[str, str]
    tiempo_estimado: int  # minutos

@dataclass
class PlanningContext:
    """Contexto para la planificación."""
    tipo_proyecto: str
    tecnologias: List[str]
    complejidad: str
    nivel_estudiante: str
    objetivos_curso: List[str]

class PlanningAgent:
    """Agente especializado en planificación de evaluaciones."""
    
    def __init__(self):
        """Inicializa el agente de planificación."""
        self.provider = Config.LLM_PROVIDER
        
        if self.provider == "github":
            self.client = openai.OpenAI(
                base_url=Config.LLM_PROVIDERS["github"]["base_url"],
                api_key=Config.GITHUB_TOKEN
            )
            self.model = "gpt-4o-mini"
        elif self.provider == "ollama":
            self.ollama_url = Config.LLM_PROVIDERS["ollama"]["base_url"]
            self.model = "llama3:latest"
    
    def create_evaluation_plan(self, criterio: str, contexto: PlanningContext, evidencias: Dict[str, Any]) -> EvaluationPlan:
        """Crea un plan de evaluación detallado usando meta-prompting."""
        
        planning_prompt = self._build_planning_prompt(criterio, contexto, evidencias)
        plan_response = self._call_llm(planning_prompt)
        
        return self._parse_evaluation_plan(plan_response, criterio)
    
    def _build_planning_prompt(self, criterio: str, contexto: PlanningContext, evidencias: Dict[str, Any]) -> str:
        """Construye el prompt de planificación usando meta-prompting."""
        
        return f"""
META-PROMPTING: PLANIFICACIÓN ESTRATÉGICA DE EVALUACIÓN

Eres un experto en diseño de evaluaciones educativas que debe crear un plan estratégico detallado.

CRITERIO A EVALUAR: {criterio}

CONTEXTO DEL PROYECTO:
- Tipo de proyecto: {contexto.tipo_proyecto}
- Tecnologías utilizadas: {', '.join(contexto.tecnologias)}
- Complejidad: {contexto.complejidad}
- Nivel del estudiante: {contexto.nivel_estudiante}
- Objetivos del curso: {', '.join(contexto.objetivos_curso)}

EVIDENCIAS DISPONIBLES:
{self._format_evidence_for_planning(evidencias)}

INSTRUCCIONES DE PLANIFICACIÓN:
1. Analiza el criterio en el contexto específico del proyecto
2. Define objetivos de evaluación claros y medibles
3. Diseña estrategias de evaluación apropiadas para el nivel
4. Establece criterios específicos de puntuación
5. Identifica evidencias clave que deben ser evaluadas
6. Crea pasos de evaluación estructurados
7. Estima el tiempo necesario para una evaluación rigurosa

FORMATO DE RESPUESTA:
{{
    "objetivos": ["objetivo1", "objetivo2", "objetivo3"],
    "estrategias": ["estrategia1", "estrategia2", "estrategia3"],
    "criterios_especificos": {{
        "aspecto1": "Criterio específico para aspecto1",
        "aspecto2": "Criterio específico para aspecto2"
    }},
    "evidencias_requeridas": ["evidencia1", "evidencia2", "evidencia3"],
    "pasos_evaluacion": [
        "Paso 1: Análisis inicial",
        "Paso 2: Evaluación de evidencias",
        "Paso 3: Determinación de puntuación"
    ],
    "criterios_puntuacion": {{
        "0-25%": "Descripción de nivel básico",
        "26-50%": "Descripción de nivel elemental",
        "51-75%": "Descripción de nivel intermedio",
        "76-100%": "Descripción de nivel avanzado"
    }},
    "tiempo_estimado": 15
}}

Responde ÚNICAMENTE con JSON válido en ESPAÑOL.
"""
    
    def create_multi_criteria_plan(self, criterios: List[str], contexto: PlanningContext) -> Dict[str, EvaluationPlan]:
        """Crea planes de evaluación para múltiples criterios."""
        
        plans = {}
        for criterio in criterios:
            # Crear contexto específico para cada criterio
            criterio_contexto = self._adapt_context_for_criterion(criterio, contexto)
            
            # Crear plan individual
            plan = self.create_evaluation_plan(criterio, criterio_contexto, {})
            plans[criterio] = plan
        
        return plans
    
    def optimize_evaluation_sequence(self, plans: Dict[str, EvaluationPlan]) -> List[str]:
        """Optimiza la secuencia de evaluación para máxima eficiencia."""
        
        optimization_prompt = self._build_optimization_prompt(plans)
        sequence_response = self._call_llm(optimization_prompt)
        
        return self._parse_optimization_result(sequence_response)
    
    def _build_optimization_prompt(self, plans: Dict[str, EvaluationPlan]) -> str:
        """Construye el prompt de optimización de secuencia."""
        
        plans_info = []
        for criterio, plan in plans.items():
            plans_info.append(f"""
Criterio: {criterio}
Tiempo estimado: {plan.tiempo_estimado} minutos
Evidencias requeridas: {', '.join(plan.evidencias_requeridas)}
Complejidad: {'Alta' if len(plan.pasos_evaluacion) > 5 else 'Media' if len(plan.pasos_evaluacion) > 3 else 'Baja'}
""")
        
        return f"""
OPTIMIZACIÓN DE SECUENCIA DE EVALUACIÓN

Eres un experto en optimización de procesos que debe determinar el orden óptimo de evaluación.

PLANES DE EVALUACIÓN DISPONIBLES:
{''.join(plans_info)}

CRITERIOS DE OPTIMIZACIÓN:
1. Minimizar el tiempo total de evaluación
2. Maximizar la calidad de la evaluación
3. Aprovechar dependencias entre criterios
4. Balancear carga de trabajo
5. Considerar la importancia relativa de cada criterio

INSTRUCCIONES:
1. Analiza las dependencias entre criterios
2. Identifica criterios que pueden evaluarse en paralelo
3. Determina el orden óptimo considerando eficiencia y calidad
4. Justifica tu decisión

FORMATO DE RESPUESTA:
{{
    "secuencia_optimizada": ["criterio1", "criterio2", "criterio3"],
    "criterios_paralelos": [["criterioA", "criterioB"], ["criterioC", "criterioD"]],
    "tiempo_total_estimado": 120,
    "justificacion": "Explicación detallada del orden elegido",
    "consideraciones_especiales": ["consideración1", "consideración2"]
}}

Responde ÚNICAMENTE con JSON válido en ESPAÑOL.
"""
    
    def _call_llm(self, prompt: str) -> str:
        """Realiza la llamada al LLM."""
        try:
            if self.provider == "github":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "Eres un experto en planificación educativa. SIEMPRE responde en ESPAÑOL con JSON válido."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.1,
                    max_tokens=2000
                )
                return response.choices[0].message.content
                
            elif self.provider == "ollama":
                payload = {
                    "model": self.model,
                    "prompt": f"Eres un experto en planificación educativa. SIEMPRE responde en ESPAÑOL con JSON válido.\n\n{prompt}",
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "num_predict": 2000,
                        "top_p": 0.9
                    }
                }
                
                response = requests.post(
                    f"{self.ollama_url}/api/generate",
                    json=payload,
                    timeout=120
                )
                
                if response.status_code == 200:
                    return response.json()["response"]
                else:
                    raise Exception(f"Error de Ollama: {response.status_code}")
                    
        except Exception as e:
            print(f"Error en llamada LLM del Planning Agent: {e}")
            return self._generate_fallback_plan()
    
    def _parse_evaluation_plan(self, response: str, criterio: str) -> EvaluationPlan:
        """Parsea la respuesta del LLM en un plan de evaluación."""
        try:
            data = self._extract_json(response)
            
            return EvaluationPlan(
                criterio=criterio,
                objetivos=data.get('objetivos', []),
                estrategias=data.get('estrategias', []),
                criterios_especificos=data.get('criterios_especificos', {}),
                evidencias_requeridas=data.get('evidencias_requeridas', []),
                pasos_evaluacion=data.get('pasos_evaluacion', []),
                criterios_puntuacion=data.get('criterios_puntuacion', {}),
                tiempo_estimado=data.get('tiempo_estimado', 10)
            )
            
        except Exception as e:
            print(f"Error parseando plan de evaluación: {e}")
            return self._create_fallback_plan(criterio)
    
    def _parse_optimization_result(self, response: str) -> List[str]:
        """Parsea el resultado de optimización."""
        try:
            data = self._extract_json(response)
            return data.get('secuencia_optimizada', [])
        except:
            return []
    
    def _extract_json(self, text: str) -> Dict:
        """Extrae JSON de una respuesta de texto."""
        try:
            start = text.find('{')
            end = text.rfind('}') + 1
            json_str = text[start:end]
            return json.loads(json_str)
        except:
            return {}
    
    def _adapt_context_for_criterion(self, criterio: str, contexto: PlanningContext) -> PlanningContext:
        """Adapta el contexto para un criterio específico."""
        # Aquí se pueden hacer adaptaciones específicas según el criterio
        return contexto
    
    def _format_evidence_for_planning(self, evidencias: Dict[str, Any]) -> str:
        """Formatea las evidencias para la planificación."""
        if not evidencias:
            return "Evidencias no especificadas - evaluación general"
        
        evidence_text = []
        if evidencias.get('directories'):
            evidence_text.append(f"Directorios disponibles: {len(evidencias['directories'])}")
        if evidencias.get('files'):
            evidence_text.append(f"Archivos disponibles: {len(evidencias['files'])}")
        if evidencias.get('readme'):
            evidence_text.append("README presente")
        if evidencias.get('requirements'):
            evidence_text.append("Requirements presente")
        
        return "\n".join(evidence_text) if evidence_text else "Evidencias limitadas"
    
    def _generate_fallback_plan(self) -> str:
        """Genera un plan de respaldo."""
        return json.dumps({
            "objetivos": ["Evaluar cumplimiento del criterio"],
            "estrategias": ["Análisis de evidencias disponibles"],
            "criterios_especificos": {"cumplimiento": "Verificar cumplimiento básico"},
            "evidencias_requeridas": ["Evidencias disponibles"],
            "pasos_evaluacion": ["Análisis", "Evaluación", "Puntuación"],
            "criterios_puntuacion": {
                "0-25%": "Cumplimiento básico",
                "26-50%": "Cumplimiento elemental",
                "51-75%": "Cumplimiento intermedio",
                "76-100%": "Cumplimiento avanzado"
            },
            "tiempo_estimado": 10
        }, ensure_ascii=False)
    
    def _create_fallback_plan(self, criterio: str) -> EvaluationPlan:
        """Crea un plan de respaldo."""
        return EvaluationPlan(
            criterio=criterio,
            objetivos=["Evaluar cumplimiento básico"],
            estrategias=["Análisis general"],
            criterios_especificos={"cumplimiento": "Verificar cumplimiento"},
            evidencias_requeridas=["Evidencias disponibles"],
            pasos_evaluacion=["Análisis", "Evaluación"],
            criterios_puntuacion={
                "0-25%": "Básico",
                "26-50%": "Elemental",
                "51-75%": "Intermedio",
                "76-100%": "Avanzado"
            },
            tiempo_estimado=10
        )
