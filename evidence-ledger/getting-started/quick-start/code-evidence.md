# Code Evidence: Quick Start Tutorial

## Scope Information
This evidence covers section 1.4: Quick Start Tutorial
- Your first grammar (rules, tokens, Live Preview, beginner patterns)
- Generating parser code (Ctrl+Shift+G, generated files, package structure)
- Creating a language plugin (Language, FileType, ParserDefinition, lexer, highlighting)
- Testing your parser (test files, PSI Viewer, basic tests)

---

## Your First Grammar

### Grammar File Structure
- File extension: `.bnf`
- Grammar file has two sections: header attributes block `{ ... }` and rules
- Header block contains `tokens`, `extends`, `name`, and other global attributes
- Rules follow the header, each in form: `rule_name ::= expression`
- Comments: `//` for line comments, `/* */` for block comments

### Token Definitions (in header block)
- Simple tokens: `SEMI=';'` (name=value, value in quotes)
- Regexp tokens: `number='regexp:\d+(\.\d*)?'` (prefixed with `regexp:`)
- Keyword tokens: unquoted values matching their names
- Whitespace token: `space='regexp:\s+'` (treated as whitespace in Live Preview if unused in rules)
- Comment token: `comment='regexp://.*'` (treated as comment in Live Preview if unused in rules)
- String token: `string="regexp:('([^'\\\\]|\\\\.)*'|\"([^\"\\\\]|\\\\.)*\")"` (double-quoted value)
- Source: `TUTORIAL.md` lines 85-103, `tokens.html`

### Basic Rule Syntax (beginner-level only)
- Sequence: `rule ::= part1 part2 part3`
- Choice: `rule ::= part1 | part2 | part3`
- Optional: `rule ::= [optional_part]` or `rule ::= optional_part?`
- Zero-or-more: `rule ::= part *`
- One-or-more: `rule ::= part +`
- Grouping: `rule ::= (group_a | group_b) rest`
- Rule reference: use rule name directly (e.g., `property ::= id '=' expr`)
- Token reference by value: use quoted string (e.g., `'='`, `';'`)
- Token reference by name: use token name (e.g., `SEMI`, `EQ`)
- Source: `README.md` lines 90-106

### Rule Modifiers (beginner-level)
- `private`: skip PSI node creation, children included in parent
- `left`: take previous sibling AST node and become its parent
- Default: rules are public (non-private, non-fake)
- Source: `README.md` lines 131-147

### Tutorial Grammar (complete, from TUTORIAL.md)
- Located at: `testData/livePreview/LivePreviewTutorial.bnf`
- Demonstrates: tokens block, extends pattern, name pattern, pin, recoverWhile, left rules
- Root rule: `root ::= root_item *`
- Private helper: `private root_item ::= !<<eof>> property ';' {pin=1 recoverWhile=property_recover}`
- Property rule: `property ::= id '=' expr {pin=2}`
- Recovery rule: `private property_recover ::= !(';' | id '=')`
- Expression rules use `left` modifier for operator precedence
- Pattern attributes: `name(".*expr")='expression'` and `extends(".*expr")=expr`

### Simpler Example Grammar (JSON)
- Located at: `testData/livePreview/Json.bnf`
- Demonstrates: tokens, extends, hooks, pin, recoverWhile in a simpler context
- 27 lines total, good beginner reference

### Common Beginner Patterns
- Root rule with repetition: `root ::= item *`
- Private wrapper with recovery: `private item ::= content {pin=1 recoverWhile=recover}`
- Recovery predicate (NOT predicate): `private recover ::= !(',' | ']' | '}')`
- Parenthesized expression: `paren_expr ::= '(' expr ')' {pin=1}`
- Literal alternatives: `literal ::= number | string`
- Source: `TUTORIAL.md` lines 109-127

---

## Generating Parser Code

