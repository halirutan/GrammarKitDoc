# Section 4.1.3: Testing — Code Evidence

## 1. Test Suite Structure

**Source: `tests/org/intellij/grammar/BnfTestSuite.java:21-54`**

Two test tiers:

### Fast Tests (no IDE features needed)
- `BnfUtilTest` — utility function tests
- `JFlexGenerationTest` — JFlex generation tests
- `JFlexParserTest` — JFlex parser tests
- `BnfParserTest` — BNF parser tests
- `BnfGeneratorTest` — parser code generation tests
- `FleetBnfGeneratorTest` — Fleet-specific generation
- `ExpressionParserTest` — expression parsing tests
- `BnfLivePreviewParserTest` — Live Preview parser tests

### Full Tests (require IDE fixture)
- `BnfFirstNextTest` — FIRST/NEXT set analysis
- `BnfRuleGraphTest` — rule graph analysis
- `BnfCompletionTest` — code completion tests
- `BnfHighlightingTest` — highlighting and inspections
- `BnfInlineRuleTest` — inline rule refactoring
- `BnfIntroduceRuleTest` — introduce rule refactoring
- `BnfFlipChoiceIntentionTest` — flip choice intention
- `BnfMoveLeftRightTest` — move left/right tests
- `BnfConvertOptExpressionIntentionTest` — convert optional intention
- `JFlexCompletionTest` — JFlex completion

## 2. Test Configuration

**Source: `build.gradle.kts:155-160`**

```kotlin
withType<Test> {
    useJUnit()
    include("**/BnfTestSuite.class")
    isScanForTestClasses = false
    ignoreFailures = true
}
```

Tests run through `BnfTestSuite` entry point. The `isScanForTestClasses = false` means only the explicitly included suite is executed.

## 3. Test Data Organization

**Source: `testData/` directory structure**

```
testData/
  generator/         # Parser generation golden files
    ExprParser.bnf / ExprParser.expected.java / ExprParser.PSI.expected.java
    PsiGen.bnf / PsiGen.expected.java / PsiGen.PSI.expected.java
    Stub.bnf / Stub.expected.java / Stub.PSI.expected.java
    ... (29 .bnf files with corresponding .expected.java files)
  livePreview/       # Live Preview test grammars
    Json.bnf / JsonRecovery.live.txt / JsonRecovery.txt
    LivePreviewTutorial.bnf
    AutoRecovery.bnf / AutoRecovery.live.txt / AutoRecovery.txt
    ... (9 .bnf files with paired .txt and .live.txt files)
```

Pattern: `<Name>.bnf` + `<Name>.expected.java` for generator tests; `<Name>.bnf` + `<Name>.txt` + `<Name>.live.txt` for parser/live preview tests.

## 4. Generator Test Pattern

**Source: `tests/org/intellij/grammar/BnfGeneratorTestCase.java` (test base class)**

Generator tests:
1. Parse a `.bnf` file
2. Run `ParserGenerator.generate()`
3. Compare generated output against `.expected.java` golden files
4. PSI class generation compared against `.PSI.expected.java`

## 5. LightPsi for Standalone Testing

**Source: `src/org/intellij/grammar/LightPsi.java:49-82`**

`LightPsi` provides a minimal IntelliJ environment for parsing:
```java
public static @Nullable PsiFile parseFile(@NotNull String name, @NotNull String text, @NotNull ParserDefinition parserDefinition)
public static @NotNull ASTNode parseText(@NotNull String text, @NotNull ParserDefinition parserDefinition)
```

Creates a `CoreApplicationEnvironment` and `CoreProjectEnvironment` with minimal extensions. Registers `CachesBasedRefSearcher`, `PsiSearchHelper`, and `JavaHelper` (ASM or reflection).

## 6. Expression Parser Test

**Source: `tests/org/intellij/grammar/expression/ExpressionParserTest.java`**

Tests the expression parser from `ExprParser.bnf` against real input, verifying PSI tree structure, operator precedence, and associativity.

## 7. Test Framework Dependencies

**Source: `build.gradle.kts:40-42`**

```kotlin
intellijPlatform {
    testFramework(TestFrameworkType.Platform)
    testFramework(TestFrameworkType.Plugin.Java)
}
```

Uses IntelliJ Platform test framework and Java plugin test support.

## 8. Source Organization

**Source: `build.gradle.kts:45-54`**

```kotlin
sourceSets {
    main { java.srcDirs("src", "gen"); resources.srcDirs("resources") }
    test { java.srcDirs("tests"); resources.srcDirs("testData") }
}
```

Test sources in `tests/`, test data in `testData/` (treated as resources).
