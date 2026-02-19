# Examples: BNF Grammar Syntax

## Example 1: Minimal Grammar File Structure

Shows the basic structure of a `.bnf` file: global attributes, token declarations, and rules.

```bnf
// Global attributes block
{
  parserClass="com.example.MyParser"
  tokens=[
    SEMI=';'
    EQ='='
    LP='('
    RP=')'
    space='regexp:\s+'
    id='regexp:\p{Alpha}\w*'
    number='regexp:\d+'
  ]
}

// First rule is implicitly private (grammar root)
root ::= statement *

// Public rule — generates PSI node and IElementType
statement ::= id '=' number ';'
```

**Key points:**
- The `{ }` block at the top contains global attributes.
- `tokens=[...]` declares token names and values.
- `regexp:` prefix marks regular expression tokens (required for Live Preview).
- The first rule (`root`) is implicitly private — no PSI node is generated for it.
- `statement` is a public rule that generates a PSI class and IElementType constant.

Source: based on TUTORIAL.md lines 84-127, Grammar.bnf structure.

---

## Example 2: Token Definition Variants

Demonstrates the three forms of token declarations and how tokens are referenced in rules.

```bnf
{
  tokens=[
    // Named tokens with string values
    PLUS='+'
    MINUS='-'
    OP_EQ="="                    // double quotes work the same as single quotes

    // Regexp tokens (required for Live Preview)
    id='regexp:\p{Alpha}\w*'
    number="regexp:\d+(\.\d*)?"
    string="regexp:('([^'\\]|\\.)*'|\"([^\"\\]|\\.)*\")"

    // Whitespace/comment tokens (auto-detected in Live Preview)
    space='regexp:\s+'           // matches whitespace — treated as whitespace in Live Preview
    comment='regexp://.*'        // name ends with "comment" — treated as comment in Live Preview

    // Name-only token (no value or pattern)
    IDENTIFIER
  ]
}

// Reference tokens by value (recommended for readability)
addition ::= number '+' number

// Reference tokens by name (resolves conflicts)
assignment ::= id OP_EQ number

// Implicit tokens (not declared in tokens block)
// Unquoted implicit tokens: name equals value
create_statement ::= CREATE TABLE id    // CREATE and TABLE are keyword tokens

// Quoted implicit tokens: matched by text (slower)
special ::= 'begin' id 'end'            // matched by text, not IElementType
```

**Key points:**
- Three token forms: name=value, name=regexp, name-only.
- Token values in single or double quotes are interchangeable.
- Whitespace/comment tokens in Live Preview are auto-detected by pattern and name.
- Use values (`'+'`) over names (`PLUS`) for readability; use names to resolve conflicts.
- Text-matched (quoted implicit) tokens are slower because they match by text, not by IElementType.

Source: Grammar.bnf lines 22-47, tokens.html, README.md lines 172-185, TUTORIAL.md lines 79-81.

---

## Example 3: Rule Syntax Fundamentals

Demonstrates sequences, choices, quantifiers, grouping, and optional expressions.

```bnf
// Sequence: items separated by whitespace, all must match
import_statement ::= 'import' qualified_name ';'

// Ordered choice: alternatives separated by |, first match wins (PEG semantics)
literal ::= number | string | 'true' | 'false' | 'null'

// Quantifiers
argument_list ::= argument *              // zero or more
statements ::= statement +                // one or more
type_annotation ::= type_ref?             // zero or one (optional)

// Grouping with parentheses
repeated_pair ::= (id '=' number) *       // repeat the grouped sequence

// Optional with brackets: [expr] is shorthand for (expr)?
field_decl ::= type_ref id ['=' expr] ';'

// Choice with braces: { | | } alternative syntax for ( | | )
value ::= { number | string | 'null' }

// Combining constructs
param_list ::= '(' [!')' param (',' param) *] ')'
```

**Key points:**
- Sequences match left to right; all items must succeed.
- Ordered choice tries alternatives in order; first match wins (PEG, not ambiguous).
- `[expr]` is equivalent to `(expr)?` — both mean "optional."
- `{ a | b | c }` is equivalent to `( a | b | c )` — alternative grouping syntax.
- Quantifiers (`?`, `+`, `*`) apply as postfix to any expression.

