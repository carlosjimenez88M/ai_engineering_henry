"""
Ejemplos completos de manejo de excepciones en Python.

Este módulo muestra ejemplos prácticos y ejecutables de:
- try/except/else/finally
- Jerarquía de excepciones personalizadas
- Encadenamiento de excepciones
- LBYL vs EAFP
- Captura específica vs genérica

Filosofía: Código claro, ejemplos ejecutables, enfoque en el "por qué".
"""

import time
from typing import Dict, Any, Optional


# ============================================================================
# SECCIÓN 1: Jerarquía de Excepciones Personalizadas
# ============================================================================

class APIError(Exception):
    """
    Excepción base para todos los errores de API.

    Heredar de Exception te permite crear jerarquías de errores que puedes
    capturar de forma específica o general según necesites.
    """

    def __init__(self, message: str, status_code: Optional[int] = None) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class AuthenticationError(APIError):
    """Error de autenticación - credenciales inválidas."""

    def __init__(self, message: str = "Credenciales inválidas") -> None:
        super().__init__(message, status_code=401)


class RateLimitError(APIError):
    """Error de límite de tasa - demasiadas peticiones."""

    def __init__(self, retry_after: int = 60) -> None:
        self.retry_after = retry_after
        super().__init__(
            f"Límite de tasa excedido. Reintenta en {retry_after} segundos",
            status_code=429
        )


class ResourceNotFoundError(APIError):
    """Error de recurso no encontrado."""

    def __init__(self, resource_id: str) -> None:
        self.resource_id = resource_id
        super().__init__(
            f"Recurso '{resource_id}' no encontrado",
            status_code=404
        )


# ============================================================================
# SECCIÓN 2: Try/Except/Else/Finally - Ejemplo Completo
# ============================================================================

