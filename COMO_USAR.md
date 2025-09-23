# 🎯 Cómo Usar tu Sistema de Evaluación con Agentes Inteligentes

## ✅ Estado Actual: ¡SISTEMA FUNCIONANDO!

Tu sistema está completamente configurado y listo para usar. Aquí tienes todo lo que necesitas saber:

## 🚀 Comandos Principales

### **1. Verificar que todo funciona**
```bash
python start.py
```

### **2. Ver demo de capacidades**
```bash
python main.py demo
```

### **3. Evaluar un repositorio individual**
```bash
python app.py --repo https://github.com/usuario/proyecto --student "Nombre Estudiante"
```

### **4. Evaluar una clase completa**
```bash
python app.py --class examples/estudiantes_ejemplo.csv
```

### **5. Ver configuración**
```bash
python config_simple.py
```

## 📊 Lo que ya funciona

✅ **Configuración completa** - Token de GitHub configurado  
✅ **Dependencias instaladas** - Todas las librerías necesarias  
✅ **Agentes inteligentes** - Análisis, recomendaciones y monitoreo  
✅ **Evaluación automática** - Rúbricas Kedro funcionando  
✅ **Reportes generados** - HTML y JSON automáticamente  
✅ **Sistema modular** - Fácil de mantener y extender  

## 🎯 Ejemplos que ya funcionan

### Evaluación Individual
```bash
python app.py --repo https://github.com/kedro-org/kedro-starters --student "Ana García"
```
**Resultado**: Nota 5.8/7.0 con insights y recomendaciones

### Demo Completo
```bash
python main.py demo
```
**Resultado**: Demuestra todas las capacidades del sistema

## 📁 Resultados Generados

Después de cada evaluación encontrarás en `evaluaciones_agentes/`:
- **Archivos JSON**: Datos completos de la evaluación
- **Reportes HTML**: Reportes visuales navegables
- **Insights inteligentes**: Análisis generado por IA
- **Recomendaciones**: Planes personalizados
- **Alertas**: Monitoreo automático

## 🤖 Agentes Inteligentes Activos

### 🔍 Agente de Análisis
- Identifica tendencias y patrones
- Genera insights sobre el código
- Analiza problemas comunes

### 💡 Agente de Recomendaciones
- Crea planes personalizados
- Sugiere recursos específicos
- Adapta al nivel del estudiante

### 🚨 Agente de Monitoreo
- Detecta alertas críticas
- Monitorea progreso
- Identifica posibles problemas

## 🎓 Para Evaluar Estudiantes

### 1. Crear archivo CSV de estudiantes
```csv
nombre,email,repo_url,nivel
Juan Pérez,juan@universidad.cl,https://github.com/usuario/proyecto1,intermedio
María García,maria@universidad.cl,https://github.com/usuario/proyecto2,avanzado
```

### 2. Ejecutar evaluación masiva
```bash
python app.py --class estudiantes.csv
```

### 3. Revisar resultados
Los resultados se guardan automáticamente en `evaluaciones_agentes/`

## 🔧 Personalización Disponible

### Cambiar Rúbricas
Edita `src/rubrica_evaluator.py` para agregar tus propias rúbricas

### Cambiar Proveedor de IA
Edita `.env`:
```bash
LLM_PROVIDER=gemini  # Cambiar a Gemini si quieres
```

### Agregar Nuevos Criterios
Modifica las rúbricas en el código para agregar criterios específicos

## 📈 Reportes Generados

### Formato HTML
- Reportes visuales navegables
- Gráficos y estadísticas
- Fácil de compartir

### Formato JSON
- Datos completos
- Para análisis posterior
- Integración con otros sistemas

## 🎉 ¡Listo para Usar!

Tu sistema está completamente funcional y listo para evaluar repositorios de estudiantes con:

- ✅ **Evaluación automática** con rúbricas
- ✅ **Agentes inteligentes** para análisis avanzado
- ✅ **Reportes profesionales** en HTML y JSON
- ✅ **Recomendaciones personalizadas** por estudiante
- ✅ **Monitoreo automático** de alertas
- ✅ **Sistema modular** fácil de mantener

## 🚀 Próximos Pasos

1. **Prueba con tus propios repositorios**
2. **Crea rúbricas personalizadas** para tus cursos
3. **Evalúa clases completas** usando archivos CSV
4. **Revisa los reportes** generados automáticamente
5. **Personaliza los agentes** según tus necesidades

**¡Tu sistema de evaluación con IA está listo para usar!** 🎓🤖
