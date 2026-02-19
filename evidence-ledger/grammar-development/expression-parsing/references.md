# References: Expression Parsing

## Internal File References (Verified)

### Primary Expression Grammar
| File | Path | Status | Notes |
|------|------|--------|-------|
| ExprParser.bnf | `testData/generator/ExprParser.bnf` | Verified | 76 lines; complete expression parser: BINARY, PREFIX, POSTFIX, N_ARY, ATOM, ternary, call, qualification, between, is-not |
| ExprParser.expected.java | `testData/generator/ExprParser.expected.java` | Verified | Generated parser with priority table comment, 2-method structure for expr root |
| ExprParser.PSI.expected.java | `testData/generator/ExprParser.PSI.expected.java` | Verified | Generated PSI types and element type constants |

### Traditional (left Modifier) Approach
| File | Path | Status | Notes |
|------|------|--------|-------|
| LeftAssociative.bnf | `testData/generator/LeftAssociative.bnf` | Verified | 11 lines; `left`, `inner`, `private left` modifier combinations |
| LivePreviewTutorial.bnf | `testData/livePreview/LivePreviewTutorial.bnf` | Verified | 43 lines; TUTORIAL.md grammar using traditional `left` expression rules |

### Additional Expression Examples
| File | Path | Status | Notes |
|------|------|--------|-------|
| Case153.bnf | `testData/livePreview/Case153.bnf` | Verified | 15 lines; minimal expression grammar with `extends` |
| PsiGen.bnf | `testData/generator/PsiGen.bnf` | Verified | Expression rules with `extends` pattern, `cast_expr`, `item_expr` |

### Documentation Files
| File | Path | Status | Notes |
|------|------|--------|-------|
| README.md | `README.md` | Verified | Rule modifiers (lines 131-147), meta rules (149-157) |
| HOWTO.md | `HOWTO.md` | Verified | Section 2.4: compact expression parsing with priorities (lines 121-223); Section 3.1: PSI basics with extends (lines 229-250) |
| TUTORIAL.md | `TUTORIAL.md` | Verified | Traditional expression grammar example (lines 115-127) |

### Source Code
| File | Path | Status | Notes |
|------|------|--------|-------|
| ExpressionHelper.java | `src/org/intellij/grammar/analysis/ExpressionHelper.java` | Referenced | `OperatorType` enum: ATOM, PREFIX, POSTFIX, BINARY, N_ARY; operator detection logic |
| ExpressionGeneratorHelper.java | `src/org/intellij/grammar/generator/ExpressionGeneratorHelper.java` | Referenced | Priority table generation; `expr()` and `expr_0()` method generation |
| BnfDocumentationProvider.java | `src/org/intellij/grammar/BnfDocumentationProvider.java` | Referenced | `dumpPriorityTable()` for Quick Documentation priority display |

### Attribute Description Files
| File | Path | Status | Notes |
|------|------|--------|-------|
| rightAssociative.html | `resources/messages/attributeDescriptions/rightAssociative.html` | Verified | "Mark operator as right-associative, i.e. a = b = c should be equal to a = (b = c)" |
| extends.html | `resources/messages/attributeDescriptions/extends.html` | Verified | "AST nodes produced by rules extending the same rule will be collapsed by parser" |
| extraRoot.html | `resources/messages/attributeDescriptions/extraRoot.html` | Verified | "Marks a rule as an extra root rule" for `parse_extra_roots()` method |
| consumeTokenMethod.html | `resources/messages/attributeDescriptions/consumeTokenMethod.html` | Verified | `consumeTokenFast` pattern for expressions |
| name.html | `resources/messages/attributeDescriptions/name.html` | Verified | Display name for error messages |

---

## External References

### Pratt Parsing
- **Top Down Operator Precedence (Crockford)**: <http://javascript.crockford.com/tdop/tdop.html>
  - Referenced in HOWTO.md line 200: "a procedural rewrite of the Pratt parsing described here"
- **Pratt Parsing (Wikipedia)**: <https://en.wikipedia.org/wiki/Operator-precedence_parser#Pratt_parsing>

### Grammar-Kit Project
- **GitHub repository**: <https://github.com/JetBrains/Grammar-Kit>
- **ExprParser.bnf (direct link)**: <https://github.com/JetBrains/Grammar-Kit/blob/master/testData/generator/ExprParser.bnf>
  - Referenced in HOWTO.md line 137: "complete example"

### IntelliJ Platform SDK
- **Custom Language Support Tutorial**: <https://plugins.jetbrains.com/docs/intellij/custom-language-support-tutorial.html>
- **PSI Tree Structure**: <https://plugins.jetbrains.com/docs/intellij/psi.html>

---

## Key Technical Claims Verified Against Source

