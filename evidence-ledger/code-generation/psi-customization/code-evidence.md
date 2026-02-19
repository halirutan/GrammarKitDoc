# Section 3.4: PSI Customization — Code Evidence

## 1. PSI Class Generation Basics

**Source: `HOWTO.md:226-251`**

### Key Principles
1. Specify `private` on rules not needed in AST as early as possible. The first rule is implicitly `private`.
2. Use `extends` for two goals: make PSI hierarchy look nice and make AST shallow.

```bnf
{
  extends(".*_expr")=expr    // FileNode/LiteralExpr instead of FileNode/Expr/LiteralExpr
  tokens = [PLUS='+' MINUS='-']
}
expr ::= factor add_expr *
private factor ::= primary mul_expr *     // no AST node
private primary ::= literal_expr          // no AST node
left add_expr ::= ('+'|'-') factor
left mul_expr ::= ('*'|'/') primary
literal_expr ::= ...
```

## 2. Fake Rules for PSI Hierarchy

**Source: `HOWTO.md:253-301`**

Fake rules shape the generated PSI classes without affecting parsing:

```bnf
{
  extends("(add|mul)_expr")=binary_expr
  extends(".*_expr")=expr
}
fake binary_expr ::= expr + {
  methods=[
    left="/expr[0]"     // @NotNull (due to "+" in expression)
    right="/expr[1]"    // "expr" is auto-calculated child property name
  ]
}
```

Generates:
```java
public interface BinaryExpr {
  List<Expr> getExprList();
  @NotNull Expr getLeft();
  @Nullable Expr getRight();
}
public interface AddExpr extends BinaryExpr { ... }
public interface MulExpr extends BinaryExpr { ... }
```

And visitor:
```java
public class Visitor extends PsiElementVisitor {
  public visitAddExpr(AddExpr o) { visitBinaryExpr(o); }
  public visitMulExpr(MulExpr o) { visitBinaryExpr(o); }
  public visitBinaryExpr(BinaryExpr o) { visitExpr(o); }
}
```

**Source: `README.md:141-142`**

> *fake* (PSI classes): a rule for shaping the generated PSI classes; only PSI classes are generated.
> *fake* should not be combined with *private*.

## 3. Implementation Mixin via `mixin` Attribute

**Source: `HOWTO.md:304-321`**

```bnf
{
  mixin("my_named")="com.sample.psi.impl.MyNamedImplMixin"
}
my_named ::= part1 part2 part3
```

```java
public class MyNamedImplMixin extends MyNamed implements PsiNamedElement {
  @Nullable @NonNls String getName() { ... }
  PsiElement setName(@NonNls @NotNull String name) throws IncorrectOperationException { ... }
}
```

**Source: `resources/messages/attributeDescriptions/mixin.html`**

> Qualified name of the implementation class which will be mixed into the hierarchy.

**Gradle limitation** (from `README.md:49-51`):
> Method mixins are not supported (two-pass generation is not implemented) [in Gradle]

## 4. Method Injection via `psiImplUtilClass`

**Source: `HOWTO.md:323-341`**

```bnf
{
  psiImplUtilClass="com.sample.SamplePsiImplUtil"
  implements("my_named")="com.intellij.psi.PsiNamedElement"
}
my_named ::= part1 part2 part3 {
  methods=[getName setName]   // no need for argument types or return type
}
```

```java
public class SamplePsiImplUtil {
  // Extra first parameter is the PSI element
  public static @Nullable String getName(MyNamed o) { ... }
  public static PsiElement setName(MyNamed o, @NotNull String name) { ... }
}
```

## 5. The `methods` Attribute — Comprehensive

**Source: `resources/messages/attributeDescriptions/methods.html`**

### User PSI Accessors
```bnf
sum_expr ::= expr '+' expr {
  methods=[
    left="/expr[0]"      // @NotNull child accessor
    right="/expr[1]"     // indexed child accessor
    op="/OP_PLUS"        // explicit token accessor
  ]
}
```

### Method Mix-ins
```bnf
sum_expr ::= expr '+' expr {
  methods=[evaluate toString]  // from psiImplUtilClass
}
```

### Renaming Accessors
```bnf
list ::= item + {
  methods=[
    element="item"   // rename getItemList() to getElementList()
    // item=""       // suppress accessor completely
  ]
}
reference ::= id {
  methods=[
    nameIdentifier="id"  // rename getId() to getNameIdentifier()
    getReferences         // method mix-in for API
  ]
}
```

## 6. PsiGen.bnf — Comprehensive PSI Example

**Source: `testData/generator/PsiGen.bnf:1-76`**

```bnf
{
  classHeader="//header.txt"
  parserClass="PsiGen"
  psiClassPrefix="X"
  implements="XComposite"
  parserUtilClass="PsiGenUtil"
  extends(".*expr")=expr
  extends("root_.")="root"
  tokens=[OP_MUL="*" OP_DIV="/" SLASH='\' id='regexp:A' number='regexp:B']
  elementTypeClass("root_.*")="sample.MyRootType"
  elementTypeFactory(".*_expr")="sample.MyTypeFactory.createExprType"
  methods("expr")=[missing]
}
```

