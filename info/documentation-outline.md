# Grammar-Kit Documentation Outline

## Overview
A comprehensive guide for creating language parsers and PSI (Program Structure Interface) implementations using Grammar-Kit, the IntelliJ IDEA plugin for BNF grammar development.

## Target Audiences
1. **IntelliJ Plugin Developers** - Creating custom language support with IDE features
2. **Build/CI Users** - Automating parser generation in Gradle builds
3. **Grammar Maintainers** - Evolving and optimizing existing grammars

---

## 1. Introduction to Grammar-Kit (Home Page)

### 1.1 What is Grammar-Kit?
**File:** `docs/index.md`
- **Overview of BNF grammar support and parser generation**
  - IntelliJ IDEA plugin for language development
  - BNF Grammars and JFlex file editing support
  - Parser/PSI code generation capabilities
  - Live Preview for rapid development
- **Key features and capabilities**
  - Syntax highlighting and code completion for BNF
  - Real-time grammar validation
  - Integrated parser testing
  - PSI hierarchy generation
  - Error recovery mechanisms
- **Relationship to IntelliJ Platform language support**
  - Integration with Language API
  - PSI (Program Structure Interface) foundation
  - Custom language plugin architecture
- **When to use Grammar-Kit**
  - Custom language plugin development
  - DSL (Domain Specific Language) support
  - File format parsers
  - Configuration file processors
  - Scripting language implementations

### 1.2 Installation and Setup
**File:** `docs/installation.md`
- **Prerequisites**
  - IntelliJ IDEA basics
  - Java development knowledge (Java 17+ for recent versions)
  - Understanding of parsing concepts (optional but helpful)
- **Installing the Grammar-Kit plugin**
  - Via IDE plugin marketplace
  - Version compatibility matrix
  - Offline installation options
  - Verifying installation
- **Project setup**
  - Creating a new language plugin project
  - Directory structure recommendations
  - Essential dependencies
  - Recommended project templates
- **Development environment**
  - Configuring SDK
  - Setting up source folders
  - Version control considerations
  - Team development setup
- **First grammar file**
  - Creating a `.bnf` file
  - Basic grammar structure
  - Editor features overview
  - Initial validation

**Examples needed:**
- Minimal working grammar file
- Basic project structure
- plugin.xml configuration

**Visual aids:**
- Screenshot of plugin installation
- Project structure diagram
- IDE setup walkthrough

### 1.3 Quick Start Tutorial
**File:** `docs/quick-start.md`
- **Your first grammar**
  - Simple expression grammar example
  - Understanding rules and tokens
  - Using Live Preview
  - Common beginner patterns
- **Generating parser code**
  - Running the generator (Ctrl+Shift+G)
  - Understanding generated files
  - Package structure
  - Integrating with IntelliJ Platform
- **Creating a language plugin**
  - Language and file type registration
  - Basic ParserDefinition
  - Lexer integration
  - Simple syntax highlighting
- **Testing your parser**
  - Creating test files
  - Using PSI Viewer
  - Basic parsing tests
  - Validation strategies

**Examples needed:**
- Complete arithmetic expression grammar
- Sample test files
- Generated code walkthrough
- Working language plugin

---

## 2. Grammar Development

### 2.1 BNF Grammar Syntax
**File:** `docs/grammar-development/grammar-syntax.md`
- **Grammar file structure**
  - File header and metadata
  - Grammar attributes section
  - Token definitions
  - Grammar rules
  - Comments and documentation
- **Token definitions**
  - Literal tokens (quoted strings)
  - Named tokens
  - Regexp tokens
  - Token precedence and conflicts
  - Whitespace and comment handling
- **Rule syntax fundamentals**
  - Basic rule structure
  - Sequences and choices (|)
  - Quantifiers (?, +, *)
  - Grouping with parentheses
  - Rule references
- **Advanced constructs**
  - Predicates (& and !)
  - External rules (<<external>>)
  - Private rules (private prefix)
  - Meta rules and parameters
  - Upper/lower rule variants
- **EBNF extensions**
  - Grammar-Kit specific syntax
  - Shortcuts and sugar syntax
  - Built-in token types
  - Special symbols

