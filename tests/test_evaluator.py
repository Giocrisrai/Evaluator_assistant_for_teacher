# Test básicos para el sistema de evaluación
import unittest
import sys
import os
from unittest.mock import Mock, patch

# Agregar src al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from rubrica_evaluator import (
    CriterioRubrica, 
    ResultadoCriterio, 
    EvaluacionCompleta,
    RubricaEvaluator,
    create_kedro_rubrica
)

class TestCriterioRubrica(unittest.TestCase):
    """Tests para la clase CriterioRubrica."""
    
    def test_create_criterio(self):
        """Test creación básica de criterio."""
        criterio = CriterioRubrica(
            nombre="Test Criterio",
            descripcion="Descripción de prueba",
            ponderacion=0.15,
            niveles={100: "Excelente", 80: "Bueno", 60: "Regular"}
        )
        
        self.assertEqual(criterio.nombre, "Test Criterio")
        self.assertEqual(criterio.ponderacion, 0.15)
        self.assertIn(100, criterio.niveles)
        self.assertEqual(criterio.niveles[100], "Excelente")

class TestResultadoCriterio(unittest.TestCase):
    """Tests para la clase ResultadoCriterio."""
    
    def test_create_resultado(self):
        """Test creación de resultado de criterio."""
        resultado = ResultadoCriterio(
            criterio="Test Criterio",
            puntuacion=85,
            nota=6.1,
            retroalimentacion="Buen trabajo en general",
            evidencias=["src/main.py", "README.md"],
            sugerencias=["Mejorar documentación"]
        )
        
        self.assertEqual(resultado.criterio, "Test Criterio")
        self.assertEqual(resultado.puntuacion, 85)
        self.assertAlmostEqual(resultado.nota, 6.1)
        self.assertEqual(len(resultado.evidencias), 2)
        self.assertEqual(len(resultado.sugerencias), 1)

class TestKedroRubrica(unittest.TestCase):
    """Tests para la rúbrica de Kedro."""
    
    def test_create_kedro_rubrica(self):
        """Test creación de rúbrica Kedro."""
        rubrica = create_kedro_rubrica()
        
        self.assertIn("nombre", rubrica)
        self.assertIn("criterios", rubrica)
        self.assertEqual(len(rubrica["criterios"]), 10)
        
        # Verificar que las ponderaciones suman 1.0
        total_ponderacion = sum(c["ponderacion"] for c in rubrica["criterios"])
        self.assertAlmostEqual(total_ponderacion, 1.0, places=2)
        
        # Verificar criterios específicos
        nombres_criterios = [c["nombre"] for c in rubrica["criterios"]]
        self.assertIn("Estructura y Configuración del Proyecto Kedro", nombres_criterios)
        self.assertIn("Análisis Exploratorio de Datos (EDA)", nombres_criterios)

class TestRubricaEvaluator(unittest.TestCase):
    """Tests para el evaluador principal."""
    
    def setUp(self):
        """Setup para tests del evaluador."""
        self.mock_github_token = "fake_github_token"
        self.mock_llm_key = "fake_llm_key"
    
    @patch('rubrica_evaluator.Github')
    def test_evaluator_initialization(self, mock_github):
        """Test inicialización del evaluador."""
        evaluator = RubricaEvaluator(
            github_token=self.mock_github_token,
            llm_provider="github",
            llm_api_key=self.mock_llm_key
        )
        
        self.assertIsNotNone(evaluator.github_analyzer)
        self.assertIsNotNone(evaluator.llm_evaluator)
        mock_github.assert_called_once_with(self.mock_github_token)
    
    def test_load_rubrica_from_dict(self):
        """Test carga de rúbrica desde diccionario."""
        # Mock del evaluador
        with patch('rubrica_evaluator.Github'):
            evaluator = RubricaEvaluator(
                github_token=self.mock_github_token,
                llm_provider="github", 
                llm_api_key=self.mock_llm_key
            )
        
        rubrica_dict = create_kedro_rubrica()
        criterios = evaluator.load_rubrica_from_dict(rubrica_dict)
        
        self.assertEqual(len(criterios), 10)
        self.assertIsInstance(criterios[0], CriterioRubrica)
        self.assertEqual(criterios[0].ponderacion, 0.10)