Source: Grammar.bnf lines 94-121, README.md lines 92-96.

---

## Example 4: Predicates

Demonstrates and-predicates (`&`) and not-predicates (`!`) for lookahead without consuming input.

```bnf
// Not-predicate: succeeds if expression does NOT match, consumes nothing
// Common use: prevent consuming a closing delimiter
array ::= '[' [!']' item (',' item) *] ']'

// And-predicate: succeeds if expression matches, consumes nothing
// Common use: require a specific token ahead before committing
guarded_rule ::= &'class' class_declaration

// Combining predicates
statement ::= &required_keyword !forbidden_keyword rest_of_statement

// Recovery predicate — the most common use of not-predicates
private statement_recover ::= !(';' | 'class' | 'function')

// Not-at-end-of-file guard (built-in <<eof>>)
private root_item ::= !<<eof>> property ';'

// Edge cases: empty predicates
private always_true ::= &()    // and-predicate on empty always succeeds
private always_false ::= !()   // not-predicate on empty always fails
```

**Key points:**
- Predicates test the input without consuming any tokens.
- `!expr` is negative lookahead — succeeds when `expr` does NOT match.
- `&expr` is positive lookahead — succeeds when `expr` matches.
- Recovery predicates are always NOT predicates listing boundary tokens.
- `!<<eof>>` is a common guard to prevent infinite loops at end of input.
- `&()` and `!()` are valid edge cases (Small.bnf lines 22-23).

Source: Grammar.bnf lines 106-107, README.md line 95, Small.bnf lines 22-23.

---

## Example 5: Rule Modifiers

Demonstrates all seven rule modifiers and their combinations.

```bnf
// private: no PSI node — children merge into parent
private primary ::= literal_expr | ref_expr | paren_expr

// left: takes previous sibling and wraps it (becomes its parent)
// Used for binary operators in traditional expression parsing
left plus_expr ::= ('+' | '-') factor

// inner left: takes previous sibling and injects into it (becomes its child)
left inner leech ::= id

// private left: equivalent to private left inner
private left leech2 ::= id

// upper: takes parent node and replaces it, adopting all children
upper abc_one ::= just_b X {pin=1}

// meta: parametrized rule, accepts parse functions as arguments
meta comma_list ::= <<param>> (',' <<param>>) *

// external: hand-written parse function, no code generated
external my_rule ::= parseMyRule param1 param2

// fake: only PSI classes generated, no parsing code
fake ref_expr ::= expr? '.' identifier

// Combining modifiers
private left inner tail ::= id     // private + left + inner
```

**Key points:**
- Modifiers appear before the rule name.
- Multiple modifiers can be combined: `private left inner`.
- `inner` should only be used with `left`.
- `private left` is equivalent to `private left inner`.
- `fake` should not be combined with `private`.
- By default, rules are public (no modifiers).

Source: Grammar.bnf lines 65-67, README.md lines 131-147, LeftAssociative.bnf, UpperRules.bnf.

---

## Example 6: External Rules and External Expressions

Demonstrates external rule declarations, inline external expressions, and parameter passing.

```bnf
{
  parserUtilClass="com.example.MyParserUtil"
  parserImports=["static com.example.ManualParsing.*"]
}

// External rule: hand-written parse function
external my_rule ::= parseMyRule false 10

// Using the external rule in another rule
content ::= header my_rule footer

// Inline external expression (equivalent to external rule but inline)
content2 ::= header <<parseMyRule true 5>> footer

// Built-in external: <<eof>> tests end of input
private root_item ::= !<<eof>> statement ';'

// Empty external expression (valid)
private empty_ext ::= <<>>

// Parameter passing in external expressions
// Double-quoted strings passed "as is": "1+1" passes the string 1+1
// Single-quoted strings are unquoted: '1+1' passes 1+1
// Rule references passed as Parser instances
external parameterized_rule ::= parseIt "qualified.Enum.VALUE" '1+1' some_rule
```

The corresponding Java implementation:

