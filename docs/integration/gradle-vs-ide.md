# Gradle vs IDE Generation

Grammar-Kit offers three ways to generate parser code: from the IDE (Ctrl+Shift+G), from the Gradle plugin, and from the command-line JAR. Each approach makes different trade-offs between feature completeness, automation, and reproducibility. This page helps you choose the right one for your project.

## Feature Comparison

| Feature | IDE (Ctrl+Shift+G) | Gradle Plugin | CLI (grammar-kit.jar) |
|---|---|---|---|
| Two-pass generation | Yes | No | No |
| Method mixins | Yes | No | No |
| Generic signatures | Correct | May be incorrect | May be incorrect |
| Type annotations (ASM) | Yes | Limited | Limited |
| Live Preview | Yes | N/A | N/A |
| Output directory resolution | Automatic (from source roots) | Configured explicitly | Specified on command line |
| Progress reporting | IDE progress bar | Gradle logging | Console output |
| Incremental builds | Partial (VFS refresh) | Gradle up-to-date checks | None |
| CI/CD compatible | No (requires running IDE) | Yes | Yes |
| Reproducible builds | Depends on IDE state | Yes | Yes |

The most significant difference is two-pass generation. The IDE runs the generator in two passes: the first collects type information from the grammar and the project's Java classes, and the second generates code with full knowledge of types, generics, and annotations. This enables method mixins and produces correct generic signatures. The Gradle plugin and CLI run a single pass with limited type information.

## IDE Generation

IDE generation is the recommended approach during active grammar development. It provides the tightest feedback loop: edit the grammar, press Ctrl+Shift+G, and the generator writes files directly into your source tree. The IDE resolves output directories automatically from the `parserClass` attribute using `PackageIndex`, so you do not need to configure paths manually.

The generation runs as a background task with a progress indicator and reports results through a notification showing file count, total size, and duration. After generation, the IDE refreshes its virtual file system so you can immediately use the new code.

IDE generation is also the only way to use Live Preview (Ctrl+Alt+P), which lets you test grammar changes against sample input in real time without regenerating.

!!! note
    Fleet IDE also supports Grammar-Kit generation through context menu actions: "Fleet: Generate Parser Code", "Fleet: Generate JFlex Lexer", and "Fleet: Run JFlex Generator".

## Gradle and CLI Generation

The Gradle plugin and CLI are the right choice when you need automated, reproducible builds. Both produce identical output for the same input grammar, regardless of which machine runs the build. This matters for CI/CD pipelines, team synchronization, and build verification.

The Gradle plugin integrates with Gradle's task dependency and up-to-date checking, so generation runs only when the grammar file changes. The CLI JAR is a simpler option for scripts or build systems other than Gradle. Both use `LightPsi` to create a minimal parsing environment without a running IDE.

The limitations are the same for both: no two-pass generation, no method mixins, and potentially incorrect generic signatures and annotations. If your grammar does not use `mixin` attributes and does not depend on precise generics in the generated code, these limitations may not affect you.

For details on configuring the Gradle plugin, see [Gradle Plugin Setup](gradle-setup.md).

## Choosing an Approach

The right strategy depends on whether your grammar uses method mixins and how your team manages generated code.

If your grammar uses `mixin` attributes, generate from the IDE and commit the generated files to version control. CI compiles the committed sources without running the generator. This gives you correct output from two-pass generation while keeping builds reproducible.

If your grammar does not use mixins, the Gradle plugin works well as the sole generation method. Add `src/main/gen` to `.gitignore` and let every build (local and CI) regenerate from the grammar. This avoids merge conflicts in generated files and guarantees that the committed grammar is the single source of truth.

A hybrid approach works for teams transitioning between methods: generate from the IDE during development for fast feedback and accurate output, then verify in CI that the Gradle plugin produces compilable code. Over time, you can reduce reliance on IDE generation as you remove mixin dependencies.

Whichever approach you choose, keep the grammar file itself in version control and document the generation method in your project's build instructions.
