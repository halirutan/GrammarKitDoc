# References: Features

## Scope Information

This validates references for section 1.2: Features.
Covers Grammar-Kit's feature overview including BNF editing, code generation, Live Preview, JFlex support, and IntelliJ Platform integration.

## Internal Links

- Prerequisites: `getting-started/introduction` (Section 1.1 - What is Grammar-Kit?)
- Related: `getting-started/installation` (Section 1.3 - Installation and Setup)
- Related: `getting-started/quick-start` (Section 1.4 - Quick Start Tutorial)
- Advanced: `grammar-development/live-preview` (Section 2.5 - Live Preview Workflow)
- Advanced: `code-generation/attributes` (Section 3.1 - Attributes System)
- Advanced: `integration/language-features` (Section 4.1.2 - Language Features)

---

## Code References

### Primary Documentation Sources

| Reference | Path | Status |
|-----------|------|--------|
| README.md "Plugin features" section | `Grammar-Kit/README.md#L54-L78` | Verified - 20 features listed |
| Plugin descriptor | `Grammar-Kit/resources/META-INF/plugin.xml` | Verified - all extensions registered |
| Plugin descriptor (Java-dependent) | `Grammar-Kit/resources/META-INF/plugin-java.xml` | Verified - generator actions, Java helpers |
| Plugin descriptor (UML-dependent) | `Grammar-Kit/resources/META-INF/plugin-uml.xml` | Verified - diagram provider |
| Plugin descriptor (Copyright) | `Grammar-Kit/resources/META-INF/plugin-copyright.xml` | Verified - copyright support |
| Bundle (inspection names) | `Grammar-Kit/resources/messages/GrammarKitBundle.properties#L28-L36` | Verified - 8 inspections + group |

### Image Assets

| Image | Path | Status | Description |
|-------|------|--------|-------------|
| Editor screenshot | `Grammar-Kit/images/editor.png` | Verified - exists | Shows BNF editor with syntax highlighting, structure view |
| Live Preview screenshot | `Grammar-Kit/images/livePreview.png` | Verified - exists | Shows Live Preview editor with parse tree |

---

## Feature Verification

### 1. Syntax Highlighting

| Feature | Source File | Status |
|---------|------------|--------|
| BNF syntax highlighter | `src/org/intellij/grammar/editor/BnfSyntaxHighlighter.java` | Verified |
| BNF highlighter factory | `src/org/intellij/grammar/editor/BnfSyntaxHighlighterFactory.java` | Verified |
| BNF annotator (semantic) | `src/org/intellij/grammar/editor/BnfAnnotator.java` | Verified |
| Pin marker annotator | `src/org/intellij/grammar/editor/BnfPinMarkerAnnotator.java` | Verified |
| Expression marker annotator | `src/org/intellij/grammar/editor/BnfExpressionMarkerAnnotator.java` | Verified |
| Color settings page | `src/org/intellij/grammar/editor/BnfColorSettingsPage.java` | Verified |
| JFlex syntax highlighter | `src/org/intellij/jflex/editor/JFlexSyntaxHighlighterFactory.java` | Verified |
| JFlex annotator | `src/org/intellij/jflex/editor/JFlexAnnotator.java` | Verified |
| JFlex color settings | `src/org/intellij/jflex/editor/JFlexColorSettingsPage.java` | Verified |
| Live Preview highlighter | `src/org/intellij/grammar/livePreview/LivePreviewSyntaxHighlighterFactory.java` | Verified |

**Customizable color keys** (from `BnfSyntaxHighlighter.java`):
Illegal, Comment, String, Pattern, Number, Keyword, Explicit Token, Implicit Token, Rule, Meta Rule, Meta Param, Attribute, External, Parentheses, Braces, Brackets, Angles, Op Sign, Recover Marker, Pin Marker (20 color keys total).

### 2. Code Completion

