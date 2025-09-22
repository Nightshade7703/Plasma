# Plasma

Plasma is a staticlly-typed variant of Python designed to combine Python's readable, indentation-based syntax with C-style type declarations for variables and functions. Unlike Python, Plasma omits the `def` keyword for function declarations and enforces static typing to enable performance optimizations and early error detection. In its prototyping phase, Plasma compiles `.pls` files to Python `.py` files, similar to how TypeScript compiles to JavaScript. In later stages, Plasma will run in its own dedicated interpreter for greater control and performance.

## Features

- **C-Style Typing**: Declare variables with `type var = value;` (e.g., `int x = 42;`) and functions with `return_type func_name(param_type param, ...)`.
- **Python-Like Indentation**: Retains Python's indentation-based block structure for clean, readable code.
- **Static Type Checking**: Enforces type safety at compile time to catch errors early.
- **Compilation to Python**: In the prototyping phase, `.pls` files are compiled to `.py` files for execution with Python's interpreter.
- **Future Interpreter**: Planned dedicated interpreter for optimized execution independent of Python.

## Example

```plasma
int x = 42;

float add(int a, int b):
    return a + b;
```

Compiles to:
```python
x = 42

def add(a, b):
    return a + b
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip for installing dependencies

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Nightshade7703/Plasma.git
   cd plasma
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv  # Use 'python3' if 'python' is not recognized
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

- Compile a `.pls` file to Python:
  ```bash
  python -m plasma compile example.pls
  ```
  This generates `example.py`, which can be run with:
  ```bash
  python example.py
  ```
- Run tests:
  ```bash
  pytest
  ```

## Project Structure

- `plasma/`: Core compiler code (parser, type checker, code generator).
- `tests/`: Unit tests for the compiler.
- `examples/`: Sample `.pls` files demonstrating Plasma's syntax.
- `requirements.txt`: Python dependencies for development.

## Development

To contribute to Plasma:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

### Roadmap

- **Phase 1 (Prototyping)**: Complete the `.pls`-to-`.py` compiler with full type checking.
- **Phase 2**: Develop a tree-walking interpreter for Plasma.
- **Phase 3**: Implement a bytecode-based interpreter with optimizations.
- **Phase 4**: Build a standard library and IDE integration (e.g., LSP support).

## License

MIT License. See [LICENSE](LICENSE) for details.

## Contact

For questions or feedback, open an issue or reach out on [Twitter](https://x.com/Enderbyte7703)
