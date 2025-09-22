"""
Compiler components for Plasma: parser, type checker, and code generator.
"""
from .parser import PlasmaParser
from .type_checker import TypeChecker
from .codegen import CodeGenerator

__all__ = ["PlasmaParser", "TypeChecker", "CodeGenerator"]
# Exposes core compiler components for internal use or testing.
# Usage: `from plasma.compiler import PlasmaParser, TypeChecker, CodeGenerator`
