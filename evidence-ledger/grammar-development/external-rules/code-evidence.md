# Section 2.6: External Rules — Code Evidence

## 1. Rule Modifiers: External and Meta

**Source: `README.md:138-141`**

```
6. *external* (parser): a rule with a hand-written parse function; no parsing code is generated.
5. *meta* (parser): a parametrized rule; its parse function can take other parse functions as parameters.
```

## 2. External Rule Syntax

**Source: `README.md:149-170`**

### External Expression (inline variant)
```
rule ::= part1 <<parseMyExternalRule true 5>> part3
```

### External Rule Declaration
```
external manually_parsed_rule ::= methodName param1 param2 ...
```

### Key behavior:
- Double-quoted strings are passed "as is" as parameters.
- Single-quoted strings are **unquoted first** before passing.
- Rule references in parameter lists are implemented as `GeneratedParserUtilBase.Parser` instances.

## 3. External Rule Implementation Contract

**Source: `HOWTO.md:96-119`**

### Use cases:
1. When it's easier to do something right in code.
2. When there's an external dependency.
3. When logic is already implemented elsewhere.

### Grammar syntax:
```bnf
{
  parserUtilClass="com.sample.SampleParserUtil"
}
external my_external_rule ::= parseMyExternalRule false 10
rule ::= part1 my_external_rule part3
// alternative inline syntax:
// rule ::= part1 <<parseMyExternalRule true 5>> part3
```

### Java implementation:
```java
public class SampleParserUtil {
  public static boolean parseMyExternalRule(PsiBuilder builder, int level,       // required arguments
                                            boolean extraArg1, int extraArg2) {  // extra arguments
    // do the work
  }
}
```

The first two parameters (`PsiBuilder builder, int level`) are always required. Additional parameters follow in the order declared in the grammar.

## 4. Parser Utility Class Configuration

**Source: `resources/messages/attributeDescriptions/parserUtilClass.html`**

> Parser util class qualified name, most likely GeneratedParserUtilBase (default) or its subclass.

```bnf
{
  parserUtilClass="org.intellij.grammar.parser.GrammarParserUtil"
}
// parseGrammar reference resolves to
//   GrammarParserUtil#parseGrammar(PsiBuilder builder, int level)
external grammar ::= parseGrammar grammar_element
// alternative syntax:
grammar ::= <<parseGrammar grammar_element>>
```

## 5. Parser Imports for External Rule Methods

**Source: `README.md:211-217`**

External rule methods can be in any class, imported via `parserImports`:
```bnf
{
  parserImports=["static org.sample.ManualParsing.*"]
}
```

**Source: `resources/messages/attributeDescriptions/parserImports.html`**
```bnf
{
  parserImports=[
    "static com.sample.ExtraTokens.*"
  ]
}
```

## 6. Meta Rule Syntax and Patterns

**Source: `README.md:104-106, 154-157`**

Basic meta rule:
```bnf
private meta list ::= <<p>> (',' <<p>>) *
private list_usage ::= <<list rule_D>>
```

With named parameters:
```bnf
meta comma_separated_list ::= <<param>> ( ',' <<param>> ) *
option_list ::= <<comma_separated_list (OPTION1 | OPTION2 | OPTION3)>>
```

## 7. ExternalRules.bnf — Comprehensive Test Data

**Source: `testData/generator/ExternalRules.bnf` (100 lines)**

### External Rule Declarations (lines 15-19)
```bnf
root ::= <<listOf statement>>
external ref ::= parseRef
external unique_list_of ::= uniqueListOf
external unique_list_of_params ::= uniqueListOf <<p1>> "1+1" <<p2>> '1+1'
external empty_external ::=
```

Key patterns:
- `external ref ::= parseRef` — simple external rule mapping to a method name.
- `external unique_list_of_params ::= uniqueListOf <<p1>> "1+1" <<p2>> '1+1'` — external rule with mixed meta-parameters and literal arguments.
- `external empty_external ::=` — empty external rule (no method name).

### Meta Rules (lines 38-45)
```bnf
meta comma_list ::= <<param>> (',' <<param>>) *
meta comma_list_pinned ::= <<head>> <<param>> (<<comma_list_tail <<param>>>>) *
meta comma_list_tail ::= ',' <<param>> {pin=1}
meta list_of_lists ::= <<head>> <<comma_list <<param>>>> (<<comma_list_tail <<comma_list <<param>>>>>>) *
meta meta_multi_level ::= <<comma_list <<comma_list <<comma_list <<comma_list <<comma_list <<param>>>>>>>>>>>>
```

