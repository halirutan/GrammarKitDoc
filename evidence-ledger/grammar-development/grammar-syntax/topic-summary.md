# Topic Summary: BNF Grammar Syntax

## Target File
`docs/grammar-development/grammar-syntax.md`

## Page Title
**BNF Grammar Syntax**

## Purpose
Core syntax reference for Grammar-Kit's `.bnf` file format. Readers arrive here to look up specific syntax constructs, understand how grammar files are structured, or verify the correct form for tokens, rules, and modifiers. The page should be comprehensive but scannable, structured so readers can jump to the section they need.

## Audience
Plugin developers writing or reading `.bnf` grammars. Assumes basic familiarity with BNF notation and parsing concepts. Does not assume prior Grammar-Kit experience.

---

## Recommended Structure

### H1: BNF Grammar Syntax

Opening paragraph: Grammar-Kit uses a PEG-based BNF dialect. Briefly state that `.bnf` files contain an optional attributes block followed by rule definitions, and that the `::=` operator defines rules. Mention PEG ordered-choice semantics (first match wins) and link to the PEG Wikipedia article.

### H2: File Structure

Explain the overall layout of a `.bnf` file.

- **Global attributes block**: `{ }` at the top containing `name=value` pairs. Mention `tokens=[...]` as the most common content. Reference code-evidence "Header / Global Attributes Block."
- **Rules**: `rule_name ::= expression` form. Note the optional trailing `;`. Reference code-evidence "Rule Definition Syntax."
- **Comments**: `//` line comments and `/* */` block comments.
- **Grammar sections**: `;{` separator for splitting into multiple parser classes. Keep brief; this is an advanced feature. Reference code-evidence "Semicolon as Section Separator" and examples.md Example 8.
- **First rule**: Implicitly private (the grammar root). Reference code-evidence line about `HOWTO.md` line 232.

Use the minimal grammar from examples.md Example 1 as the primary code sample.

### H2: Tokens

Cover token declarations and token references in rules.

#### H3: Declaring Tokens

- `tokens=[...]` attribute with `TOKEN_NAME='value'` entries.
- Three forms: name with string value (`SEMI=';'`), name with regexp value (`id='regexp:\w+'`), and name-only (`IDENTIFIER`).
- Single and double quotes are interchangeable.
- `regexp:` prefix for regular expression patterns. Note that regexp tokens are required for Live Preview.
- Whitespace/comment auto-detection in Live Preview: space-matching regexp tokens not used in rules become whitespace; tokens named ending in "comment" become comments.

Reference code-evidence "Token Forms" and examples.md Example 2.

#### H3: Referencing Tokens in Rules

- By value (quoted): `'+'` -- recommended for readability.
- By name (unquoted): `PLUS`.
- Implicit tokens (undeclared): unquoted keywords where name equals value; quoted text-matched tokens (slower).
- When to use names vs. values: names resolve conflicts when an unquoted value matches a rule name.

Reference code-evidence "Token Reference in Rules" and "Token Precedence and Conflicts."

### H2: Rules and Expressions

Core syntax constructs for writing rules. This is the longest section.

#### H3: Sequences, Choices, and Quantifiers

- Sequences: items separated by whitespace, matched left to right.
- Ordered choice (`|`): first match wins (PEG semantics).
- Quantifiers: `?` (optional), `+` (one or more), `*` (zero or more), applied as postfix.
- Grouping: `( )` for grouping, `[ ]` as shorthand for `( )?`, `{ | }` as alternative choice syntax.

Use examples.md Example 3 as the primary code sample.

#### H3: Predicates

- And-predicate `&expr`: positive lookahead, consumes nothing.
- Not-predicate `!expr`: negative lookahead, consumes nothing.
- Common pattern: `!<<eof>>` guard against infinite loops.
- Edge cases: `&()` always true, `!()` always false (mention briefly).

Use examples.md Example 4 as the primary code sample.

#### H3: Rule Modifiers

- Table or compact prose covering all seven modifiers: `private`, `left`, `inner`, `upper`, `meta`, `external`, `fake`.
- Placement: before the rule name, multiple can combine.
- Key combinations: `inner` only with `left`; `private left` equals `private left inner`; `fake` not with `private`.
- Brief descriptions of each modifier's effect. Do not deeply explain `meta`/`external` (they get their own subsections below) or `left`/`extends` expression patterns (covered in Section 2.3).

Reference code-evidence "Rule Modifiers" and examples.md Example 5.

