# Merged Grammar-Kit User Task Map

This map merges (1) the repo-facing “what you can do” list and shortcuts, (2) the IntelliJ Platform SDK “what you must wire up” steps, and (3) the richer tuning and maintenance tasks from your attached agent output.  ([GitHub][1])

---

## A) User personas

### Persona 1: IntelliJ plugin developer (interactive)

Edits `*.bnf` and `*.flex` inside an IDE, uses Live Preview and inspections, then generates code and runs `runIde`. ([GitHub][1])

### Persona 2: Build/CI user (Gradle)

Runs deterministic generation via Gradle tasks (not IDE actions), commits or packages generated sources, and keeps builds green across IDE upgrades. ([JetBrains Marketplace][2])

### Persona 3: Grammar maintainer (evolving a grammar)

Refactors rules, fixes precedence and recovery, adds PSI behaviors, and manages migrations across Grammar-Kit and IntelliJ Platform changes.  ([JetBrains Platform][3])

---

## B) End-to-end story (“happy path”)

1. **Install and enable Grammar-Kit**

* **Purpose:** Add BNF and JFlex editor support plus generators.
* **Inputs:** IDE plugin install.
* **Outputs:** New file types and generator actions available.
* **Where:** IDE Settings | Plugins → Marketplace → “Grammar-Kit”. (Also listed in JetBrains plugin repo.)
* **Verify:** You can open/create `*.bnf` and see Grammar-Kit actions and shortcuts. ([JetBrains Marketplace][4])

2. **Create a `*.bnf` grammar**

* **Purpose:** Define tokens and grammar rules, plus generator settings (packages, parser class names).
* **Inputs:** `MyLanguage.bnf`.
* **Outputs:** A grammar that Live Preview can parse.
* **Where:** Create a `*.bnf` file in your plugin project (commonly under `src/main/java` or a dedicated grammar folder).
* **Verify:** Editor highlighting and Structure view reflect rules; no critical BNF errors. ([GitHub][1])

3. **Tune grammar quickly with Live Preview + Structure view**

* **Purpose:** Validate rule shape and recoverability before generating code.
* **Inputs:** `*.bnf` + sample text in preview.
* **Outputs:** Preview parse tree and highlighting.
* **Where:** “Live preview” action (Ctrl-Alt-P / Cmd-Alt-P). Optional: start/stop evaluator highlighting (Ctrl-Alt-F7 / Cmd-Alt-F7) in preview editor.
* **Verify:** Preview tree matches expectations; fewer “failed” nodes; rule navigation works. ([GitHub][1])
  **Note:** Live Preview uses a simplified “toy lexer” built from `regexp:` and literal tokens; it can differ from your real JFlex lexer behavior. ([IntelliJ Support][5])

4. **Generate parser, PSI, and element types**

* **Purpose:** Produce parser and PSI scaffolding from the BNF.
* **Inputs:** `*.bnf` (with header attributes like parser/PSI packages and class names).
* **Outputs:** Generated parser + `*Types`/element types + PSI interfaces/impls (location depends on your project configuration, often `gen/` or `src/main/gen`).
* **Where:** “Generate parser/ElementTypes/PSI classes” (Ctrl-Shift-G / Cmd-Shift-G).
* **Verify:** Generated sources appear and compile; navigation “go to related file” reaches generated outputs. ([GitHub][1])

5. **Create a `*.flex` lexer spec**

* **Purpose:** Define tokenization that matches your language needs (states, unicode, bad characters).
* **Inputs:** `MyLanguage.flex`.
* **Outputs:** A JFlex spec that returns IntelliJ token types.
* **Where:** Grammar-Kit context menu: “Generate lexer *.flex file” (or create manually, often based on the SDK tutorial pattern).
* **Verify:** The token set and names align with what the parser expects. ([GitHub][1])

6. **Run JFlex generator to produce the lexer class**

* **Purpose:** Generate a Java lexer used at runtime.
* **Inputs:** `*.flex`.
* **Outputs:** Generated lexer class (often under `gen/` like `src/main/gen/.../MyLanguageLexer`).
* **Where:** Context menu on the `*.flex` file → “Run JFlex Generator”.
* **Verify:** Class is generated and compiles. If this is the first run, the IDE prompts for a folder to download the JFlex library and skeleton; choose the project root. ([JetBrains Marketplace][6])

