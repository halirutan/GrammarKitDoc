# References: BNF Grammar Syntax

## Internal File References (Verified)

### Grammar Definition Files
| File | Path | Status | Notes |
|------|------|--------|-------|
| Grammar.bnf | `grammars/Grammar.bnf` | Verified | Self-defining BNF grammar; 123 lines; defines all syntax constructs |
| BnfConstants.java | `src/org/intellij/grammar/psi/BnfConstants.java` | Verified | Constants including `REGEXP_PREFIX`, `RECOVER_AUTO` |
| KnownAttribute.java | `src/org/intellij/grammar/KnownAttribute.java` | Verified | All 38+ known attributes with types and defaults |
| BnfFileType.java | `src/org/intellij/grammar/BnfFileType.java` | Verified | Registers `.bnf` file extension |

### Test Data Files
| File | Path | Status | Notes |
|------|------|--------|-------|
| Small.bnf | `testData/generator/Small.bnf` | Verified | 28 lines; empty rules, private rules, token references, left/inner modifiers |
| ExternalRules.bnf | `testData/generator/ExternalRules.bnf` | Verified | 100 lines; meta rules, external rules, `;{` section separators, parameter passing |
| ExprParser.bnf | `testData/generator/ExprParser.bnf` | Verified | 76 lines; expression parsing with all operator types, `extends`, `fake`, `extraRoot` |
| LeftAssociative.bnf | `testData/generator/LeftAssociative.bnf` | Verified | 11 lines; `left`, `inner`, `private left` modifier combinations |
| UpperRules.bnf | `testData/generator/UpperRules.bnf` | Verified | 23 lines; `upper` modifier with `extends` pattern |
| PsiGen.bnf | `testData/generator/PsiGen.bnf` | Verified | 76 lines; fake rules, multiple parser classes via `;{}`, elementType="" |
| AutoRecovery.bnf | `testData/generator/AutoRecovery.bnf` | Verified | 6 lines; `#auto` recoverWhile example |
| Autopin.bnf | `testData/generator/Autopin.bnf` | Verified | 31 lines; pattern-based pin, `extends` on statements |
| Json.bnf | `testData/livePreview/Json.bnf` | Verified | 27 lines; complete JSON grammar with regexp tokens |
| LivePreviewTutorial.bnf | `testData/livePreview/LivePreviewTutorial.bnf` | Verified | 43 lines; TUTORIAL.md's sample grammar |
| AlternativeSyntax.bnf | `testData/parser/AlternativeSyntax.bnf` | Referenced | Alternative syntax forms including `<>` in rule names |

### Documentation Files
| File | Path | Status | Notes |
|------|------|--------|-------|
| README.md | `README.md` | Verified | Primary syntax overview (lines 80-251); rule modifiers, tokens, attributes |
| TUTORIAL.md | `TUTORIAL.md` | Verified | 130 lines; sample grammar walkthrough with Live Preview |
| HOWTO.md | `HOWTO.md` | Verified | 431 lines; parser basics, recoverWhile, external rules, expression parsing |

### Attribute Description Files
| File | Path | Status | Notes |
|------|------|--------|-------|
| tokens.html | `resources/messages/attributeDescriptions/tokens.html` | Verified | Token declaration syntax; confirms regexp tokens required for Live Preview |
| name.html | `resources/messages/attributeDescriptions/name.html` | Verified | Display name for error messages |
| pin.html | `resources/messages/attributeDescriptions/pin.html` | Verified | Pin contract and parenthesized list example |
| recoverWhile.html | `resources/messages/attributeDescriptions/recoverWhile.html` | Verified | Recovery contract, `#auto` = `! FOLLOWS(rule)` |
| extends.html | `resources/messages/attributeDescriptions/extends.html` | Verified | PSI hierarchy + AST collapsing |
| extendedPin.html | `resources/messages/attributeDescriptions/extendedPin.html` | Verified | Default true; generates sequence tail parsing |
| parserImports.html | `resources/messages/attributeDescriptions/parserImports.html` | Verified | Static imports for external rule resolution |
| consumeTokenMethod.html | `resources/messages/attributeDescriptions/consumeTokenMethod.html` | Verified | `consumeToken` vs `consumeTokenFast` |

---

## External References

### Foundational Concepts
- **PEG (Parsing Expression Grammar)**: <https://en.wikipedia.org/wiki/Parsing_expression_grammar>
  - Referenced in README.md line 82: "See Parsing Expression Grammar (PEG) for basic syntax"
  - Grammar-Kit uses PEG semantics: `::=` replaces PEG `←`; ordered choice, not ambiguous

### Grammar-Kit Project
- **GitHub repository**: <https://github.com/JetBrains/Grammar-Kit>
- **Plugin page**: <https://plugins.jetbrains.com/plugin/6606>
- **Gradle plugin**: <https://github.com/JetBrains/gradle-grammar-kit-plugin>

