# Plasma Language Specification

## Overview

Plasma is a statically-typed variant of Python that combines Python's readable, indentation-based syntax with C-style type declarations for variables and functions. It omits the `def` keyword for function declarations and uses colons (`:`) to initiate blocks for functions, conditionals, and loops. Plasma enforces static typing to enable early error detection and performance optimizations. In its prototyping phase, Plasma compiles `.pls` files to Python `.py` files. Future phases will introduce a dedicated interpreter.

This document outlines the syntax and semantics of Plasma, focusing on the prototyping phase.

## Syntax

### Variable Declarations

Variables are declared with C-style typing using the format `type name = expression;`. Types are checked at compile time.

- **Syntax**: `type identifier = expression;`
- **Supported Types**: `int`, `float`, `str`, `bool`
- **Example**:
    ```pls
    int x = 42;
    float pi = 3.14;
    str greeting = "Hello";
    bool is_active = true;
    ```

### Function Declarations

Functions are declared without the `def` keyword, using C-style typing for return types and parameters, followed by a colon (`:`) and an indented block.

- **Syntax**: `return_type name(param_type param, ...): block`
- **Supported Types**: `int`, `float`, `str`, `bool`, `void`
- **Semantics**: Functions with `void` return type must not return a value or use a bare `return;`.
- **Example**:
    ```pls
    float add(int a, int b):
        return a + b;
    
    void print_message(str msg):
        print(msg);
    ```

### Control Structures

Control structures use colons (`:`) to initiate indented blocks, similar to Python.

#### If Statements

- **Syntax**: `if expression: block [elif expression: block]* [else: block]?`
- **Semantics**: The `expression` must evaluate to a `bool`. The first true branch is executed; otherwise the `else` branch (if present) is executed.
- **Example**:
    ```pls
    bool is_positive(int x):
        if x > 0:
            return true;
        elif x == 0:
            return false;
        else:
            return false;
    ```

#### While Loops

- **Syntax**: `while expression: block`
- **Semantics**: The `expression` must evaluate to a `bool`. The block is executed repeatedly while the expression is true.
- **Example**:
    ```pls
    int sum_to(int n):
        int total = 0;
        while n > 0:
            total = total + n;
            n = n - 1;
        return total;
    ```

#### For Loops

- **Syntax**: `for identifier in range(expression): block`
- **Semantics**: Iterates over a range of integers from 0 to `expression - 1`. The `expression` must evaluate to an `int`.
- **Example**:
    ```pls
    int sum_range(int n):
        int total = 0;
        for i in range(n):
            total = total + i;
        return total;
    ```

### Expressions

Expressions include literals, variables, operators, and function calls.

- **Literals**: `int` (e.g., `42`), `float` (e.g., `3.14`), `str` (e.g., `"hello"`), `bool` (`true`, `false`)
- **Operators**:
  - Arithmetic: `+`, `-`, `*`, `/`
  - Comparison: `==`, `!=`, `<`, `>`, `<=`, `>=`
- **Function Calls**: `name(arg, ...)`
- **Example**:
    ```pls
    int x = 42 + 8 * 2;  // Evaluates to 58
    bool eq = x == 58;    // true
    float result = add(10, 20);  // Calls add function
    ```

### Comments

Plasma supports C-style single-line comments starting with `//`.

- **Example**:
    ```pls
    // This is a comment
    int x = 42;  // Initialize x
    ```

## Semantics

- **Static Typing**: Types are checked at compile time. Type mismatches (e.g., `int x = "hello";`) result in compilation errors.
- **Type Inference**: Not supported in the prototyping phase; all variables and functions require explicit type declarations.
- **Block Scope**: Variables declared in a block are scoped to that block, similar to Python.
- **Compilation**: In the prototyping phase, `.pls` files are compiled to `.py` files, stripping type declarations and converting function headers to use `def`. For example:
    ```pls
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

## Future Features

- **Advanced Types**: Support for arrays, structs, or genarics.
- **Interpreter**: A tree-walking or bytecode-based interpreter for direct `.pls` execution.
- **Standard Library**: Functions for I/O, math, and data structures tailored to Plasma's type system.

## Example Program

```pls
int main():
    int x = 42;
    float sum = add(x, 10);
    bool pos = is_positive(x);
    int total = 0;
    for i in range(5):
        total = total + i;
    return total;

float add(int a, int b):
    return a + b;

bool is_positive(int x):
    if x > 0:
        return true;
    elif x == 0:
        return false;
    else:
        return false;
```

This specification will evolve as Plasma develops. Feedback is welcome via GitHub issues.
