#!/usr/bin/env python3
"""Herramienta de consola para convertir archivos de formato JSON a CSV.

Uso:
    python json2csv.py {-i input.txt} {-o output.txt} {-d delimitador}

Argumentos opcionales:
    -i, --input        Ruta al archivo JSON de entrada. Si se omite, se lee de stdin.
    -o, --output       Ruta al archivo CSV de salida. Si se omite, se emite por stdout.
    -d, --delimiter    Carácter delimitador de campos CSV. Por defecto es ','.
"""

import argparse
import sys

from src.json2csv.converter import ejecutar_filtro


def parsear_argumentos(argumentos: list[str] | None = None) -> argparse.Namespace:
    """Configura y parsea los argumentos de línea de comandos.

    Args:
        argumentos (list[str] | None): Lista de argumentos a procesar
            (sys.argv por defecto).

    Returns:
        argparse.Namespace: Objeto con los parámetros parseados.
    """
    parser = argparse.ArgumentParser(
        description="Filtro para convertir archivos de formato JSON a formato CSV.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Ejemplos:\n"
            "  python json2csv.py -i datos.json -o datos.csv\n"
            "  python json2csv.py -i datos.json -d ';'\n"
            "  cat datos.json | python json2csv.py -o salida.csv\n"
            "  cat datos.json | python json2csv.py\n"
        ),
    )

    parser.add_argument(
        "-i",
        "--input",
        dest="input_file",
        required=False,
        default=None,
        help="Archivo JSON de entrada (si se omite, se utiliza la entrada estándar).",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_file",
        required=False,
        default=None,
        help="Archivo CSV resultante (si se omite, se utiliza la salida estándar).",
    )
    parser.add_argument(
        "-d",
        "--delimiter",
        dest="delimiter",
        required=False,
        default=",",
        help="Delimitador de campos para el formato CSV (por defecto: ',').",
    )

    return parser.parse_args(argumentos)


def main() -> None:
    """Punto de entrada principal para la ejecución por consola."""
    args = parsear_argumentos()
    codigo_salida = ejecutar_filtro(
        archivo_entrada=args.input_file,
        archivo_salida=args.output_file,
        delimitador=args.delimiter,
    )
    sys.exit(codigo_salida)


if __name__ == "__main__":
    main()
