# External Rules

Some parsing tasks are easier to handle in Java than in BNF. External rules let you delegate part of the parsing to hand-written code while keeping the rest of the grammar declarative. Meta rules take this further by letting you write parametrized grammar patterns that accept other parse expressions as arguments.

Use external rules when:

- The parsing logic is easier to write directly in code.
- You need to call into an existing parser or library.
- The logic involves context-sensitive decisions that BNF cannot express.

## External Rule Syntax

Grammar-Kit provides two ways to call external parsing code. The first is a named declaration. The second is an inline expression you can place anywhere in a rule body.

A named external rule maps a grammar rule to a Java method:

```bnf
{
  parserUtilClass="com.sample.SampleParserUtil"
}
external my_external_rule ::= parseMyExternalRule false 10
rule ::= part1 my_external_rule part3
```

The equivalent inline form uses double angle brackets:

```bnf
rule ::= part1 <<parseMyExternalRule true 5>> part3
```

Both forms call the same kind of Java method. The method must be a public static method whose first two parameters are always `PsiBuilder builder` and `int level`. Any additional parameters declared in the grammar follow in order:

```java
public class SampleParserUtil {
  public static boolean parseMyExternalRule(PsiBuilder builder, int level,
                                            boolean extraArg1, int extraArg2) {
    // builder and level are always present
    // extraArg1 and extraArg2 come from the grammar declaration
    return true;
  }
}
```

The method returns `true` if parsing succeeded and `false` otherwise.

Grammar-Kit resolves external methods by looking in the class specified by the `parserUtilClass` attribute. If your methods live in a different class, use `parserImports` to add static imports:

```bnf
{
  parserImports=["static org.sample.ManualParsing.*"]
}
rule ::= <<customParse param1 param2>>
```

## Meta Rules

A meta rule is a parametrized grammar pattern. You declare it with the `meta` modifier and use `<<param>>` as a placeholder for parse expressions that callers supply. This lets you define reusable patterns like comma-separated lists without repeating the structure for every element type.

The canonical example is a comma-separated list:

```bnf
meta comma_list ::= <<param>> (',' <<param>>) *
```

To use it, pass a rule or expression in place of `<<param>>`:

```bnf
item_list ::= <<comma_list item>>
keyword_list ::= <<comma_list ('if' | 'else' | 'while')>>
```

When Grammar-Kit generates code, each argument passed to a meta rule becomes a `GeneratedParserUtilBase.Parser` instance. The generated method receives these as function parameters and calls them during parsing.

Parameters follow specific quoting rules:

| Parameter syntax | Java type | Example |
|---|---|---|
| Rule name | `Parser` instance | `<<comma_list item>>` |
| `(expr)` grouped | `Parser` instance | `<<comma_list (a \| b)>>` |
| `"double-quoted"` | String (as-is) | `<<method "1+1">>` |
| `'single-quoted'` | String (unquoted) | `<<method '1+1'>>` |
| `<<meta_param>>` | `Parser` instance | Inside meta rule body |

### Nested Meta Rules

Meta rules compose naturally. You can pass one meta rule invocation as an argument to another:

```bnf
meta comma_list ::= <<param>> (',' <<param>>) *
meta comma_list_tail ::= ',' <<param>> {pin=1}
meta comma_list_pinned ::= <<head>> <<param>> (<<comma_list_tail <<param>>>>) *
meta list_of_lists ::= <<head>> <<comma_list <<param>>>> (<<comma_list_tail <<comma_list <<param>>>>>>) *
```

A meta rule can also accept multiple parameters:

```bnf
meta two_params_meta ::= <<a>> <<b>>
private meta nested_meta ::= <<two_params_meta <<nested1>> <<two_params_meta <<nested2>> <<nested3>>>>>>
```

The nesting can go deep, but readability drops quickly. Keep meta rule nesting to two or three levels when possible.

### Recovery in Meta Rules

Recovery predicates can be passed as meta parameters. This lets you write a reusable "recoverable item" pattern where the caller decides the recovery condition:

```bnf
private meta recoverable_item ::= <<param>> {recoverWhile="item_recover"}
private item_recover ::= !(',' | ';' | ')')

// Recovery predicate as a meta parameter
private meta recoverable_item2 ::= <<param>> {recoverWhile="<<recover_arg>>"}
private meta recoverable_item3 ::= <<recover_arg>> <<param>> {pin=1 recoverWhile="<<recover_arg>>"}
```

The `recoverWhile="<<recover_arg>>"` syntax tells Grammar-Kit to use whatever parse expression the caller passes as the recovery predicate. See [Error Recovery](error-recovery.md) for more on `recoverWhile` and `pin`.

## Limitations and Live Preview

External rules that call static Java methods do not work in [Live Preview](live-preview.md). The preview parser cannot resolve or invoke your `parserUtilClass` methods, so any rule that depends on external code returns false during preview.

Two built-in external expressions work in Live Preview:

- `<<eof>>` checks whether the parser has reached the end of input.
- `<<anything>>` consumes tokens with error recovery (skips forward).

Meta rules work normally in Live Preview because they are interpreted directly from the grammar without calling external Java methods.

!!! note
    If your grammar relies heavily on external rules, you will need to test with the generated parser rather than Live Preview. Consider isolating external rule usage so that most of your grammar remains previewable.

When meta rules reference other meta rules across [parser class boundaries](grammar-composition.md), the generated code handles the cross-class calls automatically. You can define a meta rule in one parser class and invoke it from another without any special configuration.
