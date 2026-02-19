# Topic Summary: What is Grammar-Kit?

## Documentation Outline Reference
Section 1.1: What is Grammar-Kit?
Source: info/documentation-outline.md, lines 15-35
Target file: `docs/index.md` (site landing page)

---

## Learning Objectives

Based on the outline and evidence, after reading this page the reader should:

- Understand what Grammar-Kit does: transforms BNF grammars into working parsers, lexers, and PSI classes for IntelliJ-based IDEs.
- Know who Grammar-Kit is for: plugin developers building language support, DSLs, or configuration format parsers.
- Recognize the key capabilities that distinguish Grammar-Kit: Live Preview, expression parsing with precedence, error recovery, and tight IntelliJ Platform integration.
- Know where to go next: installation, features overview, or the quick start tutorial.

## Prerequisites

- None. This is the first section in the documentation (references.md confirms no prerequisites).
- The page should assume the reader knows what an IDE is and has a general sense of what parsing means, but should not assume IntelliJ Platform or Grammar-Kit knowledge.

---

## Content Structure

### H1: Grammar-Kit

The page title. This is the site landing page (`docs/index.md`), so the H1 doubles as the documentation's main heading.

### H2: What it does

**Purpose**: Explain the core value proposition in concrete terms. No marketing language.

Cover these points (all from outline "BNF-to-parser transformation tool"):

- Grammar-Kit is an IntelliJ IDEA plugin by JetBrains for language plugin developers.
  - Evidence: code-evidence.md "Plugin Identity" section. Official description: "BNF Grammars and JFlex lexers editor. Readable parser/PSI code generator." Tagline: "An IntelliJ IDEA plugin for language plugin developers."
- It transforms BNF grammar definitions into working parsers (PsiBuilder-based recursive descent).
  - Evidence: code-evidence.md "Core Capabilities" section. Generates parser code, ElementTypes, PSI classes from BNF grammar. Shortcut: Ctrl-Shift-G.
- It generates lexers (JFlex) and PSI implementations automatically.
  - Evidence: code-evidence.md "Core Capabilities." Generates JFlex lexer definition (*.flex) from BNF grammar, then Java lexer code via JFlex generator. Also generates PSI interfaces and implementation classes.
  - Verified: references.md Claim 1 (PASS), Claim 2 (PASS).
- It eliminates the need for hand-written parsing code.
  - Evidence: IntelliJ SDK docs explicitly recommend Grammar-Kit: "we highly recommend generating parser and corresponding PSI classes from BNF grammars using Grammar-Kit plugin" (references.md, IntelliJ Platform SDK Documentation section).

Keep this section to 2-3 short paragraphs. Avoid listing every generated artifact; the point is the transformation from grammar to working code.

### H2: Use cases

**Purpose**: Show the breadth of what Grammar-Kit can build. Helps readers self-identify.

Cover these points (all from outline "Target use cases"):

- Building language support for IntelliJ-based IDEs (programming languages).
  - Evidence: code-evidence.md "Target Use Cases > Programming languages." Eight open-source plugins listed: Rust, Erlang, Elm, Elixir, Perl, Dart, Haxe, Clojure. Also Cypher (query language).
- Adding syntax highlighting and code completion (IDE features that Grammar-Kit enables).
  - Evidence: code-evidence.md "IntelliJ Platform Integration." Generated parsers extend LightPsiParser; PSI tree integrates with IntelliJ PSI. Users implement ParserDefinition and register in plugin.xml.
- Configuration formats (JSON, YAML).
  - Evidence: code-evidence.md "Target Use Cases > Configuration formats." JSON grammar exists as test/example: `testData/livePreview/Json.bnf`.
- Domain-specific languages (DSLs).
  - Evidence: code-evidence.md "Target Use Cases > DSL support." Tutorial demonstrates building a custom expression language from scratch. Also self-hosting: Grammar-Kit's own BNF grammar is defined in Grammar-Kit.

Structure: A short introductory sentence, then a concise list of use case categories. Mention 3-4 real-world plugins by name (Rust, Erlang, Dart) as social proof, but keep it brief. Link to the full list in the README or an appendix rather than enumerating all eight.

### H2: Key capabilities

**Purpose**: Give a quick sense of what makes Grammar-Kit productive. Each capability gets a sentence or two, not a full explanation. This section sets up forward references to deeper documentation.

