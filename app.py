#!/usr/bin/env python3
"""
Aplicación Principal - Sistema de Evaluación con Agentes Inteligentes
Interfaz simplificada para evaluar repositorios GitHub
"""

import os
import sys
import argparse
from pathlib import Path

# Agregar src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.agents_manager import AgentsManager
from src.config import Config

def print_banner():
    """Muestra banner de la aplicación."""
    print("🤖" + "="*60 + "🤖")
    print("   SISTEMA DE EVALUACIÓN CON AGENTES INTELIGENTES")
    print("   Evaluación automática de repositorios GitHub con IA")
    print("🤖" + "="*60 + "🤖")

def check_configuration():
    """Verifica que la configuración esté correcta."""
    print("🔧 Verificando configuración...")
    
    if not Config.validate_config():
        print("\n❌ CONFIGURACIÓN INCOMPLETA")
        print("📝 Configura tu archivo .env con:")
        print("   GITHUB_TOKEN=tu_token_de_github")
        print("   LLM_PROVIDER=github")
        print("   LLM_API_KEY=tu_token_de_github")
        print("\n💡 Obtén tu token en: https://github.com/settings/tokens")
        return False
    
    print("✅ Configuración correcta")
    return True

def evaluate_single_repo(repo_url: str, student_name: str = None):
    """Evalúa un repositorio individual."""
    
    if not repo_url.startswith('https://github.com/'):
        print("❌ URL debe ser de GitHub (https://github.com/...)")
        return
    
    print(f"\n🚀 EVALUANDO REPOSITORIO")
    print(f"📍 URL: {repo_url}")
    
    if student_name:
        print(f"👤 Estudiante: {student_name}")
    
    try:
        manager = AgentsManager()
        results = manager.evaluate_with_agents(repo_url, {"nombre": student_name} if student_name else None)
        
        print(f"\n🎯 RESULTADO FINAL:")
        print(f"📊 Nota: {results['evaluacion_basica']['nota_final']}/7.0")
        print(f"🔍 Insights: {len(results['insights'])}")
        print(f"💡 Recomendaciones: {len(results['recomendaciones'])}")
        print(f"🚨 Alertas: {len(results['alertas'])}")
        
        print(f"\n📁 Resultados guardados en: evaluaciones_agentes/")
        
        # Mostrar insight principal
        if results['insights']:
            insight = results['insights'][0]
            print(f"\n🔍 INSIGHT PRINCIPAL:")
            print(f"   {insight['titulo']}")
            print(f"   {insight['descripcion'][:100]}...")
        
        # Mostrar recomendación principal
        if results['recomendaciones']:
            rec = results['recomendaciones'][0]
            print(f"\n💡 RECOMENDACIÓN PRINCIPAL:")
            print(f"   {rec['titulo']}")
            print(f"   Tiempo: {rec['tiempo_estimado']}")
            print(f"   Prioridad: {rec['prioridad']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def evaluate_class(csv_file: str):
    """Evalúa una clase completa."""
    
    if not os.path.exists(csv_file):
        print(f"❌ Archivo no encontrado: {csv_file}")
        return
    
    print(f"\n🎓 EVALUANDO CLASE COMPLETA")
    print(f"📂 Archivo: {csv_file}")
    
    try:
        # Cargar estudiantes
        import csv
        students_data = []
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                students_data.append({
                    'nombre': row.get('nombre', ''),
                    'email': row.get('email', ''),
                    'repo_url': row.get('repo_url', ''),
                    'nivel': row.get('nivel', 'intermedio')
                })
        
        print(f"👥 Estudiantes cargados: {len(students_data)}")
        
        # Confirmar evaluación automáticamente
        print(f"\n⚠️  La evaluación tomará ~{len(students_data) * 3} minutos. Iniciando automáticamente...")
        print("💡 Para cancelar en el futuro, usa Ctrl+C")
        
        # Evaluar
        manager = AgentsManager()
        results = manager.evaluate_class_with_agents(students_data)
        
        print(f"\n🎯 EVALUACIÓN DE CLASE COMPLETADA")
        print(f"👥 Estudiantes: {results['resumen_clase']['total_estudiantes']}")
        print(f"📊 Nota promedio: {results['resumen_clase']['nota_promedio']:.2f}/7.0")
        print(f"🔍 Tendencias: {len(results['tendencias_clase'])}")
        print(f"⚠️  Problemas: {len(results['problemas_comunes'])}")
        print(f"🚨 Alertas: {len(results['alertas_clase'])}")
        
        print(f"\n📁 Reportes guardados en: evaluaciones_agentes/")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def interactive_mode():
    """Modo interactivo."""
    
    print(f"\n🎮 MODO INTERACTIVO")
    print("-" * 30)
    
    while True:
        print(f"\n🎯 MODO INTERACTIVO DISPONIBLE")
        print("Para usar el modo interactivo, ejecuta:")
        print("python app.py")
        print("\n📋 OPCIONES DISPONIBLES:")
        print("1. Evaluar un repositorio:")
        print("   python app.py --repo https://github.com/usuario/proyecto")
        print("2. Evaluar una clase completa:")
        print("   python app.py --class examples/estudiantes_ejemplo.csv")
        print("3. Ver configuración:")
        print("   python config_simple.py")
        
        # Mostrar configuración actual
        print(f"\n🔧 CONFIGURACIÓN ACTUAL:")
        print(f"   GitHub Token: {'✅' if Config.GITHUB_TOKEN else '❌'}")
        print(f"   LLM Provider: {Config.LLM_PROVIDER}")
        print(f"   LLM API Key: {'✅' if Config.LLM_API_KEY else '❌'}")
        
        if Config.LLM_PROVIDER == "github":
            print(f"\n💡 Proveedor: GitHub Models (Recomendado)")
            print(f"   Modelos: gpt-4o-mini, gpt-3.5-turbo")
            print(f"   Gratuito: Sí, límites generosos")
        
        break  # Salir del bucle

def main():
    """Función principal."""
    
    print_banner()
    
    # Verificar configuración
    if not check_configuration():
        return
    
    # Parsear argumentos
    parser = argparse.ArgumentParser(
        description="Sistema de Evaluación con Agentes Inteligentes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python app.py --repo https://github.com/usuario/proyecto
  python app.py --repo https://github.com/usuario/proyecto --student "Juan Pérez"
  python app.py --class estudiantes.csv
  python app.py  # Modo interactivo
        """
    )
    
    parser.add_argument("--repo", type=str, help="URL del repositorio a evaluar")
    parser.add_argument("--student", type=str, help="Nombre del estudiante")
    parser.add_argument("--class", type=str, dest="class_file", help="Archivo CSV con estudiantes")
    
    args = parser.parse_args()
    
    # Ejecutar según argumentos
    if args.repo:
        evaluate_single_repo(args.repo, args.student)
    
    elif args.class_file:
        evaluate_class(args.class_file)
    
    else:
        interactive_mode()

if __name__ == "__main__":
    main()
