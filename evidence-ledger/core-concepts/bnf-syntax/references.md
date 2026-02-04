# References: BNF Grammar Syntax

## Scope Information
This validates references for section 2.1: BNF Grammar Syntax

## Internal Links
- Prerequisites: None (this is foundational)
- Related: `core-concepts/attributes` (Section 2.2)
- Related: `core-concepts/live-preview` (Section 2.3)
- Advanced: `parser-development/expression-parsing` (Section 3.2)
- Advanced: `code-generation/parser-generation` (Section 4.1)

## Code References
- BNF self-definition: `grammars/Grammar.bnf`
- Token definitions: `grammars/Grammar.bnf#L22-47`
- Rule syntax examples: `testData/livePreview/Json.bnf`
- Expression parsing: `testData/generator/ExprParser.bnf`
- External rules demo: `testData/generator/ExternalRules.bnf`
- Tutorial grammar: `testData/livePreview/LivePreviewTutorial.bnf`
- Rule modifiers docs: `resources/messages/attributeDescriptions/*.html`

## External Links
- IntelliJ SDK: https://plugins.jetbrains.com/docs/intellij/custom-language-support.html
- Grammar-Kit Repository: https://github.com/JetBrains/Grammar-Kit
- BNF Wikipedia: https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_form
- EBNF Standard: https://www.iso.org/standard/26153.html

## Validation
- [x] Code refs valid (2025-02-04)
- [x] Examples compile (2025-02-04)
- [x] File paths accurate (2025-02-04)
- [x] External links accessible (2025-02-04)

## Errors Found
None - all references validated successfully

## Out of Scope References
- Attribute-specific references → Validated in Section 2.2
- Live Preview tool references → Validated in Section 2.3
- Parser generation references → Validated in Section 4.1
- Grammar design pattern references → Validated in Section 3.1
- Expression parsing patterns → Validated in Section 3.2

## Additional References Found

### Token Type Documentation
- Literal tokens: Demonstrated in `grammars/Grammar.bnf` with quotes
- Named tokens: `grammars/Grammar.bnf#L22-39` shows token declarations
- Regexp tokens: `grammars/Grammar.bnf#L41-47` shows regexp syntax
- Token precedence: Not explicitly documented in source, inferred from implementation

### Rule Modifier Definitions
- `private`: Documented in `resources/messages/attributeDescriptions/pin.html`
- `external`: Documented in `resources/messages/attributeDescriptions/parserUtilClass.html`
- `meta`: Referenced in `testData/generator/ExternalRules.bnf`
- `left`: Documented in `resources/messages/attributeDescriptions/methods.html`
- `inner`, `upper`, `fake`: Referenced in attribute descriptions

### BNF Syntax Elements
- Rule definition operator `::=`: `grammars/Grammar.bnf#L23`
- Choice operator `|`: `grammars/Grammar.bnf#L25`
- Quantifiers `?`, `+`, `*`: `grammars/Grammar.bnf#L26-28`
- Predicates `&`, `!`: `grammars/Grammar.bnf#L29-30`
- Grouping `()`, `[]`, `{}`: `grammars/Grammar.bnf#L32-37`
- External expressions `<<>>`: `grammars/Grammar.bnf#L38-39`

### Related Documentation
- README.md: Basic PEG BNF syntax overview
- TUTORIAL.md: BNF readability explanation
- HOWTO.md: Expression parsing and operator precedence

## Notes
- Grammar-Kit extends standard BNF with PEG-like features (predicates, quantifiers)
- The `grammars/Grammar.bnf` file serves as both the BNF definition and a complete example
- Token precedence is implementation-dependent and follows declaration order
- Rule modifiers are Grammar-Kit specific extensions not found in standard BNF