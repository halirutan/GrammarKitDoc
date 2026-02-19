# Code Evidence: Error Recovery

## Scope Information
This evidence covers section 2.4: Error Recovery

INCLUDES: Error recovery fundamentals, pin attribute mechanics, recoverWhile predicates, advanced recovery patterns, testing and validation
EXCLUDES: Grammar syntax (2.1), grammar design (2.2), expression parsing (2.3)

---

## Error Recovery Fundamentals

### Why Recovery Matters
- Without recovery: parser stops matching on any failure
- With `pin`: parser considers match successful even if only pinned prefix matches
- With `recoverWhile`: parser skips unexpected tokens to resynchronize
- Recovery enables: partial PSI trees, error highlighting, code completion in broken code
- Source: TUTORIAL.md lines 8-24

### Two Core Strategies
- **Pin** = handles input that *misses* some parts (incomplete input)
- **RecoverWhile** = handles input that *includes* something unexpected (extra tokens)
- Source: TUTORIAL.md lines 14, 24

### Error Message Formats (User-Visible)
- `"<expected> expected"` — when expected token missing at EOF
- `"<expected> expected, got '<actual>'"` — when wrong token found
- `"'<actual>' unexpected"` — when no expected tokens known
- `"unmatched input"` — when nothing expected and nothing found
- Max error token text display: 20 characters
- Max variants in error message: 50 (then `" and ..."`)
- Multiple expected tokens joined with `", "` and last with `" or"`
- Source: GeneratedParserUtilBase.java lines 783-797, 53-54, 994-1009

### IDE User Experience
- Error elements appear as `PsiErrorElement` in PSI tree
- Skipped tokens wrapped in error markers with descriptive messages
- Recovery preserves PSI structure for code completion and navigation
- Brace matching awareness during recovery (parenCount tracking)
- Source: GeneratedParserUtilBase.java lines 572-577

---

## Pin Attribute Mechanics

### Basic Pin Contract
- Applied to items of grammar **sequence** expressions only
- Parser ignores errors after pinned item in a sequence
- Sequence matches if prefix up to pinned item matches
- Source: pin.html, README.md lines 188-193

### Pin Value Formats
- **Numeric**: `{pin=2}` — pins at the 2nd item (1-indexed)
- **Pattern**: `{pin="rule_B"}` — pins at item matching regex pattern
- **Pattern on sub-expressions**: `{pin(".*")=1}` — applies pin=1 to all sub-sequences
- Pin value is 1-indexed (pin=1 means first item, pin=2 means second item)
- Source: KnownAttribute.java line 59, PinMatcher class lines 784-813

### Pin Matching Logic
- Numeric: matches when `i == pinIndex - 1` (0-indexed internal)
- Pattern: matches when `pinPattern.matcher(child.getText()).matches()`
- Last item pin is trivial and skipped (`shouldGenerate` skips last expression)
- Source: ParserGeneratorUtil.java lines 802-811

### ExtendedPin Mode
- Global attribute: `extendedPin` (default: **true**)
- When ON: parser tries to match rest of sequence even after failures past pin point
- When OFF: parser stops matching on first failure if pinned part not reached
- Uses `report_error_()` to continue matching after pin with error reporting
- Source: TUTORIAL.md lines 11-12, KnownAttribute.java line 35, extendedPin.html

### ExtendedPin Generated Code Pattern
- After pin applied, subsequent items use `report_error_()` wrapper
- Pattern: `result_ = pinned_ && report_error_(builder_, <next_call>) && result_;`
- Last child in sequence: no `report_error_()` wrapper
- Source: ParserGenerator.java lines 799-818

### Pin in Global Attributes (Pattern Targeting)
- `pin("create_.*_statement")=".*_ref"` — pin by pattern on matching rules
- `pin(".*_list(?:_\\d+)*")=1` — pin=1 on all list rules and sub-expressions
- `pin("override.*")=1` — pin=1 on all override rules
- Source: Autopin.bnf lines 6-8, README.md lines 127-128

