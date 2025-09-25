"""
Sistema Principal de Evaluación para Proyectos Kedro ML
Curso: MLY0100 - Machine Learning
Evaluación Parcial 1 - Proyecto Práctico (70% de la nota)
"""

import os
import json
import logging
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import yaml

from github import Github, GithubException
from examples.rubrica_kedro import create_kedro_ml_rubrica, OLLAMA_CONFIG

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('evaluaciones_kedro.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class EvaluacionKedro:
    """Estructura de datos para la evaluación de un proyecto Kedro."""
    
    # Información del estudiante
    estudiante_nombre: str
    estudiante_pareja: Optional[str]
    repositorio_url: str
    fecha_evaluacion: datetime
    
    # Evaluación general
    nota_final: float
    porcentaje_total: float
    estado: str  # APROBADO, REPROBADO, PENDIENTE
    
    # Evaluación por criterios
    criterios_evaluados: List[Dict[str, Any]]
    
    # Bonificaciones y penalizaciones
    bonificaciones_aplicadas: Dict[str, float]
    penalizaciones_aplicadas: Dict[str, float]
    
    # Análisis del código
    metricas_codigo: Dict[str, Any]
    
    # Metadatos
    tiempo_evaluacion: float
    version_evaluador: str = "1.0.0"
    
    # Retroalimentación
    resumen_general: str
    fortalezas: List[str]
    areas_mejora: List[str]
    recomendaciones: List[str]
    
    def to_dict(self) -> Dict:
        """Convierte la evaluación a diccionario."""
        data = asdict(self)
        data['fecha_evaluacion'] = self.fecha_evaluacion.isoformat()
        return data
    
    def calcular_nota_escala_chilena(self) -> float:
        """Convierte el porcentaje a nota en escala chilena (1.0 - 7.0)."""
        escala = {
            100: 7.0, 90: 6.5, 80: 6.0, 70: 5.5,
            60: 5.0, 50: 4.5, 40: 4.0, 30: 3.5,
            20: 3.0, 10: 2.0, 0: 1.0
        }
        
        # Encontrar la nota correspondiente
        for porcentaje, nota in sorted(escala.items(), reverse=True):
            if self.porcentaje_total >= porcentaje:
                return nota
        return 1.0


class KedroProjectAnalyzer:
    """Analizador específico para proyectos Kedro."""
    
    def __init__(self, github_token: str, ollama_client=None):
        """
        Inicializa el analizador.
        
        Args:
            github_token: Token de acceso a GitHub
            ollama_client: Cliente de Ollama para análisis con IA
        """
        self.github = Github(github_token)
        self.ollama_client = ollama_client
        self.rubrica = create_kedro_ml_rubrica()
        
    def analizar_estructura_kedro(self, repo) -> Dict[str, Any]:
        """
        Analiza la estructura específica de un proyecto Kedro.
        
        Returns:
            Diccionario con el análisis de la estructura
        """
        estructura = {
            "tiene_estructura_kedro": False,
            "directorios_principales": [],
            "archivos_configuracion": [],
            "pipelines_encontrados": [],
            "datasets_configurados": 0,
            "notebooks_crisp_dm": [],
            "errores": []
        }
        
        try:
            # Verificar directorios principales de Kedro
            directorios_requeridos = ['conf', 'data', 'src', 'notebooks']
            for dir_name in directorios_requeridos:
                try:
                    repo.get_contents(dir_name)
                    estructura["directorios_principales"].append(dir_name)
                except:
                    estructura["errores"].append(f"Falta directorio: {dir_name}")
            
            # Verificar archivos de configuración
            archivos_config = [
                'conf/base/catalog.yml',
                'conf/base/parameters.yml',
                'pyproject.toml',
                'requirements.txt'
            ]
            
            for archivo in archivos_config:
                try:
                    contenido = repo.get_contents(archivo)
                    estructura["archivos_configuracion"].append(archivo)
                    
                    # Analizar catalog.yml para contar datasets
                    if archivo == 'conf/base/catalog.yml':
                        catalog_content = contenido.decoded_content.decode()
                        estructura["datasets_configurados"] = self._contar_datasets(catalog_content)
                except:
                    estructura["errores"].append(f"Falta archivo: {archivo}")
            
            # Buscar pipelines
            try:
                src_contents = repo.get_contents("src")
                for item in src_contents:
                    if item.type == "dir":
                        pipelines_path = f"src/{item.name}/pipelines"
                        try:
                            pipelines = repo.get_contents(pipelines_path)
                            for pipeline in pipelines:
                                if pipeline.type == "dir":
                                    estructura["pipelines_encontrados"].append(pipeline.name)
                        except:
                            pass
            except:
                estructura["errores"].append("No se pudo acceder a src/pipelines")
            
            # Verificar notebooks CRISP-DM
            notebooks_esperados = [
                '01_business_understanding',
                '02_data_understanding', 
                '03_data_preparation'
            ]
            
            try:
                notebooks = repo.get_contents("notebooks")
                for notebook in notebooks:
                    if notebook.name.endswith('.ipynb'):
                        for fase in notebooks_esperados:
                            if fase in notebook.name.lower():
                                estructura["notebooks_crisp_dm"].append(notebook.name)
                                break
            except:
                estructura["errores"].append("No se encontraron notebooks")
            
            # Determinar si tiene estructura Kedro válida
            estructura["tiene_estructura_kedro"] = (
                len(estructura["directorios_principales"]) >= 3 and
                len(estructura["archivos_configuracion"]) >= 2
            )
            
        except Exception as e:
            logger.error(f"Error analizando estructura: {str(e)}")
            estructura["errores"].append(str(e))
        
        return estructura
    
    def _contar_datasets(self, catalog_content: str) -> int:
        """Cuenta el número de datasets en el catálogo."""
        try:
            catalog = yaml.safe_load(catalog_content)
            if catalog:
                # Filtrar solo datasets válidos (no templates ni versioned)
                datasets = [k for k in catalog.keys() 
                           if not k.startswith('_') and isinstance(catalog[k], dict)]
                return len(datasets)
        except:
            pass
        return 0
    
    def verificar_reproducibilidad(self, repo) -> Dict[str, bool]:
        """
        Verifica la reproducibilidad del proyecto.
        
        Returns:
            Diccionario con verificaciones de reproducibilidad
        """
        checks = {
            "tiene_requirements": False,
            "tiene_readme": False,
            "tiene_gitignore": False,
            "tiene_env_example": False,
            "tiene_tests": False,
            "usa_parametros": False,
            "tiene_logging": False
        }
        
        archivos_verificar = {
            "requirements.txt": "tiene_requirements",
            "README.md": "tiene_readme",
            ".gitignore": "tiene_gitignore",
            ".env.example": "tiene_env_example",
            "conf/base/parameters.yml": "usa_parametros",
            "conf/base/logging.yml": "tiene_logging"
        }
        
        for archivo, key in archivos_verificar.items():
            try:
                repo.get_contents(archivo)
                checks[key] = True
            except:
                pass
        
        # Verificar si hay tests
        try:
            tests = repo.get_contents("tests")
            if tests:
                checks["tiene_tests"] = True
        except:
            try:
                src_tests = repo.get_contents("src/tests")
                if src_tests:
                    checks["tiene_tests"] = True
            except:
                pass
        
        return checks
    
    def analizar_calidad_codigo(self, repo) -> Dict[str, Any]:
        """
        Analiza la calidad del código del proyecto.
        
        Returns:
            Métricas de calidad del código
        """
        metricas = {
            "total_archivos_python": 0,
            "lineas_codigo": 0,
            "tiene_docstrings": False,
            "usa_type_hints": False,
            "complejidad_promedio": 0,
            "archivos_analizados": []
        }
        
        def analizar_archivo_python(contenido: str, nombre: str):
            """Analiza un archivo Python individual."""
            lineas = contenido.split('\n')
            metricas["lineas_codigo"] += len(lineas)
            
            # Verificar docstrings
            if '"""' in contenido or "'''" in contenido:
                metricas["tiene_docstrings"] = True
            
            # Verificar type hints
            if '->' in contenido or ': ' in contenido:
                metricas["usa_type_hints"] = True
            
            metricas["archivos_analizados"].append(nombre)
        
        def explorar_directorio(path=""):
            """Explora recursivamente el repositorio."""
            try:
                contents = repo.get_contents(path)
                if not isinstance(contents, list):
                    contents = [contents]
                
                for content in contents:
                    if content.type == "dir" and content.name not in ['.git', '__pycache__', '.venv', 'venv']:
                        explorar_directorio(content.path)
                    elif content.name.endswith('.py'):
                        metricas["total_archivos_python"] += 1
                        try:
                            file_content = content.decoded_content.decode('utf-8')
                            analizar_archivo_python(file_content, content.path)
                        except:
                            pass
            except:
                pass
        
        # Analizar principalmente src/ y pipelines/
        for directorio in ['src', 'pipelines']:
            explorar_directorio(directorio)
        
        return metricas


class KedroEvaluator:
    """Evaluador principal para proyectos Kedro ML."""
    
    def __init__(self, github_token: str, ollama_client=None):
        """
        Inicializa el evaluador.
        
        Args:
            github_token: Token de GitHub
            ollama_client: Cliente de Ollama (opcional)
        """
        self.analyzer = KedroProjectAnalyzer(github_token, ollama_client)
        self.rubrica = create_kedro_ml_rubrica()
        self.github = Github(github_token)
        
    def evaluar_proyecto(self, 
                         repo_url: str,
                         estudiante_nombre: str,
                         estudiante_pareja: Optional[str] = None,
                         aplicar_bonificaciones: bool = True) -> EvaluacionKedro:
        """
        Evalúa completamente un proyecto Kedro.
        
        Args:
            repo_url: URL del repositorio
            estudiante_nombre: Nombre del estudiante
            estudiante_pareja: Nombre de la pareja (opcional)
            aplicar_bonificaciones: Si aplicar bonificaciones/penalizaciones
            
        Returns:
            Objeto EvaluacionKedro con los resultados
        """
        inicio_evaluacion = time.time()
        logger.info(f"Iniciando evaluación de {repo_url} para {estudiante_nombre}")
        
        # Obtener repositorio
        try:
            repo_name = repo_url.replace("https://github.com/", "").replace(".git", "")
            repo = self.github.get_repo(repo_name)
        except GithubException as e:
            logger.error(f"Error accediendo al repositorio: {e}")
            return self._crear_evaluacion_error(repo_url, estudiante_nombre, str(e))
        
        # Analizar estructura
        estructura = self.analyzer.analizar_estructura_kedro(repo)
        reproducibilidad = self.analyzer.verificar_reproducibilidad(repo)
        calidad_codigo = self.analyzer.analizar_calidad_codigo(repo)
        
        # Evaluar cada criterio
        criterios_evaluados = []
        puntuacion_total = 0
        
        for criterio in self.rubrica["criterios"]:
            resultado_criterio = self._evaluar_criterio(
                criterio, estructura, reproducibilidad, calidad_codigo, repo
            )
            criterios_evaluados.append(resultado_criterio)
            puntuacion_total += resultado_criterio["puntuacion_ponderada"]
        
        # Aplicar bonificaciones y penalizaciones
        bonificaciones = {}
        penalizaciones = {}
        
        if aplicar_bonificaciones:
            bonificaciones = self._calcular_bonificaciones(estructura, reproducibilidad)
            penalizaciones = self._calcular_penalizaciones(estructura)
            
            # Ajustar puntuación
            puntuacion_total += sum(bonificaciones.values())
            puntuacion_total -= sum(penalizaciones.values())
        
        # Calcular nota final
        porcentaje_final = max(0, min(100, puntuacion_total))
        nota_final = self._porcentaje_a_nota_chilena(porcentaje_final)
        
        # Generar retroalimentación
        fortalezas = self._identificar_fortalezas(criterios_evaluados)
        areas_mejora = self._identificar_areas_mejora(criterios_evaluados)
        recomendaciones = self._generar_recomendaciones(areas_mejora)
        
        # Crear evaluación
        evaluacion = EvaluacionKedro(
            estudiante_nombre=estudiante_nombre,
            estudiante_pareja=estudiante_pareja,
            repositorio_url=repo_url,
            fecha_evaluacion=datetime.now(),
            nota_final=nota_final,
            porcentaje_total=porcentaje_final,
            estado="APROBADO" if nota_final >= 4.0 else "REPROBADO",
            criterios_evaluados=criterios_evaluados,
            bonificaciones_aplicadas=bonificaciones,
            penalizaciones_aplicadas=penalizaciones,
            metricas_codigo=calidad_codigo,
            tiempo_evaluacion=time.time() - inicio_evaluacion,
            resumen_general=self._generar_resumen(nota_final, porcentaje_final),
            fortalezas=fortalezas,
            areas_mejora=areas_mejora,
            recomendaciones=recomendaciones
        )
        
        logger.info(f"Evaluación completada: Nota {nota_final} ({porcentaje_final}%)")
        return evaluacion
    
    def _evaluar_criterio(self, criterio: Dict, estructura: Dict, 
                         reproducibilidad: Dict, calidad: Dict, repo) -> Dict:
        """Evalúa un criterio individual."""
        nombre = criterio["nombre"]
        puntuacion = 0
        evidencias = []
        retroalimentacion = ""
        
        # Lógica específica por criterio
        if "Estructura y Configuración" in nombre:
            if estructura["tiene_estructura_kedro"]:
                puntuacion = 80
                if len(estructura["errores"]) == 0:
                    puntuacion = 100
                elif len(estructura["errores"]) <= 2:
                    puntuacion = 80
            else:
                puntuacion = 40 if len(estructura["directorios_principales"]) >= 2 else 20
            
            evidencias = estructura["directorios_principales"] + estructura["archivos_configuracion"]
            retroalimentacion = f"Estructura {'completa' if puntuacion >= 80 else 'incompleta'}. "
            if estructura["errores"]:
                retroalimentacion += f"Problemas encontrados: {', '.join(estructura["errores"][:3])}"
        
        elif "Catálogo de Datos" in nombre:
            num_datasets = estructura["datasets_configurados"]
            if num_datasets >= 3:
                puntuacion = 100 if num_datasets > 3 else 80
            elif num_datasets == 2:
                puntuacion = 60
            elif num_datasets == 1:
                puntuacion = 40
            else:
                puntuacion = 20
            
            evidencias = [f"{num_datasets} datasets configurados"]
            retroalimentacion = f"Se encontraron {num_datasets} datasets. "
            if num_datasets < 3:
                retroalimentacion += f"Se requieren mínimo 3 datasets."
        
        elif "Pipelines" in nombre:
            num_pipelines = len(estructura["pipelines_encontrados"])
            if num_pipelines >= 3:
                puntuacion = 100
            elif num_pipelines == 2:
                puntuacion = 80
            elif num_pipelines == 1:
                puntuacion = 60
            else:
                puntuacion = 20
            
            evidencias = estructura["pipelines_encontrados"]
            retroalimentacion = f"Pipelines encontrados: {', '.join(estructura['pipelines_encontrados']) if estructura['pipelines_encontrados'] else 'ninguno'}"
        
        elif "Documentación" in nombre:
            if reproducibilidad["tiene_readme"]:
                puntuacion = 60
                if len(estructura["notebooks_crisp_dm"]) >= 3:
                    puntuacion = 100
                elif len(estructura["notebooks_crisp_dm"]) >= 2:
                    puntuacion = 80
            else:
                puntuacion = 20
            
            evidencias = estructura["notebooks_crisp_dm"]
            retroalimentacion = f"Notebooks CRISP-DM: {len(estructura['notebooks_crisp_dm'])}/3"
        
        elif "Reproducibilidad" in nombre:
            checks_pasados = sum(1 for v in reproducibilidad.values() if v)
            total_checks = len(reproducibilidad)
            puntuacion = int((checks_pasados / total_checks) * 100)
            
            evidencias = [k for k, v in reproducibilidad.items() if v]
            retroalimentacion = f"Verificaciones de reproducibilidad: {checks_pasados}/{total_checks}"
        
        else:
            # Evaluación genérica basada en estructura
            if estructura["tiene_estructura_kedro"]:
                puntuacion = 60
            else:
                puntuacion = 40
            retroalimentacion = "Evaluación basada en estructura general"
        
        # Calcular puntuación ponderada
        puntuacion_ponderada = puntuacion * criterio["ponderacion"]
        
        return {
            "nombre": nombre,
            "ponderacion": criterio["ponderacion"],
            "puntuacion": puntuacion,
            "puntuacion_ponderada": puntuacion_ponderada,
            "nota_criterio": self._porcentaje_a_nota_chilena(puntuacion),
            "evidencias": evidencias,
            "retroalimentacion": retroalimentacion
        }
    
    def _porcentaje_a_nota_chilena(self, porcentaje: float) -> float:
        """Convierte porcentaje a nota chilena."""
        escala = [
            (100, 7.0), (90, 6.5), (80, 6.0), (70, 5.5),
            (60, 5.0), (50, 4.5), (40, 4.0), (30, 3.5),
            (20, 3.0), (10, 2.0), (0, 1.0)
        ]
        
        for umbral, nota in escala:
            if porcentaje >= umbral:
                return nota
        return 1.0
    
    def _calcular_bonificaciones(self, estructura: Dict, reproducibilidad: Dict) -> Dict[str, float]:
        """Calcula bonificaciones según extras implementados."""
        bonificaciones = {}
        
        # Verificar Kedro Viz
        if "kedro-viz" in str(estructura.get("archivos_configuracion", [])):
            bonificaciones["kedro_viz"] = 3.0  # +0.3 en nota final
        
        # Verificar tests
        if reproducibilidad.get("tiene_tests"):
            bonificaciones["tests_unitarios"] = 5.0  # +0.5 en nota final
        
        return bonificaciones
    
    def _calcular_penalizaciones(self, estructura: Dict) -> Dict[str, float]:
        """Calcula penalizaciones."""
        penalizaciones = {}
        
        # Penalización por falta de datasets
        datasets_faltantes = max(0, 3 - estructura.get("datasets_configurados", 0))
        if datasets_faltantes > 0:
            penalizaciones["datasets_faltantes"] = datasets_faltantes * 10  # -1.0 por dataset
        
        # Penalización si no tiene estructura Kedro
        if not estructura.get("tiene_estructura_kedro"):
            penalizaciones["sin_estructura_kedro"] = 20  # -2.0 en nota
        
        return penalizaciones
    
    def _identificar_fortalezas(self, criterios: List[Dict]) -> List[str]:
        """Identifica las fortalezas del proyecto."""
        fortalezas = []
        for criterio in criterios:
            if criterio["puntuacion"] >= 80:
                fortalezas.append(f"✓ {criterio['nombre']}: Excelente implementación")
        return fortalezas
    
    def _identificar_areas_mejora(self, criterios: List[Dict]) -> List[str]:
        """Identifica áreas de mejora."""
        areas = []
        for criterio in criterios:
            if criterio["puntuacion"] < 60:
                areas.append(f"⚠ {criterio['nombre']}: Necesita mejoras significativas")
        return areas
    
    def _generar_recomendaciones(self, areas_mejora: List[str]) -> List[str]:
        """Genera recomendaciones específicas."""
        recomendaciones = []
        
        for area in areas_mejora:
            if "Estructura" in area:
                recomendaciones.append("📁 Revisar la estructura de directorios de Kedro")
            elif "Catálogo" in area:
                recomendaciones.append("📊 Agregar más datasets al catálogo (mínimo 3)")
            elif "Pipeline" in area:
                recomendaciones.append("🔧 Implementar pipelines para cada fase CRISP-DM")
            elif "Documentación" in area:
                recomendaciones.append("📝 Completar notebooks y documentación")
            elif "Reproducibilidad" in area:
                recomendaciones.append("🔄 Agregar requirements.txt y mejorar reproducibilidad")
        
        return recomendaciones
    
    def _generar_resumen(self, nota: float, porcentaje: float) -> str:
        """Genera un resumen de la evaluación."""
        if nota >= 6.0:
            nivel = "Excelente"
        elif nota >= 5.0:
            nivel = "Bueno"
        elif nota >= 4.0:
            nivel = "Suficiente"
        else:
            nivel = "Insuficiente"
        
        return (f"Proyecto evaluado con nota {nota:.1f} ({porcentaje:.0f}%). "
                f"Nivel de desempeño: {nivel}. "
                f"{'APROBADO' if nota >= 4.0 else 'REPROBADO'}.")
    
    def _crear_evaluacion_error(self, repo_url: str, estudiante: str, error: str) -> EvaluacionKedro:
        """Crea una evaluación de error cuando no se puede acceder al repositorio."""
        return EvaluacionKedro(
            estudiante_nombre=estudiante,
            estudiante_pareja=None,
            repositorio_url=repo_url,
            fecha_evaluacion=datetime.now(),
            nota_final=1.0,
            porcentaje_total=0,
            estado="ERROR",
            criterios_evaluados=[],
            bonificaciones_aplicadas={},
            penalizaciones_aplicadas={},
            metricas_codigo={},
            tiempo_evaluacion=0,
            resumen_general=f"Error al evaluar: {error}",
            fortalezas=[],
            areas_mejora=["No se pudo acceder al repositorio"],
            recomendaciones=["Verificar que el repositorio sea público y la URL sea correcta"]
        )
    
    def generar_reporte(self, evaluacion: EvaluacionKedro, formato: str = "json") -> str:
        """
        Genera un reporte de la evaluación en el formato especificado.
        
        Args:
            evaluacion: Objeto de evaluación
            formato: Formato de salida (json, html, markdown)
            
        Returns:
            Reporte en el formato especificado
        """
        if formato == "json":
            return json.dumps(evaluacion.to_dict(), indent=2, ensure_ascii=False)
        
        elif formato == "markdown":
            return self._generar_reporte_markdown(evaluacion)
        
        elif formato == "html":
            return self._generar_reporte_html(evaluacion)
        
        else:
            raise ValueError(f"Formato no soportado: {formato}")
    
    def _generar_reporte_markdown(self, evaluacion: EvaluacionKedro) -> str:
        """Genera reporte en formato Markdown."""
        md = f"""# 📊 Reporte de Evaluación - Proyecto Kedro ML

## 👤 Información del Estudiante
- **Nombre**: {evaluacion.estudiante_nombre}
- **Pareja**: {evaluacion.estudiante_pareja or 'Individual'}
- **Repositorio**: {evaluacion.repositorio_url}
- **Fecha**: {evaluacion.fecha_evaluacion.strftime('%d/%m/%Y %H:%M')}

## 📈 Resultados Generales
- **Nota Final**: **{evaluacion.nota_final:.1f}** / 7.0
- **Porcentaje**: {evaluacion.porcentaje_total:.0f}%
- **Estado**: **{evaluacion.estado}**

## 📋 Evaluación por Criterios

| Criterio | Peso | Puntuación | Nota |
|----------|------|------------|------|
"""
        for criterio in evaluacion.criterios_evaluados:
            md += f"| {criterio['nombre']} | {criterio['ponderacion']*100:.0f}% | "
            md += f"{criterio['puntuacion']:.0f}% | {criterio['nota_criterio']:.1f} |\n"
        
        md += f"""
## ✅ Fortalezas
"""
        for fortaleza in evaluacion.fortalezas:
            md += f"- {fortaleza}\n"
        
        md += f"""
## ⚠️ Áreas de Mejora
"""
        for area in evaluacion.areas_mejora:
            md += f"- {area}\n"
        
        md += f"""
## 💡 Recomendaciones
"""
        for rec in evaluacion.recomendaciones:
            md += f"- {rec}\n"
        
        if evaluacion.bonificaciones_aplicadas:
            md += f"""
## 🎁 Bonificaciones Aplicadas
"""
            for bonus, valor in evaluacion.bonificaciones_aplicadas.items():
                md += f"- {bonus}: +{valor/10:.1f} puntos\n"
        
        if evaluacion.penalizaciones_aplicadas:
            md += f"""
## ⛔ Penalizaciones Aplicadas
"""
            for penal, valor in evaluacion.penalizaciones_aplicadas.items():
                md += f"- {penal}: -{valor/10:.1f} puntos\n"
        
        md += f"""
## 📊 Métricas del Código
- Archivos Python: {evaluacion.metricas_codigo.get('total_archivos_python', 0)}
- Líneas de código: {evaluacion.metricas_codigo.get('lineas_codigo', 0)}
- Tiene docstrings: {'✅' if evaluacion.metricas_codigo.get('tiene_docstrings') else '❌'}
- Usa type hints: {'✅' if evaluacion.metricas_codigo.get('usa_type_hints') else '❌'}

---
*Evaluación generada automáticamente en {evaluacion.tiempo_evaluacion:.1f} segundos*
"""
        return md
    
    def _generar_reporte_html(self, evaluacion: EvaluacionKedro) -> str:
        """Genera reporte en formato HTML."""
        estado_color = "green" if evaluacion.estado == "APROBADO" else "red"
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Evaluación Kedro - {evaluacion.estudiante_nombre}</title>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 900px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        .info-box {{ background: #f9f9f9; padding: 15px; border-radius: 5px; margin: 10px 0; }}
        .nota-final {{ font-size: 48px; font-weight: bold; color: {estado_color}; text-align: center; }}
        .estado {{ font-size: 24px; text-align: center; padding: 10px; background: {"#d4edda" if evaluacion.estado == "APROBADO" else "#f8d7da"}; border-radius: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 10px; border: 1px solid #ddd; text-align: left; }}
        th {{ background: #4CAF50; color: white; }}
        tr:nth-child(even) {{ background: #f9f9f9; }}
        .fortaleza {{ color: green; }}
        .mejora {{ color: orange; }}
        .metric {{ display: inline-block; margin: 10px; padding: 10px; background: #e7f3ff; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Evaluación Proyecto Kedro ML</h1>
        
        <div class="info-box">
            <h2>Información del Estudiante</h2>
            <p><strong>Nombre:</strong> {evaluacion.estudiante_nombre}</p>
            <p><strong>Pareja:</strong> {evaluacion.estudiante_pareja or 'Individual'}</p>
            <p><strong>Repositorio:</strong> <a href="{evaluacion.repositorio_url}">{evaluacion.repositorio_url}</a></p>
            <p><strong>Fecha:</strong> {evaluacion.fecha_evaluacion.strftime('%d/%m/%Y %H:%M')}</p>
        </div>
        
        <div class="nota-final">{evaluacion.nota_final:.1f} / 7.0</div>
        <div class="estado">{evaluacion.estado}</div>
        
        <h2>Evaluación por Criterios</h2>
        <table>
            <tr>
                <th>Criterio</th>
                <th>Ponderación</th>
                <th>Puntuación</th>
                <th>Nota</th>
                <th>Retroalimentación</th>
            </tr>
"""
        for criterio in evaluacion.criterios_evaluados:
            html += f"""
            <tr>
                <td>{criterio['nombre']}</td>
                <td>{criterio['ponderacion']*100:.0f}%</td>
                <td>{criterio['puntuacion']:.0f}%</td>
                <td>{criterio['nota_criterio']:.1f}</td>
                <td>{criterio['retroalimentacion']}</td>
            </tr>
"""
        
        html += f"""
        </table>
        
        <h2>✅ Fortalezas</h2>
        <ul>
"""
        for fortaleza in evaluacion.fortalezas:
            html += f"            <li class='fortaleza'>{fortaleza}</li>\n"
        
        html += """        </ul>
        
        <h2>⚠️ Áreas de Mejora</h2>
        <ul>
"""
        for area in evaluacion.areas_mejora:
            html += f"            <li class='mejora'>{area}</li>\n"
        
        html += f"""        </ul>
        
        <h2>Métricas del Código</h2>
        <div>
            <span class="metric">📁 Archivos Python: {evaluacion.metricas_codigo.get('total_archivos_python', 0)}</span>
            <span class="metric">📝 Líneas de código: {evaluacion.metricas_codigo.get('lineas_codigo', 0)}</span>
            <span class="metric">📖 Docstrings: {'✅' if evaluacion.metricas_codigo.get('tiene_docstrings') else '❌'}</span>
            <span class="metric">🔍 Type Hints: {'✅' if evaluacion.metricas_codigo.get('usa_type_hints') else '❌'}</span>
        </div>
        
        <hr>
        <p style="text-align: center; color: #999;">
            Evaluación generada automáticamente en {evaluacion.tiempo_evaluacion:.1f} segundos<br>
            Sistema de Evaluación Kedro ML v1.0
        </p>
    </div>
</body>
</html>"""
        
        return html


# Función principal para pruebas
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Uso: python kedro_evaluator.py <github_token> <repo_url> [estudiante_nombre]")
        sys.exit(1)
    
    github_token = sys.argv[1]
    repo_url = sys.argv[2]
    estudiante = sys.argv[3] if len(sys.argv) > 3 else "Estudiante de Prueba"
    
    # Crear evaluador
    evaluador = KedroEvaluator(github_token)
    
    # Evaluar proyecto
    print(f"Evaluando proyecto: {repo_url}")
    evaluacion = evaluador.evaluar_proyecto(repo_url, estudiante)
    
    # Generar reportes
    print("\n" + "="*60)
    print(evaluador.generar_reporte(evaluacion, "markdown"))
    
    # Guardar reporte HTML
    with open(f"evaluacion_{estudiante.replace(' ', '_')}.html", "w", encoding="utf-8") as f:
        f.write(evaluador.generar_reporte(evaluacion, "html"))
    
    print(f"\n✅ Evaluación completada. Reporte HTML guardado.")
