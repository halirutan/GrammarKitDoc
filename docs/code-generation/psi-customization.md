# PSI Customization

This page covers PSI (Program Structure Interface) customization in Grammar-Kit, including hierarchy design, custom methods, and advanced PSI features.

## PSI Architecture

Understanding the IntelliJ Platform's PSI system and how Grammar-Kit generates PSI elements.

### PSI Tree Structure

TODO:
- Explain PSI tree fundamentals
- Show relationship between parse tree and PSI
- Describe node types and hierarchy
- Detail memory and performance characteristics

### Element Interfaces

TODO:
- Explain generated PSI interfaces
- Show naming conventions and organization
- Describe method contracts
- Detail relationship to grammar rules

### Implementation Classes

TODO:
- Explain generated implementation classes
- Show the separation from interfaces
- Describe constructor patterns
- Detail internal structure

### Visitor Pattern

TODO:
- Explain PSI visitor generation
- Show visitor interface structure
- Describe visitor method patterns
- Detail usage in analysis and refactoring

### Stub-Based PSI

TODO:
- Explain stub-based PSI benefits
- Show when to use stubs
- Describe stub serialization
- Detail index integration

## Type Hierarchy Design

Creating well-structured PSI hierarchies for maintainable language support.

### Using Extends Attribute

TODO:
- Explain the extends attribute syntax
- Show inheritance patterns
- Describe impact on generated code
- Detail type safety benefits

### Interface Implementation

TODO:
- Explain the implements attribute
- Show marker interface patterns
- Describe multiple interface implementation
- Detail integration with platform interfaces

### Common Base Types

TODO:
- Show recommended base type patterns
- Explain shared functionality extraction
- Describe utility method placement
- Detail framework integration points

### Marker Interfaces

TODO:
- Explain marker interface purposes
- Show common marker patterns
- Describe usage in references and navigation
- Detail performance considerations

## Mixin Classes

Extending generated PSI with custom functionality through mixin classes.

### Mixin Attribute Usage

TODO:
- Explain mixin attribute syntax
- Show how mixins are integrated
- Describe the class hierarchy
- Detail method resolution order

### Implementation Patterns

TODO:
- Show mixin class structure
- Explain required constructors
- Describe method implementation patterns
- Detail access to PSI tree

### Constructor Requirements

TODO:
- Explain mandatory constructor signatures
- Show parameter passing patterns
- Describe initialization order
- Detail error handling

### Method Delegation

TODO:
- Explain delegation patterns
- Show utility method integration
- Describe performance considerations
- Detail debugging techniques

## Custom Methods

Adding custom methods to PSI elements for enhanced functionality.

### Methods Attribute Syntax

TODO:
- Explain methods attribute format
- Show method declaration syntax
- Describe parameter types
- Detail return type specifications

### Path-Based Accessors

TODO:
- Explain path syntax (/expr[0])
- Show child element navigation
- Describe type-safe accessors
- Detail null handling patterns

### Collection Accessors

TODO:
- Show list and array accessors
- Explain collection method patterns
- Describe filtering and searching
- Detail performance optimization

### Type-Safe Methods

TODO:
- Explain type safety in custom methods
- Show generic method patterns
- Describe type casting avoidance
- Detail compile-time verification

### Utility Method Integration

TODO:
- Show integration with psiImplUtilClass
- Explain static utility patterns
- Describe common utility methods
- Detail organization strategies

## Fake Rules

Using fake rules to define shared interfaces without parsing logic.

### Purpose and Patterns

TODO:
- Explain fake rule concept
- Show when to use fake rules
- Describe interface extraction patterns
- Detail naming conventions

### Interface Generation

TODO:
- Show how fake rules generate interfaces
- Explain the lack of parser methods
- Describe usage in type hierarchy
- Detail integration patterns

### Shared Method Sets

TODO:
- Explain method sharing via fake rules
- Show common method patterns
- Describe inheritance strategies
- Detail maintenance benefits

### Type Hierarchy Control

TODO:
- Show hierarchy manipulation with fakes
- Explain multiple inheritance simulation
- Describe type unification patterns
- Detail refactoring strategies

## Advanced PSI Features

Implementing sophisticated PSI functionality for professional language support.

### Reference Implementation

TODO:
- Explain PsiReference basics
- Show reference provider patterns
- Describe reference resolution
- Detail caching strategies

### Name Providers

TODO:
- Explain PsiNamedElement integration
- Show name provider patterns
- Describe rename support
- Detail search integration

### Stub Indices

TODO:
- Explain stub index creation
- Show index key patterns
- Describe query optimization
- Detail memory efficiency

### Smart Pointers

TODO:
- Explain SmartPsiElementPointer usage
- Show pointer creation patterns
- Describe validity checking
- Detail memory management

### Performance Optimization

TODO:
- Explain PSI performance patterns
- Show caching strategies
- Describe lazy evaluation
- Detail profiling techniques

## Examples

TODO:
- Add PSI hierarchy diagram example
- Include custom method implementation samples
- Show complete mixin class example
- Provide reference provider implementation