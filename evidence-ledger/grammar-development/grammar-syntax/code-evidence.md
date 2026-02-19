# Code Evidence: BNF Grammar Syntax

## Scope Information
This evidence covers section 2.1: BNF Grammar Syntax

INCLUDES: Grammar file structure, token definitions, rule syntax fundamentals, advanced constructs, EBNF extensions
EXCLUDES: Grammar design patterns (2.2), expression parsing (2.3), error recovery details (2.4), attribute system details (3.1)

---

## Grammar File Structure

### File Extension
- Grammar files use `.bnf` extension
- Source: `BnfFileType.java` registers `.bnf` file type

### Overall Structure
- A `.bnf` file contains: optional global attributes block, then rules
- Grammar elements are either `attrs` (attribute blocks) or `rule` definitions
- Source: `Grammar.bnf` line 59: `private grammar_element ::= !<<eof>> (attrs | rule)`

### Header / Global Attributes Block
- Enclosed in `{ }` braces at top of file
- Contains `name=value` pairs separated by optional `;`
- Can contain pattern-based attributes: `name("pattern")=value`
- Multiple global attribute blocks allowed, separated by `;{` syntax
- Source: `Grammar.bnf` lines 1-54, `README.md` lines 108-111

### Semicolon as Section Separator
- `;{` starts a new global attributes section mid-file
- Used to split parser into multiple classes via `parserClass` changes
- Source: `ExternalRules.bnf` lines 84-86: `;{ parserClass="ExternalRules2" }`
- Source: `PsiGen.bnf` lines 39-41, 57-59

### Comments
- Line comments: `//` to end of line
- Block comments: `/* ... */`
- Source: `Grammar.bnf` lines 45-46: `line_comment="regexp://.*"`, `block_comment="regexp:/\*(.|\n)*\*/"`
- Line comments require a line break after them (from `BnfParserDefinition.java` line 75)

### Rule Definition Syntax
- Basic form: `rule_name ::= expression`
- With modifiers: `modifier* id '::=' expression`
- Optional trailing `;`
- Optional rule-level attributes: `rule_name ::= expression { attr=value }`
- Source: `Grammar.bnf` line 64: `rule ::= rule_start expression attrs? ';'?`

### Assignment Operators
- `::=` is the standard rule definition operator
- `=` is used for attribute assignment only
- Source: `Grammar.bnf` lines 23-24: `OP_EQ="="`, `OP_IS="::="`

---

## Token Definitions

### Token Block Syntax
- Declared in global `tokens` attribute as a list: `tokens=[ ... ]`
- Each entry: `token_name='token_value'` or `token_name="token_value"`
- Entries separated by whitespace (no comma needed)
- Optional `;` after each entry
- Source: `Grammar.bnf` lines 22-47

### Token Forms

#### Named tokens with string values
- `TOKEN_NAME='value'` or `TOKEN_NAME="value"`
- Name becomes IElementType constant, value is string representation
- Example: `SEMI=';'`, `OP_EQ="="`
- Source: `Grammar.bnf` lines 23-38

#### Regexp tokens
- Value prefixed with `regexp:` — e.g., `id='regexp:\w+'`
- Single or double quotes both work: `id="regexp:\w+"`
- Regexp tokens required by Live Preview
- Full Java RegExp syntax supported in Live Preview
- JFlex supports only a subset; Grammar-Kit attempts conversions
- Source: `Grammar.bnf` lines 41-46, `BnfConstants.java` line 16: `REGEXP_PREFIX = "regexp:"`
- Source: `tokens.html`: "Regexp tokens are required by Live Preview"

#### Name-only tokens (no value)
- Just `token_name` with no `=` or value
- Source: `tokens.html` line 10: `string  // no value or pattern`

### Token Reference in Rules

#### By name (unquoted)
- Reference token by its declared name: `OP_EQ`
- Source: `README.md` lines 173-178

