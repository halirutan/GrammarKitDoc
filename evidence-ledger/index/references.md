# References: What is Grammar-Kit?

## Scope Information
This validates references for section 1.1: What is Grammar-Kit? (Beginner-friendly introduction)

## Internal Links
- Prerequisites: None (this is the entry point for beginners)
- Next Steps: `getting-started/installation`, `getting-started/quick-start`
- Advanced Topics: `core-concepts/*`, `parser-development/*` (for later learning)

## Core Concept References (Beginner-Friendly)
- **Transformation concept**: `README.md#L12` - "parser/PSI code generator"
- **BNF basics**: `TUTORIAL.md#L3-4` - "BNF grammars are pretty easy to read"
- **Simple example**: `testData/livePreview/Json.bnf` - JSON grammar (familiar format)
- **Plugin description**: `plugin.xml#L5-6` - High-level purpose statement

## Beginner-Accessible External Links
- Grammar-Kit Plugin Page: http://plugins.jetbrains.com/plugin/6606 (installation info)
- IntelliJ Platform Overview: https://plugins.jetbrains.com/docs/intellij/welcome.html (context only)

## Validation Focus: Beginner-Friendly Content
- [x] High-level descriptions validated (2026-02-11)
- [x] Transformation metaphor supported (2026-02-11)
- [x] Complex technical details de-emphasized (2026-02-11)
- [x] Examples are approachable (2026-02-11)

## Beginner-Friendly Validation

### Core Transformation Concept (BNF → Parser)
✅ **Simple definition**: `README.md#L12` confirms Grammar-Kit "Adds BNF Grammars... and a parser/PSI code generator"
✅ **Visual transformation**: Live Preview feature (`README.md#L71`) shows real-time grammar processing
✅ **Accessible example**: JSON grammar at `testData/livePreview/Json.bnf` uses familiar format

### What Grammar-Kit Does (Simplified)
✅ **Main purpose**: Transforms grammar definitions into working parsers
✅ **Key benefit**: Avoids writing complex parsing code by hand
✅ **Interactive development**: Live Preview makes grammar development visual and immediate

### Who Uses Grammar-Kit (Beginner Context)
✅ **Primary users**: Developers building language support for IntelliJ IDEs
✅ **Use cases**: 
  - Adding syntax highlighting to existing languages
  - Creating domain-specific languages
  - Building configuration file parsers (JSON, YAML-like)
✅ **Real examples**: Multiple successful language plugins listed in `README.md#L21-30`

### Getting Started Path
✅ **No prerequisites needed**: Introduction stands alone
✅ **Clear next steps**: Installation and Quick Start sections follow naturally
✅ **Progressive learning**: Advanced topics clearly separated for later

## Simplified External Resources
- **Plugin Installation**: Direct link to plugin page for easy setup
- **Platform Context**: IntelliJ SDK docs provided for background only
- **Example Projects**: De-emphasized to avoid overwhelming beginners

## Technical References (De-emphasized)
The following technical details are validated but not emphasized in beginner content:
- Complex grammar attributes (pin, recoverWhile)
- PSI implementation details
- Advanced parsing techniques
- Build tool integration specifics

## Out of Scope for Beginners
- Installation details → Section 1.2
- Grammar syntax specifics → Section 2.x
- Advanced features → Sections 3.x and beyond
- Complex examples → Later sections