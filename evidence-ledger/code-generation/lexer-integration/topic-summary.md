# Section 3.3: Lexer Integration — Topic Summary

## Purpose

Explain how Grammar-Kit integrates with JFlex for lexer generation: the token definition workflow, flex file generation, JFlex compilation, token mapping between parser and lexer, and IDE support for `.flex` files. Cover the practical steps a developer follows to go from grammar tokens to a working lexer.

## Audience

Plugin developers creating a lexer for the first time, and maintainers updating token definitions.

## Prerequisites

- Basic BNF grammar with token definitions (Section 2.1)
- Parser generation basics (Section 3.2)

## Structure

### H1: Lexer Integration

Opening paragraph: The parser generator produces IElementType constants that a lexer must recognize and return. Grammar-Kit integrates with JFlex to generate a lexer from the token definitions in your grammar. Outline the two-step process: generate flex file, then compile it.

### H2: Defining Tokens

Explain the `tokens` attribute and the three token categories:

1. Explicit tokens with patterns: `id='regexp:\w+'`
2. Explicit tokens with literal values: `PLUS='+'`
3. Implicit tokens: unquoted references in rules that are not rule names

Cover regexp token syntax. Note that text-matched tokens (quoted strings not in the `tokens` list) are slower.

Evidence: code-evidence.md sections 2, 12; examples.md examples 1, 6

### H2: Generating the Flex File

Explain the "Generate JFlex Lexer" action:

- Naming convention: `_<GrammarName>Lexer.flex`
- Output location (same directory as `.bnf` by default)
- Template-based generation using Velocity
- Structure of the generated flex file: imports, macros, rules
- Java regex to JFlex conversion (key mappings table)

Show a concrete generated flex file example.

Evidence: code-evidence.md sections 3, 4; examples.md examples 2, 3

### H2: Compiling the Lexer

Explain "Run JFlex Generator" action:

- Parses `%class` and `package` from the flex file
- Downloads JFlex jar if needed (from JetBrains cache)
- Uses `idea-flex.skeleton`
- Output shown in Messages tool window
- Token type configuration: `tokenTypeClass` vs `tokenTypeFactory`

Evidence: code-evidence.md sections 5, 11; examples.md example 4

### H2: JFlex IDE Support

Brief coverage of the IDE features Grammar-Kit provides for `.flex` files:

- Syntax highlighting, code completion, find usages
- Refactoring, structure view, brace matching
- Java code injection in action blocks

Note that the flex file is typically edited manually after initial generation for complex lexing logic.

Evidence: code-evidence.md sections 6, 7, 8

## Key Examples to Include

1. Token definitions in grammar (regexp + literal)
2. Generated flex file for a simple grammar
3. Java-to-JFlex regex conversion table
4. Token type configuration (class vs factory)
5. Explicit vs implicit token comparison

## Cross-References

- Section 2.1 (BNF Grammar Syntax) for token definition syntax
- Section 3.2 (Parser Generation) for element types holder
- Section 4.2 (Build Integration) for Gradle lexer generation
- JFlex documentation (external link)

## Writing Notes

- Emphasize the two-step workflow: generate flex, then compile
- The generated flex file is a starting point -- developers customize it
- Lead with the practical steps, not the implementation details
- Include the regex conversion table as a practical reference
- Keep JFlex IDE support section brief
