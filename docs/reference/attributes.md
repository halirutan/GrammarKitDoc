# Attribute Reference

This page catalogs every attribute Grammar-Kit recognizes. Attributes control parser generation, PSI class output, error recovery, and other code generation behaviors. They appear in the header block at the top of a `.bnf` file (global scope) or inline on individual rules (rule scope).

For an explanation of how attributes work, including scope rules and pattern-based targeting, see [Attributes System](../code-generation/attributes.md).

## Global Parser Attributes

These attributes configure the generated parser class and its runtime behavior. Set them in the grammar header block.

| Attribute | Type | Default | Description |
|---|---|---|---|
| `parserClass` | String | `"generated.GeneratedParser"` | Fully qualified name of the generated parser class. |
| `parserUtilClass` | String | `"...GeneratedParserUtilBase"` | Runtime support class used by the generated parser. Change this to extend parser utilities with custom methods. |
| `parserImports` | List | `[]` | Additional import statements added to the generated parser. Useful for importing static methods from external rule classes or hook implementations. |
| `extendedPin` | Boolean | `true` | When enabled, pin applies to sequences inside choices, not just top-level sequences. |
| `tokens` | List | `[]` | Declares tokens and their string or regexp values. Regexp tokens (prefixed with `regexp:`) are required for Live Preview. |

### `parserImports` example

```bnf
{
  parserImports=[
    "static com.sample.ExtraTokens.*"
    "static com.sample.MyHooks.*"
  ]
}
```

### `tokens` example

```bnf
{
  tokens = [
    id="regexp:\w+"       // regexp token
    string                // name only, no value
    PLUS_OP="+"           // simple text token
    SWITCH="switch"       // keyword token
  ]
}
```

## Global PSI Attributes

These attributes control the structure and naming of generated PSI classes.

| Attribute | Type | Default | Description |
|---|---|---|---|
| `psiPackage` | String | `"generated.psi"` | Package for generated PSI interfaces. |
| `psiImplPackage` | String | `"generated.psi.impl"` | Package for generated PSI implementation classes. |
| `psiClassPrefix` | String | `""` | Prefix added to all generated PSI class names. |
| `psiImplClassSuffix` | String | `"Impl"` | Suffix added to PSI implementation class names. |
| `psiVisitorName` | String | `"Visitor"` | Name of the generated PSI visitor class. |
| `psiImplUtilClass` | String | `null` | Fully qualified name of a class containing static methods for method mix-ins. When set, methods listed in a rule's `methods` attribute are delegated to static methods in this class. |
| `psiTreeUtilClass` | String | `"com.intellij.psi.util.PsiTreeUtil"` | Utility class used in generated PSI code for tree traversal. |

## Global Generation Control

These attributes toggle entire categories of generated output.

| Attribute | Type | Default | Description |
|---|---|---|---|
| `generatePsi` | Boolean | `true` | Generate PSI interfaces and implementation classes. Set to `false` to generate only the parser. |
| `generateTokens` | Boolean | `true` | Generate token type constants in the element type holder class. |
| `generateTokenAccessors` | Boolean | `false` | Generate getter methods for token elements in PSI classes. |
| `generateFirstCheck` | Integer | `2` | Number of tokens used in FIRST-set lookahead optimization. Higher values improve performance but increase code size. |
| `classHeader` | String | `"// This is a generated file..."` | Header text or file path added to all generated files. If the value matches a filename in the same directory, its contents are used. |

## Global Type Mapping

These attributes control element type and token type infrastructure.

| Attribute | Type | Default | Description |
|---|---|---|---|
| `elementTypeHolderClass` | String | `"generated.GeneratedTypes"` | Fully qualified name of the class that holds all `IElementType` constants. |
| `elementTypePrefix` | String | `""` | Prefix added to generated element type constant names. |
| `elementTypeClass` | String | `"...IElementType"` | Class used to instantiate composite element types. |
| `tokenTypeClass` | String | `"...IElementType"` | Class used to instantiate token element types. |
| `tokenTypeFactory` | String | `null` | Static factory method for creating token types (e.g., `"com.sample.Factory.getTokenType"`). When set, token types are created through this method instead of the constructor. |

## Rule-Level Parsing Attributes

These attributes control how individual rules are parsed. Apply them inline on a rule or through a pattern in the header block.

| Attribute | Type | Default | Scope | Description |
|---|---|---|---|---|
| `pin` | Integer/String | `-1` (none) | Rule | Position or token pattern in a sequence after which the parser commits to the match and tolerates errors. See [Error Recovery](../grammar-development/error-recovery.md). |
| `recoverWhile` | String | `null` | Rule | Name of a predicate rule that controls how far the parser skips tokens after an error. Use `"#auto"` for automatic recovery based on the rule's NEXT set. |
| `name` | String | `null` | Rule | Display name used in error messages ("expected &lt;name&gt;"). Set to `""` to suppress the short error message. |
| `consumeTokenMethod` | String | `"consumeToken"` | Rule | Token consumption method. Use `"consumeTokenFast"` to skip error position recording in recovery rules or expression parsing for better performance. |
| `rightAssociative` | Boolean | `false` | Rule | Makes an expression rule right-associative instead of the default left-associative. Applies to expression parsing with `extends`. |
| `extraRoot` | Boolean | `false` | Rule | Marks the rule as an additional parsing entry point, added to the `parse_extra_roots()` method. |

### `pin` and `recoverWhile` example

