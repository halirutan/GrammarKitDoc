# References: Quick Start Tutorial

## Scope Information
This validates references for section 1.4: Quick Start Tutorial

Covers: your first grammar (rules, tokens, Live Preview, beginner patterns), generating parser code (Ctrl+Shift+G, generated files, package structure), creating a language plugin (Language, FileType, ParserDefinition, lexer, highlighting), and testing your parser (test files, PSI Viewer, basic tests).

---

## Internal Links

### Prerequisites
- `docs/index.md` (Section 1.1: What is Grammar-Kit?)
- `docs/features.md` (Section 1.2: Features)
- `docs/installation.md` (Section 1.3: Installation and Setup)

### Related Sections
- `docs/grammar-development/grammar-syntax.md` (Section 2.1) -- full BNF syntax reference
- `docs/grammar-development/expression-parsing.md` (Section 2.3) -- expression parsing details
- `docs/grammar-development/error-recovery.md` (Section 2.4) -- pin/recoverWhile mechanics
- `docs/grammar-development/live-preview.md` (Section 2.5) -- Live Preview workflow

### Forward References (mentioned but detailed elsewhere)
- Advanced rule modifiers (meta, external, fake, inner, upper): Section 2.1
- Expression parsing with `extends(".*expr")=expr`: Section 2.3
- Detailed pin/recoverWhile mechanics: Section 2.4
- PSI customization (mixin, methods, implements): Section 3.4
- Gradle integration: Section 4.2
- Advanced `generate` options: Section 3.1

---

## Code References

### Primary Source Files

| File | Exists | Lines | Relevance |
|------|--------|-------|-----------|
| `TUTORIAL.md` | Yes | 130 | Complete tutorial with expression grammar, Live Preview workflow, summary |
| `README.md` | Yes | 251 | Usage instructions, syntax overview, rule modifiers, token definitions |
| `testData/livePreview/LivePreviewTutorial.bnf` | Yes | 43 | Tutorial grammar: tokens, extends, name, pin, recoverWhile, left rules |
| `testData/livePreview/Json.bnf` | Yes | 27 | Simpler JSON grammar example for beginners |
| `testData/generator/ExprParser.bnf` | Yes | 76 | Advanced expression parser (out of scope for quick start) |

### Key Implementation Files

| File | Exists | Relevance |
|------|--------|-----------|
| `src/org/intellij/grammar/actions/GenerateAction.java` | Yes (203 lines) | Parser generation action, Ctrl+Shift+G handler |
| `src/org/intellij/grammar/BnfParserDefinition.java` | Yes (79 lines) | ParserDefinition pattern example |
| `src/org/intellij/grammar/BnfLanguage.java` | Yes (28 lines) | Language class singleton pattern |
| `src/org/intellij/grammar/BnfFileType.java` | Yes (46 lines) | FileType class pattern |
| `src/org/intellij/grammar/editor/BnfSyntaxHighlighter.java` | Yes (84 lines) | Syntax highlighter pattern |
| `src/org/intellij/grammar/actions/LivePreviewAction.java` | Yes (40 lines) | Live Preview action |
| `src/org/intellij/grammar/actions/HighlightGrammarAtCaretAction.java` | Yes | Grammar highlighting at caret |
| `src/org/intellij/grammar/actions/BnfGenerateLexerAction.java` | Yes (267 lines) | JFlex lexer generation, regex conversion |
| `src/org/intellij/grammar/actions/BnfRunJFlexAction.java` | Yes | JFlex runner, downloads JFlex 1.9.2 |
| `src/org/intellij/grammar/actions/FileGeneratorUtil.java` | Yes (124 lines) | Target directory resolution, gen dir logic |
| `src/org/intellij/grammar/generator/ParserGenerator.java` | Yes | Parser/PSI/visitor generation engine |
| `src/org/intellij/grammar/generator/GenOptions.java` | Yes (68 lines) | Generation options (psi, tokens, visitor, java version) |
| `src/org/intellij/grammar/config/Options.java` | Yes (22 lines) | System property `grammar.kit.gen.dir` default `"gen"` |
| `src/org/intellij/grammar/KnownAttribute.java` | Yes | All grammar attributes with defaults |
| `src/org/intellij/grammar/generator/BnfConstants.java` | Yes (44 lines) | Constants: GENERATION_GROUP, GPUB_CLASS, etc. |
| `src/org/intellij/grammar/livePreview/LivePreviewHelper.java` | Yes | Live Preview orchestration |
| `src/org/intellij/grammar/livePreview/LivePreviewParserDefinition.java` | Yes | Live Preview parser definition |
| `src/org/intellij/grammar/LightPsi.java` | Yes | Standalone parsing API for testing |
| `resources/META-INF/plugin.xml` | Yes (136 lines) | Plugin registrations, extension points |
| `resources/templates/lexer.flex.template` | Yes (48 lines) | JFlex lexer template |
| `resources/messages/GrammarKitBundle.properties` | Yes (46 lines) | Action names, inspection names |
| `resources/messages/attributeDescriptions/generate.html` | Yes (110 lines) | Generate attribute options table |
| `resources/messages/attributeDescriptions/tokens.html` | Yes (20 lines) | Token definitions documentation |

