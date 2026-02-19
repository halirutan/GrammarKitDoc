# References: Designing Grammar Rules

## Internal File References (Verified)

### Primary Grammar Examples
| File | Path | Status | Notes |
|------|------|--------|-------|
| Grammar.bnf | `grammars/Grammar.bnf` | Verified | Self-defining grammar; demonstrates top-down design, private helpers, recovery, pin patterns |
| Json.bnf | `testData/livePreview/Json.bnf` | Verified | 27 lines; well-structured JSON grammar with lists, objects, shared recovery |
| ExprParser.bnf | `testData/generator/ExprParser.bnf` | Verified | 76 lines; expression parsing with private priority groups, extends pattern |
| LivePreviewTutorial.bnf | `testData/livePreview/LivePreviewTutorial.bnf` | Verified | 43 lines; TUTORIAL.md's sample grammar; property parsing with recovery |

### Design Pattern Examples
| File | Path | Status | Notes |
|------|------|--------|-------|
| Small.bnf | `testData/generator/Small.bnf` | Verified | Basic patterns: private rules, empty rules, token references |
| Autopin.bnf | `testData/generator/Autopin.bnf` | Verified | Pattern-based pin attributes, extends on statements, CREATE TABLE pattern |
| AutoRecovery.bnf | `testData/generator/AutoRecovery.bnf` | Verified | Auto-recovery with `#auto` recoverWhile |
| ExternalRules.bnf | `testData/generator/ExternalRules.bnf` | Verified | Meta rules, comma_list pattern, reusable patterns, grammar sections |
| PsiGen.bnf | `testData/generator/PsiGen.bnf` | Verified | PSI-oriented design: fake rules, extends, elementType, multiple parser classes |
| UpperRules.bnf | `testData/generator/UpperRules.bnf` | Verified | Upper modifier usage with recovery and extends |
| LeftAssociative.bnf | `testData/generator/LeftAssociative.bnf` | Verified | Left, inner, private left modifier combinations |

### Documentation Files
| File | Path | Status | Notes |
|------|------|--------|-------|
| README.md | `README.md` | Verified | Syntax overview, rule modifiers, token recommendations, error recovery attributes |
| TUTORIAL.md | `TUTORIAL.md` | Verified | Live Preview workflow, sample grammar design, pin/recoverWhile explanation |
| HOWTO.md | `HOWTO.md` | Verified | Parser basics, recoverWhile contract, external rules, expression parsing, PSI hierarchy |

### Source Code (Inspections and IDE Features)
| File | Path | Status | Notes |
|------|------|--------|-------|
| BnfLeftRecursionInspection | `src/org/intellij/grammar/inspection/` | Referenced | Left recursion detection |
| BnfUnusedRuleInspection | `src/org/intellij/grammar/inspection/` | Referenced | Unused/unreachable rule detection; non-private recovery rule warning |
| BnfDocumentationProvider | `src/org/intellij/grammar/BnfDocumentationProvider.java` | Referenced | Quick Documentation: FIRST/FOLLOWS, priority tables, #auto expansion |
| RuleGraphHelper | `src/org/intellij/grammar/analysis/RuleGraphHelper.java` | Referenced | First rule implicitly private (line 827-828) |

### Attribute Description Files
| File | Path | Status | Notes |
|------|------|--------|-------|
| extends.html | `resources/messages/attributeDescriptions/extends.html` | Verified | PSI hierarchy and AST collapsing |
| name.html | `resources/messages/attributeDescriptions/name.html` | Verified | Display name for error messages |
| pin.html | `resources/messages/attributeDescriptions/pin.html` | Verified | Pin contract with list example |
| recoverWhile.html | `resources/messages/attributeDescriptions/recoverWhile.html` | Verified | Recovery contract, `#auto` |
| consumeTokenMethod.html | `resources/messages/attributeDescriptions/consumeTokenMethod.html` | Verified | Performance optimization |

---

## External References

### Grammar-Kit Project
- **GitHub repository**: <https://github.com/JetBrains/Grammar-Kit>
- **Plugin page**: <https://plugins.jetbrains.com/plugin/6606>
- **Gradle plugin**: <https://github.com/JetBrains/gradle-grammar-kit-plugin>

### IntelliJ Platform SDK
- **Custom Language Support Tutorial**: <https://plugins.jetbrains.com/docs/intellij/custom-language-support-tutorial.html>
- **Implementing Parser and PSI**: <https://plugins.jetbrains.com/docs/intellij/implementing-parser-and-psi.html>

### PEG Theory
- **PEG (Parsing Expression Grammar)**: <https://en.wikipedia.org/wiki/Parsing_expression_grammar>
  - Grammar-Kit uses PEG semantics: ordered choice, first match wins