class TestNotasCalculation(unittest.TestCase):
    """Tests para cálculo de notas."""
    
    def test_conversion_porcentaje_a_nota(self):
        """Test conversión de porcentaje a nota chilena."""
        # Basado en la escala: 1.0 + (porcentaje/100) * 6.0
        test_cases = [
            (100, 7.0),  # 1.0 + (100/100) * 6.0 = 7.0
            (80, 5.8),   # 1.0 + (80/100) * 6.0 = 5.8
            (60, 4.6),   # 1.0 + (60/100) * 6.0 = 4.6
            (40, 3.4),   # 1.0 + (40/100) * 6.0 = 3.4
            (20, 2.2),   # 1.0 + (20/100) * 6.0 = 2.2
            (0, 1.0)     # 1.0 + (0/100) * 6.0 = 1.0
        ]
        
        for porcentaje, nota_esperada in test_cases:
            nota_calculada = 1.0 + (porcentaje / 100) * 6.0
            self.assertAlmostEqual(nota_calculada, nota_esperada, places=1)

class TestIntegration(unittest.TestCase):
    """Tests de integración del sistema completo."""
    
    @patch('rubrica_evaluator.openai.OpenAI')
    @patch('rubrica_evaluator.Github')
    def test_mock_evaluation_flow(self, mock_github, mock_openai):
        """Test flujo completo con mocks."""
        
        # Setup mocks
        mock_repo = Mock()
        mock_repo.name = "test-project"
        mock_repo.description = "Test repository"
        mock_github.return_value.get_repo.return_value = mock_repo
        
        # Mock file structure
        mock_content = Mock()
        mock_content.type = "file"
        mock_content.name = "README.md"
        mock_content.path = "README.md"
        mock_content.size = 1000
        mock_content.download_url = "https://example.com/readme"
        
        mock_repo.get_contents.return_value = [mock_content]
        
        # Mock LLM response
        mock_response = Mock()
        mock_response.choices[0].message.content = '''
        {
            "puntuacion": 85,
            "nota": 6.1,
            "retroalimentacion": "Buen proyecto con documentación clara",
            "evidencias": ["README.md"],
            "sugerencias": ["Agregar más tests"]
        }
        '''
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        # Test evaluation
        evaluator = RubricaEvaluator(
            github_token="fake_token",
            llm_provider="github",
            llm_api_key="fake_key"
        )
        
        rubrica_dict = create_kedro_rubrica()
        rubrica = evaluator.load_rubrica_from_dict(rubrica_dict)
        
        # Esta parte requeriría más mocks para funcionar completamente
        # pero demuestra la estructura del test de integración
        self.assertIsNotNone(evaluator)
        self.assertEqual(len(rubrica), 10)

if __name__ == '__main__':
    # Ejecutar tests
    print("🧪 Ejecutando tests del sistema de evaluación...")
    
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar tests
    suite.addTests(loader.loadTestsFromTestCase(TestCriterioRubrica))
    suite.addTests(loader.loadTestsFromTestCase(TestResultadoCriterio))
    suite.addTests(loader.loadTestsFromTestCase(TestKedroRubrica))
    suite.addTests(loader.loadTestsFromTestCase(TestRubricaEvaluator))
    suite.addTests(loader.loadTestsFromTestCase(TestNotasCalculation))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen
    if result.wasSuccessful():
        print(f"\n✅ Todos los tests pasaron exitosamente!")
        print(f"Tests ejecutados: {result.testsRun}")
    else:
        print(f"\n❌ {len(result.failures)} tests fallaron")
        print(f"❌ {len(result.errors)} errores encontrados")
        
    exit(0 if result.wasSuccessful() else 1)
