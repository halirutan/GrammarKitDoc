# Topic Summary: Error Recovery

## Target File
`docs/grammar-development/error-recovery.md`

## Page Title
**Error Recovery**

## Purpose
Explain how to make Grammar-Kit parsers resilient to broken or incomplete input. Error recovery is critical for IDE-quality parsing: without it, a single typo can destroy the entire PSI tree, breaking code completion, navigation, and error highlighting. Readers arrive here needing to understand the `pin` and `recoverWhile` attributes, how to write recovery predicates, and how to apply recovery patterns to their grammars.

## Audience
Plugin developers whose grammar parses successfully on valid input but needs to handle broken code gracefully. Assumes familiarity with BNF syntax (Section 2.1) and grammar design basics (Section 2.2). May be read after a developer notices that their parser produces poor error messages or loses PSI structure on invalid input.

---

## Recommended Structure

### H1: Error Recovery

Opening paragraph: A Grammar-Kit parser without error recovery stops on the first unexpected token, losing all structure beyond that point. Two attributes make recovery possible: `pin` commits a rule after a recognizable prefix, and `recoverWhile` skips unexpected tokens to resynchronize. Together, they let the parser preserve PSI nodes for code completion and navigation even in broken code. This page explains how both work and shows the patterns for applying them.

Reference: TUTORIAL.md -- "pin: if a prefix of a sequence matches up to and including the pinned item, the parser considers the match successful. recoverWhile: regardless of the result, parser will continue to consume tokens while the predicate rule matches."

### H2: Pin

How pin commits a rule and prevents rollback.

#### H3: How Pin Works

- Pin applies to items of a grammar **sequence** only (not choices).
- Value is 1-indexed: `{pin=2}` means the second item in the sequence.
- Once the pinned item matches, the parser considers the rule matched even if later items fail.
- With `extendedPin=true` (the default), the parser still attempts to match the rest of the sequence after pin, recording errors for missing parts.
- The return value changes: `result_ || pinned_` -- true if the pin point was reached.

Illustrate with a simple property rule: `property ::= id '=' expr {pin=2}`. Walk through what happens when `id '='` matches but `expr` is missing: the property node is created, an error is recorded for missing `expr`, and parsing continues.

Reference code-evidence "Basic Pin Contract," "ExtendedPin Mode."

#### H3: Pin Value Formats

- **Numeric**: `{pin=2}` -- pins at position 2 (1-indexed).
- **Pattern**: `{pin="table_ref"}` -- pins at the item whose text matches the regex.
- **Sub-expression**: `{pin(".*")=1}` -- applies pin=1 to all sub-sequences in the rule.
- **Global pattern**: `pin("create_.*")=2` in the global attributes block.
- Note: pinning the last item is trivial and ignored by the generator.

Use examples.md Example 5 (pin attribute variants) as the illustration.

### H2: RecoverWhile

How recoverWhile skips unexpected tokens to resynchronize.

#### H3: How RecoverWhile Works

The contract (from recoverWhile.html):

1. The attributed rule is handled as usual (matches or fails).
2. Regardless of the result, the parser continues to consume tokens while the predicate rule matches.

Usage rules:

1. Should be on a rule that is inside a loop (so there is a "next iteration" to resume at).
2. That rule should have `pin` somewhere (otherwise recovery runs but the rule never commits).
3. The value should be a predicate rule that leaves input intact (does not consume tokens).
4. In most cases the predicate is `!(token1 | token2 | ...)` -- a NOT predicate listing boundary tokens.

Reference code-evidence "Basic RecoverWhile Contract," "RecoverWhile Usage Rules."

#### H3: Writing Recovery Predicates

- Always a NOT predicate: `private rule_recover ::= !(';' | KEYWORD | ...)`.
- Must be `private` (inspection warns "Non-private recovery rule" otherwise).
- Boundary tokens are where the parser should stop skipping and resume normal parsing.
- Common boundaries: delimiters (`;`, `,`, `)`, `}`), statement-starting keywords.
- The predicate does NOT consume input. It only tests whether the next token is a boundary.

