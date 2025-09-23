# 🤖 Sistema de Evaluación Automática con Rúbricas y Agentes Inteligentes

Sistema modular y profesional para evaluar automáticamente repositorios GitHub de estudiantes usando rúbricas personalizables y agentes de IA especializados.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![GitHub](https://img.shields.io/badge/github-api-green.svg)
![AI](https://img.shields.io/badge/ai-powered-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🚀 Características Principales

### ✨ Evaluación Automática
- **Análisis de repositorios GitHub** con acceso completo al código fuente
- **Rúbricas personalizables** para diferentes tipos de proyectos (ML, Python, React, etc.)
- **Sistema de notas chileno** (1.0 - 7.0) con retroalimentación detallada
- **Evaluación masiva** de clases completas desde archivos CSV

### 🤖 Agentes Inteligentes
- **Agente de Análisis**: Identifica tendencias, patrones y áreas de mejora
- **Agente de Recomendaciones**: Genera planes personalizados de aprendizaje
- **Agente de Monitoreo**: Detecta alertas, plagio y problemas críticos

### 🔧 Integración con IA
- **GitHub Models** (Recomendado) - Gratuito con límites generosos
- **Google Gemini** - Alternativa gratuita
- **Análisis de código** con comprensión semántica avanzada
- **Retroalimentación contextual** basada en el dominio del proyecto

## 📁 Estructura del Proyecto

```
rubrica-evaluator/
├── main.py                    # Punto de entrada principal
├── app.py                     # Aplicación principal
├── src/                       # Módulos del sistema
│   ├── agents_manager.py      # Coordinador de agentes
│   ├── demo.py               # Demostración del sistema
│   ├── config.py             # Configuración
│   ├── rubrica_evaluator.py  # Evaluador principal
│   └── agents/               # Agentes inteligentes
│       ├── analysis_agent.py
│       ├── recommendation_agent.py
│       └── monitoring_agent.py
├── examples/                 # Ejemplos y plantillas
│   ├── rubrica_python.py     # Rúbrica para proyectos Python
│   ├── rubrica_react.py      # Rúbrica para proyectos React
│   └── estudiantes_ejemplo.csv
├── tests/                    # Tests unitarios
└── evaluaciones_agentes/     # Resultados con IA
```

## 🛠️ Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/rubrica-evaluator.git
cd rubrica-evaluator
```

### 2. Crear entorno virtual
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate     # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar con tu configuración
nano .env
```

**Contenido del archivo `.env`:**
```bash
# Token de GitHub (OBLIGATORIO)
GITHUB_TOKEN=ghp_tu_token_de_github_aqui

# Configuración de IA
LLM_PROVIDER=github
LLM_API_KEY=ghp_tu_token_de_github_aqui

# URLs de GitHub Models
OPENAI_BASE_URL=https://models.inference.ai.azure.com
```

### 5. Obtener token de GitHub
1. Ve a: [GitHub Settings > Personal Access Tokens](https://github.com/settings/tokens)
2. Click en "Generate new token (classic)"
3. Nombre: "Evaluador Rúbricas"
4. Selecciona permisos:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `read:user` (Read user profile data)
5. Click "Generate token"
6. Copia el token y pégalo en tu archivo `.env`

### 6. Verificar configuración
```bash
python validate.py
```

## 🎯 Uso del Sistema

### Comandos Principales

```bash
# Configuración inicial
python main.py config

# Aplicación principal
python main.py app

# Demo de capacidades
python main.py demo

# Pruebas del sistema
python main.py test
```

### Evaluación Individual

```bash
# Evaluar un repositorio
python main.py app --repo https://github.com/usuario/proyecto

# Con información del estudiante
python main.py app --repo https://github.com/usuario/proyecto --student "Juan Pérez"

# Modo interactivo
python main.py app
```

### Evaluación Masiva

```bash
# Crear archivo CSV de estudiantes
# Ver: examples/estudiantes_ejemplo.csv

# Evaluar clase completa
python main.py app --class examples/estudiantes_ejemplo.csv
```

### Formato del archivo CSV
```csv
nombre,email,repo_url,nivel
Juan Pérez,juan@universidad.cl,https://github.com/usuario/proyecto1,intermedio
María García,maria@universidad.cl,https://github.com/usuario/proyecto2,avanzado
```

## 🤖 Agentes Inteligentes

### Agente de Análisis
- **Función**: Identifica tendencias y patrones en las evaluaciones
- **Capacidades**:
  - Análisis de tendencias de clase
  - Identificación de problemas comunes
  - Generación de insights sobre el rendimiento

### Agente de Recomendaciones
- **Función**: Crea planes personalizados de mejora
- **Capacidades**:
  - Recomendaciones específicas por estudiante
  - Planes de aprendizaje adaptados al nivel
  - Recursos y ejercicios sugeridos

### Agente de Monitoreo
- **Función**: Detecta alertas y problemas críticos
- **Capacidades**:
  - Alertas de rendimiento bajo
  - Detección de posibles plagios
  - Monitoreo de progreso individual y grupal

## 📊 Rúbricas Incluidas

### Rúbrica Kedro (Machine Learning)
- **Estructura del Proyecto** (15%)
- **Análisis de Datos** (15%)
- **Modelado y Métricas** (20%)
- **Validación y Testing** (15%)
- **Documentación** (10%)
- **Código Limpio** (10%)
- **Gestión de Dependencias** (5%)
- **Configuración y Deployment** (5%)
- **Innovación y Creatividad** (3%)
- **Presentación Final** (2%)

### Rúbrica Python (Desarrollo General)
- **Estructura y Organización** (20%)
- **Calidad del Código** (20%)
- **Documentación** (15%)
- **Testing** (15%)
- **Funcionalidad** (15%)
- **Buenas Prácticas** (10%)
- **Innovación** (5%)

### Rúbrica React (Frontend)
- **Componentes** (25%)
- **Estado y Props** (20%)
- **Estilos y UI** (15%)
- **Funcionalidad** (15%)
- **Performance** (10%)
- **Testing** (10%)
- **Documentación** (5%)

## 📈 Reportes Generados

### Formatos de Salida
- **HTML**: Reportes visuales navegables con gráficos
- **JSON**: Datos completos para análisis posterior
- **CSV**: Resúmenes para hojas de cálculo

### Contenido de Reportes
- **Evaluación detallada** por criterio
- **Insights inteligentes** generados por IA
- **Recomendaciones personalizadas** por estudiante
- **Alertas y monitoreo** automático
- **Análisis de tendencias** de clase
- **Comparativas** entre estudiantes

## 🔧 Configuración Avanzada

### Proveedores de IA Disponibles

#### GitHub Models (Recomendado)
```bash
LLM_PROVIDER=github
LLM_API_KEY=tu_github_token
```
- ✅ Gratuito con límites generosos
- ✅ Modelos: gpt-4o-mini, gpt-3.5-turbo
- ✅ Integración nativa con GitHub

#### Google Gemini
```bash
LLM_PROVIDER=gemini
LLM_API_KEY=tu_gemini_api_key
```
- ✅ 60 requests por minuto
- ✅ Modelo: gemini-pro
- ⚠️ Requiere API key de Google

### Personalización de Rúbricas

Crear una nueva rúbrica:
```python
def create_mi_rubrica():
    return {
        "nombre": "Mi Rúbrica Personalizada",
        "descripcion": "Rúbrica para mi curso específico",
        "criterios": [
            {
                "criterio": "Criterio 1",
                "descripcion": "Descripción del criterio",
                "peso": 0.3,  # 30%
                "niveles": {
                    7.0: "Excelente implementación",
                    6.0: "Buena implementación",
                    5.0: "Implementación aceptable",
                    4.0: "Implementación básica",
                    3.0: "Implementación deficiente",
                    2.0: "Implementación muy deficiente",
                    1.0: "Sin implementación"
                }
            }
        ]
    }
```

## 🧪 Testing y Validación

### Ejecutar Tests
```bash
# Tests unitarios
python -m pytest tests/

# Validación completa
python validate.py

# Prueba rápida del sistema
python main.py test
```

### Verificar Configuración
```bash
python validate.py
```

Salida esperada:
```
✅ GitHub Token: Configurado
✅ LLM Provider: github
✅ LLM API Key: Configurado
✅ Conexión GitHub: OK (Rate limit: 4999/5000)
✅ LLM Connection: OK
```

## 🚨 Solución de Problemas

### Error: "GitHub Token: ❌ Faltante"
```bash
# Verificar archivo .env
cat .env

# Asegurar que el token esté configurado
GITHUB_TOKEN=ghp_tu_token_aqui
```

### Error: "ModuleNotFoundError"
```bash
# Reinstalar dependencias
pip install -r requirements.txt

# Verificar entorno virtual
source .venv/bin/activate
```

### Error: "Rate limit exceeded"
```bash
# Verificar límites de GitHub
python validate.py

# Esperar reset del rate limit (1 hora)
```

### Error: "JSON serialization"
```bash
# Limpiar archivos de resultados anteriores
rm -rf evaluaciones_agentes/*

# Reintentar evaluación
```

## 📚 Ejemplos de Uso

### Ejemplo 1: Evaluación Simple
```bash
python main.py app --repo https://github.com/kedro-org/kedro-starters
```

### Ejemplo 2: Evaluación con Estudiante
```bash
python main.py app --repo https://github.com/usuario/proyecto --student "Ana García"
```

### Ejemplo 3: Evaluación de Clase
```bash
python main.py app --class examples/estudiantes_ejemplo.csv
```

### Ejemplo 4: Demo Interactivo
```bash
python main.py demo
```

## 🤝 Contribución

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 🆘 Soporte

- **Issues**: [GitHub Issues](https://github.com/tu-usuario/rubrica-evaluator/issues)
- **Documentación**: [Wiki del proyecto](https://github.com/tu-usuario/rubrica-evaluator/wiki)
- **Email**: tu-email@universidad.cl

## 🎉 Agradecimientos

- [GitHub Models](https://github.com/marketplace/models) por el acceso gratuito a IA
- [Kedro](https://kedro.org/) por el framework de ML
- [PyGithub](https://pygithub.readthedocs.io/) por la integración con GitHub API

---

**¿Listo para evaluar?** 🚀

```bash
python main.py config  # Configuración inicial
python main.py demo    # Ver demo
python main.py app     # Comenzar a evaluar
```