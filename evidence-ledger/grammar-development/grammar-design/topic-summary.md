# Topic Summary: Designing Grammar Rules

## Target File
`docs/grammar-development/grammar-design.md`

## Page Title
**Designing Grammar Rules**

## Purpose
Design-focused guide for structuring Grammar-Kit grammars effectively. Readers arrive here after learning the syntax (Section 2.1) and need to understand how to organize rules, decide what appears in the PSI tree, apply common patterns, and avoid pitfalls. The emphasis is on architectural decisions and practical patterns rather than syntax mechanics.

## Audience
Plugin developers building or maintaining a `.bnf` grammar. Assumes the reader knows BNF syntax from Section 2.1. May be read sequentially by someone building their first grammar, or consulted by an experienced developer looking for specific patterns.

---

## Recommended Structure

### H1: Designing Grammar Rules

Opening paragraph: Writing syntactically correct BNF is only the first step. A working parser requires deliberate decisions about rule organization, PSI tree shape, and error handling hooks. This page covers the architectural principles, common patterns, and pitfalls that turn a raw grammar into a robust parser.

Reference: HOWTO.md opening -- "Writing a grammar doesn't mean the generated parser will work. The tricky part is to *tune* some raw grammar into a *working* grammar."

### H2: Grammar Architecture

How to structure a grammar top-down, and the key decisions that shape the generated parser and PSI tree.

#### H3: Top-Down Structure

- The first rule is the grammar root (implicitly private, no PSI node).
- Root rule typically delegates to a private helper with a loop: `root ::= item *`.
- The `!<<eof>>` guard on loop items prevents infinite loops.
- Each public rule produces one PSI node and one `IElementType` constant.
- Private rules are structural helpers: no PSI node, children merge into parent.

Use the well-structured grammar template from examples.md Example 1 as the primary illustration. Annotate the sections (attributes, root, dispatch, public rules, recovery).

#### H3: Choosing Private vs. Public

- Default is public. Use `private` when the rule is structural plumbing that should not appear in the PSI tree.
- Common private uses: root loop items, dispatch/choice rules, recovery predicates, operator grouping.
- HOWTO guidance: "Specify *private* attribute on any rule if you don't want it to be present in AST as early as possible."
- Anti-pattern: public helper rules that create unnecessary PSI nodes (examples.md Example 4, Anti-Pattern 2).

#### H3: Flattening with `extends`

- Without `extends`: deep AST nesting (e.g., `FileNode/Expr/AddExpr/MulExpr/LiteralExpr`).
- With `extends(".*_expr")=expr`: flat AST (`FileNode/LiteralExpr`).
- Root expression rule never appears in AST when extending rules collapse nodes.
- Brief explanation here; full expression parsing coverage in Section 2.3.

Use examples.md Example 3 (before/after refactoring) as the illustration.

### H2: Common Patterns

Practical, reusable grammar patterns that readers can adapt.

#### H3: Lists and Separators

- Comma-separated list: `<<param>> (',' <<param>>) *` via meta rule.
- Parenthesized list with recovery: `list ::= '(' [!')' item (',' item) *] ')' {pin(".*")=1}`.
- Trailing comma support: `(',' (element | &')'))` pattern.
- `#auto` recovery on list items as an alternative to manual predicates.

Show the meta `comma_list` pattern and the parenthesized list pattern from examples.md Example 2. Keep recovery details brief (link to Section 2.4).

#### H3: Declarations and Blocks

- Property/assignment pattern: `property ::= id '=' expr {pin=2}`.
- Block structure: `block ::= '{' statement * '}' {pin=1}`.
- Pin on the operator or opening delimiter commits the node early.
- Nested structures: lookahead negation `!'}'` prevents consuming closing delimiters.

Reference examples.md Example 2 (Declaration with Pin, Block Structure).

#### H3: Statement-Level Design

- Root loop with recovery: `script ::= script_item *` with private loop item.
- Private dispatch rule for statement alternatives.
- Each concrete statement pinned at its keyword.
- `extends(".*_statement")=statement` for PSI hierarchy.
- Pattern-based pin: `pin("create_.*")=2`.

Use examples.md Example 5 (statement-level grammar) as the primary illustration.

### H2: Reducing Repetition

How pattern-based attributes and meta rules reduce boilerplate and improve maintainability.

- Pattern-based attributes: `extends(".*_expr")=expr`, `pin(".*_list")=1`, `name(".*_expr")='expression'`.
- Before/after comparison showing verbose per-rule attributes vs. single pattern attribute.
- Meta rules for reusable structural patterns (comma_list, paren_list).
- Grammar sections via `;{ parserClass="..." }` for large grammars.

