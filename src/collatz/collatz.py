"""Módulo para el cálculo de la conjetura de Collatz.

Este programa solicita un número entero positivo entre 1 y 1999,
calcula el número de iteraciones necesarias para alcanzar el valor 1
según las reglas de Collatz e imprime el número inicial y las iteraciones.
"""


def collatz(num: int) -> int:
    """Calcula el número de iteraciones de la conjetura de Collatz.

    Args:
        num (int): Número entero positivo de partida (1 <= num <= 1999).

    Returns:
        int: Número total de iteraciones hasta alcanzar el valor 1.

    Raises:
        ValueError: Si num no es un entero en el rango [1, 1999].
    """
    if not isinstance(num, int) or isinstance(num, bool):
        raise TypeError("El valor debe ser un número entero.")
    if num < 1 or num > 1999:
        raise ValueError("El número debe estar en el rango de 1 a 1999.")

    iteraciones = 0
    actual = num
    while actual != 1:
        if actual % 2 == 0:
            actual = actual // 2
        else:
            actual = 3 * actual + 1
        iteraciones += 1

    return iteraciones


def procesar_entrada(entrada_texto: str) -> tuple[int, int]:
    """Valida la entrada del usuario y calcula las iteraciones de Collatz.

    Args:
        entrada_texto (str): Texto ingresado por el usuario.

    Returns:
        Tuple[int, int]: Tupla con (número de partida, iteraciones).
    """
    try:
        num = int(entrada_texto.strip())
    except ValueError as exc:
        raise ValueError("Debe ingresar un valor numérico entero válido.") from exc

    iteraciones = collatz(num)
    return num, iteraciones


def main() -> None:
    """Función principal para la ejecución interactiva por consola."""
    try:
        texto = input("Ingrese un número entero positivo (1 a 1999): ")
        num, iters = procesar_entrada(texto)
        print(f"El número de partida es {num} y el número de iteraciones es {iters}")
    except (ValueError, TypeError) as err:
        print(f"Error: {err}")


if __name__ == "__main__":
    main()
