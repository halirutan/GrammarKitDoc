# Section 2.7: Grammar Composition — Code Evidence

## 1. Grammar Splitting via `parserClass`

**Source: `resources/messages/attributeDescriptions/parserClass.html`**

> The generated parser class qualified name. Can be used several times in a large grammar to split parsing code into different classes and files.

```bnf
{
  classHeader="license.txt"
  parserClass="org.intellij.grammar.parser.GrammarParser"
  parserUtilClass="org.intellij.grammar.parser.GrammarParserUtil"
}

...

// parsing code for the rest of the grammar will be in a separate file
// (semicolon is required to make this attributes global for sure)
;{
  parserClass="org.intellij.grammar.parser.GrammarParser2"
}
```

Key rule: the semicolon before the `{` is required to make the attributes block global (not attached to the previous rule).

## 2. Generated Parser Structure

**Source: `README.md:202-208`**

> The generator can split parser code into several classes for better support of large grammars.

In simple cases, a parser consists of several generated classes. The actual error recovery/reporting code, parser-based completion support, and token matching code reside in the `parserUtilClass`.

## 3. Multi-Parser Grammar in Practice

### ExternalRules.bnf — Three Parser Classes

**Source: `testData/generator/ExternalRules.bnf:1-99`**

Demonstrates a grammar split across three parser classes:

```bnf
{
  parserClass="ExternalRules"
  ...
}
// Rules here generate into ExternalRules.java

;{
  parserClass="ExternalRules2"
}
// Rules here generate into ExternalRules2.java
private one_list ::= <<listOf one>>
extra_root ::= {extraRoot=true}

;{
  parserClass="ExternalRules3"
}
// Rules here generate into ExternalRules3.java
private meta third_class_meta ::= <<fmp>>
```

### Cross-Class Meta Rule References

```bnf
// In ExternalRules (main class):
private meta main_class_meta ::= <<p>>
private second_class_meta_usage_from_main ::= <<comma_list <<second_class_meta some>>>>

// In ExternalRules2:
private meta second_class_meta ::= <<bmp>>
private main_class_meta_usage_from_second ::= <<comma_list <<main_class_meta some>>>>
private third_class_meta_usage_from_second ::= <<comma_list <<third_class_meta some>>>>

// In ExternalRules3:
private meta third_class_meta ::= <<fmp>>
private second_class_meta_usage_from_third ::= <<comma_list <<second_class_meta some>>>>
```

This shows meta rules defined in one parser class can be referenced from another.

### ExternalRulesLambdas.bnf — Lambda Variant

**Source: `testData/generator/ExternalRulesLambdas.bnf:78-92`**

Same multi-parser pattern with Java 8 lambdas:
```bnf
;{
  parserClass="ExternalRulesLambdas2"
}
// ...
;{
  parserClass="ExternalRulesLambdas3"
}
```

## 4. PsiGen.bnf — Two-Class Split with Shared Grammar

**Source: `testData/generator/PsiGen.bnf:1-76`**

```bnf
{
  parserClass="PsiGen"
  ...
}
// Main parser class with expression grammar, external types, etc.

;{
  parserClass="PsiGen2"
}
// Second parser class with reference and literal rules
meta blockOf ::= <<p>> +
private reference ::= ref_expr qref_expr *
ref_expr ::= identifier {extends="expr" mixin="MyRefImpl" implements="MyRef"}

;{
  parserClass="PsiGenFixes"
  extends(".*statement")=statement
}
// Third parser class with statement rules
```

Key observations:
- Attributes like `extends` can be redefined in each parser class section.
- PSI configuration (`psiClassPrefix`, `psiPackage`, etc.) is shared across all parser classes.
- Each parser class section can have its own attribute overrides.

## 5. Grammar.bnf — Self-Describing Grammar

**Source: `grammars/Grammar.bnf:1-54`**

The Grammar-Kit BNF grammar itself demonstrates grammar composition patterns:

```bnf
{
  classHeader="license.txt"
  generate=[java="8" names="long" visitor-value="R"]
  parserClass="org.intellij.grammar.parser.GrammarParser"
  parserUtilClass="org.intellij.grammar.parser.GrammarParserUtil"
  implements="org.intellij.grammar.psi.BnfComposite"
  extends="org.intellij.grammar.psi.impl.BnfCompositeImpl"
  psiClassPrefix="Bnf"
  psiImplClassSuffix="Impl"
  psiPackage="org.intellij.grammar.psi"
  psiImplPackage="org.intellij.grammar.psi.impl"
  psiImplUtilClass="org.intellij.grammar.psi.impl.GrammarPsiImplUtil"
  elementTypeHolderClass="org.intellij.grammar.psi.BnfTypes"
  elementTypePrefix="BNF_"
  elementTypeClass="org.intellij.grammar.psi.BnfCompositeElementType"
  tokenTypeClass="org.intellij.grammar.psi.BnfTokenType"
}
```

