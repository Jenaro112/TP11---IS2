"""Módulo de conversión de datos en formato JSON a formato CSV.

Este módulo implementa una arquitectura de filtro orientada al flujo de datos,
permitiendo la lectura desde archivos o flujos de entrada estándar (stdin),
el aplanamiento de estructuras jerárquicas y la emisión resultante hacia
archivos de salida o la salida estándar (stdout).
"""

import contextlib
import csv
import json
import sys
from collections.abc import Iterable
from typing import Any, TextIO


def aplanar_diccionario(
    datos: dict[str, Any], prefijo: str = "", separador: str = "."
) -> dict[str, Any]:
    """Aplana recursivamente un diccionario con estructuras anidadas.

    Args:
        datos (Dict[str, Any]): Diccionario a aplanar.
        prefijo (str, optional): Prefijo acumulado para las claves anidadas.
        separador (str, optional): Separador jerárquico. Por defecto es '.'.

    Returns:
        Dict[str, Any]: Diccionario plano con claves compuestas.
    """
    resultado: dict[str, Any] = {}
    for clave, valor in datos.items():
        clave_compuesta = f"{prefijo}{separador}{clave}" if prefijo else str(clave)
        if isinstance(valor, dict):
            resultado.update(
                aplanar_diccionario(valor, clave_compuesta, separador=separador)
            )
        elif isinstance(valor, list):
            # Si la lista contiene elementos primitivos, los unimos o serializamos
            resultado[clave_compuesta] = json.dumps(valor, ensure_ascii=False)
        else:
            resultado[clave_compuesta] = valor
    return resultado


def normalizar_datos_json(contenido_json: Any) -> list[dict[str, Any]]:
    """Normaliza y valida que la entrada JSON sea convertible a registros tabulares.

    Args:
        contenido_json (Any): Estructura deserializada de JSON.

    Returns:
        List[Dict[str, Any]]: Lista de diccionarios aplanados listos para CSV.

    Raises:
        ValueError: Si la estructura no es una lista ni un diccionario.
    """
    if isinstance(contenido_json, dict):
        return [aplanar_diccionario(contenido_json)]
    if isinstance(contenido_json, list):
        filas: list[dict[str, Any]] = []
        for item in contenido_json:
            if isinstance(item, dict):
                filas.append(aplanar_diccionario(item))
            else:
                filas.append({"valor": item})
        return filas
    raise ValueError(
        f"Tipo de estructura JSON no soportada: {type(contenido_json).__name__}. "
        "Se esperaba un objeto o lista de objetos."
    )


def obtener_encabezados(filas: Iterable[dict[str, Any]]) -> list[str]:
    """Extrae la unión ordenada de todos los nombres de campos presentes.

    Args:
        filas (Iterable[Dict[str, Any]]): Colección de diccionarios aplanados.

    Returns:
        List[str]: Lista con todas las columnas únicas encontradas.
    """
    encabezados: list[str] = []
    vistos = set()
    for fila in filas:
        for clave in fila:
            if clave not in vistos:
                vistos.add(clave)
                encabezados.append(clave)
    return encabezados


def json_a_csv_stream(
    flujo_entrada: TextIO,
    flujo_salida: TextIO,
    delimitador: str = ",",
) -> int:
    """Convierte un flujo de entrada JSON a un flujo de salida CSV.

    Args:
        flujo_entrada (TextIO): Flujo de lectura (archivo o sys.stdin).
        flujo_salida (TextIO): Flujo de escritura (archivo o sys.stdout).
        delimitador (str, optional): Carácter delimitador de campos. Por defecto ','.

    Returns:
        int: Número total de filas de datos escritas (excluyendo el encabezado).

    Raises:
        ValueError: Si el delimitador no es válido o la entrada está vacía.
        json.JSONDecodeError: Si el contenido no es JSON válido.
    """
    if not delimitador or len(delimitador) != 1:
        raise ValueError(
            f"El delimitador debe ser un único carácter. Recibido: {delimitador!r}"
        )

    reconfigure_fn = getattr(flujo_entrada, "reconfigure", None)
    if callable(reconfigure_fn):
        with contextlib.suppress(AttributeError, ValueError, OSError):
            reconfigure_fn(encoding="utf-8-sig")

    contenido_texto = flujo_entrada.read()
    if not contenido_texto.strip():
        # Entrada vacía: no se escriben registros
        return 0

    # Manejo de BOM en Windows PowerShell (UTF-8 o ANSI)
    if contenido_texto.startswith("\xef\xbb\xbf"):
        try:
            contenido_texto = contenido_texto.encode("latin1").decode("utf-8-sig")
        except Exception:  # noqa: BLE001
            contenido_texto = contenido_texto.lstrip("\xef\xbb\xbf")
    elif contenido_texto.startswith("\ufeff"):
        contenido_texto = contenido_texto.lstrip("\ufeff")

    datos_deserializados = json.loads(contenido_texto)
    filas = normalizar_datos_json(datos_deserializados)

    if not filas:
        return 0

    encabezados = obtener_encabezados(filas)
    escritor = csv.DictWriter(
        flujo_salida,
        fieldnames=encabezados,
        delimiter=delimitador,
        quoting=csv.QUOTE_MINIMAL,
        lineterminator="\n",
    )

    escritor.writeheader()
    for fila in filas:
        escritor.writerow(fila)

    return len(filas)


def ejecutar_filtro(
    archivo_entrada: str | None = None,
    archivo_salida: str | None = None,
    delimitador: str = ",",
) -> int:
    """Ejecuta la estrategia de filtro resolviendo los orígenes y destinos de datos.

    Args:
        archivo_entrada (Optional[str]): Ruta del archivo de entrada, o None para stdin.
        archivo_salida (Optional[str]): Ruta del archivo de salida, o None para stdout.
        delimitador (str): Delimitador a emplear. Por defecto ','.

    Returns:
        int: Código de retorno (0 para éxito, distinto de 0 en error).
    """
    manejador_entrada: TextIO = sys.stdin
    manejador_salida: TextIO = sys.stdout

    try:
        if archivo_entrada:
            manejador_entrada = open(archivo_entrada, "r", encoding="utf-8")
        if archivo_salida:
            manejador_salida = open(archivo_salida, "w", encoding="utf-8", newline="")

        json_a_csv_stream(manejador_entrada, manejador_salida, delimitador=delimitador)
        return 0

    except FileNotFoundError as err:
        sys.stderr.write(
            f"Error: No se encontró el archivo de entrada '{err.filename}'.\n"
        )
        return 1
    except PermissionError as err:
        sys.stderr.write(f"Error: Permiso denegado al acceder a '{err.filename}'.\n")
        return 2
    except json.JSONDecodeError as err:
        sys.stderr.write(
            f"Error: Formato JSON inválido. Detalle: {err.msg} "
            f"(Línea {err.lineno}, Col {err.colno}).\n"
        )
        return 3
    except ValueError as err:
        sys.stderr.write(f"Error de valor: {err}\n")
        return 4
    except Exception as err:
        sys.stderr.write(f"Error inesperado durante la conversión: {err}\n")
        return 5
    finally:
        if manejador_entrada and archivo_entrada:
            manejador_entrada.close()
        if manejador_salida and archivo_salida:
            manejador_salida.close()