### Running the Generator
- Action name: "Generate Parser Code"
- Shortcut: Ctrl+Shift+G (Windows/Linux), Cmd+Shift+G (macOS)
- Available from: context menu on `.bnf` files, editor popup menu
- Works on single or multiple `.bnf` files (batch generation)
- Runs as background task with progress indicator
- Source: `GenerateAction.java`, `GrammarKitBundle.properties` line 16

### Generation Notification
- Success: `"[filename].bnf generated ([size])"` with `"to [directory]"` detail
- Batch: `"[N] grammars: [M] files generated ([size]) in [duration]"` (shown when >3 files)
- Failure: `"[filename].bnf generation failed"` with stack trace
- Notification group: "Grammar Generator"
- Source: `GenerateAction.java` lines 126-191

### Default Output Directory
- System property: `grammar.kit.gen.dir` (default: `"gen"`)
- If `.bnf` file is in source root: generates alongside sources
- If `.bnf` file is in content root (not source): generates into `gen/` subdirectory
- Existing files are found by filename index and reused in place
- Source: `FileGeneratorUtil.java`, `Options.java` line 14

### Generated Files (from ParserGenerator.generate())
1. **Parser class** (e.g., `MyLanguageParser.java`)
   - Default: `generated.GeneratedParser`
   - Configured via: `parserClass` attribute
   - Contains static parse methods for each rule
   - Can be split across multiple classes for large grammars
2. **Element type holder class** (e.g., `MyLanguageTypes.java`)
   - Default: `generated.GeneratedTypes`
   - Configured via: `elementTypeHolderClass` attribute
   - Contains IElementType constants for rules and tokens
   - Contains PSI element factory method (if `generate=[psi-factory="yes"]`)
3. **PSI interface classes** (one per public rule)
   - Default package: `generated.psi`
   - Configured via: `psiPackage` attribute
   - Prefix: `psiClassPrefix` attribute (default: empty)
4. **PSI implementation classes** (one per public rule)
   - Default package: `generated.psi.impl`
   - Configured via: `psiImplPackage` attribute
   - Suffix: `psiImplClassSuffix` attribute (default: `"Impl"`)
5. **Visitor class** (optional)
   - Default name: `"Visitor"`
   - Configured via: `psiVisitorName` attribute
   - Can be disabled: `generate=[visitor="no"]`
- Source: `ParserGenerator.java` lines 277-341, `KnownAttribute.java`

### Generated Parser Structure
- Static method per rule: `static boolean rule_name(PsiBuilder, int)`
- Sub-expressions: `static boolean rule_name_0(..)`, `rule_name_N1_N2_..._NX(..)`
- Naming warning: avoid naming rules like `rule_name_N1_N2` (conflicts with generated sub-expression names)
- Source: `README.md` lines 113-119

### Key Global Attributes for Generation
- `parserClass`: default `"generated.GeneratedParser"`
- `elementTypeHolderClass`: default `"generated.GeneratedTypes"`
- `psiPackage`: default `"generated.psi"`
- `psiImplPackage`: default `"generated.psi.impl"`
- `psiClassPrefix`: default `""` (empty)
- `psiImplClassSuffix`: default `"Impl"`
- `psiVisitorName`: default `"Visitor"`
- `parserUtilClass`: default `"com.intellij.lang.parser.GeneratedParserUtilBase"`
- `generatePsi`: default `true`
- `generateTokens`: default `true`
- Source: `KnownAttribute.java` lines 29-48

### Generation Can Be Controlled
- `generate=[psi="no"]`: skip PSI class generation
- `generate=[tokens="no"]`: skip token constant generation
- `generate=[visitor="no"]`: skip visitor generation
- `generate=[java="11"]`: target Java version (default 11)
- Source: `generate.html`, `GenOptions.java`

---

## Creating a Language Plugin

### Language Class Pattern
- Extend `com.intellij.lang.Language`
- Singleton pattern: `public static final MyLanguage INSTANCE = new MyLanguage()`
- Constructor: `super("MyLanguage")` with language ID string
- Example: `BnfLanguage.java` - `super("BNF")`
- Source: `BnfLanguage.java`