### H2: Advanced Constructs

Group the more specialized syntax features.

#### H3: External Expressions and Rules

- `<<methodName arg1 arg2>>` inline syntax.
- `external rule_name ::= methodName param1 param2` declaration form.
- `<<eof>>` built-in external.
- Parameter passing: double-quoted strings passed as-is, single-quoted strings unquoted first, rule references passed as `Parser` instances.
- Method signature requirement: `public static boolean method(PsiBuilder, int, ...)`.

Use examples.md Example 6 (including the Java implementation snippet).

#### H3: Meta Rules

- `meta rule_name ::= <<param>> (',' <<param>>) *` pattern.
- Parameters referenced with `<<param_name>>` in body.
- Invocation: `<<meta_rule arg>>`.
- Arguments: rule references, `(choice)`, `[optional]`, `{alt_choice}`.
- Nested meta calls.
- Highlight the `comma_list` pattern as the most common use case.

Use examples.md Example 7.

#### H3: Attributes (Syntax Overview)

- Global attributes: `{ name=value }` at top of file or after `;` separator.
- Rule-level attributes: `{ name=value }` after rule expression.
- Pattern-based attributes: `name("regex")=value` applied to matching rule names.
- List values: `name=[item1 item2]`.
- Do NOT catalog all attributes here -- cross-reference to the Attribute Reference page (Section 3.1).

Use examples.md Example 9.

---

## Key Points Mapped to Evidence

| Point | Evidence Source |
|-------|---------------|
| PEG semantics, `::=` replaces PEG `<-` | code-evidence "PEG Foundation" |
| `.bnf` file extension registered | code-evidence "File Extension" (BnfFileType.java) |
| First rule implicitly private | code-evidence "Basic Rule Structure" (HOWTO.md:232) |
| Token forms (name=value, regexp, name-only) | code-evidence "Token Forms"; examples.md Example 2 |
| Regexp tokens required for Live Preview | code-evidence "Regexp tokens" (tokens.html) |
| Token value recommended over name | code-evidence "By value" (README.md:177) |
| Seven rule modifiers | code-evidence "Available Modifiers" (Grammar.bnf:66-67) |
| `private left` = `private left inner` | code-evidence "Modifier Combinations" (README.md:143-147) |
| External expression syntax `<< >>` | code-evidence "External Expressions" (Grammar.bnf:114) |
| Meta rule `<<param>>` syntax | code-evidence "Meta Rules" (README.md:149-157) |
| `;{` section separators | code-evidence "Semicolon-Separated Grammar Sections" |
| Pattern-based attributes | code-evidence "Global Pattern-Based Attributes" (README.md:122-129) |
| Empty rules and predicates as edge cases | code-evidence "Empty Rules," "Empty Predicate Expressions" (Small.bnf) |

---

## Tone Guidance

- Reference style: clear, direct, scannable. This is the page readers will return to repeatedly.
- Use short code snippets inline with explanations. Avoid long narrative blocks.
- Define terms on first use (PEG, predicate, quantifier) but keep definitions brief.
- Use tables where comparing options (e.g., token forms, modifier effects).
- Imperative mood for guidance ("Use token values for readability").

---

## Cross-References

- **Grammar Design** (`grammar-design.md`): patterns for structuring grammars, when to use `private`, naming conventions.
- **Expression Parsing** (`expression-parsing.md`): how `left`, `extends`, and priority groups work for expressions.
- **Error Recovery** (`error-recovery.md`): `pin` and `recoverWhile` attributes that appear in rule syntax.
- **Attribute Reference** (Section 3.1): full catalog of all 38+ attributes with types and defaults.
- **Live Preview** (Section 2.5): testing grammars with regexp tokens.
- **Getting Started / Quick Start**: links back here for syntax details.

---

## What to Avoid (Scope Boundaries)

- Do NOT cover grammar design patterns or when to choose `private` vs. public (that belongs in Section 2.2).
- Do NOT deeply explain expression parsing, `extends` for AST flattening, or priority tables (Section 2.3).
- Do NOT explain `pin`/`recoverWhile` mechanics or error recovery strategies (Section 2.4).
- Do NOT catalog all attributes with types, defaults, and effects (Section 3.1). Only cover attribute *syntax* (how to write them).
- Do NOT cover JFlex or lexer generation.
- Do NOT cover generated code structure or PSI class details.
- Keep the JSON grammar example brief if used; a full walkthrough belongs in Section 2.2.