### IntelliJ Platform SDK
- **Custom Language Support Tutorial**: <https://plugins.jetbrains.com/docs/intellij/custom-language-support-tutorial.html>
  - Referenced in README.md line 33
- **PsiBuilder documentation**: <https://plugins.jetbrains.com/docs/intellij/implementing-parser-and-psi.html>
- **ParserDefinition**: <https://plugins.jetbrains.com/docs/intellij/language-and-filetype.html>

### JFlex
- **JFlex documentation**: <https://jflex.de/manual.html>
  - Referenced in README.md line 240 for regexp subset limitations

---

## Key Technical Claims Verified Against Source

### Grammar File Structure
| Claim | Source | Verified |
|-------|--------|----------|
| `.bnf` file extension | `BnfFileType.java` | Yes |
| Grammar contains attrs or rules | `Grammar.bnf:59` — `private grammar_element ::= !<<eof>> (attrs \| rule)` | Yes |
| `::=` is the rule definition operator | `Grammar.bnf:24` — `OP_IS="::="` | Yes |
| `=` is for attribute assignment only | `Grammar.bnf:23` — `OP_EQ="="` | Yes |
| Optional trailing `;` on rules | `Grammar.bnf:64` — `rule ::= rule_start expression attrs? ';'?` | Yes |

### Token Definitions
| Claim | Source | Verified |
|-------|--------|----------|
| Tokens declared via `tokens=[...]` | `Grammar.bnf:22-47`, `tokens.html` | Yes |
| Regexp prefix `regexp:` | `Grammar.bnf:41-46`, confirmed `BnfConstants.java:16` | Yes |
| Name-only tokens allowed | `tokens.html:10` — `string  // no value or pattern` | Yes |
| Recommended to use token values over names | `README.md:177` | Yes |
| Implicit unquoted tokens: name equals value | `README.md:181` | Yes |
| Text-matched tokens are slower | `README.md:182-183` | Yes |

### Rule Modifiers
| Claim | Source | Verified |
|-------|--------|----------|
| 7 modifiers: private, left, inner, upper, meta, external, fake | `Grammar.bnf:66-67` | Yes |
| `inner` only with `left` | `README.md:143` | Yes |
| `private left` = `private left inner` | `README.md:144` | Yes |
| `fake` should not combine with `private` | `README.md:145` | Yes |
| First rule is implicitly private | `HOWTO.md:232` | Yes |

### Quantifiers and Grouping
| Claim | Source | Verified |
|-------|--------|----------|
| `?`, `+`, `*` as quantifiers | `Grammar.bnf:104` — `quantifier ::= '?' \| '+' \| '*'` | Yes |
| `[expr]` is shorthand for `(expr)?` | `Grammar.bnf:121`, `README.md:83,94` | Yes |
| `{expr \| expr}` for choices | `Grammar.bnf:120`, `README.md:83,96` | Yes |

### Predicates
| Claim | Source | Verified |
|-------|--------|----------|
| `&` and-predicate (lookahead) | `Grammar.bnf:106-107` | Yes |
| `!` not-predicate (negative lookahead) | `Grammar.bnf:106-107` | Yes |
| Predicates do not consume input | `TUTORIAL.md:22`, PEG semantics | Yes |

### External and Meta Rules
| Claim | Source | Verified |
|-------|--------|----------|
| `<< >>` external expression syntax | `Grammar.bnf:114` | Yes |
| `<<eof>>` tests end of input | `Grammar.bnf:59`, `TUTORIAL.md:110` | Yes |
| Meta rules use `<<param>>` syntax | `ExternalRules.bnf:38`, `README.md:155` | Yes |
| Double-quoted strings passed "as is" | `README.md:165-168` | Yes |
| Single-quoted strings unquoted first | `README.md:167` | Yes |
| `<<>>` empty external expression valid | `ExternalRules.bnf:75` | Yes |

### `;{` Section Separator
| Claim | Source | Verified |
|-------|--------|----------|
| `;{` starts new attributes section | `ExternalRules.bnf:84-86` | Yes |
| Splits grammar into multiple parser classes | `ExternalRules.bnf` shows 3 classes: `ExternalRules`, `ExternalRules2`, `ExternalRules3` | Yes |
| Also used in PsiGen.bnf | `PsiGen.bnf:39-41,57-59` — 3 classes: `PsiGen`, `PsiGen2`, `PsiGenFixes` | Yes |

### Empty Rules and Edge Cases
| Claim | Source | Verified |
|-------|--------|----------|
| `empty ::= ()` is valid | `Small.bnf:17` | Yes |
| `empty2 ::= {}` is valid | `Small.bnf:18` | Yes |
| `empty3 ::= []` is valid | `Small.bnf:19` | Yes |
| `&()` always-true predicate | `Small.bnf:22` | Yes |
| `!()` always-false predicate | `Small.bnf:23` | Yes |
| `[({})]` nested empty groupings valid | `Small.bnf:24` | Yes |
