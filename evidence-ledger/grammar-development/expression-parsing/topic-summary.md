# Topic Summary: Expression Parsing

## Target File
`docs/grammar-development/expression-parsing.md`

## Page Title
**Expression Parsing**

## Purpose
Explain how Grammar-Kit handles operator precedence and associativity in expression grammars. This is a key technical topic because expression parsing is where Grammar-Kit diverges most from textbook BNF: it supports left-recursive rules via a Pratt-style mechanism and auto-detects operator types. Readers arrive here when building a language with infix operators, and they need to understand both the recommended approach and how to handle complex patterns like ternary operators and function calls.

## Audience
Plugin developers implementing expression parsing in their language grammar. Assumes familiarity with BNF syntax (Section 2.1) and basic grammar design (Section 2.2). May know what operator precedence means conceptually but needs to learn Grammar-Kit's specific mechanism.

---

## Recommended Structure

### H1: Expression Parsing

Opening paragraph: Grammar-Kit provides a compact, Pratt-style mechanism for expression parsing that handles operator precedence and associativity through rule ordering and attributes. The generated parser rewrites left-recursive expression rules into an efficient iterative parser that produces a flat PSI tree. This page covers the recommended approach, how precedence and associativity work, and patterns for complex expression constructs.

Reference: HOWTO.md -- "a procedural rewrite of the Pratt parsing" and link to Crockford's TDOP paper.

### H2: How Expression Parsing Works

The fundamentals of Grammar-Kit's expression parsing mechanism.

#### H3: The Expression Root

- The expression root rule lists all expression alternatives as ordered choices.
- Grammar-Kit auto-detects expression roots by: left recursion + empty PSI children (ExprParser.bnf comment).
- Priority increases from top to bottom in the choice list (first alternative = lowest priority).
- Private rules group operators at the same priority level.
- The generator produces only two methods for the root: `expr()` and `expr_0()`.
- The `extends(".*_expr")=expr` attribute is required for AST flattening and for enabling the expression framework.

Show the expression root and priority groups from examples.md Example 1 (complete expression grammar). Show the generated priority table as a comment block.

#### H3: Operator Types

Grammar-Kit auto-detects five operator types from rule structure:

- **ATOM**: no reference to root expression rule (e.g., `literal_expr ::= number`).
- **PREFIX**: root expression reference after operator (e.g., `unary_min_expr ::= '-' expr`).
- **POSTFIX**: root expression reference before operator (e.g., `factorial_expr ::= expr '!'`).
- **BINARY**: two references to root expression rule (e.g., `plus_expr ::= expr '+' expr`).
- **N_ARY**: uses `(<op> expr)+` syntax (e.g., `exp_expr ::= expr ('**' expr) +`).

Note: `paren_expr ::= '(' expr ')'` is classified as PREFIX (not ATOM) because it does not start with `expr`.

Reference code-evidence "Operator Types" and the priority table from examples.md Example 2.

### H2: Precedence and Associativity

How to control operator binding.

#### H3: Defining Precedence

- Position in the root rule's choice list determines priority: first = lowest, last = highest.
- Private groups: `private mul_group ::= mul_expr | div_expr` -- all operators in a group share the same priority.
- Walk through a concrete example: `1 + 2 * 3` parses as `1 + (2 * 3)` because `mul_expr` has higher priority than `plus_expr`.

Use examples.md Example 2 (operator precedence table) as the reference.

#### H3: Associativity

- Left associativity is the default: `a + b + c` parses as `(a + b) + c`.
- Right associativity via `rightAssociative=true`: `a = b = c` parses as `a = (b = c)`.
- The attribute is per-rule, allowing different operators to have different associativity.
- No explicit non-associativity attribute; comparison operators at the same priority level approximate non-associative behavior (they parse left-associatively).

Use examples.md Example 5 (right associativity) and Example 9 (associativity comparison with parse trees).

### H2: Complex Expression Patterns

Patterns beyond simple binary and unary operators.

#### H3: Ternary and Multi-Token Operators

- Ternary: `elvis_expr ::= expr '?' expr ':' expr` -- treated as BINARY with a tail.
- Multi-token operators: `is_not_expr ::= expr IS NOT expr`.
- Choice operators: `conditional_expr ::= expr ('<' | '>' | '<=' | '>=') expr`.
- The operator part can contain any valid BNF expression.

Reference examples.md Example 6 (complex expression patterns).

#### H3: Function Calls and Qualification

- Function call as postfix: `call_expr ::= ref_expr arg_list` -- uses type-constrained left operand.
- Qualification: `qualification_expr ::= expr '.' identifier`.
- Fake rules for PSI unification: `fake ref_expr ::= expr? '.' identifier` with `elementType=ref_expr` on concrete rules.
- The `elementType` attribute maps multiple rules to a single PSI type.

Reference examples.md Example 6 (call_expr, qualification_expr).

#### H3: Narrowing Operand Types

- Use a specific expression rule or private group instead of generic `expr` to restrict what operands are accepted.
- Example: `between_expr ::= expr BETWEEN add_group AND add_group` -- restricts operands to add-level priority and above.
- The generated code passes the priority of the referenced group.

Reference code-evidence "Narrowing Parse to Specific Expression Rules."

#### H3: Multiple Expression Roots

