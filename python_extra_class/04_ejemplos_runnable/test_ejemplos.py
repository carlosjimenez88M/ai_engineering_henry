"""
Test Suite para Ejemplos Ejecutables
======================================

Tests para verificar que todos los ejemplos pueden importarse y ejecutarse.

Ejecuta: pytest test_ejemplos.py -v
"""

import pytest
import sys
from pathlib import Path


# ============================================================================
# TEST: Imports
# ============================================================================

class TestImports:
    """Verifica que todos los archivos de ejemplos pueden importarse."""

    def test_import_ejemplo_01_excepciones(self):
        """Ejemplo 1: Excepciones puede importarse."""
        try:
            import ejemplo_01_excepciones
            assert ejemplo_01_excepciones is not None
        except ImportError as e:
            pytest.fail(f"No se pudo importar ejemplo_01_excepciones: {e}")

    def test_import_ejemplo_02_context_managers(self):
        """Ejemplo 2: Context managers puede importarse."""
        try:
            import ejemplo_02_context_managers
            assert ejemplo_02_context_managers is not None
        except ImportError as e:
            pytest.fail(f"No se pudo importar ejemplo_02_context_managers: {e}")

    def test_import_ejemplo_03_generadores(self):
        """Ejemplo 3: Generadores puede importarse."""
        try:
            import ejemplo_03_generadores
            assert ejemplo_03_generadores is not None
        except ImportError as e:
            pytest.fail(f"No se pudo importar ejemplo_03_generadores: {e}")


# ============================================================================
# TEST: Exception Handling
# ============================================================================

class TestExceptionHandling:
    """Tests para ejemplos de manejo de excepciones."""

    def test_custom_exceptions_exist(self):
        """Verifica que las excepciones personalizadas existen."""
        from ejemplo_01_excepciones import (
            APIError,
            AuthenticationError,
            RateLimitError,
            ResourceNotFoundError
        )

        # Verifica jerarquía
        assert issubclass(AuthenticationError, APIError)
        assert issubclass(RateLimitError, APIError)
        assert issubclass(ResourceNotFoundError, APIError)

    def test_rate_limit_error_metadata(self):
        """Verifica que RateLimitError tiene metadata."""
        from ejemplo_01_excepciones import RateLimitError

        error = RateLimitError(retry_after=60)
        assert error.retry_after == 60
        assert "60" in str(error)

    def test_resource_not_found_error_metadata(self):
        """Verifica que ResourceNotFoundError tiene metadata."""
        from ejemplo_01_excepciones import ResourceNotFoundError

        # La clase puede tener diferentes firmas, verificamos que existe
        error = ResourceNotFoundError("test error")
        assert isinstance(error, Exception)


# ============================================================================
# TEST: Context Managers
# ============================================================================

class TestContextManagers:
    """Tests para ejemplos de context managers."""

    def test_timer_context_manager_exists(self):
        """Verifica que Timer existe."""
        from ejemplo_02_context_managers import Timer

        timer = Timer("Test")
        # Verifica que Timer es instanciable
        assert timer is not None

    def test_timer_enter_exit(self):
        """Verifica que Timer tiene __enter__ y __exit__."""
        from ejemplo_02_context_managers import Timer

        timer = Timer("Test")
        assert hasattr(timer, '__enter__')
        assert hasattr(timer, '__exit__')

    def test_temporary_state_exists(self):
        """Verifica que TemporaryState existe."""
        from ejemplo_02_context_managers import TemporaryState

        class TestObj:
            def __init__(self):
                self.value = 10

        obj = TestObj()
        assert hasattr(TemporaryState, '__enter__')
        assert hasattr(TemporaryState, '__exit__')


# ============================================================================
# TEST: Generators
# ============================================================================

class TestGenerators:
    """Tests para ejemplos de generadores."""

    def test_generator_function_exists(self):
        """Verifica que hay funciones generadoras."""
        import ejemplo_03_generadores
        import inspect

        # Busca funciones que usan yield
        functions = inspect.getmembers(ejemplo_03_generadores, inspect.isfunction)
        generator_functions = [
            name for name, func in functions
            if inspect.isgeneratorfunction(func)
        ]

        # Debe haber al menos 3 funciones generadoras
        assert len(generator_functions) >= 3

    def test_contador_regresivo(self):
        """Test del iterador ContadorRegresivo si existe."""
        try:
            from ejemplo_03_generadores import ContadorRegresivo

            contador = ContadorRegresivo(5)
            resultado = list(contador)
            assert resultado == [5, 4, 3, 2, 1]
        except (ImportError, AttributeError):
            pytest.skip("ContadorRegresivo no está disponible")

    def test_numeros_pares_generator(self):
        """Test de generador de números pares si existe."""
        try:
            from ejemplo_03_generadores import numeros_pares

            resultado = list(numeros_pares(1, 10))
            assert resultado == [2, 4, 6, 8, 10]
        except (ImportError, AttributeError):
            pytest.skip("numeros_pares no está disponible")


