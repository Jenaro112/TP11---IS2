# Changelog

Todos los cambios notables de este proyecto se documentan en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y este proyecto se adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [1.0.0] - 2026-10-13

### Añadido
- Módulo `src/collatz/collatz.py` con implementación robusta, validación de rango `[1, 1999]`, tipado estático y función interactiva por consola.
- Módulo `src/json2csv/converter.py` con arquitectura de filtro, soporte para flujos `sys.stdin`/`sys.stdout`, aplanamiento jerárquico recursivo de diccionarios JSON y manejo integral de excepciones.
- Punto de entrada CLI `json2csv.py` con argumentos opcionales `-i`, `-o` y `-d`.
- Suite exhaustiva de pruebas unitarias y funcionales en `tests/test_collatz.py` y `tests/test_json2csv.py` (42 pruebas, cobertura 92%).
- Configuración de herramientas de calidad en `pyproject.toml` para `ruff`, `black`, `mypy`, `pyright` y `pytest`.
- Documentación HTML autogenerada mediante `pdoc` en la carpeta `docs/`.
- Pipeline de Integración Continua (CI/CD) automatizado en GitHub Actions (`.github/workflows/ci.yml`).
- Registro de prompts de Inteligencia Artificial en `CONTEXT.md`.
- Registro formal de metadatos en archivos `VERSION` y `BUILD`.
- Listas de dependencias en `REQUIREMENTS.TXT` y `requirements.txt`.

### Corregido
- Defectos sintácticos de indentación y delimitadores de bloque en el código inicial de Collatz.
- Corrección de la referencia semántica inválida `return iter` por `return iteraciones`.
- Corrección de la variable no inicializada `j` en `collatz(j)`.
- Manejo seguro de archivos sin fugas de descriptores de entrada/salida.