Demonstrates:
- `psiClassPrefix="X"` — All PSI classes prefixed with X.
- `implements="XComposite"` — All rules implement XComposite.
- Pattern-based `extends` — `extends(".*expr")=expr`.
- Pattern-based `elementTypeClass` — `elementTypeClass("root_.*")="sample.MyRootType"`.
- Pattern-based `elementTypeFactory` — `elementTypeFactory(".*_expr")="sample.MyTypeFactory.createExprType"`.
- `methods("expr")=[missing]` — Pattern-based method injection.
- `elementType` override — `external_type ::= number {elementType="missing_external_type"}`.
- `elementType` sharing — `external_type2 ::= id {elementType="id_expr"}`.
- `elementType=""` — suppress element type generation: `publicMethodToCall ::= identifier {elementType=""}`.
- Fake rules — `fake other_expr ::= expr +` and `fake namedElement ::= ...`.

### Expression Grammar with Left Rules
```bnf
expr ::= a_expr (',' a_expr) * {methods=[kids="expr"]}
private a_expr ::= b_expr plus_expr *
left plus_expr ::= '+' expr {extends="expr"}
private b_expr ::= id_expr mul_expr *
left mul_expr ::= '*' expr {extends="expr"}
```

### Fake Rule with Implements
```bnf
fake namedElement ::= identifier publicMethodToCall (id (',' id) *) {
  implements="com.intellij.psi.PsiNameIdentifierOwner"
}
fake wrapping_statement ::= statement
```

## 7. PsiAccessors.bnf — Advanced Accessor Patterns

**Source: `testData/generator/PsiAccessors.bnf:1-91`**

### Path-Based Accessors
```bnf
binary ::= expression operator expression {
  methods = [
    alias = "/expression"
    left = "/expression[0]"
    right = "/expression[1]"
    op = "/operator"
    left_left = "/expression[0]/value[0]"
    right_right = "/expression[1]/value[1]"
    last = "/expression[last]"
    first = "/expression[first]"
    right_left = "/expression[1]/value[0]"   // total nullable test
    left_right = "/expression[0]/value[1]"
    bad_index = "/expression[bad_index]/value[wrong_turn]"
  ]
  pin = "operator"
}
```

Index syntax:
- `/expr[0]` — first child of type
- `/expr[1]` — second child
- `/expr[last]` — last child
- `/expr[first]` — first child (same as [0])
- Multi-level paths: `/expression[0]/value[0]`

### Fake Rules with Per-Rule Package Override
```bnf
fake some-child ::= some-grand-child "something" something2 {
  methods=[smth1="MY_SOMETHING" smth2="MY_SOMETHING"]
  psiPackage="generated.psi.child"
  psiImplPackage="generated.psi.impl.child"
}
fake some-grand-child ::= MY_SOMETHING something2 {
  psiPackage="generated.psi.grand"
  psiImplPackage="generated.psi.impl.grand"
}
```

Per-rule `psiPackage` and `psiImplPackage` overrides for organizing PSI into sub-packages.

### Suppressing Accessors
```bnf
fake some-root ::= some-child value {
  methods=[
    value=""   // disable value accessor
  ]
}
```

### Token Accessors with generateTokenAccessors
```bnf
{
  generateTokenAccessors("some-.*")=true
}
```

Pattern-based token accessor generation control.

## 8. Stub Support

### stubClass Attribute

**Source: `HOWTO.md:346-381`**

Two approaches for stub indices:

**Direct implements/mixin approach:**
```bnf
property ::= id '=' expr {
  implements=[
    "com.sample.SampleElement"
    "com.intellij.psi.StubBasedPsiElement<com.sample.PropertyStub>"
  ]
  mixin="com.sample.SampleStubElement<com.sample.PropertyStub>"
}
```

**stubClass shorthand:**
```bnf
property ::= id '=' expr {
  stubClass="com.sample.PropertyStub"
}
```

**Source: `resources/messages/attributeDescriptions/stubClass.html`**

> Stub object class for StubIndex support. Generated PSI will implement StubBasedPsiElementBase and extend StubBasedPsiElementBase.

With `<?>` substitution:
```bnf
stub_element ::= {extends="com.sample.StubBase<?>" stubClass="com.sample.StubElementStub"}
```

### Stub.bnf Test Data

**Source: `testData/generator/Stub.bnf:1-32`**

