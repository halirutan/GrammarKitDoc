# Topic Summary: What is Grammar-Kit?

## Documentation Outline Reference
Section 1.1: What is Grammar-Kit?
Source: info/documentation-outline.md

## Learning Objectives
After reading this introduction, readers will:
- Understand Grammar-Kit as a tool that transforms grammar definitions into parser code
- Know the primary use cases for Grammar-Kit in IntelliJ plugin development
- Recognize how Grammar-Kit fits into the IntelliJ Platform ecosystem
- Understand the basic workflow: write grammar rules, generate parser code
- Know where to continue their learning path

## Prerequisites
- Basic familiarity with IntelliJ IDEA
- General programming experience
- Interest in language support or parsing

## Content Structure
Following documentation outline with evidence support:

### 1. **BNF-to-Parser Transformation Tool**
   - Grammar-Kit is an IntelliJ IDEA plugin for grammar development
   - Core function: transforms BNF grammar definitions into working parsers
   - Generates lexers and PSI implementations automatically
   - Eliminates need for hand-written parsing code
   - Evidence: code-evidence.md lines 6-11

### 2. **Target Use Cases**
   - Building language support for IntelliJ-based IDEs
   - Adding syntax highlighting and code completion
   - Creating parsers for programming languages
   - Supporting configuration formats (JSON, YAML)
   - Developing domain-specific languages (DSLs)
   - Evidence: code-evidence.md lines 14-31, examples include Rust, Erlang, Elixir plugins

### 3. **Key Development Features**
   - Live Preview for real-time grammar testing
   - Interactive grammar development workflow
   - Automatic expression parsing with operator precedence
   - Advanced error recovery mechanisms
   - Seamless IntelliJ Platform integration
   - Evidence: code-evidence.md lines 34-50

### 4. **Real-World Applications**
   - Language plugins: Examples from code-evidence.md lines 15-17
   - Configuration parsers: JSON example at testData/livePreview/Json.bnf
   - DSL implementations: Business rules, query languages, templates
   - Evidence: code-evidence.md lines 20-30, 59-62

### 5. **Development Workflow**
   - Write grammar rules in BNF format
   - Test with Live Preview
   - Generate parser code
   - Integrate with IntelliJ Platform
   - Evidence: code-evidence.md lines 34-50

### 6. **Platform Integration**
   - Part of IntelliJ Platform since version 12.1
   - Works with all JetBrains IDEs
   - Standard plugin architecture
   - Evidence: code-evidence.md lines 52-56

## Evidence Mapping
- BNF transformation → code-evidence.md lines 6-11
- Use cases → code-evidence.md lines 14-31
- Development features → code-evidence.md lines 34-50
- Integration details → code-evidence.md lines 52-56
- Example locations → code-evidence.md lines 59-62

## Key Takeaways
- Grammar-Kit transforms BNF grammars into Java parser code
- Primary use is building language support for IntelliJ IDEs
- Live Preview enables interactive grammar development
- Suitable for languages, DSLs, and configuration formats

## Documentation Notes
- Focus on the transformation concept (BNF → parser)
- Emphasize practical use cases
- Show the development workflow
- Keep technical details minimal for this introduction
- Direct readers to installation as the next step