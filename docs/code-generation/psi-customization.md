# PSI Customization

Grammar-Kit generates a PSI interface and an implementation class for each public rule in your grammar. By default, every implementation extends `ASTWrapperPsiElement` and every interface extends `PsiElement`. These defaults produce a working PSI tree, but most real-world plugins need a richer type hierarchy, custom accessor methods, and integration with IntelliJ features like navigation and refactoring.

This section covers the attributes and patterns that let you reshape the generated PSI to fit your language's needs.

## Shaping the Type Hierarchy

The `extends` and `implements` attributes control the inheritance structure of generated PSI classes.

When `extends` names another grammar rule, two things happen. First, the generated PSI interface for the current rule extends the named rule's interface instead of `PsiElement`. Second, the parser collapses the AST -- it drops the intermediate node, producing a flatter tree. For expression grammars, this is essential:

```bnf
{
  extends(".*_expr")=expr
}
expr ::= factor add_expr *
private factor ::= primary mul_expr *
private primary ::= literal_expr
left add_expr ::= ('+'|'-') factor
left mul_expr ::= ('*'|'/') primary
literal_expr ::= number
```

Without `extends`, parsing `42` produces `FileNode -> Expr -> LiteralExpr`. With `extends(".*_expr")=expr`, it produces `FileNode -> LiteralExpr` directly. The `Expr` wrapper node is eliminated because `LiteralExpr` already extends `Expr` in the PSI hierarchy.

When `extends` names a Java class instead of a grammar rule, it sets the base class for the implementation without affecting the AST structure:

```bnf
{
  extends="com.example.psi.impl.MyBaseElement"
}
```

The `implements` attribute adds interfaces to the generated PSI interface. It accepts a list and supports pattern-based application:

```bnf
{
  implements("rule|attr")="org.intellij.grammar.psi.BnfNamedElement"
}
```

The `private` modifier prevents a rule from creating an AST node. Its matched content is included directly in the parent node. Use `private` on intermediate rules that exist only for grammar structure and do not need a PSI representation. Mark rules as `private` as early as possible in your grammar design -- it keeps the AST shallow and avoids unnecessary PSI classes.

The generated visitor respects the `extends` hierarchy. If `AddExpr` extends `BinaryExpr` which extends `Expr`, the visitor dispatches `visitAddExpr` to `visitBinaryExpr` to `visitExpr`, so you can handle groups of related types at any level.

## Fake Rules

Fake rules generate PSI interfaces and implementations without producing any parsing code. They exist only to shape the PSI hierarchy -- to create abstract base types that real rules extend.

```bnf
{
  extends("(add|mul)_expr")=binary_expr
  extends(".*_expr")=expr
}
fake binary_expr ::= expr + {
  methods=[
    left="/expr[0]"
    right="/expr[1]"
  ]
}
```

This generates an interface that `AddExpr` and `MulExpr` both extend:

```java
public interface BinaryExpr extends Expr {
  @NotNull List<Expr> getExprList();
  @NotNull Expr getLeft();
  @Nullable Expr getRight();
}

public interface AddExpr extends BinaryExpr { }
public interface MulExpr extends BinaryExpr { }
```

The `+` quantifier in the fake rule's body (`expr +`) tells the generator that the `left` accessor (first child) is `@NotNull` while `right` (second child) is `@Nullable`. Without the `+`, both would be nullable.

Fake rules can also declare `implements` to add interfaces, and they can override `psiPackage` and `psiImplPackage` to place their generated classes in separate sub-packages:

```bnf
fake some_child ::= some_grand_child "something" {
  psiPackage="generated.psi.child"
  psiImplPackage="generated.psi.impl.child"
}
```

!!! warning
    Do not combine `fake` with `private`. A fake rule needs to generate PSI classes, and `private` suppresses PSI generation.

## Custom Methods and Accessors

The `methods` attribute defines three kinds of entries: path-based accessors, method mix-ins, and accessor renames.

**Path-based accessors** use a `/` prefix and an optional index to create getters that navigate the PSI tree:

