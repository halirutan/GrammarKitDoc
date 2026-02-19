# Topic Summary: Quick Start Tutorial

## Documentation Outline Reference
Section 1.4: Quick Start Tutorial
File: `docs/quick-start.md`
Source: `info/documentation-outline.md` lines 100-128

## Learning Objectives
Based on outline and evidence:

- Write a complete BNF grammar with tokens, rules, and generation attributes
- Use Live Preview to test a grammar interactively before generating code
- Generate parser, PSI, and lexer code from a grammar file
- Understand the generated file structure and what each file does
- Build a minimal language plugin (Language, FileType, ParserDefinition, syntax highlighting)
- Register plugin components in `plugin.xml`
- Verify parsing with sample input files and the PSI Viewer

## Prerequisites

- IntelliJ IDEA installed with Grammar-Kit plugin (Section 1.3)
- Basic familiarity with Java development
- Understanding of what Grammar-Kit does (Section 1.1)
- A plugin development project set up (Section 1.3)

## Content Structure

The page follows a single end-to-end walkthrough: write a grammar, generate code, wire up a plugin, verify it works. Use the "Calc" example throughout. Four major sections map to the outline.

### 1. Your First Grammar (H2)

**Outline items:** Simple expression grammar example, understanding rules and tokens, using Live Preview, common beginner patterns.

Open with the complete `Calc.bnf` grammar (examples.md section 1). Present it first, then explain its parts. This avoids the "build-up" pattern where readers wait 10 paragraphs before seeing anything concrete.

Content sequence:

1. Show the full `Calc.bnf` file (arithmetic expressions with +, -, *, /, parentheses, semicolons).
2. Explain the header attributes block: what `parserClass`, `elementTypeHolderClass`, `psiPackage`, `psiImplPackage` control. Use the table from examples.md "What Each Header Attribute Does."
3. Explain token definitions: simple tokens (`SEMI=';'`), regexp tokens (`number='regexp:\d+(\.\d*)?'`), auto-whitespace/comment detection. Use the table from examples.md "What Each Token Definition Does."
4. Explain the rules section: `root ::= statement *`, private rules, sequence, choice, optional, repetition. Keep to beginner syntax only (code-evidence "Basic Rule Syntax").
5. Explain `pin` and `recoverWhile` briefly (one paragraph each). Mention they are covered in depth in Section 2.4. Show the root-with-recovery pattern.
6. Introduce Live Preview: Ctrl+Alt+P (Cmd+Alt+P on macOS) opens a split editor for real-time testing. Mention structure view (Ctrl+F12) and grammar highlighting at caret (Ctrl+Alt+F7). Note that `space` and `comment` regexp tokens are auto-detected as whitespace/comments in Live Preview. Reference the Live Preview screenshot (`images/livePreview.png`) if available.
7. Note: Live Preview uses simplified tokenization. It is for prototyping. After the grammar stabilizes, switch to a real JFlex lexer.

**Evidence mapping:**
- Grammar file structure -> code-evidence "Grammar File Structure"
- Token definitions -> code-evidence "Token Definitions", references claim 2
- Rule syntax -> code-evidence "Basic Rule Syntax", references claim 3
- Rule modifiers -> code-evidence "Rule Modifiers", references claim 4
- Calc.bnf example -> examples.md section 1
- Live Preview -> code-evidence "Opening Live Preview", "Live Preview Features", references claims 22-24
- Common patterns -> code-evidence "Common Beginner Patterns", examples.md "Common Patterns"

### 2. Generating Parser Code (H2)

**Outline items:** Running the generator (Ctrl+Shift+G), understanding generated files, package structure, integrating with IntelliJ Platform.

Content sequence:

1. How to run: Ctrl+Shift+G (Cmd+Shift+G on macOS), or right-click the `.bnf` file and select **Generate Parser Code**. Mention the success notification format.
2. Show the generated file tree (examples.md "Generated File List"). Explain the `gen/` output directory and the `grammar.kit.gen.dir` system property.
3. Walk through `CalcTypes.java`: element type constants (one per public rule) and token type constants (one per named token). Show the code from examples.md.
4. Walk through `CalcParser.java`: static method per rule, `PsiBuilder` and recursion level parameters, sub-expression naming convention. Warn about naming conflicts (`expr_0`).
5. Mention PSI interfaces, implementations, and visitor (one sentence each). These are covered in depth in Section 3.4.
6. Note: mark `gen/` as Generated Sources Root in the IDE so it compiles.

