# Code Evidence: Features (Section 1.2)

## Scope Information
This evidence covers section 1.2: Features
- Overview of BNF grammar support and parser generation
- Key features and capabilities
- Relationship to IntelliJ Platform language support
- When to use Grammar-Kit

---

## Plugin Identity
- Plugin ID: `org.jetbrains.idea.grammar`
- Plugin name: "Grammar-Kit"
- Description: "BNF Grammars and JFlex lexers editor. Readable parser/PSI code generator."
- Vendor: JetBrains
- Requires Java 17 (since 2022.3)
- Source: `resources/META-INF/plugin.xml`

## File Types Supported
- **BNF files**: `.bnf` extension, language ID `BNF`
  - Source: `plugin.xml` line 15, `BnfFileType.java`
- **JFlex files**: `.flex` extension, language ID `JFlex`
  - Source: `plugin.xml` line 96, `JFlexFileType.java`
- **Live Preview files**: virtual file type `BNF_LP`, language ID `BNF_LP`
  - Source: `plugin.xml` line 16, `LivePreviewFileType.java`

---

## Editor Features: BNF

### Syntax Highlighting
- 20 customizable color/font elements via Settings > Colors and Fonts
- Configurable elements:
  - Illegal character, Comment, String, Number, Keyword
  - Explicit token, Implicit token
  - Rule, Meta rule, Meta rule parameter
  - Attribute, Pattern, External
  - Parenthesis, Braces, Brackets, Angles
  - Operation sign, Pin marker, Recover marker
- Color settings page with live preview demo text
- Source: `BnfSyntaxHighlighter.java`, `BnfColorSettingsPage.java`

### Semantic Annotations (BnfAnnotator)
- Rules colored differently based on type (regular vs meta)
- Attributes highlighted distinctly
- Modifiers (`private`, `external`, `meta`, etc.) highlighted as keywords
- External references highlighted with dedicated color
- Meta rule parameters highlighted distinctly
- Explicit tokens vs implicit tokens distinguished by color
- Text-matched tokens show info message: "Tokens matched by text are slower than tokens matched by types"
- Rules with `recoverWhile` attribute get recover marker highlighting
- Boolean values (`true`/`false`) in attributes highlighted as keywords
- Source: `editor/BnfAnnotator.java`

### Pin Marker Annotations (BnfPinMarkerAnnotator)
- Pinned expressions visually marked in editor
- Tooltip shows pin attribute value in charge
- Nested pins show "Pinned again" message
- Source: `editor/BnfPinMarkerAnnotator.java`

### Code Completion
- Attribute name completion (context-aware: global vs rule-level)
- Rule name completion with icons (bold for public, strikethrough for fake)
- Token name completion from explicit token definitions
- Implicit token name completion from rule bodies
- Keyword completion: `private`, `external`, `meta`, `left`, `inner`, `upper`, `fake`
- External expression: completes static methods from `parserUtilClass`
- Meta rule references filtered in external expressions
- Source: `BnfCompletionContributor.java`

### Code Folding
- Global attribute blocks fold to `{..}`
- Rule-level attribute blocks fold to `{..}`
- Value lists fold to `[..]`
- Block comments fold to `/*..*/`
- Global attribute blocks collapsed by default
- Value lists collapsed by default
- Source: `BnfFoldingBuilder.java`

### Structure View
- Quick structure popup: Ctrl+F12 / Cmd+F12
- Shows rules and attribute blocks
- Attributes display as: `name(pattern) = value`
- Sortable tree (alphabetical)
- Rules shown as leaf nodes
- Source: `BnfStructureViewFactory.java`

### Quick Documentation (Ctrl+Q / Cmd+J)
- **Rule documentation shows:**
  - FIRST set (starts with)
  - FOLLOW set (followed by)
  - `#auto` recovery predicate expansion
  - Expression priority table (for expression rules)
  - Contained public rules with cardinality
  - Contained tokens with cardinality
  - Contained external rules
- **Attribute documentation shows:**
  - Attribute description from HTML files in `resources/messages/attributeDescriptions/`
- Source: `BnfDocumentationProvider.java`