### Pin IDE Features
- **Pin marker highlighting**: pinned expressions highlighted in editor
- Customizable color: Settings > Colors and Fonts > "Pin marker" (`BNF_PIN`)
- Tooltip shows: pin value in charge (e.g., `pin=2`)
- Annotation message: "Pinned" (first pin) or "Pinned again" (nested pin)
- Source: BnfPinMarkerAnnotator.java lines 56-60, BnfColorSettingsPage.java line 50, README.md line 67

### Pin Return Value
- Pinned rule returns `result_ || pinned_` (true if pin point was reached)
- Source: ParserGenerator.java line 890

---

## RecoverWhile Predicates

### Basic RecoverWhile Contract
1. The attributed rule is handled as usual
2. **Regardless** of the result, parser continues to consume tokens while predicate rule matches
- Source: recoverWhile.html, HOWTO.md lines 81-85

### RecoverWhile Usage Rules
1. Should be specified on a rule that is **inside a loop**
2. That rule should always have `pin` attribute somewhere as well
3. Attribute value should be a **predicate rule** (leaves input intact)
4. In most cases the predicate is `! FOLLOWS(rule)` — can be copied from Quick Documentation
- Source: recoverWhile.html, HOWTO.md lines 76-79

### RecoverWhile Value Formats
- **Rule reference**: `recoverWhile=my_recover_rule` — names a predicate rule
- **#auto**: `recoverWhile="#auto"` — auto-generates `! FOLLOWS(rule)` predicate
- **Meta parameter**: `recoverWhile="<<param>>"` — for meta rules, uses parameter as predicate
- Source: BnfConstants.java line 40, ParserGenerator.java lines 873-878

### Writing Recovery Predicates
- Always a NOT predicate: `private rule_recover ::= !(token1 | token2 | ...)`
- Predicate must be **private** (inspection warns: "Non-private recovery rule")
- Tokens in predicate = boundary tokens where parsing should resume
- Predicate does NOT consume input — it only tests
- Source: TUTORIAL.md line 22, BnfUnusedRuleInspection.java lines 106-107

### Common Predicate Patterns
- Statement recovery: `!(';' | KEYWORD1 | KEYWORD2 | ...)` — stop at delimiters or next statement start
- List item recovery: `!(',' | ')' | ']' | '}')` — stop at separator or closing bracket
- Property recovery: `!(';' | id '=')` — stop at delimiter or next property start
- Source: TUTORIAL.md lines 17-18, HOWTO.md lines 88-93

### #auto Recovery
- Value: `"#auto"` — special string constant
- Generates: `!nextTokenIsFast(builder_, TOKEN1, TOKEN2, ...)` predicate
- Tokens computed from: `FOLLOWS(rule)` — the NEXT set of the rule
- Generated predicate name: `<rule_name>_auto_recover_`
- Warning on failure: `"<rule_name> #auto recovery generation failed: <reason>"`
- Ignores: left-recursive rules, EOF, NOTHING matches in FOLLOWS set
- Source: ParserGenerator.java lines 896-923, BnfConstants.java line 40

### #auto in Quick Documentation
- When `recoverWhile="#auto"`, Quick Documentation (Ctrl-Q/Cmd-J) shows:
  - `#auto recovery predicate:` section
  - Expanded predicate: `private <rule>_recover ::= !(token1 | token2 | ...)`
- Source: BnfDocumentationProvider.java lines 56-69

### RecoverWhile IDE Features
- **Recover marker highlighting**: rules with recoverWhile highlighted in editor
- Customizable color: Settings > Colors and Fonts > "Recover marker" (`BNF_RECOVER_MARKER`)
- Source: BnfAnnotator.java lines 162-167, BnfColorSettingsPage.java line 51

### RecoverWhile Generated Code
- Recovery predicate passed as lambda to `exit_section_()`
- For `#auto`: generates `static final Parser item_auto_recover_ = (builder_, level_) -> !nextTokenIsFast(builder_, TOKEN1, TOKEN2, ...);`
- For named rule: generates wrapped call to the predicate rule
- Source: AutoRecovery.expected.java line 155, ParserGenerator.java lines 870-886

---

## Name Attribute (Error Reporting)

### Purpose
- Controls display name in error messages: `"expected <rule name>"`
- Without `name`: error lists all expected tokens individually
- With `name`: error shows single descriptive name instead
- Empty string value: suppresses short error message entirely
- Source: name.html, README.md lines 199-200

