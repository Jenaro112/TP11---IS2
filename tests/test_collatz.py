"""Tests unitarios y funcionales para la conjetura de Collatz."""

import pytest

from src.collatz.collatz import collatz, procesar_entrada

# ============================================================================
# Pruebas Unitarias (Caja Blanca)
# ============================================================================


def test_t1_frontera_minima():
    """T1: Caso num = 1 (bucle termina inmediatamente con 0 iteraciones)."""
    assert collatz(1) == 0


def test_t2_par_inmediato():
    """T2: Caso num = 2 (rama par única, 2 -> 1 en 1 iteración)."""
    assert collatz(2) == 1


def test_t3_impar_pequeno():
    """T3: Caso num = 3 (rama impar y pares sucesivos: 3->10->5->16->8->4->2->1)."""
    assert collatz(3) == 7


def test_t4_ejemplo_original():
    """T4: Caso num = 20 (caso de prueba del enunciado original)."""
    assert collatz(20) == 7


def test_t5_limite_maximo():
    """T5: Caso num = 1999 (límite superior de cálculo válido)."""
    assert collatz(1999) == 50


# ============================================================================
# Pruebas Funcionales (Caja Negra)
# ============================================================================


def test_t6_funcional_normal():
    """T6: Proceso de entrada normal con valor 20."""
    num, iters = procesar_entrada("20")
    assert num == 20
    assert iters == 7


def test_t7_funcional_frontera_min():
    """T7: Proceso de entrada con frontera mínima '1'."""
    num, iters = procesar_entrada("1")
    assert num == 1
    assert iters == 0


def test_t8_funcional_frontera_max():
    """T8: Proceso de entrada con frontera máxima '1999'."""
    num, iters = procesar_entrada("1999")
    assert num == 1999
    assert iters == 50


@pytest.mark.parametrize("valor_invalido", ["0", "-1", "-20", "2000", "5000"])
def test_t9_funcional_fuera_de_rango(valor_invalido):
    """T9: Entradas numéricas fuera del rango permitido [1, 1999]."""
    with pytest.raises(ValueError, match="rango de 1 a 1999"):
        procesar_entrada(valor_invalido)


@pytest.mark.parametrize("texto_invalido", ["abc", "12.5", "", "  ", "None", "!#"])
def test_t10_funcional_no_numerico(texto_invalido):
    """T10: Entradas que no son números enteros válidos."""
    with pytest.raises(ValueError, match="valor numérico entero válido"):
        procesar_entrada(texto_invalido)


def test_tipo_invalido():
    """Verifica que tipos booleanos o no enteros arrojen TypeError."""
    with pytest.raises(TypeError):
        collatz(True)
    with pytest.raises(TypeError):
        collatz("10")  # type: ignore


def test_main_exitoso(monkeypatch, capsys):
    """Prueba la función main con entrada válida."""
    from src.collatz.collatz import main

    monkeypatch.setattr("builtins.input", lambda _: "20")
    main()
    captured = capsys.readouterr()
    assert "El número de partida es 20 y el número de iteraciones es 7" in captured.out


def test_main_error(monkeypatch, capsys):
    """Prueba la función main con entrada errónea."""
    from src.collatz.collatz import main

    monkeypatch.setattr("builtins.input", lambda _: "abc")
    main()
    captured = capsys.readouterr()
    assert "Error:" in captured.out
