# Section 3.2: Parser Generation — Examples

## Example 1: Generated Code for Sequence Rule

**Source: `HOWTO.md:18-68`**

Grammar:
```bnf
rule ::= part1 part2 part3
```

Generated code pattern:
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

## Example 2: Generated Code for Choice Rule

Grammar:
```bnf
rule ::= part1 | part2 | part3
```

Generated code pattern:
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

## Example 3: Expression Parser Generation

**Source: `testData/generator/ExprParser.bnf`**

Grammar:
```bnf
{
  extends(".*expr")=expr
  elementTypeFactory="org.intellij.grammar.expression.ExpressionParserDefinition.createType"
}
expr ::= assign_expr | conditional_group | add_group | mul_group | ...
assign_expr ::= expr '=' expr { rightAssociative=true }
plus_expr ::= expr '+' expr
mul_expr ::= expr '*' expr
```

Generated: two methods with a priority table comment:
```java
// Expression root: expr
// Operator priority table:
// 0: BINARY(assign_expr)
// 1: BINARY(plus_expr) BINARY(minus_expr)
// 2: BINARY(mul_expr) BINARY(div_expr)
// 3: PREFIX(unary_plus_expr) PREFIX(unary_min_expr)
// 4: N_ARY(exp_expr)
// 5: POSTFIX(factorial_expr)
// 6: ATOM(simple_ref_expr) ATOM(literal_expr) PREFIX(paren_expr)
public static boolean expr(PsiBuilder b, int l, int g) { ... }
```

## Example 4: Generated Element Types Holder

**Source: `ParserGenerator.java:277-341`**

For a grammar with rules `statement`, `expression`, and tokens `PLUS`, `NUMBER`:
```java
public interface GeneratedTypes {
  IElementType STATEMENT = new IElementType("STATEMENT", MyLanguage.INSTANCE);
  IElementType EXPRESSION = new IElementType("EXPRESSION", MyLanguage.INSTANCE);

  IElementType PLUS = new IElementType("PLUS", MyLanguage.INSTANCE);
  IElementType NUMBER = new IElementType("NUMBER", MyLanguage.INSTANCE);

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

## Example 5: Generation Options

**Source: `testData/generator/GenOptions.bnf`**

```bnf
{
  parserClass="GenOptions"
  generate=[java="7" fqn="yes" visitor-value="Val" token-case="lower"
            element-case="upper" psi-classes-map="yes"]
}
```

Effects:
- `java="7"` — anonymous classes instead of lambdas
- `fqn="yes"` — fully qualified names in generated code (no imports)
- `visitor-value="Val"` — generates `Visitor<Val>`
- `token-case="lower"` — token constants in lowercase
- `element-case="upper"` — element constants in uppercase
- `psi-classes-map="yes"` — adds IElementType→Class map

## Example 6: Command-Line Generation

**Source: `HOWTO.md:400-424`**

```bash
# Using the grammar-kit jar directly
java -jar grammar-kit.jar src/gen src/grammars/MyLang.bnf

# With explicit classpath
java -cp grammar-kit.jar;intellij-deps.jar \
  org.intellij.grammar.Main src/gen src/grammars/
```

## Example 7: Variable Naming Styles

**Source: `Names.java:13-63`**

| Style | `generate=[names="..."]` | Builder | Level | Marker | Result |
|---|---|---|---|---|---|
| `short` (default) | `names="short"` | `b` | `l` | `m` | `r` |
| `long` | `names="long"` | `builder` | `level` | `marker` | `result` |
| `classic` | `names="classic"` | `builder_` | `level_` | `marker_` | `result_` |
