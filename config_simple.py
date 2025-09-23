#!/usr/bin/env python3
"""
Configurador Automático del Sistema
Ayuda a configurar el sistema paso a paso de forma profesional
"""

import os
import sys
from pathlib import Path

# Agregar src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def create_env_file():
    """Crea archivo .env si no existe."""
    
    env_file = Path(".env")
    
    if env_file.exists():
        print("✅ Archivo .env ya existe")
        return True
    
    print("🔧 Creando archivo .env...")
    
    # Contenido básico
    env_content = """# Configuración del Sistema de Evaluación
GITHUB_TOKEN=tu_token_aqui
LLM_PROVIDER=github
LLM_API_KEY=tu_token_aqui
OPENAI_BASE_URL=https://models.inference.ai.azure.com
"""
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print("✅ Archivo .env creado")
    print("⚠️  IMPORTANTE: Edita .env con tu token real de GitHub")
    return False

def show_token_instructions():
    """Muestra instrucciones para obtener el token."""
    
    print("\n🔑 INSTRUCCIONES PARA OBTENER TOKEN DE GITHUB")
    print("=" * 50)
    print("1. Ve a: https://github.com/settings/tokens")
    print("2. Haz clic en 'Generate new token (classic)'")
    print("3. Nombre: 'Evaluador Rúbricas'")
    print("4. Selecciona estos permisos:")
    print("   ✅ repo (Full control of private repositories)")
    print("   ✅ read:user (Read user profile data)")
    print("5. Haz clic en 'Generate token'")
    print("6. Copia el token (empieza con 'ghp_')")
    print("7. Edita tu archivo .env y reemplaza 'tu_token_aqui'")

def test_configuration():
    """Prueba la configuración usando el módulo de configuración."""
    
    print("\n🧪 PROBANDO CONFIGURACIÓN...")
    
    try:
        from src.config import Config
        
        if not Config.validate_config():
            print("❌ Configuración incompleta")
            return False
        
        print("✅ Configuración válida")
        print(f"   GitHub Token: {Config.GITHUB_TOKEN[:10] if Config.GITHUB_TOKEN else 'No configurado'}...")
        print(f"   LLM Provider: {Config.LLM_PROVIDER}")
        print(f"   LLM API Key: {Config.LLM_API_KEY[:10] if Config.LLM_API_KEY else 'No configurado'}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal."""
    
    print("🔧 CONFIGURADOR DEL SISTEMA DE EVALUACIÓN")
    print("=" * 50)
    
    # Crear archivo .env
    env_created = create_env_file()
    
    if not env_created:
        show_token_instructions()
        print("\n💡 Después de configurar tu token, ejecuta:")
        print("   python config_simple.py")
        return
    
    # Probar configuración
    if test_configuration():
        print("\n🎉 ¡CONFIGURACIÓN COMPLETADA!")
        print("✅ Puedes usar la aplicación:")
        print("   python app.py")
        print("   python demo_agentes.py")
    else:
        print("\n⚠️  Configuración incompleta")
        show_token_instructions()

if __name__ == "__main__":
    main()