Cover these points (all from outline "Key development features"):

- Live Preview for real-time grammar testing (Ctrl-Alt-P / Cmd-Alt-P).
  - Evidence: code-evidence.md "Key Development Features > Live Preview." Tests grammar against sample text in real time. Structure view shows PSI tree. No code generation or compilation needed.
  - Verified: references.md Claim 3 (PASS). Full implementation package confirmed.
  - Forward ref: Section 2.5 (`docs/grammar-development/live-preview.md`).

- Interactive grammar development workflow.
  - Evidence: code-evidence.md "Interactive Grammar Development Workflow." Six-step workflow from creating .bnf file through generating parser, lexer, implementing ParserDefinition, and mixing in functionality.
  - Forward ref: Section 1.4 (`docs/quick-start.md`).

- Automatic expression parsing with operator precedence.
  - Evidence: code-evidence.md "Expression Parsing with Operator Precedence." Uses `extends(".*_expr")=expr` pattern. Supports BINARY, PREFIX, POSTFIX, N_ARY, ATOM operator types. Pratt-like parsing. Only 2 methods generated for entire expression root.
  - Verified: references.md Claim 4 (PASS). ExpressionHelper.java and ExpressionGeneratorHelper.java confirmed.
  - Forward ref: Section 2.3 (`docs/grammar-development/expression-parsing.md`).

- Advanced error recovery mechanisms (pin, recoverWhile).
  - Evidence: code-evidence.md "Error Recovery Mechanisms." `pin` commits parser at a position; `recoverWhile` skips unexpected tokens. `#auto` recovery available. `name` attribute customizes error messages.
  - Verified: references.md Claim 5 (PASS).
  - Forward ref: Section 2.4 (`docs/grammar-development/error-recovery.md`).

- Seamless IntelliJ Platform integration.
  - Evidence: code-evidence.md "IntelliJ Platform Integration." Generated parsers extend LightPsiParser. GeneratedParserUtilBase included in IntelliJ Platform since 12.1. Gradle integration via gradle-grammar-kit-plugin. Fleet support exists (changelog entry).
  - Forward ref: Section 4.1 (`docs/integration/parser-definition.md`).

Structure: Brief intro paragraph, then a compact treatment of each capability. Use forward-reference links so readers can dive deeper. Do not explain how any of these features work; that belongs in later sections.

### Closing navigation

**Purpose**: Direct readers to their logical next step. Not a separate H2; just a short closing paragraph or a 3-item list at the end of the page.

Options to link:

- `docs/features.md` (Section 1.2) for a detailed feature overview.
- `docs/installation.md` (Section 1.3) to install and set up.
- `docs/quick-start.md` (Section 1.4) to start building immediately.

Evidence: references.md "Related Sections" confirms these three as the direct follow-ups.

---

## Evidence Mapping

| Outline Item | Evidence Source | Status |
|---|---|---|
| IntelliJ IDEA plugin for grammar development | code-evidence.md "Plugin Identity" | Fully supported |
| Transforms BNF grammar definitions into working parsers | code-evidence.md "Core Capabilities"; references.md Claim 1 | Verified (PASS) |
| Generates lexers and PSI implementations automatically | code-evidence.md "Core Capabilities"; references.md Claims 1, 2 | Verified (PASS) |
| Eliminates need for hand-written parsing code | references.md IntelliJ SDK recommendation | Supported |
| Building language support for IntelliJ-based IDEs | code-evidence.md "Target Use Cases > Programming languages" | 8 real-world examples |
| Adding syntax highlighting and code completion | code-evidence.md "IntelliJ Platform Integration" | Supported (indirect: PSI enables these) |
| Creating parsers for programming languages | code-evidence.md "Target Use Cases > Programming languages" | 8 examples |
| Supporting configuration formats (JSON, YAML) | code-evidence.md "Target Use Cases > Configuration formats" | JSON confirmed; YAML not evidenced |
| Developing domain-specific languages (DSLs) | code-evidence.md "Target Use Cases > DSL support" | Tutorial example confirmed |
| Live Preview for real-time grammar testing | code-evidence.md "Live Preview"; references.md Claim 3 | Verified (PASS) |
| Interactive grammar development workflow | code-evidence.md "Interactive Grammar Development Workflow" | 6-step workflow documented |
| Automatic expression parsing with operator precedence | code-evidence.md "Expression Parsing"; references.md Claim 4 | Verified (PASS) |
| Advanced error recovery mechanisms | code-evidence.md "Error Recovery Mechanisms"; references.md Claim 5 | Verified (PASS) |
| Seamless IntelliJ Platform integration | code-evidence.md "IntelliJ Platform Integration" | Supported |

