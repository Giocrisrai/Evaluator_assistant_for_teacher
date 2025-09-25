# 🎓 Sistema de Evaluación Automática para Proyectos Kedro ML

[![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)](https://www.python.org/)
[![Kedro](https://img.shields.io/badge/kedro-v0.18+-green.svg)](https://kedro.org/)
[![GitHub](https://img.shields.io/badge/github-api-orange.svg)](https://docs.github.com/en/rest)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Sistema profesional para evaluar automáticamente proyectos de Machine Learning implementados con el framework Kedro, siguiendo la metodología CRISP-DM y utilizando agentes inteligentes con Ollama.

## 📋 Características Principales

### ✅ Evaluación Automática Completa
- **10 criterios de evaluación** con ponderación del 10% cada uno
- **Escala de notas chilena** (1.0 - 7.0)
- **Análisis profundo** de estructura, código y documentación
- **Evaluación masiva** de múltiples repositorios en paralelo

### 🤖 Inteligencia Artificial Local
- **Ollama** para análisis con LLMs locales
- **Sin costos de API** - completamente local
- **Privacidad garantizada** - los datos no salen de tu servidor

### 📊 Reportes Detallados
- **Reportes individuales** en HTML, Markdown y JSON
- **Estadísticas del curso** con distribución de notas
- **Exportación** a Excel y CSV
- **Dashboard interactivo** (opcional)

## 🚀 Instalación Rápida

### Opción 1: Instalación Automática
```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/rubrica-evaluator.git
cd rubrica-evaluator

# Configuración rápida completa
make quick-start
```

### Opción 2: Instalación Manual
```bash
# 1. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar GitHub token
export GITHUB_TOKEN="ghp_tuTokenAqui"

# 4. Instalar Ollama (opcional pero recomendado)
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama2
```

## 📁 Estructura del Proyecto

```
rubrica-evaluator/
├── src/
│   ├── kedro_evaluator.py      # Evaluador principal para Kedro
│   └── rubrica_evaluator.py    # Sistema base de evaluación
├── examples/
│   └── rubrica_kedro.py         # Rúbrica específica para proyectos Kedro
├── scripts/
│   ├── evaluate_batch.py        # Evaluación masiva
│   └── validate_installation.py # Validador de instalación
├── data/
│   └── estudiantes_kedro.csv   # Lista de estudiantes
├── evaluaciones/                # Resultados de evaluaciones (generado)
├── requirements.txt             # Dependencias Python
├── Makefile                     # Comandos simplificados
└── README.md                    # Este archivo
```

## 💻 Uso del Sistema

### Evaluación Individual
```bash
# Con Make
make evaluate-single REPO=https://github.com/estudiante/proyecto STUDENT="Juan Pérez"

# O directamente con Python
python src/kedro_evaluator.py $GITHUB_TOKEN https://github.com/estudiante/proyecto "Juan Pérez"
```

### Evaluación Masiva (Recomendado)
```bash
# Evaluar todos los estudiantes del CSV
make evaluate-all

# O con parámetros personalizados
python scripts/evaluate_batch.py \
    --csv data/estudiantes_kedro.csv \
    --output evaluaciones \
    --parallel 3
```

### Generar Reportes
```bash
# Generar reportes consolidados
make report

# Ver estadísticas rápidas
make stats
```

## 📝 Formato del CSV de Estudiantes

El archivo `data/estudiantes_kedro.csv` debe tener el siguiente formato:

```csv
nombre,pareja,repositorio
Juan Pérez,María González,https://github.com/juanperez/kedro-ml-project
Ana Rodríguez,Carlos López,https://github.com/anarodriguez/proyecto-kedro
Pedro Martínez,,https://github.com/pmartinez/ml-kedro-parcial1
```

## 📊 Criterios de Evaluación

El sistema evalúa los siguientes 10 criterios, cada uno con 10% de ponderación:

1. **Estructura y Configuración del Proyecto Kedro**
2. **Implementación del Catálogo de Datos** (mínimo 3 datasets)
3. **Desarrollo de Nodos y Funciones**
4. **Construcción de Pipelines**
5. **Análisis Exploratorio de Datos (EDA)**
6. **Limpieza y Tratamiento de Datos**
7. **Transformación y Feature Engineering**
8. **Identificación de Targets para ML**
9. **Documentación y Notebooks**
10. **Reproducibilidad y Mejores Prácticas**

### Bonificaciones (Puntos Extra)
- **Kedro Viz**: +0.3
- **Tests Unitarios**: +0.5
- **CI/CD**: +0.3
- **Docker**: +0.2
- **Dashboard**: +0.5

### Penalizaciones
- **Entrega tardía**: -0.5 por día
- **Falta de dataset**: -1.0 por cada uno bajo 3
- **Proyecto no ejecuta**: -2.0

## 🔧 Configuración Avanzada

### Variables de Entorno
```bash
# Obligatorias
export GITHUB_TOKEN="ghp_tuTokenAqui"

# Opcionales
export LLM_PROVIDER="ollama"  # o "github", "gemini"
export OUTPUT_DIRECTORY="./evaluaciones"
export EVALUATION_TIMEOUT=300
```

### Personalizar la Rúbrica
Edita `examples/rubrica_kedro.py` para ajustar:
- Ponderaciones de criterios
- Niveles de evaluación
- Archivos a revisar
- Bonificaciones y penalizaciones

## 🐳 Uso con Docker

```bash
# Construir imagen
docker build -t kedro-evaluator .

# Ejecutar evaluación
docker run -it --rm \
    -v $(pwd)/data:/app/data \
    -v $(pwd)/evaluaciones:/app/evaluaciones \
    -e GITHUB_TOKEN=$GITHUB_TOKEN \
    kedro-evaluator
```

## 🧪 Testing y Validación

```bash
# Validar instalación
make validate

# Ejecutar tests
make test

# Tests con cobertura
make dev-test-coverage
```

## 📈 Ejemplos de Output

### Evaluación Individual
```
✅ Juan Pérez: Nota 5.8 - APROBADO
   - Estructura: 80%
   - Catálogo: 100%
   - Pipelines: 60%
   - Documentación: 80%
   ...
```

### Estadísticas del Curso
```
Total evaluados: 25
Aprobados: 18 (72%)
Nota promedio: 5.2
Nota máxima: 6.8
Nota mínima: 3.2
```

## 🛠️ Comandos Útiles (Makefile)

| Comando | Descripción |
|---------|-------------|
| `make help` | Muestra todos los comandos disponibles |
| `make setup` | Configuración inicial completa |
| `make evaluate-all` | Evalúa todos los estudiantes |
| `make stats` | Muestra estadísticas rápidas |
| `make clean` | Limpia archivos temporales |
| `make backup` | Crea backup de evaluaciones |

## 🐛 Solución de Problemas

### Ollama no responde
```bash
# Verificar que el servicio esté activo
ollama serve

# Verificar modelos disponibles
ollama list
```

### GitHub API Rate Limit
- Usar token con más permisos
- Implementar cache: `--use-cache`
- Reducir paralelismo

### Proyecto no se puede clonar
- Verificar que el repositorio sea público
- Comprobar URL correcta
- Revisar permisos del token

## 📚 Documentación de la Asignatura

- **Curso**: MLY0100 - Machine Learning
- **Evaluación**: Parcial 1 (40% de la asignatura)
- **Componentes**:
  - Prueba Teórica: 30%
  - Proyecto Práctico con Kedro: 70% (evaluado por este sistema)
- **Modalidad**: Parejas
- **Duración**: 4 semanas
- **Metodología**: CRISP-DM (3 primeras fases)

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍🏫 Créditos

Desarrollado para el curso de Machine Learning (MLY0100) para facilitar la evaluación justa, consistente y eficiente de proyectos estudiantiles.

## 📞 Soporte

Para soporte y consultas:
- 📧 Email: giocrisrai.godoy@profesor.duoc.cl
- 💬 Issues: [GitHub Issues](https://github.com/tu-usuario/rubrica-evaluator/issues)

---

*Sistema de Evaluación Automática v1.0 - Facilitando la evaluación de proyectos de Machine Learning*
