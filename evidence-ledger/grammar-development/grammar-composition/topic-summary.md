# Section 2.7: Grammar Composition -- Topic Summary

## Purpose

Explain how to split large grammars across multiple parser classes, share tokens and PSI configuration, define multiple entry points, and manage independent grammars within a single plugin. This section covers the structural and organizational aspects of scaling grammars.

## Audience

IntelliJ plugin developers whose grammars have grown large enough to benefit from splitting, or who need multiple parsers in a single plugin. Assumes familiarity with grammar syntax (Section 2.1) and attributes (Section 3.1).

## Page Structure

### H1: Grammar Composition

Opening paragraph: Explain the problem (large grammars produce large parser files) and Grammar-Kit's solution (splitting via `parserClass`). Mention the other composition pattern: independent grammars sharing a plugin.

### H2: Splitting a Grammar into Multiple Parsers

The `;{ parserClass="..." }` syntax. Explain the semicolon requirement (makes the attribute block global, not attached to the previous rule). Show the three-class ExternalRules.bnf example. Explain what is shared (PSI config, tokens, elementTypeHolderClass) vs. what is per-section (parserClass, attribute overrides like extends patterns).

### H2: Cross-Class References

Rules from one parser class can reference rules in another, including meta rules. Show the ExternalRules.bnf cross-class meta rule example. Explain that generated code handles the static method calls across classes automatically.

### H2: Multiple Entry Points

The `extraRoot` attribute for additional parse entry points. Explain the use case (embedded code blocks, different file contexts). Show the syntax.

### H2: Independent Grammars

When two grammars are completely separate (Grammar.bnf and JFlex.bnf pattern). Explain namespace isolation: different parserClass, psiClassPrefix, elementTypePrefix, psiPackage. No conflicts because nothing is shared.

### H2: Pattern-Based Attributes

Using regex patterns in attribute declarations to apply settings across many rules at once. This is a composition mechanism that keeps the grammar DRY. Show extends, pin, elementTypeFactory patterns.

## Key Evidence to Include

- `;{ parserClass="..." }` syntax and semicolon requirement
- Shared vs. per-section configuration
- Cross-class meta rule references
- extraRoot attribute
- Grammar.bnf vs. JFlex.bnf namespace isolation
- Pattern-based attribute application
- Generator file output order: parser classes, types holder, PSI interfaces, PSI impls, visitor

## Examples to Include

- Three-class split (ExternalRules.bnf, Example 1)
- Cross-class meta rules (Example 2)
- Two independent grammars (Example 3)
- Pattern-based attributes (Example 4)
- Extra root (Example 5)
- Multi-parser with shared PSI (Example 6)

## Cross-References

- Section 2.1 (Grammar Syntax) for grammar file structure
- Section 2.6 (External Rules) for meta rules and external rule patterns
- Section 3.1 (Attributes System) for detailed attribute coverage
- Section 3.2 (Parser Generation) for generated file structure
- Section 3.4 (PSI Customization) for PSI configuration