```bnf
binary ::= expression operator expression {
  methods = [
    left = "/expression[0]"
    right = "/expression[1]"
    op = "/operator"
  ]
}
```

The index syntax supports `[0]` (first child of type), `[1]` (second), `[first]`, and `[last]`. Multi-level paths navigate deeper: `/expression[0]/value[0]` returns the first `value` child of the first `expression` child.

**Method mix-ins** list method names that map to static methods in the `psiImplUtilClass`. The generator adds the method to the PSI interface and delegates the implementation to the utility class:

```bnf
{
  psiImplUtilClass="com.example.SamplePsiImplUtil"
  implements("my_named")="com.intellij.psi.PsiNamedElement"
}
my_named ::= part1 part2 part3 {
  methods=[getName setName]
}
```

The utility class provides static methods where the first parameter is the PSI element:

```java
public class SamplePsiImplUtil {
  public static @Nullable String getName(MyNamed o) {
    return o.getPart1().getText();
  }
  public static PsiElement setName(MyNamed o, @NotNull String name) {
    // replace the element
  }
}
```

You do not need to specify parameter types or return types in the `methods` attribute -- Grammar-Kit resolves them from the utility class.

**Accessor renames** change the name of an auto-generated getter. Setting the value to an empty string suppresses the accessor:

```bnf
list ::= item + {
  methods=[
    element="item"    // renames getItemList() to getElementList()
    // item=""        // would suppress getItemList() entirely
  ]
}
```

## Mixins and Method Injection

The `mixin` attribute sets the implementation base class for a rule. This is how you integrate with IntelliJ contracts like `PsiNamedElement` or `PsiReference`:

```bnf
{
  mixin("my_named")="com.example.psi.impl.MyNamedImplMixin"
}
my_named ::= part1 part2 part3
```

The mixin class replaces `ASTWrapperPsiElement` as the base class of the generated `MyNamedImpl`:

```java
public class MyNamedImplMixin extends ASTWrapperPsiElement
    implements PsiNamedElement {
  public MyNamedImplMixin(@NotNull ASTNode node) { super(node); }

  @Nullable public String getName() { /* ... */ }
  public PsiElement setName(@NotNull String name) { /* ... */ }
}
```

The `psiImplUtilClass` approach (described above in the methods section) is an alternative to mixins. It uses static methods rather than inheritance, which can be simpler when you only need to add a few methods without changing the base class.

!!! warning
    The Gradle plugin does not support method mixins because two-pass generation is not implemented. If your grammar uses `mixin` or method injection through `psiImplUtilClass`, generate from the IDE and commit the generated files.

## Stub Support

Stubs enable persistent indexing of PSI elements, allowing IntelliJ to look up symbols without parsing every file. Grammar-Kit provides the `stubClass` attribute as a shorthand for the verbose `implements`/`extends` configuration that stub support normally requires.

The concise form:

```bnf
{
  elementTypeFactory="com.example.MyParserDefinition.createType"
  extends("element1|type")="com.example.StubBase<?>"
}
element1 ::= 'aa' element5 { stubClass="com.example.stub.Element1Stub" }
```

The `<?>` in the `extends` value is replaced with the `stubClass` value during generation, producing `StubBase<Element1Stub>` as the base class. The generated implementation extends `StubBasedPsiElementBase` instead of `ASTWrapperPsiElement`.

An `elementTypeFactory` is required for stub support because stubs need `IStubElementType` instances rather than plain `IElementType`. The factory method must return the appropriate stub element type.

The `fallbackStubElementType` attribute handles compilation order issues. If the parent class is not yet compiled when the generator runs, it cannot determine the element type class from the parent. Setting `fallbackStubElementType` provides an explicit fallback:

```bnf
{
  fallbackStubElementType="com.intellij.psi.tree.IElementType"
}
```

This is a per-parser attribute and cannot be overridden on individual rules.

For more on the `elementType` attribute (sharing types between rules, suppressing generation), see [Attributes System](attributes.md). For the complete attribute catalog, see the [Attribute Reference](../reference/attributes.md).