### Parameter Passing Patterns (lines 25-35)
```bnf
private perc_list ::= <<listOf '%'>>                              // passing a token literal
private perc_re_list1 ::= <<listOf perc_re>>                      // passing a token name
private perc_re_list2 ::= <<listOf (perc_re)>>                    // passing a grouped expression
private param_seq ::= '{' <<uniqueListOf "1+1" '1+1' one two 10 some>> '}'  // multiple mixed params
private param_choice ::= '{' <<uniqueListOf (one | two | 10 | some)>> '}'   // choice as param
private param_opt ::= '{' <<uniqueListOf [one | two | 10 | some]>> '}'      // optional as param
private param_choice_alt ::= '{' <<uniqueListOf {one | two | 10 | some}>> '}'  // braces choice
```

### Nested Meta Rules (lines 77-79)
```bnf
meta two_params_meta ::= <<a>> <<b>>
private meta nested_meta ::= <<two_params_meta <<nested1>> <<two_params_meta <<nested2>> <<nested3>>>>>>
private meta nested_mixed ::= <<two_params_meta (<<two_params_meta '%' <<c>>>>) perc_re>>
```

### Recovery in Meta Rules (lines 64-68)
```bnf
private meta recoverable_item ::= <<param>> {recoverWhile="item_recover"}
private item_recover ::= !(',' | ';' | ')')

private meta recoverable_item2 ::= <<param>> {recoverWhile="<<recover_arg>>"}
private meta recoverable_item3 ::= <<recover_arg>> <<param>> {pin=1 recoverWhile="<<recover_arg>>"}
```

Meta rules can accept recovery predicates as parameters using `<<recover_arg>>` syntax.

### Multi-Parser External Rules (lines 81-99)
```bnf
private meta main_class_meta ::= <<p>>
private second_class_meta_usage_from_main ::= <<comma_list <<second_class_meta some>>>>

;{
  parserClass="ExternalRules2"
}
private meta second_class_meta ::= <<bmp>>
private main_class_meta_usage_from_second ::= <<comma_list <<main_class_meta some>>>>
```

Meta rules can reference meta rules from other parser classes, demonstrating cross-class interaction.

## 8. ExternalRulesLambdas.bnf — Lambda Generation

**Source: `testData/generator/ExternalRulesLambdas.bnf` (93 lines)**

Uses `generate=[java='8']` to enable lambda generation:
```bnf
{
  parserClass="ExternalRulesLambdas"
  generate=[
    psi='no'
    java='8'
  ]
}
```

Same patterns as ExternalRules.bnf but generates Java 8+ lambdas instead of anonymous classes for Parser instances.

## 9. Small.bnf — Simple External Root

**Source: `testData/generator/Small.bnf:8`**

```bnf
external root ::= parseRoot statement
```

Demonstrates an external root rule that delegates to `parseRoot` and passes `statement` as a rule argument.

## 10. LivePreviewParser External Expression Support

**Source: `src/org/intellij/grammar/livePreview/LivePreviewParser.java:424-512`**

The Live Preview parser handles external expressions by:
1. Resolving the target rule from the first expression.
2. For meta rules, building an argument map from parameter names to Parser lambdas.
3. Hard-coded external functions: `eof` (checks end-of-file) and `anything` (skips tokens with error recovery).
4. External rules referencing static methods (non-meta) are **not supported** — returns false.

## 11. Key Concepts Summary

### External Rule vs. External Expression
- **External rule**: `external my_rule ::= methodName params...` — declares a named rule backed by hand-written code.
- **External expression**: `<<methodName params...>>` — inline version, usable anywhere in a rule body.

### Meta Rule
- **Declaration**: `meta comma_list ::= <<param>> (',' <<param>>) *`
- **Usage**: `list ::= <<comma_list item>>` — the expression passed replaces `<<param>>`.
- Meta rules are **parametrized**: their parse function takes other parse functions as parameters.
- Parameters are wrapped as `GeneratedParserUtilBase.Parser` instances.

### Parameter Types
1. **Rule references**: Become Parser instances.
2. **Double-quoted strings**: Passed as-is (e.g., `"1+1"` stays `"1+1"`).
3. **Single-quoted strings**: Unquoted first (e.g., `'1+1'` becomes `1+1`).
4. **Grouped expressions**: `(one | two)` is passed as a single Parser instance.
