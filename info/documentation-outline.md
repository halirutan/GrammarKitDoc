# GrammarKit Documentation Outline

## Overview
A comprehensive guide for creating language parsers and PSI (Program Structure Interface) implementations using GrammarKit, the IntelliJ IDEA plugin for BNF grammar development.

## Target Audiences
1. **IntelliJ Plugin Developers** - Creating custom language support with IDE features
2. **Build/CI Users** - Automating parser generation in Gradle builds
3. **Grammar Maintainers** - Evolving and optimizing existing grammars

---

## 1. Getting Started

### [x] 1.1 Introduction to GrammarKit
**File:** `docs/getting-started/introduction.md`
- **What is GrammarKit?**
  - Overview of BNF grammar support and parser generation
  - Key features and capabilities
  - Relationship to IntelliJ Platform language support
- **When to use GrammarKit**
  - Custom language plugin development
  - DSL (Domain Specific Language) support
  - File format parsers
- **Prerequisites**
  - IntelliJ IDEA basics
  - Java development knowledge
  - Understanding of parsing concepts (optional but helpful)

### [x] 1.2 Installation and Setup
**File:** `docs/getting-started/installation.md`
- **Installing the GrammarKit plugin**
  - Via IDE plugin marketplace
  - Version requirements (Java 17+ for recent versions)
  - Verifying installation
- **Project setup**
  - Creating a new language plugin project
  - Directory structure recommendations
  - Essential dependencies
- **First grammar file**
  - Only a minimal example!
  - Creating a `.bnf` file
  - Basic grammar structure
  - Editor features overview
  
**Examples needed:**
- Minimal working grammar file
- Basic project structure

**Visual aids:**
- Screenshot of plugin installation
- Project structure diagram

### [ ] 1.3 Quick Start Tutorial
**File:** `docs/getting-started/quick-start.md`
- **Your first grammar**
  - Simple expression grammar example
  - Understanding rules and tokens
  - Using Live Preview
- **Generating parser code**
  - Running the generator (Ctrl+Shift+G)
  - Understanding generated files
  - Integrating with IntelliJ Platform
- **Testing your parser**
  - Creating test files
  - Using PSI Viewer
  - Basic parsing tests

**Examples needed:**
- Complete arithmetic expression grammar
- Sample test file
- Generated code walkthrough

---

## 2. Core Concepts

### [x] 2.1 BNF Grammar Syntax
**File:** `docs/core-concepts/bnf-syntax.md`
- **Grammar structure**
  - Header attributes
  - Token definitions
  - Grammar rules
  - Rule modifiers
- **Rule syntax**
  - Sequences and choices
  - Quantifiers (?, +, *)
  - Grouping with parentheses
  - Predicates (& and !)
- **Token types**
  - Literal tokens (quoted strings)
  - Named tokens
  - Regexp tokens
  - Token precedence in Live Preview

**Examples needed:**
- Comprehensive syntax examples
- Token definition patterns
- Common rule patterns

### [x] 2.2 Attributes System
**File:** `docs/core-concepts/attributes.md`
- **Global attributes**
  - Parser configuration (parserClass, parserPackage)
  - PSI configuration (psiPackage, psiClassPrefix)
  - Generation options
- **Rule attributes**
  - pin - Committing to parse branches
  - recoverWhile - Error recovery
  - extends/implements - PSI hierarchy
  - methods - Custom PSI accessors
- **Pattern-based attributes**
  - Applying attributes to multiple rules
  - Name pattern matching
  - Inheritance of attributes

**Examples needed:**
- Complete attribute reference with use cases
- Pattern matching examples
- Attribute inheritance demonstration

### [x] 2.3 Live Preview
**File:** `docs/core-concepts/live-preview.md`
- **Using Live Preview effectively**
  - Opening preview (Ctrl+Alt+P)
  - Understanding the preview lexer
  - Structure view integration
  - Evaluator highlighting (Ctrl+Alt+F7)
- **Preview limitations**
  - Simplified tokenization
  - Whitespace handling differences
  - When to trust preview vs. runtime
- **Rapid iteration workflow**
  - Edit → Preview → Adjust cycle
  - Testing error recovery
  - Validating rule structure

**Examples needed:**
- Preview workflow demonstration
- Common preview vs. runtime differences

**Visual aids:**
- Live Preview interface screenshot
- Structure view examples

---