```java
public class MyParserUtil {
  // Required signature: PsiBuilder, int level, then extra parameters
  public static boolean parseMyRule(PsiBuilder builder, int level,
                                    boolean extraArg1, int extraArg2) {
    // Custom parsing logic
    return true;
  }
}
```

**Key points:**
- External rules declare the method name and optional parameters after `::=`.
- `<< >>` is the inline variant of an external rule.
- The method must be static and follow the signature: `boolean method(PsiBuilder, int, ...)`.
- Methods live in `parserUtilClass` or a class imported via `parserImports`.
- `<<eof>>` is a built-in external that tests for end of input.

Source: HOWTO.md lines 96-118, README.md lines 149-170, ExternalRules.bnf.

---

## Example 7: Meta Rules

Demonstrates meta rules with parameters, invocation syntax, and nesting.

```bnf
// Basic meta rule: the comma-separated list pattern
meta comma_list ::= <<param>> (',' <<param>>) *

// Using a meta rule — pass a rule reference as the argument
option_list ::= <<comma_list option>>

// Pass a choice expression as argument (in parentheses)
keyword_list ::= <<comma_list (SELECT | INSERT | DELETE)>>

// Meta rule with multiple parameters
meta two_params ::= <<a>> '=' <<b>>
assignment_list ::= <<two_params id number>>

// Pinned meta rule (comma-separated with recovery)
meta comma_list_pinned ::= <<head>> <<item>> (<<comma_list_tail <<item>>>>) *
meta comma_list_tail ::= ',' <<item>> {pin=1}

// Nested meta calls
nested_example ::= <<comma_list <<comma_list some_rule>>>>

// Meta rule with parenthesized list
private meta paren_list ::= '(' <<param>> (',' <<param>>) * ')' {pin=1}
function_args ::= <<paren_list expr>>

// Arguments can be: rule references, (choices), [optionals], {alt_choices}
usage1 ::= <<comma_list rule_ref>>
usage2 ::= <<comma_list (a | b | c)>>
usage3 ::= <<comma_list [optional_item]>>
usage4 ::= <<comma_list {alt1 | alt2}>>
```

**Key points:**
- `meta` modifier marks a rule as parametrized.
- Parameters referenced with `<<param_name>>` inside the rule body.
- Invoked via external expression: `<<meta_rule_name arg1 arg2>>`.
- Arguments can be rule references, parenthesized expressions, brackets, or braces.
- Meta rules can be nested: `<<comma_list <<comma_list some>>>>`.
- The `comma_list` pattern is the most common meta rule pattern in practice.

Source: README.md lines 149-157, ExternalRules.bnf lines 38-55, 77-78.

---

## Example 8: Grammar Sections and Multiple Parser Classes

Demonstrates splitting a grammar into multiple parser classes using `;{` separators.

```bnf
// Main parser class — rules defined here go into MainParser
{
  parserClass="com.example.MainParser"
  tokens=[
    id='regexp:\w+'
    number='regexp:\d+'
  ]
}

root ::= (statement | expression) *
statement ::= id '=' number

// Semicolon-brace separator starts a new section
// Rules after this go into ExpressionParser
;{
  parserClass="com.example.ExpressionParser"
}

expression ::= id '+' id
complex_expr ::= expression ('*' expression) *

// Another section — rules go into UtilityParser
;{
  parserClass="com.example.UtilityParser"
}

utility_rule ::= id number
```

**Key points:**
- `;{` starts a new global attributes section mid-file.
- Primarily used to split parser into multiple classes via `parserClass` changes.
- Each section's rules generate methods in the specified parser class.
- Useful for large grammars to keep generated code manageable.

Source: ExternalRules.bnf lines 84-99 (3 classes), PsiGen.bnf lines 39-41, 57-59 (3 classes).

---

## Example 9: Attribute Syntax

Demonstrates global attributes, rule-level attributes, pattern-based attributes, and list values.