**Examples needed:**
- Comprehensive syntax examples
- Token definition patterns
- Common rule patterns
- Grammar organization templates

### 2.2 Designing Grammar Rules
**File:** `docs/grammar-development/grammar-design.md`
- **Grammar architecture principles**
  - Top-down design approach
  - Identifying language constructs
  - Separation of concerns
  - Modularity and reusability
- **Rule organization**
  - Naming conventions
  - Private vs. public rules
  - Rule grouping strategies
  - Documentation practices
- **Common patterns**
  - Lists and separators
  - Optional elements
  - Nested structures
  - Statement vs. expression distinction
  - Block structures
  - Declaration patterns
- **Best practices**
  - Rule granularity
  - Token vs. rule decisions
  - Performance considerations
  - Maintainability patterns
- **Avoiding common pitfalls**
  - Left recursion issues
  - Ambiguous grammars
  - Token conflicts
  - Backtracking problems
  - Grammar complexity

**Examples needed:**
- Well-structured grammar template
- Common pattern library
- Before/after refactoring examples
- Anti-pattern catalog

### 2.3 Expression Parsing
**File:** `docs/grammar-development/expression-parsing.md`
- **Expression parsing fundamentals**
  - Expression vs. statement parsing
  - Operator types (prefix, infix, postfix)
  - Precedence and associativity concepts
  - Expression grammar patterns
- **Implementing precedence**
  - Traditional precedence climbing
  - Layer-based approach
  - Priority attributes
  - Operator precedence tables
- **Associativity control**
  - Left associative operators
  - Right associative operators
  - Non-associative operators
  - Mixed associativity
- **Expression optimization**
  - Avoiding deep PSI trees
  - Using extends for flat structure
  - The expression parsing idiom
  - Binary and n-ary operations
- **Complex expressions**
  - Mixing operator types
  - Ternary operators
  - Function calls and indexing
  - Type constraints
  - Contextual expressions

**Examples needed:**
- Complete expression grammar
- Precedence table implementation
- PSI tree comparison (deep vs. flat)
- Real-world expression parsers

### 2.4 Error Recovery
**File:** `docs/grammar-development/error-recovery.md`
- **Error recovery fundamentals**
  - Why error recovery matters
  - Recovery strategies overview
  - IDE user experience considerations
  - Testing recovery effectiveness
- **Pin attribute mechanics**
  - How pinning works
  - Choosing pin points
  - Pin patterns for statements
  - Pin in sequences and choices
  - Common pin strategies
- **RecoverWhile predicates**
  - Writing recovery predicates
  - Token sets for recovery
  - Using #auto recovery
  - Recovery boundaries
  - Nested recovery
- **Advanced recovery patterns**
  - Combining pin and recoverWhile
  - Multi-level recovery
  - Context-aware recovery
  - Partial parsing strategies
- **Testing and validation**
  - Creating broken input samples
  - Validating PSI structure
  - Ensuring IDE features work
  - Performance impact

**Examples needed:**
- Statement parsing with recovery
- List parsing with recovery
- Complex recovery scenarios
- Test cases for broken code

### 2.5 Live Preview Workflow
**File:** `docs/grammar-development/live-preview.md`
- **Live Preview overview**
  - Purpose and capabilities
  - Opening preview (Ctrl+Alt+P)
  - Preview window layout
  - Real-time feedback
- **Understanding the preview lexer**
  - Automatic token detection
  - Whitespace handling
  - Comment detection
  - Token precedence rules
- **Preview features**
  - Structure view integration
  - Parse tree visualization
  - Error highlighting
  - First/follow set display
  - Rule reachability
- **Workflow optimization**
  - Edit → Preview → Adjust cycle
  - Testing rule changes
  - Validating error recovery
  - Performance indicators
- **Preview limitations**
  - Simplified tokenization
  - External rule handling
  - Complex lexer features
  - When to test with real parser

**Examples needed:**
- Preview workflow demonstration
- Common preview vs. runtime differences
- Debugging techniques