7. **Wire lexer + parser into the IntelliJ language pipeline**

* **Purpose:** Make the IDE use your lexer/parser for files of your language.
* **Inputs:** Generated lexer, generated parser, generated `*Types`, plus your handwritten glue code.
* **Outputs:** `ParserDefinition`, lexer adapter (often `FlexAdapter`), token sets, root PSI file class.
* **Where:** Implement `ParserDefinition.createLexer()` and `createParser()`, return `*Types.Factory.createElement(node)` from `createElement()`. Register via `lang.parserDefinition` extension in `plugin.xml`.
* **Verify:** Running `runIde` recognizes your file type and builds PSI; PSI Viewer shows tokens and PSI nodes. ([JetBrains Marketplace][6])

8. **Add parsing tests and validate output**

* **Purpose:** Lock in grammar behavior and catch regressions.
* **Inputs:** Test data files + parsing test code; updated grammar definitions for negative cases.
* **Outputs:** Passing parsing tests in CI and locally.
* **Where:** Use the SDK “Parsing Test” flow; update grammar and regenerate when instructed.
* **Verify:** Tests pass; parse tree output matches expected. ([JetBrains Marketplace][7])

---

## C) Task map (main artifact)

> Format: **Goal → Tasks → Subtasks**. Each top-level task includes a compact “card”.

### 1) Set up Grammar-Kit tooling

* **User intent:** Enable grammar editing, preview, and generators.
* **Entry points:** Install “Grammar-Kit” plugin; open `*.bnf` / `*.flex`. ([JetBrains Marketplace][4])
* **Inputs:** IDE plugin install; project on Java 17+ for newer Grammar-Kit plugin versions. ([GitHub][1])
* **Outputs:** BNF + JFlex editor support; generator actions available.
* **Verification:** Shortcuts and context menu items appear in `*.bnf` and `*.flex`. ([GitHub][1])
* **Common failure modes:**

   * Plugin loads but actions missing → file is not recognized as `*.bnf`/`*.flex`.
   * Java runtime mismatch (plugin requires Java 17 since 2022.3) → run IDE on correct runtime. ([GitHub][1])
* **Source anchors:** `README.md` “General usage instructions”, “Plugin features”. ([GitHub][1])

---

### 2) Create a BNF grammar skeleton

* **User intent:** Start a language grammar with correct generator metadata.
* **Entry points:** Create `*.bnf`; Structure view; documentation popup (Ctrl-Q / Cmd-J). ([GitHub][1])
* **Inputs:** `MyLanguage.bnf` header attributes (parser/PSI packages, class names).
* **Outputs:** A grammar file ready for Live Preview and generation.
* **Verification:** Structure view lists rules; Ctrl-Q shows FIRST/FOLLOWS and PSI hints for rules. ([GitHub][1])
* **Common failure modes:**

   * Wrong package/class attributes → generated files go to unexpected packages or fail compile.
   * Unintended literal matching in rules → confirm token vs literal semantics in BNF. ([IntelliJ Support][5])
* **Source anchors:** `README.md` “Syntax overview”; agent: `TUTORIAL.md` sections on grammar header and tokens.  ([GitHub][1])

---

### 3) Define tokens and lexical expectations (BNF side)

* **User intent:** Make parser rules refer to stable token types.
* **Entry points:** BNF token block; inspections; matched-expression navigation (Ctrl-B / Cmd-B in attribute patterns). ([GitHub][1])
* **Inputs:** `tokens=[ ... ]` in `*.bnf` (including `regexp:` tokens and literal tokens).
* **Outputs:** Token names used by grammar rules and generator.
* **Verification:** Live Preview recognizes tokens; generated `*Types` contains token constants.
* **Common failure modes:**

   * Token conflicts in Live Preview (first matcher wins) → adjust token order or move complexity into JFlex. ([IntelliJ Support][5])
   * Newlines/spaces “disappear” in Live Preview due to whitespace heuristics → ensure whitespace handling matches your goals. ([GitHub][8])
* **Source anchors:** agent: examples in `testData/livePreview/*`; forum explanations of Live Preview lexer.  ([IntelliJ Support][5])