### Open-Source Grammars Built with Grammar-Kit
- **Clojure-Kit**: <https://github.com/gregsh/Clojure-Kit>
- **intellij-rust**: <https://github.com/intellij-rust/intellij-rust>
- **intellij-erlang**: <https://github.com/ignatov/intellij-erlang>
- **intellij-elm**: <https://github.com/intellij-elm/intellij-elm>
- **intellij-elixir**: <https://github.com/KronicDeth/intellij-elixir>

---

## Key Technical Claims Verified Against Source

### Grammar Architecture
| Claim | Source | Verified |
|-------|--------|----------|
| First rule is implicitly private | `HOWTO.md:232`, `RuleGraphHelper.java:827-828` | Yes |
| Root rule typically delegates to private helper | `Grammar.bnf:59`, `Json.bnf:17`, `TUTORIAL.md:109` | Yes — all examples show this pattern |
| Each public rule produces a PSI node | `README.md:133`, `HOWTO.md:232` | Yes |
| Private rules create no PSI node | `README.md:133` | Yes |
| Grammar can be split across parser classes | `ExternalRules.bnf:84-99`, `PsiGen.bnf:39-41,57-59` | Yes — both show `;{parserClass="..."}` |

### Rule Organization
| Claim | Source | Verified |
|-------|--------|----------|
| Rule names use snake_case | All test grammars | Yes — `literal_expr`, `root_item`, `property_recover` |
| Generated methods follow rule names | `README.md:113-120` | Yes |
| Sub-expression naming: `rule_name_0`, `rule_name_N1_N2_NX` | `README.md:116-118` | Yes |
| Avoid naming rules like generated sub-expressions | `README.md:120` | Yes |
| PSI class names derived via CamelCase | Observed in generated code | Yes — `literal_expr` → `LiteralExpr` |
| `name` attribute overrides error display | `name.html`, `README.md:199-200` | Yes |

### Common Patterns
| Claim | Source | Verified |
|-------|--------|----------|
| Comma-separated list: `<<param>> (',' <<param>>) *` | `ExternalRules.bnf:38` | Yes — exact pattern |
| Parenthesized list: `'(' [!')' item (',' item) *] ')' {pin(".*")=1}` | `AutoRecovery.bnf:5`, `pin.html`, `recoverWhile.html` | Yes |
| Trailing comma: `(',' (element \| &')'))` | `HOWTO.md:394` | Yes |
| JSON object pattern with `!'}' ` lookahead | `Json.bnf:23` | Yes |
| `prop ::= [] name ':' value {pin=1}` makes name optional | `Json.bnf:24` | Yes — comment confirms |
| Statement recovery: private choice + recoverWhile | `HOWTO.md:88-93` | Yes |
| Property recovery: `!(';' \| id '=')` | `TUTORIAL.md:17` | Yes |

### Best Practices
| Claim | Source | Verified |
|-------|--------|----------|
| Use `private` for structural grouping | `HOWTO.md:232` | Yes — "Specify *private* as early as possible" |
| Use `extends` to flatten AST | `HOWTO.md:233-237` | Yes — shows FileNode/LiteralExpr vs FileNode/Expr/LiteralExpr |
| `consumeTokenFast` for recovery and expressions | `consumeTokenMethod.html` | Yes — exact patterns documented |
| Pattern-based attributes for multiple rules | `README.md:122-128` | Yes |
| Text-matched tokens slower than IElementType | `README.md:182-183` | Yes |

### IDE Features
| Claim | Source | Verified |
|-------|--------|----------|
| Quick Documentation shows FIRST/FOLLOWS | `README.md:69` | Yes |
| Live Preview: Ctrl-Alt-P | `README.md:71`, `TUTORIAL.md:45` | Yes |
| Grammar Highlighting: Ctrl-Alt-F7 | `README.md:72`, `TUTORIAL.md:49` | Yes |
| Extract Rule refactoring: Ctrl-Alt-M | `README.md:59` | Yes |
| Introduce Token: Ctrl-Alt-C | `README.md:60` | Yes |
| Flip choice branches: Alt-Enter | `README.md:61` | Yes |
| Structure popup: Ctrl-F12 | `README.md:63` | Yes |

### Pitfalls
| Claim | Source | Verified |
|-------|--------|----------|
| Left recursion causes StackOverflowError | PEG/recursive descent theory; `HOWTO.md:5-6` | Yes |
| Left recursion exception for expression parsing | `ExprParser.bnf:25` — "left recursion and empty PSI children define expression root" | Yes |
| PEG ordered choice: first match wins | `README.md:82` | Yes |
| Writing grammar ≠ working parser | `HOWTO.md:5-6` | Yes — "The tricky part is to *tune*" |
| `pin` reduces backtracking | `TUTORIAL.md:9-12` | Yes |
| `extendedPin` default is true | `extendedPin.html` | Yes — "The value is **true** by default" |
