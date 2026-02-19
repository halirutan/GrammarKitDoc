# Topic Summary: Installation and Setup

## Documentation Outline Reference
Section 1.3: Installation and Setup
Source: info/documentation-outline.md (lines 63-98)
Target file: `docs/installation.md`

---

## Learning Objectives

Based on the outline and evidence, the reader should be able to:

- Install the Grammar-Kit plugin in IntelliJ IDEA and verify it works
- Understand the system requirements (Java version, IntelliJ version)
- Set up a project with separate source roots for handwritten and generated code
- Create a `.bnf` grammar file with a proper attributes block
- Confirm the editor recognizes the file (icon, highlighting, Live Preview)

---

## Prerequisites

- IntelliJ IDEA (Community or Ultimate), version 2023.3 or later (code-evidence: since-build 233)
- Java 17 or later (code-evidence: required since Grammar-Kit 2022.3; README.md L19)
- Basic familiarity with IntelliJ IDEA (creating projects, navigating settings)
- Java development knowledge (the generated code is Java)
- No parsing theory required at this stage

---

## Content Structure

The page has five sections that follow the outline exactly. Each section below includes the evidence that supports it and drafting notes.

### H2: Prerequisites

Outline items:
- IntelliJ IDEA basics
- Java development knowledge (Java 17+ for recent versions)
- Understanding of parsing concepts (optional but helpful)

Evidence support:
- Java 17 required since 2022.3 (code-evidence, references: README.md L19, gradle.properties L33)
- IntelliJ IDEA 2023.3+ required for current Grammar-Kit (code-evidence: since-build 233)
- Plugin works on both Community and Ultimate editions (code-evidence: "Platform type: IU ... but plugin works on Community")
- Required platform dependency: `com.intellij.modules.lang` (code-evidence, references: plugin.xml L9)
- 2024.2+ requires Java 21 (references: "Additional References Discovered")

Drafting notes:
- State the hard requirements (Java 17, IDEA 2023.3+) up front in a short table or compact list.
- Mention that parsing concepts are helpful but not needed yet.
- Do not list every historical version. Point to the version compatibility section for older setups.

### H2: Installing the plugin

Outline items:
- Via IDE plugin marketplace
- Version compatibility matrix
- Offline installation options
- Verifying installation

Evidence support:
- Marketplace install path: Settings > Plugins > Marketplace > search "Grammar-Kit" (code-evidence)
- Marketplace URL: `https://plugins.jetbrains.com/plugin/6606-grammar-kit` (references: corrected to HTTPS with slug)
- Plugin ID: `org.jetbrains.idea.grammar` (code-evidence, references: plugin.xml L2)
- Dev builds URL from TeamCity (code-evidence; references: status "not independently verified")
- Version compatibility matrix reconstructed from CHANGELOG (code-evidence): 2023.3 -> IDEA 2023.3+/Java 17; 2022.3 -> IDEA 2022.3+/Java 17; 2021.1 -> IDEA 2021.1+; 2020.3 -> IDEA 2020.3+
- Verification: `.bnf` files get BNF icon and syntax highlighting (code-evidence)
- Editor features after install: code completion, Structure view, Live Preview, Generate Parser Code, Quick documentation (code-evidence)
- Inspections active by default: unresolved references, unused rules, left recursion, etc. (code-evidence)

Drafting notes:
- Lead with the marketplace install (3-step numbered list).
- Include a version compatibility table (Grammar-Kit version | IntelliJ version | Java version). Keep it to 4-5 rows.
- Offline install: mention the TeamCity dev builds link briefly. Note it is not officially documented (references: "not independently verified"). Keep this short.
- Verification: describe what the reader should see after install. Use a short numbered list: create `.bnf` file, check icon, check highlighting, try Ctrl+Alt+P. This doubles as a confidence check.

### H2: Project setup

Outline items:
- Creating a new language plugin project
- Directory structure recommendations
- Essential dependencies
- Recommended project templates

Evidence support:
- Directory structure: separate `src/` and `gen/` source roots (code-evidence: HOWTO.md L11 exact quote)
- Grammar-Kit's own layout: `src`, `gen`, `resources`, `tests`, `testData` (code-evidence: build.gradle.kts)
- Generated output directory configurable via `grammar.kit.gen.dir` system property, default `"gen"` (code-evidence: Options.java L14)
- Two project layout examples in examples.md: standard Gradle layout (`src/main/java` + `src/main/gen`) and classic flat layout (`src/` + `gen/`)
- `build.gradle.kts` snippet for marking `gen/` as generated source root (examples.md)
- Essential dependency: `GeneratedParserUtilBase` included in IntelliJ Platform since 12.1, no bundling needed (code-evidence, references: README.md L209)
- Gradle plugin: `org.jetbrains.grammarkit` version `2023.3.0.2` (references: SDK docs confirmed)
- Gradle plugin limitations: no method mixins, generic signatures may be incorrect (code-evidence, references: README.md L51-52)
- IntelliJ Platform Plugin Template: `https://github.com/JetBrains/intellij-platform-plugin-template` (code-evidence, references: confirmed)
- Creating a Plugin Project SDK docs: `https://plugins.jetbrains.com/docs/intellij/creating-plugin-project.html` (references: confirmed)
- Anti-pattern: mixing generated and handwritten code in same source root (examples.md)

