# Code Evidence: Expression Parsing

## Scope Information
This evidence covers section 2.3: Expression Parsing
- Expression parsing fundamentals
- Implementing precedence
- Associativity control
- Expression optimization
- Complex expressions

---

## Expression Parsing Fundamentals

### Two Approaches Available
- **Traditional approach**: `left` modifier + manual layering (TUTORIAL.md style)
- **Pratt/priority approach**: left-recursive rules + `extends` + auto-detection (HOWTO.md 2.4 style)
- Pratt approach described as "compact expression parsing with priorities"
- Generated parser is "a procedural rewrite of the Pratt parsing" (HOWTO.md line 199)
- Reference: http://javascript.crockford.com/tdop/tdop.html

### Operator Types (Auto-Detected)
- `ATOM`: no reference to root expression rule (e.g., `literal_expr ::= number`)
- `PREFIX`: root expression reference appears after operator (e.g., `unary_min_expr ::= '-' expr`)
- `POSTFIX`: root expression reference appears before operator (e.g., `factorial_expr ::= expr '!'`)
- `BINARY`: two references to root expression rule (e.g., `plus_expr ::= expr '+' expr`)
- `N_ARY`: uses `(<op> expr)+` syntax (e.g., `exp_expr ::= expr ('**' expr) +`)
- Source: `ExpressionHelper.OperatorType` enum: `{ATOM, PREFIX, POSTFIX, BINARY, N_ARY}`

### Expression vs Statement
- Expressions use left recursion and `extends` to form expression hierarchy
- Statements use sequential parsing with `pin` and `recoverWhile`
- Expression root rule lists all expression alternatives as ordered choices
- Statement-level wrapping: `private element ::= expr ';'? {recoverWhile=element_recover}`

### Expression Root Detection (Auto)
- Rule is detected as expression root when:
  - Rule is not `private` and not `fake`
  - Rule has no direct content (empty content rules map)
  - Rule's FIRST set contains the rule's own name (left recursion)
- Comment in ExprParser.bnf: "left recursion and empty PSI children define expression root"

---

## Implementing Precedence

### Pratt/Priority-Based Approach (Recommended)
- Priority increases from top to bottom in the root rule's choice list
- Ordered choice semantics preserved
- Private rules group operators at the same priority level
- Generated parser produces only 2 methods for the root rule

### Root Rule Structure
- Users write:
  ```
  expr ::= assign_expr
    | add_group
    | mul_group
    | unary_group
    | exp_expr
    | primary_group
  ```
- Priority 0 = lowest (first alternative), priority N = highest (last alternative)

### Private Priority Groups
- Users write: `private mul_group ::= mul_expr | div_expr`
- All operators in a private group share the same priority level
- Groups keep the root rule readable

### Generated Priority Table Format
- Generated as comment in parser code:
  ```
  // 0: BINARY(assign_expr)
  // 1: BINARY(plus_expr) BINARY(minus_expr)
  // 2: BINARY(mul_expr) BINARY(div_expr)
  // 3: PREFIX(unary_plus_expr) PREFIX(unary_min_expr)
  // 4: N_ARY(exp_expr)
  // 5: POSTFIX(factorial_expr)
  // 6: ATOM(simple_ref_expr) ATOM(literal_expr) PREFIX(paren_expr)
  ```

### Traditional Layer-Based Approach (Using `left` Modifier)
- Users write:
  ```
  expr ::= factor plus_expr *
  left plus_expr ::= plus_op factor
  private plus_op ::= '+'|'-'
  private factor ::= primary mul_expr *
  left mul_expr ::= mul_op primary
  ```
- Each precedence level is a separate rule layer
- `left` modifier: takes AST node on the left and encloses it as parent
- Requires manual layering of rules by precedence
- Results in deeper PSI tree without `extends` attribute

### IDE Feature: Quick Documentation Priority Table
- Ctrl-Q / Cmd-J on expression rules shows priority table
- Table highlights current rule's position in blue
- Shows operator type and priority number
- Source: `BnfDocumentationProvider.dumpPriorityTable()`

---

## Associativity Control

### Left Associativity (Default)
- All binary operators are left-associative by default
- `a + b + c` parses as `(a + b) + c`
- Generated code: `expr(builder_, level_, priority)` — same priority for right operand

### Right Associativity
- Attribute: `rightAssociative=true`
- Users write: `assign_expr ::= expr '=' expr { rightAssociative=true }`
- `a = b = c` parses as `a = (b = c)`
- Default value: `false`
- Generated code passes `argPriority - 1` for right operand (allows same-level recursion)
- Source: `KnownAttribute.RIGHT_ASSOCIATIVE` — type Boolean, default false

### Official Attribute Description
- "Mark operator as right-associative, i.e. a = b = c should be equal to a = (b = c) while a + b + c usually equals to (a + b) + c."