### Find Usages
- Find usages for rules (Alt+F7)
- Find usages for attributes
- Attribute pattern reference search
- Source: `BnfFindUsagesProvider.java`, `BnfAttrPatternRefSearcher`

### Navigation
- Go to related file: Ctrl+Alt+Home / Cmd+Alt+Home
  - Navigates to generated parser and PSI code
  - Gutter icon shows "Click to navigate to parser and PSI code"
  - Sub-expression navigation via GotoRelated action
- Navigate to matched expressions: Ctrl+B / Cmd+B inside attribute patterns
- Recursive rule gutter icon (recursive method icon in gutter)
- Source: `BnfRuleLineMarkerProvider.java`, `BnfRecursionLineMarkerProvider.java`

### Brace Matching
- Matched pairs: `()`, `{}`, `[]`, `<<>>`
- Source: `BnfBraceMatcher.java`

### Commenter
- Line comment: `//`
- Block comment: `/* */`
- Source: `BnfCommenter.java`

### Spellchecking
- Spell checking support for BNF files
- Source: `BnfSpellCheckingStrategy.java`

### Word Selection
- Extended word selection for BNF expressions
- Source: `BnfWordSelectioner.java`

### Move Left/Right
- Move elements left/right within sequences
- Source: `BnfMoveLeftRightHandler.java`

### Quote Handling
- Auto-close quotes in BNF files
- Source: `BnfQuoteHandler.java`

### RegExp Injection
- String literals with `regexp:` prefix get RegExp language injection
- Source: `BnfStringRegexpInjector.java`, `BnfStringRegexHost` (with Java plugin)

---

## Editor Features: JFlex

### Syntax Highlighting
- JFlex-specific syntax highlighter
- Customizable colors via Settings > Colors and Fonts
- Source: `JFlexSyntaxHighlighterFactory.java`, `JFlexColorSettingsPage.java`

### Code Completion
- Keywords and `%` directives
- Context-aware suggestions
- Source: `JFlexCompletionContributor.java`

### Annotations
- Macro highlighting, state highlighting
- Unresolved reference detection
- Source: `JFlexAnnotator.java`

### Find Usages
- Find usages for JFlex macros and states
- Source: `JFlexFindUsagesProvider.java`

### Structure View
- JFlex file structure popup
- Source: `JFlexStructureViewFactory.java`

### Brace Matching
- Matched pairs in JFlex files
- Source: `JFlexBraceMatcher.java`

### Commenter
- Line/block comments for JFlex
- Source: `JFlexCommenter.java`

### Refactoring
- Rename support for JFlex elements
- Source: `JFlexRefactoringSupportProvider.java`

### Quote Handling
- Auto-close quotes in JFlex files
- Source: `JFlexQuoteHandler.java`

---

## Refactoring Features

### Extract Rule (Introduce Rule)
- Shortcut: Ctrl+Alt+M / Cmd+Alt+M (same as Extract Method)
- Extracts selected expression into a new named rule
- Works in injected fragments
- Source: `BnfIntroduceRuleAction.java`, `BnfIntroduceRuleHandler.java`

### Introduce Token
- Shortcut: Ctrl+Alt+C / Cmd+Alt+C (same as Introduce Constant)
- Extracts token into named token definition
- Source: `BnfIntroduceTokenAction.java`, `BnfIntroduceTokenHandler.java`

### Inline Rule
- Replaces rule references with rule body
- Supports "inline this occurrence only" and "inline all and remove"
- Handles meta rule inlining with parameter substitution
- Source: `BnfInlineRuleProcessor.java`, `BnfInlineRuleActionHandler.java`

### Rename (In-place)
- In-place rename for rules and attributes
- Source: `BnfRefactoringSupportProvider.java`

### Unwrap/Remove Expression
- Shortcut: Ctrl+Shift+Del / Cmd+Shift+Del
- Unwraps parenthesized expressions `()`, `[]`, `{}`
- Handles quantifiers and predicates on unwrap
- Source: `BnfUnwrapDescriptor.java`

---

## Inspections (All Enabled by Default, WARNING Level)

