# Code Evidence: Designing Grammar Rules

## Scope Information
This evidence covers section 2.2: Designing Grammar Rules

---

## Grammar Architecture Principles

### Top-Down Design
- First rule in grammar is the root entry point
- First rule is implicitly treated as root: no PSI class generated for it (`RuleGraphHelper.java:827-828`)
- Root rule typically delegates to a `private` helper with a loop: `root ::= root_item *`
- Grammar.bnf pattern: `external grammar ::= parseGrammar grammar_element`
- Json.bnf pattern: `root ::= json`
- Tutorial pattern: `root ::= root_item *`

### Identifying Language Constructs
- Each public rule produces a PSI node in the tree
- Each public rule generates an `IElementType` constant
- Private rules are structural helpers: no PSI node created
- Users decide what appears in PSI tree by choosing `private` vs public
- HOWTO guidance: "Specify *private* attribute on any rule if you don't want it to be present in AST as early as possible"

### Separation of Concerns
- Grammar rules define parsing structure
- Attributes control code generation behavior
- Handwritten classes and generated classes should be in different source roots (HOWTO I.3)
- Grammar manipulation is "a higher level of abstraction" over generated code (HOWTO I.2)
- Parser splits across classes for large grammars via `parserClass` attribute with `;{}` separator

---

## Rule Organization

### Naming Conventions
- Rule names use `snake_case`: `property_recover`, `root_item`, `literal_expr`
- Generated methods follow rule names: `static boolean rule_name(..)`
- Sub-expressions generate: `rule_name_0(..)`, `rule_name_N1_N2_..._NX(..)`
- WARNING: Naming a rule like `rule_name_N1_N2_..._NX` should be avoided (conflicts with generated sub-expression names)
- PSI class names derived from rule names via CamelCase: `literal_expr` -> `LiteralExpr`
- `name` attribute overrides display name in error messages: `name(".*expr")='expression'`
- `name` attribute value: text string or rule reference
- Empty `name` string suppresses short error message generation

### Private vs Public Rules
- By default, rules are public (non-private, non-fake, etc.)
- `private` modifier: skip PSI node creation, children included in parent
- `private` rules do not generate PSI classes or IElementType constants
- First rule is implicitly private (no PSI generated for root)
- Common pattern: `private` helper rules group alternatives
  - `private primary_group ::= simple_ref_expr | literal_expr | paren_expr`
  - `private unary_group ::= unary_plus_expr | unary_min_expr`
  - `private mul_group ::= mul_expr | div_expr`
- `private` rules used for recovery predicates: `private statement_recover ::= !(';' | SELECT | DELETE | ...)`
- `private` rules used for operator grouping in expressions

### Rule Modifiers (Complete List)
- `private` (PSI tree): skip node creation, children go to parent
- `left` (PSI tree): take left sibling AST node, become its parent
- `inner` (PSI tree): take left sibling, inject into it as child
- `upper` (PSI tree): take parent node, replace it by adopting children
- `meta` (parser): parametrized rule, parse function takes other parse functions
- `external` (parser): hand-written parse function, no code generated
- `fake` (PSI classes): only PSI classes generated, no parsing code
- Modifier combinations: `inner` only with `left`; `private left` = `private left inner`; `fake` not with `private`

### Rule Grouping Strategies
- Grammar.bnf groups: tokens block, then rules by function
- Pattern: root rule -> private dispatch -> public leaf rules
- Expression grammars: root expr -> private priority groups -> public operator rules
- Recovery rules placed near the rules they recover
- Attribute blocks can be placed at top (global) or after rules (local)
- Grammar can be split across parser classes using `;{ parserClass="..." }` separator

### Documentation Practices
- BNF comments: `// line comment` and `/* block comment */`
- Quick Documentation (Ctrl-Q/Cmd-J) shows FIRST/FOLLOWS sets for rules
- Quick Documentation shows attribute descriptions
- Quick Documentation shows expression priority table for expression rules
- Quick Documentation shows `#auto` recovery predicate expansion

---

## Common Patterns

### Lists and Separators
- Comma-separated list: `<<param>> (',' <<param>>) *`
- Meta rule for reuse: `meta comma_list ::= <<param>> (',' <<param>>) *`
- Usage: `option_list ::= <<comma_list (OPTION1 | OPTION2 | OPTION3)>>`
- Parenthesized list: `list ::= '(' [!')' item (',' item) *] ')' {pin(".*")=1}`
- Trailing commas: `element_list ::= '(' element (',' (element | &')'))* ')' {pin(".*")=1}`
- Auto-recovery list: `item ::= number {recoverWhile="#auto"}`
- Pinned comma-separated list with recovery:
  ```
  list ::= "(" [!")" item (',' item) * ] ")" {pin(".*")=1}
  item ::= number {recoverWhile=item_recover}
  private item_recover ::= !(")" | ",")
  ```