#### By value (quoted)
- Reference token by its string value: `'='` or `"="`
- Recommended for readability
- Source: `README.md` line 177: "It is recommended to use values where possible"

#### Implicit tokens (undeclared)
- Tokens used in rules but not declared in `tokens` block
- Unquoted implicit tokens (keywords): name equals value, e.g., `CREATE` matches text "CREATE"
- Quoted implicit tokens (text-matched): matched by text, not IElementType — slower
- Text-matched tokens can span multiple real lexer tokens
- Source: `README.md` lines 180-184

### Token Precedence and Conflicts
- Names resolve conflicts when unquoted value matches a rule name
- Rules, tokens, and text-matched tokens have different editor colors
- Source: `README.md` lines 178-185

### Whitespace and Comment Handling
- Whitespace/comments declared in `ParserDefinition` are skipped by `PsiBuilder`
- In Live Preview: any space/newline-matching regexp token NOT used in rules is treated as whitespace
- Tokens named ending in "comment" (case-insensitive) and not used in rules are treated as comments
- Source: `TUTORIAL.md` lines 79-81
- Source: `LivePreviewLexer.java` lines 200-218: `guessDelegateType()` method

---

## Rule Syntax Fundamentals

### Basic Rule Structure
- `rule_name ::= expression`
- Rule names: identifiers matching `\w+` (letters, digits, underscores)
- Rule names can contain hyphens and angle brackets: `<include-section-recover?>` (from `PsiGen.bnf` line 36)
- First rule is implicitly private (the grammar root)
- Source: `Grammar.bnf` lines 64-65, `HOWTO.md` line 232

### Sequences
- Items separated by whitespace: `rule_A rule_B rule_C`
- Matches left to right; all must match for success
- Source: `Grammar.bnf` line 94: `expression ::= sequence choice?`
- Source: `README.md` line 92: `root_rule ::= rule_A rule_B rule_C rule_D`

### Ordered Choice (`|`)
- Alternatives separated by `|`: `rule_A | rule_B | rule_C`
- Tries alternatives in order; first match wins (PEG semantics)
- Source: `Grammar.bnf` line 102: `left choice ::= ( '|' sequence ) +`
- Source: `README.md` line 93: `rule_A ::= token | 'or_text' | "another_one"`

### Quantifiers
- `?` — optional (zero or one)
- `+` — one or more
- `*` — zero or more
- Applied as postfix to any expression
- Source: `Grammar.bnf` line 104: `quantifier ::= '?' | '+' | '*'`
- Source: `README.md` lines 94-96

### Grouping with Parentheses `( )`
- `(expr)` groups expressions for quantifiers or choices
- Source: `Grammar.bnf` line 120: `paren_expression ::= '(' expression ')'`
- Example: `(rule_A | rule_B)*`

### Optional Grouping with Brackets `[ ]`
- `[expr]` is shorthand for `(expr)?` — optional expression
- Source: `Grammar.bnf` line 121: `paren_opt_expression ::= '[' expression ']'`
- Source: `README.md` line 83, line 94: `rule_B ::= [ optional_token ] and_another_one?`

### Alternative Choice with Braces `{ }`
- `{expr | expr}` is an alternative syntax for choices (when not an attribute block)
- Distinguished from attribute blocks by context (no `attr_start` pattern)
- Source: `Grammar.bnf` line 120: `paren_expression ::= '(' expression ')' | '{' alt_choice_element '}'`
- Source: `Grammar.bnf` line 122: `private alt_choice_element ::= !attr_start_simple expression`
- Source: `README.md` line 83: "use { | | } for choices as these variants are popular in real-world grammars"
- Source: `README.md` line 96: `rule_D ::= { can_use_braces + (and_parens) * }`

### Rule References
- Reference another rule by its name (unquoted identifier)
- Resolves to the referenced rule's parse function
- Source: `Grammar.bnf` line 117: `reference_or_token ::= id`

