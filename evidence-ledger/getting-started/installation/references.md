# References: Installation and Setup

## Scope Information
This validates references for section 1.3: Installation and Setup.
Covers prerequisites, plugin installation, project setup, and first grammar file.

---

## Internal Links (Documentation Cross-References)
- Prerequisites: `docs/index.md` (Section 1.1 - What is Grammar-Kit?)
- Related: `docs/features.md` (Section 1.2 - Features)
- Next: `docs/quick-start.md` (Section 1.4 - Quick Start Tutorial)
- Advanced: `docs/integration/gradle-setup.md` (Section 4.2.1 - Gradle Plugin Setup)
- Advanced: `docs/code-generation/attributes.md` (Section 3.1 - Attributes System)

---

## Code References

### Plugin Identity and Configuration
| Reference | File | Line(s) | Status |
|---|---|---|---|
| Plugin ID: `org.jetbrains.idea.grammar` | `resources/META-INF/plugin.xml` | L2 | ✅ Verified |
| Plugin name: `Grammar-Kit` | `resources/META-INF/plugin.xml` | L5 | ✅ Verified |
| Vendor: JetBrains | `resources/META-INF/plugin.xml` | L3 | ✅ Verified |
| Description text | `resources/META-INF/plugin.xml` | L6 | ✅ Verified |
| Plugin group: `org.jetbrains` | `gradle.properties` | L3 | ✅ Verified |
| Dev version: `2023.3-dev` | `gradle.properties` | L6 | ✅ Verified |
| License: Apache 2.0 | `build.gradle.kts` | L217 | ✅ Verified |

### System Requirements
| Claim | Source | Line(s) | Status |
|---|---|---|---|
| Java 17 required since 2022.3 | `README.md` | L19 | ✅ Verified |
| `javaVersion=17` (compile target) | `gradle.properties` | L33 | ✅ Verified |
| Default generated Java version: 11 | `src/.../generator/GenOptions.java` | L65 | ✅ Verified: `StringUtil.parseInt(genOptions.get("java"), 11)` |
| Since build `233` (IntelliJ 2023.3+) | `gradle.properties` | L9 | ✅ Verified |
| Platform type: IU | `gradle.properties` | L12 | ✅ Verified |

### Plugin Dependencies
| Dependency | Type | Source | Line | Status |
|---|---|---|---|---|
| `com.intellij.modules.lang` | Required | `plugin.xml` | L9 | ✅ Verified |
| `com.intellij.copyright` | Optional | `plugin.xml` | L10 | ✅ Verified |
| `com.intellij.java` | Optional | `plugin.xml` | L11 | ✅ Verified |
| `com.intellij.diagram` | Optional | `plugin.xml` | L12 | ✅ Verified |

### Plugin Settings (System Properties)
| Property | Default | Source | Line | Status |
|---|---|---|---|---|
| `grammar.kit.gen.dir` | `"gen"` | `src/.../config/Options.java` | L14 | ✅ Verified |
| `grammar.kit.gen.jflex.args` | `""` | `src/.../config/Options.java` | L15 | ✅ Verified |
| `grammar.kit.gpub.max.level` | `1000` | `src/.../config/Options.java` | L17 | ✅ Verified |
| `grammar.kit.inject.java` | `true` | `src/.../config/Options.java` | L19 | ✅ Verified |
| `grammar.kit.inject.regexp` | `true` | `src/.../config/Options.java` | L20 | ✅ Verified |

### Default Attribute Values (KnownAttribute.java)
| Attribute | Default | Line | Status |
|---|---|---|---|
| `parserClass` | `"generated.GeneratedParser"` | L46 | ✅ Verified |
| `psiPackage` | `"generated.psi"` | L41 | ✅ Verified |
| `psiImplPackage` | `"generated.psi.impl"` | L42 | ✅ Verified |
| `elementTypeHolderClass` | `"generated.GeneratedTypes"` | L48 | ✅ Verified |
| `psiClassPrefix` | `""` (empty) | L38 | ✅ Verified |
| `psiImplClassSuffix` | `"Impl"` | L39 | ✅ Verified |
| `psiVisitorName` | `"Visitor"` | L43 | ✅ Verified |
| `extendedPin` | `true` | L35 | ✅ Verified |
| `generatePsi` | `true` | L31 | ✅ Verified |
| `generateTokens` | `true` | L32 | ✅ Verified |
| `generateFirstCheck` | `2` | L34 | ✅ Verified |

