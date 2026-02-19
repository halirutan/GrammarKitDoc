# Topic Summary: Features

## Documentation Outline Reference
Section 1.2: Features
File: `docs/features.md`
Source: info/documentation-outline.md (lines 37-61)

## Page Purpose

This page gives readers a scannable overview of what Grammar-Kit can do. It sits between the introduction (what Grammar-Kit is) and installation (how to set it up). The reader should leave knowing whether Grammar-Kit covers their needs and what capabilities they can expect.

This is not a tutorial or reference page. Keep descriptions brief. Point readers toward the relevant detailed pages rather than explaining mechanics.

## Learning Objectives

Based on outline and evidence:

- Understand the scope of Grammar-Kit: BNF editing, parser/PSI generation, JFlex support, Live Preview
- Know the major feature categories and what each provides
- Understand how Grammar-Kit fits into the IntelliJ Platform language support pipeline
- Determine whether Grammar-Kit is the right tool for a given project

## Prerequisites

- Familiarity with IntelliJ IDEA as a development environment
- Basic understanding of what a parser does (covered in Section 1.1)
- No Grammar-Kit installation required to read this page

## Content Structure

### H1: Features

Short opening paragraph (2-3 sentences). State what Grammar-Kit provides at a high level: a BNF grammar editor, a parser/PSI code generator, and a Live Preview system, all integrated into IntelliJ IDEA. Mention that it also supports JFlex lexer development.

---

### H2: Grammar Editing

Cover the BNF and JFlex editor capabilities as a unified editing experience. The goal is to show that Grammar-Kit provides a full IDE experience for grammar files, not just a text editor.

Key points to cover:

- BNF files (`.bnf`) and JFlex files (`.flex`) are first-class file types with dedicated language support
- Syntax highlighting with 20 customizable color keys for BNF (source: code-evidence, BnfSyntaxHighlighter.java). Mention JFlex has its own highlighter.
- Code completion: rule names, token names, attribute names, keywords, external method references (source: code-evidence, BnfCompletionContributor.java)
- Navigation: structure view (Ctrl+F12), find usages (Alt+F7), go to generated code (Ctrl+Alt+Home), quick documentation showing FIRST/FOLLOW sets (source: code-evidence, multiple navigation sources)
- Refactoring: extract rule (Ctrl+Alt+M), introduce token (Ctrl+Alt+C), inline rule, rename, unwrap expression (source: code-evidence, refactoring section)
- 8 built-in inspections that catch problems like unresolved references, unused rules, left recursion, suspicious tokens, duplicate rules, identical/unreachable choice branches (source: code-evidence, inspections section; references.md confirms all 8 verified)
- 2 intentions: flip choice branches, convert between `?` and `[]` optional syntax (source: code-evidence, intentions section)
- Additional editor conveniences: code folding, brace matching, commenting, spell checking, regexp injection in token patterns (source: code-evidence, additional editor features)

Approach: Use a short paragraph for the main editing story (highlighting, completion, navigation), then a compact list for the inspection names since there are 8 parallel items. Mention refactoring actions in a brief paragraph or short list. Do not enumerate every minor editor feature; group the smaller ones (folding, brace matching, commenting, spell check) into a single sentence about standard editor conveniences.

---

### H2: Code Generation

Cover what Grammar-Kit generates and how generation is triggered. This is the core value proposition.

Key points to cover:

- Parser generation from BNF grammars: produces parser class, element types, PSI interfaces, and PSI implementation classes (source: code-evidence, GenerateAction.java)
- Trigger: Ctrl+Shift+G from the IDE, or via Gradle plugin for build automation (source: code-evidence, generation features; references.md, Gradle plugin link)
- JFlex lexer generation: creates a `.flex` file from BNF token definitions, converting Java regex to JFlex syntax (source: code-evidence, BnfGenerateLexerAction.java)
- JFlex compilation: runs JFlex to produce Java lexer code, auto-downloads JFlex 1.9.2 if needed (source: code-evidence, BnfRunJFlexAction.java)
- Parser utility class generation: scaffolds a custom `parserUtilClass` (source: code-evidence, BnfGenerateParserUtilAction.java)
- Two-pass generation available in IDE mode (not Gradle) (source: code-evidence, GenerateAction.java note)
- Batch generation: multiple `.bnf` files at once (source: code-evidence)

