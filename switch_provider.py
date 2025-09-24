#!/usr/bin/env python3
"""
Script para cambiar fácilmente entre proveedores de LLM
Mantiene la compatibilidad con ambos sistemas
"""

import os
import sys
from pathlib import Path

def switch_to_ollama():
    """Cambia la configuración a Ollama."""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ Archivo .env no encontrado")
        return False
    
    # Leer archivo actual
    with open(env_file, 'r') as f:
        lines = f.readlines()
    
    # Actualizar líneas
    updated_lines = []
    for line in lines:
        if line.startswith("LLM_PROVIDER="):
            updated_lines.append("LLM_PROVIDER=ollama\n")
            print("✅ Cambiado a Ollama")
        else:
            updated_lines.append(line)
    
    # Escribir archivo actualizado
    with open(env_file, 'w') as f:
        f.writelines(updated_lines)
    
    print("🤖 Configuración actualizada para Ollama")
    print("💡 Sin límites de rate, completamente privado")
    return True

def switch_to_github():
    """Cambia la configuración a GitHub Models."""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ Archivo .env no encontrado")
        return False
    
    # Leer archivo actual
    with open(env_file, 'r') as f:
        lines = f.readlines()
    
    # Actualizar líneas
    updated_lines = []
    for line in lines:
        if line.startswith("LLM_PROVIDER="):
            updated_lines.append("LLM_PROVIDER=github\n")
            print("✅ Cambiado a GitHub Models")
        else:
            updated_lines.append(line)
    
    # Escribir archivo actualizado
    with open(env_file, 'w') as f:
        f.writelines(updated_lines)
    
    print("🌐 Configuración actualizada para GitHub Models")
    print("⚠️ Puede tener límites de rate")
    return True

def show_current_config():
    """Muestra la configuración actual."""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ Archivo .env no encontrado")
        return
    
    with open(env_file, 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    provider = "No configurado"
    
    for line in lines:
        if line.startswith("LLM_PROVIDER="):
            provider = line.split('=')[1].strip('"')
            break
    
    print(f"📋 Proveedor actual: {provider}")
    
    if provider == "ollama":
        print("🤖 Usando Ollama Local")
        print("✅ Sin límites de rate")
        print("✅ Completamente privado")
        print("✅ Sin costos de API")
    elif provider == "github":
        print("🌐 Usando GitHub Models")
        print("⚠️ Puede tener límites de rate")
        print("⚠️ Requiere conexión a internet")
        print("💰 Puede tener costos asociados")

def main():
    """Función principal."""
    print("🔄 CAMBIADOR DE PROVEEDORES DE LLM")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("Uso: python switch_provider.py [ollama|github|status]")
        print()
        print("Comandos disponibles:")
        print("  ollama  - Cambiar a Ollama local")
        print("  github  - Cambiar a GitHub Models")
        print("  status  - Mostrar configuración actual")
        return
    
    command = sys.argv[1].lower()
    
    if command == "ollama":
        switch_to_ollama()
    elif command == "github":
        switch_to_github()
    elif command == "status":
        show_current_config()
    else:
        print(f"❌ Comando desconocido: {command}")
        print("Comandos válidos: ollama, github, status")

if __name__ == "__main__":
    main()
