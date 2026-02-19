# References: Error Recovery

## Internal File References (Verified)

### Primary Recovery Examples
| File | Path | Status | Notes |
|------|------|--------|-------|
| AutoRecovery.bnf | `testData/generator/AutoRecovery.bnf` | Verified | 6 lines; `#auto` recovery with parenthesized list |
| AutoRecovery.expected.java | `testData/generator/AutoRecovery.expected.java` | Verified | Generated code showing `#auto` predicate: `item_auto_recover_` lambda |
| Autopin.bnf | `testData/generator/Autopin.bnf` | Verified | 31 lines; numeric pin, regex-pattern pin, global pin patterns |
| Autopin.expected.java | `testData/generator/Autopin.expected.java` | Verified | Generated code for various pin patterns |
| Json.bnf | `testData/livePreview/Json.bnf` | Verified | 27 lines; complete JSON grammar with pin + recoverWhile + shared recovery |
| LivePreviewTutorial.bnf | `testData/livePreview/LivePreviewTutorial.bnf` | Verified | 43 lines; property recovery pattern from TUTORIAL.md |

### Live Preview Test Data (Recovery Behavior)
| File | Path | Status | Notes |
|------|------|--------|-------|
| AutoRecovery.live.txt | `testData/livePreview/AutoRecovery.live.txt` | Verified | 4 lines of broken input: `(1, 2, 3);\n;\n(-, , 3, );\n(1)` |
| AutoRecovery.txt | `testData/livePreview/AutoRecovery.txt` | Verified | 44 lines; expected PSI tree with recovery; shows PsiErrorElement and ITEM nodes preserved |
| JsonRecovery.live.txt | `testData/livePreview/JsonRecovery.live.txt` | Verified | 14 lines; 12 error scenarios: missing name, missing colon, missing value, extra tokens, etc. |
| JsonRecovery.txt | `testData/livePreview/JsonRecovery.txt` | Verified | 189 lines; expected PSI tree for broken JSON; demonstrates PROP/NAME nodes preserved despite errors |

### Documentation Files
| File | Path | Status | Notes |
|------|------|--------|-------|
| README.md | `README.md` | Verified | Error recovery attributes (lines 187-200): pin, recoverWhile, name |
| TUTORIAL.md | `TUTORIAL.md` | Verified | Pin/recoverWhile explanation (lines 6-24), sample grammar (lines 84-127) |
| HOWTO.md | `HOWTO.md` | Verified | recoverWhile contract (lines 73-93), parser basics (lines 18-70) |

### Source Code
| File | Path | Status | Notes |
|------|------|--------|-------|
| GeneratedParserUtilBase.java | `src/org/intellij/grammar/parser/GeneratedParserUtilBase.java` | Referenced | Error message formatting (lines 783-797, 994-1009); `eof()` (lines 109-111); token matching; recovery runtime |
| ParserGenerator.java | `src/org/intellij/grammar/generator/ParserGenerator.java` | Referenced | Pin code generation (lines 799-818); recoverWhile code gen (lines 870-886); #auto generation (lines 896-923) |
| ParserGeneratorUtil.java | `src/org/intellij/grammar/generator/ParserGeneratorUtil.java` | Referenced | PinMatcher class (lines 784-813); modifier logic |
| BnfConstants.java | `src/org/intellij/grammar/psi/BnfConstants.java` | Referenced | `RECOVER_AUTO = "#auto"` (line 40) |
| KnownAttribute.java | `src/org/intellij/grammar/KnownAttribute.java` | Referenced | Pin attribute (line 59), extendedPin (line 35), RIGHT_ASSOCIATIVE |
| BnfUnusedRuleInspection.java | `src/org/intellij/grammar/inspection/BnfUnusedRuleInspection.java` | Referenced | "Non-private recovery rule" warning (lines 105-108) |
| BnfPinMarkerAnnotator.java | `src/org/intellij/grammar/editor/BnfPinMarkerAnnotator.java` | Referenced | Pin marker highlighting (lines 56-60) |
| BnfAnnotator.java | `src/org/intellij/grammar/editor/BnfAnnotator.java` | Referenced | Recover marker highlighting (lines 162-167) |
| BnfDocumentationProvider.java | `src/org/intellij/grammar/BnfDocumentationProvider.java` | Referenced | FIRST/FOLLOWS display, #auto expansion (lines 40-69) |

