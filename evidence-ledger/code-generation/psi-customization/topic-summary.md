# Section 3.4: PSI Customization — Topic Summary

## Purpose

Explain how to shape and customize the PSI (Program Structure Interface) classes that Grammar-Kit generates: controlling the type hierarchy with `extends`/`implements`, adding behavior through mixins and method injection, using fake rules for abstract interfaces, customizing accessors, and enabling stub support. This is the deepest section in the Code Generation chapter.

## Audience

Plugin developers who need to add navigation, refactoring, or other IDE features that require custom PSI methods and a well-structured type hierarchy.

## Prerequisites

- Parser generation basics (Section 3.2)
- Attributes system overview (Section 3.1)
- Basic understanding of IntelliJ PSI

## Structure

### H1: PSI Customization

Opening paragraph: Grammar-Kit generates PSI interfaces and implementation classes for each public rule. By default, every rule extends `ASTWrapperPsiElement` and implements `PsiElement`. You can reshape this hierarchy, add custom methods, and integrate with IntelliJ features through several attributes and techniques.

### H2: Shaping the Type Hierarchy

Cover `extends` and `implements` attributes:

- `extends` with a rule name: makes AST flat (collapsing), sets PSI supertype
- `extends` with a Java class: sets implementation base class
- `implements` with interface list: adds interfaces to PSI
- Pattern-based application: `extends(".*_expr")=expr`
- Effect on the visitor: visitor dispatch follows the extends chain
- The `private` modifier: skips AST node creation

Evidence: code-evidence.md sections 1, 10, 13; examples.md examples 1, 8

### H2: Fake Rules

Explain fake rules as PSI-only constructs:

- Generate interfaces and implementations but no parsing code
- Used to create abstract base types in the PSI hierarchy
- Can define methods, implements, extends
- Cannot be combined with `private`
- Per-rule `psiPackage`/`psiImplPackage` overrides

Show the `binary_expr` fake rule pattern with `left`/`right` accessors.

Evidence: code-evidence.md sections 2, 6 (PsiGen.bnf); examples.md examples 2, 6

### H2: Custom Methods and Accessors

Cover the three kinds of `methods` entries:

1. Path-based accessors: `/expr[0]`, `/expr[last]`, multi-level paths
2. Method mix-ins: names from `psiImplUtilClass` (static methods with PSI element as first param)
3. Accessor renames and suppression: `element="item"`, `item=""`

Also cover `psiImplUtilClass` setup and the Gradle mixin limitation.

Evidence: code-evidence.md sections 4, 5, 7, 11; examples.md examples 3, 4, 5

### H2: Mixins and Method Injection

Cover the `mixin` attribute:

- Sets the base implementation class for a rule
- Used for PsiNamedElement, references, and other IntelliJ contracts
- Gradle limitation: method mixins require two-pass generation (IDE only)

Cover the `psiImplUtilClass` pattern:

- Static methods with PSI element as the extra first parameter
- Listed in `methods` attribute by name only (no signatures needed)

Evidence: code-evidence.md sections 3, 4; examples.md examples 3, 4

### H2: Stub Support

Cover the `stubClass` attribute:

- Shorthand for `implements StubBasedPsiElement<Stub>` + `extends StubBasedPsiElementBase<Stub>`
- `<?>` syntax in `extends` is replaced with the stub class
- `elementTypeFactory` is required for stubs
- `fallbackStubElementType` for compilation order issues

Evidence: code-evidence.md section 8; examples.md example 7

## Key Examples to Include

1. `extends` for flat AST (before/after tree structure)
2. Fake rule with `left`/`right` accessors and visitor hierarchy
3. Mixin class implementing PsiNamedElement
4. Method injection via psiImplUtilClass
5. Path-based accessor syntax
6. Stub configuration

## Cross-References

- Section 3.1 (Attributes System) for attribute syntax
- Section 3.2 (Parser Generation) for generation process
- Section 2.3 (Expression Parsing) for expression hierarchy patterns
- Section 6.1 (Attribute Reference) for complete attribute details

## Writing Notes

- Lead with the simplest customization (extends for flat AST) and build toward stubs
- Show generated Java alongside BNF so readers see the cause-effect
- The fake rules section is conceptually tricky -- use a concrete example throughout
- Mention the Gradle mixin limitation each time mixins come up
- Keep stub support concise -- it is an advanced topic