### 1. Unresolved BNF References
- Display name: "Unresolved BNF references"
- Detects: unresolved rule references, token references, method references
- Messages:
  - "Unresolved rule reference"
  - "Unresolved method reference"
  - "Unresolved rule or method reference"
  - "Pattern does not match any rule"
- Source: `BnfResolveInspection.java`

### 2. Unused Rule
- Display name: "Unused rule"
- Detects: unused rules, unreachable rules, unused fake rules, reachable fake rules
- Messages: "Unused rule", "Unreachable rule", "Unused fake rule", "Reachable fake rule"
- Also warns: "Non-private recovery rule" for recoverWhile targets
- Whole-file inspection (analyzes rule graph)
- Source: `BnfUnusedRuleInspection.java`

### 3. Unused Attribute
- Display name: "Unused attribute"
- Detects: unknown attribute names, deprecated attribute names
- Message: "Unused attribute" or "Deprecated attribute, use 'X' instead"
- Source: `BnfUnusedAttributeInspection.java`

### 4. Suspicious Token
- Display name: "Suspicious token"
- Detects: tokens that look like rule references (mixed case, contains `-` or `_`)
- Message: "'X' token looks like a reference to a missing rule"
- Quick fix: "Create 'X' rule" (creates private rule stub)
- Source: `BnfSuspiciousTokenInspection.java`, `CreateRuleFromTokenFix.java`

### 5. Left Recursion
- Display name: "Left recursion"
- Detects: direct left recursion unsupported by generator
- Message: "'X' employs left-recursion unsupported by generator"
- Description: "Detects left recursion which leads to StackOverflowError"
- Skips fake rules and expression-parsing rules
- Source: `BnfLeftRecursionInspection.java`

### 6. Duplicate Rule
- Display name: "Duplicate rule"
- Detects: rules with non-unique names
- Message: "'X' rule is defined more than once"
- Source: `BnfDuplicateRuleInspection.java`

### 7. Identical Choice Branches
- Display name: "Identical choice branches"
- Detects: duplicate branches in choice expressions
- Message: "Duplicate choice branch"
- Quick fix: "Remove expression"
- Source: `BnfIdenticalChoiceBranchesInspection.java`

### 8. Unreachable Choice Branch
- Display name: "Unreachable choice branch"
- Detects: branches preceded by empty-matching branches, branches unable to match
- Messages:
  - "Branch matches empty input making the rest branches unreachable"
  - "Branch is unable to match anything due to & or ! conditions"
- Source: `BnfUnreachableChoiceBranchInspection.java`

### Inspection Suppression
- Suppress for rule (comment before rule)
- Suppress for attribute (comment before attribute)
- Suppress for file (comment at file start)
- Uses `//noinspection` comment syntax
- Source: `BnfInspectionSuppressor.java`

---

## Intentions (via Alt+Enter)

### 1. Flip Choice Branches
- Category: "Grammar-Kit BNF"
- Description: "Flip arguments of a given choice"
- Source: `BnfFlipChoiceIntention`, `intentionDescriptions/BnfFlipChoiceIntention/description.html`

### 2. Convert Optional Expression
- Category: "Grammar-Kit BNF"
- Description: "Converts `?` expressions to `[]` expressions and vice-versa"
- Source: `BnfConvertOptExpressionIntention`, `intentionDescriptions/BnfConvertOptExpressionIntention/description.html`

---

## Generation Features

### Generate Parser Code
- Action name: "Generate Parser Code"
- Shortcut: Ctrl+Shift+G / Cmd+Shift+G
- Available from: Tools menu, Editor popup menu, Project view popup menu
- Generates: parser class, element types, PSI interfaces, PSI implementations
- Batch generation: multiple `.bnf` files at once
- Background task with progress indicator
- Notification on completion: file count, total size, duration
- Two-pass generation (IDE only, not available in Gradle)
- Source: `GenerateAction.java`, `plugin-java.xml`

### Generate JFlex Lexer
- Action name: "Generate JFlex Lexer"
- Creates `.flex` file from BNF token definitions
- Uses Velocity template (`templates/lexer.flex.template`)
- Separates simple tokens and regexp tokens
- Converts Java regex patterns to JFlex syntax
- File save dialog for output location
- Source: `BnfGenerateLexerAction.java`