Uses `external` root rule for custom parsing:
```bnf
external grammar ::= parseGrammar grammar_element
```

This delegates the top-level parsing to `GrammarParserUtil.parseGrammar()`.

## 6. JFlex.bnf — Companion Grammar

**Source: `grammars/JFlex.bnf:1-80`**

Independent grammar for JFlex file support with its own complete configuration:

```bnf
{
  classHeader="license.txt"
  generate=[java="8" names="long" visitor-value="R"]
  parserClass="org.intellij.jflex.parser.JFlexParser"
  parserUtilClass="org.intellij.jflex.parser.JFlexParserUtil"
  implements="org.intellij.jflex.psi.JFlexComposite"
  extends="org.intellij.jflex.psi.impl.JFlexCompositeImpl"
  psiClassPrefix="JFlex"
  psiImplClassSuffix="Impl"
  psiPackage="org.intellij.jflex.psi"
  psiImplPackage="org.intellij.jflex.psi.impl"
  psiImplUtilClass="org.intellij.jflex.psi.impl.JFlexPsiImplUtil"
  elementTypeHolderClass="org.intellij.jflex.psi.JFlexTypes"
  elementTypePrefix="FLEX_"
  elementTypeClass="org.intellij.jflex.psi.JFlexCompositeElementType"
  tokenTypeClass="org.intellij.jflex.psi.JFlexTokenType"
}
```

Key observations:
- Completely separate namespace from Grammar.bnf.
- Different PSI prefix (`JFlex` vs `Bnf`).
- Different element type prefix (`FLEX_` vs `BNF_`).
- Shows how two grammars can coexist in the same plugin with no conflicts.

## 7. Shared Token Configuration

**Source: `README.md:172-186`**

Tokens can be defined in the global `tokens` attribute:
```bnf
{
  tokens = [
    PLUS='+'
    MINUS='-'
  ]
}
```

When splitting a grammar, the token definitions from the first `tokens` block apply to all parser classes. Token element types are generated once in the `elementTypeHolderClass`.

## 8. ExtraRoot for Additional Entry Points

**Source: `resources/messages/attributeDescriptions/extraRoot.html`**

> Marks a rule as an extra root rule, so it will be added to `parse_extra_roots()` method.

```bnf
{
  extraRoot("my_named")=true
}
```

**Source: `testData/generator/ExternalRules.bnf:93`**
```bnf
extra_root ::= {extraRoot=true}
```

Extra roots allow a single grammar to define multiple parsing entry points. This is useful when different parts of a file need independent parsing (e.g., embedded code blocks).

## 9. Generator File Structure

**Source: `src/org/intellij/grammar/generator/ParserGenerator.java:277-341`**

The `generate()` method produces files in this order:
1. **Parser class(es)** — via `generateParser()`, one per `parserClass` value
2. **ElementTypes holder class** — contains IElementType constants and PSI factory
3. **PSI interface classes** — one per non-private, non-fake rule with PSI
4. **PSI implementation classes** — corresponding Impl classes
5. **Visitor class** — if `generate=[visitor="yes"]`

## 10. RuleInfo: Per-Rule Composition Data

**Source: `src/org/intellij/grammar/generator/ParserGenerator.java:60-93`**

Each rule tracks:
- `parserClass` — which parser file it belongs to
- `intfPackage` / `implPackage` — where PSI classes go
- `intfClass` / `implClass` — fully qualified PSI class names
- `elementType` — the IElementType constant name

Rules can have different `parserClass` values, but PSI settings are typically shared.

## 11. Pattern-Based Attribute Application

**Source: `README.md:122-129`**

Attributes can be applied to multiple rules at once using regex patterns:
```bnf
{
  extends(".*_expr")=expr        // applies to all .*_expr rules
  pin(".*_list(?:_\d+)*")=1      // applies to all .*_list rules and their sub-expressions
}
```

This is a key composition mechanism: define behavioral patterns that span across the grammar.

## 12. Modular Design Patterns

From the test data and source analysis, these composition patterns emerge:

1. **Single grammar, multiple parser classes**: Use `;{ parserClass="..." }` to split generated code.
2. **Shared PSI across parser classes**: PSI configuration is defined once at the top.
3. **Cross-class references**: Rules from different parser classes can reference each other (including meta rules).
4. **Multiple independent grammars**: Each grammar has its own complete configuration (as shown by Grammar.bnf and JFlex.bnf).
5. **External delegation**: Use `external` rules to delegate to hand-written parsing code.
6. **Extra roots**: Define multiple entry points within a single grammar.
