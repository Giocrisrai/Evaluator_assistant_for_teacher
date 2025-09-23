import os
import json
import yaml
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import requests
import base64
from pathlib import Path
import openai
from github import Github
import google.generativeai as genai

@dataclass
class CriterioRubrica:
    """Representa un criterio de evaluación en la rúbrica."""
    nombre: str
    descripcion: str
    ponderacion: float  # Porcentaje (0.0 - 1.0)
    niveles: Dict[int, str]  # {porcentaje: descripción}
    archivos_revisar: List[str] = None  # Archivos específicos a revisar
    comandos_verificacion: List[str] = None  # Comandos para verificar

@dataclass
class ResultadoCriterio:
    """Resultado de evaluación de un criterio."""
    criterio: str
    puntuacion: int  # 0-100
    nota: float  # Nota final del criterio
    retroalimentacion: str
    evidencias: List[str]  # Links o paths a evidencias encontradas
    sugerencias: List[str]

@dataclass
class EvaluacionCompleta:
    """Resultado completo de la evaluación."""
    repositorio: str
    fecha_evaluacion: str
    criterios: List[ResultadoCriterio]
    nota_final: float
    resumen_general: str
    tiempo_evaluacion: float

class GitHubAnalyzer:
    """Analizador de repositorios de GitHub."""
    
    def __init__(self, github_token: str):
        from github import Auth
        self.github = Github(auth=Auth.Token(github_token))
        
    def get_repository_structure(self, repo_url: str) -> Dict[str, Any]:
        """Obtiene la estructura completa del repositorio."""
        repo_name = repo_url.replace("https://github.com/", "").replace(".git", "")
        repo = self.github.get_repo(repo_name)
        
        structure = {
            "name": repo.name,
            "description": repo.description,
            "files": {},
            "directories": set(),
            "readme": None,
            "requirements": None,
            "has_gitignore": False
        }
        
        # Obtener contenido recursivamente
        def get_contents(path=""):
            try:
                contents = repo.get_contents(path)
                if not isinstance(contents, list):
                    contents = [contents]
                    
                for content in contents:
                    if content.type == "dir":
                        structure["directories"].add(content.path)
                        get_contents(content.path)
                    else:
                        structure["files"][content.path] = {
                            "size": content.size,
                            "url": content.download_url
                        }
                        
                        # Archivos especiales
                        if content.name.lower() == "readme.md":
                            structure["readme"] = content.download_url
                        elif content.name.lower() in ["requirements.txt", "pyproject.toml", "environment.yml"]:
                            structure["requirements"] = content.download_url
                        elif content.name.lower() == ".gitignore":
                            structure["has_gitignore"] = True
                            
            except Exception as e:
                print(f"Error accediendo a {path}: {e}")
                
        get_contents()
        return structure

    def get_file_content(self, repo_url: str, file_path: str) -> Optional[str]:
        """Obtiene el contenido de un archivo específico."""
        try:
            repo_name = repo_url.replace("https://github.com/", "").replace(".git", "")
            repo = self.github.get_repo(repo_name)
            file_content = repo.get_contents(file_path)
            return base64.b64decode(file_content.content).decode('utf-8')
        except Exception as e:
            print(f"Error obteniendo archivo {file_path}: {e}")
            return None