### File Types
| File Type | Extension | Language ID | Source | Status |
|---|---|---|---|---|
| BNF | `.bnf` | `BNF` | `plugin.xml` L15, `BnfFileType.java` L36-37 | ✅ Verified |
| JFlex | `.flex` | `JFlex` | `plugin.xml` L96 | ✅ Verified |
| Live Preview | (internal) | `BNF_LP` | `plugin.xml` L16 | ✅ Verified |

### Directory Structure Recommendation
| Claim | Source | Line | Status |
|---|---|---|---|
| "Handwritten classes and generated classes should always be in different source roots." | `HOWTO.md` | L11 | ✅ Verified (exact quote) |
| Source dirs: `src`, `gen`, `resources` | `build.gradle.kts` | L46-53 | ✅ Verified |
| `gen` marked as generated source dir | `build.gradle.kts` | L59 | ✅ Verified |
| Gen dir uses `Options.GEN_DIR` | `FileGeneratorUtil.java` | L88 | ✅ Verified |

### Maven Publishing Coordinates
| Claim | Source | Status |
|---|---|---|
| groupId: `org.jetbrains` | `build.gradle.kts` L206 | ✅ Verified |
| artifactId: `Grammar-Kit` (project name) | `build.gradle.kts` L207 | ✅ Verified |
| Artifact jar: `grammar-kit` | `build.gradle.kts` L135 | ✅ Verified |
| Published to MavenCentral via Sonatype | `build.gradle.kts` L238-245 | ✅ Verified |

### Gradle Plugin Limitations
| Claim | Source | Line | Status |
|---|---|---|---|
| Method mixins not supported | `README.md` | L51 | ✅ Verified |
| Generic signatures may not be correct | `README.md` | L52 | ✅ Verified |

### GeneratedParserUtilBase
| Claim | Source | Line | Status |
|---|---|---|---|
| Included in IntelliJ Platform since 12.1 | `README.md` | L209 | ✅ Verified |
| GPUB class: `com.intellij.lang.parser.GeneratedParserUtilBase` | `BnfConstants.java` | L18 | ✅ Verified |

### Example Grammar Files
| File | Path | Status |
|---|---|---|
| JSON grammar (minimal) | `testData/livePreview/Json.bnf` | ✅ File exists |
| Expression parser | `testData/generator/ExprParser.bnf` | ✅ File exists |
| Live Preview tutorial | `testData/livePreview/LivePreviewTutorial.bnf` | ✅ File exists |
| Grammar-Kit self-definition | `grammars/Grammar.bnf` | ✅ File exists |

---

## External Links

### JetBrains / Grammar-Kit Official
| Link | URL | Status |
|---|---|---|
| GitHub Repository | `https://github.com/JetBrains/Grammar-Kit` | ✅ Valid (referenced in plugin.xml L1, build.gradle.kts L116) |
| JetBrains Marketplace | `https://plugins.jetbrains.com/plugin/6606-grammar-kit` | ✅ Valid (page loads) |
| Marketplace (README link) | `http://plugins.jetbrains.com/plugin/6606` | ⚠️ Works but uses HTTP; canonical URL is HTTPS with slug |
| TeamCity dev builds | `https://teamcity.jetbrains.com/guestAuth/app/rest/builds/buildType:IntellijIdeaPlugins_GrammarKit_Build,status:SUCCESS/artifacts/content/GrammarKit*.zip` | ⚠️ Not independently verified; URL from README.md L14 |
| CHANGELOG | `CHANGELOG.md` | ✅ File exists, 409 lines, covers versions 1.0 through 2023.3 |

