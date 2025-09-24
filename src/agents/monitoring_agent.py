#!/usr/bin/env python3
"""
Agente de Monitoreo y Alertas Inteligentes
Monitorea el progreso de estudiantes y detecta patrones preocupantes
"""

import os
import json
import sys
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import openai
import requests
from dotenv import load_dotenv

# Agregar src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config import Config

# Cargar variables de entorno
load_dotenv()

@dataclass
class Alert:
    """Alerta generada por el agente de monitoreo."""
    tipo: str  # "progreso", "plagio", "riesgo_academico", "mejora"
    severidad: str  # "baja", "media", "alta", "critica"
    titulo: str
    descripcion: str
    estudiante: str
    evidencias: List[str]
    recomendaciones: List[str]
    timestamp: datetime

@dataclass
class StudentProgress:
    """Progreso de un estudiante a lo largo del tiempo."""
    estudiante_id: str
    nombre: str
    evaluaciones: List[Dict]
    tendencia: str  # "mejorando", "estable", "empeorando"
    nota_promedio: float
    areas_fuertes: List[str]
    areas_debiles: List[str]
    ultima_evaluacion: datetime

class MonitoringAgent:
    """Agente que monitorea el progreso y detecta alertas."""
    
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
        
        # Umbrales para alertas
        self.thresholds = {
            "nota_baja": 3.0,
            "nota_muy_baja": 2.0,
            "degradacion_rapida": 1.0,  # Diferencia entre evaluaciones
            "sin_progreso": 0.2,  # Diferencia mínima esperada
            "plagio_similarity": 0.8  # Similitud entre proyectos
        }
    
    def monitor_student_progress(self, student_evaluations: List[Dict]) -> StudentProgress:
        """Monitorea el progreso de un estudiante específico."""
        
        if not student_evaluations:
            return None
        
        # Ordenar evaluaciones por fecha
        sorted_evaluations = sorted(
            student_evaluations, 
            key=lambda x: x.get('fecha_evaluacion', ''),
            reverse=True
        )
        
        # Calcular métricas
        notas = [e.get('nota_final', 0) for e in sorted_evaluations]
        nota_promedio = sum(notas) / len(notas)
        
        # Determinar tendencia
        if len(notas) >= 2:
            diferencia = notas[0] - notas[-1]  # Última vs primera
            if diferencia > self.thresholds["sin_progreso"]:
                tendencia = "mejorando"
            elif diferencia < -self.thresholds["sin_progreso"]:
                tendencia = "empeorando"
            else:
                tendencia = "estable"
        else:
            tendencia = "estable"
        
        # Identificar áreas fuertes y débiles
        areas_fuertes, areas_debiles = self._analyze_criteria_strengths(sorted_evaluations[0])
        
        return StudentProgress(
            estudiante_id=sorted_evaluations[0].get('estudiante_id', ''),
            nombre=sorted_evaluations[0].get('estudiante', ''),
            evaluaciones=sorted_evaluations,
            tendencia=tendencia,
            nota_promedio=nota_promedio,
            areas_fuertes=areas_fuertes,
            areas_debiles=areas_debiles,
            ultima_evaluacion=datetime.fromisoformat(
                sorted_evaluations[0].get('fecha_evaluacion', datetime.now().isoformat())
            )
        )
    
    def generate_alerts(self, all_evaluations: List[Dict]) -> List[Alert]:
        """Genera alertas basadas en todas las evaluaciones."""
        
        alerts = []
        
        # Agrupar evaluaciones por estudiante
        by_student = {}
        for eval_data in all_evaluations:
            student_id = eval_data.get('estudiante_id', eval_data.get('repositorio', ''))
            if student_id not in by_student:
                by_student[student_id] = []
            by_student[student_id].append(eval_data)
        
        # Analizar cada estudiante
        for student_id, evaluations in by_student.items():
            student_alerts = self._analyze_student_alerts(student_id, evaluations)
            alerts.extend(student_alerts)
        
        # Detectar patrones de plagio
        plagiarism_alerts = self._detect_plagiarism_patterns(all_evaluations)
        alerts.extend(plagiarism_alerts)
        
        # Ordenar por severidad
        severity_order = {"critica": 4, "alta": 3, "media": 2, "baja": 1}
        alerts.sort(key=lambda x: severity_order.get(x.severidad, 0), reverse=True)
        
        return alerts
    
    def _analyze_student_alerts(self, student_id: str, evaluations: List[Dict]) -> List[Alert]:
        """Analiza alertas para un estudiante específico."""
        
        alerts = []
        
        if not evaluations:
            return alerts
        
        # Ordenar por fecha
        sorted_evaluations = sorted(
            evaluations, 
            key=lambda x: x.get('fecha_evaluacion', ''),
            reverse=True
        )
        
        latest_eval = sorted_evaluations[0]
        student_name = latest_eval.get('estudiante', student_id)
        latest_nota = latest_eval.get('nota_final', 0)
        
        # Alerta por nota muy baja
        if latest_nota < self.thresholds["nota_muy_baja"]:
            alerts.append(Alert(
                tipo="riesgo_academico",
                severidad="critica",
                titulo=f"Nota crítica: {latest_nota}/7.0",
                descripcion=f"El estudiante {student_name} tiene una nota muy baja que requiere atención inmediata.",
                estudiante=student_name,
                evidencias=[f"Nota actual: {latest_nota}/7.0"],
                recomendaciones=[
                    "Reunión urgente con el estudiante",
                    "Revisar dificultades específicas",
                    "Considerar apoyo académico adicional"
                ],
                timestamp=datetime.now()
            ))
        
        # Alerta por nota baja
        elif latest_nota < self.thresholds["nota_baja"]:
            alerts.append(Alert(
                tipo="riesgo_academico",
                severidad="alta",
                titulo=f"Nota baja: {latest_nota}/7.0",
                descripcion=f"El estudiante {student_name} tiene una nota por debajo del umbral mínimo.",
                estudiante=student_name,
                evidencias=[f"Nota actual: {latest_nota}/7.0"],
                recomendaciones=[
                    "Seguimiento personalizado",
                    "Identificar áreas de mejora específicas",
                    "Proporcionar recursos adicionales"
                ],
                timestamp=datetime.now()
            ))
        
        # Alerta por degradación rápida
        if len(sorted_evaluations) >= 2:
            nota_anterior = sorted_evaluations[1].get('nota_final', 0)
            diferencia = nota_anterior - latest_nota
            
            if diferencia > self.thresholds["degradacion_rapida"]:
                alerts.append(Alert(
                    tipo="progreso",
                    severidad="alta",
                    titulo="Degradación rápida en el rendimiento",
                    descripcion=f"El estudiante {student_name} ha tenido una caída significativa en su rendimiento.",
                    estudiante=student_name,
                    evidencias=[
                        f"Nota anterior: {nota_anterior}/7.0",
                        f"Nota actual: {latest_nota}/7.0",
                        f"Diferencia: -{diferencia:.1f}"
                    ],
                    recomendaciones=[
                        "Investigar causas de la degradación",
                        "Revisar carga de trabajo",
                        "Ofrecer apoyo adicional"
                    ],
                    timestamp=datetime.now()
                ))
        
        # Alerta por falta de progreso
        if len(sorted_evaluations) >= 3:
            notas_recientes = [e.get('nota_final', 0) for e in sorted_evaluations[:3]]
            variacion = max(notas_recientes) - min(notas_recientes)
            
            if variacion < self.thresholds["sin_progreso"]:
                alerts.append(Alert(
                    tipo="progreso",
                    severidad="media",
                    titulo="Estancamiento en el progreso",
                    descripcion=f"El estudiante {student_name} muestra poco progreso en las últimas evaluaciones.",
                    estudiante=student_name,
                    evidencias=[
                        f"Notas recientes: {', '.join([f'{n:.1f}' for n in notas_recientes])}",
                        f"Variación: {variacion:.1f}"
                    ],
                    recomendaciones=[
                        "Identificar barreras al aprendizaje",
                        "Ajustar estrategia de enseñanza",
                        "Proporcionar desafíos adicionales"
                    ],
                    timestamp=datetime.now()
                ))
        
        return alerts
    
    def _detect_plagiarism_patterns(self, all_evaluations: List[Dict]) -> List[Alert]:
        """Detecta posibles patrones de plagio."""
        
        alerts = []
        
        # Agrupar por criterios y buscar similitudes
        criteria_groups = {}
        
        for eval_data in all_evaluations:
            for criterio in eval_data.get('criterios', []):
                criterio_name = criterio.get('criterio', '')
                retroalimentacion = criterio.get('retroalimentacion', '')
                
                if criterio_name not in criteria_groups:
                    criteria_groups[criterio_name] = []
                
                criteria_groups[criterio_name].append({
                    'estudiante': eval_data.get('estudiante', ''),
                    'retroalimentacion': retroalimentacion,
                    'evaluacion': eval_data
                })
        
        # Buscar similitudes en retroalimentaciones
        for criterio_name, evaluaciones in criteria_groups.items():
            if len(evaluaciones) < 2:
                continue
            
            # Comparar retroalimentaciones (simplificado)
            similarities = self._find_text_similarities(evaluaciones)
            
            for sim in similarities:
                if sim['similarity'] > self.thresholds["plagio_similarity"]:
                    alerts.append(Alert(
                        tipo="plagio",
                        severidad="alta",
                        titulo="Posible similitud en proyectos",
                        descripcion=f"Se detectó similitud alta en el criterio '{criterio_name}' entre estudiantes.",
                        estudiante=f"{sim['student1']} y {sim['student2']}",
                        evidencias=[
                            f"Criterio: {criterio_name}",
                            f"Similitud: {sim['similarity']:.2f}",
                            f"Estudiantes: {sim['student1']}, {sim['student2']}"
                        ],
                        recomendaciones=[
                            "Revisar manualmente los proyectos",
                            "Verificar originalidad del trabajo",
                            "Aplicar políticas de integridad académica"
                        ],
                        timestamp=datetime.now()
                    ))
        
        return alerts
    
    def _find_text_similarities(self, evaluations: List[Dict]) -> List[Dict]:
        """Encuentra similitudes entre textos (implementación simplificada)."""
        
        similarities = []
        
        for i, eval1 in enumerate(evaluations):
            for j, eval2 in enumerate(evaluations[i+1:], i+1):
                text1 = eval1['retroalimentacion'].lower()
                text2 = eval2['retroalimentacion'].lower()
                
                # Similitud básica por palabras comunes
                words1 = set(text1.split())
                words2 = set(text2.split())
                
                if len(words1) > 0 and len(words2) > 0:
                    common_words = words1.intersection(words2)
                    similarity = len(common_words) / max(len(words1), len(words2))
                    
                    if similarity > 0.5:  # Umbral de similitud
                        similarities.append({
                            'student1': eval1['estudiante'],
                            'student2': eval2['estudiante'],
                            'similarity': similarity
                        })
        
        return similarities
    
    def _analyze_criteria_strengths(self, evaluation: Dict) -> tuple:
        """Analiza las fortalezas y debilidades de un estudiante."""
        
        areas_fuertes = []
        areas_debiles = []
        
        for criterio in evaluation.get('criterios', []):
            puntuacion = criterio.get('puntuacion', 0)
            nombre = criterio.get('criterio', '')
            
            if puntuacion >= 80:
                areas_fuertes.append(nombre)
            elif puntuacion < 60:
                areas_debiles.append(nombre)
        
        return areas_fuertes, areas_debiles
    
    def generate_monitoring_report(self, alerts: List[Alert], progress_data: List[StudentProgress]) -> str:
        """Genera un reporte de monitoreo completo."""
        
        report = f"""# 🚨 Reporte de Monitoreo Inteligente

**Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}  
**Total Alertas:** {len(alerts)}  
**Estudiantes Monitoreados:** {len(progress_data)}

## 🔴 Alertas Críticas

"""
        
        # Filtrar alertas críticas
        critical_alerts = [a for a in alerts if a.severidad == "critica"]
        
        if critical_alerts:
            for alert in critical_alerts:
                report += f"### 🚨 {alert.titulo}\n\n"
                report += f"**Estudiante:** {alert.estudiante}\n"
                report += f"**Tipo:** {alert.tipo}\n"
                report += f"**Descripción:** {alert.descripcion}\n\n"
                
                if alert.evidencias:
                    report += "**Evidencias:**\n"
                    for evidencia in alert.evidencias:
                        report += f"- {evidencia}\n"
                    report += "\n"
                
                if alert.recomendaciones:
                    report += "**Recomendaciones:**\n"
                    for rec in alert.recomendaciones:
                        report += f"- {rec}\n"
                    report += "\n"
                
                report += "---\n\n"
        else:
            report += "✅ No hay alertas críticas\n\n"
        
        # Alertas por severidad
        for severidad in ["alta", "media", "baja"]:
            severity_alerts = [a for a in alerts if a.severidad == severidad]
            
            if severity_alerts:
                emoji = {"alta": "🟠", "media": "🟡", "baja": "🟢"}[severidad]
                report += f"## {emoji} Alertas {severidad.title()}\n\n"
                
                for alert in severity_alerts[:5]:  # Máximo 5 por severidad
                    report += f"### {alert.titulo}\n"
                    report += f"**Estudiante:** {alert.estudiante}\n"
                    report += f"**Tipo:** {alert.tipo}\n\n"
                
                report += "\n"
        
        # Resumen de progreso
        report += "## 📊 Resumen de Progreso\n\n"
        
        if progress_data:
            # Estadísticas generales
            notas_promedio = [p.nota_promedio for p in progress_data]
            report += f"**Nota promedio general:** {sum(notas_promedio)/len(notas_promedio):.2f}/7.0\n\n"
            
            # Tendencias
            tendencias = {"mejorando": 0, "estable": 0, "empeorando": 0}
            for progress in progress_data:
                tendencias[progress.tendencia] += 1
            
            report += "**Distribución de tendencias:**\n"
            for tendencia, count in tendencias.items():
                emoji = {"mejorando": "📈", "estable": "➡️", "empeorando": "📉"}[tendencia]
                report += f"- {emoji} {tendencia.title()}: {count} estudiantes\n"
            
            report += "\n"
            
            # Top estudiantes
            top_students = sorted(progress_data, key=lambda x: x.nota_promedio, reverse=True)[:3]
            report += "### 🏆 Top 3 Estudiantes\n\n"
            
            for i, student in enumerate(top_students, 1):
                report += f"{i}. **{student.nombre}** - {student.nota_promedio:.2f}/7.0\n"
                report += f"   - Tendencia: {student.tendencia}\n"
                report += f"   - Fortalezas: {', '.join(student.areas_fuertes[:2])}\n\n"
        
        report += f"\n---\n\n*Reporte generado automáticamente el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}*"
        
        return report


