# Parser Generation

This page covers the parser generation process in Grammar-Kit, including configuration options, generated components, and integration with build systems.

## Generator Overview

Grammar-Kit uses a sophisticated two-pass generation process to create efficient parsers from BNF grammars.

### Two-Pass Generation Process

TODO:
- Explain the first pass: grammar analysis and validation
- Explain the second pass: code generation based on analysis
- Describe how the two-pass approach enables better optimization
- Explain error detection and reporting during generation

### Generated File Structure

TODO:
- Detail the typical structure of generated parser files
- Explain the relationship between grammar rules and generated methods
- Describe the organization of generated token types
- Show how package structure is determined

### Package Organization

TODO:
- Explain default package conventions
- Describe how to customize package structure
- Show best practices for organizing generated code
- Discuss integration with existing project structure

### Naming Conventions

TODO:
- Document the naming patterns for generated classes
- Explain how rule names translate to method names
- Describe element type naming conventions
- Show how to customize naming through attributes

## Configuration Options

Control how Grammar-Kit generates parser code through various attributes and settings.

### Generation Attributes

TODO:
- List all generation-related global attributes
- Explain parserClass and its usage
- Describe parserPackage configuration
- Detail parserImports for custom imports
- Cover generatePsi and its implications

### Output Directory Setup

TODO:
- Explain default output directory structure
- Show how to configure custom output paths
- Describe IDE vs build tool directory handling
- Discuss version control considerations

### Package Structure Control

TODO:
- Detail psiPackage and psiImplPackage attributes
- Explain separation of interfaces and implementations
- Show how to organize multi-module projects
- Describe namespace management strategies

### Class Naming Patterns

TODO:
- Document psiClassPrefix and psiClassSuffix usage
- Show examples of custom naming schemes
- Explain impact on generated code readability
- Describe naming conflict resolution

## Generated Parser Components

Understanding the structure and purpose of generated parser components.

### Parser Class Structure

TODO:
- Explain the main parser class organization
- Detail the role of static methods
- Describe instance methods and their purpose
- Show the integration with parser utility classes

### Static Parse Methods

TODO:
- Explain entry point methods
- Describe parameter handling
- Show error reporting mechanisms
- Detail return value conventions

### Rule Methods

TODO:
- Explain how grammar rules become methods
- Describe method signatures and parameters
- Show the parsing logic implementation
- Detail error recovery integration

### Utility Integration

TODO:
- Explain parserUtilClass usage
- Show common utility methods
- Describe custom utility integration
- Detail performance optimizations

### Error Handling

TODO:
- Explain error reporting mechanisms
- Describe error recovery integration
- Show custom error handling patterns
- Detail error message customization

## Element Types System

The foundation of Grammar-Kit's type system for parsed elements.

### IElementType Hierarchy

TODO:
- Explain IElementType and its role
- Describe the type hierarchy structure
- Show relationships between element types
- Detail custom element type creation

### Token Type Constants

TODO:
- Explain token type generation
- Describe naming conventions
- Show usage in lexer integration
- Detail token set creation

### Rule Element Types

TODO:
- Explain how rules map to element types
- Describe the relationship to PSI elements
- Show custom element type attributes
- Detail performance considerations

### Element Type Holder

TODO:
- Explain elementTypeHolderClass purpose
- Show default generation behavior
- Describe customization options
- Detail integration patterns

## Generation Customization

Advanced options for customizing the parser generation process.

### Java Version Targeting

TODO:
- Explain version compatibility options
- Show how to target specific Java versions
- Describe language feature usage
- Detail backward compatibility

### Code Style Options

TODO:
- Document available style configurations
- Show indentation and formatting options
- Explain naming convention choices
- Detail import organization

### Debug Information

TODO:
- Explain debug information generation
- Show how to enable parser tracing
- Describe debugging aids in generated code
- Detail production vs debug builds

### Optimization Levels

TODO:
- Explain available optimization options
- Show performance vs readability tradeoffs
- Describe specific optimizations
- Detail measurement and profiling

### Custom Templates

TODO:
- Explain template customization possibilities
- Show how to override default templates
- Describe template variables and expansion
- Detail advanced customization scenarios

## Build Integration

Integrating parser generation into your build process.

### IDE Generation (Ctrl+Shift+G)

TODO:
- Explain the IDE generation workflow
- Show keyboard shortcuts and menu options
- Describe generation options dialog
- Detail error reporting and feedback

### Command-Line Generation

TODO:
- Document command-line usage
- Show available command-line options
- Explain batch processing
- Detail integration with scripts

### Gradle Plugin Usage

TODO:
- Show basic Gradle configuration
- Explain task dependencies
- Describe incremental generation
- Detail multi-module setups

### CI/CD Pipelines

TODO:
- Show GitHub Actions integration
- Explain Jenkins pipeline setup
- Describe reproducible builds
- Detail artifact management

## Examples

TODO:
- Add complete generation setup example
- Include generated code walkthrough
- Show customization examples
- Provide build configuration samples