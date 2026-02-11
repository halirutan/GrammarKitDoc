# Attributes System

Grammar-Kit uses attributes to control parser generation, PSI structure, and various aspects of code generation. This comprehensive guide covers all attribute types, their usage patterns, and practical examples.

## Attribute Categories

TODO: Provide an overview of the different attribute categories in Grammar-Kit
- [ ] Explain the distinction between global and rule-level attributes
- [ ] Describe pattern-based attributes and their use cases
- [ ] Detail attribute inheritance rules and precedence
- [ ] Include visual diagram showing attribute hierarchy

## Global Parser Attributes

Global parser attributes control the overall parser generation process and appear at the top of your grammar file.

### parserClass
TODO: Document the parserClass attribute
- [ ] Explain how to set the main parser class name
- [ ] Show default naming conventions
- [ ] Provide examples of custom parser class names
- [ ] Discuss package organization considerations

### parserPackage
TODO: Document the parserPackage attribute
- [ ] Describe how to specify parser package location
- [ ] Show relationship to project structure
- [ ] Include examples with different package hierarchies
- [ ] Explain impact on generated imports

### parserImports
TODO: Document the parserImports attribute
- [ ] Explain how to add import statements to generated parser
- [ ] Show syntax for single and multiple imports
- [ ] Provide examples of commonly needed imports
- [ ] Discuss static imports and wildcard usage

### parserUtilClass
TODO: Document the parserUtilClass attribute
- [ ] Describe the parser utility class reference
- [ ] Explain when to use custom utility classes
- [ ] Show how to implement parser utility methods
- [ ] Provide examples of common utility patterns

### generatePsi
TODO: Document the generatePsi attribute
- [ ] Explain PSI generation control options
- [ ] Show how to disable PSI generation
- [ ] Describe use cases for parser-only generation
- [ ] Include examples of different generation modes

## Global PSI Attributes

These attributes control the generation of PSI (Program Structure Interface) classes.

### psiPackage
TODO: Document the psiPackage attribute
- [ ] Explain how to set PSI classes package
- [ ] Show naming conventions for PSI packages
- [ ] Describe relationship to parser package
- [ ] Include multi-module project examples

### psiImplPackage
TODO: Document the psiImplPackage attribute
- [ ] Describe implementation package configuration
- [ ] Explain separation of interfaces and implementations
- [ ] Show default package structure
- [ ] Provide examples of custom package layouts

### psiClassPrefix/Suffix
TODO: Document psiClassPrefix and psiClassSuffix attributes
- [ ] Explain PSI class naming patterns
- [ ] Show how to add prefixes to generated classes
- [ ] Demonstrate suffix usage for implementations
- [ ] Include examples of naming conventions

### psiImplUtilClass
TODO: Document the psiImplUtilClass attribute
- [ ] Describe PSI utility class configuration
- [ ] Show how to implement PSI utility methods
- [ ] Explain method resolution order
- [ ] Provide examples of common PSI utilities

### elementTypeHolderClass
TODO: Document the elementTypeHolderClass attribute
- [ ] Explain token types holder configuration
- [ ] Show default element type organization
- [ ] Describe custom element type holders
- [ ] Include examples of token type management

## Rule-Specific Attributes

Attributes that can be applied to individual grammar rules to control their behavior.

### pin
TODO: Document the pin attribute
- [ ] Explain parse tree commitment mechanism
- [ ] Show how pinning affects error recovery
- [ ] Describe pin patterns for different rule types
- [ ] Include examples of effective pin usage

### recoverWhile
TODO: Document the recoverWhile attribute
- [ ] Describe error recovery predicates
- [ ] Show syntax for recovery expressions
- [ ] Explain relationship with pin attribute
- [ ] Provide examples of recovery strategies

### extends/implements
TODO: Document the extends and implements attributes
- [ ] Explain type hierarchy configuration
- [ ] Show how to extend PSI interfaces
- [ ] Describe implementation inheritance
- [ ] Include examples of PSI hierarchies

### methods
TODO: Document the methods attribute
- [ ] Describe custom accessor generation
- [ ] Show syntax for method declarations
- [ ] Explain method naming conventions
- [ ] Provide examples of common accessors

### mixin
TODO: Document the mixin attribute
- [ ] Explain implementation mixing mechanism
- [ ] Show how to add behavior to PSI classes
- [ ] Describe mixin class requirements
- [ ] Include examples of mixin patterns

### stubClass
TODO: Document the stubClass attribute
- [ ] Describe stub support configuration
- [ ] Explain benefits of stub-based PSI
- [ ] Show stub class implementation
- [ ] Provide examples of indexing integration

### elementType
TODO: Document the elementType attribute
- [ ] Explain custom element type assignment
- [ ] Show how to override default types
- [ ] Describe element type factories
- [ ] Include examples of type customization

### name
TODO: Document the name attribute
- [ ] Describe rule result naming
- [ ] Show impact on generated methods
- [ ] Explain naming strategies
- [ ] Provide examples of name overrides

## Pattern Attributes

Pattern-based attributes allow applying attributes to multiple rules using wildcards.

### Pattern Syntax
TODO: Document pattern attribute syntax
- [ ] Explain wildcard patterns (* and **)
- [ ] Show how to target multiple rules
- [ ] Describe pattern matching order
- [ ] Include examples of complex patterns

### Attribute Application Order
TODO: Explain how pattern attributes are applied
- [ ] Describe precedence rules
- [ ] Show override mechanisms
- [ ] Explain conflict resolution
- [ ] Provide examples of attribute cascading

## Advanced Attributes

Specialized attributes for advanced code generation control.

### tokens
TODO: Document the tokens attribute
- [ ] Explain token generation configuration
- [ ] Show how to define token sets
- [ ] Describe token type customization
- [ ] Include examples of token management

### generate
TODO: Document the generate attribute
- [ ] Describe selective generation control
- [ ] Show how to exclude rules from generation
- [ ] Explain use cases for partial generation
- [ ] Provide examples of generation filtering

### elementTypeClass/Factory
TODO: Document elementTypeClass and elementTypeFactory
- [ ] Explain custom element type creation
- [ ] Show factory pattern implementation
- [ ] Describe use cases for custom types
- [ ] Include examples of type factories

### consumeTokenMethod
TODO: Document the consumeTokenMethod attribute
- [ ] Describe custom token consumption
- [ ] Show how to override token handling
- [ ] Explain performance implications
- [ ] Provide examples of custom consumption

### Special-Purpose Attributes
TODO: Document other specialized attributes
- [ ] List and explain rarely used attributes
- [ ] Show specific use cases for each
- [ ] Include warnings about compatibility
- [ ] Provide examples when applicable

## Examples

TODO: Add comprehensive attribute usage examples
- [ ] Create a complete grammar with all common attributes
- [ ] Show pattern matching examples with real grammars
- [ ] Demonstrate attribute combinations for different scenarios
- [ ] Include examples from real-world language implementations