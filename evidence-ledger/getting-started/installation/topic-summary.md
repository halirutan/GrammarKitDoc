# Topic Summary: Installation and Setup

## Documentation Outline Reference
Section 1.2: Installation and Setup
Source: info/documentation-outline.md

## Learning Objectives
Based on outline and evidence:
- Understand how to install Grammar-Kit plugin via IDE marketplace
- Learn to verify successful installation with editor features
- Master creating a new language plugin project with proper structure
- Create and test a minimal working grammar file

## Prerequisites
- IntelliJ IDEA 2023.3 or later installed
- Java 17+ runtime environment
- Basic familiarity with IntelliJ IDEA interface
- Understanding of plugin development concepts (helpful but not required)

## Content Structure
Following documentation outline:

1. **Installing the GrammarKit plugin** - Supported by all evidence files
   - Via IDE plugin marketplace (primary method)
   - Version requirements (Java 17+ for recent versions)
   - Verifying installation through editor features

2. **Project setup** - Supported by examples.md and code-evidence.md
   - Creating a new language plugin project
   - Directory structure recommendations
   - Essential dependencies

3. **First grammar file** - Supported by examples.md
   - Only a minimal example!
   - Creating a `.bnf` file
   - Basic grammar structure
   - Editor features overview

## Evidence Mapping
- "Via IDE plugin marketplace" → Supported by references.md (installation methods)
- "Version requirements" → Supported by code-evidence.md (Java 17+, platform 2023.3+)
- "Verifying installation" → Supported by examples.md (verify installation example)
- "Creating a new language plugin project" → Supported by examples.md (project structure)
- "Directory structure recommendations" → Supported by examples.md (standard layout)
- "Essential dependencies" → Supported by examples.md (plugin.xml, build.gradle)
- "Creating a .bnf file" → Supported by code-evidence.md (file extension info)
- "Basic grammar structure" → Supported by examples.md (minimal grammar)
- "Editor features overview" → Supported by code-evidence.md (shortcuts list)

## Key Takeaways
- Grammar-Kit requires Java 17+ and IntelliJ IDEA 2023.3+
- Installation is straightforward via plugin marketplace (ID: org.jetbrains.idea.grammar)
- Project structure should separate grammars from generated code
- Minimal grammar file demonstrates successful installation
- Editor provides immediate feedback with syntax highlighting and shortcuts

## Documentation Notes
- Focus on getting users to a working state quickly
- Include screenshot placeholders for plugin installation and project structure
- Emphasize verification steps after each installation phase
- Keep examples minimal per outline requirement
- Address common setup errors found in anti-patterns
- Provide clear next steps to Quick Start Tutorial (1.3)

## Writing Guidance for Drafter

### Task-Oriented Flow
1. Start with plugin installation via marketplace
2. Show how to verify installation worked
3. Guide through project creation step-by-step
4. End with minimal working grammar that users can test

### Progressive Disclosure
- Start with simplest installation method (marketplace)
- Mention manual/Gradle methods only as alternatives
- Keep grammar example absolutely minimal (3-4 lines)
- Save complex features for later sections

### Visual Elements Needed
- Screenshot: Plugin marketplace search for "Grammar-Kit"
- Screenshot: Installed plugin in settings
- Diagram: Recommended project structure
- Screenshot: Editor with syntax highlighting on .bnf file

### Common Pitfalls to Address
- Missing .bnf extension (files won't be recognized)
- Wrong project structure (grammars in src folder)
- Version incompatibility (old IDEA versions)
- Not testing installation before proceeding

### Success Criteria
Users should be able to:
1. Install Grammar-Kit successfully
2. Create a new project with correct structure
3. Write and save a minimal .bnf file
4. See syntax highlighting and use basic shortcuts
5. Feel confident to proceed to Quick Start Tutorial