---

### 4) Author core grammar rules (statements, blocks, lists)

* **User intent:** Parse real code into a stable PSI tree shape.
* **Entry points:** BNF editor + inspections; Live Preview (Ctrl-Alt-P). ([GitHub][1])
* **Inputs:** Rule definitions in `*.bnf`.
* **Outputs:** Parseable grammar; predictable PSI node hierarchy.
* **Verification:** Live Preview tree matches intended nesting; Structure view reflects key rules.
* **Common failure modes:**

   * Left recursion that Grammar-Kit cannot generate → rewrite into iterative/list forms or expression patterns. ([IntelliJ Support][9])
   * Ambiguity from overlapping prefixes → factor shared prefixes; use pin/recoverWhile where needed.
* **Source anchors:** agent: `TUTORIAL.md` and `HOWTO.md` tuning guidance.

---

### 5) Implement expression precedence and associativity

* **User intent:** Parse `a + b * c` into the right tree without deep nesting.
* **Entry points:** Edit expression rules; Live Preview; regenerate and inspect PSI.
* **Inputs:** Expression rules (often layered) and optional attributes (`extends`, associativity flags, etc.).
* **Outputs:** Correct precedence parse tree and manageable PSI structure.
* **Verification:** Target expressions parse into expected nesting.
* **Common failure modes:**

   * Deep trees or wrong grouping → adjust precedence layering; adopt HOWTO expression patterns.  ([IntelliJ Support][10])
* **Source anchors:** agent: `HOWTO.md` “Compact expression parsing”; support discussions on deep trees.  ([IntelliJ Support][10])

---

### 6) Design error recovery and reporting

* **User intent:** Keep PSI usable on incomplete or invalid code in the editor.
* **Entry points:** Add `pin` and `recoverWhile` attributes; Live Preview on broken input.
* **Inputs:** `*.bnf` rule attributes.
* **Outputs:** Parser that continues past errors and builds partial PSI.
* **Verification:** Broken input still yields a meaningful PSI tree in preview and runtime.
* **Common failure modes:**

   * `recoverWhile` without an effective pin → recovery never triggers or loops.
   * Misplaced pin commits too early → wrong branch “wins”. ([Stack Overflow][11])
* **Source anchors:** agent: `HOWTO.md` recovery sections; error-handling Q&A.  ([IntelliJ Support][12])

---

### 7) Use Live Preview as the fast iteration loop

* **User intent:** Catch grammar shape problems before generating and wiring code.
* **Entry points:** Live Preview (Ctrl-Alt-P); evaluator highlighting (Ctrl-Alt-F7).
* **Inputs:** `*.bnf` + sample snippet.
* **Outputs:** Preview parse tree and rule coverage signal.
* **Verification:** Parse tree stabilizes as you iterate; fewer “unexpected” nodes.
* **Common failure modes:**

   * Live Preview differs from runtime lexer behavior → treat preview as parser-shape tool, not final tokenization truth. ([IntelliJ Support][5])
   * Whitespace/newline handling surprises → see LivePreviewLexer whitespace heuristics and related issues. ([GitHub][8])
* **Source anchors:** `README.md` “Live preview”; Live Preview behavior discussions/issues. ([GitHub][1])

---

### 8) Generate parser, PSI, and element types (IDE generator)

* **User intent:** Produce compile-ready parser and PSI scaffolding.
* **Entry points:** “Generate parser/ElementTypes/PSI classes” (Ctrl-Shift-G). ([GitHub][1])
* **Inputs:** `*.bnf` (generator attributes must be correct).
* **Outputs:** Parser class, `*Types`, PSI interfaces/impls, element types, sometimes `parserUtilClass`. ([GitHub][1])
* **Verification:** Generated sources compile; “go to related file” finds generated parser/PSI. ([GitHub][1])
* **Common failure modes:**

   * Stale generated output → delete/purge generated dirs and regenerate.
   * Generated PSI missing mixin methods when using Gradle path → use IDE generator for two-pass mixins. ([GitHub][1])
* **Source anchors:** `README.md` “General usage instructions”, “Using with Gradle”. ([GitHub][1])

---

### 9) Generate a JFlex `*.flex` from BNF (optional bootstrap)

