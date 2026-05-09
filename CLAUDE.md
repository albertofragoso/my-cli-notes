# MY CLI NOTES

CLI para agregar, listar y buscar notas. Herramienta de línea de comandos construida con Python y Click.

## Stack
- Python 3.12
- Click 8.1 (framework CLI)
- pytest 8.0 (testing)
- Ruff (linter y formatter)

## Estructura

src/
├── __init__.py
├── cli.py               → Entry point, registra todos los comandos
├── commands/            → Un archivo por comando
│   ├── __init__.py
│   ├── add.py          → Comando: mi-cli add-note [TEXTO] --tag TAG
│   ├── list.py         → Comando: mi-cli list-notes [--tag TAG]
│   └── search.py       → Comando: mi-cli search-notes [QUERY]
└── utils.py            → Funciones de utilidad (I/O, formateo, display)

tests/
├── __init__.py
├── test_add.py              → 5 tests básicos (legacy)
├── test_add_improved.py      → 10 tests con CliRunner (clase TestAddCommand)
├── test_list.py             → 6 tests con CliRunner (clase TestListCommand)
└── test_search.py           → 6 tests con CliRunner (clase TestSearchCommand)

## Testing

**Suite completa: 27 tests, 100% pasando**

```
Cobertura por comando:
- add-note:     10 tests (validación, edge cases, UUID, timestamp)
- list-notes:   6 tests (lista vacía, filtros, opciones)
- search-notes: 6 tests (búsqueda, case-insensitive, partial match)
- Legacy:       5 tests (tests iniciales)
```

**Patrón de tests:**
Todos los tests modernos usan CliRunner con el grupo cli:

```python
from click.testing import CliRunner
from src.cli import cli

class TestXyzCommand:
    def setup_method(self) -> None:
        self.runner = CliRunner()
    
    def test_scenario(self) -> None:
        """Descripción del test."""
        result = self.runner.invoke(cli, ["comando-name", "arg"])
        assert result.exit_code == 0
        assert "expected output" in result.output
```

**Ejecución de tests:**
```bash
pytest                    # Ejecutar todos (27 tests)
pytest -v               # Verbose
pytest tests/test_add_improved.py -v  # Tests específicos
pytest --tb=short       # Con output corto de errores
```

## Convenciones
- snake_case para archivos, funciones y variables.
- Type hints en todas las funciones públicas.
- Docstrings en funciones de comandos (se usan como help text).
- Click decorators para argumentos y opciones.
- click.echo para output formateado (NO print()).
- Manejo de errores con click.ClickException (NO sys.exit()).

## Comandos de Uso

```bash
# Crear una nota
mi-cli add-note "Mi nota de texto" --tag trabajo
mi-cli add-note "Nota sin etiqueta"

# Listar notas
mi-cli list-notes              # Todas las notas
mi-cli list-notes --tag trabajo   # Solo notas con tag 'trabajo'

# Buscar notas
mi-cli search-notes "palabra clave"  # Búsqueda case-insensitive
```

## Comandos de Desarrollo
- Instalar: `pip install -e ".[dev]"`
- Ejecutar CLI: `mi-cli [comando]` o `python -m src.cli [comando]`
- Test: `pytest`
- Test verbose: `pytest -v`
- Lint: `ruff check src/`
- Format: `ruff format src/`

## Reglas

### Código
- Cada comando en su propio archivo dentro de src/commands/.
- Todos los comandos se registran en src/cli.py con `cli.add_command()`.
- NO mezclar lógica de negocio con lógica de CLI (Click).
- Siempre incluir --help con descripción clara en docstrings.
- Manejo de errores con click.ClickException, no sys.exit().

### Testing
- Usar CliRunner para testear comandos (invocar grupo `cli`, no funciones directas).
- Estructura: clase `TestXyzCommand` con `setup_method()` que crea `self.runner`.
- Usar `tempfile` para datos temporales, `patch()` para mockear rutas.
- Limpiar con `finally` blocks (no pytest fixtures para modelos nuevos).
- Ejecutar `pytest` después de modificar comandos o utilidades.
- Docstrings en tests: descripción clara de lo que valida (acción + escenario).

## Storage
- Ubicación: `~/.notes/notes.json`
- Formato: JSON con estructura `{ "notes": [{ "id", "text", "tag", "timestamp" }] }`
- Creación automática del directorio en primer uso