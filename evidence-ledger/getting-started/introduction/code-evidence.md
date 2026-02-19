# Code Evidence: What is Grammar-Kit?

## Scope Information
This evidence covers section 1.1: What is Grammar-Kit?
Extracted from Grammar-Kit source repository on 2026-02-19.

---

## Plugin Identity

- **Official name**: "Grammar-Kit" (dash required)
  - Source: `plugin.xml` → `<name>Grammar-Kit</name>`
- **Plugin ID**: `org.jetbrains.idea.grammar`
  - Source: `plugin.xml` → `<id>org.jetbrains.idea.grammar</id>`
- **Vendor**: JetBrains
  - Source: `plugin.xml` → `<vendor>JetBrains</vendor>`
- **Official description**: "BNF Grammars and JFlex lexers editor. Readable parser/PSI code generator."
  - Source: `plugin.xml` → `<description>`
- **Tagline from README**: "An IntelliJ IDEA plugin for language plugin developers."
  - Source: `README.md` line 10
- **README summary**: "Adds BNF Grammars and JFlex file editing support, and a parser/PSI code generator."
  - Source: `README.md` line 12
- **Library description**: "Grammar-Kit library dedicated for language plugin developers."
  - Source: `build.gradle.kts` line 213
- **License**: Apache License 2.0
  - Source: `README.md` badge
- **Status**: Official JetBrains project (badge: "official project")
  - Source: `README.md` line 4
- **Marketplace URL**: http://plugins.jetbrains.com/plugin/6606
  - Source: `README.md` line 10

## Version and Compatibility

- **Current version**: `2023.3-dev`
  - Source: `gradle.properties` → `pluginVersion`
- **Minimum IDE build**: 233 (IntelliJ IDEA 2023.3+)
  - Source: `gradle.properties` → `pluginSinceBuild`
- **Java requirement**: Java 17 (since 2022.3)
  - Source: `README.md` line 19, `gradle.properties` → `javaVersion=17`
- **Platform type**: IU (IntelliJ IDEA Ultimate used for development)
  - Source: `gradle.properties` → `platformType`
- **Optional dependencies**: Copyright plugin, Java plugin, UML/Diagram plugin
  - Source: `plugin.xml` lines 10-12
- **Required dependency**: `com.intellij.modules.lang` (any IntelliJ-based IDE with language support)
  - Source: `plugin.xml` line 9

## Core Capabilities (BNF-to-Parser Transformation)

- **Generates**: parser code, ElementTypes, PSI classes from BNF grammar
  - Source: `README.md` line 39 → "Generate parser/ElementTypes/PSI classes (Ctrl-Shift-G)"
- **Generates**: JFlex lexer definition (*.flex) from BNF grammar
  - Source: `README.md` line 40 → "Generate lexer *.flex file"
- **Generates**: Java lexer code from *.flex files via JFlex generator
  - Source: `README.md` line 40 → "run JFlex generator (both via context menu)"
- **Generates**: custom `parserUtilClass` class
  - Source: `README.md` line 74
- **Generates**: PsiElementVisitor implementation
  - Source: `HOWTO.md` lines 288-300
- **Parser type**: PsiBuilder-based recursive descent parser
  - Source: `CHANGELOG.md` line 358 → "Readable PsiBuilder-based recursive descent parser"
- **Token definition**: tokens can include `regexp:` patterns for lexer generation
  - Source: `README.md` lines 226-238
- **File types supported**: `.bnf` (BNF grammar), `.flex` (JFlex lexer)
  - Source: `plugin.xml` lines 15, 96

## Target Use Cases