Drafting notes:
- Show the recommended directory structure diagram from examples.md (the standard Gradle layout).
- Include the `build.gradle.kts` snippet for source root configuration.
- Mention the classic flat layout as an alternative in a brief paragraph, not a full diagram.
- List essential dependencies: IntelliJ Platform Gradle Plugin, Grammar-Kit Gradle plugin (`org.jetbrains.grammarkit`). Note that `GeneratedParserUtilBase` ships with the platform.
- Link to the IntelliJ Platform Plugin Template as a starting point. Link to Section 4.2.1 for full Gradle setup details.
- Mention the anti-pattern (mixed source roots) as a brief warning, not a separate section.

### H2: Development environment

Outline items:
- Configuring SDK
- Setting up source folders
- Version control considerations
- Team development setup

Evidence support:
- Source folder setup covered by project structure above (code-evidence, examples.md)
- `grammar.kit.gen.dir` system property for custom gen directory (code-evidence: Options.java L14)
- Other system properties: `grammar.kit.gen.jflex.args`, `grammar.kit.gpub.max.level`, `grammar.kit.inject.java`, `grammar.kit.inject.regexp` (code-evidence: Options.java)
- These are Java system properties (`-D` flags), not IDE settings UI (references: validation note)
- `gen/` directory: can be gitignored or committed, team preference (examples.md)
- No official SDK configuration steps specific to Grammar-Kit found (code-evidence: "Missing Documentation")
- No team development / VCS best practices documented in source (code-evidence: "Missing Documentation")

Drafting notes:
- This section is thin on evidence. Merge it into "Project setup" as an H3 subsection rather than a standalone H2, unless the drafter finds enough to fill a full section.
- Cover: marking `gen/` as generated source root (already in project setup), VCS decision for `gen/` (brief paragraph), system properties table (compact, 5 rows).
- For SDK configuration, link to the IntelliJ Platform SDK docs rather than inventing content. The evidence does not support detailed SDK setup instructions specific to Grammar-Kit.
- Do not speculate about team workflows. State the `gen/` VCS choice and move on.

### H2: First grammar file

Outline items:
- Creating a `.bnf` file
- Basic grammar structure
- Editor features overview
- Initial validation

Evidence support:
- File extension: `.bnf` (code-evidence, references: BnfFileType.java, plugin.xml)
- Grammar structure: optional attributes block `{ ... }` followed by rules (code-evidence)
- Rules use `::=` operator (code-evidence)
- Comments: `//` line, `/* */` block (code-evidence)
- Strings: single-quoted or double-quoted (code-evidence)
- Regexp tokens: `'regexp:\pattern'` (code-evidence)
- First rule is the root (code-evidence)
- Token definitions in `tokens=[...]` block (code-evidence)
- Minimal grammar example: `config.bnf` with full attributes and rules (examples.md)
- Bare-minimum grammar: `root ::= 'hello' 'world'` (examples.md)
- Default attribute values if omitted: `parserClass="generated.GeneratedParser"`, etc. (code-evidence, references: KnownAttribute.java)
- Anti-pattern: grammar without generation attributes (examples.md)
- Editor features: syntax highlighting, code completion, Structure view (Ctrl+F12), Live Preview (Ctrl+Alt+P), Generate Parser (Ctrl+Shift+G), Quick documentation (Ctrl+Q) (code-evidence)
- Inspections: unresolved references, unused rules, left recursion, duplicate rules, etc. (code-evidence)
- How to test: save file, check icon, open Live Preview, type sample input (examples.md)

Drafting notes:
- Start with the bare-minimum grammar to show something working fast. Then show the full `config.bnf` example with attributes.
- Explain the three sections of a grammar file: attributes block, token definitions, rules. Keep it brief; detailed syntax belongs in Section 2.1.
- List the editor features the reader should try, with keyboard shortcuts. Use a compact table (Feature | Shortcut | What it does).
- End with a validation step: open Live Preview, type sample input, confirm parse tree appears.
- Link forward to Section 1.4 (Quick Start Tutorial) for the next step.

---

## Evidence Mapping