# Ejemplo de uso
if __name__ == "__main__":
    # Crear agente
    agent = MonitoringAgent()
    
    # Datos de ejemplo
    sample_evaluations = [
        {
            "estudiante_id": "est1",
            "estudiante": "Juan Pérez",
            "repositorio": "https://github.com/juan/proyecto1",
            "nota_final": 2.1,
            "fecha_evaluacion": "2024-01-15",
            "criterios": [
                {"criterio": "Estructura del Proyecto", "puntuacion": 20, "retroalimentacion": "Proyecto mal estructurado"},
                {"criterio": "Análisis de Datos", "puntuacion": 30, "retroalimentacion": "Análisis básico"},
                {"criterio": "Modelado", "puntuacion": 15, "retroalimentacion": "Modelo no funcional"}
            ]
        },
        {
            "estudiante_id": "est2", 
            "estudiante": "María García",
            "repositorio": "https://github.com/maria/proyecto2",
            "nota_final": 6.2,
            "fecha_evaluacion": "2024-01-15",
            "criterios": [
                {"criterio": "Estructura del Proyecto", "puntuacion": 85, "retroalimentacion": "Excelente organización"},
                {"criterio": "Análisis de Datos", "puntuacion": 90, "retroalimentacion": "Análisis muy completo"},
                {"criterio": "Modelado", "puntuacion": 80, "retroalimentacion": "Modelo bien implementado"}
            ]
        }
    ]
    
    print("🚨 Agente de Monitoreo y Alertas")
    print("=" * 50)
    
    # Monitorear progreso
    print("📊 Monitoreando progreso de estudiantes...")
    progress_data = []
    for student_id in set(e.get('estudiante_id') for e in sample_evaluations):
        student_evals = [e for e in sample_evaluations if e.get('estudiante_id') == student_id]
        progress = agent.monitor_student_progress(student_evals)
        if progress:
            progress_data.append(progress)
    
    print(f"✅ Monitoreados {len(progress_data)} estudiantes")
    
    # Generar alertas
    print("\n🚨 Generando alertas...")
    alerts = agent.generate_alerts(sample_evaluations)
    print(f"✅ Generadas {len(alerts)} alertas")
    
    # Generar reporte
    report = agent.generate_monitoring_report(alerts, progress_data)
    
    print("\n📊 Reporte de monitoreo generado:")
    print(report)
