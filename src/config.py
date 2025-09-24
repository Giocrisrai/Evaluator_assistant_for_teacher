# config.py - Archivo de configuración
import os
from typing import Dict, List
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    """Configuración del sistema de evaluación."""
    
    # Proveedores de IA Disponibles
    LLM_PROVIDERS = {
        "github": {
            "base_url": "https://models.inference.ai.azure.com",
            "models": ["gpt-4o-mini", "gpt-3.5-turbo"],
            "free_tier": "Sí - Límites generosos"
        },
        "gemini": {
            "models": ["gemini-pro"],
            "free_tier": "Sí - 60 requests/minuto"
        },
        "ollama": {
            "base_url": "http://localhost:11434",
            "models": ["llama3:latest", "codellama:latest", "gpt-oss:latest"],
            "free_tier": "Sí - Sin límites (local)"
        }
    }
    
    # Variables de entorno
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    LLM_API_KEY = os.getenv("LLM_API_KEY") 
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
    
    # Configuraciones por defecto
    DEFAULT_OUTPUT_DIR = "./evaluaciones"
    DEFAULT_TIMEOUT = 300  # 5 minutos
    
    @classmethod
    def validate_config(cls):
        """Valida que la configuración esté completa."""
        missing = []
        
        if not cls.GITHUB_TOKEN:
            missing.append("GITHUB_TOKEN")
        if not cls.LLM_API_KEY and cls.LLM_PROVIDER not in ["ollama"]:
            missing.append("LLM_API_KEY")
        
        # Validar que Ollama esté funcionando si es el proveedor seleccionado
        if cls.LLM_PROVIDER == "ollama":
            import requests
            try:
                response = requests.get(f"{cls.LLM_PROVIDERS['ollama']['base_url']}/api/tags", timeout=5)
                if response.status_code == 200:
                    print("✅ Ollama está funcionando correctamente")
                else:
                    print("❌ Ollama no está respondiendo correctamente")
                    missing.append("OLLAMA_SERVER")
            except Exception as e:
                print(f"❌ No se puede conectar a Ollama: {e}")
                print("💡 Asegúrate de que Ollama esté ejecutándose con: ollama serve")
                missing.append("OLLAMA_SERVER")
            
        if missing:
            print("❌ Configuración incompleta. Variables faltantes:")
            for var in missing:
                print(f"   - {var}")
            print("\nCrea un archivo .env con:")
            print("GITHUB_TOKEN=tu_token_aqui")
            print("LLM_API_KEY=tu_api_key_aqui")  
            print("LLM_PROVIDER=ollama")
            return False
        
        print("✅ Configuración válida")
        return True
