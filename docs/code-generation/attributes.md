# Attributes System

Attributes control what Grammar-Kit generates and how. They appear in the curly-brace header block at the top of a `.bnf` file and, optionally, inline on individual rules. Through attributes you configure package names, class naming, PSI hierarchy, error recovery, and dozens of other generation behaviors.

Grammar-Kit attributes fall into three scope levels: global attributes that apply to the entire grammar, rule-level attributes that apply to a single rule, and pattern-based attributes that apply to all rules matching a regex.

## Scope and Placement

Global attributes go in the header block at the top of the grammar file. They set defaults for the entire grammar:

```bnf
{
  parserClass="com.example.lang.MyParser"
  psiPackage="com.example.lang.psi"
  psiImplPackage="com.example.lang.psi.impl"
}
```

Rule-level attributes appear inline after a rule's definition, inside curly braces:

```bnf
item ::= number {recoverWhile=item_recover pin=1}
```

Pattern-based attributes use a regex in the header block to target multiple rules at once. The pattern appears in parentheses after the attribute name:

```bnf
{
  extends(".*_expr")=expr
  pin(".*_list(?:_\d+)*")=1
  consumeTokenMethod(".*_recover")="consumeTokenFast"
}
```

When a rule-level attribute is set directly on a rule, it overrides any pattern-based or global default for that rule. Pattern-based attributes override global defaults for matching rules.

## Common Configurations

Most grammars configure the same core set of attributes. The Grammar-Kit plugin's own grammar shows a typical real-world header:

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

  tokens = [
    OP_EQ="="
    OP_IS="::="
    OP_OR="|"
  ]

  implements("rule|attr")="org.intellij.grammar.psi.BnfNamedElement"
  extends("rule|attr")="org.intellij.grammar.psi.impl.BnfNamedImpl"
  mixin("reference_or_token")="org.intellij.grammar.psi.impl.BnfRefOrTokenImpl"
}
```

These attributes group into three categories.

**Parser configuration** controls the generated parser class and its dependencies. `parserClass` sets the fully qualified name of the parser (default: `"generated.GeneratedParser"`). `parserUtilClass` points to the utility base class (default: `GeneratedParserUtilBase`). `parserImports` adds extra import statements to the parser source.

**PSI configuration** controls the generated PSI interfaces and implementations. `psiPackage` and `psiImplPackage` set the package for interfaces and implementations. `psiClassPrefix` adds a prefix to all PSI class names (e.g., `"Bnf"` produces `BnfRule`, `BnfExpr`). `psiImplClassSuffix` sets the suffix for implementation classes (default: `"Impl"`). `psiImplUtilClass` points to the class containing static method mix-in implementations. `psiVisitorName` sets the visitor class name (default: `"Visitor"`).

**Element type configuration** controls the generated `IElementType` constants. `elementTypeHolderClass` names the interface that holds all type constants. `elementTypePrefix` adds a prefix to constant names (e.g., `"BNF_"` produces `BNF_RULE`). `elementTypeClass` and `tokenTypeClass` set the `IElementType` subclass used for composite and token types. `elementTypeFactory` and `tokenTypeFactory` specify factory methods instead of constructor calls when you need custom type creation logic.

## Rule-Level Attributes

Individual rules accept attributes that control parsing behavior, PSI generation, and error recovery. The most commonly used ones fall into several groups.

`extends` sets the base class or super-rule for a rule's PSI class. When it names another rule (not a Java class), the parser collapses the AST, producing a flatter tree. `implements` adds interfaces to the generated PSI class. Both support pattern-based application. See [PSI Customization](psi-customization.md) for details on building type hierarchies.

`pin` and `recoverWhile` control error recovery. `pin` marks the point in a sequence after which the parser commits to that branch even if later elements fail. `recoverWhile` names a predicate rule (or `"#auto"`) that consumes tokens until the predicate stops matching, allowing the parser to resynchronize. See [Error Recovery](../grammar-development/error-recovery.md) for patterns and examples.

`methods` defines custom PSI accessors, accessor renames, and method mix-ins. `mixin` sets an implementation base class that is mixed into the PSI hierarchy. Both are covered in [PSI Customization](psi-customization.md).

`elementType` overrides the element type name for a rule. Setting it to another rule's name makes two rules share the same `IElementType` and PSI class. Setting it to an empty string suppresses element type and PSI generation entirely:

```bnf
some_statement ::= 'some' expression
some_statement_alt_syntax ::= expression 'some' {elementType=some_statement}

publicMethodToCall ::= identifier {elementType=""}
```

`hooks` attaches whitespace binders or custom parsing hooks to a rule. To use hooks, import the binder classes through `parserImports`:

```bnf
{
  parserImports=[
    "static com.intellij.lang.WhitespacesBinders.*"
  ]
}
left_binder ::= A B { hooks=[leftBinder="GREEDY_LEFT_BINDER"] }
right_binder ::= item { hooks=[rightBinder="GREEDY_RIGHT_BINDER"] }
both_binders ::= A item B {
  hooks=[wsBinders="GREEDY_LEFT_BINDER, GREEDY_RIGHT_BINDER"]
}
```

Other rule-level attributes include `name` (display name in error messages), `consumeTokenMethod` (use `"consumeTokenFast"` for recovery rules to skip error recording), `stubClass` (shorthand for stub index support), `rightAssociative` (for operators like assignment), and `extraRoot` (marks a rule as an additional parse entry point).

## The `generate` Attribute

The `generate` attribute consolidates many generation options into a single key-value list. It supersedes the older standalone attributes like `generatePsi`, `generateTokens`, and `extendedPin`. When both forms are present, the `generate` option takes priority.

```bnf
{
  generate=[psi="no" tokens="no" names="short" java="11"]
}
```

The full set of options and their defaults:

| Option | Default | Description |
|---|---|---|
| `psi` | yes | Generate PSI classes |
| `psi-factory` | yes | Generate PsiElement factory in the types holder |
| `psi-classes-map` | no | Generate IElementType-to-class map |
| `visitor` | yes | Generate PSI visitor class |
| `visitor-value` | void | Visitor generic type parameter |
| `elements` | yes | Generate composite element type constants |
| `element-case` | upper | Casing for element constants (upper, lower, as-is) |
| `tokens` | yes | Generate token constants |
| `token-case` | upper | Casing for token constants (upper, lower, as-is) |
| `token-sets` | no | Generate TokenSets from choice rules |
| `token-accessors` | no | Generate token getter methods in PSI |
| `exact-types` | no | Exact type for constants (all, no, tokens, elements) |
| `fqn` | no | Use fully qualified class names (no imports) |
| `names` | short | Variable naming style: short (`b`, `l`, `r`), long (`builder`, `level`, `result`), or classic (`builder_`, `level_`, `result_`) |
| `first-check` | 2 | FIRST-based look-ahead optimization threshold |
| `java` | 11 | Java version for generated code |

!!! tip
    Start with the defaults and override only what you need. The `names="short"` default produces compact generated code. Switch to `names="long"` if you need to read through the generated parser for debugging.

For a complete reference of all attributes with their types, defaults, and interaction effects, see the [Attribute Reference](../reference/attributes.md).