## 3. Parser Development

### [x] 3.1 Designing Grammar Rules
**File:** `docs/parser-development/grammar-design.md`
- **Grammar organization**
  - Top-down design approach
  - Identifying language constructs
  - Rule naming conventions
  - Private vs. public rules
- **Common patterns**
  - Lists and separators
  - Optional elements
  - Nested structures
  - Statement vs. expression distinction
- **Avoiding common pitfalls**
  - Left recursion issues
  - Ambiguous grammars
  - Token conflicts
  - Performance considerations

**Examples needed:**
- Well-structured grammar template
- Common pattern library
- Before/after refactoring examples

### [ ] 3.2 Expression Parsing
**File:** `docs/parser-development/expression-parsing.md`
- **Precedence and associativity**
  - Traditional precedence layers
  - Using priority rules
  - Left vs. right associativity
  - Operator precedence table
- **Expression optimization**
  - Avoiding deep PSI trees
  - Using extends for flat structure
  - The expression parsing pattern
  - Binary and n-ary operations
- **Advanced techniques**
  - Mixing prefix/postfix/infix
  - Ternary operators
  - Expression with type constraints

**Examples needed:**
- Complete expression grammar
- Precedence table implementation
- PSI tree comparison (deep vs. flat)

### [ ] 3.3 Error Recovery
**File:** `docs/parser-development/error-recovery.md`
- **Pin attribute**
  - How pinning works
  - Choosing pin points
  - Pin patterns for sub-expressions
  - Common pin strategies
- **RecoverWhile predicates**
  - Writing recovery predicates
  - Using #auto recovery
  - Recovery boundaries
  - Combining pin and recoverWhile
- **Testing recovery**
  - Creating broken input samples
  - Validating PSI structure
  - Ensuring IDE features work

**Examples needed:**
- Statement parsing with recovery
- List parsing with recovery
- Complex recovery scenarios

---

## 4. Code Generation

### [ ] 4.1 Parser Generation
**File:** `docs/code-generation/parser-generation.md`
- **Generator configuration**
  - Understanding generate attributes
  - Output directory setup
  - Package structure
  - Class naming conventions
- **Generated components**
  - Parser class structure
  - Element types (tokens and rules)
  - PSI interfaces and implementations
  - Visitor pattern support
- **Generation options**
  - Java version targeting
  - Name style options (CamelCase, snake_case)
  - Debugging generated code
  - Performance optimizations

**Examples needed:**
- Complete generation configuration
- Generated code walkthrough
- Customization examples

### [ ] 4.2 Lexer Integration
**File:** `docs/code-generation/lexer-integration.md`
- **Creating JFlex lexers**
  - JFlex file structure
  - Token type mapping
  - State management
  - Unicode support
- **Lexer generation**
  - From BNF tokens (bootstrap)
  - Manual lexer creation
  - Running JFlex generator
  - Lexer testing
- **Advanced lexing**
  - Context-sensitive tokens
  - Nested comments/strings
  - Error tokens
  - Performance optimization

**Examples needed:**
- Complete JFlex lexer
- State machine examples
- Token type mapping

### [ ] 4.3 PSI Customization
**File:** `docs/code-generation/psi-customization.md`
- **PSI hierarchy design**
  - Using extends attribute
  - Interface implementation
  - Mixin classes
  - Fake rules for structure
- **Custom methods**
  - Methods attribute syntax
  - Path-based accessors (/expr[0])
  - Utility method integration
  - Name and reference support
- **Stub support**
  - When to use stubs
  - Stub implementation
  - Index integration
  - Performance benefits

**Examples needed:**
- PSI hierarchy diagram
- Custom method implementations
- Stub-based PSI example

---

## 5. IDE Integration

### [ ] 5.1 Parser Definition
**File:** `docs/ide-integration/parser-definition.md`
- **Implementing ParserDefinition**
  - Required methods
  - Token type sets
  - Creating lexer and parser
  - File and element creation
- **Registration**
  - plugin.xml configuration
  - Extension points
  - File type association
  - Language registration
- **Testing integration**
  - Using PSI Viewer
  - Verifying token streams
  - Debugging parse trees

**Examples needed:**
- Complete ParserDefinition
- plugin.xml configuration
- Integration checklist

### [ ] 5.2 Language Features
**File:** `docs/ide-integration/language-features.md`
- **Basic features**
  - Syntax highlighting
  - Brace matching
  - Code folding
  - Structure view
