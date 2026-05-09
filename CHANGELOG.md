# Changelog

## [0.1.0] - 2026-05-08

### 🎉 Initial Release: Notes CLI

A complete command-line interface for managing notes with tags, search capabilities, and persistent JSON storage.

---

## 📋 Features

### ✨ Three Core Commands

#### 1. **add-note** - Create Notes
Add new notes with optional tags and automatic timestamping.

```bash
# Add note with tag
mi-cli add-note "Prepare presentation" --tag work

# Add note without tag
mi-cli add-note "Remember to call mom"

# Short option
mi-cli add-note "Quick note" -t personal
```

**What it does:**
- Validates non-empty text (rejects whitespace-only input)
- Generates unique UUID v4 identifier
- Captures Unix timestamp automatically
- Stores in `~/.notes/notes.json`

#### 2. **list-notes** - Display Notes
List all notes with optional filtering by tag.

```bash
# List all notes
mi-cli list-notes

# Filter by tag
mi-cli list-notes --tag work

# Short option
mi-cli list-notes -t personal
```

**Output format:**
```
ID       | Texto                          | Tag        | Fecha
---------|--------------------------------|------------|-------------------
abc12345 | Prepare presentation           | work       | 2026-05-08 14:30:45
def67890 | Remember to call mom           | -          | 2026-05-07 09:15:30

Total: 2 notas
```

#### 3. **search-notes** - Find Notes
Search notes by text with case-insensitive matching.

```bash
# Basic search
mi-cli search-notes "python"

# Partial match (finds "testing" in text)
mi-cli search-notes "test"
```

**Output format:**
```
Búsqueda: "python"

ID       | Texto                          | Tag        | Fecha
---------|--------------------------------|------------|-------------------
ghi11111 | Python tips and tricks         | dev        | 2026-05-06 16:20:10
jkl22222 | Learning Python fundamentals   | learn      | 2026-05-05 11:45:00

Total: 2 resultados
```

---

## 🛠️ Technical Stack

- **Python:** 3.12
- **CLI Framework:** Click 8.1
- **Testing:** pytest 8.0 with CliRunner
- **Code Quality:** Ruff (linting & formatting)
- **Type Safety:** Full type hints throughout

---

## 📦 Storage

Notes are stored in `~/.notes/notes.json` with the following structure:

```json
{
  "notes": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "text": "My note text",
      "tag": "work",
      "timestamp": 1714070400.123456
    },
    {
      "id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
      "text": "Note without tag",
      "tag": null,
      "timestamp": 1714070400.654321
    }
  ]
}
```

---

## 🧪 Testing

**Complete test suite with 27 tests (100% passing):**

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_add_improved.py -v

# Run with short error output
pytest --tb=short
```

**Test Coverage:**
- **add-note:** 10 tests (validation, edge cases, UUID, timestamp)
- **list-notes:** 6 tests (empty list, filtering, options)
- **search-notes:** 6 tests (matching, case-insensitivity, partial match)
- **Legacy tests:** 5 tests (initial tests preserved)

**Testing Pattern:**
All modern tests use Click's `CliRunner` with the CLI group:

```python
from click.testing import CliRunner
from src.cli import cli

class TestAddCommand:
    def setup_method(self) -> None:
        self.runner = CliRunner()
    
    def test_add_basic_usage(self) -> None:
        result = self.runner.invoke(cli, ["add-note", "Test note"])
        assert result.exit_code == 0
        assert "Nota creada" in result.output
```

---

## 🚀 Getting Started

### Installation

```bash
# Clone the repository
git clone git@github.com:albertofragoso/my-cli-notes.git
cd my-cli-notes

# Install in development mode
pip install -e ".[dev]"

# Verify installation
mi-cli --version
```

### Quick Start

```bash
# Create a few notes
mi-cli add-note "First note" --tag important
mi-cli add-note "Python tips" --tag dev
mi-cli add-note "Quick reminder"

# List all notes
mi-cli list-notes

# Filter by tag
mi-cli list-notes --tag dev

# Search
mi-cli search-notes "python"

# View the storage file
cat ~/.notes/notes.json
```

---

## 📐 Architecture

```
src/
├── cli.py              # Entry point, registers all commands
├── utils.py            # Shared utilities (I/O, formatting, display)
└── commands/           # One file per command
    ├── add.py          # add-note command
    ├── list.py         # list-notes command
    └── search.py       # search-notes command

tests/
├── test_add.py         # Legacy tests
├── test_add_improved.py     # Modern CliRunner tests (10 tests)
├── test_list.py             # Modern CliRunner tests (6 tests)
└── test_search.py           # Modern CliRunner tests (6 tests)
```

---

## ✅ Quality Assurance

- **Type Safety:** Full type hints on all public functions
- **Error Handling:** Consistent use of `click.ClickException`
- **Code Style:** Enforced with ruff (check & format)
- **Testing:** 27 comprehensive tests with 100% pass rate
- **Documentation:** Complete CLAUDE.md with usage and conventions

---

## 📝 Development Commands

```bash
# Run tests
pytest

# Check code with ruff
ruff check src/

# Format code with ruff
ruff format src/

# Run tests with coverage info
pytest -v

# Clean test artifacts
rm -rf .pytest_cache __pycache__
```

---

## 🔄 What's Next?

Potential enhancements for future versions:
- Add note deletion functionality
- Export notes to different formats (CSV, Markdown)
- Implement note editing capability
- Add priority levels or categories
- Integration with external calendars
- Cloud synchronization
- Rich terminal UI with interactive selection

---

## 📄 License

MIT License - Feel free to use, modify, and distribute.

---

## 👤 Author

Alberto Fragoso - Initial implementation

---

**Built with Python, Click, and ❤️**