### Run JFlex Generator
- Action name: "Run JFlex Generator"
- Shortcut: same as Generate Parser Code (Ctrl+Shift+G)
- Processes `.flex` files to generate Java lexer code
- Auto-downloads JFlex 1.9.2 jar if not found
- Creates global library "JFlex & idea-flex.skeleton"
- Console output in Messages tool window
- Batch processing support
- Source: `BnfRunJFlexAction.java`

### Generate Parser Util
- Action name: "Generate Parser Util"
- Generates custom `parserUtilClass` skeleton
- Source: `BnfGenerateParserUtilAction.java`

---

## Live Preview Features

### Open Live Preview
- Shortcut: Ctrl+Alt+P / Cmd+Alt+P
- Available from: Tools menu, Editor popup menu, Project view popup menu
- Opens split editor with preview pane
- Creates virtual file: `{grammar-name}.preview`
- Source: `LivePreviewAction.java`, `LivePreviewHelper.java`

### Real-time Grammar Evaluation
- Auto-reparses preview when BNF file changes
- 500ms debounce on grammar changes
- Structure view integration for preview
- Syntax highlighting in preview based on grammar
- Source: `LivePreviewHelper.java` (MergingUpdateQueue, 500ms delay)

### Grammar Highlighting at Caret
- Shortcut: Ctrl+Alt+F7 / Cmd+Alt+F7 (in preview editor)
- Toggle action: Start/Stop grammar evaluator highlighting
- Highlights which grammar expressions match at caret position
- Tracks expression matching results (success/failure)
- Source: `HighlightGrammarAtCaretAction.java`, `LivePreviewHelper.collectExpressionsAtOffset()`

### Live Preview Infrastructure
- Dynamic language registration per grammar file
- Structure view for preview files
- Parser definition for preview files
- Lexer for preview files (from grammar tokens)
- Source: `LivePreviewLanguage`, `LivePreviewParserDefinition`, `LivePreviewLexer`

---

## Diagram Support (Optional)

- PSI tree diagram (requires UML plugin)
- Diagram provider: `BnfDiagramProvider`
- Optional dependency: `com.intellij.diagram`
- Source: `plugin-uml.xml`, `diagram/BnfDiagramProvider.java`

---

## Platform Integration Points

### Required Dependencies
- `com.intellij.modules.lang` (core language support)
- Source: `plugin.xml` line 9

### Optional Dependencies
- `com.intellij.copyright` - Copyright support for generated files
- `com.intellij.java` - Java-aware features (PSI navigation, RegExp hosting, generation actions)
- `com.intellij.diagram` - UML diagram support
- Source: `plugin.xml` lines 10-12

### Language API Integration
- `lang.parserDefinition` - BNF and JFlex parser definitions
- `lang.syntaxHighlighterFactory` - Syntax highlighting for BNF, JFlex, and Live Preview
- `lang.findUsagesProvider` - Find usages for BNF and JFlex
- `lang.braceMatcher` - Brace matching for BNF and JFlex
- `lang.psiStructureViewFactory` - Structure view for BNF and JFlex
- `lang.commenter` - Comment/uncomment for BNF and JFlex
- `lang.refactoringSupport` - Refactoring for BNF and JFlex
- `lang.foldingBuilder` - Code folding for BNF
- `lang.namesValidator` - Name validation for BNF
- `lang.unwrapDescriptor` - Unwrap expressions for BNF
- `lang.inspectionSuppressor` - Inspection suppression for BNF
- `lang.elementManipulator` - String manipulation for BNF
- `lang.ast.factory` - AST node factory for BNF and JFlex
- Source: `plugin.xml`

### PSI Foundation
- Generated parser produces `PsiElement` implementations
- Generated PSI interfaces and implementation classes
- Element type constants (`IElementType`)
- Visitor pattern generation
- Stub-based PSI support
- Source: `README.md` (general usage instructions)

