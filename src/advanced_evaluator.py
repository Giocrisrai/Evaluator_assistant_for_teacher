#!/usr/bin/env python3
"""
Evaluador Avanzado con Meta-Prompting y Chain-of-Thought Reasoning
Sistema profesional de evaluación con técnicas de IA avanzadas
"""

import os
import sys
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import requests
import openai

# Agregar src al path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from config import Config
# Importación diferida para evitar circular import

@dataclass
class EvaluationStep:
    """Paso individual en el proceso de evaluación."""
    step_name: str
    description: str
    reasoning: str
    evidence: List[str]
    confidence: float  # 0.0 - 1.0

@dataclass
class AdvancedEvaluation:
    """Evaluación avanzada con reasoning detallado."""
    criterio: str
    puntuacion: int
    nota: float
    retroalimentacion: str
    evidencias: List[str]
    sugerencias: List[str]
    reasoning_steps: List[EvaluationStep]
    confidence_score: float
    validation_checks: List[str]

class MetaPromptingEvaluator:
    """Evaluador con técnicas de meta-prompting avanzadas."""
    
    def __init__(self, provider: str = None, api_key: str = None):
        self.provider = provider or Config.LLM_PROVIDER
        self.api_key = api_key or Config.LLM_API_KEY
        self.setup_client()
        
    def setup_client(self):
        """Configura el cliente según el proveedor."""
        if self.provider == "github":
            self.client = openai.OpenAI(
                base_url=Config.LLM_PROVIDERS["github"]["base_url"],
                api_key=Config.GITHUB_TOKEN
            )
            self.model = "gpt-4o-mini"
        elif self.provider == "ollama":
            self.ollama_url = Config.LLM_PROVIDERS["ollama"]["base_url"]
            self.model = "llama3:latest"
    
    def evaluate_criterion_advanced(self, criterio, evidencias: Dict[str, Any]) -> AdvancedEvaluation:
        """Evalúa un criterio usando meta-prompting y chain-of-thought."""
        
        # Paso 1: Meta-prompting para planificación
        planning_prompt = self._build_planning_prompt(criterio, evidencias)
        plan = self._call_llm(planning_prompt)
        
        # Paso 2: Chain-of-thought reasoning
        reasoning_prompt = self._build_reasoning_prompt(criterio, evidencias, plan)
        reasoning = self._call_llm(reasoning_prompt)
        
        # Paso 3: Evaluación estructurada
        evaluation_prompt = self._build_evaluation_prompt(criterio, evidencias, reasoning)
        evaluation = self._call_llm(evaluation_prompt)
        
        # Paso 4: Self-reflection y validación
        validation_prompt = self._build_validation_prompt(criterio, evaluation)
        validation = self._call_llm(validation_prompt)
        
        # Paso 5: Parsear y estructurar resultado
        return self._parse_advanced_evaluation(evaluation, validation, criterio.nombre)
    
    def _build_planning_prompt(self, criterio, evidencias: Dict[str, Any]) -> str:
        """Construye el prompt de planificación usando meta-prompting."""
        
        return f"""
META-PROMPTING: PLANIFICACIÓN DE EVALUACIÓN

Eres un experto evaluador que debe crear un plan detallado para evaluar el siguiente criterio:

CRITERIO: {criterio.nombre}
DESCRIPCIÓN: {criterio.descripcion}
PONDERACIÓN: {criterio.ponderacion * 100}%

NIVELES DE EVALUACIÓN:
{self._format_evaluation_levels(criterio)}

EVIDENCIAS DISPONIBLES:
{self._format_evidence(evidencias)}

INSTRUCCIONES DE PLANIFICACIÓN:
1. Analiza el criterio y determina qué aspectos específicos debes evaluar
2. Identifica qué evidencias son más relevantes para cada aspecto
3. Define un plan paso a paso para la evaluación
4. Establece criterios de puntuación específicos
5. Considera posibles casos edge y excepciones

FORMATO DE RESPUESTA:
{{
    "aspectos_a_evaluar": ["aspecto1", "aspecto2", "aspecto3"],
    "evidencias_relevantes": {{"aspecto1": ["evidencia1"], "aspecto2": ["evidencia2"]}},
    "plan_evaluacion": ["paso1", "paso2", "paso3"],
    "criterios_puntuacion": {{"0-25%": "descripción", "26-50%": "descripción", "51-75%": "descripción", "76-100%": "descripción"}},
    "consideraciones_especiales": ["consideración1", "consideración2"]
}}

Responde ÚNICAMENTE con JSON válido en ESPAÑOL.
"""
    
    def _build_reasoning_prompt(self, criterio, evidencias: Dict[str, Any], plan: str) -> str:
        """Construye el prompt de reasoning usando chain-of-thought."""
        
        return f"""
CHAIN-OF-THOUGHT REASONING: ANÁLISIS DETALLADO

Eres un evaluador experto que debe realizar un análisis detallado paso a paso.

CRITERIO: {criterio.nombre}
PLAN DE EVALUACIÓN: {plan}

EVIDENCIAS A ANALIZAR:
{self._format_evidence(evidencias)}

INSTRUCCIONES DE REASONING:
1. Sigue el plan de evaluación paso a paso
2. Para cada aspecto, analiza las evidencias disponibles
3. Aplica el criterio de evaluación de manera rigurosa
4. Considera tanto aspectos positivos como negativos
5. Documenta tu razonamiento de manera clara y lógica

FORMATO DE RESPUESTA:
{{
    "analisis_por_aspecto": {{
        "aspecto1": {{
            "evidencias_encontradas": ["evidencia1", "evidencia2"],
            "analisis": "Análisis detallado del aspecto",
            "fortalezas": ["fortaleza1", "fortaleza2"],
            "debilidades": ["debilidad1", "debilidad2"],
            "puntuacion_parcial": 75
        }}
    }},
    "sintesis_general": "Síntesis del análisis completo",
    "puntuacion_tentativa": 80,
    "razonamiento_final": "Explicación detallada de la puntuación final"
}}

Responde ÚNICAMENTE con JSON válido en ESPAÑOL.
"""
    
    def _build_evaluation_prompt(self, criterio, evidencias: Dict[str, Any], reasoning: str) -> str:
        """Construye el prompt de evaluación final."""
        
        return f"""
EVALUACIÓN FINAL: DETERMINACIÓN DE PUNTUACIÓN

Eres un evaluador experto que debe determinar la puntuación final basada en el análisis realizado.

CRITERIO: {criterio.nombre}
ANÁLISIS REALIZADO: {reasoning}

NIVELES DE EVALUACIÓN:
{self._format_evaluation_levels(criterio)}

INSTRUCCIONES FINALES:
1. Basándote en el análisis detallado, determina la puntuación final
2. Asegúrate de que la puntuación refleje el nivel de cumplimiento real
3. Proporciona retroalimentación específica y constructiva
4. Incluye evidencias concretas que respalden tu evaluación
5. Ofrece sugerencias de mejora accionables

FORMATO DE RESPUESTA:
{{
    "puntuacion": 85,
    "nota": 6.1,
    "retroalimentacion": "Retroalimentación detallada y específica en español",
    "evidencias": ["evidencia1", "evidencia2"],
    "sugerencias": ["sugerencia1", "sugerencia2"],
    "justificacion_puntuacion": "Justificación detallada de por qué se asignó esta puntuación"
}}

Responde ÚNICAMENTE con JSON válido en ESPAÑOL.
"""
    
    def _build_validation_prompt(self, criterio, evaluation: str) -> str:
        """Construye el prompt de validación y auto-reflexión."""
        
        return f"""
AUTO-VALIDACIÓN: VERIFICACIÓN DE EVALUACIÓN

Eres un supervisor que debe validar la calidad de la evaluación realizada.

CRITERIO: {criterio.nombre}
EVALUACIÓN REALIZADA: {evaluation}

CRITERIOS DE VALIDACIÓN:
1. ¿La puntuación es consistente con las evidencias?
2. ¿La retroalimentación es específica y constructiva?
3. ¿Las sugerencias son accionables y relevantes?
4. ¿Se consideraron todos los aspectos importantes del criterio?
5. ¿La evaluación es imparcial y objetiva?

FORMATO DE RESPUESTA:
{{
    "validacion_general": "Válida" o "Requiere revisión",
    "puntuacion_consistente": true/false,
    "retroalimentacion_adecuada": true/false,
    "sugerencias_utiles": true/false,
    "aspectos_considerados": true/false,
    "evaluacion_imparcial": true/false,
    "observaciones": "Observaciones adicionales sobre la calidad de la evaluación",
    "confidence_score": 0.85
}}

Responde ÚNICAMENTE con JSON válido en ESPAÑOL.
"""
    
    def _call_llm(self, prompt: str) -> str:
        """Realiza la llamada al LLM con manejo de errores."""
        try:
            if self.provider == "github":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "Eres un evaluador experto en proyectos de Machine Learning. SIEMPRE responde en ESPAÑOL con JSON válido."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.1,
                    max_tokens=2000
                )
                return response.choices[0].message.content
                
            elif self.provider == "ollama":
                payload = {
                    "model": self.model,
                    "prompt": f"Eres un evaluador experto en proyectos de Machine Learning. SIEMPRE responde en ESPAÑOL con JSON válido.\n\n{prompt}",
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "num_predict": 2000,
                        "top_p": 0.9,
                        "stop": ["```", "---", "==="]
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
            print(f"Error en llamada LLM: {e}")
            return self._generate_fallback_response()
    
    def _generate_fallback_response(self) -> str:
        """Genera una respuesta de respaldo cuando falla la llamada al LLM."""
        return json.dumps({
            "puntuacion": 60,
            "nota": 4.6,
            "retroalimentacion": "Evaluación automática generada debido a limitaciones técnicas. Se recomienda revisión manual.",
            "evidencias": [],
            "sugerencias": ["Revisar manualmente este criterio", "Consultar la rúbrica de evaluación"],
            "justificacion_puntuacion": "Puntuación por defecto debido a error técnico"
        }, ensure_ascii=False)
    
    def _parse_advanced_evaluation(self, evaluation: str, validation: str, criterio_nombre: str) -> AdvancedEvaluation:
        """Parsea la evaluación avanzada y la estructura."""
        try:
            # Parsear evaluación
            eval_data = self._extract_json(evaluation)
            val_data = self._extract_json(validation)
            
            # Crear pasos de reasoning
            reasoning_steps = [
                EvaluationStep(
                    step_name="Planificación",
                    description="Análisis del criterio y planificación de evaluación",
                    reasoning="Se analizó el criterio y se creó un plan de evaluación estructurado",
                    evidence=[],
                    confidence=0.9
                ),
                EvaluationStep(
                    step_name="Análisis",
                    description="Análisis detallado de evidencias",
                    reasoning="Se realizó un análisis paso a paso de las evidencias disponibles",
                    evidence=eval_data.get('evidencias', []),
                    confidence=0.8
                ),
                EvaluationStep(
                    step_name="Evaluación",
                    description="Determinación de puntuación final",
                    reasoning=eval_data.get('justificacion_puntuacion', ''),
                    evidence=eval_data.get('evidencias', []),
                    confidence=val_data.get('confidence_score', 0.7)
                )
            ]
            
            return AdvancedEvaluation(
                criterio=criterio_nombre,
                puntuacion=eval_data.get('puntuacion', 60),
                nota=eval_data.get('nota', 4.6),
                retroalimentacion=eval_data.get('retroalimentacion', ''),
                evidencias=eval_data.get('evidencias', []),
                sugerencias=eval_data.get('sugerencias', []),
                reasoning_steps=reasoning_steps,
                confidence_score=val_data.get('confidence_score', 0.7),
                validation_checks=[
                    f"Puntuación consistente: {val_data.get('puntuacion_consistente', False)}",
                    f"Retroalimentación adecuada: {val_data.get('retroalimentacion_adecuada', False)}",
                    f"Sugerencias útiles: {val_data.get('sugerencias_utiles', False)}"
                ]
            )
            
        except Exception as e:
            print(f"Error parseando evaluación avanzada: {e}")
            return self._create_fallback_evaluation(criterio_nombre)
    
    def _extract_json(self, text: str) -> Dict:
        """Extrae JSON de una respuesta de texto."""
        try:
            start = text.find('{')
            end = text.rfind('}') + 1
            json_str = text[start:end]
            return json.loads(json_str)
        except:
            return {}
    
    def _create_fallback_evaluation(self, criterio_nombre: str) -> AdvancedEvaluation:
        """Crea una evaluación de respaldo."""
        return AdvancedEvaluation(
            criterio=criterio_nombre,
            puntuacion=60,
            nota=4.6,
            retroalimentacion=f"Evaluación automática para {criterio_nombre}. Se recomienda revisión manual.",
            evidencias=[],
            sugerencias=["Revisar manualmente este criterio"],
            reasoning_steps=[],
            confidence_score=0.5,
            validation_checks=["Evaluación de respaldo generada"]
        )
    
    def _format_evaluation_levels(self, criterio) -> str:
        """Formatea los niveles de evaluación."""
        levels = []
        for porcentaje, descripcion in criterio.niveles.items():
            nota = 1.0 + (porcentaje / 100) * 6.0
            levels.append(f"- {porcentaje}% (Nota {nota:.1f}): {descripcion}")
        return "\n".join(levels)
    
    def _format_evidence(self, evidencias: Dict[str, Any]) -> str:
        """Formatea las evidencias disponibles."""
        evidence_text = []
        
        if evidencias.get('directories'):
            evidence_text.append(f"Directorios: {list(evidencias['directories'])}")
        
        if evidencias.get('files'):
            evidence_text.append(f"Archivos: {list(evidencias['files'].keys())}")
        
        if evidencias.get('readme'):
            evidence_text.append("README: Presente")
        
        if evidencias.get('requirements'):
            evidence_text.append("Requirements: Presente")
        
        if evidencias.get('has_gitignore'):
            evidence_text.append(".gitignore: Presente")
        
        return "\n".join(evidence_text) if evidence_text else "No hay evidencias específicas"