### Syntax
- Per-rule: `operator ::= '+' | '-' | '*' | '/' {name="operator"}`
- Pattern-based: `name(".*expr")='expression'`
- Value can be text or a rule reference
- Source: name.html, TUTORIAL.md line 105

### Effect on Error Messages
- Without name: `"'+', '-', '*', '/' expected"`
- With `name="operator"`: `"<operator> expected"`
- Names wrapped in angle brackets in error messages when starting with letter or `<`
- Source: GeneratedParserUtilBase.java lines 1002-1004

---

## consumeTokenMethod (Performance Optimization)

### Relationship to Error Recovery
- `consumeToken` (default): records error reporting information (variants)
- `consumeTokenFast`: skips error reporting — better performance, no error messages
- Use `consumeTokenFast` for recovery rules and expression operators
- Source: consumeTokenMethod.html, GeneratedParserUtilBase.java lines 214-228

### Patterns
- `consumeTokenMethod(".*_recover")="consumeTokenFast"` — skip reporting in recovery rules
- `consumeTokenMethod(".*_expr|expr")="consumeTokenFast"` — skip reporting in expressions
- Source: consumeTokenMethod.html, README.md lines 193-197

---

## Advanced Recovery Patterns

### Combining Pin and RecoverWhile
- Pin handles missing parts; recoverWhile handles extra tokens
- Typical pattern: pin on the rule, recoverWhile on the loop item
- Source: TUTORIAL.md lines 16-21

### Statement-Level Recovery Pattern
```
script ::= statement *
private statement ::= select_statement | delete_statement | ... {recoverWhile="statement_recover"}
private statement_recover ::= !(';' | SELECT | DELETE | ...)
select_statement ::= SELECT ... {pin=1}
```
- recoverWhile on the private choice rule (loop item)
- pin on each concrete statement variant
- Source: HOWTO.md lines 88-93

### Property/Assignment Recovery Pattern
```
root ::= root_item *
private root_item ::= !<<eof>> property ';' {pin=1 recoverWhile=property_recover}
property ::= id '=' expr {pin=2}
private property_recover ::= !(';' | id '=')
```
- Outer loop item has recoverWhile
- Inner property has pin=2 (commits at '=')
- `!<<eof>>` guard prevents infinite loop
- Source: TUTORIAL.md lines 110-113

### Parenthesized List Recovery Pattern
```
list ::= "(" [!")" item (',' item) * ] ")" {pin(".*")=1}
item ::= number {recoverWhile=item_recover}
private item_recover ::= !(")" | ",")
```
- `pin(".*")=1` pins all sub-sequences at first item
- `!")"` lookahead prevents matching empty list as error
- recoverWhile on each item stops at comma or closing paren
- Source: pin.html, recoverWhile.html

### Parenthesized List with #auto Recovery
```
list ::= "(" [!")" item (',' item) * ] ")" {pin(".*")=1}
item ::= number {recoverWhile="#auto"}
```
- #auto computes: `!nextTokenIsFast(builder_, PAREN2, COMMA, SEMI)`
- Equivalent to manual `!(")" | "," | ";")`
- Source: AutoRecovery.bnf, AutoRecovery.expected.java line 155

### JSON Object Recovery Pattern
```
object ::= '{' [!'}' prop (!'}' ',' prop) *] '}' {pin(".*")=1}
prop ::= [] name ':' value {pin=1 recoverWhile=recover}
name ::= id | string {name="name"}
private recover ::= !(',' | ']' | '}' | '[' | '{')
```
- `prop ::= []` with `pin=1`: empty optional makes prop always pinned (name becomes optional)
- Shared recover predicate across array items and object props
- `name` attribute on `name` rule: errors show `<name> expected` instead of `id, string expected`
- Source: Json.bnf lines 23-26

### Trailing Comma Pattern
```
element_list ::= '(' element (',' (element | &')'))* ')' {pin(".*")=1}
```
- `&')'` and-predicate allows trailing comma before closing paren
- Source: HOWTO.md lines 386-395

