# 📋 Instrucciones de Uso - Sistema de Evaluación con Agentes Inteligentes

## 🚀 Inicio Rápido (5 minutos)

### 1. Configuración Inicial
```bash
# Clonar y entrar al directorio
git clone <tu-repositorio>
cd rubrica-evaluator

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o .venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar tokens
python config_simple.py
```

### 2. Obtener Token de GitHub
1. Ve a: https://github.com/settings/tokens
2. "Generate new token (classic)"
3. Nombre: "Evaluador Rúbricas"
4. Permisos: ✅ `repo`, ✅ `read:user`
5. Copia el token y pégalo en `.env`

### 3. Verificar Configuración
```bash
python validate.py
```

### 4. ¡Listo para usar!
```bash
python start.py  # Guía interactiva
```

## 🎯 Comandos Principales

### Configuración
```bash
python config_simple.py    # Configurar sistema
python validate.py         # Verificar configuración
python start.py           # Guía de inicio rápido
```

### Uso Principal
```bash
python main.py app        # Aplicación principal
python main.py demo       # Demo de capacidades
python main.py test       # Pruebas del sistema
python main.py config     # Configuración
```

### Evaluación
```bash
# Evaluación individual
python main.py app --repo https://github.com/usuario/proyecto

# Con estudiante
python main.py app --repo https://github.com/usuario/proyecto --student "Juan Pérez"

# Evaluación masiva
python main.py app --class examples/estudiantes_ejemplo.csv

# Modo interactivo
python main.py app
```

## 📊 Estructura del Proyecto

```
rubrica-evaluator/
├── main.py                 # 🎯 Punto de entrada principal
├── start.py               # 🚀 Guía de inicio rápido
├── app.py                 # 📱 Aplicación principal
├── src/                   # 📦 Módulos del sistema
│   ├── agents_manager.py  # 🤖 Coordinador de agentes
│   ├── config.py          # ⚙️ Configuración
│   ├── rubrica_evaluator.py # 📊 Evaluador principal
│   ├── demo.py           # 🎬 Demostración
│   └── agents/           # 🧠 Agentes inteligentes
├── examples/             # 📚 Ejemplos y plantillas
└── evaluaciones_agentes/ # 📁 Resultados con IA
```

## 🤖 Agentes Inteligentes

### 🔍 Agente de Análisis
- Identifica tendencias y patrones
- Genera insights sobre rendimiento
- Analiza problemas comunes

### 💡 Agente de Recomendaciones  
- Crea planes personalizados
- Sugiere recursos específicos
- Adapta al nivel del estudiante

### 🚨 Agente de Monitoreo
- Detecta alertas críticas
- Monitorea progreso
- Identifica posibles plagios

## 📈 Reportes Generados

### Formatos
- **HTML**: Reportes visuales navegables
- **JSON**: Datos completos para análisis
- **CSV**: Resúmenes para hojas de cálculo

### Contenido
- Evaluación detallada por criterio
- Insights inteligentes de IA
- Recomendaciones personalizadas
- Alertas y monitoreo
- Análisis de tendencias

## 🛠️ Solución de Problemas

### Error: "Configuración incompleta"
```bash
python config_simple.py  # Reconfigurar
```

### Error: "ModuleNotFoundError"
```bash
pip install -r requirements.txt  # Reinstalar
```

### Error: "Rate limit exceeded"
```bash
# Esperar 1 hora o verificar token
python validate.py
```

## 📚 Ejemplos Prácticos

### Ejemplo 1: Evaluación Simple
```bash
python main.py app --repo https://github.com/kedro-org/kedro-starters
```

### Ejemplo 2: Con Estudiante
```bash
python main.py app --repo https://github.com/usuario/proyecto --student "Ana García"
```

### Ejemplo 3: Clase Completa
```bash
# Crear archivo CSV con estudiantes
# Ver: examples/estudiantes_ejemplo.csv

python main.py app --class examples/estudiantes_ejemplo.csv
```

### Ejemplo 4: Demo
```bash
python main.py demo
```

## 🔧 Personalización

### Crear Nueva Rúbrica
Edita `src/rubrica_evaluator.py` y agrega tu función:

```python
def create_mi_rubrica():
    return {
        "nombre": "Mi Rúbrica",
        "descripcion": "Para mi curso específico",
        "criterios": [
            {
                "criterio": "Criterio 1",
                "peso": 0.5,  # 50%
                "niveles": {
                    7.0: "Excelente",
                    6.0: "Bueno",
                    # ...
                }
            }
        ]
    }
```

### Cambiar Proveedor de IA
Edita `.env`:
```bash
LLM_PROVIDER=gemini  # o github
LLM_API_KEY=tu_api_key
```

## 🎉 ¡Listo!

Tu sistema está configurado y listo para evaluar repositorios de estudiantes con IA.

**Comandos más usados:**
- `python start.py` - Guía interactiva
- `python main.py demo` - Ver demo
- `python main.py app` - Evaluar repositorios

**Soporte:**
- Revisa `README.md` para documentación completa
- Ejecuta `python validate.py` para diagnosticar problemas
- Usa `python start.py` para guía paso a paso