### Optional Elements
- Quantifier `?`: `rule_B ::= [ optional_token ] and_another_one?`
- Bracket syntax: `[expression]` equivalent to `(expression)?`
- Optional in sequence: `create_table_statement ::= CREATE TEMP? (GLOBAL|LOCAL) TABLE table_ref '(' ')'`
- Empty optional for "always match": `prop ::= [] name ':' value {pin=1}` (makes name optional)

### Nested Structures
- Parenthesized expressions: `paren_expr ::= '(' expr ')' {pin=1}`
- JSON objects: `object ::= '{' [!'}' prop (!'}' ',' prop) *] '}' {pin(".*")=1}`
- JSON arrays: `array ::= '[' [!']' item (!']' ',' item) *] ']' {pin(".*")=1}`
- Lookahead negation prevents consuming closing delimiter: `!']'` before items

### Statement vs Expression Distinction
- Statements: typically top-level constructs in a loop
  - `script ::= statement *`
  - `private statement ::= select_statement | delete_statement | ...`
- Expressions: recursive structures with operator precedence
  - `expr ::= assign_expr | add_group | mul_group | ...`
- Statements use `recoverWhile` for error recovery between items
- Expressions use `extends` for flat PSI tree

### Block Structures
- Attribute blocks: `attrs ::= '{' attr * '}' {pin=1}`
- Grammar element recovery: `private grammar_element_recover ::= !('{'|rule_start)`
- Nested blocks with pin on opening delimiter

### Declaration Patterns
- Property pattern: `property ::= id '=' expr {pin=2}`
- Recovery after property: `private property_recover ::= !(';' | id '=')`
- Rule definition: `rule ::= rule_start expression attrs? ';'? {pin=2}`
- Pattern: identifier + operator + value, pin on operator

---

## Best Practices

### Rule Granularity
- Each public rule = one PSI node type
- Use `private` for structural grouping that shouldn't appear in PSI
- Use `fake` rules to shape PSI hierarchy without affecting parsing
- HOWTO: "Specify *private* attribute on any rule if you don't want it to be present in AST as early as possible"
- Use `extends` to flatten AST: avoids deep nesting like `FileNode/Expr/AddExpr/MulExpr/LiteralExpr`
- With `extends(".*_expr")=expr`: AST becomes `FileNode/LiteralExpr` (one level deep)

### Token vs Rule Decisions
- Explicit tokens declared in `tokens` attribute: matched by IElementType (fast)
- Quoted implicit tokens (text-matched): slower, matched by text
- Warning shown in editor: "Tokens matched by text are slower than tokens matched by types"
- Unquoted implicit tokens (keywords): names equal their values
- Recommendation: "use values where possible for better readability"
- Names resolve conflicts when unquoted token value matches a rule name
- Rules, tokens, and text-matched tokens have different editor colors

### Performance Considerations
- `consumeTokenMethod` attribute controls token matching performance
  - `consumeToken` (default): records error reporting info
  - `consumeTokenFast`: skips error reporting, faster
  - Pattern: `consumeTokenMethod(".*_recover")="consumeTokenFast"`
  - Pattern: `consumeTokenMethod(".*_expr|expr")="consumeTokenFast"` for expressions
- `first-check` generate option: FIRST-based lookahead optimization (default: 2 tokens)
- Text-matched tokens span multiple real tokens: performance cost
- `extends` attribute: collapses redundant AST nodes, reduces tree depth
- Choice ordering matters: PEG semantics, first match wins

### Maintainability Patterns
- Pattern-based attributes apply to multiple rules at once:
  - `extends(".*_expr")=expr` applies to all `*_expr` rules
  - `pin(".*_list(?:_\\d+)*")=1` applies to all `*_list` rules and sub-expressions
- `name` attribute with pattern: `name(".*expr")='expression'` for cleaner error messages
- Meta rules for reusable patterns: `meta comma_list ::= <<param>> (',' <<param>>) *`
- Grammar split across parser classes for large grammars

---

## Avoiding Common Pitfalls

### Left Recursion Issues
- Inspection: "BnfLeftRecursion" detects left recursion
- Error message: `'<ruleName>' employs left-recursion unsupported by generator`
- Left recursion causes `StackOverflowError` in recursive descent
- Exception: expression parsing with `extends` handles left recursion specially
- Left recursion detection skips `fake` rules
- Left recursion detection skips rules participating in expression parsing
- Solution: use `left` modifier for binary/postfix expressions within expression parsing framework
- Solution: refactor to right-recursive or iterative form

### Ambiguous Grammars
- Inspection: "BnfIdenticalChoiceBranches" detects identical choice branches
- Inspection: "BnfUnreachableChoiceBranch" detects unreachable branches
  - "A branch is unreachable if it is preceded by a branch that matches empty sequences"
- PEG ordered choice: first matching branch wins (not ambiguous in traditional sense)
- Ambiguity manifests as unreachable alternatives

### Token Conflicts
- Inspection: "BnfSuspiciousToken" highlights tokens that look like rule references
- Inspection: "BnfResolve" detects unresolved rule/token references
- Inspection: "BnfDuplicateRule" checks rule name uniqueness
- Quoted vs unquoted tokens have different matching behavior
- Text-matched tokens can span multiple lexer tokens (unexpected behavior)
- Token names resolve conflicts when unquoted value matches a rule name