- **Navigation**
  - Go to declaration
  - Find usages
  - File structure popup
  - Breadcrumbs
- **Refactoring**
  - Rename support
  - Safe delete
  - Move refactoring
  - Extract variable

**Examples needed:**
- Feature implementation guides
- PSI patterns for references
- Refactoring support code

### [ ] 5.3 Testing
**File:** `docs/ide-integration/testing.md`
- **Parsing tests**
  - Test framework setup
  - Expected PSI structure
  - Regression testing
  - Performance testing
- **Integration tests**
  - Feature testing
  - Editor behavior
  - Refactoring tests
  - Inspection tests
- **Debugging techniques**
  - Using PSI Viewer
  - Parser tracing
  - Performance profiling
  - Memory analysis

**Examples needed:**
- Test suite structure
- Parsing test examples
- Debugging scenarios

---

## 6. Build Integration

### [ ] 6.1 Gradle Plugin Setup
**File:** `docs/build-integration/gradle-setup.md`
- **Plugin configuration**
  - Adding the plugin
  - Version compatibility
  - Task configuration
  - Source set setup
- **Generation tasks**
  - generateParser task
  - generateLexer task
  - Task dependencies
  - Incremental builds
- **CI/CD integration**
  - Deterministic builds
  - Caching strategies
  - Multi-module projects
  - Version control practices

**Examples needed:**
- Complete build.gradle
- Multi-module setup
- CI configuration

### [ ] 6.2 Gradle vs IDE Generation
**File:** `docs/build-integration/gradle-vs-ide.md`
- **Feature comparison**
  - Two-pass generation (IDE only)
  - Method mixins support
  - Generation speed
  - Debugging capabilities
- **Choosing an approach**
  - Development workflow
  - Team considerations
  - Build reproducibility
  - Hybrid approaches
- **Migration strategies**
  - From IDE to Gradle
  - Handling limitations
  - Workarounds

**Examples needed:**
- Comparison table
- Migration guide
- Workaround patterns

---

## 7. Advanced Topics

### [ ] 7.1 External Rules
**File:** `docs/advanced-topics/external-rules.md`
- **When to use external rules**
  - Complex parsing logic
  - Performance optimization
  - Reusing existing parsers
  - Custom token matching
- **Implementation**
  - External rule declaration
  - Parser utility methods
  - Integration patterns
  - Testing external rules
- **Common patterns**
  - Indentation-based parsing
  - Context-sensitive parsing
  - Lookahead optimization

**Examples needed:**
- External rule implementations
- Parser utility class
- Integration patterns

### [ ] 7.2 Grammar Composition
**File:** `docs/advanced-topics/grammar-composition.md`
- **Modular grammar design**
  - Splitting large grammars
  - Shared token definitions
  - Rule organization
  - Namespace management
- **Reusability patterns**
  - Common rule libraries
  - Grammar inheritance
  - Mixin strategies
  - Version management
- **Multi-language support**
  - Embedded languages
  - Language injection
  - Shared PSI elements
  - Cross-language references

**Examples needed:**
- Modular grammar structure
- Reusable components
- Multi-language setup

### [ ] 7.3 Performance Optimization
**File:** `docs/advanced-topics/performance.md`
- **Parser performance**
  - First-check optimization
  - Token prediction
  - Lookahead tuning
  - Memory efficiency
- **PSI optimization**
  - Lazy evaluation
  - Stub indices
  - Caching strategies
  - Tree structure
- **Profiling and analysis**
  - Performance metrics
  - Bottleneck identification
  - Optimization techniques
  - Benchmarking

**Examples needed:**
- Performance patterns
- Optimization techniques
- Benchmarking setup

---

## 8. Troubleshooting

### [ ] 8.1 Common Issues
**File:** `docs/troubleshooting/common-issues.md`
- **Generation problems**
  - Missing generated files
  - Compilation errors
  - Package mismatches
  - Stale output
- **Parser issues**
  - Left recursion errors
  - Ambiguous grammars
  - Token conflicts
  - Performance problems
- **Integration issues**
  - PSI not created
  - Features not working
  - Plugin conflicts
  - Version incompatibilities

**Examples needed:**
- Error messages and solutions
- Diagnostic techniques
- Common fixes

