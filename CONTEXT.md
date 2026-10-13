# Registro de Prompts de Inteligencia Artificial (CONTEXT.md)

Este documento registra los prompts e interacciones con herramientas de Inteligencia Artificial utilizadas durante el ciclo de vida del Trabajo Práctico Nº 11 - Gestión de Calidad (Ingeniería de Software II), dando cumplimiento al requerimiento **(c)** de las especificaciones de entrega.

---

## 1. Contexto General y Propósito
El desarrollo asistido por IA tuvo como finalidad:
1. Diseñar y estructurar la suite de verificación y validación (V&V) del algoritmo de Collatz (inspección de código, casos de prueba unitarios de caja blanca y funcionales de caja negra).
2. Desarrollar la herramienta de filtrado y conversión `json2csv.py` bajo estándares de arquitectura limpia y manejo robusto de excepciones.
3. Asegurar el cumplimiento de puertas de calidad (*Quality Gates*): formateo con `black`, linter con `ruff`, cumplimiento de `PEP8` y `PEP257`, tipado estático con `mypy` y `pyright`, pruebas automatizadas con `pytest` ($\ge 85\%$ de cobertura) y análisis estático de seguridad con `bandit`.

---

## 2. Registro de Prompts Utilizados

### Prompt 1: Análisis Integral de Requerimientos del TP11
- **Fecha:** 2026-10-13
- **Herramienta:** Asistente IA Antigravity (Google DeepMind - Gemini 3.8 Flash High)
- **Prompt:**
  > *"necesito que leas Pdf/IS2_TP11_Gestión de Calidad.pdf exhaustivamente y decirme si necesitas algo mas para realizarlo, caso contrario, haz todo lo que te pida el pdf, pero anda punto por punto, asi me explicas como funciona y que es lo que hiciste. tambien quiero que, a parte de todo y que no se suba ni al github ni al changelog, un archivo en .md para entregar el proyecto, podes usar latex o lo que creas necesario, pero solo hazmelo cuando este finalizado todo"*
- **Resultado Obtenido:**
  - Lectura completa y extracción OCR de las 5 páginas del PDF del trabajo práctico.
  - Verificación de la disponibilidad de todos los materiales necesarios (código Collatz, notebook `Taller_Defectos.ipynb`, referencias teóricas de Mendarozqueta y Colla).
  - Planificación exhaustiva de la resolución punto por punto.

---

### Prompt 2: Estructuración de Requerimientos y Casos de Prueba de Collatz
- **Herramienta:** Asistente IA Antigravity
- **Prompt:**
  > *"Estructura los requerimientos funcionales R={R1,...,Rn} y no funcionales F={F1,...,Fm} para el algoritmo de Collatz especificado en el PDF. Diseña el conjunto de casos de prueba T={T1,...,Tn} dividiéndolos en pruebas unitarias (caja blanca) y pruebas funcionales (caja negra), y establece la matriz de trazabilidad RTMX validando la cobertura del 100%."*
- **Resultado Obtenido:**
  - Definición formal de 6 requerimientos funcionales ($R_1$ a $R_6$) y 5 requerimientos no funcionales ($F_1$ a $F_5$).
  - Formulación de 10 casos de prueba ($T_1$ a $T_5$ unitarios; $T_6$ a $T_{10}$ funcionales).
  - Construcción de la matriz RTMX con integridad completa bidireccional.

---

### Prompt 3: Implementación de la Herramienta `json2csv.py`
- **Herramienta:** Asistente IA Antigravity
- **Prompt:**
  > *"Desarrolla la herramienta en Python `json2csv.py` implementando una estrategia de filtro orientada a flujo. Debe soportar la ejecución `python json2csv.py {-i input.txt} {-o output.txt} {-d delimitador}`. Si falta -i lee de stdin, si falta -o escribe en stdout, delimitador por defecto ','. Debe aplanar diccionarios anidados, normalizar registros heterogéneos y capturar robustamente excepciones (FileNotFoundError, PermissionError, JSONDecodeError, ValueError). Incluye anotaciones de tipos completas y docstrings bajo convención PEP 257."*
- **Resultado Obtenido:**
  - Creación del módulo central `src/json2csv/converter.py` y del script de entrada `json2csv.py`.
  - Soporte completo para flujos interactivos o redirigidos (`sys.stdin` / `sys.stdout`).
  - Cumplimiento estricto de tipado y convenciones de documentación.

---

### Prompt 4: Configuración de CI/CD, Linters y Quality Gates
- **Herramienta:** Asistente IA Antigravity
- **Prompt:**
  > *"Configura el pipeline de calidad para el proyecto: crea pyproject.toml con exclusiones y reglas para ruff, black, mypy, pyright y pytest. Escribe pruebas exhaustivas con pytest cubriendo más del 85% del código. Ejecuta ruff, black, flake8, pydocstyle, mypy, pyright y bandit asegurando 0 errores. Automatiza todo en un workflow de GitHub Actions (.github/workflows/ci.yml) incluyendo la generación de documentación con pdoc."*
- **Resultado Obtenido:**
  - Cobertura de pruebas unitarias y funcionales alcanzada: **92%** (42 tests pasando).
  - 0 errores en `ruff`, `black`, `flake8` (PEP 8), `pydocstyle` (PEP 257), `mypy`, `pyright` y `bandit`.
  - Workflow de CI/CD `.github/workflows/ci.yml` configurado y validado.