### Backtracking Problems
- HOWTO I.1: "Writing a grammar doesn't mean the generated parser will work"
- "The tricky part is to *tune* some raw grammar into a *working* grammar"
- Each BNF expression is boolean: true = matched, false = nothing matched (rollback)
- Sequence: fails entirely if any non-pinned part fails (rollback)
- Choice: tries alternatives in order until one matches
- `pin` attribute reduces backtracking: commits after pinned item
- `extendedPin` (default: true): parser tries to match rest of sequence after pin regardless

### Grammar Complexity
- Inspection: "BnfUnusedRule" detects unused/unreachable rules
- Generated sub-expression naming: avoid `rule_name_N1_N2_..._NX` pattern
- Large grammars: split parser across classes with `;{ parserClass="..." }`
- HOWTO: "Once you've mastered some basics, the rest is as easy as combining different blocks"

---

## IDE Features for Grammar Design

### Inspections
- Left recursion detection (warning)
- Suspicious token detection (info)
- Unused rule detection (warning)
- Duplicate rule detection (error)
- Unresolved reference detection (error)
- Identical choice branches (warning)
- Unreachable choice branch (warning)
- Unused attribute detection (warning)

### Editor Support
- Syntax highlighting: different colors for rules, tokens, text-matched tokens, meta rules, meta params
- Pin markers: highlighted in editor, tooltip shows pin value
- Recovery markers: rules with `recoverWhile` get visual marker
- Quick Documentation (Ctrl-Q/Cmd-J): FIRST/FOLLOWS sets, recovery predicates, priority tables
- Structure view (Ctrl-F12): rule and attribute tree
- Refactoring: Extract Rule (Ctrl-Alt-M), Introduce Token (Ctrl-Alt-C)
- Refactoring: Inline Rule (replaces references with rule body)
- Intention: Flip choice branches (Alt-Enter)
- Navigation: Go to related file (Ctrl-Alt-Home) for parser/PSI
- Navigation: Navigate to matched expressions (Ctrl-B inside attribute pattern)
- Find Usages (Alt-F7): rule references, attribute usages

### Live Preview
- Real-time grammar testing without code generation (Ctrl-Alt-P)
- Structure view integration for PSI tree observation
- Grammar highlighting in preview editor (Ctrl-Alt-F7)

---

## Example Locations
- `grammars/Grammar.bnf`: Self-definition, complete grammar architecture example
- `testData/livePreview/Json.bnf`: Well-structured JSON grammar with lists, objects, recovery
- `testData/livePreview/LivePreviewTutorial.bnf`: Tutorial grammar with expressions, recovery
- `testData/generator/ExprParser.bnf`: Expression parsing with priority groups, extends pattern
- `testData/generator/Autopin.bnf`: Pattern-based pin attributes, extends patterns
- `testData/generator/AutoRecovery.bnf`: Auto-recovery with `#auto` recoverWhile
- `testData/generator/PsiGen.bnf`: PSI-oriented design with extends, fake rules, elementType
- `testData/generator/ExternalRules.bnf`: Meta rules, comma_list pattern, reusable patterns
- `testData/generator/Small.bnf`: Basic patterns, empty rules, private rules
- `TUTORIAL.md`: Complete sample.bnf with expression language grammar
- `HOWTO.md`: Statement recovery pattern, expression parsing pattern, PSI hierarchy design

---

## Out of Scope
Features found but excluded (belong to other sections):

### Grammar Syntax Details -> Section 2.1
- Detailed EBNF syntax (sequences, choices, quantifiers, predicates)
- Token definition syntax (`tokens` attribute format)
- External expression syntax (`<< >>`)
- Attribute syntax (braces, name=value pairs)

### Expression Parsing -> Section 2.3
- Priority-based expression parsing with `extends`
- `rightAssociative` attribute
- Left recursion in expression context
- Operator type detection (BINARY, PREFIX, POSTFIX, N_ARY, ATOM)
- Expression root and priority table generation

### Error Recovery -> Section 2.4
- Detailed `pin` attribute mechanics
- Detailed `recoverWhile` attribute mechanics
- `#auto` recovery mode
- `extendedPin` attribute behavior
- Recovery predicate design

### Attribute System -> Section 3.1
- Complete attribute catalog
- Pattern-based attribute application
- Global vs rule-level attributes
- `extends`, `implements`, `mixin`, `methods` details
- `elementType`, `elementTypeFactory`, `stubClass` details
- `generate` options table

---

## Missing Documentation
- No explicit user docs for rule naming best practices beyond generated method naming warning
- No formal guidance on when to use `private` vs public (only HOWTO hints)
- No documentation on grammar file organization conventions (ordering of rules)
- No explicit guidance on choice ordering for performance
- No documentation on maximum grammar complexity limits
- The `upper` modifier has minimal documentation and examples