```bnf
// Global attributes at top of file
{
  // Simple key=value pairs
  parserClass="com.example.MyParser"
  generatePsi=true

  // List values
  tokens=[PLUS='+' MINUS='-' id='regexp:\w+']
  parserImports=["static com.example.ManualParsing.*"]

  // Pattern-based attributes — regex matched against rule names
  extends(".*_expr")=expr               // all *_expr rules extend expr
  pin(".*_list(?:_\\d+)*")=1            // pin=1 on all *_list rules
  name(".*_expr")='expression'          // display name for error messages
  consumeTokenMethod(".*_recover")="consumeTokenFast"
}

// Rule-level attributes (placed after rule expression)
property ::= id '=' expr {pin=2}

// Rule-level attributes with multiple values
list_item ::= number {recoverWhile=item_recover elementType=my_type}

// Pattern attributes in global block target sub-expressions too
list ::= '(' [!')' item (',' item) *] ')' {pin(".*")=1}
// pin(".*")=1 applies pin=1 to every sub-sequence in the rule
```

**Key points:**
- Global attributes go in `{ }` at the top or after a `;` separator.
- Rule attributes go in `{ }` immediately after the rule expression.
- Pattern-based attributes use Java regex: `extends(".*_expr")=expr`.
- Pattern targets apply to sub-expressions too: `pin(".*")=1`.
- List values use `[item1 item2]` syntax; items can include `id=string` pairs.

Source: Grammar.bnf lines 69-92, README.md lines 108-129.

---

## Example 10: Empty Rules and Edge Cases

Demonstrates valid edge cases in Grammar-Kit BNF syntax.

```bnf
// Empty rules — all three bracket types are valid
empty_parens ::= ()
empty_braces ::= {}
empty_brackets ::= []

// Private empty rules
private empty_private ::= ()
private empty_opt ::= []

// Nested empty groupings
private nested_empty ::= [({})]

// Non-empty nested groupings
private nested_content ::= [({some_token})]
private nested_seq ::= [({token1 token2})]

// Left and inner with empty rules
left empty_left ::= []
inner left empty_inner_left ::= []

// Rule names can contain special characters
include-section ::= id number
<include (section) alt> ::= id number
private <include-section-recover?> ::= !()

// elementType="" makes a rule private for PSI purposes
utility_rule ::= id {elementType=""}
```

**Key points:**
- Empty rules with `()`, `{}`, or `[]` are all valid.
- Rule names can contain hyphens, angle brackets, parentheses, and question marks.
- `elementType=""` (empty string) prevents IElementType generation without making the rule private.
- Nested empty groupings like `[({})]` are valid syntax.

Source: Small.bnf lines 17-28, PsiGen.bnf lines 34-36, 66.

---

## Example 11: Complete Grammar (JSON)

A real-world grammar demonstrating most syntax features together. Taken from Grammar-Kit's Live Preview test data.

```bnf
{
  tokens = [
    space='regexp:\s+'
    string = "regexp:\"[^\"]*\"|'[^']*'"
    number = "regexp:(\+|\-)?\p{Digit}*"
    id = "regexp:\p{Alpha}\w*"
    comma = ","
    colon = ":"
    brace1 = "{"
    brace2 = "}"
    brack1 = "["
    brack2 = "]"
  ]
  extends("array|object|json")=value
}

root ::= json
json ::= array | object
value ::= string | number | json {name="value"}

array ::= '[' [!']' item (!']' ',' item) *] ']' {pin(".*")=1}
private item ::= json {recoverWhile=recover}
object ::= '{' [!'}' prop (!'}' ',' prop) *] '}' {pin(".*")=1}
prop ::= [] name ':' value {pin=1 recoverWhile=recover}
name ::= id | string {name="name"}
private recover ::= !(',' | ']' | '}' | '[' | '{')
```

**Key points:**
- Complete, working grammar for JSON parsing.
- Uses regexp tokens for Live Preview compatibility.
- Pattern-based `extends` for PSI hierarchy.
- `pin(".*")=1` pins all sub-sequences.
- `!']'` and `!'}' ` lookahead prevents consuming closing delimiters.
- Shared `recover` predicate for both array items and object properties.
- `name` attribute on `value` and `name` rules improves error messages.
- `prop ::= []` with `pin=1` makes the property name optional (always pinned).

Source: testData/livePreview/Json.bnf (verbatim).
