# Parser Generation

Grammar-Kit transforms BNF rules into a recursive-descent parser implemented as static Java methods. The generator reads your `.bnf` file, resolves attributes, and produces up to five categories of output files: the parser class, an element types holder, PSI interfaces, PSI implementation classes, and a visitor class.

## Running the Generator

You can trigger generation in three ways.

**IDE action** is the preferred approach. Open a `.bnf` file and press **Ctrl+Shift+G** (Windows/Linux) or **Cmd+Shift+G** (macOS). Grammar-Kit saves all open files, resolves the output directory from the `parserClass` attribute's package, runs the generator in a background task, and reports the number of files, total size, and duration in a notification. The output directory structure mirrors the Java package hierarchy.

**Command line** works for automation outside the IDE:

```bash
java -jar grammar-kit.jar src/gen src/grammars/MyLang.bnf
```

Or with an explicit classpath when the grammar-kit jar does not bundle all dependencies:

```bash
java -cp grammar-kit.jar:intellij-deps.jar \
  org.intellij.grammar.Main src/gen src/grammars/
```

**Gradle plugin** integrates generation into the build. Use the [gradle-grammar-kit-plugin](https://github.com/JetBrains/gradle-grammar-kit-plugin) for CI/CD pipelines and team builds. See [Build Integration](../integration/gradle-setup.md) for configuration details.

!!! warning
    The Gradle plugin does not support method mixins (two-pass generation is not implemented). Generic signatures and annotations may also differ. If your grammar uses `mixin` or `psiImplUtilClass` method injection, generate from the IDE and commit the output.

## Generated Files

The generator produces files in a fixed order. Each category can be controlled through attributes.

**Parser class.** One Java class (or several, if you use section-level `parserClass` overrides) containing a static method for each BNF expression. The class implements `LightPsiParser` and delegates to `GeneratedParserUtilBase` for marker management, error recovery, and section handling. The name and package come from the `parserClass` attribute.

**Element types holder.** An interface containing `IElementType` constants for all composite (rule) types and, if `tokens="yes"`, all token types. It also contains a `Factory` class with a `createElement` method that maps each element type to its PSI implementation:

```java
public interface MyTypes {
  IElementType STATEMENT = new IElementType("STATEMENT", MyLanguage.INSTANCE);
  IElementType EXPRESSION = new IElementType("EXPRESSION", MyLanguage.INSTANCE);

  IElementType PLUS = new MyTokenType("PLUS");
  IElementType NUMBER = new MyTokenType("NUMBER");

  class Factory {
    public static PsiElement createElement(ASTNode node) {
      IElementType type = node.getElementType();
      if (type == STATEMENT) return new StatementImpl(node);
      if (type == EXPRESSION) return new ExpressionImpl(node);
      throw new AssertionError("Unknown element type: " + type);
    }
  }
}
```

The holder class name comes from `elementTypeHolderClass`. Constant name casing is controlled by `generate=[element-case="upper"]` and `generate=[token-case="upper"]`. The `elementTypePrefix` attribute adds a prefix to all constant names.

**PSI interfaces.** One interface per non-private, non-fake rule that produces an AST node. Each interface extends the class or interface specified by `implements` (default: `PsiElement`) and contains getter methods for child elements.

**PSI implementation classes.** One class per PSI interface. Each extends the class specified by `extends` (default: `ASTWrapperPsiElement`) or the `mixin` class, and implements its corresponding interface. The class suffix is controlled by `psiImplClassSuffix` (default: `"Impl"`).

**Visitor class.** Generated when `generate=[visitor="yes"]` (the default). Contains a `visit` method for each PSI type, with dispatch following the `extends` hierarchy. The visitor class name comes from `psiVisitorName` (default: `"Visitor"`). If `visitor-value` is set, the visitor becomes generic: `Visitor<R>`.

## Grammar-to-Code Mapping

Understanding how BNF constructs map to Java helps when reading generated code or debugging parse failures.

A **sequence** becomes a short-circuit `&&` chain. If any part fails before a pin point, the parser rolls back:

```bnf
rule ::= part1 part2 part3
```

```java
public static boolean rule(PsiBuilder b, int l) {
  if (!recursion_guard_(b, l, "rule")) return false;
  boolean r;
  Marker m = enter_section_(b);
  r = part1(b, l + 1);
  r = r && part2(b, l + 1);
  r = r && part3(b, l + 1);
  exit_section_(b, m, RULE, r);
  return r;
}
```

An **ordered choice** becomes a fallthrough chain. The parser tries each alternative until one succeeds:

```bnf
rule ::= part1 | part2 | part3
```

```java
public static boolean rule(PsiBuilder b, int l) {
  if (!recursion_guard_(b, l, "rule")) return false;
  boolean r;
  Marker m = enter_section_(b);
  r = part1(b, l + 1);
  if (!r) r = part2(b, l + 1);
  if (!r) r = part3(b, l + 1);
  exit_section_(b, m, RULE, r);
  return r;
}
```

A **zero-or-more** repetition becomes a `while(true)` loop that always returns true (zero matches is valid):

```bnf
rule ::= part *
```

```java
public static boolean rule(PsiBuilder b, int l) {
  while (true) {
    if (!part(b, l + 1)) break;
  }
  return true;
}
```

**Expression rules** that use the `extends` pattern produce an optimized Pratt parser. Instead of one method per precedence level, Grammar-Kit generates two methods for the root expression rule and a priority table as a comment:

```java
// Expression root: expr
// Operator priority table:
// 0: BINARY(assign_expr)
// 1: BINARY(plus_expr) BINARY(minus_expr)
// 2: BINARY(mul_expr) BINARY(div_expr)
// 3: PREFIX(unary_plus_expr) PREFIX(unary_min_expr)
// 4: POSTFIX(factorial_expr)
// 5: ATOM(literal_expr) PREFIX(paren_expr)
public static boolean expr(PsiBuilder b, int l, int g) { ... }
```

The generator names sub-expression methods by appending position indices: `rule_name_0`, `rule_name_1_2`. Avoid naming your own rules in this `rule_name_N1_N2` pattern to prevent conflicts.

## Configuration

The `generate` attribute controls several aspects of the generated output. The most commonly adjusted options:

| Option | Values | Effect |
|---|---|---|
| `java` | 6, 8, **11** | Java version; affects lambda vs anonymous class syntax |
| `names` | **short**, long, classic | Variable names in generated parser (`b`/`l`/`r` vs `builder`/`level`/`result`) |
| `fqn` | yes, **no** | Fully qualified names instead of imports |
| `element-case` | lower, **upper**, as-is | Casing for element type constants |
| `token-case` | lower, **upper**, as-is | Casing for token type constants |
| `psi` | **yes**, no | Generate PSI classes |
| `visitor` | **yes**, no | Generate visitor class |
| `visitor-value` | **void**, type name | Visitor return type parameter |

Bold values are defaults. See [Attributes System](attributes.md) for the complete options table.

The `classHeader` attribute adds a comment header to all generated files. It accepts either literal text or a filename (resolved relative to the grammar file's directory):

```bnf
{
  classHeader="license.txt"
}
```

!!! tip
    Use `generate=[names="long"]` during development if you need to step through the generated parser in a debugger. Switch back to `names="short"` for production to keep the generated code compact.

For Gradle-based generation and CI/CD setup, see [Gradle Plugin Setup](../integration/gradle-setup.md).