### String Literals in Rules
- Single-quoted: `'text'`
- Double-quoted: `"text"`
- Match token values or text directly
- Source: `Grammar.bnf` lines 118-119

### Number Literals
- Numeric values: `\d+`
- Used in attribute values and as literal expressions
- Source: `Grammar.bnf` line 118: `literal_expression ::= string_literal_expression | number`

---

## Rule Modifiers

### Available Modifiers
- `private` — skip PSI node creation; children included in parent
- `external` — hand-written parse function; no code generated
- `meta` — parametrized rule; accepts other parse functions as parameters
- `left` — takes previous sibling AST node and becomes its parent
- `inner` — takes previous sibling AST node and becomes its child (used with `left`)
- `upper` — takes parent node and replaces it, adopting all its children
- `fake` — only PSI classes generated; no parsing code
- Source: `Grammar.bnf` lines 66-67: `modifier ::= 'private' | 'external' | 'meta' | 'inner' | 'left' | 'upper' | 'fake'`
- Source: `README.md` lines 131-147

### Modifier Placement
- Before rule name: `private left rule_name ::= expression`
- Multiple modifiers can be combined
- Source: `Grammar.bnf` line 65: `private rule_start ::= modifier* id '::='`

### Modifier Combinations
- `inner` should only be used with `left`
- `private left` is equivalent to `private left inner`
- `fake` should not be combined with `private`
- By default, rules are public (non-private, non-fake, etc.)
- Source: `README.md` lines 143-147

### Modifier Effects Summary
- `private`: no PSI node; children merge into parent
- `left`: restructures AST — wraps left sibling
- `inner left`: restructures AST — injects into left sibling
- `upper`: restructures AST — replaces parent, adopts siblings
- `meta`: enables `<<param>>` parameters in rule body
- `external`: body specifies method name and parameters, not grammar
- `fake`: generates PSI interfaces/classes only, no parser code
- Source: `README.md` lines 131-147, `ParserGeneratorUtil.java` lines 698-734

---

## Advanced Constructs

### Predicates

#### And-predicate `&`
- `&expression` — succeeds if expression matches, consumes nothing
- Lookahead assertion
- Source: `Grammar.bnf` lines 106-107: `predicate ::= predicate_sign simple`, `predicate_sign ::= '&' | '!'`
- Source: `README.md` line 95: `rule_C ::= &required !forbidden`

#### Not-predicate `!`
- `!expression` — succeeds if expression does NOT match, consumes nothing
- Negative lookahead
- Common in recovery predicates: `!(',' | ';' | ')')`
- Source: `Grammar.bnf` lines 106-107
- Source: `README.md` line 95

### External Expressions `<< >>`
- Inline variant of external rule: `<<methodName arg1 arg2>>`
- Also used to invoke meta rules with arguments: `<<meta_rule arg>>`
- Source: `Grammar.bnf` line 114: `external_expression ::= '<<' reference_or_token option * '>>'`
- Source: `README.md` lines 150-151

#### External Rule Declaration
- `external rule_name ::= methodName param1 param2 ...`
- Body specifies method name and optional parameters
- Method must be static, in `parserUtilClass` or imported via `parserImports`
- Required signature: `public static boolean methodName(PsiBuilder builder, int level, ...extraParams)`
- Source: `README.md` lines 159-163, `HOWTO.md` lines 96-118

#### External Expression (Inline)
- `<<methodName param1 param2>>` used inline in any rule
- Equivalent to external rule but inline
- Source: `HOWTO.md` line 109: `// rule ::= part1 <<parseMyExternalRule true 5>> part3`

#### Parameter Passing in External Expressions
- Double-quoted strings passed "as is": `"1+1"` passes the string `1+1`
- Single-quoted strings are unquoted first: `'1+1'` passes `1+1` (unquoted)
- Rule references passed as `Parser` instances (functional interface)
- Helps pass qualified enum constants, Java expressions
- Source: `README.md` lines 165-170