### Gaps

- **YAML**: The outline mentions "Supporting configuration formats (JSON, YAML)" but no YAML grammar evidence exists. The drafter should mention configuration formats generally and use JSON as the concrete example. Do not claim YAML support without evidence.
- **Syntax highlighting and code completion**: The outline lists these as use cases. Evidence supports them indirectly (PSI integration enables IDE features), but Grammar-Kit does not generate highlighters or completion contributors directly. The drafter should frame this as "Grammar-Kit produces the PSI foundation that powers syntax highlighting, code completion, and other IDE features" rather than implying Grammar-Kit generates those features itself.

---

## Key Takeaways

- Grammar-Kit is a JetBrains-maintained IntelliJ plugin that generates recursive descent parsers and PSI classes from BNF grammars.
- It is the officially recommended tool for parser/PSI generation in the IntelliJ Platform SDK documentation.
- Real-world adoption is strong: at least eight open-source language plugins use it, including JetBrains' own Dart plugin.
- The tool covers the full development cycle: grammar authoring, live testing, code generation, and IDE integration.
- Grammar-Kit is self-hosting: its own grammar is written in its own BNF format.

---

## Documentation Notes

### Tone and approach
- This is the landing page. It must orient the reader quickly: what is this tool, is it for me, where do I go next.
- Write for a developer who has landed here from a search engine or the IntelliJ SDK docs. They are evaluating whether Grammar-Kit solves their problem.
- No "Welcome to the Grammar-Kit documentation" opener. Start with what Grammar-Kit is.
- Keep the page short. Aim for roughly 400-600 words of body text (excluding headings and navigation links).

### What to include
- The official description from plugin.xml: "BNF Grammars and JFlex lexers editor. Readable parser/PSI code generator."
- The IntelliJ SDK endorsement (paraphrased, with link).
- 3-4 named real-world plugins as concrete examples.
- Forward-reference links to deeper sections for each key capability.
- The keyboard shortcuts for the two most visible features: Generate Parser (Ctrl-Shift-G) and Live Preview (Ctrl-Alt-P).

### What to avoid
- Do not explain grammar syntax, attributes, or generation details. Those belong in Sections 2.x and 3.x.
- Do not cover installation steps (Section 1.3).
- Do not include a tutorial or walkthrough (Section 1.4).
- Do not list all features exhaustively (Section 1.2).
- Do not discuss Gradle integration in depth (Section 4.2).
- Do not mention Fleet support (only a changelog entry, no user-facing documentation).
- Do not use the word "seamless" even though the outline does. Describe the integration concretely instead.

### Cross-references to include
| Link text | Target |
|---|---|
| Features overview | `docs/features.md` |
| Installation and setup | `docs/installation.md` |
| Quick start tutorial | `docs/quick-start.md` |
| Live Preview | `docs/grammar-development/live-preview.md` |
| Expression parsing | `docs/grammar-development/expression-parsing.md` |
| Error recovery | `docs/grammar-development/error-recovery.md` |
| BNF grammar syntax | `docs/grammar-development/grammar-syntax.md` |
| Gradle integration | `docs/integration/gradle-setup.md` |

### External links to include
| Link text | URL | Source |
|---|---|---|
| GitHub repository | https://github.com/JetBrains/Grammar-Kit | references.md |
| JetBrains Plugin Marketplace | https://plugins.jetbrains.com/plugin/6606-grammar-kit | references.md |
| IntelliJ Platform SDK: Implementing Parser and PSI | https://plugins.jetbrains.com/docs/intellij/implementing-parser-and-psi.html | references.md |

---

## Planning Checklist

- [x] Read all evidence files for topic
- [x] Identify learning objectives
- [x] Extract prerequisites
- [x] Design content structure
- [x] Map evidence to sections
- [x] Write topic-summary.md