### Attribute Description Files
| File | Path | Status | Notes |
|------|------|--------|-------|
| pin.html | `resources/messages/attributeDescriptions/pin.html` | Verified | Pin contract: "Pin is applied to items of grammar sequence expressions"; parenthesized list example |
| recoverWhile.html | `resources/messages/attributeDescriptions/recoverWhile.html` | Verified | Recovery contract: "regardless of the result parser will continue to consume tokens while the predicate rule matches"; `#auto` = `! FOLLOWS(rule)` |
| extendedPin.html | `resources/messages/attributeDescriptions/extendedPin.html` | Verified | "Generate code for parsing a sequence tail even if some parts are missing if it is already pinned. The value is **true** by default" |
| name.html | `resources/messages/attributeDescriptions/name.html` | Verified | Display name: "expected <rule name>"; empty string suppresses short error message |
| consumeTokenMethod.html | `resources/messages/attributeDescriptions/consumeTokenMethod.html` | Verified | `consumeTokenFast` for recovery rules and expressions |

---

## External References

### Grammar-Kit Project
- **GitHub repository**: <https://github.com/JetBrains/Grammar-Kit>
- **Plugin page**: <https://plugins.jetbrains.com/plugin/6606>

### IntelliJ Platform SDK
- **Error Recovery**: <https://plugins.jetbrains.com/docs/intellij/implementing-parser-and-psi.html>
- **PsiBuilder**: <https://plugins.jetbrains.com/docs/intellij/implementing-parser-and-psi.html>
- **PsiErrorElement**: Part of IntelliJ Platform PSI API

### Parser Theory
- **PEG (Parsing Expression Grammar)**: <https://en.wikipedia.org/wiki/Parsing_expression_grammar>
- **Error Recovery in Parsers**: General concept — Grammar-Kit implements pin-based and predicate-based recovery

---

## Key Technical Claims Verified Against Source

### Pin Mechanics
| Claim | Source | Verified |
|-------|--------|----------|
| Pin applies to sequence expression items | pin.html: "Pin is applied to items of grammar sequence expressions" | Yes |
| Parser ignores errors after pinned item | pin.html: "parser will ignore errors after a pinned item" | Yes |
| Numeric pin: `{pin=2}` — 1-indexed | README.md line 191, pin.html | Yes |
| Pattern pin: `{pin="rule_B"}` — regex match | README.md line 191 | Yes |
| Sub-expression pin: `{pin(".*")=1}` | README.md lines 192-193 | Yes |
| Last item pin is trivial and skipped | ParserGeneratorUtil.java `shouldGenerate` | Yes (referenced) |

### ExtendedPin
| Claim | Source | Verified |
|-------|--------|----------|
| Default: true | extendedPin.html: "The value is **true** by default" | Yes |
| Tries to match rest of sequence after pin | extendedPin.html, TUTORIAL.md lines 11-12 | Yes |
| Generated pattern: `pinned_ && report_error_()` | ParserGenerator.java lines 799-818 | Yes (referenced) |
| Stops matching on first failure if pin not reached | TUTORIAL.md line 12 | Yes |

### RecoverWhile
| Claim | Source | Verified |
|-------|--------|----------|
| Rule handled as usual, then recovery runs regardless of result | recoverWhile.html: "regardless of the result" | Yes |
| Should be on rule inside a loop | recoverWhile.html, HOWTO.md line 76 | Yes |
| Rule should have pin somewhere | recoverWhile.html, HOWTO.md line 77 | Yes |
| Value is predicate rule or "#auto" | recoverWhile.html, BnfConstants.java line 40 | Yes |
| Predicate leaves input intact | recoverWhile.html, HOWTO.md line 78 | Yes |
| `#auto` means `! FOLLOWS(rule)` | recoverWhile.html: "Name of the recovery predicate rule or '#auto' which means '! FOLLOWS(rule)'" | Yes |

### Recovery Predicates
| Claim | Source | Verified |
|-------|--------|----------|
| Always a NOT predicate | TUTORIAL.md line 22, HOWTO.md line 90 | Yes — all examples use `!(...)` |
| Must be private | BnfUnusedRuleInspection.java lines 105-108 | Yes — "Non-private recovery rule" warning |
| Tokens = boundary tokens where parsing resumes | HOWTO.md line 90, recoverWhile.html | Yes |