**Visual aids:**
- Live Preview interface screenshot
- Structure view examples
- Parse tree visualization

### 2.6 External Rules
**File:** `docs/grammar-development/external-rules.md`
- **When to use external rules**
  - Complex parsing logic
  - Performance optimization
  - Reusing existing parsers
  - Custom token matching
  - Context-sensitive parsing
- **External rule declaration**
  - Syntax and attributes
  - Method signatures
  - Return value conventions
  - Parameter passing
- **Implementation patterns**
  - Parser utility methods
  - State management
  - Error reporting
  - Token consumption
  - Lookahead techniques
- **Common use cases**
  - Indentation-based parsing
  - Complex string interpolation
  - Performance-critical sections
  - Legacy parser integration
- **Testing external rules**
  - Unit testing approaches
  - Integration with grammar tests
  - Debugging techniques
  - Performance profiling

**Examples needed:**
- External rule implementations
- Parser utility class
- Integration patterns
- Python-style indentation

### 2.7 Grammar Composition
**File:** `docs/grammar-development/grammar-composition.md`
- **Modular grammar design**
  - Splitting large grammars
  - Logical module boundaries
  - Shared token definitions
  - Rule organization strategies
- **Grammar includes**
  - Include mechanisms
  - Namespace management
  - Attribute inheritance
  - Override patterns
- **Reusability patterns**
  - Common rule libraries
  - Generic grammar components
  - Parameterized rules
  - Template grammars
- **Multi-language support**
  - Embedded languages
  - Language injection points
  - Shared PSI elements
  - Cross-language references
- **Version management**
  - Grammar evolution
  - Backward compatibility
  - Deprecation strategies
  - Migration paths

**Examples needed:**
- Modular grammar structure
- Reusable components
- Multi-language setup
- Include patterns

---

## 3. Code Generation & Customization

### 3.1 Attributes System
**File:** `docs/code-generation/attributes.md`
- **Attribute categories**
  - Global attributes overview
  - Rule-level attributes
  - Pattern-based attributes
  - Attribute inheritance rules
- **Global parser attributes**
  - parserClass - Main parser class name
  - parserPackage - Parser package location
  - parserImports - Import statements
  - parserUtilClass - Utility class reference
  - generatePsi - PSI generation control
- **Global PSI attributes**
  - psiPackage - PSI classes package
  - psiImplPackage - Implementation package
  - psiClassPrefix/Suffix - Naming patterns
  - psiImplUtilClass - PSI utilities
  - elementTypeHolderClass - Token types
- **Rule-specific attributes**
  - pin - Parse tree commitment
  - recoverWhile - Error recovery
  - extends/implements - Type hierarchy
  - methods - Custom accessors
  - mixin - Implementation mixing
  - stubClass - Stub support
  - elementType - Custom element types
  - name - Rule result naming
- **Pattern attributes**
  - Pattern syntax and wildcards
  - Attribute application order
  - Override mechanisms
  - Complex patterns
- **Advanced attributes**
  - tokens - Token generation
  - generate - Selective generation
  - elementTypeClass/Factory
  - consumeTokenMethod
  - Special-purpose attributes

**Examples needed:**
- Complete attribute reference
- Pattern matching examples
- Attribute combinations
- Real-world configurations

### 3.2 Parser Generation
**File:** `docs/code-generation/parser-generation.md`
- **Generator overview**
  - Two-pass generation process
  - Generated file structure
  - Package organization
  - Naming conventions
- **Configuration options**
  - Generation attributes
  - Output directory setup
  - Package structure control
  - Class naming patterns
- **Generated parser components**
  - Parser class structure
  - Static parse methods
  - Rule methods
  - Utility integration
  - Error handling
- **Element types system**
  - IElementType hierarchy
  - Token type constants
  - Rule element types
  - Element type holder
- **Generation customization**
  - Java version targeting
  - Code style options
  - Debug information
  - Optimization levels
  - Custom templates
- **Build integration**
  - IDE generation (Ctrl+Shift+G)
  - Command-line generation
  - Gradle plugin usage
  - CI/CD pipelines

