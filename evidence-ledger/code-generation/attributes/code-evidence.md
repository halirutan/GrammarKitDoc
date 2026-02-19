# Section 3.1: Attributes System — Code Evidence

## 1. Complete Attribute Catalog

**Source: `src/org/intellij/grammar/KnownAttribute.java:29-72`**

All attributes are defined as static `KnownAttribute<T>` fields. Each has: name, type, default value, and global scope flag.

### Global Attributes (apply to entire grammar)

| Attribute | Type | Default | Description |
|---|---|---|---|
| `classHeader` | String | `"// This is a generated file..."` | Header text or file for generated files |
| `generate` | ListValue | `[]` | Generator options list (supersedes individual generate* attributes) |
| `generatePsi` | Boolean | `true` | Generate PSI classes |
| `generateTokens` | Boolean | `true` | Generate token constants |
| `generateTokenAccessors` | Boolean | `false` | Generate token getter methods in PSI |
| `generateFirstCheck` | Integer | `2` | FIRST-based look-ahead optimization threshold |
| `extendedPin` | Boolean | `true` | Extended pin mode for sequence parsing |
| `parserImports` | ListValue | `[]` | Additional import statements for parser |
| `psiClassPrefix` | String | `""` | Prefix for PSI class names |
| `psiImplClassSuffix` | String | `"Impl"` | Suffix for PSI impl class names |
| `psiTreeUtilClass` | String | `"com.intellij.psi.util.PsiTreeUtil"` | PSI tree utility class |
| `psiPackage` | String | `"generated.psi"` | Package for PSI interfaces |
| `psiImplPackage` | String | `"generated.psi.impl"` | Package for PSI implementations |
| `psiVisitorName` | String | `"Visitor"` | Name of the generated visitor class |
| `psiImplUtilClass` | String | `null` | Class containing method mix-in implementations |
| `tokenTypeClass` | String | `"com.intellij.psi.tree.IElementType"` | IElementType subclass for tokens |
| `parserClass` | String | `"generated.GeneratedParser"` | Generated parser class name |
| `parserUtilClass` | String | `"com.intellij.lang.parser.GeneratedParserUtilBase"` | Parser utility class |
| `elementTypeHolderClass` | String | `"generated.GeneratedTypes"` | Class holding IElementType constants |
| `elementTypePrefix` | String | `""` | Prefix for element type constants |
| `tokenTypeFactory` | String | `null` | Factory method for token types |
| `tokens` | ListValue | `[]` | Token name-value definitions |

### Rule-Level Attributes (apply to individual rules)

| Attribute | Type | Default | Description |
|---|---|---|---|
| `extends` | String | `"com.intellij.extapi.psi.ASTWrapperPsiElement"` | Base class or super rule |
| `implements` | ListValue | `["com.intellij.psi.PsiElement"]` | Interfaces to implement |
| `elementType` | String | `null` | Override element type name |
| `elementTypeClass` | String | `"com.intellij.psi.tree.IElementType"` | IElementType subclass for this rule |
| `elementTypeFactory` | String | `null` | Factory method for this rule's type |
| `fallbackStubElementType` | String | `"com.intellij.psi.stubs.IStubElementType"` | Fallback stub element class |
| `pin` | Object | `-1` | Pin value (number or pattern) |
| `mixin` | String | `null` | Implementation mixin class |
| `recoverWhile` | String | `null` | Recovery predicate rule name or "#auto" |
| `name` | String | `null` | Display name in error messages |
| `extraRoot` | Boolean | `false` | Extra root rule flag |
| `rightAssociative` | Boolean | `false` | Right-associative operator flag |
| `consumeTokenMethod` | String | `"consumeToken"` | Token consumption method |
| `stubClass` | String | `null` | Stub class for StubIndex support |
| `methods` | ListValue | `[]` | Custom PSI methods |
| `hooks` | ListValue | `[]` | Parsing hooks (whitespace binders, etc.) |

## 2. Attribute Scope: Global vs Rule-Level

**Source: `src/org/intellij/grammar/KnownAttribute.java:79-81`**

```java
private static <T> KnownAttribute<T> create(boolean global, Class<T> clazz, String name, T defaultValue)
```

The `boolean global` parameter (first arg to `create()`) determines scope:
- `true` = global attribute (applies to all rules, set at file top)
- `false` = rule-level attribute (can vary per rule)

