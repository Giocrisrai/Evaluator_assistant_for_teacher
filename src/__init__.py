# __init__.py - Módulo principal del sistema de evaluación

"""
Sistema de Evaluación Automática con Rúbricas

Este módulo proporciona herramientas para evaluar automáticamente 
repositorios de GitHub usando IA y rúbricas personalizables.
"""

__version__ = "1.0.0"
__author__ = "Tu Nombre"
__email__ = "tu.email@universidad.cl"

# Imports principales para facilitar el uso
from .rubrica_evaluator import (
    CriterioRubrica,
    ResultadoCriterio, 
    EvaluacionCompleta,
    GitHubAnalyzer,
    LLMEvaluator,
    RubricaEvaluator,
    create_kedro_rubrica
)

from .config import Config

# Versiones de las APIs compatibles
SUPPORTED_APIS = {
    "github": ">=1.59.0",
    "openai": ">=1.3.0", 
    "google-generativeai": ">=0.3.0",
    "huggingface": ">=0.19.0"
}

__all__ = [
    "CriterioRubrica",
    "ResultadoCriterio",
    "EvaluacionCompleta", 
    "GitHubAnalyzer",
    "LLMEvaluator",
    "RubricaEvaluator",
    "create_kedro_rubrica",
    "Config"
]