### FileType Class Pattern
- Extend `com.intellij.openapi.fileTypes.LanguageFileType`
- Singleton pattern: `public static final MyFileType INSTANCE = new MyFileType()`
- Constructor: `super(MyLanguage.INSTANCE)`
- Required methods: `getName()`, `getDescription()`, `getDefaultExtension()`, `getIcon()`
- BNF example: extension `"bnf"`, name `"BNF"`
- Source: `BnfFileType.java`

### FileType Registration (plugin.xml)
- Extension point: `com.intellij.fileType`
- Attributes: `name`, `implementationClass`, `fieldName="INSTANCE"`, `extensions`, `language`
- Example: `<fileType name="BNF" implementationClass="org.intellij.grammar.BnfFileType" fieldName="INSTANCE" extensions="bnf" language="BNF"/>`
- Source: `plugin.xml` line 15

### ParserDefinition Pattern
- Implement `com.intellij.lang.ParserDefinition`
- Required methods:
  - `createLexer(Project)`: return lexer instance
  - `createParser(Project)`: return generated parser instance
  - `getFileNodeType()`: return `IFileElementType` singleton
  - `getWhitespaceTokens()`: return `TokenSet` of whitespace tokens
  - `getCommentTokens()`: return `TokenSet` of comment tokens
  - `getStringLiteralElements()`: return `TokenSet` of string literal tokens
  - `createElement(ASTNode)`: create PSI element from AST node
  - `createFile(FileViewProvider)`: return PsiFile implementation
- `IFileElementType` created as: `new IFileElementType("MY_FILE", MyLanguage.INSTANCE)`
- Source: `BnfParserDefinition.java`

### ParserDefinition Registration (plugin.xml)
- Extension point: `com.intellij.lang.parserDefinition`
- Attributes: `language`, `implementationClass`
- Example: `<lang.parserDefinition language="BNF" implementationClass="org.intellij.grammar.BnfParserDefinition"/>`
- Source: `plugin.xml` line 17

### Lexer Integration

#### Generating JFlex Lexer
- Action: "Generate JFlex Lexer" (context menu on `.bnf` file)
- Generates `.flex` file from BNF token definitions
- Output filename: `_[GrammarName]Lexer.flex` (prefixed with underscore)
- Uses Velocity template: `resources/templates/lexer.flex.template`
- Template produces: package, imports, class definition, token rules
- Source: `BnfGenerateLexerAction.java`

#### Running JFlex Generator
- Action: "Run JFlex Generator" (context menu on `.flex` file)
- Converts `.flex` file to Java lexer class
- Downloads JFlex 1.9.2 automatically if needed
- Source: `BnfRunJFlexAction.java`, `GrammarKitBundle.properties` line 15

#### Lexer Template Structure
- Implements `FlexLexer` interface
- Returns `IElementType` from `advance()` method
- Imports token constants from element type holder class
- Handles: `WHITE_SPACE`, regexp tokens, simple tokens, `BAD_CHARACTER`
- Source: `lexer.flex.template`

#### Regexp Token Conversion
- Java regex `\d` becomes JFlex `[0-9]`
- Java regex `\s` becomes JFlex `[ \t\n\x0B\f\r]`
- Java regex `\w` becomes JFlex `[a-zA-Z_0-9]`
- Java regex `\p{Alpha}` becomes JFlex `[:letter:]`
- Java regex `\p{Digit}` becomes JFlex `[:digit:]`
- Source: `BnfGenerateLexerAction.java` lines 238-253

### Simple Syntax Highlighting Pattern
- Extend `com.intellij.openapi.fileTypes.SyntaxHighlighterBase`
- Override `getHighlightingLexer()`: return lexer instance
- Override `getTokenHighlights(IElementType)`: map token types to `TextAttributesKey`
- Register via: `<lang.syntaxHighlighterFactory>` extension point
- BNF highlighter defines keys for: COMMENT, STRING, NUMBER, KEYWORD, RULE, TOKEN, ATTRIBUTE, OP_SIGN, PARENTHS, BRACES, BRACKETS, ANGLES, PIN_MARKER, RECOVER_MARKER, and more
- Source: `BnfSyntaxHighlighter.java`