Patterns:
- Statement recovery: `!(';' | SELECT | DELETE | INSERT)`.
- List item recovery: `!(',' | ')')`.
- Property recovery: `!(';' | id '=')`.
- JSON structural: `!(',' | ']' | '}' | '[' | '{')`.

Reference code-evidence "Writing Recovery Predicates," "Common Predicate Patterns."

#### H3: Automatic Recovery with #auto

- `recoverWhile="#auto"` generates a predicate from the rule's FOLLOWS set.
- Equivalent to `! FOLLOWS(rule)` -- stops at any token that can legally follow the rule.
- Generated predicate name: `<rule>_auto_recover_`.
- Quick Documentation (Ctrl-Q) shows the expanded predicate for verification.
- Use `#auto` when the FOLLOWS set naturally covers the right boundary tokens. Write a manual predicate when you need to include additional boundaries (e.g., statement-starting keywords that are not in the FOLLOWS set).

Use the AutoRecovery.bnf example: `item ::= number {recoverWhile="#auto"}`.

### H2: Recovery Patterns

Concrete, reusable patterns combining `pin` and `recoverWhile`.

#### H3: Statement-Level Recovery

```
script ::= script_item *
private script_item ::= !<<eof>> statement ';' {pin=1 recoverWhile=statement_recover}
private statement_recover ::= !(';' | SELECT | DELETE | ...)
private statement ::= select_statement | delete_statement | ...
select_statement ::= SELECT ... {pin=1}
```

Walk through broken input showing how recovery preserves subsequent statements. Reference examples.md Example 1.

#### H3: List Recovery

```
list ::= '(' [!')' item (',' item) *] ')' {pin(".*")=1}
item ::= number {recoverWhile=item_recover}
private item_recover ::= !(',' | ')')
```

Explain each piece: `pin(".*")=1` pins all sub-sequences, `!')'` lookahead prevents matching an empty list as an error, `recoverWhile` on each item skips garbage until `,` or `)`. Show the PSI tree for broken input `(1, -, , 3, )` from examples.md Example 2.

Mention the `#auto` variant and trailing comma support.

#### H3: Nested Recovery

- JSON object/array pattern: shared `recover` predicate across array items and object properties.
- The `prop ::= []` trick: empty optional with `pin=1` makes the property name effectively optional during error recovery without changing the grammar's formal structure.
- Multi-level recovery: outer recovery (statement level) catches what inner recovery (item level) misses. Inner boundaries should be a subset of outer boundaries.

Use the JSON grammar from examples.md Example 4 with annotated walkthrough of broken input cases.

### H2: Error Messages

How to improve the error messages the parser produces.

- Default error messages list all expected token alternatives: `"'+', '-', '*', '/' expected"`.
- The `name` attribute replaces token lists with a descriptive name: `name(".*_expr")='expression'` produces `"<expression> expected"`.
- Pattern-based `name` applies to all matching rules.
- Empty `name=""` suppresses the short error message entirely.
- `consumeTokenMethod(".*_recover")="consumeTokenFast"` skips error reporting in recovery rules and expression operators for better performance.

Reference examples.md Example 7 and Example 8.

---

## Key Points Mapped to Evidence