- A grammar can have multiple independent expression hierarchies.
- Constraint: hierarchies must not intersect (no rule in both).
- `extraRoot=true` attribute marks an additional expression root.
- Each root generates its own pair of methods.

Reference examples.md Example 8.

### H2: PSI Tree Shape and Performance

Practical considerations for the generated output.

- **Flat vs. deep PSI tree**: without `extends`, the AST has redundant wrapping nodes. With `extends`, nodes collapse. Show the side-by-side comparison from examples.md Example 3.
- **`consumeTokenMethod(".*_expr|expr")="consumeTokenFast"`**: skips error reporting in expression rules for better performance. "No one really needs to know that + - * / are expected at any offset."
- **`name(".*_expr")='expression'`**: cleans up error messages from token lists to `<expression> expected`.
- **Quick Documentation**: Ctrl-Q / Cmd-J on expression rules shows the priority table with operator types and the current rule highlighted. Useful for verifying precedence.

Mention the traditional approach (manual `left` modifier layering) briefly, noting it is more verbose and the Pratt approach is recommended for new grammars. Reference examples.md Example 4 for anyone maintaining legacy grammars.

---

## Key Points Mapped to Evidence

| Point | Evidence Source |
|-------|---------------|
| Pratt-style mechanism, "procedural rewrite of Pratt parsing" | code-evidence "Two Approaches" (HOWTO.md:199) |
| Only 2 methods generated for root | code-evidence "Pratt/Priority-Based Approach" (HOWTO.md:201) |
| Five operator types: ATOM, PREFIX, POSTFIX, BINARY, N_ARY | code-evidence "Operator Types" (ExpressionHelper.OperatorType) |
| Priority increases top to bottom | code-evidence "Root Rule Structure" (HOWTO.md:131) |
| Private groups share priority | code-evidence "Private Priority Groups" |
| `rightAssociative=true` for right associativity | code-evidence "Right Associativity" (ExprParser.bnf:58) |
| No explicit non-associativity attribute | code-evidence "Non-Associative Operators" |
| `extends` collapses redundant AST nodes | code-evidence "The extends Attribute" (extends.html) |
| Root expression rule never appears in AST | code-evidence "Expression Optimization" (HOWTO.md:130) |
| `paren_expr` classified as PREFIX | code-evidence (HOWTO.md priority table line 213) |
| Ternary treated as BINARY with tail | code-evidence "Ternary Operators" |
| `call_expr` uses type-constrained left operand | code-evidence "Function Calls as Postfix" |
| `between_expr` narrows operand types | code-evidence "Narrowing Parse to Specific Expression Rules" |
| `extraRoot=true` for multiple expression roots | code-evidence "Multiple Expression Roots" (ExprParser.bnf:37) |
| `consumeTokenFast` for expression performance | code-evidence "consumeTokenMethod" (consumeTokenMethod.html) |
| Quick Documentation priority table | code-evidence "IDE Feature" (BnfDocumentationProvider) |
| Traditional approach with `left` modifier | code-evidence "Traditional Layer-Based Approach" |
| Expression root auto-detection | code-evidence "Expression Root Detection" (ExprParser.bnf:25) |

---

## Tone Guidance

- Technical but grounded in practical examples. Every concept should be illustrated with a concrete grammar snippet and, where helpful, a parse tree showing the result.
- Use the ExprParser.bnf grammar as the running example throughout the page. It contains all operator types and is the canonical reference.
- Avoid abstract parser theory. Explain Pratt parsing only enough for readers to understand why they write rules the way they do.
- Be direct about the recommended approach (Pratt/priority) vs. the traditional approach (manual `left` layering). Do not present them as equal alternatives; the Pratt approach is clearly preferred for new grammars.
- Parse tree diagrams (text-based) are valuable for showing precedence and associativity effects.

---

## Cross-References

- **BNF Grammar Syntax** (`grammar-syntax.md`): `left`, `fake`, `extends` modifier definitions; `<<param>>` and meta rule syntax.
- **Grammar Design** (`grammar-design.md`): when to use `private` groups, `extends` for PSI hierarchy, pattern-based attributes.
- **Error Recovery** (`error-recovery.md`): wrapping expressions in a loop with recovery (the `element` pattern at the top of the expression grammar).
- **Attribute Reference** (Section 3.1): `rightAssociative`, `extends`, `extraRoot`, `consumeTokenMethod`, `name`, `elementType`.
- **PSI Customization** (Section 3.4): `fake` rules for PSI interfaces, `mixin`, `implements`, `methods`.

---

## What to Avoid (Scope Boundaries)

- Do NOT re-explain BNF syntax constructs (sequences, choices, quantifiers, predicates) -- that is Section 2.1.
- Do NOT cover `pin` and `recoverWhile` mechanics in depth -- that is Section 2.4. Mention the `element` recovery wrapper briefly.
- Do NOT cover PSI class customization (`mixin`, `implements`, `methods`, `stubClass`) -- that is Section 3.x. Mention `fake` rules and `elementType` only in the context of expression PSI unification.
- Do NOT cover the full attribute catalog -- that is Section 3.1.
- Do NOT provide a tutorial-style walkthrough of building an expression grammar from scratch. The examples should be reference-oriented, showing the complete pattern and explaining how it works.
- Do NOT cover the `upper` modifier (rare, minimal documentation, not expression-related).