### #auto Recovery
| Claim | Source | Verified |
|-------|--------|----------|
| Special constant `"#auto"` | BnfConstants.java line 40 | Yes |
| Generates `!nextTokenIsFast(builder_, TOKEN1, TOKEN2, ...)` | AutoRecovery.expected.java line 155 | Yes (referenced) |
| Tokens from FOLLOWS set | recoverWhile.html, ParserGenerator.java lines 896-923 | Yes |
| Quick Documentation shows expanded predicate | BnfDocumentationProvider.java lines 56-69 | Yes (referenced) |

### Error Message Formats
| Claim | Source | Verified |
|-------|--------|----------|
| `"<expected> expected"` format | AutoRecovery.txt: `"number expected, got '-'"` | Yes |
| `"<expected> expected, got '<actual>'"` format | AutoRecovery.txt: `"number expected, got ','"` | Yes |
| `"'<actual>' unexpected"` format | JsonRecovery.txt line 137: `"'6' unexpected"` | Yes |
| `name` attribute changes error text | JsonRecovery.txt line 9: `"<name> expected, got ':'"` | Yes — confirms `<name>` format |
| Empty `name` suppresses short error | name.html: "For an empty string short error message will not be generated" | Yes |

### Pin IDE Features
| Claim | Source | Verified |
|-------|--------|----------|
| Pin marker highlighting in editor | README.md line 67: "pinned expression markers (tooltip shows pin value in charge)" | Yes |
| Tooltip shows pin value | README.md line 67 | Yes |

### Recovery Test Results
| Claim | Source | Verified |
|-------|--------|----------|
| AutoRecovery preserves ITEM nodes despite errors | AutoRecovery.txt lines 31-33: ITEM node present with number '3' after error | Yes |
| JsonRecovery preserves PROP nodes despite missing parts | JsonRecovery.txt: PROP nodes present even with missing names/values | Yes |
| PsiErrorElement wraps skipped tokens | AutoRecovery.txt lines 23-24: `PsiErrorElement` with `BAD_CHARACTER('-')` | Yes |
| Multiple error scenarios handled | JsonRecovery.live.txt: 12 distinct error patterns | Yes |

### Statement-Level Recovery Pattern
| Claim | Source | Verified |
|-------|--------|----------|
| Pattern: `script ::= statement *` + private statement + recoverWhile | HOWTO.md lines 88-93 | Yes — exact pattern shown |
| Pin on each concrete statement | HOWTO.md line 91: `select_statement ::= SELECT ... {pin=1}` | Yes |
| Comment: "something has to be pinned!" | HOWTO.md line 91 | Yes |

### Property Recovery Pattern
| Claim | Source | Verified |
|-------|--------|----------|
| Pattern: `root_item ::= !<<eof>> property ';' {pin=1 recoverWhile=...}` | TUTORIAL.md line 110 | Yes |
| `property ::= id '=' expr {pin=2}` | TUTORIAL.md line 112 | Yes |
| Recovery: `!(';' \| id '=')` | TUTORIAL.md line 113 | Yes |

### Parenthesized List Recovery Pattern
| Claim | Source | Verified |
|-------|--------|----------|
| Pattern: `list ::= "(" [!")" item (',' item) *] ")" {pin(".*")=1}` | AutoRecovery.bnf line 5, pin.html, recoverWhile.html | Yes — identical in all three sources |
| `item ::= number {recoverWhile="#auto"}` | AutoRecovery.bnf line 6 | Yes |
| Manual equivalent: `item_recover ::= !(")" \| ",")` | pin.html, recoverWhile.html | Yes |

### JSON Recovery Pattern
| Claim | Source | Verified |
|-------|--------|----------|
| `prop ::= [] name ':' value {pin=1 recoverWhile=recover}` | Json.bnf line 24 | Yes |
| `[]` makes name optional | Json.bnf line 24 comment: "remove [] to make NAME mandatory" | Yes |
| Shared recover predicate | Json.bnf line 26: `private recover ::= !(',' \| ']' \| '}' \| '[' \| '{')` | Yes |
| `name` attribute for clean errors | Json.bnf line 25: `{name="name"}`, line 19: `{name="value"}` | Yes |