## 3. Pattern-Based Attribute Application

**Source: `README.md:122-129`**

Global attributes support regex patterns to apply to multiple rules:
```bnf
{
  extends(".*_expr")=expr        // applies to all .*_expr rules
  pin(".*_list(?:_\d+)*")=1      // applies to all .*_list rules and sub-expressions
}
```

## 4. The `generate` Attribute — Consolidated Options

**Source: `resources/messages/attributeDescriptions/generate.html`**

The `generate` attribute is a list of key-value pairs that supersedes individual `generateXXX` attributes.

| Option | Values | Description |
|---|---|---|
| `psi` | **yes**, no | Generate PSI classes |
| `psi-classes-map` | yes, **no** | Generate IElementType to node class map |
| `psi-factory` | **yes**, no | Generate PsiElement factory |
| `visitor` | **yes**, no | Generate PSI visitor class |
| `visitor-value` | **void**, type name | Visitor generic type parameter |
| `fqn` | **no**, yes | Use fully qualified class names |
| `elements` | **yes**, no | Generate composite element type constants |
| `element-case` | lower, **upper**, as-is | Element type constant casing |
| `tokens` | **yes**, no | Generate token constants |
| `token-case` | lower, **upper**, as-is | Token constant casing |
| `token-sets` | yes, **no** | Generate token sets from choice rules |
| `exact-types` | all, **no**, tokens, elements | Exact type for constants |
| `token-accessors` | yes, **no** | Generate token getter methods |
| `names` | **short**, long, classic | Local variable naming style |
| `first-check` | positive number, **2** | FIRST-based optimization threshold |
| `java` | 6, 8, **11**, etc. | Java version for code generation |

Example:
```bnf
{
  generate=[psi="no" tokens="no" names="short"]
}
```

### GenOptions.java Implementation

**Source: `src/org/intellij/grammar/generator/GenOptions.java:21-67`**

```java
public GenOptions(BnfFile myFile) {
    Map<String, String> genOptions = getRootAttribute(myFile, KnownAttribute.GENERATE).asMap();
    names = Names.forName(genOptions.get("names"));
    generatePsi = getGenerateOption(myFile, KnownAttribute.GENERATE_PSI, genOptions, "psi");
    generateTokenTypes = getGenerateOption(myFile, KnownAttribute.GENERATE_TOKENS, genOptions, "tokens");
    generateTokenSets = generateTokenTypes && "yes".equals(genOptions.get("token-sets"));
    generateElementTypes = !"no".equals(genOptions.get("elements"));
    generateExtendedPin = getGenerateOption(myFile, KnownAttribute.EXTENDED_PIN, genOptions, "extended-pin", "extendedPin");
    generateVisitor = !"no".equals(genOptions.get("visitor"));
    visitorValue = "void".equals(genOptions.get("visitor-value")) ? null : genOptions.get("visitor-value");
    generateFQN = "yes".equals(genOptions.get("fqn"));
    generateTokenCase = ParserGeneratorUtil.enumFromString(genOptions.get("token-case"), Case.UPPER);
    generateElementCase = ParserGeneratorUtil.enumFromString(genOptions.get("element-case"), Case.UPPER);
    javaVersion = StringUtil.parseInt(genOptions.get("java"), 11);
    // ...
}
```

The `generate` attribute options take priority, falling back to standalone attributes.

## 5. GenOptions.bnf — Example of Generate Attribute

**Source: `testData/generator/GenOptions.bnf:1-8`**

```bnf
{
  parserClass="GenOptions"
  generate=[java="7" fqn="yes" visitor-value="Val" token-case="lower"
            element-case="upper" psi-classes-map="yes"]
  extends(".*_statement")="statement"
  pin("create_.*_statement")=".*_ref"
  pin("drop_.*_statement")=".*_ref"
}
```

## 6. Individual Attribute Descriptions

### `classHeader`
**Source: `resources/messages/attributeDescriptions/classHeader.html`**

Add a header (file or text) to all generated files:
```bnf
{ classHeader="//This is a generated file" }
{ classHeader="license.txt" }  // file in same directory
```

### `pin`
**Source: `resources/messages/attributeDescriptions/pin.html`**

The number or pattern of expression to pin:
1. Applied to items of grammar sequence expressions.
2. Parser ignores errors after a pinned item.

