# Quick Start Tutorial

This tutorial guides you through creating your first grammar with Grammar-Kit, generating parser code, and building a basic language plugin. By the end, you'll have a working parser with syntax highlighting in IntelliJ IDEA.

## Your First Grammar

Let's start by creating a simple expression grammar to understand Grammar-Kit's core concepts.

### Simple Expression Grammar Example

TODO: Create a complete arithmetic expression grammar:
- Basic structure with number literals
- Addition and multiplication operators
- Proper operator precedence
- Comments and whitespace handling

### Understanding Rules and Tokens

TODO: Explain fundamental concepts:
- What are rules (non-terminals)
- What are tokens (terminals)
- Rule references and recursion
- Token patterns and regular expressions
- Difference between lexer and parser rules

### Using Live Preview

TODO: Document Live Preview feature:
- How to open Live Preview (keyboard shortcut)
- Testing grammar rules interactively
- Understanding the parse tree
- Debugging grammar issues
- Live Preview limitations

### Common Beginner Patterns

TODO: Cover frequently used patterns:
- Optional elements (?)
- Zero or more (*)
- One or more (+)
- Alternatives (|)
- Grouping with parentheses
- Common mistakes to avoid

## Generating Parser Code

Grammar-Kit transforms your BNF grammar into working Java code.

### Running the Generator

TODO: Explain code generation process:
- Using Ctrl+Shift+G shortcut
- Generator configuration options
- Output directory setup
- Regeneration best practices
- Command-line generation for builds

### Understanding Generated Files

TODO: Describe generated code structure:
- Parser class and its methods
- PSI (Program Structure Interface) classes
- Visitor and adapter classes
- Token types and element types
- How generated code relates to grammar rules

### Package Structure

TODO: Explain recommended package organization:
- Where generated files go
- Separating generated from manual code
- Package naming conventions
- Managing imports and dependencies

### Integrating with IntelliJ Platform

TODO: Show integration steps:
- Registering generated parser
- Connecting to language infrastructure
- PSI implementation patterns
- Working with IntelliJ's parsing framework

## Creating a Language Plugin

Transform your parser into a full IntelliJ IDEA language plugin.

### Language and File Type Registration

TODO: Document registration process:
- Creating Language class
- Defining file type
- File extension associations
- Icon configuration
- plugin.xml entries

### Basic ParserDefinition

TODO: Create ParserDefinition implementation:
- Required methods
- Connecting parser to language
- Token type mapping
- Element type factory
- Complete code example

### Lexer Integration

TODO: Explain lexer setup:
- JFlex lexer vs Grammar-Kit lexer
- Lexer adapter implementation
- Token type coordination
- Whitespace and comment handling
- Performance considerations

### Simple Syntax Highlighting

TODO: Implement basic highlighting:
- Creating SyntaxHighlighter
- Defining text attribute keys
- Mapping tokens to colors
- Registration in plugin.xml
- Testing highlighting

## Testing Your Parser

Ensure your parser works correctly with comprehensive testing.

### Creating Test Files

TODO: Develop test file strategy:
- Test file organization
- Positive test cases
- Error recovery tests
- Edge case examples
- Test data management

### Using PSI Viewer

TODO: Document PSI Viewer usage:
- Opening PSI Viewer
- Interpreting the tree structure
- Debugging parsing issues
- PSI element properties
- Performance analysis

### Basic Parsing Tests

TODO: Create unit tests:
- ParsingTestCase setup
- Test file conventions
- Comparing expected PSI
- Testing error recovery
- Automated test execution

### Validation Strategies

TODO: Implement validation:
- Grammar validation
- Semantic validation
- Error reporting
- Quick fixes
- Integration with IDE inspections

## Complete Examples

TODO: Provide the following complete examples:
- Full arithmetic expression grammar with all features
- Sample test files demonstrating grammar capabilities
- Annotated walkthrough of generated code
- Working language plugin with all components integrated

## Running Your Plugin

TODO: Add instructions for:
- Running plugin in development instance
- Debugging parser issues
- Performance profiling
- Packaging for distribution

## Next Steps

After completing this tutorial, you'll have:
- A working grammar file
- Generated parser code
- Basic language plugin with syntax highlighting
- Understanding of Grammar-Kit workflow

Continue learning by:
- Exploring advanced grammar features
- Adding code completion
- Implementing refactoring support
- Creating custom language features

## Troubleshooting

TODO: Address common issues:
- Parser generation fails
- Plugin doesn't recognize files
- Syntax highlighting not working
- Performance problems
- Debugging techniques