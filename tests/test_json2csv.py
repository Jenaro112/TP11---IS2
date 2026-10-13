"""Tests unitarios y funcionales para el conversor json2csv."""

import io
import json
import os
import tempfile

import pytest

from json2csv import main, parsear_argumentos
from src.json2csv.converter import (
    aplanar_diccionario,
    ejecutar_filtro,
    json_a_csv_stream,
    normalizar_datos_json,
    obtener_encabezados,
)

# ============================================================================
# Pruebas Unitarias de Funciones Auxiliares
# ============================================================================


def test_aplanar_diccionario_simple():
    """Verifica el aplanamiento de un diccionario plano."""
    datos = {"id": 1, "nombre": "Alice"}
    assert aplanar_diccionario(datos) == {"id": 1, "nombre": "Alice"}


def test_aplanar_diccionario_anidado():
    """Verifica el aplanamiento recursivo de estructuras anidadas."""
    datos = {
        "id": 10,
        "usuario": {"nombre": "Bob", "direccion": {"ciudad": "Paraná", "cp": "3100"}},
        "etiquetas": ["admin", "staff"],
    }
    esperado = {
        "id": 10,
        "usuario.nombre": "Bob",
        "usuario.direccion.ciudad": "Paraná",
        "usuario.direccion.cp": "3100",
        "etiquetas": '["admin", "staff"]',
    }
    assert aplanar_diccionario(datos) == esperado


def test_normalizar_datos_objeto_unico():
    """Verifica que un único objeto se normalice como una lista de 1 elemento."""
    datos = {"a": 1, "b": 2}
    normalizado = normalizar_datos_json(datos)
    assert len(normalizado) == 1
    assert normalizado[0] == {"a": 1, "b": 2}


def test_normalizar_datos_lista_objetos():
    """Verifica normalización de lista de objetos heterogéneos."""
    datos = [{"a": 1}, {"b": 2}, {"a": 3, "b": 4}]
    normalizado = normalizar_datos_json(datos)
    assert len(normalizado) == 3
    assert normalizado[0] == {"a": 1}
    assert normalizado[1] == {"b": 2}
    assert normalizado[2] == {"a": 3, "b": 4}


def test_normalizar_datos_lista_primitivos():
    """Verifica normalización de lista con valores primitivos."""
    datos = [10, 20, 30]
    normalizado = normalizar_datos_json(datos)
    assert normalizado == [{"valor": 10}, {"valor": 20}, {"valor": 30}]


def test_normalizar_datos_tipo_invalido():
    """Verifica que tipos no soportados arrojen ValueError."""
    with pytest.raises(ValueError, match="Tipo de estructura JSON no soportada"):
        normalizar_datos_json("texto_plano")


def test_obtener_encabezados_orden_y_unicidad():
    """Verifica que los encabezados preserven el orden de aparición sin duplicados."""
    filas = [{"x": 1, "y": 2}, {"y": 3, "z": 4}, {"w": 5, "x": 6}]
    encabezados = obtener_encabezados(filas)
    assert encabezados == ["x", "y", "z", "w"]


# ============================================================================
# Pruebas de json_a_csv_stream
# ============================================================================


def test_stream_conversion_valida():
    """Verifica la conversión en streaming con delimitador estándar."""
    json_str = json.dumps([{"id": 1, "nombre": "Juan"}, {"id": 2, "nombre": "Ana"}])
    entrada = io.StringIO(json_str)
    salida = io.StringIO()

    total = json_a_csv_stream(entrada, salida, delimitador=",")
    assert total == 2
    contenido = salida.getvalue()
    assert "id,nombre\n" in contenido
    assert "1,Juan\n" in contenido
    assert "2,Ana\n" in contenido


def test_stream_delimitador_personalizado():
    """Verifica la conversión con delimitador ';' o tabulación."""
    json_str = json.dumps([{"colA": "1", "colB": "2"}])
    entrada = io.StringIO(json_str)
    salida = io.StringIO()

    json_a_csv_stream(entrada, salida, delimitador=";")
    assert salida.getvalue() == "colA;colB\n1;2\n"


def test_stream_delimitador_invalido():
    """Verifica error ante delimitador de longitud distinta a 1."""
    entrada = io.StringIO("[]")
    salida = io.StringIO()
    with pytest.raises(ValueError, match="delimitador debe ser un único carácter"):
        json_a_csv_stream(entrada, salida, delimitador="")
    with pytest.raises(ValueError, match="delimitador debe ser un único carácter"):
        json_a_csv_stream(entrada, salida, delimitador=",,")