### Multi-Level Recovery
- Outer recovery (statement level) catches what inner recovery misses
- Inner recovery (item level) handles item-specific errors
- Recovery predicates should not overlap — inner boundaries subset of outer
- Source: derived from Json.bnf pattern (array items + object props + top-level)

---

## Testing and Validation

### Live Preview for Recovery Testing
- Open: Ctrl-Alt-P / Cmd-Alt-P
- Structure toolwindow shows PSI tree with error elements
- File Structure popup: Ctrl-F12 / Cmd-F12
- PSI Viewer dialog for detailed inspection
- Grammar Highlighting: Ctrl-Alt-F7 / Cmd-Alt-F7 in preview editor
- Source: TUTORIAL.md lines 45-49, README.md lines 38, 71-72

### PSI Tree Validation
- Successful recovery: rule nodes present despite errors
- Error elements: `PsiErrorElement` with descriptive messages
- Skipped tokens: wrapped in error markers
- Recovery preserves parent structure (e.g., list still contains items)
- Source: AutoRecovery.txt, JsonRecovery.txt

### Quick Documentation for Recovery
- Ctrl-Q / Cmd-J on a rule shows:
  - "Starts with:" (FIRST set)
  - "Followed by:" (FOLLOWS/NEXT set)
  - "#auto recovery predicate:" (when recoverWhile="#auto")
- FOLLOWS set = what #auto uses for recovery predicate
- Source: BnfDocumentationProvider.java lines 40-69, README.md line 69

### Inspections Related to Recovery
- **"Non-private recovery rule"**: recovery predicate rules should be `private`
- **"Unused rule"**: detects recovery rules not referenced by any recoverWhile
- Source: BnfUnusedRuleInspection.java lines 105-108

### Error Message Validation
- `name` attribute controls error message text
- Without name: lists all expected token alternatives
- With name: shows `<name> expected` (cleaner messages)
- Empty name string: suppresses short error message
- Source: name.html, GeneratedParserUtilBase.java lines 733-744

---

## Example Locations

### Primary Examples
- `testData/generator/AutoRecovery.bnf`: #auto recovery with parenthesized list
- `testData/generator/AutoRecovery.expected.java`: generated code showing #auto predicate
- `testData/generator/Autopin.bnf`: pin patterns (numeric, regex, global)
- `testData/generator/Autopin.expected.java`: generated code for pin patterns
- `testData/livePreview/Json.bnf`: complete JSON grammar with pin + recoverWhile
- `testData/livePreview/AutoRecovery.bnf`: live preview version of auto recovery
- `testData/livePreview/AutoRecovery.live.txt`: broken input for auto recovery testing
- `testData/livePreview/AutoRecovery.txt`: expected PSI tree with recovery
- `testData/livePreview/JsonRecovery.live.txt`: broken JSON input (12 error scenarios)
- `testData/livePreview/JsonRecovery.txt`: expected PSI tree for broken JSON

### Tutorial Examples
- TUTORIAL.md: `sample.bnf` — expression language with pin and recoverWhile
- HOWTO.md: statement-level recovery pattern (script/statement/select)

---

## Out of Scope

Features found but excluded (belong to other sections):
- Grammar syntax (::=, |, *, +, ?, etc.) → Section 2.1
- Rule modifiers (private, left, meta, external, fake) → Section 2.1/2.2
- Expression parsing with priorities → Section 2.3
- PSI hierarchy and extends/implements → Section 3.x
- Stub indices support → Section 3.x
- Live Preview full workflow → Section 2.5
- External rules → Section 2.6
- JFlex lexer generation → Section 4.x
- Gradle/build integration → Section 6.x

---

## Missing Documentation

- No user docs for: how `extendedPin=false` changes behavior in detail
- No user docs for: meta rule parameter as recoverWhile value (`<<param>>`)
- No user docs for: brace-aware recovery (parenCount tracking in runtime)
- No user docs for: `DUMMY_BLOCK` element type used during recovery token consumption
- No user docs for: interaction between `consumeTokenMethod` and error recovery quality
- No user docs for: `parseAsTree` recovery mechanism (tree-shaped error recovery)
- No user docs for: maximum error variants display limit (50) or token text limit (20 chars)
- Attribute `name` with empty string value behavior underdocumented
