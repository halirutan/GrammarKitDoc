# Debugging Techniques

When a grammar does not parse as expected, Grammar-Kit provides several tools for understanding what the parser sees, what it tries, and where it goes wrong. This page covers the debugging workflow from grammar analysis through runtime inspection.

## Analyzing Rules with Quick Documentation

Press **Ctrl+Q** (or **F1** on macOS) on any rule in the grammar editor to see its analysis. The documentation popup shows:

| Field | Shows |
|---|---|
| Starts with | The FIRST set (tokens that can begin parsing this rule) |
| Followed by | The NEXT set (tokens that can appear after this rule matches) |
| #auto recovery predicate | The auto-generated recovery condition for rules using `recoverWhile="#auto"` |
| Contains | Public rules, tokens, and external rules with their cardinalities |

For expression-parsing rules, the popup also shows the priority table: each operator's type (BINARY, N_ARY, PREFIX, POSTFIX, ATOM) and its priority level, with the current rule highlighted.

For attributes, the popup shows the HTML description from the attribute's documentation file.

This is the fastest way to verify that a rule's FIRST and NEXT sets look correct. If a rule's FIRST set overlaps with a sibling alternative, the parser may enter the wrong branch. If the NEXT set is missing expected tokens, the follow context may not propagate correctly through the grammar.

## Live Preview

Live Preview provides real-time parsing feedback while you edit your grammar. Open it with **Ctrl+Alt+P**. As you type sample input in the preview editor, Grammar-Kit parses it using the current grammar and shows the resulting tree in the Structure View.

### What Live Preview Shows

Error elements appear highlighted with error attributes, so you can immediately see where parsing fails. The preview reparses automatically when the grammar changes, with a 500ms debounce to avoid constant reparsing during typing.

### Grammar-at-Caret Highlighting

Press **Ctrl+Alt+F7** to enable grammar-at-caret highlighting. When you place the cursor in the preview editor, Grammar-Kit highlights the corresponding BNF expressions in the grammar file:

- Matched expressions use search-result highlighting
- Unmatched expressions use write-search-result highlighting

This lets you trace exactly which grammar rules were active at a given position in the input and which alternatives were attempted but did not match.

### Endless Recursion Detection

Live Preview detects infinite recursion at runtime. It maintains a bitset per input offset, and each rule call at a given offset sets a bit. If the bit is already set, the preview reports:

> "Endless recursion detected for 'rule_name'"

This catches grammar problems that static analysis might miss, such as indirect recursion through external rules or rules that consume no input.

## Editor Annotations

Grammar-Kit annotates the grammar editor with several visual cues that help you understand parser behavior without generating code.

### Pin Markers

The pin marker annotator visually marks pinned elements in your grammar. This helps you verify which token commits the parser to a particular sequence, which is critical for understanding error recovery behavior. If the wrong element is pinned, the parser may commit too early or too late, producing confusing error messages. See [Error Recovery](../grammar-development/error-recovery.md) for background on the `pin` attribute.

### Recursion Indicators

Gutter icons indicate recursive rules. These appear as line markers next to rules that call themselves directly or through a chain of other rules. Recursion is not necessarily a problem (expression grammars rely on it), but unexpected recursion can cause stack overflows or infinite loops.

### Rule Hierarchy Navigation

Gutter icons also show rule extends relationships, letting you navigate up and down the rule hierarchy. This is useful when debugging PSI type issues where a rule should inherit from a base type but the `extends` chain is not configured correctly.

## Testing in Isolation with LightPsi

When you need to debug a grammar outside the IDE environment, use `LightPsi` to parse input programmatically:

```java
PsiFile file = LightPsi.parseFile(
    "test.bnf", grammarText, new BnfParserDefinition()
);
```

`LightPsi` initializes a minimal PSI infrastructure without starting a full IDE instance. This is useful for writing unit tests that verify parse tree structure, for reproducing parsing issues in a controlled environment, and for automated testing in CI pipelines where the IDE is not available.

## FIRST and NEXT Set Analysis

The `BnfFirstNextAnalyzer` computes the token sets that drive parser decisions. You can access these through Quick Documentation (Ctrl+Q), but understanding what they mean helps you diagnose problems:

- `FIRST(rule)`: tokens that can start parsing this rule. If two alternatives in a choice have overlapping FIRST sets, the parser tries them in order and backtracks on failure.
- `NEXT(rule)`: tokens that can follow this rule. The `#auto` recovery predicate uses NEXT sets to determine when to stop consuming error tokens.
- Special markers: `-eof-` (end of file can follow), `-never-matches-` (rule cannot match), `-any-` (any token can follow).

If a rule's FIRST set contains `-never-matches-`, the rule is unreachable. If NEXT contains `-any-`, the rule is in a context with no constraint on what follows, which may indicate a missing recovery boundary.

## Debugging Workflow

When a grammar produces unexpected parse results, follow this sequence:

1. Open Live Preview and enter the problematic input. Check where the parse tree diverges from your expectation.
2. Place the cursor at the failure point and enable grammar-at-caret highlighting (Ctrl+Alt+F7). Identify which rule the parser was in when it failed.
3. Press Ctrl+Q on that rule to inspect its FIRST and NEXT sets. Verify that the expected token is in the FIRST set.
4. If the FIRST set is wrong, trace the rule's definition to find which subrule or alternative is causing the unexpected set.
5. If the parse succeeds but produces the wrong tree structure, check `pin` and `extends` attributes on the relevant rules. Pin affects where the parser commits; `extends` affects how nodes are wrapped.

For issues that only appear with generated code (not in Live Preview), compare the Live Preview tree with the generated parser's output. The generated parser uses a JFlex lexer while Live Preview uses a simplified lexer, so token-level differences can cause divergent behavior. See [Lexer Integration](../code-generation/lexer-integration.md) for details on how the lexer affects parsing.
