---
description: Build type-safe parameterized classes with Param for reactive dependencies, validation, and auto-generated UIs
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Parameterization

Build parameterized classes with Param for type-safe configuration and reactive UIs.

## Arguments

$ARGUMENTS — describe the need (e.g., "parameterized data filter class", "reactive config with validation", "auto-generate UI from parameters")

## Workflow

1. **Understand the requirements:**
   - Parameters needed (types, ranges, defaults)
   - Dependencies between parameters
   - Validation rules
   - Whether a Panel UI is needed

2. **Design the Parameterized class:**
   - Choose parameter types (Number, String, Selector, List, etc.)
   - Define bounds, default values, and documentation
   - Plan `@param.depends` reactive dependencies
   - Design watchers for side effects

3. **Implement** using Param:
   - Create `param.Parameterized` subclass
   - Define parameters with proper types and constraints
   - Add dependent methods with `@param.depends`
   - Add watchers with `param.watch` for side effects
   - Optionally auto-generate Panel UI with `.panel()`

4. **Report** the code with usage examples.