### Non-Associative Operators
- No explicit attribute for non-associativity
- Achieved by using comparison-style operators at same priority level
- Example: `conditional_expr ::= expr ('<' | '>' | '<=' | '>=' | '==' | '!=') expr`

### Mixed Associativity
- Different operators at different priority levels can have different associativity
- `rightAssociative` is a per-rule attribute
- Example: `assign_expr` is right-associative at priority 0, `plus_expr` is left-associative at priority 2

---

## Expression Optimization

### Problem: Deep PSI Trees
- Without `extends`: AST looks like `FileNode/Expr/AddExpr/MulExpr/LiteralExpr`
- With `extends`: AST is flat: `FileNode/LiteralExpr`
- Source: HOWTO.md section 3.1

### The `extends` Attribute for Flat Structure
- Users write: `extends(".*_expr")=expr`
- Pattern-based: applies to all rules matching `.*_expr`
- Effect: AST nodes produced by extending rules are collapsed by parser
- Root expression rule node never appears in AST
- Redundant nodes collapsed automatically
- Generates `EXTENDS_SETS_` TokenSet array in parser class

### The Expression Parsing Idiom (5 Rules)
1. All expression rules should extend the root expression rule
2. Priority increases from top to bottom, ordered choice semantics preserved
3. Use left recursion for binary and postfix expressions
4. Use `private` rules to define groups of operators with same priority
5. Use `rightAssociative` attribute when default left associativity is not appropriate
- Source: HOWTO.md section 2.4, rules 1-5

### Binary vs N-ary Operations
- Binary: `plus_expr ::= expr '+' expr` — standard two-operand
- N-ary: `exp_expr ::= expr ('**' expr) +` — mandatory `(<op> expr)+` syntax
- N-ary generates a while loop consuming all operands at same level
- Warning if N-ary syntax is wrong: "expected for N-ary operator, treating as POSTFIX"

### Performance: consumeTokenMethod
- Users write: `consumeTokenMethod(".*_expr|expr")="consumeTokenFast"`
- Avoids recording all operators in error messages
- Increases performance by skipping error reporting info
- Default method: `consumeToken`
- Available methods: `consumeToken`, `consumeTokenFast`
- Custom consume methods also supported
- Attribute description: "no one really needs to know that + - * / are expected at any offset"

### `name` Attribute for Error Messages
- Users write: `name(".*_expr")=expression`
- Changes error messages to `<expression> required` instead of long token lists
- Applies via pattern to all matching rules

---

## Complex Expressions

### Mixing Operator Types in One Hierarchy
- Single expression root can contain all operator types simultaneously
- ExprParser.bnf demonstrates: BINARY, PREFIX, POSTFIX, N_ARY, ATOM all in one hierarchy
- Priority table accommodates all types

### Ternary Operators (Elvis/Conditional)
- Users write: `elvis_expr ::= expr '?' expr ':' expr`
- Treated as BINARY with a "tail" — the `:` expr part
- Tail is parsed after the main binary structure
- Generated code uses `report_error_` for middle operand, then parses tail

### Function Calls as Postfix
- Users write: `call_expr ::= ref_expr arg_list`
- Type constraint: `ref_expr` instead of generic `expr` for left operand
- Generated code: `leftMarkerIs(builder_, REF_EXPR)` — checks left marker type
- `arg_list ::= '(' [ !')' expr (',' expr) * ] ')' {pin(".*")=1}`

### Qualification/Member Access as Postfix
- Users write: `qualification_expr ::= expr '.' identifier`
- Treated as POSTFIX operator
- Can share elementType with fake rule: `{extends=ref_expr elementType=ref_expr}`

### Narrowing Parse to Specific Expression Rules
- Users can use specific expression rule instead of generic `expr`
- Example: `between_expr ::= expr BETWEEN add_group AND add_group`
- `add_group` restricts the operand to only add-level or higher priority expressions
- Generated code passes the priority of the referenced group

### Fake Rules for PSI Hierarchy
- Users write: `fake ref_expr ::= expr? '.' identifier`
- No parsing code generated for fake rules
- Used to create shared PSI interfaces
- Combined with `extends` and `elementType` for PSI unification:
  ```
  simple_ref_expr ::= identifier {extends=ref_expr elementType=ref_expr}
  qualification_expr ::= expr '.' identifier {extends=ref_expr elementType=ref_expr}
  ```

### Operator Part Can Contain Complex BNF
- Operator part can contain any valid BNF expressions and define "tails"
- Example: `div_expr ::= expr [div_modifier | '*'] '/' expr div_expr_tail`
- Multi-token operators: `is_not_expr ::= expr IS NOT expr`
- Choice operators: `conditional_expr ::= expr ('<' | '>' | '<=' | '>=' | '==' | '!=') expr`