### Syntax Highlighter Registration (plugin.xml)
- Extension point: `com.intellij.lang.syntaxHighlighterFactory`
- Attributes: `language`, `implementationClass`
- Example: `<lang.syntaxHighlighterFactory language="BNF" implementationClass="org.intellij.grammar.editor.BnfSyntaxHighlighterFactory"/>`
- Source: `plugin.xml` line 22

### Other Essential plugin.xml Registrations
- Annotator: `<annotator language="BNF" implementationClass="...BnfAnnotator"/>`
- Structure view: `<lang.psiStructureViewFactory language="BNF" implementationClass="..."/>`
- Find usages: `<lang.findUsagesProvider language="BNF" implementationClass="..."/>`
- Brace matcher: `<lang.braceMatcher language="BNF" implementationClass="..."/>`
- Commenter: `<lang.commenter language="BNF" implementationClass="..."/>`
- Completion: `<completion.contributor language="BNF" implementationClass="..."/>`
- Source: `plugin.xml` lines 14-32

---

## Using Live Preview

### Opening Live Preview
- Action name: "Live Preview"
- Shortcut: Ctrl+Alt+P (Windows/Linux), Cmd+Alt+P (macOS)
- Available from: context menu, editor popup, Tools menu
- Only enabled when a `.bnf` file is open
- Opens a split editor: grammar on one side, preview on the other
- Preview file named: `[grammar_name].bnf.preview`
- Source: `LivePreviewAction.java`, `plugin.xml` lines 114-116

### Live Preview Features
- Real-time parsing: grammar changes auto-reparse preview (500ms debounce)
- Structure view: Ctrl+F12 / Cmd+F12 shows PSI tree
- PSI Viewer dialog: inspect parse tree structure
- Grammar highlighting at caret: Ctrl+Alt+F7 / Cmd+Alt+F7 (in preview editor)
  - Highlights grammar expressions matching current caret position in preview
  - Toggle: "Start/Stop Grammar Highlighting"
- Source: `LivePreviewHelper.java`, `HighlightGrammarAtCaretAction.java`, `TUTORIAL.md` lines 47-49

### Live Preview Lexer Behavior
- Regexp tokens from `tokens` block are used for tokenization
- Whitespace: any `regexp` token matching spaces/newlines that is NOT used in rules
- Comments: similar auto-detection for comment-like regexp tokens
- No need for JFlex lexer during prototyping
- Source: `TUTORIAL.md` lines 79-80, `LivePreviewParserDefinition.java`

### Live Preview Limitations
- Simplified tokenization vs. real JFlex lexer
- Java RegExp syntax supported (JFlex only supports subset)
- Grammar-Kit attempts some obvious regex conversions
- Not useful after lexer is finalized (would need maintaining two lexers)
- Source: `TUTORIAL.md` lines 75-76, `README.md` lines 240-241

### Recommended Workflow (from TUTORIAL.md)
1. Prototype grammar in Live Preview
2. Generate initial `.flex` file and generate Java lexer from it
3. Create ParserDefinition and/or setup lexer and parser tests
4. Perfect `.flex` and `.bnf` separately in production environment
- Source: `TUTORIAL.md` lines 66-74

---

## Testing Your Parser

### PSI Viewer
- Tool: built-in IntelliJ "PSI Viewer" dialog
- Access: Tools > View PSI Structure (or internal mode)
- Shows: PSI tree for any file in the project
- Useful for: verifying parse tree structure, debugging grammar issues
- Structure view (Ctrl+F12) also shows PSI tree outline
- Source: `TUTORIAL.md` line 47

### Basic Parsing Tests (IntelliJ test framework)
- Base class: `ParsingTestCase` from IntelliJ test framework
- Test pattern: provide input text, compare against expected PSI tree dump
- Test data organization: input files and expected output files in `testData/` directory
- `LightPsi` class: standalone parsing API for testing without full IDE
  - Can parse files outside IDE context
  - Used for command-line parser validation
