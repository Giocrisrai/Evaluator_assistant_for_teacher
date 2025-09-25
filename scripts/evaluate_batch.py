#!/usr/bin/env python
"""
Script de Evaluación Masiva para Proyectos Kedro ML
Evalúa múltiples repositorios de estudiantes de manera eficiente
"""

import os
import sys
import csv
import json
import time
import argparse
import concurrent.futures
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Tuple
import pandas as pd

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from kedro_evaluator import KedroEvaluator, EvaluacionKedro
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EvaluadorMasivo:
    """Maneja la evaluación masiva de proyectos."""
    
    def __init__(self, github_token: str, output_dir: str = "evaluaciones"):
        """
        Inicializa el evaluador masivo.
        
        Args:
            github_token: Token de GitHub
            output_dir: Directorio de salida para las evaluaciones
        """
        self.evaluador = KedroEvaluator(github_token)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.resultados = []
        
    def cargar_estudiantes_csv(self, archivo_csv: str) -> List[Dict[str, str]]:
        """
        Carga la lista de estudiantes desde un archivo CSV.
        
        Formato esperado del CSV:
        nombre,pareja,repositorio
        Juan Pérez,María González,https://github.com/usuario/repo
        
        Args:
            archivo_csv: Path al archivo CSV
            
        Returns:
            Lista de diccionarios con información de estudiantes
        """
        estudiantes = []
        
        try:
            with open(archivo_csv, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    estudiante = {
                        'nombre': row.get('nombre', '').strip(),
                        'pareja': row.get('pareja', '').strip() or None,
                        'repositorio': row.get('repositorio', '').strip()
                    }
                    
                    # Validar que tenga los campos mínimos
                    if estudiante['nombre'] and estudiante['repositorio']:
                        estudiantes.append(estudiante)
                    else:
                        logger.warning(f"Entrada inválida en CSV: {row}")
                        
            logger.info(f"Cargados {len(estudiantes)} estudiantes desde {archivo_csv}")
            
        except FileNotFoundError:
            logger.error(f"Archivo no encontrado: {archivo_csv}")
        except Exception as e:
            logger.error(f"Error leyendo CSV: {e}")
            
        return estudiantes
    
    def evaluar_estudiante(self, estudiante: Dict[str, str]) -> Tuple[str, EvaluacionKedro]:
        """
        Evalúa un solo estudiante.
        
        Args:
            estudiante: Diccionario con información del estudiante
            
        Returns:
            Tupla (nombre_estudiante, evaluacion)
        """
        nombre = estudiante['nombre']
        logger.info(f"Evaluando a {nombre}...")
        
        try:
            evaluacion = self.evaluador.evaluar_proyecto(
                repo_url=estudiante['repositorio'],
                estudiante_nombre=nombre,
                estudiante_pareja=estudiante.get('pareja'),
                aplicar_bonificaciones=True
            )
            
            # Guardar evaluación individual
            self.guardar_evaluacion_individual(nombre, evaluacion)
            
            logger.info(f"✅ {nombre}: Nota {evaluacion.nota_final:.1f} - {evaluacion.estado}")
            return nombre, evaluacion
            
        except Exception as e:
            logger.error(f"❌ Error evaluando a {nombre}: {e}")
            return nombre, None
    
    def evaluar_todos(self, estudiantes: List[Dict[str, str]], 
                      paralelo: int = 1) -> Dict[str, Any]:
        """
        Evalúa todos los estudiantes de la lista.
        
        Args:
            estudiantes: Lista de estudiantes a evaluar
            paralelo: Número de evaluaciones en paralelo
            
        Returns:
            Diccionario con estadísticas y resultados
        """
        inicio = time.time()
        logger.info(f"Iniciando evaluación masiva de {len(estudiantes)} proyectos")
        
        evaluaciones_exitosas = []
        evaluaciones_fallidas = []
        
        if paralelo > 1:
            # Evaluación en paralelo
            with concurrent.futures.ThreadPoolExecutor(max_workers=paralelo) as executor:
                futuros = {
                    executor.submit(self.evaluar_estudiante, est): est 
                    for est in estudiantes
                }
                
                for futuro in concurrent.futures.as_completed(futuros):
                    nombre, evaluacion = futuro.result()
                    if evaluacion:
                        evaluaciones_exitosas.append((nombre, evaluacion))
                        self.resultados.append(evaluacion)
                    else:
                        evaluaciones_fallidas.append(nombre)
        else:
            # Evaluación secuencial
            for estudiante in estudiantes:
                nombre, evaluacion = self.evaluar_estudiante(estudiante)
                if evaluacion:
                    evaluaciones_exitosas.append((nombre, evaluacion))
                    self.resultados.append(evaluacion)
                else:
                    evaluaciones_fallidas.append(nombre)
        
        tiempo_total = time.time() - inicio
        
        # Generar estadísticas
        estadisticas = self.generar_estadisticas(evaluaciones_exitosas)
        estadisticas['tiempo_total'] = tiempo_total
        estadisticas['evaluaciones_fallidas'] = evaluaciones_fallidas
        
        # Guardar resumen
        self.guardar_resumen(estadisticas, evaluaciones_exitosas)
        
        logger.info(f"Evaluación masiva completada en {tiempo_total:.1f} segundos")
        logger.info(f"Exitosas: {len(evaluaciones_exitosas)}, Fallidas: {len(evaluaciones_fallidas)}")
        
        return estadisticas
    
    def generar_estadisticas(self, evaluaciones: List[Tuple[str, EvaluacionKedro]]) -> Dict:
        """Genera estadísticas del curso."""
        if not evaluaciones:
            return {}
        
        notas = [ev.nota_final for _, ev in evaluaciones]
        aprobados = [ev for _, ev in evaluaciones if ev.estado == "APROBADO"]
        
        estadisticas = {
            'total_evaluados': len(evaluaciones),
            'aprobados': len(aprobados),
            'reprobados': len(evaluaciones) - len(aprobados),
            'porcentaje_aprobacion': (len(aprobados) / len(evaluaciones)) * 100,
            'nota_promedio': sum(notas) / len(notas),
            'nota_minima': min(notas),
            'nota_maxima': max(notas)
        }
        
        return estadisticas
    
    def guardar_evaluacion_individual(self, nombre: str, evaluacion: EvaluacionKedro):
        """Guarda la evaluación individual de un estudiante."""
        nombre_limpio = nombre.replace(' ', '_').replace('/', '_')
        fecha = datetime.now().strftime("%Y%m%d")
        directorio = self.output_dir / f"{nombre_limpio}_{fecha}"
        directorio.mkdir(parents=True, exist_ok=True)
        
        # Guardar JSON
        with open(directorio / "evaluacion.json", 'w', encoding='utf-8') as f:
            json.dump(evaluacion.to_dict(), f, indent=2, ensure_ascii=False)
        
        # Guardar reportes
        with open(directorio / "reporte.md", 'w', encoding='utf-8') as f:
            f.write(self.evaluador.generar_reporte(evaluacion, "markdown"))
        
        with open(directorio / "reporte.html", 'w', encoding='utf-8') as f:
            f.write(self.evaluador.generar_reporte(evaluacion, "html"))
    
    def guardar_resumen(self, estadisticas: Dict, evaluaciones: List[Tuple[str, EvaluacionKedro]]):
        """Guarda el resumen del curso."""
        fecha = datetime.now().strftime("%Y%m%d_%H%M")
        
        # Guardar estadísticas JSON
        with open(self.output_dir / f"estadisticas_{fecha}.json", 'w', encoding='utf-8') as f:
            json.dump(estadisticas, f, indent=2, ensure_ascii=False)
        
        # Crear DataFrame con resultados
        datos_tabla = []
        for nombre, ev in evaluaciones:
            datos_tabla.append({
                'Estudiante': nombre,
                'Pareja': ev.estudiante_pareja or '-',
                'Nota Final': ev.nota_final,
                'Porcentaje': ev.porcentaje_total,
                'Estado': ev.estado,
                'Repositorio': ev.repositorio_url
            })
        
        if datos_tabla:
            df = pd.DataFrame(datos_tabla)
            df.to_csv(self.output_dir / f"notas_{fecha}.csv", index=False, encoding='utf-8')
            df.to_excel(self.output_dir / f"notas_{fecha}.xlsx", index=False)
        
        logger.info(f"Resumen guardado en {self.output_dir}")


def main():
    """Función principal del script."""
    parser = argparse.ArgumentParser(description='Evaluación masiva de proyectos Kedro ML')
    parser.add_argument('--csv', required=True, help='Archivo CSV con lista de estudiantes')
    parser.add_argument('--token', help='GitHub token (o usar variable GITHUB_TOKEN)')
    parser.add_argument('--output', default='evaluaciones', help='Directorio de salida')
    parser.add_argument('--parallel', type=int, default=1, help='Número de evaluaciones en paralelo')
    parser.add_argument('--debug', action='store_true', help='Modo debug con más información')
    
    args = parser.parse_args()
    
    # Configurar logging
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Obtener token
    github_token = args.token or os.getenv('GITHUB_TOKEN')
    if not github_token:
        logger.error("Se requiere un GitHub token (--token o variable GITHUB_TOKEN)")
        sys.exit(1)
    
    # Crear evaluador masivo
    evaluador = EvaluadorMasivo(github_token, args.output)
    
    # Cargar estudiantes
    estudiantes = evaluador.cargar_estudiantes_csv(args.csv)
    
    if not estudiantes:
        logger.error("No se encontraron estudiantes válidos en el CSV")
        sys.exit(1)
    
    # Evaluar todos
    print(f"\n{'='*60}")
    print(f"EVALUACIÓN MASIVA DE PROYECTOS KEDRO ML")
    print(f"{'='*60}")
    print(f"Estudiantes a evaluar: {len(estudiantes)}")
    print(f"Evaluaciones en paralelo: {args.parallel}")
    print(f"Directorio de salida: {args.output}")
    print(f"{'='*60}\n")
    
    estadisticas = evaluador.evaluar_todos(estudiantes, args.parallel)
    
    # Mostrar resumen
    print(f"\n{'='*60}")
    print("RESUMEN DE EVALUACIÓN")
    print(f"{'='*60}")
    print(f"Total evaluados: {estadisticas.get('total_evaluados', 0)}")
    print(f"Aprobados: {estadisticas.get('aprobados', 0)} ({estadisticas.get('porcentaje_aprobacion', 0):.1f}%)")
    print(f"Nota promedio: {estadisticas.get('nota_promedio', 0):.2f}")
    print(f"Tiempo total: {estadisticas.get('tiempo_total', 0):.1f} segundos")
    print(f"{'='*60}\n")
    
    print(f"✅ Evaluación completada. Resultados guardados en {args.output}/")


if __name__ == "__main__":
    main()