| Outline Item | Evidence Source | Coverage |
|---|---|---|
| Prerequisites: IntelliJ IDEA basics | code-evidence (since-build 233, Community/Ultimate) | Full |
| Prerequisites: Java 17+ | code-evidence, references (README.md L19, gradle.properties L33) | Full |
| Prerequisites: Parsing concepts | No specific evidence | Outline says "optional but helpful"; one sentence suffices |
| Install: Via marketplace | code-evidence (install path) | Full |
| Install: Version compatibility matrix | code-evidence (CHANGELOG reconstruction), references (verified) | Full |
| Install: Offline installation | code-evidence (TeamCity URL), references (not independently verified) | Partial |
| Install: Verifying installation | code-evidence (file icon, highlighting, features, inspections) | Full |
| Project: New language plugin project | references (Plugin Template URL, SDK docs URL) | Partial (links only, no Grammar-Kit-specific wizard) |
| Project: Directory structure | code-evidence (HOWTO.md quote), examples.md (two layouts) | Full |
| Project: Essential dependencies | code-evidence (GPUB in platform, Gradle plugin), references (Maven coords, plugin ID) | Full |
| Project: Recommended templates | code-evidence (Plugin Template URL), references (confirmed) | Partial (link only) |
| Dev env: Configuring SDK | code-evidence: "Missing Documentation" | Gap: no Grammar-Kit-specific SDK steps. Link to platform docs. |
| Dev env: Setting up source folders | code-evidence, examples.md (build.gradle.kts snippet) | Full |
| Dev env: Version control | examples.md (gen/ gitignore note) | Minimal |
| Dev env: Team development | code-evidence: "Missing Documentation" | Gap: no source evidence. State the gen/ VCS choice only. |
| First grammar: Creating .bnf file | code-evidence, examples.md (two examples) | Full |
| First grammar: Basic structure | code-evidence (attributes, rules, tokens, comments) | Full |
| First grammar: Editor features | code-evidence (shortcuts, inspections, features) | Full |
| First grammar: Initial validation | examples.md (how to test section) | Full |

---

## Gaps Between Outline and Evidence

1. **SDK configuration**: The outline calls for "Configuring SDK" under Development Environment. No Grammar-Kit-specific SDK configuration steps exist in the source. The drafter should link to the IntelliJ Platform SDK docs (`creating-plugin-project.html`) and note that Grammar-Kit has no additional SDK requirements.

2. **Team development setup**: The outline lists this under Development Environment. No source evidence exists. The drafter should limit this to the `gen/` directory VCS decision (commit vs. gitignore) and move on.

3. **Offline installation steps**: Only a TeamCity dev builds URL exists. No step-by-step offline install instructions are documented. The drafter should mention the URL and note that standard IntelliJ plugin offline installation applies (download zip, install from disk).

4. **Recommended project templates**: Only a link to the IntelliJ Platform Plugin Template exists. There is no Grammar-Kit-specific template or archetype. The drafter should link to the template and the SDK "Creating a Plugin Project" page.

---

## Key Takeaways

- Grammar-Kit requires Java 17 and IntelliJ IDEA 2023.3+. These are hard requirements for the current version.
- Install from the JetBrains Marketplace. Verify by creating a `.bnf` file and checking for syntax highlighting.
- Separate handwritten code (`src/`) from generated code (`gen/`). This is the single most important project structure decision.
- A grammar file has three parts: attributes block, token definitions, and rules. The first rule is the parse root.
- The bare minimum to test a grammar is one rule and Live Preview. No attributes needed for prototyping.
- `GeneratedParserUtilBase` ships with the IntelliJ Platform. No extra runtime dependencies to bundle.

---

## Documentation Notes

- Keep the page task-oriented. The reader's goal: install Grammar-Kit, set up a project, create a grammar file, see it work.
- Use the `config.bnf` example from examples.md as the primary example. Show the bare-minimum grammar first for instant gratification, then the full example.
- Include the `plugin.xml` and supporting Java classes from examples.md. These are needed for the "Project setup" section to feel complete, even though the reader won't run the full plugin until Section 1.4.
- The version compatibility table should be concise (4-5 rows). Do not reproduce the entire CHANGELOG.
- System properties (`grammar.kit.gen.dir`, etc.) belong in a compact table, not individual subsections.
- Forward-link to Section 1.4 (Quick Start Tutorial) at the end. Forward-link to Section 4.2.1 (Gradle Plugin Setup) from the project setup section.
- Use the corrected marketplace URL: `https://plugins.jetbrains.com/plugin/6606-grammar-kit` (references: HTTPS with slug).
- Use the corrected Maven artifact ID: `org.jetbrains:grammar-kit` lowercase (references: MavenCentral confirmed).
- The "Development environment" outline section is thin on evidence. Recommend merging it as an H3 under "Project setup" to avoid a sparse section.

---

## Suggested Page Structure (for drafter)

```
H1: Installation and Setup

H2: Prerequisites
  (compact requirements list/table, forward-link to version matrix)

H2: Installing the plugin
  H3: From the marketplace
    (3-step numbered list)
  H3: Version compatibility
    (table: Grammar-Kit version | IntelliJ | Java)
  H3: Verifying the installation
    (create .bnf, check icon/highlighting, try Live Preview)

H2: Project setup
  (directory structure diagram, build.gradle.kts snippet, dependencies)
  H3: Configuring the development environment
    (source roots, gen/ VCS decision, system properties table)
    (link to SDK docs for SDK setup)

H2: Your first grammar file
  (bare-minimum example, then full config.bnf example)
  (three-part structure explanation: attributes, tokens, rules)
  (editor features table with shortcuts)
  (validation: Live Preview test)

(closing line linking to Quick Start Tutorial)
```

This merges "Development environment" into "Project setup" as an H3, keeping the page to 3 major H2 sections after Prerequisites. The outline's five topics are all covered; the grouping avoids a thin standalone section.