### Gradle Grammar-Kit Plugin
| Link | URL | Status |
|---|---|---|
| GitHub Repository | `https://github.com/JetBrains/gradle-grammar-kit-plugin` | ✅ Valid (page loads, 94 stars, Apache-2.0) |
| Gradle Plugin Portal | `https://plugins.gradle.org/plugin/org.jetbrains.grammarkit` | ✅ Referenced in README badge |
| IntelliJ SDK Documentation | `https://plugins.jetbrains.com/docs/intellij/tools-gradle-grammar-kit-plugin.html` | ✅ Valid (page loads with full configuration docs) |
| Plugin ID | `org.jetbrains.grammarkit` | ✅ Confirmed from SDK docs |
| Latest version | `2023.3.0.2` | ✅ Confirmed from SDK docs and GitHub releases |
| Default grammarKitRelease | `2022.3.2` | ✅ Confirmed from SDK docs |
| Default jflexRelease | `1.9.2` | ✅ Confirmed from SDK docs |

### MavenCentral
| Link | URL | Status |
|---|---|---|
| Sonatype Central | `https://central.sonatype.com/artifact/org.jetbrains/grammar-kit` | ✅ Valid (page loads) |
| Latest published version | `2023.3` | ✅ Confirmed from Sonatype |
| Maven coordinates | `org.jetbrains:grammar-kit:2023.3` | ✅ Confirmed from POM |

### IntelliJ Platform SDK Documentation
| Link | URL | Status |
|---|---|---|
| Custom Language Support Tutorial | `https://plugins.jetbrains.com/docs/intellij/custom-language-support-tutorial.html` | ✅ Valid (21-step tutorial) |
| Creating a Plugin Project | `https://plugins.jetbrains.com/docs/intellij/creating-plugin-project.html` | ✅ Valid (Gradle project setup) |
| Developing a Plugin | `https://plugins.jetbrains.com/docs/intellij/developing-plugins.html` | ✅ Valid (overview page) |
| IntelliJ Platform Plugin Template | `https://github.com/JetBrains/intellij-platform-plugin-template` | ✅ Referenced in code-evidence |
| Build Number Ranges | `https://plugins.jetbrains.com/docs/intellij/build-number-ranges.html` | ✅ Referenced in gradle.properties L8 |