#### Empty External Expression
- `<<>>` is valid — represents an empty external expression
- Source: `ExternalRules.bnf` line 75: `private empty_external_usage2 ::= <<>>`

### Built-in External: `<<eof>>`
- `<<eof>>` — tests if parser has reached end of input
- Implemented as `GeneratedParserUtilBase.eof(builder, level)`
- Commonly used as `!<<eof>>` to check "not at end of file"
- Source: `GeneratedParserUtilBase.java` lines 109-111
- Source: `Grammar.bnf` line 59: `private grammar_element ::= !<<eof>> (attrs | rule)`
- Source: `TUTORIAL.md` line 110: `private root_item ::= !<<eof>> property ';'`

### Private Rules
- `private rule_name ::= expression`
- No PSI node created; children merge into parent node
- First rule in grammar is implicitly private
- Private rules not visible in PSI tree
- Source: `README.md` line 133, `HOWTO.md` line 232

### Meta Rules
- `meta rule_name ::= <<param>> (',' <<param>>) *`
- Parameters referenced with `<<param_name>>` syntax inside rule body
- Called via external expression: `<<meta_rule actual_arg>>`
- Arguments can be rule references, expressions in parens, or literals
- Source: `README.md` lines 149-157
- Source: `Grammar.bnf` line 66: modifier includes `'meta'`

#### Meta Rule Parameters
- `<<param>>` — references a parameter by name
- Multiple parameters supported: `meta two_params_meta ::= <<a>> <<b>>`
- Parameters can be nested meta calls: `<<comma_list <<comma_list some>>>>`
- Source: `ExternalRules.bnf` lines 38-45, 77-78

#### Meta Rule Invocation
- `<<meta_rule_name arg1 arg2>>` — calls meta rule with arguments
- Arguments can be: rule references, `(choice | expressions)`, `[optional]`, `{alt_choice}`
- Source: `ExternalRules.bnf` lines 47-55

#### Common Meta Rule Pattern: comma_list
- `meta comma_list ::= <<param>> (',' <<param>>) *`
- Usage: `<<comma_list some_rule>>`
- Source: `ExternalRules.bnf` line 38, `README.md` lines 155-156

### Upper Rules
- `upper rule_name ::= expression`
- Takes parent node and replaces it, adopting all parent's children
- Source: `README.md` line 137
- Source: `UpperRules.bnf` lines 17-18: `upper abc_one ::= just_b X {pin=1}`

### Left Rules
- `left rule_name ::= expression`
- Takes previous sibling and wraps it (becomes its parent)
- Used for binary operators, postfix expressions
- Source: `README.md` line 135
- Source: `LeftAssociative.bnf` lines 7-11

### Inner Left Rules
- `left inner rule_name ::= expression`
- Takes previous sibling and injects into it (becomes its child)
- Source: `README.md` line 136
- Source: `LeftAssociative.bnf` line 9: `left inner leech ::= id`

### Fake Rules
- `fake rule_name ::= expression`
- Only PSI classes generated; no parser code
- Used to shape PSI hierarchy without affecting parsing
- Source: `README.md` line 141
- Source: `ExprParser.bnf` line 47: `fake ref_expr ::= expr? '.' identifier`
- Source: `PsiGen.bnf` line 37: `fake other_expr ::= expr +`

---

## EBNF Extensions (Grammar-Kit Specific)

### PEG Foundation
- Grammar-Kit uses Parsing Expression Grammar (PEG) semantics
- `::=` replaces PEG's `←` symbol
- Ordered choice (not ambiguous): first match wins
- Source: `README.md` line 82: "See Parsing Expression Grammar (PEG) for basic syntax"

### Alternative Grouping Syntax
- `[ expr ]` — optional (equivalent to `(expr)?`)
- `{ expr | expr }` — choice (alternative to `(expr | expr)`)
- Source: `README.md` line 83: "You can also use [ .. ] for optional sequences and { | | } for choices"

