# Section 2.7: Grammar Composition — Examples

## Example 1: Splitting a Grammar into Multiple Parser Classes

**Source: `testData/generator/ExternalRules.bnf`**

```bnf
{
  parserClass="ExternalRules"
  parserUtilClass="PsiGenUtil"
  elementTypeHolderClass="ExternalRulesTypes"
}

// Rules here generate into ExternalRules.java
root ::= <<listOf statement>>
external ref ::= parseRef

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

The `;{...}` pattern (semicolon before braces) creates a new global attribute block. Each `parserClass` value produces a separate `.java` file.

## Example 2: Cross-Class Meta Rule Usage

**Source: `testData/generator/ExternalRules.bnf:81-99`**

```bnf
// In ExternalRules (main class):
private meta main_class_meta ::= <<p>>
private second_class_meta_usage_from_main ::= <<comma_list <<second_class_meta some>>>>

;{
  parserClass="ExternalRules2"
}
// In ExternalRules2:
private meta second_class_meta ::= <<bmp>>
private main_class_meta_usage_from_second ::= <<comma_list <<main_class_meta some>>>>
```

Meta rules defined in one parser class can be referenced from another parser class.

## Example 3: Two Independent Grammars in One Plugin

**Source: `grammars/Grammar.bnf` and `grammars/JFlex.bnf`**

Grammar.bnf:
```bnf
{
  parserClass="org.intellij.grammar.parser.GrammarParser"
  psiClassPrefix="Bnf"
  elementTypePrefix="BNF_"
  elementTypeClass="org.intellij.grammar.psi.BnfCompositeElementType"
  tokenTypeClass="org.intellij.grammar.psi.BnfTokenType"
  psiPackage="org.intellij.grammar.psi"
}
```

JFlex.bnf:
```bnf
{
  parserClass="org.intellij.jflex.parser.JFlexParser"
  psiClassPrefix="JFlex"
  elementTypePrefix="FLEX_"
  elementTypeClass="org.intellij.jflex.psi.JFlexCompositeElementType"
  tokenTypeClass="org.intellij.jflex.psi.JFlexTokenType"
  psiPackage="org.intellij.jflex.psi"
}
```

No namespace conflicts because each grammar has distinct prefixes and packages.

## Example 4: Pattern-Based Attribute Application

**Source: `README.md:122-129`**

```bnf
{
  extends(".*_expr")=expr           // all rules ending in _expr extend expr
  pin(".*_list(?:_\\d+)*")=1       // pin first element of all list rules
  elementTypeClass("root_.*")="sample.MyRootType"  // custom type for root_* rules
  elementTypeFactory(".*_expr")="sample.MyTypeFactory.createExprType"  // factory for expressions
  consumeTokenMethod(".*_recover")="consumeTokenFast"  // fast consume in recovery
}
```

## Example 5: ExtraRoot for Multiple Entry Points

**Source: `testData/generator/ExternalRules.bnf:93`, `attributeDescriptions/extraRoot.html`**

```bnf
{
  extraRoot("my_named")=true
}
// or inline:
extra_root ::= some_rule {extraRoot=true}
```

Extra roots generate additional `parse_root_` methods, allowing a single grammar to parse different contexts independently (e.g., embedded code blocks within a larger file).

## Example 6: Multi-Parser with Shared PSI and Override Attributes

**Source: `testData/generator/PsiGen.bnf`**

```bnf
{
  parserClass="PsiGen"
  psiClassPrefix="X"
  psiPackage="generated.psi"
  extends(".*expr")=expr
}
// Main parser class rules...

;{
  parserClass="PsiGen2"
}
// Second parser class, same PSI package
meta blockOf ::= <<p>> +
ref_expr ::= identifier {extends="expr" mixin="MyRefImpl" implements="MyRef"}

;{
  parserClass="PsiGenFixes"
  extends(".*statement")=statement  // override extends for this section
}
// Third parser class with different extends pattern
```

Each section can override attributes, but PSI settings remain shared globally.
