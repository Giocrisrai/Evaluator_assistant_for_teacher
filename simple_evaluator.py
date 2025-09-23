# simple_evaluator.py - Script simplificado para evaluar
import asyncio
from pathlib import Path
from dotenv import load_dotenv
import sys
import os

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Cargar variables de entorno
load_dotenv()

from src.config import Config
from src.rubrica_evaluator import RubricaEvaluator, create_kedro_rubrica
from typing import List

def setup_environment():
    """Configura el entorno de evaluación."""
    
    print("🔧 Configurando entorno de evaluación...")
    
    if not Config.validate_config():
        print("\n📝 Pasos para configurar:")
        print("1. Crear token de GitHub: https://github.com/settings/tokens")
        print("2. Elegir proveedor de LLM y obtener API key:")
        
        for provider, info in Config.LLM_PROVIDERS.items():
            print(f"\n   🤖 {provider.upper()}:")
            print(f"      Modelos: {', '.join(info['models'])}")
            print(f"      Gratuito: {info['free_tier']}")
            if 'signup' in info:
                print(f"      Registro: {info['signup']}")
        
        sys.exit(1)
    
    print("✅ Configuración validada correctamente")

def evaluate_single_repository(repo_url: str, rubrica_name: str = "kedro"):
    """Evalúa un repositorio individual."""
    
    setup_environment()
    
    # Inicializar evaluador
    evaluador = RubricaEvaluator(
        github_token=Config.GITHUB_TOKEN,
        llm_provider=Config.LLM_PROVIDER,
        llm_api_key=Config.LLM_API_KEY
    )
    
    # Cargar rúbrica
    if rubrica_name == "kedro":
        rubrica_dict = create_kedro_rubrica()
    else:
        raise ValueError(f"Rúbrica '{rubrica_name}' no encontrada")
    
    rubrica = evaluador.load_rubrica_from_dict(rubrica_dict)
    
    # Crear directorio de salida
    output_dir = Path(Config.DEFAULT_OUTPUT_DIR)
    output_dir.mkdir(exist_ok=True)
    
    # Generar nombre de archivo
    repo_name = repo_url.split('/')[-1]
    output_path = output_dir / f"{repo_name}_evaluacion"
    
    print(f"🚀 Evaluando: {repo_url}")
    print(f"📁 Resultados en: {output_path}")
    
    try:
        # Evaluar
        evaluacion = evaluador.evaluate_repository(repo_url, rubrica)
        
        # Exportar
        evaluador.export_evaluation(evaluacion, str(output_path))
        
        # Mostrar resumen
        print(f"\n🎯 RESULTADO FINAL:")
        print(f"Nota: {evaluacion.nota_final}/7.0")
        print(f"Tiempo: {evaluacion.tiempo_evaluacion:.1f}s")
        
        # Top 3 fortalezas y debilidades
        criterios_ordenados = sorted(
            evaluacion.criterios, 
            key=lambda x: x.puntuacion, 
            reverse=True
        )
        
        print("\n🟢 TOP 3 FORTALEZAS:")
        for i, criterio in enumerate(criterios_ordenados[:3], 1):
            print(f"   {i}. {criterio.criterio}: {criterio.puntuacion}%")
        
        print("\n🟡 ÁREAS DE MEJORA:")
        for i, criterio in enumerate(criterios_ordenados[-3:], 1):
            print(f"   {i}. {criterio.criterio}: {criterio.puntuacion}%")
            if criterio.sugerencias:
                print(f"      → {criterio.sugerencias[0]}")
        
        return evaluacion
        
    except Exception as e:
        print(f"❌ Error durante evaluación: {e}")
        return None

def evaluate_multiple_repositories(repo_urls: List[str], rubrica_name: str = "kedro"):
    """Evalúa múltiples repositorios y genera reporte comparativo."""
    
    evaluaciones = []
    
    for i, repo_url in enumerate(repo_urls, 1):
        print(f"\n{'='*60}")
        print(f"📊 EVALUANDO REPOSITORIO {i}/{len(repo_urls)}")
        print(f"{'='*60}")
        
        evaluacion = evaluate_single_repository(repo_url, rubrica_name)
        if evaluacion:
            evaluaciones.append(evaluacion)
    
    # Generar reporte comparativo
    if evaluaciones:
        generate_comparative_report(evaluaciones)

