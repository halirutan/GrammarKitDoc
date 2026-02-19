# Section 3.2: Parser Generation — Code Evidence

## 1. Generation Trigger

### IDE Action

**Source: `src/org/intellij/grammar/actions/GenerateAction.java:51-202`**

- Action class: `GenerateAction extends AnAction`
- Keyboard shortcut: **Ctrl-Shift-G / Cmd-Shift-G** (from `README.md:39`)
- Only enabled when selected files contain `.bnf` files (`BnfFile` instances).
- Flow:
  1. Commits all documents and saves all files.
  2. Resolves target directory from `parserClass` attribute.
  3. Runs `ParserGenerator.generate()` in a background task with progress indicator.
  4. Reports results via notifications (file count, size, duration).
  5. Refreshes virtual file system (`VfsUtil.markDirtyAndRefresh`).

### Gradle Integration

**Source: `README.md:44-51`**

> Invoking the parser generator from an IDE as described above is the preferred way.
> Otherwise use [gradle-grammar-kit-plugin](https://github.com/JetBrains/gradle-grammar-kit-plugin) if the following limitations are not critical:
> * Method mixins are not supported (two-pass generation is not implemented)
> * Generic signatures and annotations may not be correct

### Standalone Usage

**Source: `HOWTO.md:400-424`**

Command-line invocation:
```
java -jar grammar-kit.jar <output-dir> <grammars-and-dirs>
```
Or with explicit classpath:
```
java -cp grammar-kit.jar;<all-the-needed-jars> org.intellij.grammar.Main <output-dir> <grammars-and-dirs>
```

## 2. ParserGenerator Class

**Source: `src/org/intellij/grammar/generator/ParserGenerator.java:57-58`**

```java
public class ParserGenerator extends GeneratorBase {
  public static final Logger LOG = Logger.getInstance(ParserGenerator.class);
```

### Constructor (lines 135-180)

Initialization steps:
1. Creates `GenOptions` from grammar attributes.
2. Resolves `parserUtilClass`, `psiImplUtilClass`, `psiTreeUtilClass`.
3. Computes visitor class name from `psiVisitorName` attribute.
4. Collects token text-to-name mappings.
5. Builds `RuleGraphHelper`, `ExpressionHelper`, `RuleMethodsHelper`, `BnfFirstNextAnalyzer`.
6. Initializes `JavaHelper` for type resolution.
7. Builds `RuleInfo` for every rule (name, elementType, parserClass, packages, mixin, stub).
8. Calculates fake rules, stub names, and abstract rules.

### RuleInfo Data (lines 60-93)

Per-rule generation metadata:
```java
static class RuleInfo {
    final String name;
    final boolean isFake;
    final String elementType;
    final String parserClass;
    final String intfPackage;
    final String implPackage;
    final String intfClass;
    final String implClass;
    final String mixin;
    final String stub;
    String realStubClass;
    Set<String> superInterfaces;
    boolean mixedAST;
    String realSuperClass;
    boolean isAbstract;
    boolean isInElementType;
}
```

## 3. Generation Process

**Source: `src/org/intellij/grammar/generator/ParserGenerator.java:277-341`**

The `generate()` method produces files in this order:

### Step 1: Parser Classes
```java
generateParser();
```
Generates the main parser class and any additional parser classes (from `;{ parserClass="..." }` sections).

### Step 2: Element Types Holder
```java
if (myGrammarRoot != null && (G.generateTokenTypes || G.generateElementTypes || G.generatePsi && G.generatePsiFactory)) {
    generateElementTypesHolder(myTypeHolderClass, sortedCompositeTypes);
}
```
Contains:
- IElementType constants for all composite (rule) types
- IElementType constants for all token types (if `generateTokens=true`)
- PSI factory method (if `generatePsiFactory=true`)
- PSI classes map (if `psi-classes-map="yes"`)

### Step 3: PSI Interface Classes
```java
for (BnfRule rule : sortedPsiRules.values()) {
    generatePsiIntf(rule, info);
}
```
One interface per non-private, non-fake rule that has PSI.

### Step 4: PSI Implementation Classes
```java
for (BnfRule rule : sortedPsiRules.values()) {
    generatePsiImpl(rule, info);
}
```
One Impl class per PSI interface.

### Step 5: Visitor Class
```java
if (myVisitorClassName != null && myGrammarRoot != null) {
    generateVisitor(myVisitorClassName, sortedPsiRules);
}
```
Generated if `generate=[visitor="yes"]` (default).

## 4. Generated Parser Code Structure

**Source: `README.md:113-120`**

Generator creates a static method for each BNF expression:
```java
static boolean rule_name(..)               // rule top level expression
static boolean rule_name_0(..)             // rule sub-expression
...
static boolean rule_name_N1_N2_..._NX      // nested sub-expression
```

Naming a rule like `rule_name_N1_N2_..._NX` shall be avoided to prevent conflicts.

### Grammar-to-Code Mappings

**Source: `HOWTO.md:18-68`**

**Sequence:**
```java
// rule ::= part1 part2 part3
public boolean rule() {
    boolean result = false;
    result = part1();
    result = result && part2();
    result = result && part3();
    if (!result) <rollback>
    return result;
}
```

**Ordered choice:**
```java
// rule ::= part1 | part2 | part3
public boolean rule() {
    boolean result = false;
    result = part1();
    if (!result) result = part2();
    if (!result) result = part3();
    if (!result) <rollback>
    return result;
}
```

**Zero-or-more:**
```java
// rule ::= part *
public boolean rule() {
    while (true) {
        if (!part()) break;
    }
    return true;
}
```

## 5. GeneratorBase: Common Infrastructure

**Source: `src/org/intellij/grammar/generator/GeneratorBase.java:28-231`**

Provides:
- File output management (`openOutput`, `closeOutput`, `openOutputInner`)
- Java class header generation with import management
- Package name derivation from class names
- Indentation-aware output via `out()` method
- `NameShortener` for import optimization
- `classHeader` handling: reads from file or uses text directly

### Output File Layout
Files are written to `outputPath` with directory structure matching the package:
```java
File file = new File(myOutputPath, classNameAdjusted.replace('.', File.separatorChar) + ".java");
```

### Class Header Options
```java
String getStringOrFile(String classHeader) {
    File file = new File(mySourcePath, classHeader);
    if (file.exists()) return FileUtil.loadFile(file);
    // Otherwise: treat as text, wrapping in comments if needed
}
```

## 6. GenOptions: Generation Configuration

**Source: `src/org/intellij/grammar/generator/GenOptions.java:21-67`**

All generation options parsed from grammar attributes:

| Field | Type | Source |
|---|---|---|
| `names` | Names | `generate=[names="short"]` |
| `generateFirstCheck` | int | `generateFirstCheck` or `generate=[first-check=2]` |
| `generateTokenTypes` | boolean | `generateTokens` or `generate=[tokens="yes"]` |
| `generateTokenSets` | boolean | `generate=[token-sets="yes"]` |
| `generateElementTypes` | boolean | `generate=[elements="yes"]` |
| `generateExactTypes` | String | `generate=[exact-types="all"]` |
| `generateExtendedPin` | boolean | `extendedPin` or `generate=[extended-pin=true]` |
| `generatePsi` | boolean | `generatePsi` or `generate=[psi="yes"]` |
| `generatePsiFactory` | boolean | `generate=[psi-factory="yes"]` |
| `generatePsiClassesMap` | boolean | `generate=[psi-classes-map="yes"]` |
| `generateVisitor` | boolean | `generate=[visitor="yes"]` |
| `visitorValue` | String | `generate=[visitor-value="Val"]` |
| `generateFQN` | boolean | `generate=[fqn="yes"]` |
| `generateTokenCase` | Case | `generate=[token-case="upper"]` |
| `generateElementCase` | Case | `generate=[element-case="upper"]` |
| `generateTokenAccessors` | boolean | `generateTokenAccessors` or `generate=[token-accessors="no"]` |
| `javaVersion` | int | `generate=[java="11"]` |

## 7. Names: Variable Naming Styles

**Source: `src/org/intellij/grammar/generator/Names.java:13-63`**

Three styles controlled by `generate=[names="..."]`:

| Style | builder | level | marker | pinned | result | pos |
|---|---|---|---|---|---|---|
| `short` (default) | `b` | `l` | `m` | `p` | `r` | `c` |
| `long` | `builder` | `level` | `marker` | `pinned` | `result` | `pos` |
| `classic` | `builder_` | `level_` | `marker_` | `pinned_` | `result_` | `pos_` |

## 8. Case: Constant Name Casing

**Source: `src/org/intellij/grammar/generator/Case.java:14-27`**

```java
public enum Case {
    LOWER, UPPER, AS_IS, CAMEL;
    public String apply(String s) {
        return switch (this) {
            case LOWER -> s.toLowerCase(Locale.ENGLISH);
            case UPPER -> s.toUpperCase(Locale.ENGLISH);
            case AS_IS -> s;
            case CAMEL -> s.substring(0, 1).toUpperCase() + s.substring(1).toLowerCase();
        };
    }
}
```

## 9. BnfConstants: Platform Integration Points

**Source: `src/org/intellij/grammar/generator/BnfConstants.java:10-43`**

Key constants used in generation:

| Constant | Value | Usage |
|---|---|---|
| `GPUB_CLASS` | `com.intellij.lang.parser.GeneratedParserUtilBase` | Default parserUtilClass |
| `PSI_BUILDER_CLASS` | `com.intellij.lang.PsiBuilder` | Parser builder |
| `LIGHT_PSI_PARSER_CLASS` | `com.intellij.lang.LightPsiParser` | Light parser interface |
| `IELEMENTTYPE_CLASS` | `com.intellij.psi.tree.IElementType` | Element type base |
| `PSI_ELEMENT_CLASS` | `com.intellij.psi.PsiElement` | PSI base interface |
| `AST_WRAPPER_PSI_ELEMENT_CLASS` | `com.intellij.extapi.psi.ASTWrapperPsiElement` | Default extends class |
| `ISTUBELEMENTTYPE_CLASS` | `com.intellij.psi.stubs.IStubElementType` | Stub element type |
| `STUB_BASED_PSI_ELEMENT_BASE` | `com.intellij.extapi.psi.StubBasedPsiElementBase` | Stub PSI base |
| `RECOVER_AUTO` | `#auto` | Auto-recovery sentinel |
| `TOKEN_SET_HOLDER_NAME` | `TokenSets` | Token sets inner class |
| `CLASS_HEADER_DEF` | `"// This is a generated file..."` | Default file header |

## 10. Expression Parsing Generation

**Source: `HOWTO.md:124-223`**

For expression grammars, the generator produces an optimized Pratt-parser:
- Only 2 methods for the root expression rule: `expr()` and `expr_0()`.
- A priority table comment is generated in the output.
- Operator types: `BINARY`, `N_ARY`, `PREFIX`, `POSTFIX`, `ATOM`.

```java
// Expression root: expr
// Operator priority table:
// 0: BINARY(assign_expr)
// 1: BINARY(plus_expr) BINARY(minus_expr)
// 2: BINARY(mul_expr) BINARY(div_expr)
// 3: PREFIX(unary_plus_expr) PREFIX(unary_min_expr)
// 4: N_ARY(exp_expr)
// 5: POSTFIX(ref_expr)
// 6: ATOM(simple_ref_expr) ATOM(literal_expr) PREFIX(paren_expr)
public static boolean expr(PsiBuilder b, int l, int g) { ... }
public static boolean expr_0(PsiBuilder b, int l, int g) { ... }
```

## 11. Abstract Rules Detection

**Source: `src/org/intellij/grammar/generator/ParserGenerator.java:182-199`**

A rule is marked abstract if:
- Its elementType is not reused by another rule.
- It's not the grammar root.
- It has no modifiers.
- It has no `recoverWhile` attribute.
- It has no `hooks` attribute.
- It can collapse (`canCollapse`) and has no direct children.

Abstract rules get no parsing code generated — they serve only as PSI hierarchy nodes.

## 12. GenerateAction: Target Directory Resolution

**Source: `src/org/intellij/grammar/actions/GenerateAction.java:87-105`**

```java
String parserClass = getRootAttribute(bnfFile, KnownAttribute.PARSER_CLASS);
VirtualFile target = getTargetDirectoryFor(project, file,
    StringUtil.getShortName(parserClass) + ".java",
    StringUtil.getPackageName(parserClass), true);
```

The target directory is resolved from the `parserClass` package name, relative to source roots in the project.
