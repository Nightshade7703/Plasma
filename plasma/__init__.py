"""
Plasma: A statically-typed Python variant with C-style typing and colon-based blocks.
Compiles .pls files to .py files in the prototyping phase.
"""
__version__ = "0.2.0"

from .compiler.cli import main as compile_plasma

__all__ = ["compile_plasma"]
# Exposes the CLI entry point for compiling .pls files.
# Usage: `from plasma import compile_plasma` or `python -m plasma compile example.pls`