def generate_comparative_report(evaluaciones: List):
    """Genera reporte comparativo entre múltiples evaluaciones."""
    
    output_dir = Path(Config.DEFAULT_OUTPUT_DIR)
    report_path = output_dir / "reporte_comparativo.html"
    
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Reporte Comparativo de Evaluaciones</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
        th { background-color: #f2f2f2; }
        .best { background-color: #d4edda; }
        .worst { background-color: #f8d7da; }
        .avg { background-color: #fff3cd; }
    </style>
</head>
<body>
    <h1>📊 Reporte Comparativo de Evaluaciones</h1>
    
    <h2>🏆 Ranking General</h2>
    <table>
        <tr>
            <th>Posición</th>
            <th>Repositorio</th>
            <th>Nota Final</th>
            <th>Status</th>
        </tr>
"""
    
    # Ordenar por nota
    evaluaciones_sorted = sorted(evaluaciones, key=lambda x: x.nota_final, reverse=True)
    
    for i, eval in enumerate(evaluaciones_sorted, 1):
        repo_name = eval.repositorio.split('/')[-1]
        status_class = "best" if i == 1 else "worst" if i == len(evaluaciones) else "avg"
        status_text = "🥇 Mejor" if i == 1 else "🥉 A mejorar" if i == len(evaluaciones) else "📊 Promedio"
        
        html_content += f"""
        <tr class="{status_class}">
            <td>{i}</td>
            <td>{repo_name}</td>
            <td>{eval.nota_final:.2f}/7.0</td>
            <td>{status_text}</td>
        </tr>
"""
    
    html_content += """
    </table>
    
    <h2>📈 Análisis por Criterios</h2>
    <table>
        <tr>
            <th>Criterio</th>
"""
    
    for eval in evaluaciones:
        repo_name = eval.repositorio.split('/')[-1]
        html_content += f"<th>{repo_name}</th>"
    
    html_content += "</tr>"
    
    # Obtener todos los criterios
    criterios = evaluaciones[0].criterios
    
    for criterio in criterios:
        html_content += f"<tr><td>{criterio.criterio}</td>"
        
        for eval in evaluaciones:
            # Encontrar criterio correspondiente
            crit_eval = next((c for c in eval.criterios if c.criterio == criterio.criterio), None)
            if crit_eval:
                puntuacion = crit_eval.puntuacion
                class_css = "best" if puntuacion >= 80 else "worst" if puntuacion < 60 else "avg"
                html_content += f'<td class="{class_css}">{puntuacion}%</td>'
            else:
                html_content += '<td>N/A</td>'
        
        html_content += "</tr>"
    
    html_content += """
    </table>
</body>
</html>
"""
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n📊 Reporte comparativo generado: {report_path}")

# CLI Interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Evaluador automático de repositorios")
    parser.add_argument("--repo", type=str, help="URL del repositorio a evaluar")
    parser.add_argument("--repos-file", type=str, help="Archivo con lista de URLs")
    parser.add_argument("--rubrica", type=str, default="kedro", help="Tipo de rúbrica")
    parser.add_argument("--provider", type=str, help="Proveedor LLM (github/gemini/huggingface)")
    
    args = parser.parse_args()
    
    # Sobrescribir proveedor si se especifica
    if args.provider:
        Config.LLM_PROVIDER = args.provider
    
    if args.repo:
        # Evaluar repositorio individual
        evaluate_single_repository(args.repo, args.rubrica)
        
    elif args.repos_file:
        # Evaluar múltiples repositorios
        with open(args.repos_file, 'r') as f:
            repos = [line.strip() for line in f if line.strip()]
        
        evaluate_multiple_repositories(repos, args.rubrica)
        
    else:
        # Modo interactivo
        print("🎓 Evaluador Automático de Repositorios")
        print("="*50)
        
        while True:
            print("\n¿Qué deseas hacer?")
            print("1. Evaluar un repositorio")
            print("2. Evaluar múltiples repositorios")
            print("3. Configurar APIs")
            print("4. Salir")
            
            opcion = input("\nSelecciona opción (1-4): ").strip()
            
            if opcion == "1":
                repo_url = input("Ingresa URL del repositorio: ").strip()
                if repo_url:
                    evaluate_single_repository(repo_url)
                    
            elif opcion == "2":
                print("Ingresa URLs de repositorios (línea vacía para terminar):")
                repos = []
                while True:
                    repo = input("Repositorio: ").strip()
                    if not repo:
                        break
                    repos.append(repo)
                
                if repos:
                    evaluate_multiple_repositories(repos)
                    
            elif opcion == "3":
                print("\n🔧 Configuración de APIs:")
                print(f"GitHub Token: {'✅ Configurado' if Config.GITHUB_TOKEN else '❌ Faltante'}")
                print(f"LLM API Key: {'✅ Configurado' if Config.LLM_API_KEY else '❌ Faltante'}")
                print(f"Proveedor LLM: {Config.LLM_PROVIDER}")
                
                print(f"\nProveedores disponibles:")
                for provider, info in Config.LLM_PROVIDERS.items():
                    print(f"- {provider}: {info['free_tier']}")
                    
            elif opcion == "4":
                print("👋 ¡Hasta luego!")
                break
                
            else:
                print("❌ Opción inválida")