### Expression Parsing Framework
| Claim | Source | Verified |
|-------|--------|----------|
| Two approaches: traditional (left) and Pratt/priority (extends) | HOWTO.md lines 121-179 vs TUTORIAL.md lines 115-127 | Yes — both demonstrated |
| Pratt approach: "compact expression parsing with priorities" | HOWTO.md line 121 | Yes |
| Generated parser is "procedural rewrite of Pratt parsing" | HOWTO.md line 199 | Yes |
| Only 2 methods generated for root rule | HOWTO.md line 201, ExprParser.expected.java | Yes — `expr()` and `expr_0()` |

### Operator Types
| Claim | Source | Verified |
|-------|--------|----------|
| ATOM: no reference to root expr | ExprParser.bnf:52 — `literal_expr ::= number` | Yes |
| PREFIX: root expr after operator | ExprParser.bnf:54 — `unary_min_expr ::= '-' expr` | Yes |
| POSTFIX: root expr before operator | ExprParser.bnf:65 — `factorial_expr ::= expr '!'` | Yes |
| BINARY: two root expr references | ExprParser.bnf:63 — `plus_expr ::= expr '+' expr` | Yes |
| N_ARY: uses `(<op> expr)+` syntax | ExprParser.bnf:64 — `exp_expr ::= expr ('**' expr) +` | Yes — comment confirms |
| `paren_expr` classified as PREFIX | HOWTO.md priority table line 213 — `PREFIX(paren_expr)` | Yes |

### Priority Table
| Claim | Source | Verified |
|-------|--------|----------|
| Priority increases top to bottom | HOWTO.md line 131: "Priority increases from top to bottom" | Yes |
| Priority 0 = lowest (first alternative) | ExprParser.expected.java priority table comment | Yes — assign_expr at 0 |
| Private groups share same priority | ExprParser.bnf:42-44 — `private mul_group ::= mul_expr \| div_expr` | Yes |
| Generated priority table in parser comments | HOWTO.md lines 203-213 | Yes |

### Associativity
| Claim | Source | Verified |
|-------|--------|----------|
| Left associativity by default | HOWTO.md line 134, rightAssociative.html | Yes |
| `rightAssociative=true` for right associativity | ExprParser.bnf:58 — `assign_expr ::= expr '=' expr { rightAssociative=true }` | Yes |
| rightAssociative.html describes contract | "a = b = c should be equal to a = (b = c)" | Yes |
| No explicit non-associative attribute | ExprParser.bnf uses same-level choices for comparisons | Yes — implicit pattern |

### AST Flattening
| Claim | Source | Verified |
|-------|--------|----------|
| Without extends: deep tree `FileNode/Expr/AddExpr/MulExpr/LiteralExpr` | HOWTO.md line 237 | Yes |
| With extends: flat tree `FileNode/LiteralExpr` | HOWTO.md line 237 | Yes |
| `extends(".*_expr")=expr` collapses redundant nodes | extends.html: "AST nodes produced by rules extending the same rule will be collapsed" | Yes |
| Root expression rule never appears in AST | HOWTO.md line 130: "root expression rule node will never appear in AST" | Yes |

### Expression Root Detection
| Claim | Source | Verified |
|-------|--------|----------|
| Left recursion + empty PSI children define expression root | ExprParser.bnf:25 — comment confirms | Yes |
| `extraRoot=true` marks additional expression roots | ExprParser.bnf:37 — `{extraRoot=true}` on `expr` | Yes |
| Expression hierarchies must not intersect | HOWTO.md line 189: "as long as they do not intersect" | Yes |

### Complex Expressions
| Claim | Source | Verified |
|-------|--------|----------|
| Ternary (elvis): `expr '?' expr ':' expr` | ExprParser.bnf:67 — `elvis_expr ::= expr '?' expr ':' expr` | Yes |
| Call expression: `ref_expr arg_list` | ExprParser.bnf:50 — `call_expr ::= ref_expr arg_list` | Yes |
| Qualification: `expr '.' identifier` | ExprParser.bnf:49 — `qualification_expr ::= expr '.' identifier` | Yes |
| Between: specific expr rule for operands | ExprParser.bnf:69 — `between_expr ::= expr BETWEEN add_group AND add_group` | Yes |
| Fake rules for PSI unification | ExprParser.bnf:47-48 — `fake ref_expr` + `simple_ref_expr` with `elementType=ref_expr` | Yes |
| External expression as ATOM | ExprParser.bnf:74 — `external special_expr ::= meta_special_expr` | Yes |

### Performance
| Claim | Source | Verified |
|-------|--------|----------|
| `consumeTokenMethod(".*_expr\|expr")="consumeTokenFast"` | HOWTO.md lines 193-196, consumeTokenMethod.html | Yes |
| Reason: "no one really needs to know that + - * / are expected at any offset" | consumeTokenMethod.html | Yes |
