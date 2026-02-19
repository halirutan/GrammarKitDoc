# Section 3.4: PSI Customization — Examples

## Example 1: Flat AST with extends

**Source: `HOWTO.md:226-251`**

```bnf
{
  extends(".*_expr")=expr
  tokens = [PLUS='+' MINUS='-']
}
expr ::= factor add_expr *
private factor ::= primary mul_expr *
private primary ::= literal_expr
left add_expr ::= ('+'|'-') factor
left mul_expr ::= ('*'|'/') primary
literal_expr ::= number
```

Result: `FileNode → LiteralExpr` instead of `FileNode → Expr → LiteralExpr`.

## Example 2: Fake Rules for PSI Hierarchy

**Source: `HOWTO.md:253-301`**

```bnf
{
  extends("(add|mul)_expr")=binary_expr
  extends(".*_expr")=expr
}
fake binary_expr ::= expr + {
  methods=[
    left="/expr[0]"     // @NotNull
    right="/expr[1]"    // @Nullable
  ]
}
```

Generates:
```java
public interface BinaryExpr extends Expr {
  List<Expr> getExprList();
  @NotNull Expr getLeft();
  @Nullable Expr getRight();
}
public interface AddExpr extends BinaryExpr { }
public interface MulExpr extends BinaryExpr { }

// Visitor respects hierarchy:
public void visitAddExpr(AddExpr o) { visitBinaryExpr(o); }
public void visitBinaryExpr(BinaryExpr o) { visitExpr(o); }
```

## Example 3: Mixin Class

**Source: `HOWTO.md:304-321`**

```bnf
{
  mixin("my_named")="com.sample.psi.impl.MyNamedImplMixin"
}
my_named ::= part1 part2 part3
```

```java
public class MyNamedImplMixin extends ASTWrapperPsiElement implements PsiNamedElement {
  public MyNamedImplMixin(@NotNull ASTNode node) { super(node); }

  @Nullable @NonNls
  public String getName() { /* ... */ }

  public PsiElement setName(@NonNls @NotNull String name) { /* ... */ }
}
```

## Example 4: Method Injection via psiImplUtilClass

**Source: `HOWTO.md:323-341`**

```bnf
{
  psiImplUtilClass="com.sample.SamplePsiImplUtil"
  implements("my_named")="com.intellij.psi.PsiNamedElement"
}
my_named ::= part1 part2 part3 {
  methods=[getName setName]
}
```

```java
public class SamplePsiImplUtil {
  // Extra first parameter is the PSI element
  public static @Nullable String getName(MyNamed o) {
    return o.getPart1().getText();
  }
  public static PsiElement setName(MyNamed o, @NotNull String name) {
    // replace the element
  }
}
```

## Example 5: Path-Based Accessors

**Source: `testData/generator/PsiAccessors.bnf`**

```bnf
binary ::= expression operator expression {
  methods = [
    alias = "/expression"                    // List<Expression> alias
    left = "/expression[0]"                  // @NotNull first expression
    right = "/expression[1]"                 // @Nullable second expression
    op = "/operator"                         // single child
    left_left = "/expression[0]/value[0]"    // multi-level path
    last = "/expression[last]"               // last child
    first = "/expression[first]"             // first child
  ]
}
```

## Example 6: Per-Rule Package Override

**Source: `testData/generator/PsiAccessors.bnf`**

```bnf
fake some-child ::= some-grand-child "something" {
  psiPackage="generated.psi.child"
  psiImplPackage="generated.psi.impl.child"
}
fake some-grand-child ::= MY_SOMETHING {
  psiPackage="generated.psi.grand"
  psiImplPackage="generated.psi.impl.grand"
}
```

## Example 7: Stub Index Support

**Source: `testData/generator/Stub.bnf`, `HOWTO.md:346-381`**

```bnf
{
  elementTypeFactory="test.FooParserDefinition.createType"
  extends("element1|type")="org.intellij.grammar.test.StubTest.GenericBase<?>"
}
element1 ::= 'aa' element5 { stubClass="test.stub.Element1Stub" }
// <?> becomes <test.stub.Element1Stub>
// Generated Impl extends StubBasedPsiElementBase<Element1Stub>
```

## Example 8: Rule Modifiers and PSI Effects

**Source: `README.md:131-147`**

| Modifier | Example | PSI Effect |
|---|---|---|
| `private` | `private factor ::= primary` | No AST node; children merge into parent |
| `left` | `left add_expr ::= '+' factor` | Previous sibling becomes child |
| `inner` + `left` | `left inner impl ::= '{' body '}'` | Previous sibling stays parent |
| `upper` | `upper wrapper ::= '{' content '}'` | Replaces parent, adopts siblings |
| `fake` | `fake binary_expr ::= expr +` | PSI classes only, no parser code |