| Point | Evidence Source |
|-------|---------------|
| Pin applies to sequence items, not choices | code-evidence "Basic Pin Contract" (pin.html) |
| Pin is 1-indexed | code-evidence "Pin Value Formats" (KnownAttribute.java:59) |
| `extendedPin` default true | code-evidence "ExtendedPin Mode" (extendedPin.html) |
| RecoverWhile contract: "regardless of result" | code-evidence "Basic RecoverWhile Contract" (recoverWhile.html) |
| Rule should be inside a loop | code-evidence "RecoverWhile Usage Rules" (recoverWhile.html) |
| Rule should have pin somewhere | code-evidence "RecoverWhile Usage Rules" (recoverWhile.html) |
| Recovery predicates must be private | code-evidence "Writing Recovery Predicates" (BnfUnusedRuleInspection) |
| `#auto` = `! FOLLOWS(rule)` | code-evidence "#auto Recovery" (recoverWhile.html) |
| Quick Documentation shows #auto expansion | code-evidence "#auto in Quick Documentation" (BnfDocumentationProvider) |
| Statement-level recovery pattern | code-evidence "Statement-Level Recovery Pattern" (HOWTO.md:88-93) |
| Property recovery pattern | code-evidence "Property/Assignment Recovery Pattern" (TUTORIAL.md:110-113) |
| Parenthesized list pattern | code-evidence "Parenthesized List Recovery Pattern" (pin.html, recoverWhile.html) |
| JSON `prop ::= []` trick | code-evidence "JSON Object Recovery Pattern" (Json.bnf:24) |
| Shared recover predicate | code-evidence "JSON Object Recovery Pattern" (Json.bnf:26) |
| `name` attribute changes error messages | code-evidence "Name Attribute" (name.html) |
| `consumeTokenFast` for recovery rules | code-evidence "consumeTokenMethod" (consumeTokenMethod.html) |
| Error message formats | code-evidence "Error Message Formats" (GeneratedParserUtilBase.java) |
| Trailing comma pattern | code-evidence "Trailing Comma Pattern" (HOWTO.md:386-395) |
| PSI tree with error elements | references.md "Recovery Test Results" (AutoRecovery.txt, JsonRecovery.txt) |

---

## Tone Guidance

- Practical and concrete. Every concept should be paired with a grammar snippet and a walk-through of what happens on broken input.
- PSI tree output for broken input is highly effective here. Show the tree structure alongside the input to demonstrate that recovery preserves nodes.
- Be direct about requirements: "Recovery predicates must be private." "The rule must have `pin` somewhere."
- Do not over-explain `extendedPin`. Mention it is true by default and should not be changed. One paragraph is enough.
- Use the step-by-step "what happens on this input" format for the pattern walkthroughs. This is the most concrete way to show how pin and recoverWhile interact.

---

## Cross-References

- **BNF Grammar Syntax** (`grammar-syntax.md`): predicate syntax (`!`, `&`), `<<eof>>` external, attribute syntax.
- **Grammar Design** (`grammar-design.md`): where recovery rules fit in grammar architecture, private vs. public decisions.
- **Expression Parsing** (`expression-parsing.md`): the `element` recovery wrapper for expression roots; `consumeTokenFast` for expression rules.
- **Attribute Reference** (Section 3.1): `pin`, `recoverWhile`, `extendedPin`, `name`, `consumeTokenMethod` with types and defaults.
- **Live Preview** (Section 2.5): testing recovery behavior interactively.
- **IDE Integration** (Section 5): pin marker highlighting, recover marker highlighting, Quick Documentation.

---

## What to Avoid (Scope Boundaries)

- Do NOT re-explain BNF syntax or rule modifiers -- that is Section 2.1.
- Do NOT cover grammar architecture decisions (when to use private, how to structure a grammar top-down) -- that is Section 2.2.
- Do NOT cover expression parsing mechanics (priority tables, `extends`, operator types) -- that is Section 2.3. Mention `consumeTokenFast` for expressions briefly.
- Do NOT catalog all attributes -- that is Section 3.1. Cover only `pin`, `recoverWhile`, `extendedPin`, `name`, and `consumeTokenMethod` as they directly relate to recovery.
- Do NOT cover the Live Preview workflow in detail -- that is Section 2.5. Mention it as a testing tool.
- Do NOT cover `parseAsTree` recovery or `DUMMY_BLOCK` internals -- these are implementation details not documented for users.
- Do NOT cover brace-aware recovery internals (parenCount tracking) -- undocumented implementation detail.