### Extension Points Used
- `annotator` - 3 annotators for BNF, 1 for JFlex
- `codeInsight.lineMarkerProvider` - 2 providers (related code, recursion)
- `completion.contributor` - BNF and JFlex completion
- `documentationProvider` - Quick documentation
- `localInspection` - 8 inspections
- `intentionAction` - 2 intentions
- `colorSettingsPage` - BNF and JFlex color settings
- `languageInjector` - RegExp injection in BNF strings
- `spellchecker.support` - Spell checking for BNF
- `highlightingPassFactory` - Grammar-at-caret highlighting pass
- Source: `plugin.xml`

---

## Keyboard Shortcuts Summary

| Action | Windows/Linux | macOS |
|--------|--------------|-------|
| Generate Parser Code | Ctrl+Shift+G | Cmd+Shift+G |
| Live Preview | Ctrl+Alt+P | Cmd+Alt+P |
| Grammar Highlighting (in preview) | Ctrl+Alt+F7 | Cmd+Alt+F7 |
| Extract Rule | Ctrl+Alt+M | Cmd+Alt+M |
| Introduce Token | Ctrl+Alt+C | Cmd+Alt+C |
| Unwrap Expression | Ctrl+Shift+Del | Cmd+Shift+Del |
| Structure Popup | Ctrl+F12 | Cmd+F12 |
| Go to Related File | Ctrl+Alt+Home | Cmd+Alt+Home |
| Quick Documentation | Ctrl+Q | Cmd+J |
| Navigate to Declaration | Ctrl+B | Cmd+B |
| Find Usages | Alt+F7 | Alt+F7 |
| Intentions | Alt+Enter | Alt+Enter |
| Run JFlex Generator | Ctrl+Shift+G | Cmd+Shift+G |

---

## When to Use Grammar-Kit (Evidence from Real Projects)

### Open-source plugins built with Grammar-Kit
- Clojure-Kit (Clojure language)
- intellij-rust (Rust language)
- intellij-erlang (Erlang language)
- intellij-elm (Elm language)
- intellij-elixir (Elixir language)
- Perl5-IDEA (Perl language)
- Dart (Dart language, JetBrains)
- intellij-haxe (Haxe language)
- Cypher (Graph database query language)
- Source: `README.md` lines 23-31

### Use Case Categories (from project evidence)
- **Programming languages**: Rust, Erlang, Elm, Elixir, Perl, Dart, Haxe
- **Domain-specific languages**: Clojure, Cypher (graph queries)
- **Configuration/data formats**: JSON (testData example)
- **Scripting languages**: Multiple examples above
- Source: `README.md`, `testData/livePreview/Json.bnf`

---

## Example Locations
- `testData/livePreview/Json.bnf` - Complete JSON grammar with error recovery
- `testData/livePreview/LivePreviewTutorial.bnf` - Tutorial grammar for Live Preview
- `testData/generator/ExprParser.bnf` - Expression parser with precedence
- `testData/generator/PsiGen.bnf` - PSI generation patterns
- `testData/generator/AutoRecovery.bnf` - Auto recovery patterns
- `grammars/Grammar.bnf` - Grammar-Kit's own BNF grammar (self-hosted)
- `images/editor.png` - Screenshot of BNF editor features
- `images/livePreview.png` - Screenshot of Live Preview interface

---

## Out of Scope
Features found but excluded (belong to other sections):
- Detailed grammar syntax (rule modifiers, meta rules, tokens) -> Section 2.1
- Attribute system details (pin, recoverWhile, extends, etc.) -> Section 3.1
- Expression parsing specifics -> Section 2.3
- Error recovery details (pin/recoverWhile mechanics) -> Section 2.4
- Live Preview workflow details -> Section 2.5
- PSI customization (mixin, methods, fake rules) -> Section 3.4
- Gradle plugin usage -> Section 4.2
- Installation steps -> Section 1.3
- Tutorial content -> Section 1.4

---

## Missing Documentation
- No user docs for: BnfExpressionMarkerAnnotator (registered but currently a no-op/todo)
- No user docs for: BnfGenerateParserUtilAction (generates parserUtilClass skeleton)
- No user docs for: Fleet-specific generation actions (Fleet: Generate Parser Code, etc.)
- No user docs for: Copyright plugin integration
- Inspection descriptions are minimal (1-2 sentences each)
- No keyboard shortcut reference page in existing docs
