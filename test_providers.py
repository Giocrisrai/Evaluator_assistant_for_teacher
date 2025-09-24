#!/usr/bin/env python3
"""
Script para probar ambos proveedores de LLM
Verifica que GitHub Models y Ollama funcionen correctamente
"""

import os
import sys
from dotenv import load_dotenv

# Agregar src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config import Config

def test_github_models():
    """Prueba GitHub Models."""
    print("🧪 PROBANDO GITHUB MODELS...")
    
    try:
        import openai
        
        client = openai.OpenAI(
            base_url=Config.LLM_PROVIDERS["github"]["base_url"],
            api_key=Config.GITHUB_TOKEN
        )
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un evaluador de código."},
                {"role": "user", "content": "Responde solo: 'GitHub Models funcionando'"}
            ],
            max_tokens=50,
            temperature=0.1
        )
        
        result = response.choices[0].message.content.strip()
        print(f"✅ GitHub Models: {result}")
        return True
        
    except Exception as e:
        print(f"❌ GitHub Models Error: {e}")
        return False

def test_ollama():
    """Prueba Ollama."""
    print("🧪 PROBANDO OLLAMA...")
    
    try:
        import requests
        
        payload = {
            "model": "llama3:latest",
            "prompt": "Responde solo: 'Ollama funcionando'",
            "stream": False,
            "options": {
                "temperature": 0.1,
                "num_predict": 50
            }
        }
        
        response = requests.post(
            f"{Config.LLM_PROVIDERS['ollama']['base_url']}/api/generate",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()["response"].strip()
            print(f"✅ Ollama: {result}")
            return True
        else:
            print(f"❌ Ollama Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Ollama Error: {e}")
        return False

def main():
    """Función principal."""
    print("🔧 PROBADOR DE PROVEEDORES DE LLM")
    print("=" * 50)
    
    # Cargar configuración
    load_dotenv()
    
    print(f"📋 Proveedor actual: {Config.LLM_PROVIDER}")
    print(f"🔑 GitHub Token: {'✅ Configurado' if Config.GITHUB_TOKEN else '❌ Faltante'}")
    print(f"🔑 LLM API Key: {'✅ Configurado' if Config.LLM_API_KEY else '❌ Faltante'}")
    
    print("\n" + "="*50)
    
    # Probar ambos proveedores
    github_ok = test_github_models()
    print()
    ollama_ok = test_ollama()
    
    print("\n" + "="*50)
    print("📊 RESULTADOS:")
    print(f"GitHub Models: {'✅ Funcionando' if github_ok else '❌ Error'}")
    print(f"Ollama: {'✅ Funcionando' if ollama_ok else '❌ Error'}")
    
    if github_ok and ollama_ok:
        print("\n🎉 ¡Ambos proveedores funcionan correctamente!")
        print("💡 Puedes cambiar entre ellos modificando LLM_PROVIDER en .env")
    elif github_ok:
        print("\n⚠️ Solo GitHub Models funciona")
        print("💡 Asegúrate de que Ollama esté ejecutándose")
    elif ollama_ok:
        print("\n⚠️ Solo Ollama funciona")
        print("💡 Revisa tu token de GitHub")
    else:
        print("\n❌ Ningún proveedor funciona")
        print("💡 Revisa tu configuración")

if __name__ == "__main__":
    main()