```bnf
list ::= "(" items? ")" {pin=1}
private items ::= [!")" item (',' item) * ] {pin(".*")=1}
item ::= number {recoverWhile=item_recover}
```

**Source: `README.md:188-195`**

Pin value indicates the desired item by:
- Number: `{pin=2}`
- Pattern: `{pin="rule_B"}`
- Sub-expressions: `{pin(".*")=1}` applies to all sub-sequences.

### `recoverWhile`
**Source: `resources/messages/attributeDescriptions/recoverWhile.html`**

Recovery predicate rule or `"#auto"` (which means `! FOLLOWS(rule)`).

Contract:
1. The attributed rule is handled as usual.
2. Regardless of the result, parser consumes tokens while predicate matches.

Notes:
1. Should be on a rule inside a loop.
2. That rule should have `pin` somewhere.
3. Value should be a predicate rule (leaves input intact).

### `extends`
**Source: `resources/messages/attributeDescriptions/extends.html`**

Base class or super rule for PSI classes. AST nodes produced by rules extending the same rule are collapsed by the parser.

```bnf
{
  extends(".*_expr")=expr
}
// AST becomes "flat" — FileNode/LiteralExpr instead of FileNode/Expr/LiteralExpr
```

Can also specify a Java class for stubs:
```bnf
stub_element ::= {extends="com.sample.StubBase<?>" stubClass="com.sample.StubElementStub"}
```

### `implements`
**Source: `resources/messages/attributeDescriptions/implements.html`**

List of interfaces for PSI classes:
```bnf
{
  implements("rule|attr")="org.intellij.grammar.psi.BnfNamedElement"
}
```

### `mixin`
**Source: `resources/messages/attributeDescriptions/mixin.html`**

Qualified name of implementation class mixed into hierarchy:
```bnf
{
  mixin("my_named")="com.sample.psi.impl.MyNamedImplMixin"
}
```

### `methods`
**Source: `resources/messages/attributeDescriptions/methods.html`**

Custom PSI accessors and method mix-ins:
```bnf
sum_expr ::= expr '+' expr {
  methods=[
    left="/expr[0]"       // user PSI accessor: path to child
    right="/expr[1]"      // indexed accessor
    op="/OP_PLUS"         // explicit token accessor
    evaluate toString     // method mix-ins from psiImplUtilClass
  ]
}
list ::= item + {
  methods=[
    element="item"   // rename getItemList() to getElementList()
    // item=""       // suppress it completely
  ]
}
```

### `hooks`
**Source: `resources/messages/attributeDescriptions/hooks.html`**

Custom rule parsing hooks (whitespace binders):
```bnf
{
  parserImports=[
    "static com.intellij.lang.WhitespacesBinders.*"
    "static com.sample.MyHooks.*" ]
}
left_binder ::= ... { hooks=[leftBinder="GREEDY_LEFT_BINDER"] }
right_binder ::= ... { hooks=[rightBinder="GREEDY_RIGHT_BINDER"] }
both_binders ::= ... { hooks=[wsBinders="GREEDY_LEFT_BINDER, GREEDY_RIGHT_BINDER"] }
logging_rule ::= ... { hooks=[logHook='"in logging_rule!"'] }
got_hook1 ::= ... { hooks=[myHook1="SOME_CONST"] }
```

### `elementType`
**Source: `resources/messages/attributeDescriptions/elementType.html`**

Override element type name for a rule. Use cases:
1. Make two rules share the same node type and PSI.
2. Integrate with existing PSI implementation.

```bnf
some_statement ::=
some_statement_alt_syntax ::= {elementType=some_statement}
```

### `elementTypeFactory`
**Source: `resources/messages/attributeDescriptions/elementTypeFactory.html`**

Factory method for complex element types:
```bnf
{
  elementTypeFactory="com.sample.SampleElementFactory.getCompositeType"
  tokenTypeFactory="com.sample.SampleElementFactory.getTokenType"
}
```

### `stubClass`
**Source: `resources/messages/attributeDescriptions/stubClass.html`**

Stub class for StubIndex support:
```bnf
stub_element ::= {extends="com.sample.StubBase<?>" stubClass="com.sample.StubElementStub"}
```

The `<?>` syntax in `extends` is replaced with the `stubClass` value during generation.

### `name`
**Source: `resources/messages/attributeDescriptions/name.html`**