* **User intent:** Get a starter lexer spec aligned with tokens and literals.
* **Entry points:** Context menu: generate `*.flex`. ([GitHub][1])
* **Inputs:** `*.bnf` token definitions.
* **Outputs:** `*.flex` skeleton.
* **Verification:** `*.flex` compiles under JFlex generation.
* **Common failure modes:**

   * Escaping edge cases (example: double-quote token) → adjust generated lexer rules manually or use regexp tokens. ([GitHub][13])
* **Source anchors:** `README.md` generator features; issue history for lexer generation pitfalls. ([GitHub][1])

---

### 10) Author and maintain a real JFlex lexer

* **User intent:** Implement production-grade tokenization (states, unicode, bad characters).
* **Entry points:** Edit `*.flex`; run “Run JFlex Generator”.
* **Inputs:** `MyLanguage.flex`.
* **Outputs:** Generated lexer class.
* **Verification:** Token stream matches expectations; runtime parsing matches preview intent.
* **Common failure modes:**

   * Lexer does not cover full file (gaps) or aborts early → ensure a catch-all bad character rule and full coverage. ([JetBrains Marketplace][14])
   * First run JFlex download prompt confusion → choose project root for skeleton/JFlex download. ([JetBrains Marketplace][6])
* **Source anchors:** SDK “Implementing Lexer” and “Lexer and Parser Definition”. ([JetBrains Marketplace][14])

---

### 11) Integrate generated code into the plugin (ParserDefinition, token sets, root file)

* **User intent:** Make the IDE use the generated lexer/parser for your language files.
* **Entry points:** Implement `ParserDefinition`; register `lang.parserDefinition` in `plugin.xml`.
* **Inputs:** Generated lexer/parser, `*Types`, handwritten adapter (`FlexAdapter`) and token sets.
* **Outputs:** Working PSI pipeline in the IDE.
* **Verification:** `runIde` opens files, PSI Viewer shows tokens and PSI nodes; no extension-point errors. ([JetBrains Marketplace][6])
* **Common failure modes:**

   * Token sets not constants (unnecessary classloading) → follow SDK advice to use constants from a dedicated `$Language$TokenSets`. ([JetBrains Marketplace][6])
   * plugin.xml misregistration → confirm extension point and class name. ([JetBrains Marketplace][6])
* **Source anchors:** SDK “Lexer and Parser Definition”, “Implementing Parser and PSI”. ([JetBrains Marketplace][6])

---

### 12) Add PSI behaviors (names, references, resolve, rename)

* **User intent:** Enable navigation, rename, find usages, and semantic features.
* **Entry points:** PSI mixins (`psiImplUtilClass`, methods attributes), `getReference()`, `resolve()`, `setName()`.
* **Inputs:** BNF PSI customization attributes + handwritten PSI utility code.
* **Outputs:** PSI methods available on generated elements.
* **Verification:** “Go to Declaration”, “Find Usages”, “Rename” work for identifiers.
* **Common failure modes:**

   * Everything becomes a reference (because all uses share `id`) → implement references on the correct PSI nodes (usage sites), not on a generic `id` leaf. ([JetBrains Platform][15])
   * Gradle generation lacks method mixins → use IDE generation for two-pass mixins. ([GitHub][1])
* **Source anchors:** platform discussion on references/rename/stubs; agent: PSI customization task. ([JetBrains Platform][15])

---

### 13) Add stubs for scale (optional, performance and indexing)

* **User intent:** Make resolve/indexing fast on large codebases.
* **Entry points:** Stub-related BNF attributes and handwritten stub element types; indexing APIs.
* **Inputs:** PSI elements chosen for stubbing + stub serialization/versioning.
* **Outputs:** Stub-based PSI elements and indexes.
* **Verification:** “Find Usages” and resolve get faster; indexing remains stable.
* **Common failure modes:**

   * Stub serialization bugs or version mismatches → bump stub version and test round-trip.
   * Over-stubbing everything → stub only key declaration nodes first. ([JetBrains Platform][15])
* **Source anchors:** agent: stub support section; platform questions about stubbing and performance.  ([JetBrains Platform][15])

---

### 14) Create parsing tests and regression harness

