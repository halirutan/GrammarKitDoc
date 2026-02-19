# Grammar Composition

As a grammar grows, the generated parser class grows with it. A single parser file with thousands of methods becomes hard to navigate and slow to compile. Grammar-Kit addresses this by letting you split one grammar into multiple parser classes, each generating its own `.java` file. You can also run independent grammars side by side in the same plugin with no namespace conflicts.

## Splitting a Grammar into Multiple Parsers

To split a grammar, insert a new attribute block with a different `parserClass` value at the point where you want the split. Prefix the block with a semicolon to make it a global attribute block rather than an attribute of the previous rule:

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

The semicolon before `{` is required. Without it, Grammar-Kit treats the attribute block as belonging to the preceding rule rather than as a global declaration.

Each `parserClass` value produces a separate `.java` file. Certain settings are shared across all sections: `elementTypeHolderClass`, `psiClassPrefix`, `psiPackage`, `psiImplPackage`, and token definitions from the first `tokens` block apply everywhere. Other settings like `extends` patterns can be overridden per section:

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
  extends(".*statement")=statement
}
// Third parser class with different extends pattern
```

The generator produces files in this order: parser classes, element types holder, PSI interfaces, PSI implementation classes, and optionally a visitor class. All of these share the single `elementTypeHolderClass`, so token and rule element types are defined once regardless of how many parser classes you have.

## Cross-Class References

Rules from one parser class can reference rules in another, including [meta rules](external-rules.md). The generated code handles the cross-class static method calls automatically.

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

You do not need to add imports or forward declarations. Grammar-Kit resolves all rule references across parser class boundaries during generation. This means you can organize rules by logical concern (expressions in one class, statements in another) without worrying about dependency order.

## Multiple Entry Points

By default, a grammar has one entry point: the first rule in the file. The `extraRoot` attribute marks additional rules as independent parse entry points:

```bnf
extra_root ::= some_rule {extraRoot=true}
```

You can also apply it with a pattern in the global attribute block:

```bnf
{
  extraRoot("my_named")=true
}
```

Extra roots generate additional `parse_root_` methods, allowing the parser to be invoked at different starting points. This is useful when a file format contains embedded sections that need independent parsing, or when you want to reuse one grammar to parse different contexts.

## Independent Grammars

When two languages in the same plugin share nothing, keep them as separate `.bnf` files with fully independent configurations. Grammar-Kit's own codebase does this with `Grammar.bnf` for BNF files and `JFlex.bnf` for JFlex files:

```bnf
// Grammar.bnf
{
  parserClass="org.intellij.grammar.parser.GrammarParser"
  psiClassPrefix="Bnf"
  elementTypePrefix="BNF_"
  psiPackage="org.intellij.grammar.psi"
}
```

```bnf
// JFlex.bnf
{
  parserClass="org.intellij.jflex.parser.JFlexParser"
  psiClassPrefix="JFlex"
  elementTypePrefix="FLEX_"
  psiPackage="org.intellij.jflex.psi"
}
```

There are no namespace conflicts because each grammar uses distinct values for `parserClass`, `psiClassPrefix`, `elementTypePrefix`, `elementTypeClass`, and `psiPackage`. Each grammar generates its own complete set of parser, types, and PSI classes.

## Pattern-Based Attributes

Pattern-based attributes apply a setting to all rules whose names match a regular expression. This is a composition mechanism that keeps your grammar DRY when many rules share the same behavior:

```bnf
{
  extends(".*_expr")=expr
  pin(".*_list(?:_\\d+)*")=1
  elementTypeFactory(".*_expr")="sample.MyTypeFactory.createExprType"
  consumeTokenMethod(".*_recover")="consumeTokenFast"
}
```

The `extends(".*_expr")=expr` pattern means every rule ending in `_expr` extends the `expr` rule in the PSI hierarchy. You do not need to add `{extends=expr}` to each rule individually. This works across parser class boundaries, so rules in different parser classes that match the pattern all receive the attribute. See the [Attributes System](../code-generation/attributes.md) for the full list of attributes that support patterns.
