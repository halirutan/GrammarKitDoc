# Common Issues

This page catalogs the warnings, errors, and problems you are most likely to encounter when developing with Grammar-Kit, along with their causes and fixes.

## Grammar Inspections

Grammar-Kit includes several built-in inspections that flag problems in your `.bnf` file before you generate code. These run automatically in the editor and appear as highlights.

### Left Recursion

A rule that directly or indirectly references itself as the first element of its body triggers the error:

> "'rule_name' employs left-recursion unsupported by generator"

Grammar-Kit's recursive-descent parser cannot handle left recursion because it would loop indefinitely. The fix depends on the situation. If the rule represents an expression with operator precedence, restructure it as an expression grammar using the `extends` attribute. Grammar-Kit's Pratt-style expression parser handles left recursion internally. For non-expression rules, factor out the left-recursive part into a separate rule or use iteration (`*`, `+`).

!!! note
    The left-recursion inspection excludes expression-parsing rules that are already configured for Pratt parsing. If your rule is inside an expression group and still triggers this warning, check that the `extends` chain is set up correctly.

### Unresolved References

Grammar-Kit detects four types of unresolved references:

- "Unresolved rule reference": a rule name in an attribute value does not match any defined rule.
- "Unresolved rule or method reference": an external reference (`<<name>>`) does not resolve to a rule or a method.
- "Unresolved method reference": an entry in the `methods` attribute list does not match a generated or utility method.
- "Pattern does not match any rule": a pattern in a pattern-based attribute does not match any rule name.

Check spelling first. For external references, verify that your `parserUtilClass` contains the referenced method with the correct signature. For method references, regenerate the parser after adding utility methods.

### Suspicious Tokens

When a token in a rule body looks like it might be a mistyped rule name, Grammar-Kit shows:

> "'text' token looks like a reference to a missing rule"

A token is flagged as suspicious when it is mixed-case (not all-lowercase and not all-uppercase), or when it is all-lowercase but contains `-` or `_`. The quick fix "Create rule" generates a stub rule definition for the token.

If the token is intentional (you really do mean a literal token, not a rule reference), you can suppress the warning or add it to your token definitions.

### Unused and Unreachable Rules

Grammar-Kit traces reachability from the root rule and any extra roots to find rules that serve no purpose. The inspection reports five categories:

- "Unused rule": not referenced from any rule expression.
- "Unreachable rule": referenced somewhere but not reachable from any root.
- "Unused fake rule": a fake rule that is not referenced in expressions or attributes.
- "Reachable fake rule": a fake rule that appears in a rule body (likely a mistake, since fake rules are meant for PSI hierarchy only).
- "Non-private recovery rule": a recovery rule (used with `recoverWhile`) that should be marked `private` to avoid generating an unnecessary PSI element.

To fix these, either remove the rule, connect it to the grammar's reachable tree, or add it to `extraRoot` if it represents an independent entry point.

### Duplicate and Redundant Rules

Two inspections catch structural redundancy:

- Duplicate rules (same name defined more than once) cause generation errors. Remove the duplicate.
- Identical choice branches (`a | b | a`) waste parser time on alternatives that are already covered. Remove the duplicate branch.

### Unreachable Choice Branches

When an earlier alternative in a choice expression matches everything that a later alternative could match, the later branch never executes. Grammar-Kit detects this and flags the unreachable branch. Reorder the alternatives so that more specific branches appear first, or remove branches that are subsumed by earlier ones.

## Token and Lexer Issues

### Text-Matched Tokens

The grammar annotator warns:

> "Tokens matched by text are slower than tokens matched by types"

This appears when a quoted string in a rule body is not found in the token name-to-text mapping. Text-based matching compares characters at parse time, while type-based matching compares a single integer. To fix this, add an entry in your `tokens` section that maps a token name to the quoted string:

```bnf
{
  tokens=[
    PLUS='+'
    MINUS='-'
  ]
}
```

Then reference the token name instead of the quoted string in your rules.

## Suppressing Inspections

You can suppress any Grammar-Kit inspection for a specific rule using a comment directly above it:

```bnf
//noinspection BnfUnusedRule
private helper_rule ::= some_content
```

This works the same way as IntelliJ's standard inspection suppression comments. Use it sparingly; an inspection usually points to a real problem.

## Historical Issues

Some issues were caused by bugs in earlier Grammar-Kit versions that have since been fixed. If you encounter behavior that matches one of these patterns, check that you are running a current version:

- Endless cycle on cyclic inheritance (#234), fixed in 2020.1
- Left rule with several usages incorrectly detected as recursive, fixed in 2017.1.6
- Missing generated files on cold start, fixed in 1.0.9
- NPE with `exact-types` combined with factory methods (#286), fixed in 2021.1.2
- Incorrect method spec warning (#252), fixed in 2020.3.1

For version-specific changes, see the [Migration Guide](migration.md). For techniques to investigate grammar and parser behavior, see [Debugging Techniques](debugging.md).
