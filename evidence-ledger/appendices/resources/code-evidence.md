# Section 7.B: Resources — Code Evidence

## 1. Official Resources

**Source: `README.md`, `build.gradle.kts:214-232`**

| Resource | URL |
|---|---|
| GitHub Repository | https://github.com/JetBrains/Grammar-Kit |
| Issue Tracker | https://github.com/JetBrains/Grammar-Kit/issues |
| Plugin Marketplace | https://plugins.jetbrains.com/plugin/6606-grammar-kit |
| Maven Central | `org.jetbrains:Grammar-Kit` |
| Gradle Plugin | https://github.com/JetBrains/gradle-grammar-kit-plugin |

## 2. Documentation Files

**Source: Grammar-Kit repository root**

| File | Content |
|---|---|
| `README.md` | Main documentation, feature overview, syntax reference |
| `TUTORIAL.md` | Step-by-step tutorial with Live Preview workflow |
| `HOWTO.md` | Advanced topics: code patterns, expression parsing, stubs |
| `CHANGELOG.md` | Version history from 1.0 to 2023.3 |
| `LICENSE.md` | Apache 2.0 license |
| `CODE_OF_CONDUCT.md` | Contributor code of conduct |

## 3. Related IntelliJ Platform Resources

**Source: Referenced throughout README.md and HOWTO.md**

| Resource | URL |
|---|---|
| IntelliJ Platform SDK Docs | https://plugins.jetbrains.com/docs/intellij/ |
| Implementing a Parser | https://plugins.jetbrains.com/docs/intellij/implementing-parser-and-psi.html |
| Custom Language Support | https://plugins.jetbrains.com/docs/intellij/custom-language-support.html |
| Plugin Structure | https://plugins.jetbrains.com/docs/intellij/plugin-structure.html |
| Stub Indexes | https://plugins.jetbrains.com/docs/intellij/stub-indexes.html |
| IntelliJ Plugin Template | https://github.com/JetBrains/intellij-platform-plugin-template |

## 4. JFlex Resources

**Source: `src/org/intellij/grammar/actions/BnfRunJFlexAction.java:254-311`**

| Resource | URL/Info |
|---|---|
| JFlex Documentation | https://jflex.de/manual.html |
| JFlex Jar (Grammar-Kit) | `https://cache-redirector.jetbrains.com/.../jflex-1.9.2.jar` |
| JFlex Skeleton | `idea-flex.skeleton` (extracted from JFlex jar) |

## 5. Build Tool Resources

**Source: `build.gradle.kts`, `gradle.properties`**

| Resource | URL |
|---|---|
| Gradle | https://gradle.org/ |
| IntelliJ Platform Gradle Plugin | https://plugins.jetbrains.com/docs/intellij/tools-gradle-intellij-plugin.html |
| Gradle Changelog Plugin | https://github.com/JetBrains/gradle-changelog-plugin |

## 6. Version Information

**Source: `gradle.properties:6-14`**

Current version: `2023.3-dev`
Minimum IDE: IntelliJ IDEA 2023.3 (build 233)
Platform: IntelliJ Ultimate (IU)
Java: 17
Gradle: 8.14.2

## 7. Related Parsing References

**Source: `CHANGELOG.md:298, 304`**

- Pratt parsing: http://javascript.crockford.com/tdop/tdop.html (referenced in CHANGELOG)
- Expression parsing sample: `testData/generator/ExprParser.bnf`

## 8. Community

**Source: GitHub repository**

- Contributions via Pull Requests on GitHub
- Issues and discussions via GitHub Issues
- Author: Greg Shrago (gregsh), JetBrains