def ejemplo_try_except_else_finally() -> None:
    """
    Demuestra el flujo completo de try/except/else/finally.

    - try: código que puede fallar
    - except: maneja el error
    - else: se ejecuta si NO hubo error
    - finally: SIEMPRE se ejecuta (limpieza)
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 1: Try/Except/Else/Finally - Flujo Completo")
    print("=" * 70)

    def procesar_datos(datos: Dict[str, Any], simular_error: bool = False) -> str:
        """Procesa datos y retorna un resumen."""
        print(f"\n  → Procesando datos: {datos}")

        try:
            print("  → [TRY] Intentando acceder a 'usuario'...")
            usuario = datos["usuario"]

            if simular_error:
                raise ValueError("Error simulado intencionalmente")

            print(f"  → [TRY] Usuario encontrado: {usuario}")
            resultado = f"Usuario: {usuario}, Items: {len(datos)}"

        except KeyError as e:
            print(f"  → [EXCEPT] ¡Error! Clave faltante: {e}")
            resultado = "Error: datos incompletos"

        except ValueError as e:
            print(f"  → [EXCEPT] ¡Error de valor! {e}")
            resultado = f"Error: {e}"

        else:
            # Solo se ejecuta si NO hubo excepciones
            print("  → [ELSE] ✓ Procesamiento exitoso, sin errores")
            resultado = f"✓ {resultado}"

        finally:
            # SIEMPRE se ejecuta, haya o no error
            print("  → [FINALLY] Limpiando recursos (esto SIEMPRE se ejecuta)")

        return resultado

    # Caso 1: Todo funciona bien
    print("\nCaso 1: Datos completos, sin errores")
    resultado1 = procesar_datos({"usuario": "carlos", "edad": 30})
    print(f"  Resultado final: {resultado1}")

    # Caso 2: Falta una clave
    print("\nCaso 2: Datos incompletos (falta 'usuario')")
    resultado2 = procesar_datos({"edad": 30})
    print(f"  Resultado final: {resultado2}")

    # Caso 3: Error de valor
    print("\nCaso 3: Error simulado durante procesamiento")
    resultado3 = procesar_datos({"usuario": "ana"}, simular_error=True)
    print(f"  Resultado final: {resultado3}")


# ============================================================================
# SECCIÓN 3: Excepciones Personalizadas en Acción
# ============================================================================

def ejemplo_excepciones_personalizadas() -> None:
    """
    Demuestra el uso de jerarquía de excepciones personalizadas.

    ¿Por qué crear excepciones personalizadas?
    - Mayor claridad en el código
    - Manejo específico de diferentes errores
    - Información contextual adicional
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 2: Jerarquía de Excepciones Personalizadas")
    print("=" * 70)

    def simular_llamada_api(
        endpoint: str,
        token: Optional[str] = None,
        simular_error: str = "none"
    ) -> Dict[str, Any]:
        """Simula una llamada a API con diferentes tipos de errores."""
        print(f"\n  → Llamando a API: {endpoint}")

        if simular_error == "auth":
            print("  → Simulando error de autenticación...")
            raise AuthenticationError()

        if simular_error == "rate_limit":
            print("  → Simulando límite de tasa excedido...")
            raise RateLimitError(retry_after=30)

        if simular_error == "not_found":
            print("  → Simulando recurso no encontrado...")
            raise ResourceNotFoundError(resource_id=endpoint)

        print("  → ✓ Llamada exitosa")
        return {"status": "ok", "data": "Datos del endpoint"}

    # Caso 1: Captura específica de cada tipo de error
    print("\nCaso 1: Manejo específico de cada tipo de error")

    errores = ["auth", "rate_limit", "not_found", "none"]

    for tipo_error in errores:
        try:
            resultado = simular_llamada_api(
                "/api/usuarios",
                token="abc123",
                simular_error=tipo_error
            )
            print(f"  ✓ Resultado: {resultado}")

        except AuthenticationError as e:
            print(f"  ✗ [AuthenticationError] {e}")
            print("  → Acción: Solicitar nuevas credenciales")

        except RateLimitError as e:
            print(f"  ✗ [RateLimitError] {e}")
            print(f"  → Acción: Esperar {e.retry_after} segundos")

        except ResourceNotFoundError as e:
            print(f"  ✗ [ResourceNotFoundError] {e}")
            print(f"  → Acción: Verificar ID '{e.resource_id}'")

        except APIError as e:
            # Captura cualquier otro error de API
            print(f"  ✗ [APIError genérico] {e}")

    # Caso 2: Captura genérica de todos los errores de API
    print("\nCaso 2: Captura genérica (todos los errores de API)")

    try:
        simular_llamada_api("/api/datos", simular_error="auth")
    except APIError as e:
        # Captura CUALQUIER error que herede de APIError
        print(f"  ✗ [APIError] {e}")
        print(f"  → Tipo específico: {type(e).__name__}")
        print(f"  → Código de estado: {e.status_code}")


# ============================================================================
# SECCIÓN 4: Encadenamiento de Excepciones (raise from)
# ============================================================================