**Examples needed:**
- Complete generation setup
- Generated code walkthrough
- Customization examples
- Build configurations

### 3.3 Lexer Integration
**File:** `docs/code-generation/lexer-integration.md`
- **Lexer options**
  - JFlex integration
  - Grammar-Kit lexer
  - Custom lexer adapter
  - Lexer selection criteria
- **JFlex development**
  - JFlex file structure
  - Lexer states
  - Token type mapping
  - Unicode support
  - Performance tuning
- **Grammar-Kit lexer**
  - Automatic generation
  - Token precedence
  - Keyword handling
  - Limitations and capabilities
- **Token type mapping**
  - IElementType creation
  - Token type constants
  - Token sets
  - Token precedence
- **Advanced lexing**
  - Context-sensitive tokens
  - Nested structures (comments/strings)
  - Template languages
  - Error tokens
  - Incremental lexing
- **Testing lexers**
  - Lexer test framework
  - Token stream validation
  - Performance testing
  - Edge cases

**Examples needed:**
- Complete JFlex lexer
- Token type mapping
- State machine patterns
- Test suites

### 3.4 PSI Customization
**File:** `docs/code-generation/psi-customization.md`
- **PSI architecture**
  - PSI tree structure
  - Element interfaces
  - Implementation classes
  - Visitor pattern
  - Stub-based PSI
- **Type hierarchy design**
  - Using extends attribute
  - Interface implementation
  - Common base types
  - Marker interfaces
- **Mixin classes**
  - Mixin attribute usage
  - Implementation patterns
  - Constructor requirements
  - Method delegation
- **Custom methods**
  - methods attribute syntax
  - Path-based accessors (/expr[0])
  - Collection accessors
  - Type-safe methods
  - Utility method integration
- **Fake rules**
  - Purpose and patterns
  - Interface generation
  - Shared method sets
  - Type hierarchy control
- **Advanced PSI features**
  - Reference implementation
  - Name providers
  - Stub indices
  - Smart pointers
  - Performance optimization

**Examples needed:**
- PSI hierarchy diagram
- Custom method implementations
- Mixin class patterns
- Reference providers

---

## 4. Integration

### 4.1 IDE Integration

#### 4.1.1 Parser Definition
**File:** `docs/integration/parser-definition.md`
- **ParserDefinition basics**
  - Interface requirements
  - Core responsibilities
  - Registration mechanism
  - Lifecycle management
- **Essential methods**
  - createLexer() - Lexer instantiation
  - createParser() - Parser creation
  - getFileNodeType() - File element type
  - getTokenSets() - Token categorization
  - createElement() - PSI creation
- **Token sets**
  - Comments and whitespace
  - String literals
  - Keywords
  - Operators
  - Custom categories
- **File creation**
  - createFile() implementation
  - PsiFile subclasses
  - File element types
  - Stub file creation
- **Registration and configuration**
  - plugin.xml setup
  - Language constants
  - Extension points
  - Dependencies

**Examples needed:**
- Complete ParserDefinition
- Token set definitions
- Registration configuration
- Common patterns

#### 4.1.2 Language Features
**File:** `docs/integration/language-features.md`
- **Syntax highlighting**
  - Lexer-based highlighting
  - Annotator-based highlighting
  - Color settings page
  - Token type mapping
  - Semantic highlighting
- **Code structure**
  - Structure view provider
  - File structure popup
  - Breadcrumbs support
  - Code folding
  - Block selection
- **Navigation features**
  - Go to declaration
  - Find usages
  - Search everywhere
  - Symbol navigation
  - Reference providers
- **Code completion**
  - Completion contributors
  - Pattern matching
  - Priority and sorting
  - Documentation lookup
  - Parameter hints
- **Refactoring support**
  - Rename refactoring
  - Safe delete
  - Move refactoring
  - Extract patterns
  - Inline support
- **Code analysis**
  - Inspections
  - Quickfixes
  - Annotators
  - Daemon indicators

**Examples needed:**
- Feature implementations
- Extension point usage
- PSI patterns
- Performance tips