* **User intent:** Prevent grammar changes from silently breaking PSI shape.
* **Entry points:** SDK parsing test pattern; run tests in IDE/CI.
* **Inputs:** Test files, expected PSI output, updated grammar for negative cases.
* **Outputs:** Automated parsing tests.
* **Verification:** Tests pass; failures produce actionable diffs.
* **Common failure modes:**

   * Forgot to regenerate after grammar change → regenerate parser and rerun tests. ([JetBrains Marketplace][7])
* **Source anchors:** SDK “Parsing Test”. ([JetBrains Marketplace][7])

---

### 15) Use IDE grammar refactorings and navigation

* **User intent:** Keep grammars maintainable as they grow.
* **Entry points:**

   * Refactoring: “extract rule” (Ctrl-Alt-M / Cmd-Alt-M)
   * Refactoring: “introduce token” (Ctrl-Alt-C / Cmd-Alt-C)
   * Intention: “flip choice branches” (Alt-Enter)
   * Editing: unwrap/remove expression (Ctrl-Shift-Del / Cmd-Shift-Del)
   * Navigation: structure popup (Ctrl-F12 / Cmd-F12)
   * Navigation: go to related file (Ctrl-Alt-Home / Cmd-Alt-Home) ([GitHub][1])
* **Inputs:** `*.bnf`, `*.flex`.
* **Outputs:** Refactored grammar, faster navigation.
* **Verification:** Same sample inputs still parse; diffs are clean.
* **Common failure modes:**

   * Refactor breaks pin/recovery attributes → re-check recovery and preview on broken input.
* **Source anchors:** `README.md` “Plugin features”. ([GitHub][1])

---

### 16) Automate generation in Gradle/CI (alternative to IDE generator)

* **User intent:** Reproducible builds and CI generation.
* **Entry points:** Gradle tasks `generateParser`, `generateLexer`; `grammarKit { ... }` extension. ([JetBrains Marketplace][2])
* **Inputs:** `*.bnf`, `*.flex`, Gradle configuration (sourceFile, output dirs, purgeOldFiles).
* **Outputs:** Generated sources in configured target directories.
* **Verification:** `./gradlew generateParser generateLexer` succeeds; CI caches and artifacts contain generated code.
* **Common failure modes:**

   * Expecting method mixins to work → Gradle plugin does not support two-pass generation, so method mixins are unsupported. ([JetBrains Marketplace][2])
   * Wrong output dirs cause stale classes → enable `purgeOldFiles` or clean output dirs. ([JetBrains Marketplace][2])
* **Source anchors:** SDK “Gradle Grammar-Kit Plugin”; repo README “Using with Gradle” limitations. ([JetBrains Marketplace][2])

---

### 17) Maintain compatibility across IntelliJ Platform changes

* **User intent:** Keep generated code valid across IDE upgrades.
* **Entry points:** Upgrade IDE, Grammar-Kit plugin, Gradle plugin; watch issues and forum.
* **Inputs:** Existing grammar + generated code + platform version.
* **Outputs:** Updated generated code and fixes for breaking API/annotation changes.
* **Verification:** Project compiles on target IDE baseline; runIde starts.
* **Common failure modes:**

   * Generated annotations become invalid on new IDE (example: `@Experimental` placement) → track Grammar-Kit issue and adjust generation inputs or pin versions until fixed. ([JetBrains Platform][3])
* **Source anchors:** platform thread on invalid generated annotation; repo release discussions. ([JetBrains Platform][3])

---

### 18) Visualize PSI structure (optional)

* **User intent:** Explain and audit PSI shape for contributors and debugging.
* **Entry points:** PSI tree diagram (requires UML plugin). ([GitHub][1])
* **Inputs:** Generated PSI model.
* **Outputs:** Diagram view of PSI tree.
* **Verification:** Diagram matches expected parent/child relationships.
* **Common failure modes:**

   * UML plugin missing → install/enable UML support first. ([GitHub][1])
* **Source anchors:** `README.md` “Diagram: PSI tree diagram (UML plugin required)”. ([GitHub][1])

---

## D) Alternative paths

### Gradle-based generation instead of IDE actions