- Source: `LightPsi.java`

### Creating Test Files
- Input files: sample text in your language
- Expected files: PSI tree text representation
- Test data directory convention: `testData/` subdirectories
- Grammar-Kit's own test data: `testData/generator/`, `testData/livePreview/`, `testData/parser/`

### Validation Strategies
- Live Preview for rapid iteration (no code generation needed)
- PSI Viewer for structural verification
- Automated tests with `ParsingTestCase` for regression testing
- Inspections available in BNF editor:
  - Left recursion detection
  - Unresolved references
  - Unused rules
  - Duplicate rules
  - Suspicious tokens
  - Identical/unreachable choice branches
- Source: `plugin.xml` lines 56-79, `GrammarKitBundle.properties` lines 28-36

---

## Example Locations
- `TUTORIAL.md`: Complete tutorial with expression grammar, workflow summary
- `testData/livePreview/LivePreviewTutorial.bnf`: Tutorial grammar (43 lines)
- `testData/livePreview/Json.bnf`: JSON grammar (27 lines, simpler example)
- `testData/generator/ExprParser.bnf`: Expression parser (advanced, out of scope)
- `resources/templates/lexer.flex.template`: JFlex lexer template (48 lines)
- `src/org/intellij/grammar/BnfParserDefinition.java`: ParserDefinition example (79 lines)
- `src/org/intellij/grammar/BnfFileType.java`: FileType example (46 lines)
- `src/org/intellij/grammar/BnfLanguage.java`: Language class example (28 lines)
- `src/org/intellij/grammar/editor/BnfSyntaxHighlighter.java`: Syntax highlighter example (84 lines)
- `resources/META-INF/plugin.xml`: Plugin registration patterns (136 lines)
- `images/livePreview.png`: Live Preview screenshot
- `images/editor.png`: BNF editor screenshot

---

## Out of Scope
Features found but excluded (belong to other sections):

### Detailed Grammar Syntax (Section 2.1)
- Full PEG syntax details, predicates (`&`, `!`), external expressions (`<< >>`)
- `meta`, `external`, `fake`, `inner`, `upper` rule modifiers
- Pattern-based attribute application syntax
- Token precedence and conflict resolution

### Expression Parsing Details (Section 2.3)
- `extends(".*expr")=expr` pattern for flat PSI trees
- `left` modifier mechanics for operator precedence
- `rightAssociative` attribute
- `extraRoot` attribute
- Full ExprParser.bnf example

### Error Recovery (Section 2.4)
- Detailed `pin` mechanics and `extendedPin` mode
- `recoverWhile` predicate patterns
- `#auto` recovery mode
- `name` attribute for error messages
- Multi-level recovery strategies

### Advanced PSI Customization (Section 3.4)
- `mixin` attribute
- `methods` attribute with path syntax
- `implements` attribute
- `fake` rules for PSI shaping
- `stubClass` attribute
- `psiImplUtilClass` for method mix-ins

### Gradle Integration (Section 4.2)
- `gradle-grammar-kit-plugin` usage
- Gradle limitations (no method mixins, no two-pass generation)
- Build automation patterns

### Advanced Attributes (Section 3.1)
- `hooks` attribute (whitespace binders)
- `elementType`, `elementTypeClass`, `elementTypeFactory`
- `consumeTokenMethod` (regular/smart/fast)
- `parserImports` for external method resolution
- `classHeader` for license headers
- `generate` options table (full details)

---

## Missing Documentation
- No user docs for: PSI Viewer access path (varies by IDE version/mode)
- No user docs for: exact `ParsingTestCase` setup steps with Grammar-Kit
- No user docs for: minimal `build.gradle` for a Grammar-Kit language plugin
- Attribute `generate` has many undocumented sub-options (only partial table in `generate.html`)
- No user docs for: how to debug generated parser code step-by-step
