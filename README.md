# TP11 - Gestión de Calidad (Ingeniería de Software II)

![CI Pipeline](https://github.com/jenarogaldini/TP11---IS2/actions/workflows/ci.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)
![Coverage](https://img.shields.io/badge/coverage-92%25-brightgreen)
![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)
![Linter](https://img.shields.io/badge/linter-ruff-orange)
![Security](https://img.shields.io/badge/security-bandit-yellow)
![License](https://img.shields.io/badge/license-MIT-green)

Este repositorio contiene la resolución integral del **Trabajo Práctico Nº 11: Gestión de Calidad** de la cátedra de **Ingeniería de Software II** (Facultad de Ciencia y Tecnología - Universidad Autónoma de Entre Ríos).

---

## Estructura del Proyecto

```text
TP11---IS2/
├── .github/
│   └── workflows/
│       └── ci.yml             # Pipeline de Integración Continua (GitHub Actions)
├── docs/                      # Documentación HTML generada con pdoc
├── samples/
│   └── collatz_original.py    # Código original defectuoso analizado en inspección
├── src/
│   ├── collatz/
│   │   ├── __init__.py
│   │   └── collatz.py         # Implementación verificada y robusta de Collatz
│   └── json2csv/
│       ├── __init__.py
│       └── converter.py       # Núcleo de conversión con estrategia de filtro
├── tests/
│   ├── test_collatz.py        # Pruebas unitarias (caja blanca) y funcionales (caja negra)
│   └── test_json2csv.py       # Pruebas unitarias y funcionales del conversor JSON->CSV
├── json2csv.py                # Punto de entrada de línea de comandos (CLI)
├── pyproject.toml             # Configuración centralizada de herramientas de calidad
├── REQUIREMENTS.TXT           # Requerimientos para recrear el entorno
├── requirements.txt           # Dependencias de paquetes Python
├── VERSION                    # Registro semántico de versión (1.0.0)
├── BUILD                      # Registro de número de build
├── CONTEXT.md                 # Registro de prompts de IA
├── CHANGELOG.md               # Historial de cambios (Keep a Changelog)
├── LICENSE                    # Licencia MIT
└── README.md                  # Este documento
```

---

## 1. Módulos Desarrollados

### A. Algoritmo y Verificación de la Conjetura de Collatz
- **Función Matemática:** Implementa la conjetura $3n + 1$ para enteros positivos en el rango $[1, 1999]$.
- **Validaciones:** Control de tipos estrictos, manejo de cotas superior e inferior, y prevención de bucles infinitos.
- **Entrada/Salida:** Función de consola amigable e interactiva.

### B. Herramienta de Conversión `json2csv.py`
Filtro de conversión de archivos en formato JSON hacia CSV.

**Formato de ejecución:**
```bash
python json2csv.py {-i input.txt} {-o output.txt} {-d delimitador}
```

**Características principales:**
- **Estrategia de Filtro:** Si se omite `-i`, lee desde `stdin`. Si se omite `-o`, emite por `stdout`.
- **Delimitador Configurable:** Delimitador por defecto `,` (coma), modificable mediante `-d` (ej: `;`, `\t`, `|`).
- **Aplanamiento Jerárquico:** Transforma diccionarios anidados en claves con notación de punto (ej: `usuario.direccion.ciudad`).
- **Manejo Robusto:** Captura `FileNotFoundError`, `PermissionError`, `json.JSONDecodeError` y `ValueError` retornando códigos de salida diferenciados y mensajes claros por `stderr`.

---

## 2. Instalación y Entorno de Desarrollo

Se requiere **Python 3.10+**.

```bash
# 1. Clonar el repositorio
git clone https://github.com/jenarogaldini/TP11---IS2.git
cd TP11---IS2

# 2. Crear y activar el entorno virtual
python -m venv venv
# En Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# En Linux/macOS:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

---

## 3. Calidad y Quality Gates

El proyecto cumple de forma estricta con los siguientes controles de calidad:

| Control / Herramienta | Propósito | Estado |
| :--- | :--- | :---: |
| **`pytest`** | Pruebas unitarias y funcionales (42 tests) | **PASSED** (100%) |
| **`pytest-cov`** | Cobertura de código fuente | **92%** ($\ge 85\%$) |
| **`black`** | Formateador consistente de código | **PASSED** (0 dif) |
| **`ruff`** | Linter y verificación de reglas de estilo | **PASSED** (0 errores) |
| **`flake8`** | Verificación de reglas de formateo PEP 8 | **PASSED** (0 errores) |
| **`pydocstyle`** | Verificación de docstrings bajo PEP 257 | **PASSED** (0 errores) |
| **`mypy`** | Chequeo estático de tipos | **PASSED** (0 errores) |
| **`pyright`** | Análisis de tipos estáticos | **PASSED** (0 errores) |
| **`bandit`** | Análisis estático de seguridad (SAST) | **PASSED** (0 issues) |
| **`pdoc`** | Autogeneración de documentación HTML | **PASSED** |

### Ejecución manual de verificaciones:

```bash
# Ejecutar suite de pruebas con cobertura
pytest tests/ -v --cov=src --cov=json2csv

# Verificación de linter y formato
ruff check json2csv.py src/ tests/
black --check --exclude "collatz_original\.py" json2csv.py src/ tests/
flake8 --max-line-length=88 --extend-ignore=E203,W503 --exclude="venv,src/collatz/collatz_original.py,scratch" json2csv.py src/ tests/
pydocstyle --match='(?!collatz_original).*\.py' json2csv.py src/ tests/

# Análisis estático de tipos
mypy json2csv.py src/
pyright json2csv.py src/collatz/collatz.py src/json2csv/

# Evaluación de seguridad
bandit -r json2csv.py src/ -x src/collatz/collatz_original.py

# Generación de documentación HTML
pdoc -o docs/ src.json2csv src.collatz json2csv
```

---

## 4. Ejemplos de Uso de `json2csv.py`

### Entrada y Salida por Archivos:
```bash
python json2csv.py -i datos.json -o datos.csv
```

### Delimitador Personalizado (Punto y coma):
```bash
python json2csv.py -i datos.json -o datos.csv -d ";"
```

### Uso como Filtro de Tubería (Pipes):
```bash
cat datos.json | python json2csv.py > salida.csv
```

---

## 5. Integración Continua (CI/CD)

El archivo `.github/workflows/ci.yml` automatiza en cada *push* o *Pull Request*:
1. Configuración de matriz de versiones de Python.
2. Instalación de dependencias desde `requirements.txt`.
3. Ejecución de `ruff`, `black`, `flake8`, `pydocstyle`, `mypy`, `pyright`.
4. Ejecución de pruebas unitarias y cálculo de cobertura con `pytest`.
5. Escaneo de vulnerabilidades con `bandit`.
6. Generación y actualización de la documentación con `pdoc`.

---

## 6. Licencia

Este proyecto está bajo la Licencia **MIT** - consulte el archivo [LICENSE](LICENSE) para más detalles.