def test_stream_entrada_vacia():
    """Verifica que una entrada vacía retorne 0 filas sin fallar."""
    entrada = io.StringIO("   \n")
    salida = io.StringIO()
    assert json_a_csv_stream(entrada, salida) == 0
    assert salida.getvalue() == ""


def test_stream_lista_vacia():
    """Verifica que una lista JSON vacía '[]' retorne 0 filas."""
    entrada = io.StringIO("[]")
    salida = io.StringIO()
    assert json_a_csv_stream(entrada, salida) == 0


def test_stream_json_malformado():
    """Verifica que un JSON sintácticamente incorrecto lance JSONDecodeError."""
    entrada = io.StringIO("{id: 1, incompleto")
    salida = io.StringIO()
    with pytest.raises(json.JSONDecodeError):
        json_a_csv_stream(entrada, salida)


def test_stream_con_bom_utf8():
    r"""Verifica que el BOM UTF-8 estándar \ufeff sea eliminado sin error."""
    entrada = io.StringIO('\ufeff[{"id": 1, "nombre": "Test"}]')
    salida = io.StringIO()
    filas = json_a_csv_stream(entrada, salida)
    assert filas == 1
    assert "id,nombre\n" in salida.getvalue()


def test_stream_con_bom_ansi_powershell():
    """Verifica que el BOM de PowerShell decodificado en ANSI sea procesado."""
    entrada = io.StringIO('\xef\xbb\xbf[{"id": 1, "nombre": "Test"}]')
    salida = io.StringIO()
    filas = json_a_csv_stream(entrada, salida)
    assert filas == 1
    assert "id,nombre\n" in salida.getvalue()


# ============================================================================
# Pruebas de ejecutar_filtro (archivos reales y códigos de salida)
# ============================================================================


def test_ejecutar_filtro_archivos_exitoso():
    """Verifica conversión leyendo y escribiendo en archivos temporales."""
    datos = [{"codigo": "A1", "precio": 100}, {"codigo": "B2", "precio": 250}]
    with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as f_in:
        json.dump(datos, f_in)
        ruta_in = f_in.name

    with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as f_out:
        ruta_out = f_out.name

    try:
        ret = ejecutar_filtro(ruta_in, ruta_out, delimitador=",")
        assert ret == 0
        with open(ruta_out, "r", encoding="utf-8") as f_res:
            lineas = f_res.readlines()
        assert lineas[0] == "codigo,precio\n"
        assert lineas[1] == "A1,100\n"
        assert lineas[2] == "B2,250\n"
    finally:
        if os.path.exists(ruta_in):
            os.remove(ruta_in)
        if os.path.exists(ruta_out):
            os.remove(ruta_out)


def test_ejecutar_filtro_archivo_no_encontrado(capsys):
    """Verifica manejo de FileNotFoundError."""
    ret = ejecutar_filtro("archivo_inexistente_123456.json", None)
    assert ret == 1
    err = capsys.readouterr().err
    assert "No se encontró el archivo de entrada" in err


def test_ejecutar_filtro_json_invalido(capsys):
    """Verifica captura de json.JSONDecodeError."""
    with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as f_in:
        f_in.write("{invalido}")
        ruta_in = f_in.name
    try:
        ret = ejecutar_filtro(ruta_in, None)
        assert ret == 3
        err = capsys.readouterr().err
        assert "Formato JSON inválido" in err
    finally:
        if os.path.exists(ruta_in):
            os.remove(ruta_in)


def test_ejecutar_filtro_delimitador_invalido(capsys):
    """Verifica captura de ValueError por delimitador inválido."""
    with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as f_in:
        f_in.write("[]")
        ruta_in = f_in.name
    try:
        ret = ejecutar_filtro(ruta_in, None, delimitador="invalido")
        assert ret == 4
        err = capsys.readouterr().err
        assert "Error de valor" in err
    finally:
        if os.path.exists(ruta_in):
            os.remove(ruta_in)


# ============================================================================
# Pruebas del CLI y argumentos
# ============================================================================


def test_parsear_argumentos_defaults():
    """Verifica argumentos por defecto."""
    args = parsear_argumentos([])
    assert args.input_file is None
    assert args.output_file is None
    assert args.delimiter == ","


def test_parsear_argumentos_completos():
    """Verifica parseo con -i, -o, -d."""
    args = parsear_argumentos(["-i", "entrada.json", "-o", "salida.csv", "-d", ";"])
    assert args.input_file == "entrada.json"
    assert args.output_file == "salida.csv"
    assert args.delimiter == ";"


def test_main_cli_ejecucion(monkeypatch):
    """Verifica que main() invoque correctamente ejecutar_filtro y sys.exit."""
    monkeypatch.setattr("sys.argv", ["json2csv.py", "--help"])
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 0
