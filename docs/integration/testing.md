# Testing

Testing a language plugin involves two levels: verifying that the parser produces correct PSI trees from input, and verifying that IDE features like completion, highlighting, and refactoring work against those trees. Grammar-Kit's own test suite demonstrates both levels and provides patterns you can adapt.

## Test Framework Setup

Grammar-Kit uses the IntelliJ Platform test framework. Add the test dependencies in your `build.gradle.kts`:

```kotlin
dependencies {
    intellijPlatform {
        testFramework(TestFrameworkType.Platform)
        testFramework(TestFrameworkType.Plugin.Java)  // if your plugin depends on Java
    }
    testImplementation("junit:junit:4.13.2")
}
```

Configure your source sets so the test runner can find test sources and test data:

```kotlin
sourceSets {
    main { java.srcDirs("src", "gen"); resources.srcDirs("resources") }
    test { java.srcDirs("tests"); resources.srcDirs("testData") }
}
```

Grammar-Kit runs all tests through a single test suite class (`BnfTestSuite`) and disables class scanning. This is optional but gives you explicit control over which tests run and in what order:

```kotlin
tasks.withType<Test> {
    useJUnit()
    include("**/MyTestSuite.class")
    isScanForTestClasses = false
}
```

## Parser and Generator Tests

Parser tests verify that your grammar produces the expected PSI tree for given input. Generator tests verify that the code generator produces the expected Java source files from a grammar.

Grammar-Kit organizes test data with a naming convention. Each test case has a `.bnf` grammar file paired with expected output files:

```
testData/
  generator/
    ExprParser.bnf
    ExprParser.expected.java
    ExprParser.PSI.expected.java
  livePreview/
    Json.bnf
    JsonRecovery.txt
    JsonRecovery.live.txt
```

Generator tests follow a straightforward pattern: parse a `.bnf` file, run `ParserGenerator.generate()`, and compare the output against `.expected.java` golden files. PSI class output is compared against `.PSI.expected.java` files. When the generated output changes intentionally, update the golden files and commit them alongside the grammar change.

For parser tests, the convention pairs a grammar with `.txt` input files and `.live.txt` files for Live Preview comparisons. The test parses the input, serializes the resulting PSI tree, and compares it against the expected output.

!!! tip
    Use `LightPsi.parseFile()` for fast parser tests that do not need the full IDE environment. It creates a minimal IntelliJ context sufficient for parsing and PSI construction without starting the platform.

```java
PsiFile file = LightPsi.parseFile("test.bnf", grammarText, new BnfParserDefinition());
// assert on the resulting PSI tree
```

## Feature Tests

Feature tests verify IDE functionality that depends on the PSI tree: completion, highlighting, inspections, refactoring, and navigation. These tests require the full platform fixture because they interact with the editor, caret positioning, and project services.

Grammar-Kit's test suite splits into two tiers:

Fast tests (no IDE fixture needed) cover parsing, generation, and utility functions. These include `BnfParserTest`, `BnfGeneratorTest`, `ExpressionParserTest`, `JFlexParserTest`, `JFlexGenerationTest`, and `BnfLivePreviewParserTest`.

Full tests (require IDE fixture) cover features that interact with the editor and project model. These include `BnfCompletionTest`, `BnfHighlightingTest`, `BnfInlineRuleTest`, `BnfIntroduceRuleTest`, `BnfFlipChoiceIntentionTest`, `BnfMoveLeftRightTest`, `BnfFirstNextTest`, and `BnfRuleGraphTest`.

For your own language plugin, extend the appropriate base test class from the IntelliJ test framework (`BasePlatformTestCase` or `LightPlatformCodeInsightFixtureTestCase`) and configure the test data path. Typical feature test patterns:

- Completion tests call `myFixture.completeBasic()` and assert on the lookup element list.
- Highlighting tests call `myFixture.checkHighlighting()` with annotated test files.
- Refactoring tests invoke the refactoring action and compare the result against a golden file.
- Inspection tests enable the inspection on the fixture and check that expected warnings appear.

## Debugging and Troubleshooting

When a test fails, start by examining the PSI tree. The `PsiFile` returned by parsing has a `getText()` method and can be printed as a tree structure for comparison. For generator tests, diff the actual output against the expected file to see exactly what changed.

For feature tests running in the full fixture, enable the PSI Viewer (**Tools > View PSI Structure**) in a development IDE instance to inspect the tree visually. Set breakpoints in your parser methods or `ParserDefinition` to trace how tokens flow through the system.

Common issues and their causes:

- Tests pass locally but fail in CI: check that `testData/` is included as a test resource directory and that file paths are platform-independent.
- PSI tree mismatches after grammar changes: regenerate the parser and update golden files.
- Feature tests throw "no language registered": verify that your test class calls `super.setUp()` and that `plugin.xml` is on the test classpath.

For details on setting up Gradle-based builds that run these tests in CI, see [Gradle Plugin Setup](gradle-setup.md).
