# Google JavaScript Style Guide Summary

This document summarizes key rules and best practices from the Google JavaScript Style Guide.

## 1. Source File Organization

- **File Names:** Use `kebab-case.js`.
- **Imports:** Use ES6 modules (`import`/`export`). Group imports: standard, external, internal.

## 2. Language Rules

- **Strict Mode:** Always use `'use strict';` if not using ES6 modules.
- **Variable Declarations:** Use `const` by default. Use `let` only when necessary. Avoid `var`.
- **Arrow Functions:** Prefer arrow functions for anonymous functions and callbacks.
- **Equality:** Use `===` and `!==`.
- **Template Literals:** Use backticks `` ` `` for string interpolation and multi-line strings.

## 3. Style Rules

- **Indentation:** 2 spaces.
- **Line Length:** Maximum 80 characters (Google) / 100 characters (Project).
- **Semicolons:** Always use semicolons.
- **Quotes:** Use single quotes `'` for strings.
- **Braces:** Use K&R style braces (opening brace on the same line).

## 4. Naming Convention

- **Classes:** `PascalCase`.
- **Functions, Variables:** `camelCase`.
- **Constants:** `UPPER_SNAKE_CASE`.

## 5. Documentation

- **JSDoc:** Use `/** ... */` for public APIs.

**BE CONSISTENT.** Match existing code style.

*Source: [Google JavaScript Style Guide](https://google.github.io/styleguide/jsguide.html)*