#### 4.1.3 Testing
**File:** `docs/integration/testing.md`
- **Test framework setup**
  - Test dependencies
  - Base test classes
  - Test data organization
  - Fixtures and utilities
- **Parser testing**
  - PSI tree tests
  - Parser recovery tests
  - Lexer tests
  - Performance benchmarks
- **Feature testing**
  - Completion tests
  - Navigation tests
  - Refactoring tests
  - Highlighting tests
  - Inspection tests
- **Integration testing**
  - Multi-file scenarios
  - Project-wide features
  - Editor behavior
  - UI interaction tests
- **Debugging and troubleshooting**
  - PSI Viewer usage
  - Test debugging
  - Common test issues
  - Assertion helpers

**Examples needed:**
- Test suite structure
- Test case patterns
- Assertion examples
- Debugging workflows

### 4.2 Build Integration

#### 4.2.1 Gradle Plugin Setup
**File:** `docs/integration/gradle-setup.md`
- **Plugin installation**
  - Gradle plugin coordinates
  - Version compatibility
  - Plugin configuration
  - Repository setup
- **Basic configuration**
  - Source set configuration
  - Task dependencies
  - Output directories
  - Generation options
- **Grammar compilation**
  - generateParser task
  - Source file discovery
  - Incremental compilation
  - Error handling
- **Lexer generation**
  - generateLexer task
  - JFlex integration
  - Token mapping
  - Custom lexers
- **Advanced configuration**
  - Multi-module projects
  - Custom task configuration
  - Build caching
  - Parallel execution
- **CI/CD integration**
  - Reproducible builds
  - Build automation
  - Artifact publishing
  - Version management

**Examples needed:**
- Complete build.gradle
- Multi-module setup
- CI configurations
- Task customization

#### 4.2.2 Gradle vs IDE Generation
**File:** `docs/integration/gradle-vs-ide.md`
- **Feature comparison table**
  - Generation capabilities
  - Performance characteristics
  - Debugging support
  - Customization options
- **IDE generation benefits**
  - Two-pass generation
  - Live Preview integration
  - Immediate feedback
  - Debugging features
  - Method mixins support
- **Gradle generation benefits**
  - Build reproducibility
  - CI/CD compatibility
  - Team synchronization
  - Version control
  - Automation
- **Limitations and workarounds**
  - Gradle plugin limitations
  - Missing features
  - Common workarounds
  - Hybrid approaches
- **Choosing an approach**
  - Project requirements
  - Team considerations
  - Development workflow
  - Migration strategies
- **Best practices**
  - Configuration management
  - Version synchronization
  - Testing strategies
  - Documentation

**Examples needed:**
- Comparison scenarios
- Migration examples
- Configuration patterns
- Team workflows

---

## 5. Advanced Topics & Troubleshooting

### 5.1 Performance Optimization
**File:** `docs/advanced/performance.md`
- **Parser performance**
  - First-set optimization
  - Token prediction
  - Lookahead strategies
  - Backtracking reduction
  - Memory efficiency
- **Lexer optimization**
  - State minimization
  - Character classes
  - Buffer management
  - Incremental lexing
  - Caching strategies
- **PSI optimization**
  - Stub indices usage
  - Lazy element creation
  - Reference caching
  - Tree depth reduction
  - Smart pointers
- **Grammar optimization**
  - Rule structure impact
  - Choice ordering
  - Common prefix factoring
  - External rule usage
  - Token vs. rule balance
- **Profiling and measurement**
  - Performance metrics
  - Profiling tools
  - Bottleneck identification
  - Memory analysis
  - Benchmarking

**Examples needed:**
- Optimization patterns
- Before/after comparisons
- Profiling workflows
- Benchmark suites

### 5.2 Common Issues
**File:** `docs/advanced/common-issues.md`
- **Generation problems**
  - Missing generated files
  - Package mismatches
  - Compilation errors
  - Stale outputs
  - Path issues
- **Parser issues**
  - Left recursion detection
  - Ambiguous grammars
  - Token conflicts
  - Infinite loops
  - Stack overflow
- **Lexer problems**
  - Token precedence issues
  - State conflicts
  - Unicode handling
  - Performance degradation
  - Incremental lexing bugs