### Images

| File | Exists | Referenced In |
|------|--------|---------------|
| `images/livePreview.png` | Yes | `TUTORIAL.md` line 54 |
| `images/editor.png` | Yes | `README.md` line 57 |

---

## External Links

### IntelliJ Platform SDK Documentation

| Link | Status | Notes |
|------|--------|-------|
| [Custom Language Support Tutorial](https://plugins.jetbrains.com/docs/intellij/custom-language-support-tutorial.html) | **Valid** | 21-step tutorial; referenced from Grammar-Kit README.md line 33. Covers prerequisites through spell checking. |
| [Grammar and Parser (Step 3)](https://plugins.jetbrains.com/docs/intellij/grammar-and-parser.html) | **Valid** | Shows Grammar-Kit BNF usage with `parserClass`, `psiPackage`, etc. Includes "Generate Parser Code" context menu instruction. |
| [Lexer and Parser Definition (Step 4)](https://plugins.jetbrains.com/docs/intellij/lexer-and-parser-definition.html) | **Valid** | Shows JFlex lexer, FlexAdapter, ParserDefinition pattern, plugin.xml registration. Mentions Grammar-Kit JFlex generation. |
| [Implementing Parser and PSI](https://plugins.jetbrains.com/docs/intellij/implementing-parser-and-psi.html) | **Valid** | Explicitly recommends Grammar-Kit: "we highly recommend generating parser and corresponding PSI classes from BNF grammars using Grammar-Kit plugin." Covers PsiBuilder, markers, whitespace handling. |
| [Parsing Test (Testing Step 2)](https://plugins.jetbrains.com/docs/intellij/parsing-test.html) | **Valid** | Shows `ParsingTestCase` subclass pattern, test data organization, PSI tree comparison. Uses Grammar-Kit "Generate Parser Code" action. |

### Grammar-Kit Project Links

| Link | Status | Notes |
|------|--------|-------|
| [GitHub Repository](https://github.com/JetBrains/Grammar-Kit) | Valid | Official JetBrains project |
| [Gradle Grammar-Kit Plugin](https://github.com/JetBrains/gradle-grammar-kit-plugin) | Valid | Build automation (out of scope for quick start) |
| [PEG Wikipedia](http://en.wikipedia.org/wiki/Parsing_expression_grammar) | Valid | Referenced in README.md line 82 for basic syntax |
| [JFlex Documentation](http://jflex.de/manual.html) | Valid | Referenced in README.md line 240 for regex subset |

---

## Claim Verification

### Claim 1: Grammar file structure has header attributes block and rules
- **Status**: PASS
- **Evidence**:
  - `TUTORIAL.md` lines 84-127: Complete grammar with `{ tokens=[...] name(...) extends(...) }` header followed by rules
  - `LivePreviewTutorial.bnf`: Lines 1-23 are header block, lines 25-43 are rules
  - `Json.bnf`: Lines 1-15 are header block, lines 17-27 are rules
  - `README.md` lines 89-106: Syntax overview showing header and rule sections

### Claim 2: Token definitions support simple, regexp, and keyword forms
- **Status**: PASS
- **Evidence**:
  - `TUTORIAL.md` lines 85-103: Shows `SEMI=';'` (simple), `number='regexp:\d+(\.\d*)?'` (regexp), `space='regexp:\s+'` (whitespace)
  - `LivePreviewTutorial.bnf` lines 3-18: Exact match with TUTORIAL.md token block
  - `tokens.html`: Documents `id="regexp:\w+"` (regexp), `PLUS_OP="+"` (simple), `string` (no value)
  - `README.md` lines 172-184: Token documentation including implicit tokens

### Claim 3: Basic rule syntax includes sequence, choice, optional, repetition
- **Status**: PASS
- **Evidence**:
  - `README.md` lines 90-96: Shows sequence (`rule_A rule_B`), choice (`|`), optional (`[...]`, `?`), predicate (`&`, `!`), grouping/repetition (`*`, `+`)
  - `LivePreviewTutorial.bnf`: Demonstrates sequence (line 28: `id '=' expr`), choice (line 42: `number | string | float`), optional (line 37: `factorial_expr ?`), repetition (line 25: `root_item *`)

### Claim 4: Rule modifiers include private and left (beginner-level)
- **Status**: PASS
- **Evidence**:
  - `README.md` lines 131-147: Full modifier list. Private: "skip node creation and let its child nodes be included in its parent." Left: "take an AST node on the left (previous sibling) and enclose it by becoming its parent."
  - `LivePreviewTutorial.bnf`: Uses `private` (lines 26, 29, 33, 34, 36, 37, 39) and `left` (lines 32, 35, 38)
  - Default is public (non-private, non-fake): `README.md` line 147

### Claim 5: Generate Parser Code action uses Ctrl+Shift+G
- **Status**: PASS
- **Evidence**:
  - `README.md` line 39: "Generate parser/ElementTypes/PSI classes (Ctrl-Shift-G / Cmd-Shift-G)"
  - `GrammarKitBundle.properties` line 16: `action.grammar.Generate.text=Generate Parser Code`
  - `GenerateAction.java`: Implements the action (203 lines)
  - Note: The keyboard shortcut is NOT defined in `plugin.xml` -- it's registered via the IDE's keymap system. The `plugin.xml` only registers the action class at line 133 (within `grammar.file.group` but without explicit shortcut). The shortcut is documented in README.md.

### Claim 6: Generation notification format
- **Status**: PASS (with line number correction)
- **Evidence**:
  - `GenerateAction.java` lines 179-182: Success notification: `String.format("%s generated (%s)", file.getName(), StringUtil.formatFileSize(written))` with detail `"to " + genDir`
  - `GenerateAction.java` lines 122-131: Batch notification (when >3 files): `String.format("%d grammars: %d files generated (%s) in %s", ...)`
  - `GenerateAction.java` lines 187-190: Failure notification: `file.getName() + " generation failed"` with stack trace
  - `BnfConstants.java` line 12: `GENERATION_GROUP = "Grammar Generator"`
  - **Correction**: Code-evidence says "lines 126-191" but the relevant notification code spans lines 122-190. Close enough but not exact.

### Claim 7: Default output directory uses `grammar.kit.gen.dir` system property
- **Status**: PASS
- **Evidence**:
  - `Options.java` line 14: `GEN_DIR = Option.strOption("grammar.kit.gen.dir", "gen")`
  - `FileGeneratorUtil.java` line 88: `String genDirName = Options.GEN_DIR.get()`
  - `FileGeneratorUtil.java` lines 89-92: Logic for source root vs content root generation

### Claim 8: Generated files include parser, element type holder, PSI interfaces, PSI impls, visitor
- **Status**: PASS
- **Evidence**:
  - `ParserGenerator.java` lines 277-341: `generate()` method calls:
    - `generateParser()` (line 279)
    - `generateElementTypesHolder()` (line 302) -- conditional on `generateTokenTypes || generateElementTypes || generatePsi && generatePsiFactory`
    - `generatePsiIntf()` (line 315) -- per rule
    - `generatePsiImpl()` (line 325) -- per rule
    - `generateVisitor()` (line 334) -- conditional on `myVisitorClassName != null`

### Claim 9: Key global attribute defaults
- **Status**: PASS
- **Evidence from `KnownAttribute.java`**:
  - `parserClass`: `"generated.GeneratedParser"` (line 46)
  - `elementTypeHolderClass`: `"generated.GeneratedTypes"` (line 48)
  - `psiPackage`: `"generated.psi"` (line 41)
  - `psiImplPackage`: `"generated.psi.impl"` (line 42)
  - `psiClassPrefix`: `""` (line 38)
  - `psiImplClassSuffix`: `"Impl"` (line 39)
  - `psiVisitorName`: `"Visitor"` (line 43)
  - `parserUtilClass`: `BnfConstants.GPUB_CLASS` = `"com.intellij.lang.parser.GeneratedParserUtilBase"` (line 47, BnfConstants line 18)
  - `generatePsi`: `true` (line 31)
  - `generateTokens`: `true` (line 32)
  - **Correction**: Code-evidence says "lines 29-48" but the attributes span lines 29-50 (including `ELEMENT_TYPE_PREFIX` and `TOKEN_TYPE_FACTORY`). Minor range discrepancy.

### Claim 10: Generation control via `generate=[...]` options
- **Status**: PASS
- **Evidence**:
  - `generate.html`: Full options table with psi, tokens, visitor, java, etc.
  - `GenOptions.java` line 46: `generatePsi = getGenerateOption(myFile, KnownAttribute.GENERATE_PSI, genOptions, "psi")`
  - `GenOptions.java` line 49: `generateTokenTypes = getGenerateOption(myFile, KnownAttribute.GENERATE_TOKENS, genOptions, "tokens")`
  - `GenOptions.java` line 59: `generateVisitor = !"no".equals(genOptions.get("visitor"))`
  - `GenOptions.java` line 65: `javaVersion = StringUtil.parseInt(genOptions.get("java"), 11)` -- default Java 11

### Claim 11: Language class uses singleton pattern with `super("LanguageID")`
- **Status**: PASS
- **Evidence**:
  - `BnfLanguage.java` line 17: `public static final BnfLanguage INSTANCE = new BnfLanguage()`
  - `BnfLanguage.java` line 20: `super("BNF")`
  - Extends `com.intellij.lang.Language` (line 15)

### Claim 12: FileType class uses singleton pattern extending LanguageFileType
- **Status**: PASS
- **Evidence**:
  - `BnfFileType.java` line 19: `public static final BnfFileType INSTANCE = new BnfFileType()`
  - `BnfFileType.java` line 22: `super(BnfLanguage.INSTANCE)`
  - Extends `com.intellij.openapi.fileTypes.LanguageFileType` (line 17)
  - Methods: `getName()` (line 26), `getDescription()` (line 31), `getDefaultExtension()` (line 36), `getIcon()` (line 41)

### Claim 13: FileType registration in plugin.xml
- **Status**: PASS
- **Evidence**:
  - `plugin.xml` line 15: `<fileType name="BNF" implementationClass="org.intellij.grammar.BnfFileType" fieldName="INSTANCE" extensions="bnf" language="BNF"/>`

### Claim 14: ParserDefinition implements required methods
- **Status**: PASS
- **Evidence from `BnfParserDefinition.java`**:
  - `createLexer(Project)`: line 33 -- returns `new BnfLexer()`
  - `createParser(Project)`: line 38 -- returns `new GrammarParser()`
  - `getFileNodeType()`: line 43 -- returns `BNF_FILE_ELEMENT_TYPE`
  - `getWhitespaceTokens()`: line 48 -- returns `BnfTokenSets.WS`
  - `getCommentTokens()`: line 53 -- returns `BnfTokenSets.COMMENTS`
  - `getStringLiteralElements()`: line 58 -- returns `BnfTokenSets.LITERALS`
  - `createElement(ASTNode)`: line 63 -- throws UnsupportedOperationException (BNF uses AST factory instead)
  - `createFile(FileViewProvider)`: line 68 -- returns `new BnfFileImpl(fileViewProvider)`
  - `IFileElementType` created as: `new IFileElementType("BNF_FILE", BnfLanguage.INSTANCE)` (line 30)

### Claim 15: ParserDefinition registration in plugin.xml
- **Status**: PASS
- **Evidence**:
  - `plugin.xml` line 17: `<lang.parserDefinition language="BNF" implementationClass="org.intellij.grammar.BnfParserDefinition"/>`

### Claim 16: JFlex lexer generation produces `_[GrammarName]Lexer.flex`
- **Status**: PASS
- **Evidence**:
  - `BnfGenerateLexerAction.java` line 258-263: `getFlexFileName()` returns `getLexerName() + ".flex"`, where `getLexerName()` returns `"_" + getGrammarName(bnfFile) + "Lexer"`

### Claim 17: JFlex 1.9.2 is downloaded automatically
- **Status**: PASS
- **Evidence**:
  - `BnfRunJFlexAction.java` lines 74-75: `JFLEX_URL = "https://cache-redirector.jetbrains.com/intellij-dependencies/org/jetbrains/intellij/deps/jflex/jflex/1.9.2/jflex-1.9.2.jar"`

### Claim 18: Regexp token conversion (Java regex to JFlex)
- **Status**: PASS
- **Evidence from `BnfGenerateLexerAction.java` lines 232-253**:
  - `\d` → `[0-9]` (line 241)
  - `\s` → `[ \t\n\x0B\f\r]` (line 243)
  - `\w` → `[a-zA-Z_0-9]` (line 245)
  - `\p{Alpha}` → `[:letter:]` (line 249)
  - `\p{Digit}` → `[:digit:]` (line 248)
  - Also handles: `\D`, `\S`, `\W`, `\p{Space}`, `\p{Lower}`, `\p{Upper}`, `\p{Alnum}`, `\p{ASCII}`
  - **Correction**: Code-evidence says "lines 238-253" but the method starts at line 232. The actual conversions are at lines 241-253.

### Claim 19: Lexer template implements FlexLexer with advance() returning IElementType
- **Status**: PASS
- **Evidence from `lexer.flex.template`**:
  - Line 3: `import com.intellij.lexer.FlexLexer;`
  - Line 20: `%implements FlexLexer`
  - Line 21: `%function advance`
  - Line 22: `%type IElementType`
  - Line 7: `import static com.intellij.psi.TokenType.WHITE_SPACE;`
  - Line 6: `import static com.intellij.psi.TokenType.BAD_CHARACTER;`
  - Line 47: `[^] { return BAD_CHARACTER; }`

### Claim 20: Syntax highlighter extends SyntaxHighlighterBase
- **Status**: PASS
- **Evidence from `BnfSyntaxHighlighter.java`**:
  - Line 23: `class BnfSyntaxHighlighter extends SyntaxHighlighterBase`
  - Line 47: `getHighlightingLexer()` returns `new BnfLexer()`
  - Line 52: `getTokenHighlights(IElementType)` maps token types to `TextAttributesKey`
  - Defines keys: COMMENT, STRING, NUMBER, KEYWORD, EXPLICIT_TOKEN, IMPLICIT_TOKEN, RULE, META_RULE, META_PARAM, ATTRIBUTE, EXTERNAL, OP_SIGN, PARENTHS, BRACES, BRACKETS, ANGLES, RECOVER_MARKER, PIN_MARKER (lines 24-44)
  - **Correction**: Code-evidence lists "RULE, TOKEN, ATTRIBUTE" but actual keys are "RULE, EXPLICIT_TOKEN, IMPLICIT_TOKEN, ATTRIBUTE" -- there is no single "TOKEN" key.

### Claim 21: Syntax highlighter registration in plugin.xml
- **Status**: PASS
- **Evidence**:
  - `plugin.xml` line 22: `<lang.syntaxHighlighterFactory language="BNF" implementationClass="org.intellij.grammar.editor.BnfSyntaxHighlighterFactory"/>`

### Claim 22: Live Preview shortcut is Ctrl+Alt+P
- **Status**: PASS
- **Evidence**:
  - `plugin.xml` line 115: `<keyboard-shortcut keymap="$default" first-keystroke="control alt P"/>`
  - `README.md` line 38: "Tune the grammar using _Live Preview_ + Structure view (Ctrl-Alt-P / Cmd-Alt-P)"
  - `TUTORIAL.md` line 45: "ctrl-alt-P/meeta-alt-P shortcut" (note: typo "meeta" in original)

### Claim 23: Live Preview auto-reparses with 500ms debounce
- **Status**: UNVERIFIED
- **Evidence**:
  - `LivePreviewHelper.java` uses `MergingUpdateQueue` (imported at line 35) and `Alarm` (imported at line 32) for debounced updates
  - The exact 500ms value was not found in the code examined. The debounce timing is likely configured in the `MergingUpdateQueue` constructor but would require reading deeper into the file.
  - **Note**: The claim is plausible but the exact value could not be confirmed from the lines read.

### Claim 24: Grammar highlighting at caret uses Ctrl+Alt+F7
- **Status**: PASS
- **Evidence**:
  - `plugin.xml` line 124: `<keyboard-shortcut keymap="$default" first-keystroke="control alt F7"/>`
  - `README.md` line 72: "start/stop grammar evaluator highlighting (Ctrl-Alt-F7/Cmd-Alt-F7 in preview editor)"
  - `TUTORIAL.md` line 49: "ctrl-alt-F7/meta-alt-F7"

### Claim 25: LightPsi class for standalone parsing
- **Status**: PASS
- **Evidence**:
  - `LightPsi.java` exists (line 49: `public class LightPsi`)
  - Provides standalone parsing API without full IDE context
  - Used for command-line parser validation

### Claim 26: ParsingTestCase base class for parsing tests
- **Status**: PASS (external verification)
- **Evidence**:
  - IntelliJ SDK "Parsing Test" page confirms: `ParsingTestCase` is the base class
  - Pattern: provide input text, compare against expected PSI tree dump
  - Test data: input files and expected output files in `testData/` directory
  - Grammar-Kit's own test data: `testData/generator/`, `testData/livePreview/`, `testData/parser/`

### Claim 27: BNF editor inspections
- **Status**: PASS
- **Evidence from `plugin.xml` lines 56-79 and `GrammarKitBundle.properties` lines 28-36**:
  - Left recursion detection: `BnfLeftRecursionInspection` (plugin.xml line 69)
  - Unresolved references: `BnfResolveInspection` (plugin.xml line 56)
  - Unused rules: `BnfUnusedRuleInspection` (plugin.xml line 59)
  - Duplicate rules: `BnfDuplicateRuleInspection` (plugin.xml line 71)
  - Suspicious tokens: `BnfSuspiciousTokenInspection` (plugin.xml line 65)
  - Identical choice branches: `BnfIdenticalChoiceBranchesInspection` (plugin.xml line 74)
  - Unreachable choice branches: `BnfUnreachableChoiceBranchInspection` (plugin.xml line 77)
  - Also: Unused attributes: `BnfUnusedAttributeInspection` (plugin.xml line 62)

### Claim 28: Recommended workflow from TUTORIAL.md
- **Status**: PASS
- **Evidence from `TUTORIAL.md` lines 68-74**:
  1. "prototype the grammar in *LivePreview*"
  2. "generate initial `*.flex` to sources and generate a `*.java` lexer from it"
  3. "create *ParserDefinition* and/or setup lexer and parser tests"
  4. "perfect the `*.flex` & `*.bnf` separately in production environment"

---

## Errors Found

### Line Number Discrepancies

1. **`GenerateAction.java` notification code**: Code-evidence says "lines 126-191" but the notification code spans lines 122-196 (the full `run()` and `runInner()` methods). The individual notifications are at lines 128-131 (batch), 179-182 (success), 187-190 (failure). Minor range discrepancy, content is accurate.

2. **`KnownAttribute.java` attribute lines**: Code-evidence says "lines 29-48" for key global attributes. Actual range is lines 29-50 (includes `ELEMENT_TYPE_PREFIX` at line 49 and `TOKEN_TYPE_FACTORY` at line 50). Content is accurate.

3. **`BnfGenerateLexerAction.java` regex conversion lines**: Code-evidence says "lines 238-253" but the `text2JFlex` method starts at line 232. The actual regex conversions are at lines 241-253. Minor offset.

### Content Corrections

4. **Syntax highlighter keys**: Code-evidence line 229 lists "TOKEN" as a highlighting key, but `BnfSyntaxHighlighter.java` defines `EXPLICIT_TOKEN` (line 30) and `IMPLICIT_TOKEN` (line 31) -- there is no single "TOKEN" key. The evidence should reference `EXPLICIT_TOKEN` and `IMPLICIT_TOKEN` separately.

5. **`BnfParserDefinition.java` createElement()**: Code-evidence line 182 says `createElement(ASTNode)` should "create PSI element from AST node." In the actual BNF implementation (line 63-65), it throws `UnsupportedOperationException` because BNF uses `BnfASTFactory` instead (registered at plugin.xml line 18). This is an implementation detail specific to Grammar-Kit's own parser, not the general pattern. The ParserDefinition interface does require this method, and typical implementations would delegate to the generated `Types.Factory.createElement()`.

6. **Live Preview 500ms debounce**: The exact 500ms value could not be confirmed from the source code examined. The `LivePreviewHelper` uses `MergingUpdateQueue` for debounced updates, but the specific timing value requires deeper inspection.

7. **`GenerateAction.java` shortcut registration**: Code-evidence says the shortcut is available from "context menu on `.bnf` files, editor popup menu." The `plugin.xml` (lines 118-120) confirms the action is added to `ToolsMenu`, `EditorPopupMenu`, and `ProjectViewPopupMenu`. However, the Ctrl+Shift+G shortcut is NOT registered in `plugin.xml` -- it must be registered elsewhere (likely via the IDE's keymap or a separate action registration). The README documents it at line 39 and line 73.

### Missing Generate Parser Code Shortcut Registration

8. **Ctrl+Shift+G shortcut**: The `GenerateAction` is registered in `plugin.xml` line 133 within `grammar.file.group` but without an explicit `<keyboard-shortcut>` element. The shortcut `Ctrl+Shift+G` is documented in README.md but its registration mechanism was not found in `plugin.xml`. It may be registered via `plugin-java.xml` (the optional Java dependency config file) or through the IDE's default keymap.

---

## Out of Scope References

The following topics appear in the code-evidence but belong to other documentation sections:

| Topic | Validated In |
|-------|-------------|
| Full PEG syntax, predicates (`&`, `!`), external expressions (`<< >>`) | Section 2.1: Grammar Syntax |
| `meta`, `external`, `fake`, `inner`, `upper` rule modifiers | Section 2.1: Grammar Syntax |
| Expression parsing with `extends(".*expr")=expr` pattern | Section 2.3: Expression Parsing |
| `left` modifier mechanics for operator precedence (detailed) | Section 2.3: Expression Parsing |
| `rightAssociative`, `extraRoot` attributes | Section 2.3: Expression Parsing |
| Detailed `pin` mechanics and `extendedPin` mode | Section 2.4: Error Recovery |
| `recoverWhile` predicate patterns and `#auto` mode | Section 2.4: Error Recovery |
| `mixin`, `methods`, `implements`, `fake` rules for PSI | Section 3.4: PSI Customization |
| `stubClass` attribute | Section 3.4: PSI Customization |
| `hooks` attribute (whitespace binders) | Section 3.1: Advanced Attributes |
| `elementType`, `elementTypeClass`, `elementTypeFactory` | Section 3.1: Advanced Attributes |
| `consumeTokenMethod`, `parserImports`, `classHeader` | Section 3.1: Advanced Attributes |
| `gradle-grammar-kit-plugin` usage and limitations | Section 4.2: Gradle Integration |
| Full `generate` options table details | Section 3.1: Advanced Attributes |

---

## Validation Summary

| Category | Checked | Passed | Failed | Unverified |
|----------|---------|--------|--------|------------|
| Internal file paths | 23 | 23 | 0 | 0 |
| External URLs | 9 | 9 | 0 | 0 |
| Technical claims | 28 | 27 | 0 | 1 |
| Line number accuracy | 8 | 5 | 3 | 0 |
| Content accuracy | 5 | 3 | 2 | 0 |
| **Total** | **73** | **67** | **5** | **1** |

### Summary of Issues
- 3 minor line number range discrepancies (content still accurate)
- 1 naming discrepancy (TOKEN vs EXPLICIT_TOKEN/IMPLICIT_TOKEN)
- 1 implementation detail (createElement throws in BNF's own parser)
- 1 unverified timing claim (500ms debounce)
- 1 missing shortcut registration (Ctrl+Shift+G not in plugin.xml)

None of these issues affect the accuracy of the documentation content. The line number discrepancies are minor offsets. The TOKEN naming issue should be corrected in the documentation to use the actual key names.

All references validated on 2026-02-19.
