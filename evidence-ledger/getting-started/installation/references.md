# References: Installation and Setup

## Scope Information
This validates references for section 1.2: Installation and Setup

## Internal Links
- Prerequisites: None (first setup section)
- Related: `getting-started/quick-start` (Section 1.3)
- Advanced: `parser-development/*` (Section 3.x)

## Code References
- Plugin descriptor: `resources/META-INF/plugin.xml`
- Plugin ID: `org.jetbrains.idea.grammar`
- File type registration: `BnfFileType.java`
- Build configuration: `gradle.properties#L9` (pluginSinceBuild = 233)
- Java version requirement: `gradle.properties#L33` (javaVersion=17)
- Version info: `gradle.properties#L6` (pluginVersion = 2023.3-dev)

## External Links
- Plugin Marketplace: https://plugins.jetbrains.com/plugin/6606-grammar-kit
- IntelliJ Platform SDK: https://plugins.jetbrains.com/docs/intellij/welcome.html
- Custom Language Support Tutorial: https://plugins.jetbrains.com/docs/intellij/custom-language-support-tutorial.html
- Gradle Grammar-Kit Plugin: https://github.com/JetBrains/gradle-grammar-kit-plugin
- Grammar-Kit Repository: https://github.com/JetBrains/Grammar-Kit
- Latest Dev Build: https://teamcity.jetbrains.com/guestAuth/app/rest/builds/buildType:IntellijIdeaPlugins_GrammarKit_Build,status:SUCCESS/artifacts/content/GrammarKit*.zip

## Validation
- [x] Code refs valid (2026-02-04)
- [x] Plugin.xml verified (2026-02-04)
- [x] Version requirements confirmed (2026-02-04)
- [x] File paths accurate (2026-02-04)
- [x] External links active (2026-02-04)

## Errors Found
None - all references validated successfully

## Version Compatibility
- **Java Requirement**: Java 17+ (since Grammar-Kit 2022.3)
- **Platform Version**: IntelliJ IDEA 2023.3+ (build 233+)
- **Current Plugin Version**: 2023.3-dev
- **Dependencies**: 
  - com.intellij.modules.lang (required)
  - com.intellij.java (optional)
  - com.intellij.diagram (optional)
  - com.intellij.copyright (optional)

## Installation Methods
1. **IDE Plugin Manager**: 
   - Settings → Plugins → Marketplace → Search "Grammar-Kit"
   - Plugin ID: `org.jetbrains.idea.grammar`

2. **Manual Installation**:
   - Download from TeamCity dev builds
   - Install via Settings → Plugins → Install from disk

3. **Gradle Build Integration**:
   - Plugin: `org.jetbrains.grammarkit` version "2022.3.2"
   - Repository: Gradle Plugin Portal

## Essential Setup Resources
- File extension: `.bnf`
- Language name: BNF
- Parser generation shortcut: Ctrl+Shift+G (Cmd+Shift+G on Mac)
- Live Preview shortcut: Ctrl+Alt+P (Cmd+Alt+P on Mac)
- Structure view: Ctrl+F12 (Cmd+F12 on Mac)

## Out of Scope References
- Grammar syntax details → Validated in Section 2.1
- Attribute system documentation → Validated in Section 2.2
- Parser generation specifics → Validated in Section 3.x
- Build integration details → Validated in Section 6.x
- Advanced IDE features → Validated in Section 5.x
- Troubleshooting guides → Validated in Section 8.x