Approach: Lead with the main generation story (BNF to parser + PSI). Mention the keyboard shortcut. Follow with JFlex generation. Keep it factual. Do not explain the generated code structure here; that belongs in Section 3.2.

---

### H2: Live Preview

Cover the real-time grammar testing capability. This is a distinctive feature that differentiates Grammar-Kit from offline parser generators.

Key points to cover:

- Open with Ctrl+Alt+P; creates a split editor with a preview pane for testing grammar rules against sample input (source: code-evidence, LivePreviewAction.java)
- Real-time feedback: preview reparses automatically when the BNF file changes, with a 500ms debounce (source: code-evidence, LivePreviewHelper.java)
- Structure view integration: see the parse tree for preview input (source: code-evidence, LivePreviewStructureViewFactory)
- Grammar highlighting at caret (Ctrl+Alt+F7): highlights which grammar expressions match at the cursor position in the preview (source: code-evidence, HighlightGrammarAtCaretAction.java)
- Dynamic language registration: each grammar gets its own preview language with syntax highlighting and structure view (source: code-evidence, LivePreviewLanguage)

Approach: 2-3 short paragraphs. Emphasize the interactive development loop. Do not detail limitations here; that belongs in Section 2.5.

---

### H2: IntelliJ Platform Integration

Cover how Grammar-Kit's output connects to the IntelliJ Platform. This section answers "what do I get after generation?" from a platform perspective.

Key points to cover:

- Generated parsers produce `PsiElement` implementations that plug directly into the IntelliJ Platform's PSI framework (source: code-evidence, PSI Foundation section)
- Grammar-Kit requires only `com.intellij.modules.lang` as a core dependency (source: code-evidence, platform integration)
- Generated code integrates with standard Language API extension points: `lang.parserDefinition`, `lang.syntaxHighlighterFactory`, `lang.findUsagesProvider`, `lang.braceMatcher`, `lang.psiStructureViewFactory`, and others (source: code-evidence, Language API Integration section lists 13 extension points)
- Optional integrations: Java-aware features (PSI navigation, generation actions), UML diagram support, copyright support (source: code-evidence, optional dependencies)
- Grammar-Kit is used by production plugins: intellij-rust, intellij-erlang, Dart, Perl5-IDEA, intellij-elixir, Clojure-Kit, and others (source: code-evidence, open-source plugins list; references.md confirms all links)

Approach: Keep this concise. The reader needs to know that Grammar-Kit output is not standalone; it produces IntelliJ Platform-native code. Mention the real-world plugins as social proof in a single sentence, not a full list. Link to the IntelliJ SDK Custom Language Support page (verified accessible in references.md).

Cross-reference: Point to Section 4.1.1 (Parser Definition) and Section 4.1.2 (Language Features) for implementation details.

---

## Evidence Mapping

| Outline Bullet | Evidence Support |
|---|---|
| Overview of BNF grammar support and parser generation | code-evidence: Plugin Identity, File Types, Generation Features |
| BNF Grammars and JFlex file editing support | code-evidence: Editor Features BNF (lines 30-145), Editor Features JFlex (lines 148-188) |
| Parser/PSI code generation capabilities | code-evidence: Generation Features (lines 307-343) |
| Live Preview for rapid development | code-evidence: Live Preview Features (lines 346-375) |
| Syntax highlighting and code completion for BNF | code-evidence: Syntax Highlighting (lines 33-42), Code Completion (lines 63-70) |
| Real-time grammar validation | code-evidence: Inspections (lines 222-289), 8 inspections verified |
| Integrated parser testing | code-evidence: Live Preview (lines 346-375) |
| PSI hierarchy generation | code-evidence: PSI Foundation (lines 416-421) |
| Error recovery mechanisms | code-evidence: Pin Marker Annotations (lines 56-60); detail deferred to Section 2.4 |
| Integration with Language API | code-evidence: Language API Integration (lines 399-413), 13 extension points listed |
| PSI foundation | code-evidence: PSI Foundation (lines 416-421) |
| Custom language plugin architecture | code-evidence: Platform Integration Points (lines 388-434) |
| When to use: custom language, DSL, file format, config, scripting | code-evidence: When to Use (lines 458-477), 9 open-source projects listed |
| Keyboard shortcuts | code-evidence: Keyboard Shortcuts Summary (lines 438-454) |

### Gaps

