#!/usr/bin/env python3
"""
Script de validación para verificar que el sistema esté configurado correctamente.
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

def print_header(title):
    """Imprime header formateado."""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def check_environment():
    """Verifica el entorno Python."""
    print_header("VERIFICACIÓN DEL ENTORNO")
    
    # Versión de Python
    version = sys.version_info
    if version >= (3, 8):
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Se requiere 3.8+")
        return False
    
    # Entorno virtual
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Entorno virtual - Activo")
    else:
        print("⚠️  Entorno virtual - No detectado (recomendado)")
    
    return True

def check_dependencies():
    """Verifica dependencias instaladas."""
    print_header("VERIFICACIÓN DE DEPENDENCIAS")
    
    required_packages = [
        ("requests", "Comunicación HTTP"),
        ("PyGithub", "API de GitHub"),
        ("openai", "API OpenAI/GitHub Models"),
        ("google-generativeai", "Google Gemini"),
        ("pandas", "Manejo de datos"),
        ("python-dotenv", "Variables de entorno")
    ]
    
    all_ok = True
    
    for package, description in required_packages:
        try:
            if package == 'PyGithub':
                import github
            elif package == 'google-generativeai':
                import google.generativeai
            elif package == 'python-dotenv':
                import dotenv
            else:
                __import__(package.lower().replace('-', '_'))
            print(f"✅ {package} - Instalado ({description})")
        except ImportError:
            print(f"❌ {package} - No encontrado ({description})")
            all_ok = False
    
    return all_ok

def check_files():
    """Verifica que los archivos necesarios existan."""
    print_header("VERIFICACIÓN DE ARCHIVOS")
    
    required_files = [
        ("src/rubrica_evaluator.py", "Módulo principal"),
        ("src/config.py", "Configuración"),
        ("simple_evaluator.py", "Interface simplificada"),
        ("requirements.txt", "Lista de dependencias"),
        (".env.example", "Plantilla de configuración")
    ]
    
    optional_files = [
        (".env", "Configuración de APIs"),
        ("evaluaciones/", "Directorio de resultados")
    ]
    
    all_required_ok = True
    
    for file_path, description in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"✅ {file_path} - Encontrado ({description})")
        else:
            print(f"❌ {file_path} - Faltante ({description})")
            all_required_ok = False
    
    print("\nArchivos opcionales:")
    for file_path, description in optional_files:
        path = Path(file_path)
        if path.exists():
            print(f"✅ {file_path} - Encontrado ({description})")
        else:
            print(f"⚠️  {file_path} - No encontrado ({description})")
    
    return all_required_ok

def check_configuration():
    """Verifica la configuración de APIs."""
    print_header("VERIFICACIÓN DE CONFIGURACIÓN")
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Verificar configuración
    sys.path.append("src")
    try:
        from config import Config
        
        github_token = Config.GITHUB_TOKEN
        llm_api_key = Config.LLM_API_KEY
        llm_provider = Config.LLM_PROVIDER
        
        print(f"🤖 Proveedor LLM: {llm_provider}")
        
        if github_token:
            print(f"✅ GitHub Token - Configurado ({len(github_token[:10])}...)")
        else:
            print("❌ GitHub Token - No configurado")
            return False
        
        if llm_provider == "ollama":
            print("✅ LLM API Key - No requerido para Ollama")
        else:
            if llm_api_key:
                print(f"✅ LLM API Key - Configurado ({len(llm_api_key[:10])}...)")
            else:
                print("❌ LLM API Key - No configurado")
                return False
        
        return True
        
    except ImportError as e:
        print(f"❌ Error importando configuración: {e}")
        return False

def test_github_connection():
    """Prueba la conexión a GitHub."""
    print_header("PRUEBA DE CONEXIÓN A GITHUB")
    
    try:
        load_dotenv()
        github_token = os.getenv("GITHUB_TOKEN")
        
        if not github_token:
            print("❌ Token de GitHub no configurado")
            return False
        
        from github import Github, Auth
        
        g = Github(auth=Auth.Token(github_token))
        user = g.get_user()
        
        print(f"✅ Conectado como: {user.login}")
        rate_limit = g.get_rate_limit()
        print(f"📊 Límites de API: {rate_limit.rate.remaining}/{rate_limit.rate.limit}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error conectando a GitHub: {e}")
        return False

def test_llm_connection():
    """Prueba la conexión al LLM."""
    print_header("PRUEBA DE CONEXIÓN A LLM")
    
    try:
        load_dotenv()
        
        sys.path.append("src")
        from config import Config
        from rubrica_evaluator import LLMEvaluator
        
        if Config.LLM_PROVIDER == "ollama":
            print("🔧 Probando conexión a Ollama...")
            try:
                import ollama
                models = ollama.list()
                print(f"✅ Ollama conectado - {len(models['models'])} modelos disponibles")
                return True
            except Exception as e:
                print(f"❌ Error conectando a Ollama: {e}")
                return False
        
        else:
            print(f"🔧 Probando conexión a {Config.LLM_PROVIDER}...")
            
            # Test básico del evaluador
            evaluator = LLMEvaluator(Config.LLM_PROVIDER, Config.LLM_API_KEY)
            print(f"✅ Cliente {Config.LLM_PROVIDER} inicializado correctamente")
            
            return True
            
    except Exception as e:
        print(f"❌ Error probando LLM: {e}")
        return False

def test_basic_functionality():
    """Prueba funcionalidad básica del sistema."""
    print_header("PRUEBA DE FUNCIONALIDAD BÁSICA")
    
    try:
        sys.path.append("src")
        from rubrica_evaluator import create_kedro_rubrica, RubricaEvaluator
        
        # Probar creación de rúbrica
        rubrica_dict = create_kedro_rubrica()
        print(f"✅ Rúbrica Kedro creada - {len(rubrica_dict['criterios'])} criterios")
        
        # Verificar ponderaciones
        total_ponderacion = sum(c["ponderacion"] for c in rubrica_dict["criterios"])
        if abs(total_ponderacion - 1.0) < 0.01:
            print(f"✅ Ponderaciones correctas - Total: {total_ponderacion:.2f}")
        else:
            print(f"⚠️  Ponderaciones incorrectas - Total: {total_ponderacion:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en funcionalidad básica: {e}")
        return False

def run_sample_evaluation():
    """Ejecuta una evaluación de muestra."""
    print_header("EVALUACIÓN DE MUESTRA")
    
    try:
        load_dotenv()
        sys.path.append("src")
        
        from config import Config
        
        if not Config.validate_config():
            print("❌ Configuración incompleta - saltando evaluación de muestra")
            return False
        
        print("🚀 Ejecutando evaluación de muestra...")
        print("📍 Repositorio: https://github.com/octocat/Hello-World")
        
        # Importar después de validar configuración
        from rubrica_evaluator import RubricaEvaluator, create_kedro_rubrica
        
        evaluador = RubricaEvaluator(
            github_token=Config.GITHUB_TOKEN,
            llm_provider=Config.LLM_PROVIDER,
            llm_api_key=Config.LLM_API_KEY
        )
        
        rubrica_dict = create_kedro_rubrica()
        rubrica = evaluador.load_rubrica_from_dict(rubrica_dict)
        
        # Evaluación de muestra con repo simple
        repo_url = "https://github.com/octocat/Hello-World"
        evaluacion = evaluador.evaluate_repository(repo_url, rubrica)
        
        print(f"✅ Evaluación completada")
        print(f"📊 Nota obtenida: {evaluacion.nota_final}/7.0")
        print(f"⏱️  Tiempo: {evaluacion.tiempo_evaluacion:.1f}s")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en evaluación de muestra: {e}")
        print("💡 Esto es normal si las APIs tienen límites o el repo no es accesible")
        return False

def generate_report(results):
    """Genera reporte de validación."""
    print_header("REPORTE DE VALIDACIÓN")
    
    total_checks = len(results)
    passed_checks = sum(1 for result in results.values() if result)
    
    print(f"📊 Resultados: {passed_checks}/{total_checks} verificaciones exitosas")
    
    if passed_checks == total_checks:
        print("🎉 ¡Todas las verificaciones pasaron!")
        print("✅ El sistema está listo para usar")
        status = "COMPLETO"
    elif passed_checks >= total_checks - 2:
        print("⚠️  Configuración casi completa")
        print("🔧 Revisar elementos marcados como ❌")
        status = "PARCIAL"
    else:
        print("❌ Configuración incompleta")
        print("🔧 Revisar configuración antes de usar")
        status = "INCOMPLETO"
    
    print(f"\n🏷️  Estado: {status}")
    
    return status

def main():
    """Función principal de validación."""
    print("🔍 VALIDADOR DE CONFIGURACIÓN")
    print("Verificando que el sistema esté configurado correctamente...")
    
    # Ejecutar verificaciones
    results = {
        "environment": check_environment(),
        "dependencies": check_dependencies(), 
        "files": check_files(),
        "configuration": check_configuration(),
        "github": test_github_connection(),
        "llm": test_llm_connection(),
        "functionality": test_basic_functionality()
    }
    
    # Evaluación opcional (puede fallar sin afectar el resultado principal)
    print("\n🧪 PRUEBA OPCIONAL:")
    sample_result = run_sample_evaluation()
    if sample_result:
        results["sample_evaluation"] = True
    
    # Generar reporte final
    status = generate_report(results)
    
    # Mostrar próximos pasos
    if status == "COMPLETO":
        print(f"\n🚀 PRÓXIMOS PASOS:")
        print("python simple_evaluator.py --repo https://github.com/tu-usuario/tu-proyecto")
    elif status == "PARCIAL":
        print(f"\n🔧 ACCIONES RECOMENDADAS:")
        if not results.get("configuration"):
            print("• Configurar tokens en archivo .env")
        if not results.get("github"):
            print("• Verificar token de GitHub")
        if not results.get("llm"):
            print("• Verificar API key del proveedor LLM")
    else:
        print(f"\n📚 AYUDA:")
        print("• Ejecuta: python setup.py")
        print("• Lee: README.md")
        print("• Revisa: .env.example")
    
    return 0 if status == "COMPLETO" else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