Display name in error messages. Empty string suppresses short error message:
```bnf
operator ::= '+' | '-' | '*' | '/' | "=" {name="operator"}
```

### `consumeTokenMethod`
**Source: `resources/messages/attributeDescriptions/consumeTokenMethod.html`**

Defaults to `consumeToken`. Used for performance:
```bnf
{
  consumeTokenMethod(".*_recover")="consumeTokenFast"
  consumeTokenMethod(".*_expr|.*_op")="consumeTokenFast"
}
```

### `rightAssociative`
**Source: `resources/messages/attributeDescriptions/rightAssociative.html`**

For operators where `a = b = c` should equal `a = (b = c)`:
```bnf
assign_expr ::= expr '=' expr { rightAssociative=true }
```

### `extraRoot`
**Source: `resources/messages/attributeDescriptions/extraRoot.html`**

Marks a rule as additional parse entry point:
```bnf
{ extraRoot("my_named")=true }
```

### `extendedPin`
**Source: `resources/messages/attributeDescriptions/extendedPin.html`**

> Generate code for parsing a sequence tail even if some parts are missing if it is already pinned. The value is **true** by default and should not be changed.

### `parserClass`
**Source: `resources/messages/attributeDescriptions/parserClass.html`**

Can be used multiple times to split parsing code:
```bnf
;{
  parserClass="org.intellij.grammar.parser.GrammarParser2"
}
```

### `tokens`
**Source: `resources/messages/attributeDescriptions/tokens.html`**

Token name-value list. Regexp tokens are required by Live Preview:
```bnf
{
  tokens = [
    id="regexp:\\w+"     // regexp token
    string               // no value or pattern
    PLUS_OP="+"
    SWITCH="switch"
  ]
}
```

### `generateTokenAccessors`
**Source: `resources/messages/attributeDescriptions/generateTokenAccessors.html`**

Controls token accessor generation. When false, accessors are still generated for:
- Regexp tokens
- Lower-case tokens
- Tokens with no pattern or value

### `fallbackStubElementType`
**Source: `resources/messages/attributeDescriptions/fallbackStubElementType.html`**

> Allows specifying a fallback class for elementType in stub element constructors. Usually the parser generator looks into the parent class file. But if not available (not yet compiled), it uses `IStubElementType` by default.

Per-parser option, not overridable per rule.

## 7. Attribute Documentation Lookup

**Source: `src/org/intellij/grammar/KnownAttribute.java:119-127`**

```java
public String getDescription() {
    InputStream resourceAsStream = getClass().getResourceAsStream(
        "/messages/attributeDescriptions/" + getName() + ".html");
    return resourceAsStream == null ? null : FileUtil.loadTextAndClose(resourceAsStream);
}
```

Attribute descriptions are loaded from HTML resource files at `/messages/attributeDescriptions/<name>.html`.

## 8. ListValue Internal Structure

**Source: `src/org/intellij/grammar/KnownAttribute.java:133-166`**

`ListValue` extends `LinkedList<Pair<String, String>>` and provides:
- `asStrings()` — extracts either first or second pair values as a list
- `asMap()` — converts pairs to an ordered map
- `asInverseMap()` — converts pairs with keys/values swapped

Single string values are auto-converted to ListValue when the attribute type requires it (line 108):
```java
if (myClazz == ListValue.class && o instanceof String) {
    return (T)ListValue.singleValue(null, (String)o);
}
```

## 9. Names Configuration

**Source: `src/org/intellij/grammar/generator/Names.java:13-63`**

Three naming styles for generated parser local variables:

| Style | builder | level | marker | pinned | result | pos | root | priority |
|---|---|---|---|---|---|---|---|---|
| classic | `builder_` | `level_` | `marker_` | `pinned_` | `result_` | `pos_` | `root_` | `priority_` |
| long | `builder` | `level` | `marker` | `pinned` | `result` | `pos` | `type` | `priority` |
| short | `b` | `l` | `m` | `p` | `r` | `c` | `t` | `g` |

Default: `short` (in production), `classic` (in unit tests).

## 10. Case Configuration

**Source: `src/org/intellij/grammar/generator/Case.java:14-27`**

Four casing options for generated constant names:
- `LOWER` — all lowercase
- `UPPER` — all uppercase (default for tokens and elements)
- `AS_IS` — no transformation
- `CAMEL` — first letter uppercase, rest lowercase
