# Performance Optimization

Grammar-Kit generates recursive-descent parsers that are fast by default. Most grammars produce parsers that handle typical files in milliseconds. When you work with large files or complex grammars, though, targeted optimizations can make a measurable difference.

This page covers the built-in optimizations Grammar-Kit provides and the grammar-level choices that affect parser speed and memory use.

## Parser-Level Optimizations

### FIRST-Set Checks

When a rule's FIRST set (the tokens that can begin it) is small, Grammar-Kit generates a guard check at the start of the parse method. The parser verifies that the current token belongs to the FIRST set before creating markers or calling into subrules. This avoids unnecessary work when the rule clearly cannot match.

Control this with the `generate` attribute:

```bnf
{
  generate=[first-check=2]
}
```

The value sets the maximum size of FIRST sets that trigger optimization. The default is `2`. Increasing the value covers more rules but produces slightly larger generated code. Setting it to `0` disables the optimization entirely.

### Fast Token Consumption

By default, the `consumeToken` method records information for error reporting (which tokens were expected at a given position). In rules where detailed error context is unnecessary, you can switch to `consumeTokenFast`, which skips that bookkeeping.

Recovery rules and expression operators are good candidates, since their error reporting rarely surfaces to users:

```bnf
{
  consumeTokenMethod(".*_recover")="consumeTokenFast"
  consumeTokenMethod(".*_expr|.*_op")="consumeTokenFast"
}
```

The pattern matches against rule names, so you can target specific categories of rules with a single declaration.

### Recursion Guard

Every generated parse method starts with a recursion guard:

```java
if (!recursion_guard_(b, l, "rule_name")) return false;
```

This prevents infinite recursion by tracking call depth. The guard adds minimal overhead per call and protects against runaway parsing in malformed input. You do not need to configure it; it is always present.

### Token Sequence Optimization

When a rule contains consecutive token matches (a fixed sequence of tokens with no alternatives or subrules between them), the generator combines them into compact matching code. This reduces method calls for rules that match keyword sequences or fixed syntactic patterns.

## Expression Parsing Efficiency

Grammar-Kit's expression parsing generates a Pratt-style parser that handles operator precedence with only two methods per expression root, regardless of how many precedence levels you define. A traditional recursive-descent approach creates one method per level, which grows the call stack proportionally to the number of levels.

The generated code includes a priority table (as a comment) that maps each operator to its type and precedence. Operator types are classified as BINARY, N_ARY, PREFIX, POSTFIX, or ATOM. This classification drives the parsing logic without additional method dispatch.

For details on structuring expression grammars, see the [Expression Parsing](../grammar-development/expression-parsing.md) page.

## Grammar-Level Optimizations

### Rule Visibility

Mark rules as `private` when they do not need to appear in the PSI tree. Private rules are inlined into their callers during generation, which eliminates method call overhead and reduces the number of PSI nodes created during parsing.

### Abstract Rules

Rules that exist only to define a PSI type hierarchy (no concrete syntax of their own) are detected as abstract. Grammar-Kit generates no parsing code for them, reducing the overall size of the generated parser.

### Extended Pin

The `extendedPin` attribute (enabled by default) allows the parser to continue matching a sequence after it has been pinned, even if intermediate elements fail. This produces better error recovery without extra generated code. If you disable it (`generate=[extended-pin="false"]`), the parser stops a sequence at the first failure after the pin point, which reduces recovery quality but may simplify debugging in rare cases.

### Compact Variable Names

By default, Grammar-Kit uses `names="short"`, which generates single-letter variable names (`b`, `l`, `m`, `r`, `c`) in parse methods. This reduces the size of generated files, which matters when your grammar produces hundreds of parse methods. The alternative `names="long"` uses descriptive variable names, which is useful during development but increases file size.

## Caching in the Generator

Grammar-Kit caches several analysis results to avoid recomputation when you edit a grammar:

- `RuleGraphHelper` caches rule dependency graphs, extends relationships, per-rule content maps, and token mappings through `CachedValuesManager`.
- `ExpressionHelper` caches expression rule analysis (priority tables, operator classification) per BNF file.
- `BnfFirstNextAnalyzer` caches NEXT-set computations to avoid exponential blowup when computing follow sets across deeply nested grammars.

These caches are invalidated automatically when the grammar file changes. You do not need to manage them manually.

## Practical Recommendations

When you notice parsing slowdowns, check these areas in order:

1. Run FIRST-set analysis (Ctrl+Q on a rule) to verify that your grammar's entry points have small, distinct FIRST sets. Overlapping FIRST sets force the parser to try multiple branches.
2. Apply `consumeTokenFast` to recovery rules and expression operators where error reporting detail is not needed.
3. Mark helper rules as `private` when they serve only as grouping constructs and do not need PSI nodes.
4. Factor common prefixes in choice rules so the parser commits to a branch earlier. If two alternatives start with the same tokens, the parser must try both until they diverge.
5. Use `pin` attributes on sequences to commit the parser after a distinguishing token, reducing backtracking on malformed input.

For a broader view of grammar structuring choices that affect performance, see [Designing Grammar Rules](../grammar-development/grammar-design.md). For details on pin and recovery, see [Error Recovery](../grammar-development/error-recovery.md).