- "Custom language plugin architecture" from the outline has limited direct evidence. The evidence covers extension points and dependencies but not architecture concepts. Keep this brief and link to IntelliJ SDK docs.
- "Error recovery mechanisms" is mentioned in the outline but evidence explicitly marks it as out of scope for this section (belongs to Section 2.4). Mention it exists; do not explain mechanics.

## Key Takeaways

- Grammar-Kit provides approximately 61 distinct features across BNF editing, JFlex editing, and Live Preview (source: references.md feature count table)
- The plugin supports three file types: `.bnf`, `.flex`, and Live Preview virtual files
- All 8 inspections are enabled by default at WARNING level
- The editing experience mirrors standard IntelliJ IDE features (completion, navigation, refactoring, inspections)
- Live Preview provides real-time grammar testing without generating code
- Generated code integrates directly with IntelliJ Platform PSI and Language API
- Production-proven: used by major language plugins (Rust, Dart, Erlang, Elixir, Perl, Haxe, Elm, Clojure, Cypher)

## Tone and Approach

- Factual and scannable. This is an overview page, not a tutorial.
- Use short paragraphs (3-4 sentences each) to describe each feature category.
- Use lists only for the inspections (8 items, parallel structure) and possibly the refactoring actions (4 items).
- Do not explain how features work. State what they do and where to learn more.
- Do not include code examples. The outline says "Examples needed: NOT REQUIRED."
- Avoid feature-by-feature enumeration of minor editor conveniences. Group them.
- Mention keyboard shortcuts inline where they help (e.g., "Generate parser code with Ctrl+Shift+G") rather than in a separate table. The full shortcut reference belongs in Section 6.3.

## Cross-References

- Previous: `docs/index.md` (Section 1.1 - What is Grammar-Kit?)
- Next: `docs/installation.md` (Section 1.3 - Installation and Setup)
- Live Preview details: `docs/grammar-development/live-preview.md` (Section 2.5)
- Attributes system: `docs/code-generation/attributes.md` (Section 3.1)
- Parser generation details: `docs/code-generation/parser-generation.md` (Section 3.2)
- Language features integration: `docs/integration/language-features.md` (Section 4.1.2)
- Keyboard shortcuts reference: `docs/reference/shortcuts.md` (Section 6.3)
- External: [IntelliJ SDK - Custom Language Support](https://plugins.jetbrains.com/docs/intellij/custom-language-support.html) (verified accessible)
- External: [IntelliJ SDK - Implementing Parser and PSI](https://plugins.jetbrains.com/docs/intellij/implementing-parser-and-psi.html) (verified accessible, explicitly recommends Grammar-Kit)
- External: [Grammar-Kit on JetBrains Marketplace](https://plugins.jetbrains.com/plugin/6606-grammar-kit) (verified accessible)

## What to Avoid

- Do not explain grammar syntax, rule modifiers, or token definitions (Section 2.1)
- Do not explain attribute mechanics like `pin`, `recoverWhile`, `extends` (Section 3.1)
- Do not explain expression parsing or operator precedence (Section 2.3)
- Do not cover error recovery mechanics (Section 2.4)
- Do not detail Live Preview limitations or workflow (Section 2.5)
- Do not cover PSI customization (mixin, methods, fake rules) (Section 3.4)
- Do not cover Gradle plugin setup or CI/CD (Section 4.2)
- Do not cover installation steps (Section 1.3)
- Do not include a keyboard shortcuts table (Section 6.3)
- Do not list all 20 color keys or all 13 extension points. Mention the counts; link to reference pages.
- Do not mention Fleet-specific generation actions (undocumented, internal capability per references.md discrepancy note)
- Do not use bold-label bullet lists. Use paragraphs with inline mentions.

## Documentation Notes

- The page should work as a "feature checklist" for someone evaluating Grammar-Kit. After reading, they should know the tool's scope.
- Keep the page short. Target 400-600 words of body text (excluding headings).
- The "When to use Grammar-Kit" content from the outline maps naturally to the IntelliJ Platform Integration section (mention real-world projects) and the opening paragraph (mention use cases). It does not need its own H2 unless the drafter finds the page too short without it.
- References.md notes a discrepancy: the README calls it "Extract Rule" but the code uses "Introduce Rule." Use "Extract Rule" as the user-facing name per the README, with the Ctrl+Alt+M shortcut.
- The `BnfExpressionMarkerAnnotator` is registered but is a no-op/todo. Do not mention it.
