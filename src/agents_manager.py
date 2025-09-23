#!/usr/bin/env python3
"""
Gestor de Agentes Inteligentes - Módulo Principal
Coordina todos los agentes para crear un sistema completo de evaluación inteligente
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

# Agregar src al path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from agents import AnalysisAgent, RecommendationAgent, MonitoringAgent
from rubrica_evaluator import RubricaEvaluator, create_kedro_rubrica
from config import Config

class AgentsManager:
    """Gestor principal que coordina todos los agentes inteligentes."""
    
    def __init__(self):
        """Inicializa el gestor y todos los agentes."""
        self.analysis_agent = AnalysisAgent()
        self.recommendation_agent = RecommendationAgent()
        self.monitoring_agent = MonitoringAgent()
        self.evaluator = None
        
        # Directorio de resultados
        self.results_dir = Path("evaluaciones_agentes")
        self.results_dir.mkdir(exist_ok=True)
        
    def initialize_evaluator(self):
        """Inicializa el evaluador principal."""
        if not Config.validate_config():
            raise ValueError("Configuración incompleta. Verifica tu archivo .env")
        
        self.evaluator = RubricaEvaluator(
            github_token=Config.GITHUB_TOKEN,
            llm_provider=Config.LLM_PROVIDER,
            llm_api_key=Config.LLM_API_KEY
        )
    
    def evaluate_with_agents(self, repo_url: str, student_info: Optional[Dict] = None) -> Dict[str, Any]:
        """Evalúa un repositorio y genera insights inteligentes."""
        
        if not self.evaluator:
            self.initialize_evaluator()
        
        print(f"🚀 Evaluando con agentes inteligentes: {repo_url}")
        
        # 1. Evaluación básica
        print("📊 Realizando evaluación básica...")
        rubrica_dict = create_kedro_rubrica()
        rubrica = self.evaluator.load_rubrica_from_dict(rubrica_dict)
        evaluation = self.evaluator.evaluate_repository(repo_url, rubrica)
        
        # 2. Análisis inteligente
        print("🔍 Generando análisis inteligente...")
        evaluation_dict = self._convert_evaluation_to_dict(evaluation)
        insights = self.analysis_agent.generate_improvement_recommendations(evaluation_dict)
        
        # 3. Recomendaciones personalizadas
        print("💡 Creando recomendaciones personalizadas...")
        recommendations = self.recommendation_agent.generate_personalized_recommendations(
            evaluation_dict, student_info
        )
        
        # 4. Monitoreo y alertas
        print("🚨 Generando alertas de monitoreo...")
        alerts = self.monitoring_agent.generate_alerts([evaluation_dict])
        
        # Compilar resultados
        results = {
            "evaluacion_basica": evaluation_dict,
            "insights": [insight.__dict__ for insight in insights],
            "recomendaciones": [rec.__dict__ for rec in recommendations],
            "alertas": [alert.__dict__ for alert in alerts],
            "timestamp": datetime.now().isoformat(),
            "agente_version": "1.0.0"
        }
        
        # Guardar resultados
        self._save_results(results, repo_url)
        
        return results
    
    def evaluate_class_with_agents(self, students_data: List[Dict]) -> Dict[str, Any]:
        """Evalúa una clase completa con análisis inteligente."""
        
        if not self.evaluator:
            self.initialize_evaluator()
        
        print(f"🎓 Evaluando clase completa: {len(students_data)} estudiantes")
        
        all_evaluations = []
        all_results = []
        
        for i, student_data in enumerate(students_data, 1):
            print(f"\n{'='*60}")
            print(f"📊 EVALUANDO {i}/{len(students_data)}: {student_data.get('nombre', 'Estudiante')}")
            print(f"{'='*60}")
            
            try:
                # Evaluar con agentes
                results = self.evaluate_with_agents(
                    student_data['repo_url'], 
                    student_data
                )
                
                all_results.append(results)
                all_evaluations.append(results['evaluacion_basica'])
                
                print(f"✅ Completado - Nota: {results['evaluacion_basica']['nota_final']}/7.0")
                
            except Exception as e:
                print(f"❌ Error: {e}")
                continue
        
        # Análisis de clase completo
        print(f"\n🧠 Generando análisis inteligente de clase...")
        
        # Tendencias generales
        trends = self.analysis_agent.analyze_evaluation_trends(all_evaluations)
        
        # Problemas comunes
        issues = self.analysis_agent.identify_common_issues(all_evaluations)
        
        # Alertas de monitoreo
        class_alerts = self.monitoring_agent.generate_alerts(all_evaluations)
        
        # Compilar resultados de clase
        class_results = {
            "resumen_clase": {
                "total_estudiantes": len(all_evaluations),
                "nota_promedio": sum(e.get('nota_final', 0) for e in all_evaluations) / len(all_evaluations),
                "nota_maxima": max(e.get('nota_final', 0) for e in all_evaluations),
                "nota_minima": min(e.get('nota_final', 0) for e in all_evaluations)
            },
            "evaluaciones_individuales": all_results,
            "tendencias_clase": [trend.__dict__ for trend in trends],
            "problemas_comunes": [issue.__dict__ for issue in issues],
            "alertas_clase": [alert.__dict__ for alert in class_alerts],
            "timestamp": datetime.now().isoformat()
        }
        
        # Guardar resultados de clase
        self._save_class_results(class_results)
        
        # Generar reportes
        self._generate_class_reports(class_results)
        
        return class_results
    
    def _convert_evaluation_to_dict(self, evaluation) -> Dict[str, Any]:
        """Convierte una evaluación a diccionario serializable."""
        return {
            "repositorio": evaluation.repositorio,
            "fecha_evaluacion": evaluation.fecha_evaluacion,
            "criterios": [
                {
                    "criterio": c.criterio,
                    "puntuacion": c.puntuacion,
                    "nota": c.nota,
                    "retroalimentacion": c.retroalimentacion,
                    "evidencias": c.evidencias,
                    "sugerencias": c.sugerencias
                }
                for c in evaluation.criterios
            ],
            "nota_final": evaluation.nota_final,
            "resumen_general": evaluation.resumen_general,
            "tiempo_evaluacion": evaluation.tiempo_evaluacion
        }
    
    def _save_results(self, results: Dict, repo_url: str):
        """Guarda los resultados de una evaluación individual."""
        
        repo_name = repo_url.split('/')[-1]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Guardar JSON completo
        json_path = self.results_dir / f"{repo_name}_agentes_{timestamp}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        
        # Generar reporte HTML
        html_path = self.results_dir / f"{repo_name}_reporte_agentes_{timestamp}.html"
        self._generate_individual_report(results, html_path)
        
        print(f"📁 Resultados guardados:")
        print(f"   - JSON: {json_path}")
        print(f"   - HTML: {html_path}")
    
    def _save_class_results(self, results: Dict):
        """Guarda los resultados de evaluación de clase."""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Guardar JSON completo
        json_path = self.results_dir / f"clase_agentes_{timestamp}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"📁 Resultados de clase guardados: {json_path}")
    
    def _generate_individual_report(self, results: Dict, output_path: Path):
        """Genera reporte HTML para evaluación individual."""
        
        evaluation = results['evaluacion_basica']
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Evaluación Inteligente - {evaluation.get('repositorio', 'Proyecto')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }}
        .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
        .insight {{ background-color: #f8f9fa; padding: 10px; margin: 10px 0; border-left: 4px solid #007bff; }}
        .recommendation {{ background-color: #fff3cd; padding: 10px; margin: 10px 0; border-left: 4px solid #ffc107; }}
        .alert {{ background-color: #f8d7da; padding: 10px; margin: 10px 0; border-left: 4px solid #dc3545; }}
        .nota {{ font-size: 2em; font-weight: bold; color: #28a745; }}
        .criterio {{ margin: 10px 0; padding: 10px; background-color: #f8f9fa; }}
        .timestamp {{ color: #6c757d; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 Evaluación Inteligente con Agentes IA</h1>
        <p><strong>Repositorio:</strong> {evaluation.get('repositorio', 'N/A')}</p>
        <p><strong>Fecha:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        <div class="nota">Nota Final: {evaluation.get('nota_final', 0):.2f}/7.0</div>
    </div>
    
    <div class="section">
        <h2>📊 Evaluación por Criterios</h2>
"""
        
        for criterio in evaluation.get('criterios', []):
            html_content += f"""
        <div class="criterio">
            <h3>{criterio.get('criterio', 'N/A')}</h3>
            <p><strong>Puntuación:</strong> {criterio.get('puntuacion', 0)}%</p>
            <p><strong>Nota:</strong> {criterio.get('nota', 0):.2f}/7.0</p>
            <p><strong>Retroalimentación:</strong> {criterio.get('retroalimentacion', 'N/A')}</p>
        </div>
"""
        
        # Insights
        if results.get('insights'):
            html_content += """
    </div>
    
    <div class="section">
        <h2>🔍 Insights Inteligentes</h2>
"""
            for insight in results['insights']:
                html_content += f"""
        <div class="insight">
            <h3>{insight.get('titulo', 'N/A')}</h3>
            <p>{insight.get('descripcion', 'N/A')}</p>
            <p><strong>Criterios afectados:</strong> {', '.join(insight.get('criterios_afectados', []))}</p>
        </div>
"""
        
        # Recomendaciones
        if results.get('recomendaciones'):
            html_content += """
    </div>
    
    <div class="section">
        <h2>💡 Recomendaciones Personalizadas</h2>
"""
            for rec in results['recomendaciones']:
                html_content += f"""
        <div class="recommendation">
            <h3>{rec.get('titulo', 'N/A')}</h3>
            <p>{rec.get('descripcion', 'N/A')}</p>
            <p><strong>Prioridad:</strong> {rec.get('prioridad', 'N/A')}</p>
            <p><strong>Tiempo estimado:</strong> {rec.get('tiempo_estimado', 'N/A')}</p>
        </div>
"""
        
        html_content += """
    </div>
    
    <div class="timestamp">
        Reporte generado automáticamente por Agentes Inteligentes
    </div>
</body>
</html>
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _generate_class_reports(self, results: Dict):
        """Genera reportes para la evaluación de clase."""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Reporte HTML de clase
        html_path = self.results_dir / f"clase_report_agentes_{timestamp}.html"
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Reporte de Clase - Agentes Inteligentes</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }}
        .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
        .stat-box {{ background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center; }}
        .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
        .alert {{ background-color: #f8d7da; padding: 10px; margin: 10px 0; border-left: 4px solid #dc3545; }}
        .trend {{ background-color: #d4edda; padding: 10px; margin: 10px 0; border-left: 4px solid #28a745; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎓 Reporte de Clase - Agentes Inteligentes</h1>
        <p><strong>Fecha:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
    </div>
    
    <div class="stats">
        <div class="stat-box">
            <h2>{results['resumen_clase']['total_estudiantes']}</h2>
            <p>Estudiantes Evaluados</p>
        </div>
        <div class="stat-box">
            <h2>{results['resumen_clase']['nota_promedio']:.2f}</h2>
            <p>Nota Promedio</p>
        </div>
        <div class="stat-box">
            <h2>{results['resumen_clase']['nota_maxima']:.2f}</h2>
            <p>Nota Máxima</p>
        </div>
        <div class="stat-box">
            <h2>{results['resumen_clase']['nota_minima']:.2f}</h2>
            <p>Nota Mínima</p>
        </div>
    </div>
"""
        
        # Alertas críticas
        if results.get('alertas_clase'):
            critical_alerts = [a for a in results['alertas_clase'] if a.get('severidad') == 'critica']
            if critical_alerts:
                html_content += """
    <div class="section">
        <h2>🚨 Alertas Críticas</h2>
"""
                for alert in critical_alerts:
                    html_content += f"""
        <div class="alert">
            <h3>{alert.get('titulo', 'N/A')}</h3>
            <p><strong>Estudiante:</strong> {alert.get('estudiante', 'N/A')}</p>
            <p>{alert.get('descripcion', 'N/A')}</p>
        </div>
"""
        
        # Tendencias
        if results.get('tendencias_clase'):
            html_content += """
    </div>
    
    <div class="section">
        <h2>📈 Tendencias Identificadas</h2>
"""
            for trend in results['tendencias_clase']:
                html_content += f"""
        <div class="trend">
            <h3>{trend.get('titulo', 'N/A')}</h3>
            <p>{trend.get('descripcion', 'N/A')}</p>
        </div>
"""
        
        html_content += """
    </div>
</body>
</html>
"""
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"📊 Reporte de clase generado: {html_path}")