class LLMEvaluator:
    """Evaluador usando diferentes modelos de LLM."""
    
    def __init__(self, provider: str = "github", api_key: str = None):
        self.provider = provider
        self.api_key = api_key
        self.setup_client()
        
    def setup_client(self):
        """Configura el cliente según el proveedor."""
        if self.provider == "github":
            # GitHub Models
            self.client = openai.OpenAI(
                base_url="https://models.inference.ai.azure.com",
                api_key=self.api_key
            )
            self.model = "gpt-4o-mini"
            
        elif self.provider == "gemini":
            # Google Gemini
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            
        elif self.provider == "huggingface":
            # Hugging Face (usar su API)
            self.hf_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
            self.headers = {"Authorization": f"Bearer {self.api_key}"}
            
    def evaluate_criterion(self, criterio: CriterioRubrica, evidencias: Dict[str, Any]) -> ResultadoCriterio:
        """Evalúa un criterio específico usando LLM."""
        
        prompt = self._build_evaluation_prompt(criterio, evidencias)
        
        try:
            if self.provider == "github":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "Eres un evaluador experto en proyectos de Machine Learning y ciencia de datos."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.1
                )
                evaluation = response.choices[0].message.content
                
            elif self.provider == "gemini":
                response = self.model.generate_content(prompt)
                evaluation = response.text
                
            return self._parse_evaluation_response(evaluation, criterio.nombre)
            
        except Exception as e:
            print(f"Error en evaluación: {e}")
            return ResultadoCriterio(
                criterio=criterio.nombre,
                puntuacion=0,
                nota=1.0,
                retroalimentacion=f"Error en evaluación: {e}",
                evidencias=[],
                sugerencias=["Revisar manualmente este criterio"]
            )
    
    def _build_evaluation_prompt(self, criterio: CriterioRubrica, evidencias: Dict[str, Any]) -> str:
        """Construye el prompt para evaluación."""
        
        prompt = f"""
EVALUACIÓN DE CRITERIO: {criterio.nombre}

DESCRIPCIÓN DEL CRITERIO:
{criterio.descripcion}

PONDERACIÓN: {criterio.ponderacion * 100}%

NIVELES DE EVALUACIÓN:
"""
        for porcentaje, descripcion in criterio.niveles.items():
            nota = 1.0 + (porcentaje / 100) * 6.0
            prompt += f"- {porcentaje}% (Nota {nota:.1f}): {descripcion}\n"

        prompt += f"""

EVIDENCIAS ENCONTRADAS EN EL REPOSITORIO:

Estructura de directorios:
{list(evidencias.get('directories', []))}

Archivos encontrados:
{list(evidencias.get('files', {}).keys())}

README presente: {evidencias.get('readme') is not None}
Requirements presente: {evidencias.get('requirements') is not None}
.gitignore presente: {evidencias.get('has_gitignore', False)}

INSTRUCCIONES:
1. Analiza las evidencias contra los criterios
2. Asigna una puntuación del 0% al 100%
3. Calcula la nota correspondiente (1.0 a 7.0)
4. Proporciona retroalimentación específica
5. Lista evidencias encontradas (paths de archivos)
6. Da sugerencias de mejora

FORMATO DE RESPUESTA (JSON):
{{
    "puntuacion": <0-100>,
    "nota": <1.0-7.0>,
    "retroalimentacion": "Explicación detallada de la evaluación...",
    "evidencias": ["path/archivo1", "path/archivo2"],
    "sugerencias": ["Sugerencia 1", "Sugerencia 2"]
}}
"""
        return prompt
    
    def _parse_evaluation_response(self, response: str, criterio_nombre: str) -> ResultadoCriterio:
        """Parsea la respuesta del LLM."""
        try:
            # Buscar JSON en la respuesta
            start = response.find('{')
            end = response.rfind('}') + 1
            json_str = response[start:end]
            
            data = json.loads(json_str)
            
            return ResultadoCriterio(
                criterio=criterio_nombre,
                puntuacion=data.get('puntuacion', 0),
                nota=data.get('nota', 1.0),
                retroalimentacion=data.get('retroalimentacion', ''),
                evidencias=data.get('evidencias', []),
                sugerencias=data.get('sugerencias', [])
            )
        except Exception as e:
            print(f"Error parseando respuesta: {e}")
            return ResultadoCriterio(
                criterio=criterio_nombre,
                puntuacion=0,
                nota=1.0,
                retroalimentacion=f"Error parseando evaluación: {response}",
                evidencias=[],
                sugerencias=[]
            )

