# Section 2.6: External Rules — Examples

## Example 1: Simple External Rule

**Source: `HOWTO.md:96-119`**

Grammar declaration:
```bnf
{
  parserUtilClass="com.sample.SampleParserUtil"
}
external my_external_rule ::= parseMyExternalRule false 10
rule ::= part1 my_external_rule part3
```

Java implementation:
```java
public class SampleParserUtil {
  public static boolean parseMyExternalRule(PsiBuilder builder, int level,
                                            boolean extraArg1, int extraArg2) {
    // builder and level are always the first two parameters
    // extraArg1 = false, extraArg2 = 10 (from grammar declaration)
    return true;
  }
}
```

## Example 2: Inline External Expression

**Source: `HOWTO.md:96-119`**

```bnf
rule ::= part1 <<parseMyExternalRule true 5>> part3
```

Equivalent to the external rule form but inline. The `<<...>>` syntax can be used anywhere in a rule body.

## Example 3: Meta Rule — Comma-Separated List

**Source: `README.md:104-106`, `testData/generator/ExternalRules.bnf:38-45`**

```bnf
// Declaration: <<param>> is a placeholder for any parser expression
meta comma_list ::= <<param>> (',' <<param>>) *

// Usage: pass a rule or expression to fill <<param>>
item_list ::= <<comma_list item>>
keyword_list ::= <<comma_list ('if' | 'else' | 'while')>>
```

Generated code passes the argument as a `GeneratedParserUtilBase.Parser` lambda.

## Example 4: Meta Rule with Pinned Recovery

**Source: `testData/generator/ExternalRules.bnf:64-68`**

```bnf
// Meta rule accepting a recovery predicate as a parameter
private meta recoverable_item ::= <<param>> {recoverWhile="item_recover"}
private item_recover ::= !(',' | ';' | ')')

// Recovery predicate can also be a meta parameter
private meta recoverable_item2 ::= <<param>> {recoverWhile="<<recover_arg>>"}
private meta recoverable_item3 ::= <<recover_arg>> <<param>> {pin=1 recoverWhile="<<recover_arg>>"}
```

## Example 5: Nested Meta Rules

**Source: `testData/generator/ExternalRules.bnf:38-45, 77-79`**

```bnf
// Multi-level meta rules
meta comma_list ::= <<param>> (',' <<param>>) *
meta comma_list_pinned ::= <<head>> <<param>> (<<comma_list_tail <<param>>>>) *
meta comma_list_tail ::= ',' <<param>> {pin=1}
meta list_of_lists ::= <<head>> <<comma_list <<param>>>> (<<comma_list_tail <<comma_list <<param>>>>>>) *

// Two-parameter meta rule
meta two_params_meta ::= <<a>> <<b>>
private meta nested_meta ::= <<two_params_meta <<nested1>> <<two_params_meta <<nested2>> <<nested3>>>>>>
```

## Example 6: Parameter Passing Patterns

**Source: `testData/generator/ExternalRules.bnf:25-35`**

```bnf
// Passing a token literal
private perc_list ::= <<listOf '%'>>

// Passing a token name (rule reference)
private perc_re_list1 ::= <<listOf perc_re>>

// Passing a grouped expression
private perc_re_list2 ::= <<listOf (perc_re)>>

// Multiple mixed parameters
private param_seq ::= '{' <<uniqueListOf "1+1" '1+1' one two 10 some>> '}'

// Choice as single parameter
private param_choice ::= '{' <<uniqueListOf (one | two | 10 | some)>> '}'

// Optional as parameter
private param_opt ::= '{' <<uniqueListOf [one | two | 10 | some]>> '}'
```

## Example 7: External Root Rule

**Source: `grammars/Grammar.bnf:56`, `testData/generator/Small.bnf:8`**

```bnf
// Grammar-Kit's own grammar uses an external root:
external grammar ::= parseGrammar grammar_element

// Simple external root:
external root ::= parseRoot statement
```

## Example 8: Parser Imports for External Methods

**Source: `README.md:211-217`**

```bnf
{
  parserImports=["static org.sample.ManualParsing.*"]
}
// Now methods from ManualParsing can be referenced as external rules
rule ::= <<customParse param1 param2>>
```

## Parameter Type Summary

| Parameter Syntax | Java Type | Example |
|---|---|---|
| Rule name | `GeneratedParserUtilBase.Parser` | `<<comma_list item>>` |
| `(expr)` grouped | `GeneratedParserUtilBase.Parser` | `<<list (a \| b)>>` |
| `"double-quoted"` | `String` (as-is) | `<<method "1+1">>` |
| `'single-quoted'` | `String` (unquoted) | `<<method '1+1'>>` |
| `<<meta_param>>` | `GeneratedParserUtilBase.Parser` | Inside meta rule body |
