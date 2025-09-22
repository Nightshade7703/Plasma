# Contributing to Plasma

Thank you for your interest in contributing to Plasma! Plasma is a statically-typed Python variant designed to combine Python's readability with C-style typing and a future dedicated interpreter. We welcome contributions from the community to help advance the project.

## Getting Started

1. **Fork the Repository**: Fork the Plasma repository on GitHub.
2. **Clone Your Fork**:
   ```bash
   git clone https://github.com/Nightshade7703/Plasma.git
   cd Plasma
   ```
3. **Set Up the Environment**:
   - Ensure Python 3.8 or higher is installed.
   - Create a virtual environment:
     ```bash
     python -m venv venv  # Use 'python3' if 'python' is not recognized
     source venv/bin/activate  # On Windows: venv/Scripts/activate
     ```
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
4. **Run Tests**:
   ```bash
   pytest
   ```
   Ensure all tests pass before making changes.

## Development Workflow

1. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
   Use descriptive branch names (e.g., `feature/add-genarics`, `bugfix/parser-error`).
2. **Make Changes**:
   - Follow the coding style (see below).
   - Update tests in the `tests/` directory to cover your changes.
   - Add or update `.pls` files in the `examples/` directory if relevant.
3. **Commit Changes**:
   - Write clear, concise commit messages (e.g., `Add support for elif in parser`).
   - Use `git commit -m "Your message"`.
4. **Push to Your Fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Open a Pull Request**:
   - Go to the Plasma repository on GitHub and create a pull request from your branch.
   - Describe your changes, referencing any related issues.
   - Ensure your PR passes CI checks (e.g., tests, linting).

## Coding Style

- **Python Code**:
  - Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code in the `plasma/` and `tests/` directories.
  - Use type hints where applicable.
  - Write docstrings for public functions and classes.
- **Plasma Code** (in `examples/`):
  - Use C-style typing (e.g., `int x = 42;`).
  - Use colons for blocks (e.g., `if x > 0:`).
  - End statements with semicolons where required (e.g., variable declarations, return statements).
- **File Formatting**:
  - Use 4-space indentation for Python and Plasma code.
  - Ensure files end with a newline.

## Testing

- Add unit tests for new features in `tests/`.
- Use `pytest` for testing (e.g., `pytest tests/test_parser.py`).
- Test cases should cover:
  - Parsing (valid and invalid `.pls` syntax).
  - Type checking (e.g., type mismatches).
  - Code generation (correct `.py` output).
- Ensure 100% test coverage for new code.

## Documentation

- Update `docs/language_spec.md` for changes to Plasma's syntax or semantics.
- Update `docs/README.md` if you modify setup or usage instructions.
- Add comments in code for complex logic.
- If adding new features, provide example `.pls` files in `examples/`.

## Contribution Areas

- **Parser**: Improve the `lark` grammar in `plasma/compiler/plasma.ebnf` or parsing logic in `parser.py`.
- **Type Checker**: Enhance type checking in `type_checker.py` (e.g., add support for new types).
- **Code Generator**: Optimize Python code generation in `codegen.py`.
- **CLI**: Add features to the command-line interface in `cli.py` (e.g., new commands, better error messages).
- **Tests**: Expand test coverage in `tests/`.
- **Examples**: Create new `.pls` files in `examples/` to showcase features.
- **Documentation**: Improve `docs/` or add tutorials.

## Code of Conduct

Be respective and inclusive in all interactions. Follow the [Contributor Covenant](https://www.contributor-covenant.org/).

## Contact

For questionsk, open an issue on GitHub or reach out on [Twitter](https://x.com/Enderbyte7703).

Thank you for helping make Plasma better!