### Multiple Expression Roots
- Multiple expression roots allowed in a single grammar
- Constraint: expression hierarchies must not intersect
- `extraRoot=true` attribute marks expression root for `parse_extra_roots()` method
- Example: ExprParser.bnf uses `{extraRoot=true}` on `expr` rule

### External Expressions in Expression Hierarchy
- External rules treated as ATOM type
- Example: `external special_expr ::= meta_special_expr`
- Meta rule provides the actual parsing: `meta_special_expr ::= 'multiply' '(' simple_ref_expr ',' mul_expr ')' {elementType="special_expr" pin=2}`

---

## User-Configurable Attributes (Expression-Specific)

| Attribute | Values | Default | Scope | Effect |
|-----------|--------|---------|-------|--------|
| `rightAssociative` | `true`/`false` | `false` | rule | Right-associative binary operator |
| `extends` | rule name or pattern | none | rule/global | PSI hierarchy + AST collapsing |
| `extraRoot` | `true`/`false` | `false` | rule | Marks additional expression root |
| `consumeTokenMethod` | method name | `consumeToken` | rule/global | Token matching method for performance |
| `name` | string | rule name | rule/global | Display name in error messages |
| `elementType` | type name | auto | rule | Shared element type for PSI unification |

---

## IDE Features for Expression Parsing

- Quick Documentation (Ctrl-Q/Cmd-J): shows priority table with operator types
- Priority table highlights current rule in blue
- Live Preview (Ctrl-Alt-P/Cmd-Alt-P): test expression grammars interactively
- Structure view shows expression PSI tree structure
- Inspection: detects left recursion (BnfLeftRecursion)

---

## Warning Messages Users May See

- `'<rule>' priority is calculated twice` — rule appears in multiple priority groups
- `'<rule>' is in several expression hierarchies: X and Y` — intersecting expression roots
- `'<rule>' is not an expression rule nor private priority group` — rule doesn't extend root
- `invalid expression definition for <rule>: 2 or more arguments expected` — malformed expression rule
- `binary or n-ary expression cannot have prefix, treating as ATOM` — first element isn't root ref
- `binary expression needs operator, treating as ATOM` — no operator between operands
- `'<root> ( <op> <root>) +' expected for N-ary operator, treating as POSTFIX` — wrong N-ary syntax
- `unexpected cardinality <X> of <root>, treating as ATOM` — unexpected root rule reference count

---

## Example Locations

### Primary Expression Grammar
- `testData/generator/ExprParser.bnf` — Complete expression parser with all operator types
- `testData/generator/ExprParser.expected.java` — Generated parser with priority table
- `testData/generator/ExprParser.PSI.expected.java` — Generated PSI types

### Traditional (left modifier) Approach
- `testData/generator/LeftAssociative.bnf` — `left`, `inner`, `private left` combinations
- `testData/livePreview/LivePreviewTutorial.bnf` — Tutorial grammar with `left` expression rules

### Additional Expression Examples
- `testData/fleet/FleetExprParser.bnf` — Fleet variant of expression parser (identical structure)
- `testData/livePreview/Case153.bnf` — Minimal expression grammar with `extends`
- `testData/generator/SelfFlex.expected.java` (line 1767+) — Another expression root priority table
- `testData/generator/PsiGen.bnf` — Expression rules with `extends` pattern

### Attribute Descriptions
- `resources/messages/attributeDescriptions/rightAssociative.html`
- `resources/messages/attributeDescriptions/extends.html`
- `resources/messages/attributeDescriptions/consumeTokenMethod.html`
- `resources/messages/attributeDescriptions/extraRoot.html`
- `resources/messages/attributeDescriptions/name.html`

---

## Out of Scope

Features found but excluded (belong to other sections):
- `pin` attribute mechanics → Section 2.4 (Error Recovery)
- `recoverWhile` attribute → Section 2.4 (Error Recovery)
- Basic rule syntax (`::=`, `|`, `?`, `+`, `*`) → Section 2.1 (BNF Grammar Syntax)
- `private`, `fake`, `left`, `inner` modifier definitions → Section 2.1 (BNF Grammar Syntax)
- `meta` rules and `external` rules → Section 2.6 (External Rules)
- PSI hierarchy design with `fake` rules and `methods` → Section 3.4 (PSI Customization)
- `mixin` and `implements` attributes → Section 3.4 (PSI Customization)
- `stubClass` attribute → Section 3.4 (PSI Customization)

---

## Missing Documentation

- No explicit user docs for non-associative operator pattern
- No docs explaining how `arg1`/`arg2` substitution narrows parsing (between_expr pattern)
- No docs for multiple expression roots in same grammar (only brief mention: "there can be any number")
- No docs explaining the `leftMarkerIs` type constraint mechanism for call_expr
- No visual diagram of deep vs flat PSI tree comparison
- N-ary operator syntax requirement (`(<op> expr)+`) only mentioned in passing
- No docs for how `paren_expr` is classified as PREFIX (not ATOM) in priority table