```bnf
{
  generatePsi=true
  psiPackage="test.psi"
  psiImplPackage="test.psi.impl"
  parserClass="test.FooParser"
  elementTypeFactory="test.FooParserDefinition.createType"
  tokenTypeFactory="test.stub.FooParserDefinition.createTokenType"
  extends("element1|type")="org.intellij.grammar.test.StubTest.GenericBase<?>"
  extends("simple")="org.intellij.grammar.test.StubTest.SimpleBase"
  extends(".*type")=type
}
root ::= element1 | element2 | element3 | element4 | element5 | type
element1 ::= 'aa' element5   { stubClass="test.stub.Element1Stub" }
element2 ::= 'bb' element4*  { stubClass="test.stub.Element2Stub" }
element3 ::= 'bb' element4   { stubClass="test.stub.Element3Stub" }
element4 ::= 'bb' | element2 { stubClass="test.stub.Element4Stub" }

type ::= interface_type | struct_type {stubClass="test.stub.TypeStub"}
fake missing ::= { stubClass="test.stub.MissingStub" }
fake simple ::= { stubClass="org.intellij.grammar.test.StubTest.SimpleStub" }
```

Key patterns:
- `elementTypeFactory` is required for stubs to provide `IStubElementType`.
- `<?>` in `extends` is replaced with the stub class.
- Fake rules can also have stubs.
- The `extends(".*type")=type` makes subtypes share the parent's extends configuration.

### StubFallback.bnf

**Source: `testData/generator/StubFallback.bnf:12`**

```bnf
fallbackStubElementType="com.intellij.psi.tree.IElementType"
```

Overrides the default `IStubElementType` fallback when the parent class file isn't available during generation.

## 9. The `implements` Attribute

**Source: `resources/messages/attributeDescriptions/implements.html`**

```bnf
{
  implements("rule|attr")="org.intellij.grammar.psi.BnfNamedElement"
}
```

List of interfaces a PSI class will implement. Supports patterns.

## 10. The `extends` Attribute

**Source: `resources/messages/attributeDescriptions/extends.html`**

Base class or super rule for PSI classes:

```bnf
{
  extends(".*_expr")=expr  // super rule — also makes AST flat
}
// or
fake binary_expr ::= expression + {
  methods=[left="expression[0]" right="expression[1]"]
}
add_expr ::= expr '+' expr {extends=binary_expr}  // extends fake rule
```

## 11. UtilMethods.bnf — Method Injection Pattern

**Source: `testData/generator/UtilMethods.bnf:1-21`**

```bnf
{
  psiImplUtilClass="org.intellij.grammar.test.UtilMethods"
}
root ::= element1
element1 ::= 'aa' {
  methods = [
    foo0 foo1 foo2 foo3 foo4 foo5 foo6
  ]
}
```

Multiple methods injected at once. Each method name maps to a static method in `psiImplUtilClass` with the PSI element as the first parameter.

## 12. BindersAndHooks.bnf — Hooks with PSI

**Source: `testData/generator/BindersAndHooks.bnf:1-20`**

```bnf
{
  parserImports=[
    "static com.intellij.lang.WhitespacesBinders.*"
    "static com.sample.MyHooks.*" ]
}
root ::= left_binder right_binder both_binders
left_binder ::= A B { hooks=[leftBinder="GREEDY_LEFT_BINDER"] }
right_binder ::= item { hooks=[rightBinder="GREEDY_RIGHT_BINDER"] }
both_binders ::= A item B { hooks=[wsBinders="GREEDY_LEFT_BINDER, GREEDY_RIGHT_BINDER"] pin=1 }
got_hook ::= A { hooks=[myHook='"my", "hook", "param", "array"'] }
```

## 13. Rule Modifiers Affecting PSI

**Source: `README.md:131-147`**

| Modifier | Effect on PSI |
|---|---|
| `private` | Skip node creation; children included in parent |
| `left` | Takes previous sibling, becomes its parent |
| `inner` | Takes previous sibling, becomes its child (used with `left`) |
| `upper` | Takes parent node, replaces it by adopting children |
| `fake` | Only PSI classes generated, no parsing code |

Modifier combinations:
- `inner` should only be used with `left`.
- `private left` is equivalent to `private left inner`.
- `fake` should not be combined with `private`.

## 14. PSI Class Naming

**Source: `KnownAttribute.java:38-43`**

| Attribute | Default | Example |
|---|---|---|
| `psiClassPrefix` | `""` | `"Bnf"` → `BnfRule`, `BnfExpr` |
| `psiImplClassSuffix` | `"Impl"` | → `BnfRuleImpl`, `BnfExprImpl` |
| `psiPackage` | `"generated.psi"` | `"org.intellij.grammar.psi"` |
| `psiImplPackage` | `"generated.psi.impl"` | `"org.intellij.grammar.psi.impl"` |
| `psiVisitorName` | `"Visitor"` | `"GrammarVisitor"` |

## 15. elementType Attribute for PSI Sharing

**Source: `resources/messages/attributeDescriptions/elementType.html`**

Two rules can share the same element type and PSI:
```bnf
some_statement ::=
some_statement_alt_syntax ::= {elementType=some_statement}
```

Setting `elementType=""` suppresses element type and PSI class generation entirely:
```bnf
publicMethodToCall ::= identifier {elementType=""}
```