* Use `org.jetbrains.grammarkit` and run `generateParser` / `generateLexer`; configure output dirs and optionally `purgeOldFiles`. ([JetBrains Marketplace][2])
* Accept tradeoffs: no two-pass generation, so method mixins are not supported (also noted in README). ([JetBrains Marketplace][2])

### “Start from BNF only” vs “Start from JFlex first”

* **BNF-first:** Use `regexp:` and literal tokens to validate rule shape in Live Preview, then introduce JFlex later for production tokenization. ([IntelliJ Support][5])
* **JFlex-first:** Build a real lexer early when whitespace, newlines, or context-sensitive tokens matter, then align BNF tokens to the lexer output. ([JetBrains Marketplace][14])

### Iteration loop (recommended)

1. Edit grammar (`*.bnf`) → Live Preview (`Ctrl-Alt-P`) → adjust recovery/precedence
2. Generate parser/PSI (`Ctrl-Shift-G`)
3. Update lexer (`*.flex`) → Run JFlex Generator
4. Run parsing tests and `runIde`
5. Repeat with small diffs ([GitHub][1])

---

## E) Debugging and iteration tasks (when things break)

### Live Preview differs from real lexer behavior

* **Symptom:** Preview parses “fine” but runtime parsing fails or token boundaries differ.
* **Fix:** Treat Live Preview as parser-shape feedback only; validate tokens with PSI Viewer at runtime and rely on JFlex for production lexing. ([IntelliJ Support][5])

### Whitespace/newline handling surprises

* **Symptom:** Newlines get treated as whitespace in preview; grammar cannot “see” them.
* **Fix:** Understand LivePreviewLexer heuristics; move newline-sensitive behavior into the real lexer when needed. ([GitHub][8])

### Ambiguity and precedence issues

* **Symptom:** Wrong branch chosen, unstable parse tree, deep expression nodes.
* **Fix:** Refactor expressions into precedence layers; add pins and recovery predicates at stable points.  ([IntelliJ Support][10])

### Token/lexer mismatch

* **Symptom:** Parser expects a token that lexer never emits (or emits too broadly).
* **Fix:** Align token names and patterns; ensure lexer covers entire file and emits `BAD_CHARACTER` when needed. ([JetBrains Marketplace][14])

### Regeneration gotchas (stale output, wrong dirs)

* **Symptom:** Changes do not appear; compilation uses old generated classes.
* **Fix:** Purge generated dirs; in Gradle enable `purgeOldFiles` or clean tasks; in IDE delete and regenerate. ([JetBrains Marketplace][2])

### Generated code breaks on IDE upgrade

* **Symptom:** New platform annotations or APIs cause compilation errors.
* **Fix:** Pin Grammar-Kit/Gradle plugin versions; follow issue threads; regenerate after upgrades and adjust inputs. ([JetBrains Platform][3])

---

## F) Output checklist

* [ ] Grammar-Kit plugin installed; `*.bnf` and `*.flex` actions available ([GitHub][1])
* [ ] `*.bnf` parses in Live Preview (Ctrl-Alt-P) with representative samples ([GitHub][1])
* [ ] Parser/PSI generated (Ctrl-Shift-G) and compiles ([GitHub][1])
* [ ] `*.flex` lexer generated/maintained and JFlex generator run successfully ([JetBrains Marketplace][6])
* [ ] `ParserDefinition` implemented and registered in `plugin.xml` ([JetBrains Marketplace][6])
* [ ] `runIde` starts and PSI Viewer shows tokens and PSI nodes ([JetBrains Marketplace][6])
* [ ] Parsing tests added and pass; regenerated after grammar edits ([JetBrains Marketplace][7])
* [ ] (If CI) Gradle `generateParser`/`generateLexer` configured and reproducible ([JetBrains Marketplace][2])

---

## G) Gaps and questions (what still needs stronger evidence)

1. **Multi-file grammar composition**

* **What’s unclear:** Whether there is a first-class “import/include” mechanism for splitting BNF across files, or whether users rely on copy/paste and shared token sets.
* **Evidence to look for:** Repo examples under `grammars/` or `testData/` that reference multiple BNF files; generator settings that mention imports. (Agent map flags this as unclear.)

2. **Official, complete BNF syntax reference**

