# References: Introduction to GrammarKit

## Scope Information
This validates references for section 1.1: Introduction to GrammarKit

## Internal Links
- Prerequisites: None (this is the first section)
- Related: `getting-started/installation`, `getting-started/quick-start`
- Advanced: `core-concepts/bnf-syntax`, `parser-development/*`

## Code References
- Plugin description: `resources/META-INF/plugin.xml#L5-6`
- BNF grammar definition: `grammars/Grammar.bnf`
- JSON example: `testData/livePreview/Json.bnf`
- Tutorial grammar: `testData/livePreview/LivePreviewTutorial.bnf`
- Expression parser: `testData/generator/ExprParser.bnf`
- README overview: `README.md#L10-12`
- Java 17 requirement: `README.md#L19`

## External Links
- IntelliJ Platform SDK: https://plugins.jetbrains.com/docs/intellij/welcome.html
- Grammar-Kit Plugin Page: http://plugins.jetbrains.com/plugin/6606
- Example Projects:
  - Clojure-Kit: https://github.com/gregsh/Clojure-Kit
  - intellij-rust: https://github.com/intellij-rust/intellij-rust
  - intellij-erlang: https://github.com/ignatov/intellij-erlang
  - intellij-elixir: https://github.com/KronicDeth/intellij-elixir
  - Perl5-IDEA: https://github.com/Camelcade/Perl5-IDEA
  - Dart: https://github.com/JetBrains/intellij-plugins/tree/master/Dart

## Validation
- [x] Code refs valid (2026-02-04)
- [x] Examples compile (2026-02-04)
- [x] File paths accurate (2026-02-04)

## Errors Found
- None - all references are accurate

## Validation Details

### What is GrammarKit
✅ **BNF grammar support**: Confirmed in `README.md#L12` - "Adds BNF Grammars and JFlex file editing support"
✅ **Parser generation**: Confirmed in `README.md#L12` - "and a parser/PSI code generator"
✅ **Key features**: All features listed in code-evidence.md are confirmed in `README.md#L54-77`:
  - Live Preview: `README.md#L71` - "open language live preview editor (Ctrl-Alt-P/Cmd-Alt-P)"
  - Structure view: `README.md#L63` - "quick grammar and flex file structure popup (Ctrl-F12/Cmd-F12)"
  - Parser generation: `README.md#L73` - "generate parser/PSI code (Ctrl-Shift-G/Cmd-Shift-G)"
  - JFlex support: `README.md#L75-76` - "generate *.flex" and "run JFlex generator"
  - Refactoring: `README.md#L59-60` - "extract rule" and "introduce token"
  - Navigation: `README.md#L64` - "go to related file (parser and PSI)"
  - Inspections: `README.md#L68` - "a number of inspections"
  - Documentation: `README.md#L69` - "rule documentation popup shows FIRST/FOLLOWS/PSI content"
  - Diagram: `README.md#L77` - "PSI tree diagram (UML plugin required)"

✅ **IntelliJ Platform relationship**: Confirmed in `plugin.xml#L6` - "Readable parser/PSI code generator"
✅ **Included in platform**: Confirmed in `README.md#L209` - "included in *IntelliJ Platform* since version 12.1"

### When to Use GrammarKit
✅ **Custom language plugin development**: Confirmed with examples in `README.md#L21-30`
✅ **DSL support**: Implicit from "language plugin developers" purpose
✅ **File format parsers**: JSON example confirmed at `testData/livePreview/Json.bnf`

### Prerequisites
✅ **IntelliJ IDEA requirements**: Confirmed in `plugin.xml#L9` - depends on "com.intellij.modules.lang"
✅ **Java 17 requirement**: Confirmed in `README.md#L19` - "Since 2022.3, Grammar-Kit plugin requires Java 17"
✅ **Java development knowledge**: Implicit from generated Java code
✅ **Parsing concepts**: Confirmed helpful in `TUTORIAL.md#L3-4` - "BNF grammars are pretty easy to read"

## Out of Scope References
- Installation steps → Validated in Section 1.2
- Grammar syntax details → Validated in Section 2.1
- Attribute system → Validated in Section 2.2
- Parser generation specifics → Validated in Section 3.x
- Pin/recoverWhile attributes → Validated in Section 2.2
- Expression parsing details → Validated in Section 3.2