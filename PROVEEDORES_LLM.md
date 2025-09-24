# 🤖 Proveedores de LLM - Guía Completa

El sistema soporta múltiples proveedores de modelos de lenguaje para máxima flexibilidad.

## 🌟 Proveedores Disponibles

### 1. 🤖 Ollama (Local) - **RECOMENDADO**
- **Ventajas**: Sin límites de rate, completamente privado, sin costos
- **Modelos**: llama3:latest, codellama:latest, gpt-oss:latest
- **Configuración**: `LLM_PROVIDER=ollama`

### 2. 🌐 GitHub Models
- **Ventajas**: Modelos avanzados, fácil configuración
- **Limitaciones**: Límites de rate (150 requests/día)
- **Modelos**: gpt-4o-mini, gpt-3.5-turbo
- **Configuración**: `LLM_PROVIDER=github`

### 3. 🟢 Google Gemini
- **Ventajas**: Modelos rápidos
- **Limitaciones**: 60 requests/minuto
- **Modelos**: gemini-pro
- **Configuración**: `LLM_PROVIDER=gemini`

## 🔧 Configuración Rápida

### Para Ollama (Recomendado)
```bash
# En tu archivo .env
LLM_PROVIDER=ollama
GITHUB_TOKEN=tu_token_aqui
```

### Para GitHub Models
```bash
# En tu archivo .env
LLM_PROVIDER=github
GITHUB_TOKEN=tu_token_aqui
LLM_API_KEY=tu_token_aqui
```

## 🔄 Cambiar Entre Proveedores

### Método 1: Script Automático
```bash
# Cambiar a Ollama
python switch_provider.py ollama

# Cambiar a GitHub Models
python switch_provider.py github

# Ver configuración actual
python switch_provider.py status
```

### Método 2: Manual
Edita tu archivo `.env` y cambia la línea:
```
LLM_PROVIDER=ollama    # o github, o gemini
```

## 🧪 Probar Configuración

```bash
# Probar ambos proveedores
python test_providers.py

# Validar configuración actual
python -c "from src.config import Config; Config.validate_config()"
```

## 📊 Comparación de Proveedores

| Característica      | Ollama       | GitHub Models            | Gemini                   |
| ------------------- | ------------ | ------------------------ | ------------------------ |
| **Límites de Rate** | ❌ Ninguno    | ⚠️ 150/día                | ⚠️ 60/min                 |
| **Privacidad**      | ✅ 100% Local | ❌ En la nube             | ❌ En la nube             |
| **Costo**           | ✅ Gratis     | ⚠️ Límites                | ⚠️ Límites                |
| **Velocidad**       | ⚠️ Variable   | ✅ Rápido                 | ✅ Rápido                 |
| **Modelos**         | ⚠️ Limitados  | ✅ Avanzados              | ✅ Buenos                 |
| **Recomendado**     | ✅ **SÍ**     | ⚠️ Solo si no hay límites | ⚠️ Solo si no hay límites |

## 🚀 Uso Recomendado

### Para Evaluaciones Intensivas
```bash
# Usar Ollama para evitar límites
python switch_provider.py ollama
python app.py --repo https://github.com/estudiante/repo.git --student "Estudiante"
```

### Para Evaluaciones Rápidas (si no hay límites)
```bash
# Usar GitHub Models para velocidad
python switch_provider.py github
python app.py --repo https://github.com/estudiante/repo.git --student "Estudiante"
```

## 🔧 Solución de Problemas

### Error 429 (Rate Limit)
```bash
# Solución: Cambiar a Ollama
python switch_provider.py ollama
```

### Ollama No Responde
```bash
# Verificar que Ollama esté ejecutándose
ollama serve

# Verificar modelos instalados
ollama list

# Instalar modelo si es necesario
ollama pull llama3:latest
```

### GitHub Token Inválido
```bash
# Regenerar token en: https://github.com/settings/tokens
# Actualizar .env con el nuevo token
```

## 📝 Notas Importantes

1. **Ollama es la mejor opción** para uso intensivo
2. **GitHub Models es bueno** para pruebas rápidas
3. **Siempre mantén ambos configurados** para flexibilidad
4. **El sistema detecta automáticamente** qué proveedor usar
5. **Los agentes inteligentes** funcionan con ambos proveedores

## 🎯 Ejemplo Completo

```bash
# 1. Configurar Ollama
python switch_provider.py ollama

# 2. Verificar configuración
python switch_provider.py status

# 3. Probar ambos proveedores
python test_providers.py

# 4. Evaluar repositorio
python app.py --repo https://github.com/estudiante/repo.git --student "Estudiante"

# 5. Si hay límites, cambiar a GitHub Models
python switch_provider.py github
python app.py --repo https://github.com/estudiante/repo.git --student "Estudiante"
```

¡El sistema está diseñado para ser flexible y funcionar con cualquier proveedor! 🚀