- **PSI problems**
  - Incorrect tree structure
  - Reference resolution
  - Stub mismatches
  - Memory leaks
  - Threading issues
- **Integration issues**
  - Plugin loading failures
  - Feature registration
  - Compatibility problems
  - Performance regression
  - UI freezes

**Examples needed:**
- Error messages and solutions
- Diagnostic techniques
- Common fixes
- Prevention strategies

### 5.3 Debugging Techniques
**File:** `docs/advanced/debugging.md`
- **Grammar debugging**
  - Live Preview usage
  - First/follow analysis
  - Rule reachability
  - Conflict detection
  - Trace output
- **Parser debugging**
  - Breakpoint strategies
  - Parser trace logs
  - Token stream inspection
  - Tree visualization
  - State inspection
- **PSI debugging**
  - PSI Viewer mastery
  - Tree traversal
  - Reference tracing
  - Stub validation
  - Memory analysis
- **IDE debugging**
  - Plugin debugging setup
  - Remote debugging
  - Log analysis
  - Performance profiling
  - UI debugging
- **Advanced tools**
  - Custom inspections
  - Diagnostic actions
  - Test utilities
  - Profiler integration

**Examples needed:**
- Debugging workflows
- Tool configurations
- Analysis techniques
- Case studies

### 5.4 Migration Guide
**File:** `docs/advanced/migration.md`
- **Version compatibility**
  - Grammar-Kit versions
  - IntelliJ Platform versions
  - Java version requirements
  - API changes
  - Deprecations
- **Grammar evolution**
  - Refactoring strategies
  - Backward compatibility
  - Incremental migration
  - Testing approaches
  - Rollback procedures
- **API migrations**
  - Platform API updates
  - PSI changes
  - Extension point evolution
  - Service updates
  - UI component changes
- **Tool updates**
  - Gradle plugin updates
  - Build tool changes
  - CI/CD adjustments
  - Testing framework updates
- **Best practices**
  - Version control strategies
  - Documentation updates
  - Team communication
  - Risk management
  - Validation procedures

**Examples needed:**
- Migration checklists
- Version matrices
- Update patterns
- Team workflows

---

## 6. Reference

### 6.1 Attribute Reference
**File:** `docs/reference/attributes.md`
- **Complete attribute catalog**
  - Alphabetical listing
  - Categorized views
  - Quick reference card
  - Search index
- **Global attributes**
  - Parser configuration
  - PSI configuration
  - Generation control
  - Utility configuration
  - Advanced options
- **Rule attributes**
  - Parsing control
  - PSI generation
  - Type hierarchy
  - Recovery options
  - Optimization hints
- **Pattern attributes**
  - Pattern syntax
  - Wildcard usage
  - Priority rules
  - Complex patterns
- **Attribute details**
  - Syntax specifications
  - Value constraints
  - Default values
  - Inheritance rules
  - Interaction effects
- **Usage examples**
  - Common combinations
  - Advanced patterns
  - Real-world usage
  - Anti-patterns

**Structure:** Each attribute entry includes:
- Name and syntax
- Description and purpose
- Valid values and defaults
- Scope (global/rule/pattern)
- Examples and use cases
- Related attributes
- Version information

### 6.2 Grammar Syntax Reference
**File:** `docs/reference/grammar-syntax.md`
- **EBNF notation**
  - Complete syntax diagram
  - Grammar-Kit extensions
  - Operator precedence
  - Special constructs
- **Grammar elements**
  - Rules and tokens
  - Expressions and sequences
  - Quantifiers and groups
  - Predicates and externals
- **Built-in functions**
  - Parsing predicates
  - External predicates
  - Utility functions
  - Meta-rules
- **Special tokens**
  - Reserved words
  - Built-in token types
  - Special symbols
  - Escape sequences
- **Grammar structure**
  - File organization
  - Section ordering
  - Naming conventions
  - Style guidelines

### 6.3 Keyboard Shortcuts
**File:** `docs/reference/shortcuts.md`
- **Essential shortcuts**
  - Generate parser (Ctrl+Shift+G)
  - Live Preview (Ctrl+Alt+P)
  - Rule navigation
  - Quick documentation