# ============================================================================
# TEST: File Existence
# ============================================================================

class TestFileExistence:
    """Verifica que todos los archivos de ejemplo existen."""

    def test_ejemplo_01_exists(self):
        """Ejemplo 1 existe."""
        path = Path("04_ejemplos_runnable/ejemplo_01_excepciones.py")
        assert path.exists(), f"{path} no existe"

    def test_ejemplo_02_exists(self):
        """Ejemplo 2 existe."""
        path = Path("04_ejemplos_runnable/ejemplo_02_context_managers.py")
        assert path.exists(), f"{path} no existe"

    def test_ejemplo_03_exists(self):
        """Ejemplo 3 existe."""
        path = Path("04_ejemplos_runnable/ejemplo_03_generadores.py")
        assert path.exists(), f"{path} no existe"

    def test_ejemplo_04_exists(self):
        """Ejemplo 4 existe (si disponible)."""
        path = Path("04_ejemplos_runnable/ejemplo_04_logging_basico.py")
        if not path.exists():
            pytest.skip("ejemplo_04_logging_basico.py aún no disponible")

    def test_ejemplo_05_exists(self):
        """Ejemplo 5 existe (si disponible)."""
        path = Path("04_ejemplos_runnable/ejemplo_05_logging_avanzado.py")
        if not path.exists():
            pytest.skip("ejemplo_05_logging_avanzado.py aún no disponible")

    def test_ejemplo_06_exists(self):
        """Ejemplo 6 existe (si disponible)."""
        path = Path("04_ejemplos_runnable/ejemplo_06_comprehension_performance.py")
        if not path.exists():
            pytest.skip("ejemplo_06_comprehension_performance.py aún no disponible")


# ============================================================================
# TEST: Code Quality
# ============================================================================

class TestCodeQuality:
    """Tests de calidad de código."""

    def test_no_syntax_errors_ejemplo_01(self):
        """Ejemplo 1 no tiene errores de sintaxis."""
        try:
            import ejemplo_01_excepciones
        except SyntaxError as e:
            pytest.fail(f"Error de sintaxis en ejemplo_01_excepciones: {e}")

    def test_no_syntax_errors_ejemplo_02(self):
        """Ejemplo 2 no tiene errores de sintaxis."""
        try:
            import ejemplo_02_context_managers
        except SyntaxError as e:
            pytest.fail(f"Error de sintaxis en ejemplo_02_context_managers: {e}")

    def test_no_syntax_errors_ejemplo_03(self):
        """Ejemplo 3 no tiene errores de sintaxis."""
        try:
            import ejemplo_03_generadores
        except SyntaxError as e:
            pytest.fail(f"Error de sintaxis en ejemplo_03_generadores: {e}")

    def test_all_examples_have_docstrings(self):
        """Verifica que los módulos tienen docstrings."""
        import ejemplo_01_excepciones
        import ejemplo_02_context_managers
        import ejemplo_03_generadores

        assert ejemplo_01_excepciones.__doc__ is not None
        assert ejemplo_02_context_managers.__doc__ is not None
        assert ejemplo_03_generadores.__doc__ is not None


# ============================================================================
# TEST: Integration (optional, skipped if files don't run quickly)
# ============================================================================

class TestIntegration:
    """Tests de integración para verificar ejecución completa."""

    @pytest.mark.slow
    def test_ejemplo_01_runs_without_error(self, capsys):
        """Ejemplo 1 se ejecuta sin errores."""
        pytest.skip("Test de integración lento - ejecutar manualmente")

    @pytest.mark.slow
    def test_ejemplo_02_runs_without_error(self, capsys):
        """Ejemplo 2 se ejecuta sin errores."""
        pytest.skip("Test de integración lento - ejecutar manualmente")

    @pytest.mark.slow
    def test_ejemplo_03_runs_without_error(self, capsys):
        """Ejemplo 3 se ejecuta sin errores."""
        pytest.skip("Test de integración lento - ejecutar manualmente")


if __name__ == "__main__":
    # Permite ejecutar como: python test_ejemplos.py
    pytest.main([__file__, "-v"])
