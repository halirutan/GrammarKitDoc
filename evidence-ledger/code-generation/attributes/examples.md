# Section 3.1: Attributes System — Examples

## Example 1: Complete Grammar Header with All Major Attributes

**Source: `grammars/Grammar.bnf:1-54`**

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
    // ...more tokens
  ]

  implements("rule|attr")="org.intellij.grammar.psi.BnfNamedElement"
  extends("rule|attr")="org.intellij.grammar.psi.impl.BnfNamedImpl"
  mixin("reference_or_token")="org.intellij.grammar.psi.impl.BnfRefOrTokenImpl"
}
```

## Example 2: The `generate` Attribute Options

**Source: `attributeDescriptions/generate.html`, `testData/generator/GenOptions.bnf`**

```bnf
{
  generate=[
    java="7"            // Java version for generated code
    fqn="yes"           // Use fully qualified class names
    visitor-value="Val" // Visitor<Val> generic type
    token-case="lower"  // Token constants in lowercase
    element-case="upper" // Element constants in uppercase
    psi-classes-map="yes" // Generate IElementType→class map
    psi="no"            // Skip PSI generation
    tokens="no"         // Skip token constants
    names="short"       // Use short variable names (b, l, m, r)
    first-check=2       // FIRST-based optimization threshold
    token-sets="yes"    // Generate TokenSets for choices
  ]
}
```

## Example 3: Pin and RecoverWhile Attributes

**Source: `attributeDescriptions/pin.html`, `attributeDescriptions/recoverWhile.html`**

```bnf
// Pin by position number
list ::= "(" items? ")" {pin=1}

// Pin by pattern on sub-expressions
private items ::= [!")" item (',' item) * ] {pin(".*")=1}

// Recovery predicate
item ::= number {recoverWhile=item_recover}
private item_recover ::= !(',' | ')')

// Auto-recovery: computes !(FOLLOWS(rule)) automatically
item ::= number {recoverWhile="#auto"}
```

## Example 4: Extends for PSI Hierarchy and Flat AST

**Source: `attributeDescriptions/extends.html`, `HOWTO.md:226-251`**

```bnf
{
  extends(".*_expr")=expr
}
// Without extends: FileNode → Expr → LiteralExpr (deep tree)
// With extends:    FileNode → LiteralExpr       (flat tree)
```

## Example 5: Methods Attribute — Accessors, Renames, Mix-ins

**Source: `attributeDescriptions/methods.html`**

```bnf
sum_expr ::= expr '+' expr {
  methods=[
    left="/expr[0]"       // Path-based accessor to first child
    right="/expr[1]"      // Path-based accessor to second child
    op="/OP_PLUS"         // Explicit token accessor
    evaluate toString     // Method mix-ins from psiImplUtilClass
  ]
}

list ::= item + {
  methods=[
    element="item"        // Rename getItemList() to getElementList()
    // item=""            // Suppress accessor completely
  ]
}
```

## Example 6: Hooks for Whitespace Binders

**Source: `attributeDescriptions/hooks.html`, `testData/generator/BindersAndHooks.bnf`**

```bnf
{
  parserImports=[
    "static com.intellij.lang.WhitespacesBinders.*"
    "static com.sample.MyHooks.*"
  ]
}
left_binder ::= A B { hooks=[leftBinder="GREEDY_LEFT_BINDER"] }
right_binder ::= item { hooks=[rightBinder="GREEDY_RIGHT_BINDER"] }
both_binders ::= A item B { hooks=[wsBinders="GREEDY_LEFT_BINDER, GREEDY_RIGHT_BINDER"] }
```

## Example 7: consumeTokenMethod for Performance

**Source: `attributeDescriptions/consumeTokenMethod.html`**

```bnf
{
  // Do not record error reporting in recovery rules
  consumeTokenMethod(".*_recover")="consumeTokenFast"

  // Skip error info in expression parsing (no one needs to know + - * / expected)
  consumeTokenMethod(".*_expr|.*_op")="consumeTokenFast"
}
```

## Example 8: elementType Sharing and Suppression

**Source: `attributeDescriptions/elementType.html`**

```bnf
// Two rules share the same element type and PSI
some_statement ::= 'some' expression
some_statement_alt_syntax ::= expression 'some' {elementType=some_statement}

// Suppress element type entirely (no AST node, no PSI class)
publicMethodToCall ::= identifier {elementType=""}
```

## Example 9: Stub Support Configuration

**Source: `testData/generator/Stub.bnf`, `HOWTO.md:346-381`**

```bnf
{
  elementTypeFactory="test.FooParserDefinition.createType"
  extends("element1|type")="org.intellij.grammar.test.StubTest.GenericBase<?>"
}
element1 ::= 'aa' element5 { stubClass="test.stub.Element1Stub" }
// The <?> in extends is replaced with stubClass value during generation
```