### [ ] 8.2 Debugging Techniques
**File:** `docs/troubleshooting/debugging.md`
- **Grammar debugging**
  - Using Live Preview
  - Rule tracing
  - Token analysis
  - Structure validation
- **Runtime debugging**
  - Parser breakpoints
  - PSI inspection
  - Token stream analysis
  - Performance profiling
- **Tool usage**
  - PSI Viewer
  - Parser debugger
  - Profiler integration
  - Log analysis

**Examples needed:**
- Debugging workflows
- Tool configurations
- Analysis techniques

### [ ] 8.3 Migration Guide
**File:** `docs/troubleshooting/migration.md`
- **Version upgrades**
  - Grammar-Kit versions
  - IntelliJ Platform versions
  - Breaking changes
  - Deprecation handling
- **Grammar evolution**
  - Refactoring strategies
  - Backward compatibility
  - Migration testing
  - Rollback planning
- **Best practices**
  - Version control
  - Documentation
  - Testing strategies
  - Team coordination

**Examples needed:**
- Migration checklists
- Version compatibility matrix
- Refactoring patterns

---

## 9. Reference

### [ ] 9.1 Attribute Reference
**File:** `docs/reference/attributes.md`
- **Complete attribute list**
  - Global attributes
  - Rule attributes  
  - Pattern attributes
  - Deprecated attributes
- **Attribute details**
  - Syntax and values
  - Scope and inheritance
  - Examples and use cases
  - Common combinations

**Structure:** Alphabetical listing with:
- Syntax
- Description
- Valid values
- Scope (global/rule)
- Examples
- Related attributes

### [ ] 9.2 Grammar Syntax Reference
**File:** `docs/reference/grammar-syntax.md`
- **EBNF notation**
  - Complete syntax diagram
  - Operator precedence
  - Special constructs
  - Meta-rules
- **Built-in functions**
  - Predicates
  - External calls
  - Hooks
  - Utilities

### [ ] 9.3 Keyboard Shortcuts
**File:** `docs/reference/shortcuts.md`
- **Editor shortcuts**
  - Navigation
  - Generation
  - Refactoring
  - Preview
- **Platform differences**
  - Windows/Linux
  - macOS
  - Customization

### [ ] 9.4 Glossary
**File:** `docs/reference/glossary.md`
- **Terms and concepts**
  - Parser terminology
  - Grammar-Kit specific terms
  - IntelliJ Platform terms
  - Common abbreviations

---

## Appendices

### [ ] A. Example Grammars
**File:** `docs/appendices/examples.md`
- **Complete examples**
  - JSON parser
  - Expression calculator  
  - Simple scripting language
  - Configuration file parser
- **Code organization**
  - Project structure
  - Build configuration
  - Test suites
  - Documentation

### [ ] B. Resources
**File:** `docs/appendices/resources.md`
- **Official resources**
  - GitHub repository
  - Issue tracker
  - Release notes
  - Community forums
- **Learning resources**
  - Video tutorials
  - Blog posts
  - Sample projects
  - Related tools
- **IntelliJ Platform**
  - SDK documentation
  - API references
  - Plugin development
  - Community resources

### [ ] C. FAQ
**File:** `docs/appendices/faq.md`
- **Getting started questions**
- **Common problems**
- **Best practices**
- **Performance tips**
- **Integration questions**

---

## Documentation Notes

### Visual Elements Needed
1. **Screenshots**
   - IDE with Grammar-Kit features
   - Live Preview interface
   - PSI Viewer
   - Project structure
   - Generation output

2. **Diagrams**
   - Grammar structure flow
   - PSI hierarchy examples
   - Parser generation process
   - Error recovery illustration
   - Expression precedence trees

3. **Code Examples**
   - Should be complete and runnable
   - Include both simple and complex cases
   - Show before/after for optimizations
   - Include anti-patterns to avoid

### Writing Guidelines
1. **Progressive disclosure**
   - Start with simple examples
   - Build complexity gradually
   - Reference advanced topics
   - Provide clear learning path

2. **Task-oriented approach**
   - Focus on what users want to do
   - Provide step-by-step instructions
   - Include verification steps
   - Offer troubleshooting tips

3. **Cross-references**
   - Link related topics
   - Reference official documentation
   - Point to examples
   - Maintain topic cohesion

### Target Platforms
- **ReadTheDocs compatibility**
- **GitHub Pages ready**
- **IDE documentation viewer**
- **PDF generation support**