class RubricaEvaluator:
    """Sistema principal de evaluación con rúbricas."""
    
    def __init__(self, github_token: str, llm_provider: str = "github", llm_api_key: str = None):
        self.github_analyzer = GitHubAnalyzer(github_token)
        self.llm_evaluator = LLMEvaluator(llm_provider, llm_api_key)
        
    def load_rubrica_from_dict(self, rubrica_dict: Dict[str, Any]) -> List[CriterioRubrica]:
        """Carga rúbrica desde diccionario."""
        criterios = []
        
        for criterio_data in rubrica_dict.get('criterios', []):
            criterio = CriterioRubrica(
                nombre=criterio_data['nombre'],
                descripcion=criterio_data['descripcion'],
                ponderacion=criterio_data['ponderacion'],
                niveles=criterio_data['niveles'],
                archivos_revisar=criterio_data.get('archivos_revisar'),
                comandos_verificacion=criterio_data.get('comandos_verificacion')
            )
            criterios.append(criterio)
            
        return criterios
    
    def evaluate_repository(self, repo_url: str, rubrica: List[CriterioRubrica]) -> EvaluacionCompleta:
        """Evalúa un repositorio completo según la rúbrica."""
        
        print(f"🔍 Analizando repositorio: {repo_url}")
        start_time = datetime.now()
        
        # Obtener estructura del repositorio
        estructura = self.github_analyzer.get_repository_structure(repo_url)
        
        resultados = []
        nota_total = 0.0
        
        print(f"📋 Evaluando {len(rubrica)} criterios...")
        
        for i, criterio in enumerate(rubrica, 1):
            print(f"   {i}/{len(rubrica)} - {criterio.nombre}")
            
            # Evaluar criterio
            resultado = self.llm_evaluator.evaluate_criterion(criterio, estructura)
            resultados.append(resultado)
            
            # Calcular contribución a nota final
            nota_total += resultado.nota * criterio.ponderacion
        
        end_time = datetime.now()
        tiempo_evaluacion = (end_time - start_time).total_seconds()
        
        # Generar resumen general
        resumen = self._generate_summary(resultados, nota_total)
        
        evaluacion = EvaluacionCompleta(
            repositorio=repo_url,
            fecha_evaluacion=datetime.now().isoformat(),
            criterios=resultados,
            nota_final=round(nota_total, 2),
            resumen_general=resumen,
            tiempo_evaluacion=tiempo_evaluacion
        )
        
        print(f"✅ Evaluación completada - Nota final: {nota_total:.2f}")
        return evaluacion
    
    def _generate_summary(self, resultados: List[ResultadoCriterio], nota_final: float) -> str:
        """Genera resumen general de la evaluación."""
        
        criterios_excelentes = [r for r in resultados if r.puntuacion >= 80]
        criterios_buenos = [r for r in resultados if 60 <= r.puntuacion < 80]
        criterios_mejorables = [r for r in resultados if r.puntuacion < 60]
        
        resumen = f"""
📊 RESUMEN GENERAL DE LA EVALUACIÓN

Nota Final: {nota_final:.2f}/7.0

🟢 Fortalezas ({len(criterios_excelentes)} criterios):
"""
        for c in criterios_excelentes[:3]:  # Top 3
            resumen += f"- {c.criterio}: {c.puntuacion}% - {c.retroalimentacion[:100]}...\n"
            
        if criterios_mejorables:
            resumen += f"""
🟡 Áreas de Mejora ({len(criterios_mejorables)} criterios):
"""
            for c in criterios_mejorables:
                resumen += f"- {c.criterio}: {c.puntuacion}% - {c.sugerencias[0] if c.sugerencias else 'Revisar implementación'}\n"
        
        return resumen
    
    def export_evaluation(self, evaluacion: EvaluacionCompleta, output_path: str):
        """Exporta la evaluación a diferentes formatos."""
        
        # JSON detallado
        json_path = f"{output_path}_detallado.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(evaluacion), f, indent=2, ensure_ascii=False)
        
        # Reporte HTML
        html_path = f"{output_path}_reporte.html"
        self._generate_html_report(evaluacion, html_path)
        
        # CSV resumen
        csv_path = f"{output_path}_resumen.csv"
        self._generate_csv_summary(evaluacion, csv_path)
        
        print(f"📁 Reportes exportados:")
        print(f"   - Detallado: {json_path}")
        print(f"   - HTML: {html_path}")
        print(f"   - CSV: {csv_path}")
    
    def _generate_html_report(self, evaluacion: EvaluacionCompleta, output_path: str):
        """Genera reporte HTML."""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Reporte de Evaluación</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 10px; }}
        .criterio {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
        .nota {{ font-weight: bold; font-size: 1.2em; }}
        .excelente {{ background-color: #d4edda; }}
        .bueno {{ background-color: #fff3cd; }}
        .mejorable {{ background-color: #f8d7da; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Reporte de Evaluación</h1>
        <p><strong>Repositorio:</strong> {evaluacion.repositorio}</p>
        <p><strong>Fecha:</strong> {evaluacion.fecha_evaluacion}</p>
        <p class="nota">Nota Final: {evaluacion.nota_final}/7.0</p>
    </div>
    
    <h2>📋 Evaluación por Criterios</h2>
"""
        
        for criterio in evaluacion.criterios:
            clase_css = "excelente" if criterio.puntuacion >= 80 else "bueno" if criterio.puntuacion >= 60 else "mejorable"
            
            html_content += f"""
    <div class="criterio {clase_css}">
        <h3>{criterio.criterio}</h3>
        <p class="nota">Puntuación: {criterio.puntuacion}% - Nota: {criterio.nota}/7.0</p>
        <p><strong>Retroalimentación:</strong> {criterio.retroalimentacion}</p>
        <p><strong>Evidencias:</strong> {', '.join(criterio.evidencias) if criterio.evidencias else 'No encontradas'}</p>
        <p><strong>Sugerencias:</strong></p>
        <ul>
            {''.join(f'<li>{s}</li>' for s in criterio.sugerencias)}
        </ul>
    </div>
"""
        
        html_content += f"""
    <h2>📝 Resumen General</h2>
    <pre>{evaluacion.resumen_general}</pre>
</body>
</html>
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _generate_csv_summary(self, evaluacion: EvaluacionCompleta, output_path: str):
        """Genera resumen CSV."""
        import csv
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Criterio', 'Puntuación (%)', 'Nota', 'Retroalimentación'])
            
            for criterio in evaluacion.criterios:
                writer.writerow([
                    criterio.criterio,
                    criterio.puntuacion,
                    criterio.nota,
                    criterio.retroalimentacion[:200] + "..." if len(criterio.retroalimentacion) > 200 else criterio.retroalimentacion
                ])


def create_kedro_rubrica() -> Dict[str, Any]:
    """Crea la rúbrica para proyectos Kedro ML basada en el documento."""
    
    niveles_estandar = {
        100: "Logro completo de todos los aspectos - Muy buen desempeño",
        80: "Alto desempeño con mínimas omisiones - Buen desempeño", 
        60: "Logro de elementos básicos - Desempeño aceptable",
        40: "Importantes omisiones o errores - Desempeño incipiente",
        20: "Desempeño incorrecto - Desempeño insuficiente",
        0: "No cumple requisitos mínimos - No logrado"
    }
    
    return {
        "nombre": "Evaluación Parcial 1 - Machine Learning con Kedro",
        "descripcion": "Rúbrica para evaluar proyectos de ML usando framework Kedro y metodología CRISP-DM",
        "criterios": [
            {
                "nombre": "Estructura y Configuración del Proyecto Kedro",
                "descripcion": "Proyecto Kedro correctamente estructurado con configuración completa",
                "ponderacion": 0.10,
                "niveles": niveles_estandar,
                "archivos_revisar": ["conf/base/catalog.yml", "conf/base/parameters.yml", "README.md", "requirements.txt"]
            },
            {
                "nombre": "Implementación del Catálogo de Datos", 
                "descripcion": "Configuración correcta de mínimo 3 datasets en el catálogo",
                "ponderacion": 0.10,
                "niveles": niveles_estandar,
                "archivos_revisar": ["conf/base/catalog.yml", "data/01_raw/"]
            },
            {
                "nombre": "Desarrollo de Nodos y Funciones",
                "descripcion": "Nodos modulares con funciones puras, docstrings y manejo de errores",
                "ponderacion": 0.10,
                "niveles": niveles_estandar,
                "archivos_revisar": ["src/*/pipelines/*/nodes.py"]
            },
            {
                "nombre": "Construcción de Pipelines",
                "descripcion": "Pipelines organizados por fase CRISP-DM con dependencias claras",
                "ponderacion": 0.10,
                "niveles": niveles_estandar,
                "archivos_revisar": ["src/*/pipelines/*/pipeline.py", "src/*/pipeline_registry.py"]
            },
            {
                "nombre": "Análisis Exploratorio de Datos (EDA)",
                "descripcion": "EDA exhaustivo con visualizaciones y análisis de patrones",
                "ponderacion": 0.10,
                "niveles": niveles_estandar,
                "archivos_revisar": ["notebooks/02_data_understanding.ipynb"]
            },
            {
                "nombre": "Limpieza y Tratamiento de Datos",
                "descripcion": "Estrategias diferenciadas para manejo de missing values y outliers",
                "ponderacion": 0.10,
                "niveles": niveles_estandar,
                "archivos_revisar": ["src/*/pipelines/data_engineering/"]
            },
            {
                "nombre": "Transformación y Feature Engineering",
                "descripcion": "Transformaciones avanzadas justificadas con feature engineering creativo",
                "ponderacion": 0.10,
                "niveles": niveles_estandar,
                "archivos_revisar": ["src/*/pipelines/data_science/", "notebooks/03_data_preparation.ipynb"]
            },
            {
                "nombre": "Identificación de Targets para ML",
                "descripcion": "Targets correctos para regresión/clasificación con justificación sólida",
                "ponderacion": 0.10,
                "niveles": niveles_estandar,
                "archivos_revisar": ["notebooks/01_business_understanding.ipynb"]
            },
            {
                "nombre": "Documentación y Notebooks",
                "descripcion": "Documentación excepcional con notebooks estructurados por CRISP-DM",
                "ponderacion": 0.10,
                "niveles": niveles_estandar,
                "archivos_revisar": ["README.md", "notebooks/*.ipynb", "docs/"]
            },
            {
                "nombre": "Reproducibilidad y Mejores Prácticas",
                "descripcion": "Proyecto completamente reproducible siguiendo mejores prácticas",
                "ponderacion": 0.10,
                "niveles": niveles_estandar,
                "archivos_revisar": ["requirements.txt", ".gitignore", "conf/base/parameters.yml"]
            }
        ]
    }


# Ejemplo de uso
if __name__ == "__main__":
    
    # Configuración
    GITHUB_TOKEN = "tu_github_token_aqui"
    LLM_PROVIDER = "github"  # o "gemini", "huggingface"
    LLM_API_KEY = "tu_api_key_aqui"
    
    # Inicializar evaluador
    evaluador = RubricaEvaluator(
        github_token=GITHUB_TOKEN,
        llm_provider=LLM_PROVIDER,
        llm_api_key=LLM_API_KEY
    )
    
    # Cargar rúbrica
    rubrica_dict = create_kedro_rubrica()
    rubrica = evaluador.load_rubrica_from_dict(rubrica_dict)
    
    # Evaluar repositorio
    repo_url = "https://github.com/usuario/proyecto-ml-parejas"
    
    print("🚀 Iniciando evaluación automática...")
    evaluacion = evaluador.evaluate_repository(repo_url, rubrica)
    
    # Exportar resultados
    evaluador.export_evaluation(evaluacion, "evaluacion_proyecto")
    
    print(f"\n🎯 Evaluación completada:")
    print(f"Nota final: {evaluacion.nota_final}/7.0")
    print(f"Tiempo: {evaluacion.tiempo_evaluacion:.2f} segundos")