def ejemplo_encadenamiento_excepciones() -> None:
    """
    Demuestra el encadenamiento de excepciones con 'raise from'.

    ¿Por qué usar 'raise from'?
    - Preserva el contexto del error original
    - Facilita el debugging
    - Muestra la cadena de causas
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 3: Encadenamiento de Excepciones (raise from)")
    print("=" * 70)

    def leer_configuracion(archivo: str) -> Dict[str, Any]:
        """Lee configuración de un archivo (simulado)."""
        print(f"\n  → Intentando leer configuración de: {archivo}")

        try:
            # Simulamos un error de parsing JSON
            import json
            print("  → Parseando JSON...")
            # Esto causará un error
            raise json.JSONDecodeError("Invalid JSON", "", 0)

        except json.JSONDecodeError as e:
            # Encadenamos el error original con uno más específico
            print(f"  ✗ Error de JSON: {e}")
            print("  → Lanzando error personalizado con contexto...")
            raise APIError(
                f"No se pudo cargar configuración desde {archivo}"
            ) from e

    def inicializar_app() -> None:
        """Inicializa la aplicación cargando configuración."""
        print("\n  → Inicializando aplicación...")

        try:
            config = leer_configuracion("config.json")
        except APIError as e:
            print(f"\n  ✗ [APIError] {e}")

            # Con 'raise from', tenemos acceso a __cause__
            if e.__cause__:
                print(f"  → Causa raíz: {type(e.__cause__).__name__}: {e.__cause__}")

            print("\n  → La cadena de excepciones te muestra:")
            print("     1. El error de alto nivel (APIError)")
            print("     2. La causa raíz (JSONDecodeError)")
            print("     Esto facilita el debugging!")

    # Ejecutar ejemplo
    inicializar_app()

    # Comparación: SIN 'raise from'
    print("\n" + "-" * 70)
    print("Comparación: ¿Qué pasa SIN 'raise from'?")
    print("-" * 70)

    def leer_config_sin_from(archivo: str) -> Dict[str, Any]:
        """Lee configuración SIN preservar el contexto."""
        print(f"\n  → Intentando leer (sin 'from'): {archivo}")

        try:
            import json
            raise json.JSONDecodeError("Invalid JSON", "", 0)
        except json.JSONDecodeError as e:
            print(f"  ✗ Error de JSON: {e}")
            # SIN 'from' - perdemos el contexto
            raise APIError(f"No se pudo cargar {archivo}")

    try:
        leer_config_sin_from("config.json")
    except APIError as e:
        print(f"\n  ✗ [APIError] {e}")
        print(f"  → __cause__ es: {e.__cause__}")
        print("  → ¡Perdimos el contexto del error original!")


# ============================================================================
# SECCIÓN 5: LBYL vs EAFP - Comparación con Medición de Tiempo
# ============================================================================

def ejemplo_lbyl_vs_eafp() -> None:
    """
    Compara LBYL (Look Before You Leap) vs EAFP (Easier to Ask Forgiveness).

    LBYL: Verificar condiciones ANTES de ejecutar
    EAFP: Intentar ejecutar y MANEJAR excepciones

    En Python, EAFP es generalmente preferido (más pythonic).
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 4: LBYL vs EAFP - Comparación y Rendimiento")
    print("=" * 70)

    datos = {
        "nombre": "Carlos",
        "edad": 30,
        "ciudad": "Madrid"
    }

    # LBYL - Look Before You Leap
    print("\n[LBYL] Look Before You Leap - Verificar primero")
    print("-" * 70)

    def obtener_email_lbyl(datos: Dict[str, Any]) -> Optional[str]:
        """Estilo LBYL: verificar antes de acceder."""
        if "email" in datos:
            return datos["email"]
        return None

    start = time.perf_counter()
    for _ in range(100000):
        email = obtener_email_lbyl(datos)
    tiempo_lbyl = time.perf_counter() - start

    print(f"  Código: if 'email' in datos: return datos['email']")
    print(f"  Resultado: {email}")
    print(f"  Tiempo (100k iteraciones): {tiempo_lbyl:.4f} segundos")

    # EAFP - Easier to Ask Forgiveness than Permission
    print("\n[EAFP] Easier to Ask Forgiveness - Intentar y manejar")
    print("-" * 70)

    def obtener_email_eafp(datos: Dict[str, Any]) -> Optional[str]:
        """Estilo EAFP: intentar y manejar excepciones."""
        try:
            return datos["email"]
        except KeyError:
            return None

    start = time.perf_counter()
    for _ in range(100000):
        email = obtener_email_eafp(datos)
    tiempo_eafp = time.perf_counter() - start

    print(f"  Código: try: return datos['email'] except KeyError: return None")
    print(f"  Resultado: {email}")
    print(f"  Tiempo (100k iteraciones): {tiempo_eafp:.4f} segundos")

    # Análisis
    print("\n[ANÁLISIS]")
    print("-" * 70)
    diferencia = abs(tiempo_lbyl - tiempo_eafp)
    mas_rapido = "LBYL" if tiempo_lbyl < tiempo_eafp else "EAFP"

    print(f"  {mas_rapido} fue más rápido por {diferencia:.4f} segundos")
    print(f"\n  ¿Cuándo usar cada uno?")
    print(f"  • EAFP (preferido en Python):")
    print(f"    - Más pythonic y legible")
    print(f"    - Mejor para condiciones de carrera")
    print(f"    - Perfecto cuando el 'caso feliz' es común")
    print(f"  • LBYL:")
    print(f"    - Cuando las excepciones son muy frecuentes")
    print(f"    - Código que debe ser extremadamente rápido")

    # Ejemplo práctico: EAFP vs LBYL
    print("\n[EJEMPLO PRÁCTICO]")
    print("-" * 70)

    def procesar_usuario_lbyl(datos: Dict[str, Any]) -> str:
        """LBYL: múltiples verificaciones."""
        if "nombre" not in datos:
            return "Error: falta nombre"
        if "edad" not in datos:
            return "Error: falta edad"
        if not isinstance(datos["edad"], int):
            return "Error: edad no es un número"
        if datos["edad"] < 0:
            return "Error: edad negativa"

        return f"Usuario: {datos['nombre']}, {datos['edad']} años"

    def procesar_usuario_eafp(datos: Dict[str, Any]) -> str:
        """EAFP: intentar y manejar."""
        try:
            nombre = datos["nombre"]
            edad = datos["edad"]

            if edad < 0:
                raise ValueError("Edad negativa")

            return f"Usuario: {nombre}, {edad} años"

        except KeyError as e:
            return f"Error: falta {e}"
        except (TypeError, ValueError) as e:
            return f"Error: {e}"

    # Probar ambos
    casos = [
        {"nombre": "Ana", "edad": 25},
        {"nombre": "Bob"},
        {"nombre": "Carol", "edad": "treinta"},
        {"nombre": "David", "edad": -5}
    ]

    for i, caso in enumerate(casos, 1):
        print(f"\n  Caso {i}: {caso}")
        print(f"    LBYL: {procesar_usuario_lbyl(caso)}")
        print(f"    EAFP: {procesar_usuario_eafp(caso)}")