- **Editor shortcuts**
  - Code completion
  - Navigation
  - Refactoring
  - Selection
- **Debugging shortcuts**
  - PSI Viewer
  - Evaluator
  - Breakpoints
  - Inspection
- **Platform variations**
  - Windows/Linux mappings
  - macOS mappings
  - Customization options
  - Keymap schemes

### 6.4 Glossary
**File:** `docs/reference/glossary.md`
- **Parser terminology**
  - Grammar terms
  - Parsing concepts
  - Algorithm terms
  - Tree structures
- **Grammar-Kit terms**
  - Plugin-specific terms
  - Attribute names
  - Generation concepts
  - Tool terminology
- **IntelliJ Platform terms**
  - PSI concepts
  - API terms
  - Extension points
  - Service types
- **Common abbreviations**
  - Technical acronyms
  - File extensions
  - API abbreviations
  - Tool names

---

## 7. Appendices

### A. Example Grammars
**File:** `docs/appendices/examples.md`
- **Complete examples with explanations**
  - JSON parser - Simple hierarchical data
  - Expression calculator - Arithmetic expressions
  - Simple scripting language - Statements and control flow
  - Configuration file parser - Key-value with sections
  - Markdown subset - Mixed content parsing
- **For each example:**
  - Complete grammar file
  - Sample input files
  - Generated code overview
  - PSI hierarchy
  - Test suite
  - Integration points
  - Common extensions
- **Code organization**
  - Project structure
  - Build configuration
  - Test organization
  - Documentation

### B. Resources
**File:** `docs/appendices/resources.md`
- **Official resources**
  - GitHub repository
  - Issue tracker
  - Release notes
  - Contributing guide
- **Community resources**
  - Discussion forums
  - Stack Overflow tags
  - Gitter/Discord channels
  - User groups
- **Learning materials**
  - Video tutorials
  - Blog posts
  - Conference talks
  - Example projects
- **Related tools**
  - ANTLR comparison
  - Parser generators
  - Language workbenches
  - Testing tools
- **IntelliJ Platform resources**
  - SDK documentation
  - API reference
  - Plugin repository
  - Development forums

### C. FAQ
**File:** `docs/appendices/faq.md`
- **Getting started questions**
  - Installation issues
  - First grammar problems
  - Common misconceptions
  - Learning curve
- **Grammar development**
  - Design questions
  - Syntax clarifications
  - Pattern questions
  - Debugging help
- **Generation issues**
  - Build problems
  - Integration questions
  - Performance concerns
  - Compatibility
- **Advanced topics**
  - Complex patterns
  - Performance tuning
  - Team development
  - Large projects
- **Troubleshooting**
  - Common errors
  - Platform issues
  - Version problems
  - Migration questions

---

## Documentation Standards

### Visual Elements
1. **Screenshots**
   - IDE with Grammar-Kit features
   - Live Preview interface
   - PSI Viewer demonstrations
   - Project structure examples
   - Generation output

2. **Diagrams**
   - Grammar structure flows
   - PSI hierarchy visualizations
   - Parser generation process
   - Error recovery illustrations
   - Expression precedence trees

3. **Code Examples**
   - Complete and runnable
   - Progressive complexity
   - Well-commented
   - Include anti-patterns
   - Show best practices

### Writing Principles
1. **Progressive disclosure**
   - Start with essentials
   - Build complexity gradually
   - Clear prerequisites
   - Learning pathways

2. **Task-oriented approach**
   - Focus on goals
   - Step-by-step guides
   - Verification points
   - Troubleshooting tips

3. **Comprehensive coverage**
   - All features documented
   - Edge cases addressed
   - Performance implications
   - Version considerations

### Quality Standards
- Technical accuracy verified against source
- Examples tested and validated
- Cross-references maintained
- Consistent terminology
- Regular updates

This outline serves as the authoritative guide for Grammar-Kit documentation development, ensuring comprehensive coverage of all features and use cases while maintaining a clear learning progression for users at all skill levels.