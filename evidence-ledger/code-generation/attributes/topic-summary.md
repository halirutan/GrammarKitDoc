# Section 3.1: Attributes System — Topic Summary

## Purpose

Explain how Grammar-Kit attributes control code generation, covering the three scope levels (global, rule, pattern), the consolidated `generate` attribute, and common configurations. This is an orientation and practical guide, not a complete reference (Section 6.1 covers that).

## Audience

Plugin developers configuring Grammar-Kit for the first time, and grammar maintainers adjusting generation behavior.

## Prerequisites

- Basic BNF grammar structure (Section 2.1)
- Understanding of Grammar-Kit's generation workflow (Section 3.2)

## Structure

### H1: Attributes System

Opening paragraph: Attributes control what Grammar-Kit generates and how. They appear in the grammar header block (`{ ... }`) and on individual rules. Introduce the three scope levels.

### H2: Scope and Placement

Explain global vs. rule-level vs. pattern-based attributes. Show grammar header block placement and rule-level inline syntax. Cover pattern-based application with regex. One example showing all three.

Evidence: code-evidence.md sections 2, 3

### H2: Common Configurations

Cover the most-used attributes grouped by purpose:

- Parser configuration: `parserClass`, `parserUtilClass`, `parserImports`
- PSI configuration: `psiPackage`, `psiImplPackage`, `psiClassPrefix`, `psiImplClassSuffix`, `psiImplUtilClass`, `psiVisitorName`
- Element types: `elementTypeHolderClass`, `elementTypePrefix`, `elementTypeClass`, `tokenTypeClass`
- Generation control: the `generate` attribute with its key-value options

Show Grammar-Kit's own grammar as a complete real-world example.

Evidence: code-evidence.md sections 1, 4, 5; examples.md examples 1, 2

### H2: Rule-Level Attributes

Cover the most important rule-level attributes briefly (detail is in other sections or the reference):

- `extends` and `implements` for PSI hierarchy (link to 3.4)
- `pin` and `recoverWhile` for error recovery (link to 2.4)
- `methods` and `mixin` for PSI customization (link to 3.4)
- `elementType` for type sharing/suppression
- `hooks` for whitespace binders
- `name`, `consumeTokenMethod`, `stubClass`

Evidence: code-evidence.md sections 6-18; examples.md examples 3-9

### H2: The `generate` Attribute

Dedicated section for the consolidated `generate` attribute. Explain it supersedes individual `generateXXX` attributes. Table of all options with defaults. Show practical example.

Evidence: code-evidence.md section 4; examples.md example 2

## Key Examples to Include

1. Complete grammar header (Grammar-Kit's own grammar)
2. Pattern-based attribute application
3. The `generate` attribute with multiple options
4. `elementType` sharing between rules

## Cross-References

- Section 2.4 (Error Recovery) for `pin`/`recoverWhile` detail
- Section 3.2 (Parser Generation) for generation process
- Section 3.4 (PSI Customization) for `extends`/`implements`/`mixin`/`methods`
- Section 6.1 (Attribute Reference) for complete catalog

## Writing Notes

- Keep this as a practical orientation, not exhaustive reference
- Group attributes by purpose, not alphabetically
- Use Grammar-Kit's own grammar as the primary example
- Mention defaults for the most important attributes
- Avoid repeating detail that belongs in specialized sections