### Community Resources
| Link | URL | Status |
|---|---|---|
| JetBrains Slack (#intellij-platform) | `https://plugins.jetbrains.com/slack` | ✅ Referenced in README.md L250 |
| X/Twitter @JBPlatform | `https://x.com/JBPlatform` | ✅ Referenced in README.md L251 |

---

## Validation Summary

### Code Evidence Claims Verification

| # | Claim from code-evidence.md | Verdict | Notes |
|---|---|---|---|
| 1 | Plugin ID: `org.jetbrains.idea.grammar` | ✅ Correct | plugin.xml L2 |
| 2 | Marketplace URL: `http://plugins.jetbrains.com/plugin/6606` | ⚠️ Correct but outdated | Uses HTTP; prefer `https://plugins.jetbrains.com/plugin/6606-grammar-kit` |
| 3 | Java 17 required since 2022.3 | ✅ Correct | README.md L19 |
| 4 | Default generated Java version: 11 | ✅ Correct | GenOptions.java L65 |
| 5 | Since build 233 = IntelliJ IDEA 2023.3+ | ✅ Correct | gradle.properties L9 |
| 6 | Required dependency: `com.intellij.modules.lang` | ✅ Correct | plugin.xml L9 |
| 7 | Optional deps: copyright, java, diagram | ✅ Correct | plugin.xml L10-12 |
| 8 | `grammar.kit.gen.dir` default `"gen"` | ✅ Correct | Options.java L14 |
| 9 | `grammar.kit.gen.jflex.args` default `""` | ✅ Correct | Options.java L15 |
| 10 | `grammar.kit.gpub.max.level` default `1000` | ✅ Correct | Options.java L17 |
| 11 | `grammar.kit.inject.java` default `true` | ✅ Correct | Options.java L19 |
| 12 | `grammar.kit.inject.regexp` default `true` | ✅ Correct | Options.java L20 |
| 13 | Maven coordinates: `org.jetbrains:Grammar-Kit` | ⚠️ Partially correct | artifactId in build.gradle.kts uses `project.name` which is `Grammar-Kit`, but the published jar artifact name is `grammar-kit` (L135). MavenCentral shows `org.jetbrains:grammar-kit` (lowercase). The publication artifactId is `Grammar-Kit` (L208 uses `project.name`). |
| 14 | Gradle plugin: `gradle-grammar-kit-plugin` | ✅ Correct | GitHub repo confirmed |
| 15 | Gradle plugin limitations (no mixins, generic issues) | ✅ Correct | README.md L51-52, SDK docs confirm |
| 16 | GeneratedParserUtilBase in Platform since 12.1 | ✅ Correct | README.md L209 |
| 17 | HOWTO.md directory structure advice | ✅ Correct | HOWTO.md L11 (exact quote verified) |
| 18 | Default `parserClass`: `"generated.GeneratedParser"` | ✅ Correct | KnownAttribute.java L46 |
| 19 | Default `psiPackage`: `"generated.psi"` | ✅ Correct | KnownAttribute.java L41 |
| 20 | Default `psiImplPackage`: `"generated.psi.impl"` | ✅ Correct | KnownAttribute.java L42 |
| 21 | Default `elementTypeHolderClass`: `"generated.GeneratedTypes"` | ✅ Correct | KnownAttribute.java L48 |
| 22 | BNF file extension: `.bnf` | ✅ Correct | BnfFileType.java L37, plugin.xml L15 |
| 23 | JFlex file extension: `.flex` | ✅ Correct | plugin.xml L96 |
| 24 | Version compatibility matrix (reconstructed from CHANGELOG) | ✅ Correct | All entries verified against CHANGELOG.md |
| 25 | `2020.3` switched default Java to 11 | ✅ Correct | CHANGELOG.md L67 |
| 26 | `2019.1` switched to year-based versioning | ✅ Correct | CHANGELOG.md L100 |
| 27 | `2017.1` switched to IntelliJ IDEA versioning | ✅ Correct | CHANGELOG.md L157-158 |
| 28 | Code-evidence line ref: "GenOptions.java line 65" | ✅ Correct | Exact line confirmed |
| 29 | Code-evidence line ref: "Options.java line 14" | ✅ Correct | Exact line confirmed |
| 30 | Code-evidence line ref: "plugin.xml line 2" (plugin ID) | ✅ Correct | Exact line confirmed |
| 31 | Code-evidence line ref: "plugin.xml line 9" (modules.lang) | ✅ Correct | Exact line confirmed |

### File Path Verification
- [x] `README.md` - exists, 251 lines
- [x] `CHANGELOG.md` - exists, 409 lines
- [x] `gradle.properties` - exists, 35 lines
- [x] `resources/META-INF/plugin.xml` - exists, 136 lines
- [x] `build.gradle.kts` - exists, 257 lines
- [x] `src/org/intellij/grammar/config/Options.java` - exists, 22 lines
- [x] `src/org/intellij/grammar/config/Option.java` - exists, 59 lines
- [x] `src/org/intellij/grammar/KnownAttribute.java` - exists, 168 lines
- [x] `src/org/intellij/grammar/generator/GenOptions.java` - exists, 68 lines
- [x] `src/org/intellij/grammar/generator/BnfConstants.java` - exists, 44 lines
- [x] `src/org/intellij/grammar/actions/FileGeneratorUtil.java` - exists, 124 lines
- [x] `src/org/intellij/grammar/BnfFileType.java` - exists
- [x] `HOWTO.md` - exists (L11 verified)
- [x] `TUTORIAL.md` - exists (referenced in README)
- [x] `testData/livePreview/Json.bnf` - exists
- [x] `testData/generator/ExprParser.bnf` - exists
- [x] `testData/livePreview/LivePreviewTutorial.bnf` - exists
- [x] `grammars/Grammar.bnf` - exists

---

## Errors Found

### Minor Issues
1. **Marketplace URL uses HTTP**: code-evidence.md references `http://plugins.jetbrains.com/plugin/6606` (from README.md). The canonical URL is `https://plugins.jetbrains.com/plugin/6606-grammar-kit`. Documentation should use the HTTPS version with the slug.

2. **Maven artifactId casing ambiguity**: code-evidence.md states Maven coordinates as `org.jetbrains:Grammar-Kit`. The `build.gradle.kts` publication uses `project.name` (which is `Grammar-Kit` from gradle.properties). However, MavenCentral shows the artifact as `org.jetbrains:grammar-kit` (lowercase `g`). The Gradle Grammar-Kit Plugin SDK docs reference `grammarKitRelease` with version `2022.3.2`. Documentation should clarify: the MavenCentral artifact is `org.jetbrains:grammar-kit` (lowercase).

3. **Missing `[2023.3]` link in CHANGELOG**: The CHANGELOG.md footer has `[2023.3]: https://github.com/JetBrains/Grammar-Kit/compare/2022.3.2...2023.3` but there is no `[Unreleased]` link target for the `## [Unreleased]` header at L3. Actually, L360 has `[Unreleased]: https://github.com/JetBrains/Grammar-Kit/compare/2023.3...HEAD` — this is valid.

4. **Code-evidence references `src/org/intellij/grammar/config/Options.java` as containing "plugin settings"**: The file is actually an interface (not a class), and the code-evidence header says "Options.java" which is correct. No error, but documentation should note these are Java system properties (`-D` flags), not IDE settings UI.

### No Errors (Confirmed Accurate)
- All line number references in code-evidence.md are accurate.
- All default attribute values match KnownAttribute.java source.
- All system property names and defaults match Options.java source.
- Version compatibility matrix entries match CHANGELOG.md.
- Plugin dependency declarations match plugin.xml.
- File type registrations match plugin.xml and BnfFileType.java.

---

## Out of Scope References
These references appear in code-evidence.md but belong to other sections:

| Reference | Belongs To |
|---|---|
| Grammar syntax (rule modifiers, meta rules, predicates) | Section 2.1: BNF Grammar Syntax |
| Attribute system details (pin, recoverWhile, extends) | Section 3.1: Attributes System |
| Parser generation internals (two-pass, code splitting) | Section 3.2: Parser Generation |
| Expression parsing (left recursion, operator precedence) | Section 2.3: Expression Parsing |
| Gradle plugin setup details | Section 4.2.1: Gradle Plugin Setup |
| Quick start tutorial walkthrough | Section 1.4: Quick Start Tutorial |
| Error recovery mechanics | Section 2.4: Error Recovery |
| Live Preview workflow details | Section 2.5: Live Preview Workflow |
| PSI customization (mixin, methods, fake rules) | Section 3.4: PSI Customization |
| JFlex lexer development | Section 3.3: Lexer Integration |

---

## Additional References Discovered During Validation

These references were found during validation and may be useful for the installation section:

| Reference | URL/Path | Relevance |
|---|---|---|
| Gradle Grammar-Kit Plugin SDK docs | `https://plugins.jetbrains.com/docs/intellij/tools-gradle-grammar-kit-plugin.html` | Authoritative Gradle plugin configuration reference |
| Gradle Grammar-Kit Plugin ID | `org.jetbrains.grammarkit` | Needed for build.gradle.kts setup |
| Gradle Grammar-Kit Plugin latest version | `2023.3.0.2` | Version to recommend in docs |
| IntelliJ Platform Gradle Plugin (2.x) | `org.jetbrains.intellij.platform` | Required for modern plugin projects (2024.2+) |
| IntelliJ Platform Plugin Template | `https://github.com/JetBrains/intellij-platform-plugin-template` | Recommended starting point for new projects |
| Creating a Plugin Project (SDK docs) | `https://plugins.jetbrains.com/docs/intellij/creating-plugin-project.html` | Step-by-step new project wizard guide |
| Java version requirements by platform | 2024.2+ requires Java 21; 2022.3+ requires Java 17 | Important for prerequisites section |
| `BnfConstants.GPUB_CLASS` | `com.intellij.lang.parser.GeneratedParserUtilBase` | Runtime dependency class (no bundling needed) |
| Plugin DevKit not bundled since 2023.3 | SDK docs: "must be installed from JetBrains Marketplace" | Relevant prerequisite for Grammar-Kit development |

---

## Validation Checklist
- [x] Code refs valid (2026-02-19)
- [x] File paths accurate (2026-02-19)
- [x] Line numbers verified (2026-02-19)
- [x] External URLs checked (2026-02-19)
- [x] Default values confirmed against source (2026-02-19)
- [x] Version claims verified against CHANGELOG (2026-02-19)
- [x] Plugin dependencies verified against plugin.xml (2026-02-19)
- [x] Maven coordinates verified against MavenCentral (2026-02-19)
- [x] Gradle plugin verified against SDK docs (2026-02-19)
- [x] Example grammar files exist (2026-02-19)