| Feature | Source File | Status |
|---------|------------|--------|
| BNF completion contributor | `src/org/intellij/grammar/BnfCompletionContributor.java` | Verified |
| JFlex completion contributor | `src/org/intellij/jflex/editor/JFlexCompletionContributor.java` | Verified |

Registered in `plugin.xml#L32`: `order="before javaClassName"`.

### 3. Navigation

| Feature | Source File | Status |
|---------|------------|--------|
| Structure view (BNF) | `src/org/intellij/grammar/BnfStructureViewFactory.java` | Verified |
| Structure view (JFlex) | `src/org/intellij/jflex/editor/JFlexStructureViewFactory.java` | Verified |
| Structure view (Live Preview) | `src/org/intellij/grammar/livePreview/LivePreviewStructureViewFactory.java` | Verified |
| Find usages (BNF) | `src/org/intellij/grammar/BnfFindUsagesProvider.java` | Verified |
| Find usages (JFlex) | `src/org/intellij/jflex/editor/JFlexFindUsagesProvider.java` | Verified |
| Rule line markers (go to PSI/parser) | `src/org/intellij/grammar/editor/BnfRuleLineMarkerProvider.java` | Verified |
| Recursion line markers | `src/org/intellij/grammar/editor/BnfRecursionLineMarkerProvider.java` | Verified |
| Attribute pattern ref search | `src/org/intellij/grammar/psi/BnfAttrPatternRefSearcher.java` | Verified (registered in plugin.xml#L43) |

### 4. Refactoring

| Feature | Source File | Status |
|---------|------------|--------|
| Introduce Rule (Extract Method) | `src/org/intellij/grammar/refactor/BnfIntroduceRuleAction.java` | Verified |
| Introduce Rule handler | `src/org/intellij/grammar/refactor/BnfIntroduceRuleHandler.java` | Verified |
| Introduce Rule popup | `src/org/intellij/grammar/refactor/BnfIntroduceRulePopup.java` | Verified |
| Introduce Token (Extract Constant) | `src/org/intellij/grammar/refactor/BnfIntroduceTokenAction.java` | Verified |
| Introduce Token handler | `src/org/intellij/grammar/refactor/BnfIntroduceTokenHandler.java` | Verified |
| Inline Rule | `src/org/intellij/grammar/refactor/BnfInlineRuleActionHandler.java` | Verified |
| Inline Rule processor | `src/org/intellij/grammar/refactor/BnfInlineRuleProcessor.java` | Verified |
| Inline Rule dialog | `src/org/intellij/grammar/refactor/InlineRuleDialog.java` | Verified |
| Inline view descriptor | `src/org/intellij/grammar/refactor/BnfInlineViewDescriptor.java` | Verified |
| Unwrap/remove expression | `src/org/intellij/grammar/refactor/BnfUnwrapDescriptor.java` | Verified |
| Refactoring support (in-place rename) | `src/org/intellij/grammar/refactor/BnfRefactoringSupportProvider.java` | Verified |
| Names validator | `src/org/intellij/grammar/refactor/BnfNamesValidator.java` | Verified |
| JFlex refactoring support | `src/org/intellij/jflex/editor/JFlexRefactoringSupportProvider.java` | Verified |

**Keyboard shortcuts** (from `plugin.xml` and `plugin-java.xml`):
- Introduce Rule: uses `ExtractMethod` shortcut (Ctrl-Alt-M / Cmd-Alt-M)
- Introduce Token: uses `IntroduceConstant` shortcut (Ctrl-Alt-C / Cmd-Alt-C)

### 5. Intentions

| Intention | Source File | Description File | Status |
|-----------|------------|-----------------|--------|
| Flip choice branches | `src/org/intellij/grammar/intention/BnfFlipChoiceIntention.java` | `resources/intentionDescriptions/BnfFlipChoiceIntention/description.html` | Verified |
| Convert optional expression (`?` to `[]` and vice-versa) | `src/org/intellij/grammar/intention/BnfConvertOptExpressionIntention.java` | `resources/intentionDescriptions/BnfConvertOptExpressionIntention/description.html` | Verified |

Both intentions include before/after templates:
- `BnfFlipChoiceIntention/before.bnf.template`, `after.bnf.template`
- `BnfConvertOptExpressionIntention/before.bnf.template`, `after.bnf.template`

### 6. Inspections (8 total)

| Inspection | Source File | Description File | Display Name |
|------------|------------|-----------------|--------------|
| Unresolved BNF references | `inspection/BnfResolveInspection.java` | `inspectionDescriptions/BnfResolve.html` | "Unresolved BNF references" |
| Unused rule | `inspection/BnfUnusedRuleInspection.java` | `inspectionDescriptions/BnfUnusedRule.html` | "Unused rule" |
| Unused attribute | `inspection/BnfUnusedAttributeInspection.java` | `inspectionDescriptions/BnfUnusedAttribute.html` | "Unused attribute" |
| Suspicious token | `inspection/BnfSuspiciousTokenInspection.java` | `inspectionDescriptions/BnfSuspiciousToken.html` | "Suspicious token" |
| Left recursion | `inspection/BnfLeftRecursionInspection.java` | `inspectionDescriptions/BnfLeftRecursion.html` | "Left recursion" |
| Duplicate rule | `inspection/BnfDuplicateRuleInspection.java` | `inspectionDescriptions/BnfDuplicateRule.html` | "Duplicate rule" |
| Identical choice branches | `inspection/BnfIdenticalChoiceBranchesInspection.java` | `inspectionDescriptions/BnfIdenticalChoiceBranches.html` | "Identical choice branches" |
| Unreachable choice branch | `inspection/BnfUnreachableChoiceBranchInspection.java` | `inspectionDescriptions/BnfUnreachableChoiceBranch.html` | "Unreachable choice branch" |

All inspections are registered in `plugin.xml#L56-L79`, all at WARNING level, all enabled by default.
Inspection suppressor: `inspection/BnfInspectionSuppressor.java` (registered in `plugin.xml#L54`).
Inspection group: "Grammar-Kit BNF" (from `GrammarKitBundle.properties#L28`).

### 7. Documentation Provider

| Feature | Source File | Status |
|---------|------------|--------|
| Documentation provider | `src/org/intellij/grammar/BnfDocumentationProvider.java` | Verified |

Provides: FIRST set, FOLLOWS set, PSI content, expression info for rules; attribute documentation for attributes. Registered in `plugin.xml#L52`.

### 8. Live Preview

| Feature | Source File | Status |
|---------|------------|--------|
| Live Preview action | `src/org/intellij/grammar/actions/LivePreviewAction.java` | Verified |
| Highlight grammar at caret | `src/org/intellij/grammar/actions/HighlightGrammarAtCaretAction.java` | Verified |
| Live Preview helper (core) | `src/org/intellij/grammar/livePreview/LivePreviewHelper.java` | Verified |
| Live Preview parser | `src/org/intellij/grammar/livePreview/LivePreviewParser.java` | Verified |
| Live Preview lexer | `src/org/intellij/grammar/livePreview/LivePreviewLexer.java` | Verified |
| Live Preview language | `src/org/intellij/grammar/livePreview/LivePreviewLanguage.java` | Verified |
| Live Preview file type | `src/org/intellij/grammar/livePreview/LivePreviewFileType.java` | Verified |
| Live Preview element type | `src/org/intellij/grammar/livePreview/LivePreviewElementType.java` | Verified |
| Live Preview parser definition | `src/org/intellij/grammar/livePreview/LivePreviewParserDefinition.java` | Verified |
| Live Preview structure view | `src/org/intellij/grammar/livePreview/LivePreviewStructureViewFactory.java` | Verified |
| Live Preview syntax highlighter | `src/org/intellij/grammar/livePreview/LivePreviewSyntaxHighlighterFactory.java` | Verified |
| Grammar at caret pass factory | `src/org/intellij/grammar/livePreview/GrammarAtCaretPassFactory.java` | Verified (registered in plugin.xml#L24) |

**Keyboard shortcuts** (from `plugin.xml`):
- Open Live Preview: `Ctrl-Alt-P` (registered in `plugin.xml#L115`)
- Highlight grammar at caret: `Ctrl-Alt-F7` (registered in `plugin.xml#L124`)

### 9. Code Generation

| Feature | Source File | Status |
|---------|------------|--------|
| Generate parser/PSI | `src/org/intellij/grammar/actions/GenerateAction.java` | Verified |
| Generate JFlex lexer | `src/org/intellij/grammar/actions/BnfGenerateLexerAction.java` | Verified |
| Generate ParserUtil class | `src/org/intellij/grammar/actions/BnfGenerateParserUtilAction.java` | Verified |
| Run JFlex generator | `src/org/intellij/grammar/actions/BnfRunJFlexAction.java` | Verified |
| Parser generator (core) | `src/org/intellij/grammar/generator/ParserGenerator.java` | Verified |
| Generator base | `src/org/intellij/grammar/generator/GeneratorBase.java` | Verified |
| Expression generator helper | `src/org/intellij/grammar/generator/ExpressionGeneratorHelper.java` | Verified |
| Fleet code generation | `src/org/intellij/grammar/fleet/GenerateFleetAction.java` | Verified |
| Fleet lexer generation | `src/org/intellij/grammar/fleet/BnfGenerateFleetLexerAction.java` | Verified |
| Fleet JFlex runner | `src/org/intellij/grammar/fleet/BnfRunFleetJFlexAction.java` | Verified |

**Keyboard shortcuts** (from `plugin-java.xml`):
- Generate parser/PSI: `Ctrl-Shift-G` (registered in `plugin-java.xml#L18`)
- Run JFlex: uses same shortcut as Generate (`Ctrl-Shift-G`, context-dependent)

### 10. Additional Editor Features

| Feature | Source File | Status |
|---------|------------|--------|
| Brace matching (BNF) | `src/org/intellij/grammar/BnfBraceMatcher.java` | Verified |
| Brace matching (JFlex) | `src/org/intellij/jflex/editor/JFlexBraceMatcher.java` | Verified |
| Code folding | `src/org/intellij/grammar/BnfFoldingBuilder.java` | Verified |
| Commenter (BNF) | `src/org/intellij/grammar/BnfCommenter.java` | Verified |
| Commenter (JFlex) | `src/org/intellij/jflex/editor/JFlexCommenter.java` | Verified |
| Quote handler (BNF) | `src/org/intellij/grammar/editor/BnfQuoteHandler.java` | Verified |
| Quote handler (JFlex) | `src/org/intellij/jflex/editor/JFlexQuoteHandler.java` | Verified |
| Word selectioner | `src/org/intellij/grammar/editor/BnfWordSelectioner.java` | Verified |
| Move left/right handler | `src/org/intellij/grammar/editor/BnfMoveLeftRightHandler.java` | Verified |
| Spell checking | `src/org/intellij/grammar/editor/BnfSpellCheckingStrategy.java` | Verified |
| Regexp injection in strings | `src/org/intellij/grammar/psi/impl/BnfStringRegexpInjector.java` | Verified |
| Element description provider | `src/org/intellij/grammar/BnfDescriptionProvider.java` | Verified |

### 11. Diagram Support (Optional - requires UML plugin)

| Feature | Source File | Status |
|---------|------------|--------|
| PSI tree diagram provider | `src/org/intellij/grammar/diagram/BnfDiagramProvider.java` | Verified |

Registered in `plugin-uml.xml` as optional dependency on `com.intellij.diagram`.

---

## External Links

### IntelliJ Platform SDK Documentation

| Topic | URL | Status | Relevance |
|-------|-----|--------|-----------|
| Custom Language Support (overview) | https://plugins.jetbrains.com/docs/intellij/custom-language-support.html | Verified - accessible | Core reference for what Grammar-Kit generates support for |
| Custom Language Support Tutorial | https://plugins.jetbrains.com/docs/intellij/custom-language-support-tutorial.html | Verified - accessible | Step-by-step tutorial using Grammar-Kit (referenced in README.md#L33) |
| Implementing Parser and PSI | https://plugins.jetbrains.com/docs/intellij/implementing-parser-and-psi.html | Verified - accessible | Explicitly recommends Grammar-Kit for parser generation |
| Program Structure Interface (PSI) | https://plugins.jetbrains.com/docs/intellij/psi.html | Verified - accessible | Foundation concept for Grammar-Kit's PSI generation |
| Syntax Highlighting | https://plugins.jetbrains.com/docs/intellij/syntax-highlighting-and-error-highlighting.html | Verified - accessible | Context for Grammar-Kit's highlighting features |
| Code Completion | https://plugins.jetbrains.com/docs/intellij/code-completion.html | Verified - accessible | Context for completion contributor pattern |
| Find Usages | https://plugins.jetbrains.com/docs/intellij/find-usages.html | Verified - accessible | Context for find usages provider pattern |
| Structure View | https://plugins.jetbrains.com/docs/intellij/structure-view.html | Verified - accessible | Context for structure view factory pattern |
| Code Inspections and Intentions | https://plugins.jetbrains.com/docs/intellij/code-inspections-and-intentions.html | Verified - accessible | Context for inspection/intention patterns |
| Rename Refactoring | https://plugins.jetbrains.com/docs/intellij/rename-refactoring.html | Verified - accessible | Context for refactoring support |
| Grammar and Parser (tutorial step) | https://plugins.jetbrains.com/docs/intellij/grammar-and-parser.html | Verified - accessible | Tutorial step that uses Grammar-Kit directly |
| Gradle Grammar-Kit Plugin | https://plugins.jetbrains.com/docs/intellij/tools-gradle-grammar-kit-plugin.html | Verified - accessible | Official Gradle integration docs |

### Grammar-Kit Resources

| Resource | URL | Status |
|----------|-----|--------|
| Plugin marketplace page | https://plugins.jetbrains.com/plugin/6606-grammar-kit | Verified - accessible |
| GitHub repository | https://github.com/JetBrains/Grammar-Kit | Verified - referenced in plugin.xml#L1 |
| Gradle Grammar-Kit Plugin (GitHub) | https://github.com/JetBrains/gradle-grammar-kit-plugin | Verified - referenced in README.md#L48 |
| Tutorial (in-repo) | `Grammar-Kit/TUTORIAL.md` | Verified - exists |
| How-to (in-repo) | `Grammar-Kit/HOWTO.md` | Verified - exists |
| Changelog (in-repo) | `Grammar-Kit/CHANGELOG.md` | Verified - exists |

### Open-Source Projects Using Grammar-Kit

Referenced in `README.md#L23-L31`:

| Project | URL | Status |
|---------|-----|--------|
| Clojure-Kit | https://github.com/gregsh/Clojure-Kit | Referenced |
| intellij-rust | https://github.com/intellij-rust/intellij-rust | Referenced |
| intellij-erlang | https://github.com/ignatov/intellij-erlang | Referenced |
| intellij-elm | https://github.com/intellij-elm/intellij-elm | Referenced |
| intellij-elixir | https://github.com/KronicDeth/intellij-elixir | Referenced |
| Perl5-IDEA | https://github.com/Camelcade/Perl5-IDEA | Referenced |
| Dart (IntelliJ) | https://github.com/JetBrains/intellij-plugins/tree/master/Dart | Referenced |
| intellij-haxe | https://github.com/HaxeFoundation/intellij-haxe | Referenced |
| Cypher (Graph DB) | https://github.com/neueda/jetbrains-plugin-graph-database-support | Referenced |

### Related External Resources

| Resource | URL | Notes |
|----------|-----|-------|
| PEG (Wikipedia) | https://en.wikipedia.org/wiki/Parsing_expression_grammar | Referenced in README.md#L82 for BNF syntax basis |
| JFlex documentation | https://jflex.de/manual.html | Referenced in README.md#L240 for lexer regex subset |
| ANTLR4 IntelliJ Adaptor | https://github.com/antlr/antlr4-intellij-adaptor | Mentioned in SDK docs as alternative approach |
| IntelliJ Platform Slack | https://plugins.jetbrains.com/slack | Community channel (README.md#L250) |
| JetBrains Platform on X | https://x.com/JBPlatform | Official account (README.md#L251) |

---

## Validation Summary

### Verified Internal References

- [x] `README.md` "Plugin features" section exists at lines 54-78 (2025-02-19)
- [x] `plugin.xml` contains all registered extensions (2025-02-19)
- [x] `plugin-java.xml` contains generator actions and Java helpers (2025-02-19)
- [x] `plugin-uml.xml` contains diagram provider (2025-02-19)
- [x] All 8 inspection description HTML files exist and contain content (2025-02-19)
- [x] All 2 intention description directories exist with description.html + templates (2025-02-19)
- [x] `images/editor.png` exists (2025-02-19)
- [x] `images/livePreview.png` exists (2025-02-19)
- [x] All 38 attribute description HTML files exist in `resources/messages/attributeDescriptions/` (2025-02-19)

### Feature Claims Verified Against Source

- [x] Syntax highlighting: `BnfSyntaxHighlighter.java` with 20 color keys (2025-02-19)
- [x] Code completion: `BnfCompletionContributor.java` registered in plugin.xml (2025-02-19)
- [x] Structure view: `BnfStructureViewFactory.java` + JFlex + Live Preview variants (2025-02-19)
- [x] Find usages: `BnfFindUsagesProvider.java` + JFlex variant (2025-02-19)
- [x] Introduce Rule refactoring: `BnfIntroduceRuleAction.java` + handler + popup (2025-02-19)
- [x] Introduce Token refactoring: `BnfIntroduceTokenAction.java` + handler (2025-02-19)
- [x] Inline Rule refactoring: `BnfInlineRuleActionHandler.java` + processor + dialog (2025-02-19)
- [x] Unwrap/remove expression: `BnfUnwrapDescriptor.java` (2025-02-19)
- [x] All 8 inspections: source files + description HTML + plugin.xml registration (2025-02-19)
- [x] Both intentions: source files + description HTML + plugin.xml registration (2025-02-19)
- [x] Live Preview: `LivePreviewAction.java` + full livePreview package (10 files) (2025-02-19)
- [x] Parser generation: `GenerateAction.java` + `ParserGenerator.java` (2025-02-19)
- [x] Lexer generation: `BnfGenerateLexerAction.java` (2025-02-19)
- [x] JFlex runner: `BnfRunJFlexAction.java` (2025-02-19)
- [x] ParserUtil generation: `BnfGenerateParserUtilAction.java` (2025-02-19)
- [x] Documentation provider: `BnfDocumentationProvider.java` with FIRST/FOLLOWS/PSI (2025-02-19)
- [x] PSI diagram: `BnfDiagramProvider.java` (optional, requires UML plugin) (2025-02-19)
- [x] In-place rename: `BnfRefactoringSupportProvider.java` (2025-02-19)
- [x] Code folding: `BnfFoldingBuilder.java` (2025-02-19)
- [x] Brace matching: `BnfBraceMatcher.java` (2025-02-19)
- [x] Commenter: `BnfCommenter.java` (2025-02-19)
- [x] Spell checking: `BnfSpellCheckingStrategy.java` (2025-02-19)
- [x] Regexp injection: `BnfStringRegexpInjector.java` (2025-02-19)
- [x] Line markers (rule navigation): `BnfRuleLineMarkerProvider.java` (2025-02-19)
- [x] Line markers (recursion): `BnfRecursionLineMarkerProvider.java` (2025-02-19)
- [x] Fleet code generation: `GenerateFleetAction.java` + related (2025-02-19)

### External Links Verified

- [x] IntelliJ SDK Custom Language Support page accessible (2025-02-19)
- [x] IntelliJ SDK Custom Language Tutorial accessible (2025-02-19)
- [x] IntelliJ SDK Implementing Parser and PSI accessible - explicitly recommends Grammar-Kit (2025-02-19)
- [x] IntelliJ SDK PSI documentation accessible (2025-02-19)
- [x] Grammar-Kit marketplace page accessible (2025-02-19)

---

## Errors Found

None. All referenced files exist, all features are backed by source code, and all external links are accessible.

## Discrepancies and Notes

1. **README.md feature list vs actual features**: The README lists "Refactoring: extract rule" but the action class is named `BnfIntroduceRuleAction` (using IntelliJ's "Introduce" terminology). The shortcut mapping uses `ExtractMethod`. Documentation should use "Extract Rule" as the user-facing name per the README, noting the `Ctrl-Alt-M` / `Cmd-Alt-M` shortcut.

2. **Fleet generation support**: The `plugin-java.xml` registers Fleet-specific generation actions (`GenerateFleetAction`, `BnfGenerateFleetLexerAction`, `BnfRunFleetJFlexAction`). This is not mentioned in the README's feature list. Consider whether to document this as a feature or note it as an advanced/internal capability.

3. **Regexp injection**: The `BnfStringRegexpInjector` provides RegExp language injection for `regexp:` prefixed token values. This is not explicitly listed in the README features but is a useful editing feature. It is controlled by `Options.BNF_INJECT_REGEXP_IN_BNF`.

4. **Move left/right handler**: `BnfMoveLeftRightHandler` is registered but not mentioned in the README feature list. This allows reordering choice branches and sequence elements.

5. **Word selectioner**: `BnfWordSelectioner` extends word selection behavior but is not mentioned in the README.

6. **Recursion line markers**: `BnfRecursionLineMarkerProvider` shows gutter icons for recursive rules. Not explicitly listed in README features but visible in the editor.

## Out of Scope References

- Attribute system details (38 attribute descriptions) -> Validated in Section 3.1 (Attributes System)
- Error recovery mechanics (pin, recoverWhile) -> Validated in Section 2.4 (Error Recovery)
- Live Preview workflow details -> Validated in Section 2.5 (Live Preview Workflow)
- Expression parsing specifics -> Validated in Section 2.3 (Expression Parsing)
- Parser generation internals -> Validated in Section 3.2 (Parser Generation)
- JFlex integration details -> Validated in Section 3.3 (Lexer Integration)
- PSI customization -> Validated in Section 3.4 (PSI Customization)
- Gradle build integration -> Validated in Section 4.2 (Build Integration)
- Testing approaches -> Validated in Section 4.1.3 (Testing)

---

## Complete Feature Count

Based on source code verification:

| Category | Count | Details |
|----------|-------|---------|
| Syntax highlighting color keys | 20 | BNF: 20 customizable colors |
| Inspections | 8 | All WARNING level, all enabled by default |
| Intentions | 2 | Flip choice, Convert optional expression |
| Refactoring actions | 4 | Introduce Rule, Introduce Token, Inline Rule, Unwrap |
| Generator actions | 4+3 | Parser, Lexer, ParserUtil, JFlex runner + 3 Fleet variants |
| Navigation features | 5 | Structure view, Find usages, Rule line markers, Recursion markers, Attr pattern search |
| Live Preview components | 10 | Full language implementation with highlighting, structure, parsing |
| Editor features | 7 | Folding, brace matching, commenter, quote handler, word selectioner, move handler, spell check |
| Documentation | 1 | FIRST/FOLLOWS/PSI/expression/attribute docs |
| Diagram | 1 | PSI tree diagram (optional, requires UML plugin) |
| Language injection | 1 | RegExp in token regexp values |
| **Total distinct features** | **~61** | Across BNF, JFlex, and Live Preview |