```bnf
list ::= "(" items? ")" {pin=1}
private items ::= [!")" item (',' item) * ] {pin(".*")=1}
item ::= number {recoverWhile=item_recover}
private item_recover ::= !(")" | ",")
```

### `consumeTokenMethod` example

```bnf
{
  consumeTokenMethod(".*_recover")="consumeTokenFast"
  consumeTokenMethod(".*_expr")="consumeTokenFast"
}
```

## Rule-Level PSI Attributes

These attributes shape the PSI class hierarchy and behavior for individual rules.

| Attribute | Type | Default | Scope | Description |
|---|---|---|---|---|
| `extends` | String | `"...ASTWrapperPsiElement"` | Rule | Base class or super-rule for the generated PSI class. When rules extend the same super-rule, the parser collapses their AST nodes into a flat tree. Supports pattern-based application. |
| `implements` | List | `["...PsiElement"]` | Rule | Interfaces that the generated PSI class implements. |
| `mixin` | String | `null` | Rule | Fully qualified name of a hand-written class mixed into the PSI hierarchy as the implementation base class. |
| `elementType` | String | `null` | Rule | Overrides the generated element type constant. Use this to share a single element type across multiple rules, or to integrate with an existing PSI implementation. |
| `elementTypeClass` | String | `"...IElementType"` | Rule | Class used to instantiate this rule's element type. Overrides the global `elementTypeClass`. |
| `elementTypeFactory` | String | `null` | Rule | Static factory method for creating this rule's element type (e.g., `"com.sample.Factory.getCompositeType"`). |
| `stubClass` | String | `null` | Rule | Stub class for stub-based indexing. When set, the PSI implementation extends `StubBasedPsiElementBase` instead of `ASTWrapperPsiElement`. |
| `fallbackStubElementType` | String | `"...IStubElementType"` | Rule | Element type class to use when stubs are involved. |
| `methods` | List | `[]` | Rule | Custom PSI accessors and method mix-ins. Entries prefixed with `/` define named accessors for child elements; plain names define method mix-ins delegated to `psiImplUtilClass`. |
| `hooks` | List | `[]` | Rule | Parsing hooks such as whitespace binders. Each entry maps a hook name to its arguments. |

### `extends` example

```bnf
{
  extends(".*_expr")=expr
}
expr ::= add_expr | mul_expr | ref_expr | literal_expr
add_expr ::= expr '+' expr
mul_expr ::= expr '*' expr
```

### `methods` example

```bnf
sum_expr ::= expr '+' expr {
  methods=[
    left="/expr[0]"
    right="/expr[1]"
    op="/OP_PLUS"
    evaluate toString    // mix-ins from psiImplUtilClass
  ]
}
```

### `hooks` example

```bnf
{
  parserImports=["static com.intellij.lang.WhitespacesBinders.*"]
}
left_binder ::= ... { hooks=[leftBinder="GREEDY_LEFT_BINDER"] }
right_binder ::= ... { hooks=[rightBinder="GREEDY_RIGHT_BINDER"] }
```

## The `generate` Attribute

The `generate` attribute is a list of fine-grained options that supersede several of the global `generateXXX` attributes. It provides centralized control over what the generator produces.

```bnf
{
  generate=[psi="no" tokens="no" names="short"]
}
```

### PSI options

| Option | Values | Default | Description |
|---|---|---|---|
| `psi` | yes, no | yes | Generate PSI classes. |
| `psi-classes-map` | yes, no | no | Generate `IElementType`-to-node-class map. |
| `psi-factory` | yes, no | yes | Generate `PsiElement` factory for `ASTNode` nodes. |
| `visitor` | yes, no | yes | Generate visitor class for PSI classes. |
| `visitor-value` | void, type name | void | Type parameter for the generated visitor. |
| `fqn` | yes, no | no | Use fully qualified class names in generated code. |
| `token-accessors` | yes, no | no | Generate getter methods for token elements in PSI. |

### Type options

| Option | Values | Default | Description |
|---|---|---|---|
| `elements` | yes, no | yes | Generate composite element type constants. |
| `element-case` | lower, upper, as-is | upper | Case style for element type constant names. |
| `tokens` | yes, no | yes | Generate token type constants. |
| `token-case` | lower, upper, as-is | upper | Case style for token type constant names. |
| `token-sets` | yes, no | no | Generate `TokenSet` constants from top-level choice rules. |
| `exact-types` | all, no, tokens, elements | no | Use exact types for constants instead of `IElementType`. |

### Parser options

| Option | Values | Default | Description |
|---|---|---|---|
| `names` | short, long, classic | short | Variable naming style in generated parser code. |
| `first-check` | positive integer | 2 | Number of tokens for FIRST-set lookahead optimization. |

### Generator options

| Option | Values | Default | Description |
|---|---|---|---|
| `java` | 6, 8, 11, etc. | 11 | Target Java version. Controls whether lambdas and other language features are used in generated code. |

## Pattern-Based Attributes

Any attribute can target multiple rules using a regex pattern. The pattern appears in parentheses after the attribute name in the header block:

```bnf
{
  extends(".*_expr")=expr
  pin(".*_list(?:_\d+)*")=1
  consumeTokenMethod(".*_recover")="consumeTokenFast"
  mixin("my_named")="com.sample.psi.impl.MyNamedImplMixin"
}
```

The regex matches against rule names. All rules whose names match receive the attribute value. Pattern attributes are evaluated in declaration order, and later declarations override earlier ones for the same rule.
