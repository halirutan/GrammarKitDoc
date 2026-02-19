# Section 7.A: Example Grammars — Code Evidence

## 1. JSON Grammar (Live Preview)

**Source: `testData/livePreview/Json.bnf` — 27 lines**

Complete JSON grammar demonstrating:
- Token definitions with regexp patterns
- Extends hierarchy: `extends("array|object|json")=value`
- Error recovery: `recoverWhile=recover`
- Pin on sub-expressions: `pin(".*")=1`
- Hooks for whitespace binding
- Name override: `name="value"`

This is the simplest complete grammar in the test data.

## 2. Expression Parser Grammar

**Source: `testData/generator/ExprParser.bnf` — 76 lines**

Full expression grammar demonstrating:
- Pratt-style expression parsing with operator precedence
- 6 precedence levels with BINARY, N_ARY, PREFIX, POSTFIX, ATOM operators
- `extends(".*expr")=expr` for flat PSI hierarchy
- `rightAssociative=true` for assignment
- External meta rule: `external special_expr ::= meta_special_expr`
- Recovery with `recoverWhile=element_recover`
- Fake rule: `fake ref_expr ::= expr? '.' identifier`
- Element type reuse: `{extends=ref_expr elementType=ref_expr}`

Operator catalog:
| Priority | Operators |
|---|---|
| 0 | `assign_expr` (BINARY, rightAssociative) |
| 1 | `elvis_expr`, `conditional_expr` |
| 2 | `plus_expr`, `minus_expr` |
| 3 | `xor_expr`, `between_expr`, `is_not_expr` |
| 4 | `mul_expr`, `div_expr` |
| 5 | `unary_plus_expr`, `unary_min_expr`, `unary_not_expr` (PREFIX) |
| 6 | `exp_expr` (N_ARY) |
| 7 | `factorial_expr` (POSTFIX) |
| 8 | `call_expr` (POSTFIX), `qualification_expr` (POSTFIX) |
| 9 | `special_expr`, `simple_ref_expr`, `literal_expr`, `paren_expr` (ATOM/PREFIX) |

## 3. Live Preview Tutorial Grammar

**Source: `testData/livePreview/LivePreviewTutorial.bnf` — 43 lines**

Simple scripting language grammar used in TUTORIAL.md:
- Property assignments: `id '=' expr`
- Arithmetic expressions with left-associative operators
- Factorial postfix operator
- Recovery on property boundaries
- `name(".*expr")='expression'` for readable error messages
- `extends(".*expr")=expr` pattern

## 4. Grammar-Kit's Own Grammar

**Source: `grammars/Grammar.bnf` — 123 lines**

The BNF grammar format itself, demonstrating:
- External root rule: `external grammar ::= parseGrammar grammar_element`
- Full attribute configuration (13 global attributes)
- Pattern-based extends/implements: `implements("rule|attr")=...`
- Mixin classes for specific rules
- Left rules for choice and quantified expressions
- Fake parenthesized rule for hierarchy
- Pin and recovery throughout

## 5. JFlex Grammar

**Source: `grammars/JFlex.bnf` — 80+ lines**

JFlex file format grammar, demonstrating:
- Separate namespace from Grammar.bnf
- JFlex-specific tokens (`%class`, `%implements`, `%%`, `<<EOF>>`)
- Named element interface for definitions

## 6. Test Data Grammar Catalog

**Source: `testData/generator/` — 29 grammars**

| Grammar | Key Feature |
|---|---|
| `AutoRecovery.bnf` | `#auto` recovery, nested recovery |
| `Autopin.bnf` | Auto-pin patterns |
| `BindersAndHooks.bnf` | Whitespace binder hooks |
| `ConsumeMethods.bnf` | `consumeTokenMethod` patterns |
| `ExternalRules.bnf` | External rules, meta rules, multi-parser |
| `ExternalRulesLambdas.bnf` | Java 8 lambda generation |
| `Fixes.bnf` | Edge cases and bug fixes |
| `GenOptions.bnf` | Generation options |
| `LeftAssociative.bnf` | Left-associative operator patterns |
| `PsiAccessors.bnf` | Path-based PSI accessors |
| `PsiGen.bnf` | PSI customization patterns |
| `PsiStart.bnf` | PSI start configuration |
| `Small.bnf` | Minimal grammar |
| `Stub.bnf` | Stub index support |
| `StubFallback.bnf` | Stub fallback configuration |
| `TokenChoice.bnf` | Token set generation |
| `TokenSequence.bnf` | Token sequence optimization |
| `UpperRules.bnf` | Upper rule modifier |
| `UtilMethods.bnf` | Method injection from psiImplUtilClass |