### Rule-Level Attributes (Inline)
- `rule ::= expression {attr1=value1 attr2=value2}`
- Placed immediately after rule expression
- Source: `Grammar.bnf` line 64: `rule ::= rule_start expression attrs? ';'?`

### Global Pattern-Based Attributes
- `extends(".*_expr")=expr` — applies to all rules matching pattern
- `pin(".*_list(?:_\d+)*")=1` — applies pin to matching rules and sub-expressions
- Pattern is a Java regex matched against rule names
- Source: `README.md` lines 122-129

### Semicolon-Separated Grammar Sections
- `;{ parserClass="ClassName" }` splits grammar into multiple parser classes
- Rules after the separator go into the specified parser class
- Source: `ExternalRules.bnf` lines 84-86, 95-97

### Empty Rules
- `empty ::= ()` — valid empty rule with parentheses
- `empty2 ::= {}` — valid empty rule with braces
- `empty3 ::= []` — valid empty rule with brackets
- Source: `Small.bnf` lines 17-19

### Empty Predicate Expressions
- `&()` — and-predicate on empty (always true)
- `!()` — not-predicate on empty (always false)
- Source: `Small.bnf` lines 22-23

### Nested Empty Expressions
- `[({})]` — nested empty groupings are valid
- Source: `Small.bnf` line 24

### Token String Quoting
- Single quotes: `'token_value'`
- Double quotes: `"token_value"`
- Both are interchangeable for token values
- Source: `Grammar.bnf` line 43: `string="regexp:('([^'\\]|\\.)*'|\"([^\"\\]|\\\"|\\\'|\\)*\")"`

### Regexp Token Prefix
- `regexp:` prefix in token value indicates a regular expression
- Example: `id='regexp:\w+'`, `number="regexp:\d+(\.\d*)?"`
- RegExp language is injected into these strings for IDE support
- Source: `BnfConstants.java` line 16, `BnfStringRegexpInjector.java` lines 28-30

### `#auto` Recovery Value
- `recoverWhile="#auto"` — automatic recovery predicate
- Means `! FOLLOWS(rule)` — recovers until a token in the FOLLOW set
- Source: `BnfConstants.java` line 40: `RECOVER_AUTO = "#auto"`
- Source: `recoverWhile.html` line 3: "Name of the recovery predicate rule or '#auto' which means '! FOLLOWS(rule)'"
- Source: `AutoRecovery.bnf` line 6: `item ::= number {recoverWhile="#auto"}`

### `elementType=""` (Empty String)
- Setting `elementType=""` makes a rule private for PSI purposes (no element type generated)
- Source: `PsiGen.bnf` line 66: `publicMethodToCall ::= identifier {elementType=""}`

### Generated Method Naming Convention
- Each rule generates a static method: `static boolean rule_name(..)`
- Sub-expressions: `rule_name_0(..)`, `rule_name_N1_N2_..._NX(..)`
- Avoid naming rules like `rule_name_N1_N2_..._NX` to prevent conflicts
- Source: `README.md` lines 113-121

---

## Attribute Syntax (Structure Only — Details in Section 3.1)

### Attribute Block Syntax
- `{ name=value name2=value2 }`
- Values: identifiers, strings, numbers, lists `[...]`
- Optional `;` between entries
- Source: `Grammar.bnf` lines 69-92

### Pattern Attributes
- `name("regex_pattern")=value`
- Pattern is a Java regex matched against rule names
- Source: `Grammar.bnf` lines 82-84

### Attribute Placement
- Global: at top of file or after `;` separator
- Rule-level: immediately after rule expression
- Source: `README.md` lines 108-111

### List Values
- `name=[item1 item2 item3]`
- Items can be: `id`, `id=string`, `string`
- Source: `Grammar.bnf` lines 86-92

---

