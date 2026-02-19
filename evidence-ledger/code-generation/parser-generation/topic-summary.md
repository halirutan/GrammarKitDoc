# Section 3.2: Parser Generation — Topic Summary

## Purpose

Explain how Grammar-Kit generates parser code from a BNF grammar: the trigger mechanism, what files are produced, how grammar constructs map to Java code, configuration options, and build integration. This is the central section for understanding the generation pipeline.

## Audience

Plugin developers who need to generate and integrate a parser, and build engineers setting up CI pipelines.

## Prerequisites

- Basic BNF grammar (Section 2.1)
- Attributes system overview (Section 3.1)

## Structure

### H1: Parser Generation

Opening paragraph: Grammar-Kit transforms BNF rules into a recursive-descent parser implemented as static Java methods. Describe the generation trigger (IDE action or command line) and the five output files.

### H2: Running the Generator

Cover the three ways to generate:

1. IDE action (Ctrl+Shift+G / Cmd+Shift+G) -- preferred
2. Command line (`java -jar grammar-kit.jar`)
3. Gradle plugin (with noted limitations: no method mixins, no two-pass)

Explain what happens: documents saved, target directory resolved from `parserClass`, background task runs, results reported.

Evidence: code-evidence.md sections 1, 12

### H2: Generated Files

Walk through the five file categories in generation order:

1. Parser class -- static methods for each rule
2. Element types holder -- IElementType constants, factory, optional token sets
3. PSI interfaces -- one per non-private, non-fake rule
4. PSI implementation classes -- one per interface
5. Visitor class -- if enabled

Explain the output directory structure (package-based). Show the element types holder example.

Evidence: code-evidence.md sections 3, 5; examples.md example 4

### H2: Grammar-to-Code Mapping

Show how BNF constructs translate to Java patterns:

- Sequence: short-circuit `&&` chain
- Ordered choice: fallthrough `if (!r)` chain
- Zero-or-more: `while(true)` loop
- Expression rules: Pratt parser with priority table

Show generated method naming: `rule_name`, `rule_name_0`, `rule_name_N1_N2`.

Evidence: code-evidence.md sections 4, 10; examples.md examples 1, 2, 3

### H2: Configuration

Cover key generation options:

- `generate` attribute options (java version, naming style, case, fqn, psi control)
- Variable naming styles (short/long/classic)
- Element type casing (UPPER/lower/as-is/camel)
- Class header customization

Brief table of most important GenOptions fields.

Evidence: code-evidence.md sections 6, 7, 8; examples.md examples 5, 7

## Key Examples to Include

1. Generated sequence rule code
2. Generated choice rule code
3. Expression parser priority table
4. Element types holder with factory
5. Command-line invocation

## Cross-References

- Section 3.1 (Attributes System) for configuration attributes
- Section 3.3 (Lexer Integration) for token type mapping
- Section 3.4 (PSI Customization) for PSI class details
- Section 4.2 (Build Integration) for Gradle setup detail

## Writing Notes

- Lead with the IDE workflow since that is the preferred path
- Show concrete generated code so readers know what to expect
- Keep Gradle section brief -- link to Section 4.2 for full details
- Mention the Gradle mixin limitation prominently
- Use "short" naming style in examples since it is the default