Use examples.md Example 3 (before/after pattern attributes) and Example 7 (splitting grammar).

### H2: Pitfalls and Inspections

Common mistakes and the IDE features that catch them.

- **Left recursion**: causes `StackOverflowError` in recursive descent. Exception: expression parsing with `extends` handles it. Fix: refactor to iterative form or use expression framework. Detected by `BnfLeftRecursion` inspection.
- **Unreachable choice branches**: a branch preceded by one that matches empty is never reached. Detected by `BnfUnreachableChoiceBranch`.
- **Public recovery predicates**: recovery rules should always be `private`. Inspection warns: "Non-private recovery rule."
- **Missing pin with recoverWhile**: recovery runs but the rule never commits. The rule or its sub-rules need `pin` somewhere.
- **Rule name conflicts**: avoid naming rules like `rule_name_0` (conflicts with generated sub-expression methods).
- **Token conflicts**: text-matched tokens are slower; prefer declared tokens. Inspection: `BnfSuspiciousToken`.

Use examples.md Example 4 (anti-patterns and fixes). Keep each pitfall to 2-3 sentences + fix.

Mention IDE inspections as a group: left recursion, unused rules, duplicate rules, unresolved references, identical/unreachable choice branches, suspicious tokens.

---

## Key Points Mapped to Evidence

| Point | Evidence Source |
|-------|---------------|
| First rule implicitly private | code-evidence "Top-Down Design" (RuleGraphHelper.java:827-828) |
| Each public rule = one PSI node | code-evidence "Identifying Language Constructs" (README.md:133) |
| `private` early as possible | code-evidence "Best Practices" (HOWTO.md:232) |
| `extends` flattens AST | code-evidence "Rule Granularity" (HOWTO.md:233-237) |
| Comma-separated list meta pattern | code-evidence "Lists and Separators" (ExternalRules.bnf:38) |
| Parenthesized list with pin + recovery | code-evidence "Lists and Separators" (AutoRecovery.bnf) |
| Trailing comma pattern | code-evidence "Lists and Separators" (HOWTO.md:394) |
| Statement recovery pattern | code-evidence "Statement vs Expression Distinction" (HOWTO.md:88-93) |
| Left recursion inspection | code-evidence "Left Recursion Issues" |
| Unreachable branch inspection | code-evidence "Ambiguous Grammars" |
| Pattern-based attributes | code-evidence "Maintainability Patterns" (README.md:122-128) |
| Grammar sections for large grammars | code-evidence "Separation of Concerns" |
| `consumeTokenFast` for performance | code-evidence "Performance Considerations" |
| Rule name conflict warning | code-evidence "Grammar Complexity" (README.md:120) |
| IDE inspections list | code-evidence "Inspections" |

---

## Tone Guidance

- Practical and prescriptive. Use "do this" and "avoid that" framing where appropriate.
- Lead with the pattern, then explain why it works. Readers are building, not studying theory.
- Before/after examples are effective for showing improvements.
- Keep recovery details shallow here; direct readers to Section 2.4 for mechanics.
- Do not lecture about PEG theory. Mention ordered-choice semantics only where it directly affects a design decision (e.g., branch ordering).

---

## Cross-References

- **BNF Grammar Syntax** (`grammar-syntax.md`): syntax details for constructs referenced here (tokens, modifiers, predicates).
- **Expression Parsing** (`expression-parsing.md`): full coverage of `extends`-based expression hierarchies, priority tables, associativity.
- **Error Recovery** (`error-recovery.md`): `pin` and `recoverWhile` mechanics, recovery predicate design.
- **Attribute Reference** (Section 3.1): full catalog of attributes mentioned here (`extends`, `pin`, `name`, `consumeTokenMethod`).
- **Live Preview** (Section 2.5): testing grammar designs interactively.
- **IDE Integration** (Section 5): inspections, refactorings, Quick Documentation.

---

## What to Avoid (Scope Boundaries)

- Do NOT re-explain BNF syntax fundamentals (sequences, choices, quantifiers) -- that is Section 2.1.
- Do NOT cover expression parsing in depth (priority tables, associativity, operator types) -- that is Section 2.3.
- Do NOT explain `pin` and `recoverWhile` mechanics (how pin values work, what `#auto` computes) -- that is Section 2.4. Mention them only as part of patterns.
- Do NOT catalog attributes with types and defaults -- that is Section 3.1.
- Do NOT cover generated code structure, PSI class customization, or `mixin`/`implements` -- that is Section 3.x.
- Do NOT cover JFlex, lexer generation, or build integration.
- Do NOT turn this into a tutorial. Assume the reader has already completed the Getting Started section.
