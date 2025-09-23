#!/usr/bin/env python3
"""
Demo de Agentes Inteligentes - Módulo de Demostración
Demuestra todas las capacidades del sistema de forma modular
"""

import os
import sys
import time
from pathlib import Path

# Agregar src al path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from agents_manager import AgentsManager
from agents import AnalysisAgent, RecommendationAgent, MonitoringAgent

def print_banner():
    """Muestra banner de bienvenida."""
    print("=" * 70)
    print("🤖 DEMO: AGENTES INTELIGENTES PARA EVALUACIÓN CON RÚBRICAS")
    print("=" * 70)
    print("Sistema completo de evaluación automática con IA")
    print("Basado en GitHub Models API")
    print("=" * 70)

def demo_individual_evaluation():
    """Demo de evaluación individual con agentes."""
    
    print("\n🎯 DEMO 1: EVALUACIÓN INDIVIDUAL CON AGENTES")
    print("-" * 50)
    
    # Crear gestor
    manager = AgentsManager()
    
    # Datos de ejemplo
    repo_url = "https://github.com/kedro-org/kedro-starters"
    student_info = {
        "nombre": "Juan Pérez",
        "nivel": "intermedio",
        "experiencia": "6 meses con Python, 3 meses con ML"
    }
    
    print(f"📊 Evaluando: {repo_url}")
    print(f"👤 Estudiante: {student_info['nombre']}")
    print(f"📚 Nivel: {student_info['nivel']}")
    
    try:
        # Evaluar con agentes
        results = manager.evaluate_with_agents(repo_url, student_info)
        
        print(f"\n✅ EVALUACIÓN COMPLETADA")
        print(f"📈 Nota Final: {results['evaluacion_basica']['nota_final']}/7.0")
        print(f"🔍 Insights Generados: {len(results['insights'])}")
        print(f"💡 Recomendaciones: {len(results['recomendaciones'])}")
        print(f"🚨 Alertas: {len(results['alertas'])}")
        
        # Mostrar algunos insights
        if results['insights']:
            print(f"\n🔍 INSIGHT DESTACADO:")
            insight = results['insights'][0]
            print(f"   📝 {insight['titulo']}")
            print(f"   💭 {insight['descripcion'][:100]}...")
        
        # Mostrar recomendación
        if results['recomendaciones']:
            print(f"\n💡 RECOMENDACIÓN PRINCIPAL:")
            rec = results['recomendaciones'][0]
            print(f"   🎯 {rec['titulo']}")
            print(f"   ⏱️  Tiempo estimado: {rec['tiempo_estimado']}")
            print(f"   📊 Prioridad: {rec['prioridad']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def demo_individual_agents():
    """Demo de agentes individuales."""
    
    print("\n🤖 DEMO 2: AGENTES INDIVIDUALES")
    print("-" * 50)
    
    try:
        # Crear agentes
        analysis_agent = AnalysisAgent()
        recommendation_agent = RecommendationAgent()
        monitoring_agent = MonitoringAgent()
        
        print("✅ Agentes inicializados correctamente")
        
        # Datos de ejemplo
        sample_evaluation = {
            "repositorio": "https://github.com/estudiante/proyecto-ml",
            "nota_final": 4.2,
            "fecha_evaluacion": "2024-01-15",
            "criterios": [
                {"criterio": "Estructura del Proyecto", "puntuacion": 60, "retroalimentacion": "Proyecto bien estructurado pero necesita mejoras en documentación"},
                {"criterio": "Análisis de Datos", "puntuacion": 80, "retroalimentacion": "Excelente análisis exploratorio con visualizaciones claras"},
                {"criterio": "Modelado", "puntuacion": 30, "retroalimentacion": "Modelo básico implementado pero requiere optimización"}
            ]
        }
        
        # Demo Agente de Análisis
        print("\n🔍 Agente de Análisis:")
        insights = analysis_agent.generate_improvement_recommendations(sample_evaluation)
        print(f"   📊 Insights generados: {len(insights)}")
        
        if insights:
            insight = insights[0]
            print(f"   💡 {insight.titulo}")
            print(f"   📝 {insight.descripcion[:80]}...")
        
        # Demo Agente de Recomendaciones
        print("\n💡 Agente de Recomendaciones:")
        student_info = {"nombre": "Ana García", "nivel": "intermedio"}
        recommendations = recommendation_agent.generate_personalized_recommendations(sample_evaluation, student_info)
        print(f"   🎯 Recomendaciones generadas: {len(recommendations)}")
        
        if recommendations:
            rec = recommendations[0]
            print(f"   📋 {rec.titulo}")
            print(f"   ⏱️  Tiempo: {rec.tiempo_estimado}")
            print(f"   📊 Prioridad: {rec.prioridad}")
        
        # Demo Agente de Monitoreo
        print("\n🚨 Agente de Monitoreo:")
        alerts = monitoring_agent.generate_alerts([sample_evaluation])
        print(f"   🚨 Alertas generadas: {len(alerts)}")
        
        if alerts:
            alert = alerts[0]
            print(f"   ⚠️  {alert.titulo}")
            print(f"   📊 Severidad: {alert.severidad}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def show_capabilities():
    """Muestra las capacidades del sistema."""
    
    print("\n🚀 CAPACIDADES DEL SISTEMA")
    print("-" * 50)
    
    capabilities = [
        "✅ Evaluación automática de repositorios GitHub",
        "✅ Rúbricas personalizables (Kedro, Python, React, etc.)",
        "✅ Múltiples proveedores de IA (GitHub Models, Gemini)",
        "✅ Análisis inteligente de tendencias y patrones",
        "✅ Recomendaciones personalizadas por estudiante",
        "✅ Monitoreo y alertas automáticas",
        "✅ Detección de plagio y similitudes",
        "✅ Reportes HTML, JSON y CSV",
        "✅ Evaluación masiva de clases completas",
        "✅ Planes de aprendizaje personalizados",
        "✅ Integración con GitHub API",
        "✅ Sistema de notas chileno (1.0-7.0)"
    ]
    
    for capability in capabilities:
        print(f"   {capability}")
        time.sleep(0.1)  # Efecto visual

def main():
    """Función principal del demo."""
    
    print_banner()
    show_capabilities()
    
    print(f"\n🎬 INICIANDO DEMO INTERACTIVO")
    print("=" * 50)
    
    demos = [
        ("Evaluación Individual", demo_individual_evaluation),
        ("Agentes Individuales", demo_individual_agents)
    ]
    
    for i, (name, demo_func) in enumerate(demos, 1):
        print(f"\n🎯 Ejecutando Demo {i}: {name}")
        print("-" * 30)
        
        success = demo_func()
        
        if success:
            print(f"✅ Demo {i} completado exitosamente")
        else:
            print(f"❌ Demo {i} falló")
        
        if i < len(demos):
            print(f"\n⏸️  Continuando al siguiente demo...")
            time.sleep(2)  # Pausa de 2 segundos
    
    print(f"\n🎉 DEMO COMPLETADO")
    print("=" * 50)
    print("📁 Revisa los archivos generados en:")
    print("   - evaluaciones_agentes/ (resultados con agentes)")
    print("   - evaluaciones/ (resultados básicos)")
    
    print(f"\n🚀 PRÓXIMOS PASOS:")
    print("1. Configura tu archivo .env con tus tokens")
    print("2. Crea tu archivo CSV de estudiantes")
    print("3. Ejecuta: python app.py --help")
    print("4. Personaliza las rúbricas según tus necesidades")
    
    print(f"\n📚 RECURSOS:")
    print("- README.md - Documentación completa")
    print("- examples/ - Ejemplos de rúbricas")
    print("- tests/ - Tests unitarios")

if __name__ == "__main__":
    main()