### Programming languages (evidence from open-source plugins)
- Clojure: [Clojure-Kit](https://github.com/gregsh/Clojure-Kit)
- Rust: [intellij-rust](https://github.com/intellij-rust/intellij-rust)
- Erlang: [intellij-erlang](https://github.com/ignatov/intellij-erlang)
- Elm: [intellij-elm](https://github.com/intellij-elm/intellij-elm)
- Elixir: [intellij-elixir](https://github.com/KronicDeth/intellij-elixir)
- Perl: [Perl5-IDEA](https://github.com/Camelcade/Perl5-IDEA)
- Dart: [Dart](https://github.com/JetBrains/intellij-plugins/tree/master/Dart)
- Haxe: [intellij-haxe](https://github.com/HaxeFoundation/intellij-haxe)
  - Source: `README.md` lines 23-31

### Configuration formats
- JSON grammar exists as test/example: `testData/livePreview/Json.bnf`
  - Defines: objects, arrays, properties, values (string, number)
  - Source: `testData/livePreview/Json.bnf`

### Query languages
- Cypher (graph database): [jetbrains-plugin-graph-database-support](https://github.com/neueda/jetbrains-plugin-graph-database-support)
  - Source: `README.md` line 31

### Expression languages
- Expression parser with operators, precedence, associativity: `testData/generator/ExprParser.bnf`
  - Supports: assignment, arithmetic, boolean, unary, postfix, function calls, qualification
  - Source: `testData/generator/ExprParser.bnf`

### DSL support
- Tutorial demonstrates building a custom expression language from scratch
  - Source: `TUTORIAL.md` lines 29-42

### Self-hosting
- Grammar-Kit's own BNF grammar is defined in Grammar-Kit: `grammars/Grammar.bnf`
  - Source: `README.md` line 37, line 85

## Key Development Features

### Live Preview
- **Action**: Open Live Preview editor
- **Shortcut**: Ctrl-Alt-P / Cmd-Alt-P
- **Purpose**: Real-time grammar testing without code generation or compilation
- **Capabilities**:
  - Test grammar against sample text in real time
  - Structure view shows PSI tree as grammar is modified
  - File Structure popup (Ctrl-F12) for PSI observation
  - PSI Viewer dialog available
  - Source: `README.md` line 71, `TUTORIAL.md` lines 27-49
- **Grammar highlighting in preview**: Ctrl-Alt-F7 / Cmd-Alt-F7
  - Highlights grammar expressions at caret position in preview editor
  - Source: `TUTORIAL.md` line 49, `plugin.xml` lines 122-125
- **Supports**: full Java RegExp syntax for token patterns
  - Source: `README.md` line 240
- **Limitation**: not useful after lexer is finalized (requires maintaining 2 lexers)
  - Source: `TUTORIAL.md` lines 75-76

### Interactive Grammar Development Workflow
- Step 1: Create grammar *.bnf file
- Step 2: Tune grammar using Live Preview + Structure view
- Step 3: Generate parser/ElementTypes/PSI classes (Ctrl-Shift-G)
- Step 4: Generate lexer *.flex file, then run JFlex generator (context menu)
- Step 5: Implement ParserDefinition, add registrations to plugin.xml
- Step 6: Mix-in resolve and non-trivial functionality to PSI
  - Source: `README.md` lines 37-43

### Prototyping workflow (from Tutorial)
- Step 1: Prototype grammar in Live Preview
- Step 2: Generate initial *.flex and *.java lexer
- Step 3: Create ParserDefinition and/or setup tests
- Step 4: Perfect *.flex and *.bnf separately in production
  - Source: `TUTORIAL.md` lines 68-74

### Expression Parsing with Operator Precedence
- Compact expression parsing with automatic priority handling
- Uses `extends(".*_expr")=expr` pattern for expression hierarchy
- Priority increases from top to bottom in rule definition
- Supports: BINARY, PREFIX, POSTFIX, N_ARY, ATOM operator types
- Left recursion handled automatically for binary/postfix expressions
- `rightAssociative` attribute for right-associative operators
- Generated parser uses Pratt-like parsing (procedural rewrite of TDOP)
- Only 2 methods generated for entire expression root (compact output)
  - Source: `HOWTO.md` lines 122-223

### Error Recovery Mechanisms
- **`pin` attribute**: parser commits at pinned position, continues matching rest of sequence
  - Handles incomplete input (missing parts)
  - Source: `README.md` lines 188-194, `TUTORIAL.md` lines 7-13
- **`recoverWhile` attribute**: skips unexpected tokens until predicate matches
  - Handles unexpected input (extra tokens)
  - Source: `README.md` lines 195-197, `TUTORIAL.md` lines 16-24
- **`#auto` recovery**: automatic recovery predicate generation
  - Source: `CHANGELOG.md` line 267
- **`name` attribute**: customizes error messages (e.g., `<expression> required` instead of token list)
  - Source: `README.md` lines 199-200
- **`extendedPin` mode**: ON by default, parser tries to match rest of sequence after pin
  - Source: `TUTORIAL.md` lines 10-11

## IntelliJ Platform Integration

- **Required module**: `com.intellij.modules.lang` (core language support)
  - Source: `plugin.xml` line 9
- **Generated parsers**: extend `com.intellij.lang.LightPsiParser`
  - Source: `CHANGELOG.md` line 224
- **Runtime base class**: `GeneratedParserUtilBase` included in IntelliJ Platform since 12.1
  - No need to bundle it in projects
  - Source: `README.md` lines 208-209
- **Integration point**: users implement `ParserDefinition` and register in plugin.xml
  - Source: `README.md` line 41
- **PSI tree**: generated classes integrate with IntelliJ PSI (Program Structure Interface)
  - Source: `plugin.xml` description, `README.md` line 12
- **IElementType**: generated token type constants recognized by lexer
  - Source: `README.md` lines 220-221
- **Gradle integration**: via [gradle-grammar-kit-plugin](https://github.com/JetBrains/gradle-grammar-kit-plugin)
  - Limitations: no method mixins, generic signatures may be incorrect
  - Source: `README.md` lines 44-51
- **Standalone usage**: `java -jar grammar-kit.jar <output-dir> <grammars>` (POC, unsupported)
  - Source: `HOWTO.md` lines 400-424
- **Fleet support**: Generate Parser Code, Generate JFlex Lexer, Run JFlex Generator (context menu)
  - Source: `CHANGELOG.md` lines 12-14

## Example Locations
- `testData/livePreview/Json.bnf`: JSON grammar (configuration format use case)
- `testData/generator/ExprParser.bnf`: Expression parser (programming language use case)
- `testData/livePreview/LivePreviewTutorial.bnf`: Tutorial grammar (workflow example)
- `grammars/Grammar.bnf`: Grammar-Kit's own grammar (self-hosting example)

## Out of Scope
Features found but excluded per section boundaries:
- Detailed grammar syntax (PEG, modifiers, tokens) → Section 2.1
- Full attribute system (extends, implements, mixin, etc.) → Section 3.1
- Parser generation internals (code structure, splitting) → Section 3.2
- Plugin installation steps → Section 1.3
- Quick start tutorial → Section 1.4
- Complete feature list (refactoring, navigation, inspections) → Section 1.2
- PSI hierarchy design (fake rules, methods, stubs) → Section 3.x
- JFlex lexer details → separate section

## Missing Documentation
- No explicit list of supported IDE products (only `com.intellij.modules.lang` dependency implies broad compatibility)
- No user-facing documentation about Fleet support beyond changelog entry
- Plugin marketplace page (plugin/6606) not examined for additional description text
- No explicit statement about supported grammar paradigm (PEG-based) in plugin.xml description
