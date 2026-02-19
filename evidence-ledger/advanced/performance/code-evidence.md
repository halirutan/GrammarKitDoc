# Section 5.1: Performance Optimization — Code Evidence

## 1. FIRST-Based Look-Ahead Optimization

**Source: `attributeDescriptions/generateFirstCheck.html`**

> Generate FIRST-based optimization if FIRST(rule) contains no more than N (default: 2) tokens.

**Source: `GenOptions.java:21-67`**

Default `generateFirstCheck = 2`. Controlled via `generate=[first-check=N]`.

When enabled, generated parser checks if the current token is in the rule's FIRST set before attempting to parse, avoiding unnecessary marker creation and method calls.

## 2. consumeTokenMethod for Fast Token Consumption

**Source: `attributeDescriptions/consumeTokenMethod.html`**

Two built-in methods:
- `consumeToken` — default, records error reporting information
- `consumeTokenFast` — skips error reporting for better performance

```bnf
{
  consumeTokenMethod(".*_recover")="consumeTokenFast"
  consumeTokenMethod(".*_expr|.*_op")="consumeTokenFast"
}
```

Rationale: in recovery rules and expression operators, detailed error reporting (which tokens were expected) adds overhead without user benefit.

## 3. RuleGraphHelper: Rule Analysis

**Source: `src/org/intellij/grammar/generator/RuleGraphHelper.java:39-60`**

`RuleGraphHelper` computes:
- Rule-to-rule dependency graph (`myRulesGraph`)
- Rule extends relationships (`myRuleExtendsMap`)
- Per-rule content maps (child rules and tokens with cardinalities)
- Token name/text mappings

Results are cached via `CachedValuesManager` to avoid recomputation.

## 4. ExpressionHelper: Pratt Parser Optimization

**Source: `src/org/intellij/grammar/generator/ExpressionHelper.java:37-60`**

Expression parsing generates a Pratt-style parser with:
- Only 2 methods per expression root (instead of one per precedence level)
- Priority table as a comment in generated code
- Operator type classification: BINARY, N_ARY, PREFIX, POSTFIX, ATOM

Cached via `EXPRESSION_HELPER_KEY` per BnfFile.

## 5. BnfFirstNextAnalyzer

**Source: `src/org/intellij/grammar/analysis/BnfFirstNextAnalyzer.java:36-60`**

Computes FIRST and NEXT token sets for rules:
- `calcFirst(rule)` — tokens that can start the rule
- `calcNext(rule)` — tokens that can follow the rule
- Special markers: `MATCHES_EOF`, `MATCHES_NOTHING`, `MATCHES_ANY`
- Results cached in `myNextCache` to avoid exponential blowup

Used for:
- `#auto` recovery predicate generation
- FIRST-check optimization in parser
- Quick documentation display
- Left-recursion detection

## 6. Token Sequence Optimization

**Source: `CHANGELOG.md` (version 1.5.0)**

> Generator: include quoted tokens in token sequences

Token sequences (consecutive token matches) are optimized into compact matching code.

## 7. Recursion Guard

**Source: Generated parser code pattern**

Every generated parse method starts with:
```java
if (!recursion_guard_(b, l, "rule_name")) return false;
```

This prevents infinite recursion by tracking recursion depth.

## 8. Abstract Rules

**Source: `ParserGenerator.java:182-199`**

Rules detected as abstract generate no parsing code — they exist only for PSI hierarchy. This reduces generated code size for type-hierarchy-only rules.

## 9. Extended Pin Optimization

**Source: `attributeDescriptions/extendedPin.html`**

> Generate code for parsing a sequence tail even if some parts are missing if it is already pinned. The value is true by default.

With `extendedPin=true`, once a sequence is pinned, the parser continues parsing subsequent elements even if earlier ones failed, producing better error recovery without extra code.

## 10. Compact Variable Names

**Source: `Names.java:13-63`**

Default `names="short"` generates single-letter variables (`b`, `l`, `m`, `r`, `c`), reducing generated file sizes.