## Key Syntax-Related Attributes (Brief — Cross-ref to 3.1)

### `tokens` (global)
- Declares token names and values
- Default: empty list
- Source: `KnownAttribute.java` line 72

### `parserImports` (global)
- Additional static imports for external rule resolution
- Example: `parserImports=["static org.sample.ManualParsing.*"]`
- Source: `KnownAttribute.java` line 37, `parserImports.html`

### `name` (rule-level)
- Display name in error messages: `name(".*_expr")=expression`
- Changes error from token list to `<expression> required`
- Empty string suppresses short error message
- Source: `name.html`, `README.md` lines 199-200

---

## Example Locations

### Authoritative Syntax Reference
- `grammars/Grammar.bnf` — BNF self-definition (complete syntax)

### Basic Syntax
- `testData/generator/Small.bnf` — empty rules, private rules, external rules, token references
- `testData/parser/AlternativeSyntax.bnf` — alternative syntax forms with `<>` in names

### Token Definitions
- `testData/livePreview/Json.bnf` — complete token block with regexp tokens
- `testData/generator/ExprParser.bnf` — regexp tokens for expressions
- `TUTORIAL.md` lines 84-127 — full sample grammar with tokens

### Rule Modifiers
- `testData/generator/LeftAssociative.bnf` — left, inner, private left combinations
- `testData/generator/UpperRules.bnf` — upper modifier usage
- `testData/generator/PsiGen.bnf` — fake rules, external rules, left rules

### External and Meta Rules
- `testData/generator/ExternalRules.bnf` — comprehensive external/meta rule examples
- `testData/generator/ExternalRulesLambdas.bnf` — meta rules with Java 8 lambdas
- `HOWTO.md` lines 96-118 — external rule implementation pattern

### Expression Syntax (Cross-ref to 2.3)
- `testData/generator/ExprParser.bnf` — expression parsing with extends, left, fake

### Error Recovery (Cross-ref to 2.4)
- `testData/generator/AutoRecovery.bnf` — `#auto` recoverWhile
- `testData/generator/Autopin.bnf` — pattern-based pin

### Grammar Sections
- `testData/generator/ExternalRules.bnf` lines 84-99 — `;{` section separators
- `testData/generator/PsiGen.bnf` lines 39-41, 57-59 — multiple parser classes

---

## Out of Scope

Features found but belonging to other sections:

### Expression Parsing → Section 2.3
- `extends(".*_expr")=expr` pattern for expression roots
- Left recursion for binary/postfix operators
- `rightAssociative` attribute
- Priority/precedence tables
- N-ary operator syntax: `expr ('**' expr) +`

### Error Recovery Details → Section 2.4
- `pin` attribute mechanics and values
- `recoverWhile` predicate patterns
- `#auto` recovery implementation details
- `extendedPin` mode behavior
- Recovery predicate design patterns

### Attribute System Details → Section 3.1
- Full attribute catalog (38 known attributes)
- Global vs. rule-level attribute scope
- Attribute inheritance and override rules
- `generate` options table
- PSI-related attributes (extends, implements, mixin, methods, hooks)
- Element type attributes (elementType, elementTypeClass, elementTypeFactory)
- Stub support attributes (stubClass, fallbackStubElementType)

### Grammar Design Patterns → Section 2.2
- Rule naming conventions
- Grammar organization strategies
- Common list/separator patterns
- Trailing comma handling

---

## Missing Documentation

- No official docs for `{ | | }` brace-choice syntax beyond one README sentence
- No docs for `<<>>` empty external expression
- No docs for rule names with special characters (`<include-section-recover?>`)
- No docs for `!()` and `&()` empty predicate expressions
- No docs for `elementType=""` empty string behavior
- No docs for `;{` section separator syntax (only visible in test files)
- No docs for how `private left` equivalence to `private left inner` works
- Token precedence rules between regexp and literal tokens not documented
- No docs for number literals in rule expressions
