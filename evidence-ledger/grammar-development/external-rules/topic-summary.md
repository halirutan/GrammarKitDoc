# Section 2.6: External Rules -- Topic Summary

## Purpose

Explain when and how to use external rules and meta rules in Grammar-Kit grammars. Cover the two syntactic forms (external rule declaration and inline external expression), the Java implementation contract, meta rules as parametrized parse functions, and parameter passing mechanics.

## Audience

IntelliJ plugin developers who need to go beyond what pure BNF can express. Assumes the reader understands basic grammar syntax (Section 2.1) and has written at least a simple grammar.

## Page Structure

### H1: External Rules

Opening paragraph: Define what external rules are and why they exist. Three use cases from HOWTO.md: logic easier in code, external dependency, logic already implemented elsewhere.

### H2: External Rule Syntax

Two forms: the `external` declaration and the `<<...>>` inline expression. Show both with the SampleParserUtil example. Explain the Java method contract (PsiBuilder and level are always the first two parameters, extra parameters follow). Cover `parserUtilClass` and `parserImports` for method resolution.

### H2: Meta Rules

What meta rules are (parametrized parse functions). Explain `<<param>>` placeholders. Show the comma-separated list pattern as the canonical example. Cover parameter types: rule references become Parser instances, double-quoted strings are passed as-is, single-quoted strings are unquoted. Include the parameter type summary table.

### H3: Nested Meta Rules

Show how meta rules compose (comma_list_pinned, list_of_lists, two_params_meta). Keep this concise since nesting gets complex.

### H3: Recovery in Meta Rules

Show how recovery predicates can be passed as meta parameters using `<<recover_arg>>`.

### H2: Limitations and Live Preview

External rules referencing static methods are not supported in Live Preview. Only `eof` and `anything` work. Meta rules do work in Live Preview.

## Key Evidence to Include

- External rule syntax: `external name ::= method params`
- Inline syntax: `<<methodName params>>`
- Java contract: PsiBuilder builder, int level + extra params
- parserUtilClass attribute for method resolution
- parserImports for static imports
- Meta rule declaration: `meta name ::= <<param>> ...`
- Parameter types: rule refs -> Parser, "double" as-is, 'single' unquoted
- Recovery predicates as meta parameters
- Live Preview limitation: external static methods not supported

## Examples to Include

- Simple external rule (Example 1 from HOWTO.md)
- Inline external expression (Example 2)
- Comma-separated list meta rule (Example 3)
- Pinned recovery meta rule (Example 4)
- Parameter passing patterns (Example 6)
- Parser imports (Example 8)
- Parameter type summary table

## Cross-References

- Section 2.1 (Grammar Syntax) for rule and token basics
- Section 2.5 (Live Preview) for preview limitations with external rules
- Section 2.7 (Grammar Composition) for cross-class meta rule usage
- Section 2.4 (Error Recovery) for pin and recoverWhile context
- Section 3.1 (Attributes System) for parserUtilClass and parserImports