**Evidence mapping:**
- Running generator -> code-evidence "Running the Generator", references claim 5
- Notification -> code-evidence "Generation Notification", references claim 6
- Output directory -> code-evidence "Default Output Directory", references claim 7
- Generated files -> code-evidence "Generated Files", references claim 8
- CalcTypes -> examples.md "CalcTypes.java"
- CalcParser -> examples.md "CalcParser.java"
- Attribute defaults -> code-evidence "Key Global Attributes", references claim 9
- Generation control -> code-evidence "Generation Can Be Controlled", references claim 10

### 3. Creating a Language Plugin (H2)

**Outline items:** Language and file type registration, basic ParserDefinition, lexer integration, simple syntax highlighting.

This is the longest section. Use H3 subsections to break it into scannable chunks.

#### Generating the Lexer (H3)

1. Generate JFlex file: right-click `.bnf` -> **Generate JFlex Lexer**. Creates `_CalcLexer.flex`.
2. Show the generated `.flex` file (examples.md section 4). Explain: implements `FlexLexer`, returns `IElementType` from `advance()`, imports constants from `CalcTypes`, handles `BAD_CHARACTER` fallback.
3. Note the regex conversion: `\d` becomes `[0-9]`, `\s` becomes `[ \t\n\x0B\f\r]`, etc.
4. Generate Java lexer: right-click `.flex` -> **Run JFlex Generator**. Downloads JFlex 1.9.2 automatically if needed. Creates `_CalcLexer.java`.

**Evidence mapping:**
- JFlex generation -> code-evidence "Generating JFlex Lexer", references claim 16
- Flex template -> code-evidence "Lexer Template Structure", references claim 19
- Regex conversion -> code-evidence "Regexp Token Conversion", references claim 18
- JFlex runner -> code-evidence "Running JFlex Generator", references claim 17

#### Plugin Classes (H3)

Present each class with its code, followed by a brief explanation. Keep explanations to 2-3 sentences per class. The code is the documentation.

1. `CalcLanguage.java` - Singleton, extends `Language`, constructor takes language ID string `"Calc"`.
2. `CalcFileType.java` - Singleton, extends `LanguageFileType`, maps `.calc` extension.
3. `CalcFile.java` - Extends `PsiFileBase`, connects language and file type.
4. `CalcParserDefinition.java` - Implements `ParserDefinition`. Key methods: `createLexer()` wraps JFlex in `FlexAdapter`, `createParser()` returns generated parser, `createElement()` delegates to `CalcTypes.Factory`. Explain each method briefly.
5. `CalcSyntaxHighlighter.java` - Extends `SyntaxHighlighterBase`. Maps token types to `TextAttributesKey` using `DefaultLanguageHighlighterColors` fallbacks.
6. `CalcSyntaxHighlighterFactory.java` - Factory required by extension point.

**Evidence mapping:**
- Language class -> code-evidence "Language Class Pattern", references claim 11
- FileType class -> code-evidence "FileType Class Pattern", references claim 12
- ParserDefinition -> code-evidence "ParserDefinition Pattern", references claims 14-15
- Syntax highlighter -> code-evidence "Simple Syntax Highlighting Pattern", references claims 20-21
- All code -> examples.md section 5

#### Registering in plugin.xml (H3)

1. Show the complete `plugin.xml` (examples.md section 5).
2. Explain the three required registrations: `fileType`, `lang.parserDefinition`, `lang.syntaxHighlighterFactory`.
3. Emphasize: `language="Calc"` must match the string in `CalcLanguage` constructor exactly (case-sensitive).
4. Note: `com.intellij.modules.lang` dependency is required.

**Evidence mapping:**
- FileType registration -> code-evidence "FileType Registration", references claim 13
- ParserDefinition registration -> code-evidence "ParserDefinition Registration", references claim 15
- Highlighter registration -> code-evidence "Syntax Highlighter Registration", references claim 21
- plugin.xml -> examples.md section 5

#### Project Layout (H3)

Show the complete project file layout (examples.md section 6). Distinguish hand-written files (`src/`) from generated files (`gen/`). Note that both must be on the classpath.

### 4. Testing Your Parser (H2)

**Outline items:** Creating test files, using PSI Viewer, basic parsing tests, validation strategies.

Content sequence:

1. Run the plugin (standard IntelliJ plugin run configuration). Create a `.calc` file. Verify syntax highlighting works.
2. Show sample test input files (examples.md section 2): `valid_basic.calc`, `valid_complex.calc`, `error_recovery.calc`.
3. Show the expected PSI tree for `1 + 2;` (examples.md). Explain: public rules become PSI nodes, private rules are transparent, tokens are leaf elements.
4. Mention PSI Viewer: Tools > View PSI Structure. Useful for verifying parse tree structure.
5. Mention `ParsingTestCase` for automated regression tests: provide input text, compare against expected PSI tree dump. Link to IntelliJ SDK "Parsing Test" page.
6. List the BNF editor inspections that help catch grammar issues: left recursion, unresolved references, unused rules, duplicate rules, suspicious tokens.

**Evidence mapping:**
- Test files -> examples.md section 2
- PSI tree -> examples.md "Expected PSI Tree"
- PSI Viewer -> code-evidence "PSI Viewer"
- ParsingTestCase -> code-evidence "Basic Parsing Tests", references claim 26
- Inspections -> code-evidence "Validation Strategies", references claim 27

## Evidence Mapping Summary

| Outline Item | Evidence Source | Status |
|---|---|---|
| Simple expression grammar example | examples.md section 1 (Calc.bnf) | Fully supported |
| Understanding rules and tokens | code-evidence "Token Definitions", "Basic Rule Syntax" | Fully supported |
| Using Live Preview | code-evidence "Opening/Using Live Preview" | Fully supported |
| Common beginner patterns | code-evidence "Common Beginner Patterns", examples.md "Common Patterns" | Fully supported |
| Running the generator | code-evidence "Running the Generator" | Fully supported |
| Understanding generated files | examples.md sections 3-4 (CalcTypes, CalcParser, file tree) | Fully supported |
| Package structure | examples.md "Generated File List", "Project File Layout" | Fully supported |
| Integrating with IntelliJ Platform | examples.md section 5 (plugin classes) | Fully supported |
| Language and file type registration | code-evidence + examples.md (Language, FileType, plugin.xml) | Fully supported |
| Basic ParserDefinition | code-evidence + examples.md (CalcParserDefinition) | Fully supported |
| Lexer integration | code-evidence + examples.md (JFlex generation, FlexAdapter) | Fully supported |
| Simple syntax highlighting | code-evidence + examples.md (CalcSyntaxHighlighter) | Fully supported |
| Creating test files | examples.md section 2 (three .calc files) | Fully supported |
| Using PSI Viewer | code-evidence "PSI Viewer" | Supported (brief) |
| Basic parsing tests | code-evidence "Basic Parsing Tests" | Supported (brief) |
| Validation strategies | code-evidence "Validation Strategies" | Fully supported |

No outline items are missing evidence.

## Key Takeaways

- The tutorial uses a single "Calc" example from start to finish. This gives readers a complete, working reference.
- The grammar is deliberately simple: no `left` rules, no `extends` patterns, no advanced expression parsing. Those belong in Section 2.3.
- `pin` and `recoverWhile` appear in the grammar but get only brief explanation. Section 2.4 covers them in depth.
- Live Preview is introduced as a prototyping tool with clear limitations noted.
- The plugin skeleton requires 6 hand-written Java files, 1 grammar file, and 1 plugin.xml. The generated code adds roughly 10-12 more files.

## Documentation Notes

- Show the complete grammar first, then explain its parts. Readers want to see the whole thing before dissecting it.
- Use the Calc example consistently. Do not switch between Calc, JSON, and Tutorial grammars on this page.
- Keep `pin`/`recoverWhile` explanation to one paragraph each. Link to Section 2.4 for details.
- Keep expression parsing explanation simple. The Calc grammar uses traditional precedence layers (`add_expr` -> `mul_expr` -> `primary_expr`), not the `left`/`extends` idiom. That is intentional for a quick start.
- Include the anti-patterns section from examples.md. Beginners hit these issues immediately: missing header attributes, recovery rules that match everything, naming conflicts with generated sub-expressions, forgetting `FlexAdapter`, mismatched language IDs.
- The workflow summary (examples.md section 7) should appear near the end as a numbered checklist, not at the beginning.
- Reference the recommended workflow from TUTORIAL.md (prototype in Live Preview -> generate flex -> create ParserDefinition -> perfect separately) as the closing guidance.
- Link forward to Sections 2.1 (full syntax), 2.3 (expression parsing), 2.4 (error recovery), 3.4 (PSI customization), 4.2 (Gradle).
- Corrections from references.md: use `EXPLICIT_TOKEN`/`IMPLICIT_TOKEN` (not "TOKEN") if discussing BNF's own highlighter keys. For the Calc example this does not apply since we define our own keys.
- The Ctrl+Shift+G shortcut is documented in README.md but its registration mechanism in plugin.xml is unclear. Present it as the documented shortcut without claiming where it is registered.