* **What’s unclear:** A single authoritative “all attributes and syntax” page; users ask for it explicitly.
* **Evidence to look for:** Consolidated docs page in repo; “BNF complete syntax” answers and links. ([IntelliJ Support][16])

3. **Lexer introspection tooling**

* **What’s unclear:** Whether Grammar-Kit provides a “Live Preview for lexer tokens” comparable to parser Live Preview (users request it).
* **Evidence to look for:** Open issues and plugin UI actions; current state suggests it is requested, not standard. ([GitHub][17])

4. **CHANGELOG-driven migration notes**

* **What’s unclear:** Exact renamed/changed user-facing attributes and generator behaviors across versions.
* **Evidence to look for:** `CHANGELOG.md` entries tied to attribute renames, and upgrade guides; also forum threads around breakages (example: generated annotation changes). ([JetBrains Platform][3])

[1]: https://github.com/JetBrains/Grammar-Kit "GitHub - JetBrains/Grammar-Kit: Grammar files support & parser/PSI generation for IntelliJ IDEA"
[2]: https://plugins.jetbrains.com/docs/intellij/tools-gradle-grammar-kit-plugin.html "Gradle Grammar-Kit Plugin | IntelliJ Platform Plugin SDK"
[3]: https://platform.jetbrains.com/t/invalid-experimental-annotation-generated-in-2025-1/1406?utm_source=chatgpt.com "Invalid @Experimental annotation generated in 2025.1"
[4]: https://plugins.jetbrains.com/plugin/6606-grammar-kit?utm_source=chatgpt.com "Grammar-Kit Plugin for JetBrains IDEs"
[5]: https://intellij-support.jetbrains.com/hc/en-us/community/posts/12946208974994-BNF-Live-Preview-rule-ordering-issue?utm_source=chatgpt.com "BNF Live Preview rule ordering issue"
[6]: https://plugins.jetbrains.com/docs/intellij/lexer-and-parser-definition.html "4. Lexer and Parser Definition | IntelliJ Platform Plugin SDK"
[7]: https://plugins.jetbrains.com/docs/intellij/parsing-test.html?utm_source=chatgpt.com "2. Parsing Test | IntelliJ Platform Plugin SDK"
[8]: https://github.com/JetBrains/Grammar-Kit/issues/124?utm_source=chatgpt.com "maunual newline/whitespace handling? · Issue #124"
[9]: https://intellij-support.jetbrains.com/hc/en-us/community/posts/206122629-Starting-point-for-a-Java-like-grammar-for-Grammar-Kit?utm_source=chatgpt.com "Starting point for a Java-like grammar for Grammar-Kit?"
[10]: https://intellij-support.jetbrains.com/hc/en-us/community/posts/115000094104-Expression-handling-in-grammar-kit-issue-with-deep-trees?utm_source=chatgpt.com "Expression handling in grammar-kit - issue with deep trees"
[11]: https://stackoverflow.com/questions/48701510/pin-recoverwhile-in-a-bnf-parsing?utm_source=chatgpt.com "Pin & recoverWhile in a .bnf (Parsing) - intellij idea"
[12]: https://intellij-support.jetbrains.com/hc/en-us/community/posts/206819809-Error-Handling-in-Grammar-kit?utm_source=chatgpt.com "Error Handling in Grammar kit"
[13]: https://github.com/JetBrains/Grammar-Kit/issues/19?utm_source=chatgpt.com "Generate JFlex Lexer doesn't handle \"double quote\" ..."
[14]: https://plugins.jetbrains.com/docs/intellij/implementing-lexer.html?utm_source=chatgpt.com "Implementing Lexer | IntelliJ Platform Plugin SDK"
[15]: https://platform.jetbrains.com/t/custom-language-support-questions-also-next-steps-after-simple/2032?utm_source=chatgpt.com "Custom Language support questions - also next steps after Simple"
[16]: https://intellij-support.jetbrains.com/hc/en-us/community/posts/12925006569362-Grammar-Kit-BNF-complete-syntax?utm_source=chatgpt.com "Grammar-Kit BNF complete syntax"
[17]: https://github.com/JetBrains/Grammar-Kit/issues/301?utm_source=chatgpt.com "LivePreview for Lexer · Issue #301 · JetBrains/Grammar-Kit"