# ============================================================================
# SECCIÓN 6: Captura Específica vs Genérica
# ============================================================================

def ejemplo_captura_especifica_vs_generica() -> None:
    """
    Demuestra la importancia de capturar excepciones específicas.

    ¿Por qué es importante?
    - Diferentes errores requieren diferentes acciones
    - Evita ocultar bugs inesperados
    - Código más mantenible
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 5: Captura Específica vs Genérica")
    print("=" * 70)

    def dividir_numeros(a: float, b: float) -> float:
        """Divide dos números."""
        return a / b

    def procesar_lista(numeros: list) -> float:
        """Calcula el promedio de una lista."""
        return sum(numeros) / len(numeros)

    # MALO: Captura genérica
    print("\n❌ MAL EJEMPLO: Captura genérica (except Exception)")
    print("-" * 70)

    def calcular_mal(x: str, y: str, lista: list) -> None:
        """Ejemplo de captura demasiado genérica."""
        try:
            print(f"  → Intentando: dividir({x}, {y})")
            resultado_div = dividir_numeros(float(x), float(y))
            print(f"  → Resultado división: {resultado_div}")

            print(f"  → Intentando: promedio({lista})")
            resultado_prom = procesar_lista(lista)
            print(f"  → Resultado promedio: {resultado_prom}")

        except Exception as e:
            # ¡Esto captura TODO! Perdemos información específica
            print(f"  ✗ Error genérico: {e}")
            print(f"  ✗ Tipo: {type(e).__name__}")
            print("  ✗ No sabemos QUÉ falló ni CÓMO manejarlo")

    print("\n  Caso 1: División por cero")
    calcular_mal("10", "0", [1, 2, 3])

    print("\n  Caso 2: Lista vacía")
    calcular_mal("10", "5", [])

    print("\n  Caso 3: Conversión inválida")
    calcular_mal("abc", "5", [1, 2, 3])

    # BUENO: Captura específica
    print("\n\n✓ BUEN EJEMPLO: Captura específica")
    print("-" * 70)

    def calcular_bien(x: str, y: str, lista: list) -> None:
        """Ejemplo de captura específica de excepciones."""
        try:
            print(f"  → Intentando: dividir({x}, {y})")
            resultado_div = dividir_numeros(float(x), float(y))
            print(f"  ✓ Resultado división: {resultado_div}")

        except ValueError as e:
            print(f"  ✗ [ValueError] No se puede convertir a número: {e}")
            print("  → Acción: Validar entrada del usuario")

        except ZeroDivisionError:
            print(f"  ✗ [ZeroDivisionError] No se puede dividir por cero")
            print("  → Acción: Pedir un divisor diferente")

        try:
            print(f"  → Intentando: promedio({lista})")
            resultado_prom = procesar_lista(lista)
            print(f"  ✓ Resultado promedio: {resultado_prom}")

        except ZeroDivisionError:
            print(f"  ✗ [ZeroDivisionError] Lista vacía, no se puede promediar")
            print("  → Acción: Usar valor por defecto o pedir más datos")

        except TypeError as e:
            print(f"  ✗ [TypeError] Tipo incorrecto en lista: {e}")
            print("  → Acción: Filtrar valores no numéricos")

    print("\n  Caso 1: División por cero")
    calcular_bien("10", "0", [1, 2, 3])

    print("\n  Caso 2: Lista vacía")
    calcular_bien("10", "5", [])

    print("\n  Caso 3: Conversión inválida")
    calcular_bien("abc", "5", [1, 2, 3])

    # Orden de captura importa
    print("\n\n[IMPORTANTE: Orden de Captura]")
    print("-" * 70)
    print("  Las excepciones se capturan de ARRIBA hacia ABAJO")
    print("  Debes poner las más ESPECÍFICAS primero:")
    print()
    print("  ✓ CORRECTO:")
    print("    except ValueError:      # Específica")
    print("    except TypeError:       # Específica")
    print("    except Exception:       # Genérica")
    print()
    print("  ✗ INCORRECTO:")
    print("    except Exception:       # Genérica primero")
    print("    except ValueError:      # Nunca se alcanzará!")


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main() -> None:
    """
    Ejecuta todos los ejemplos de manejo de excepciones.

    Cada ejemplo es independiente y muestra un concepto diferente
    con salida clara para entender qué está sucediendo.
    """
    print("\n" + "=" * 70)
    print("EJEMPLOS COMPLETOS DE MANEJO DE EXCEPCIONES EN PYTHON")
    print("=" * 70)
    print("\nEstos ejemplos te mostrarán:")
    print("  1. Try/Except/Else/Finally - Flujo completo")
    print("  2. Jerarquía de excepciones personalizadas")
    print("  3. Encadenamiento de excepciones (raise from)")
    print("  4. LBYL vs EAFP con medición de rendimiento")
    print("  5. Captura específica vs genérica")

    # Ejecutar todos los ejemplos
    ejemplo_try_except_else_finally()
    ejemplo_excepciones_personalizadas()
    ejemplo_encadenamiento_excepciones()
    ejemplo_lbyl_vs_eafp()
    ejemplo_captura_especifica_vs_generica()

    # Resumen final
    print("\n" + "=" * 70)
    print("RESUMEN DE MEJORES PRÁCTICAS")
    print("=" * 70)
    print("""
1. USA try/except/else/finally para control de flujo claro
   • try: código que puede fallar
   • except: maneja errores específicos
   • else: código cuando NO hay error
   • finally: limpieza que SIEMPRE se ejecuta

2. CREA jerarquías de excepciones personalizadas
   • Hereda de Exception o una excepción más específica
   • Añade información contextual (status_code, etc.)
   • Facilita el manejo específico de errores

3. USA 'raise from' para preservar contexto
   • Muestra la cadena completa de errores
   • Facilita el debugging
   • Mantiene trazabilidad

4. PREFIERE EAFP sobre LBYL en Python
   • Más pythonic y legible
   • Mejor para threading
   • Perfecto para el 'caso feliz'

5. CAPTURA excepciones ESPECÍFICAS
   • Evita 'except Exception:' sin razón
   • Cada error puede necesitar acción diferente
   • Orden importa: específicas primero

¿Dudas? Experimenta modificando estos ejemplos. ¡La práctica es clave!
    """)


if __name__ == "__main__":
    main()
